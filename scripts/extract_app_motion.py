#!/usr/bin/env python3
"""
Route 2 CLI: Public App Store lookup, preview video downloader, ffmpeg motion
slicer + contact-sheet generator, and Motion Index pack ingestion helper.

Examples:
  python3 scripts/extract_app_motion.py lookup "Duolingo" --download-previews
  python3 scripts/extract_app_motion.py slice .cache/captures/duolingo/preview-1.mp4 --app duolingo --motion progress-surge
  python3 scripts/extract_app_motion.py validate data/packs/apps-featured.json
"""
import argparse
import json
import math
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache" / "captures"
PACKS_DIR = ROOT / "data" / "packs"


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "app"


def fetch_json(url: str, timeout: int = 15) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15"
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_text(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def discover_app_store_previews(store_url: str) -> list[str]:
    """Best-effort extraction of public App Preview video URLs (.m3u8 / .mp4) from an App Store page."""
    try:
        html = fetch_text(store_url)
    except Exception as exc:
        print(f"Warning: could not fetch App Store page ({exc})", file=sys.stderr)
        return []

    found = []
    patterns = [
        r'https://[^\s"\'\\]+?\.m3u8(?:\?[^\s"\'\\]+)?',
        r'https://[^\s"\'\\]+?video[^\s"\'\\]*?\.mp4(?:\?[^\s"\'\\]+)?',
        r'https://video-ssl\.itunes\.apple\.com/[^\s"\'\\]+',
        r'https://[^\s"\'\\]+?mzstatic\.com/[^\s"\'\\]+?\.(?:m3u8|mp4|mov)',
    ]
    for pat in patterns:
        for match in re.findall(pat, html):
            clean = match.replace("\\u002F", "/").replace("\\/", "/")
            if clean not in found:
                found.append(clean)
    return found


def cmd_lookup(args: argparse.Namespace) -> int:
    params = {
        "term": args.query,
        "entity": "software",
        "limit": args.limit,
        "country": args.country,
    }
    url = "https://itunes.apple.com/search?" + urllib.parse.urlencode(params)
    data = fetch_json(url)
    results = data.get("results", [])
    if not results:
        print(f"No App Store results found for {args.query!r}", file=sys.stderr)
        return 1

    app = results[0]
    short_name = app.get("trackName", args.query).split(":")[0].split("–")[0].split("-")[0].strip()
    slug = args.slug or slugify(short_name)
    out_dir = CACHE_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    previews = discover_app_store_previews(app.get("trackViewUrl", ""))
    record = {
        "name": short_name,
        "fullName": app.get("trackName", short_name),
        "slug": slug,
        "trackId": app.get("trackId"),
        "bundleId": app.get("bundleId", ""),
        "seller": app.get("sellerName", ""),
        "category": app.get("primaryGenreName", "Utilities"),
        "platform": ["iOS"],
        "iconUrl": app.get("artworkUrl512") or app.get("artworkUrl100", ""),
        "storeUrl": app.get("trackViewUrl", ""),
        "screenshots": app.get("screenshotUrls", [])[:6],
        "previewUrls": previews[:4],
    }

    meta_path = out_dir / "app.json"
    meta_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved app metadata -> {meta_path}")
    print(json.dumps({k: record[k] for k in ("name", "bundleId", "category", "storeUrl", "previewUrls")}, indent=2))

    if args.download_previews and previews:
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            print("ffmpeg not found in PATH; skipping preview download.", file=sys.stderr)
            return 0
        for idx, purl in enumerate(previews[: args.max_previews], start=1):
            dest = out_dir / f"preview-{idx}.mp4"
            print(f"Downloading preview {idx} -> {dest}")
            proc = subprocess.run(
                [ffmpeg, "-y", "-loglevel", "error", "-i", purl, "-c", "copy", str(dest)],
                capture_output=True,
                text=True,
            )
            if proc.returncode != 0:
                # Re-encode fallback for HLS streams that disallow stream copy into MP4
                proc = subprocess.run(
                    [
                        ffmpeg, "-y", "-loglevel", "error",
                        "-i", purl,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                        "-pix_fmt", "yuv420p", "-an",
                        str(dest),
                    ],
                    capture_output=True,
                    text=True,
                )
            if proc.returncode == 0 and dest.exists():
                print(f"  OK ({dest.stat().st_size:,} B)")
            else:
                print(f"  Skipped preview {idx}: {proc.stderr.strip()}", file=sys.stderr)
    elif args.download_previews:
        print("No public App Preview video streams found on the App Store page (common for apps that only publish static screenshots).")

    return 0


def probe_video(video_path: pathlib.Path) -> dict:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe not found in PATH")
    proc = subprocess.run(
        [
            ffprobe,
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,nb_frames,duration",
            "-show_entries", "format=duration",
            "-of", "json",
            str(video_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    raw = json.loads(proc.stdout)
    stream = (raw.get("streams") or [{}])[0]
    fmt = raw.get("format") or {}
    rfr = stream.get("r_frame_rate", "30/1")
    num, den = (int(x) for x in rfr.split("/")) if "/" in rfr else (int(rfr), 1)
    fps = round(num / max(1, den), 2)
    duration = float(stream.get("duration") or fmt.get("duration") or 0.0)
    return {
        "width": int(stream.get("width") or 0),
        "height": int(stream.get("height") or 0),
        "fps": fps,
        "durationSec": round(duration, 3),
        "durationMs": int(round(duration * 1000)),
    }


def detect_motion_activity(video_path: pathlib.Path, start: float, duration: float) -> list[dict]:
    """Compute per-frame luminance delta via ffmpeg raw gray stream (32x32) to locate motion start, peak, and settle."""
    ffmpeg = shutil.which("ffmpeg")
    cmd = [ffmpeg, "-v", "error"]
    if start > 0:
        cmd += ["-ss", str(start)]
    cmd += ["-i", str(video_path)]
    if duration > 0:
        cmd += ["-t", str(duration)]
    cmd += ["-vf", "fps=30,scale=32:32,format=gray", "-f", "rawvideo", "pipe:1"]

    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        return []
    buf = proc.stdout
    frame_size = 32 * 32
    n_frames = len(buf) // frame_size
    if n_frames < 2:
        return []

    energies = []
    prev = buf[0:frame_size]
    for i in range(1, n_frames):
        cur = buf[i * frame_size : (i + 1) * frame_size]
        diff = sum(abs(a - b) for a, b in zip(prev, cur)) / (frame_size * 255.0)
        energies.append({"tMs": int(round((i / 30.0) * 1000)), "energy": round(diff, 5)})
        prev = cur
    return energies


def summarize_motion_window(energies: list[dict]) -> dict:
    if not energies:
        return {}
    peak = max(energies, key=lambda x: x["energy"])
    threshold = max(0.004, peak["energy"] * 0.12)
    active = [e for e in energies if e["energy"] >= threshold]
    if not active:
        return {"peakMs": peak["tMs"], "peakEnergy": peak["energy"]}
    start_ms = active[0]["tMs"]
    end_ms = active[-1]["tMs"]
    return {
        "motionStartMs": start_ms,
        "motionPeakMs": peak["tMs"],
        "motionEndMs": end_ms,
        "estimatedDurationMs": max(120, end_ms - start_ms),
        "peakEnergy": peak["energy"],
        "peakRatio": round((peak["tMs"] - start_ms) / max(1, end_ms - start_ms), 2),
    }


def cmd_slice(args: argparse.Namespace) -> int:
    video = pathlib.Path(args.video).expanduser().resolve()
    if not video.exists():
        print(f"Video not found: {video}", file=sys.stderr)
        return 1

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("ffmpeg is required in PATH.", file=sys.stderr)
        return 1

    app_slug = slugify(args.app)
    motion_slug = slugify(args.motion)
    out_dir = CACHE_DIR / app_slug / motion_slug
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    info = probe_video(video)
    energies = detect_motion_activity(video, args.start, args.duration)
    window = summarize_motion_window(energies)

    # Extract individual keyframes for detailed inspection
    frame_cmd = [ffmpeg, "-y", "-loglevel", "error"]
    if args.start > 0:
        frame_cmd += ["-ss", str(args.start)]
    frame_cmd += ["-i", str(video)]
    if args.duration > 0:
        frame_cmd += ["-t", str(args.duration)]
    frame_cmd += [
        "-vf", f"fps={args.fps},scale=360:-2",
        str(frames_dir / "frame-%04d.png"),
    ]
    subprocess.run(frame_cmd, check=True)
    frame_files = sorted(frames_dir.glob("frame-*.png"))

    # Build a compact 5-column contact sheet (up to 20 frames)
    sample_count = min(20, max(1, len(frame_files)))
    cols = min(5, sample_count)
    rows = math.ceil(sample_count / cols)
    contact_sheet = out_dir / "contact-sheet.png"

    sheet_fps = args.fps
    if len(frame_files) > 20 and info["durationSec"] > 0:
        span = args.duration if args.duration > 0 else max(0.2, info["durationSec"] - args.start)
        sheet_fps = round(20.0 / span, 3)

    sheet_cmd = [ffmpeg, "-y", "-loglevel", "error"]
    if args.start > 0:
        sheet_cmd += ["-ss", str(args.start)]
    sheet_cmd += ["-i", str(video)]
    if args.duration > 0:
        sheet_cmd += ["-t", str(args.duration)]
    sheet_cmd += [
        "-vf", f"fps={sheet_fps},scale=240:-2,tile={cols}x{rows}:padding=6:margin=8:color=0x101114",
        "-frames:v", "1",
        str(contact_sheet),
    ]
    subprocess.run(sheet_cmd, check=True)

    # Load cached app metadata if available
    app_meta_path = CACHE_DIR / app_slug / "app.json"
    app_meta = json.loads(app_meta_path.read_text(encoding="utf-8")) if app_meta_path.exists() else {
        "name": args.app.replace("-", " ").title(),
        "slug": app_slug,
        "category": "App",
        "platform": ["iOS", "Android"],
        "storeUrl": "",
        "bundleId": "",
    }

    draft = {
        "id": f"app-{app_slug}-{motion_slug}",
        "title": f"{app_meta['name']}: {args.motion.replace('-', ' ').title()}",
        "use": "Micro-interactions",
        "stack": "CSS",
        "trigger": "Click",
        "feel": "Tactile",
        "surface": "dark",
        "dur": window.get("estimatedDurationMs", min(900, info["durationMs"] or 420)),
        "ease": {"t": "spring", "k": 320, "c": 24},
        "easeLabel": "spring(320, 24)",
        "props": ["transform: translate + scale", "opacity"],
        "src": app_meta["name"],
        "srcUrl": app_meta.get("storeUrl", ""),
        "collection": "Apps",
        "app": {
            "name": app_meta["name"],
            "slug": app_slug,
            "category": app_meta.get("category", "App"),
            "platform": app_meta.get("platform", ["iOS", "Android"]),
            "accent": app_meta.get("accent", "#2a94e2"),
            "iconUrl": app_meta.get("iconUrl", ""),
            "storeUrl": app_meta.get("storeUrl", ""),
            "bundleId": app_meta.get("bundleId", ""),
        },
        "summary": "TODO: Describe the observed motion choreography from contact-sheet.png.",
        "hint": "Click to replay",
        "choreography": [
            f"0-{window.get('motionPeakMs', 140)}ms: TODO describe initial impulse / peak velocity.",
            f"{window.get('motionPeakMs', 140)}-{window.get('estimatedDurationMs', 420)}ms: TODO describe settle / overshoot."
        ],
        "agentPrompt": "TODO: Reverse-engineered engineering prompt specifying spring/bezier curves, transforms, stagger delays, and interaction triggers.",
        "extractableCode": "<!-- TODO: Clean standalone interactive HTML/CSS/JS reconstruction -->",
        "html": "",
        "css": "",
        "js": "",
        "_analysis": {
            "sourceVideo": str(video),
            "videoInfo": info,
            "motionWindow": window,
            "frameCount": len(frame_files),
            "contactSheet": str(contact_sheet),
        },
    }

    draft_path = out_dir / "motion-draft.json"
    draft_path.write_text(json.dumps(draft, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Extracted {len(frame_files)} frames -> {frames_dir}")
    print(f"Contact sheet -> {contact_sheet}")
    print(f"Motion window -> {json.dumps(window)}")
    print(f"Draft spec    -> {draft_path}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.pack).resolve()
    items = json.loads(path.read_text(encoding="utf-8"))
    required = ["id", "title", "use", "stack", "trigger", "dur", "ease", "easeLabel", "props", "src", "collection", "summary", "choreography", "agentPrompt", "extractableCode", "html"]
    errors = []
    seen = set()
    for idx, m in enumerate(items):
        mid = m.get("id", f"<index {idx}>")
        if mid in seen:
            errors.append(f"Duplicate id: {mid}")
        seen.add(mid)
        for key in required:
            if key not in m or m[key] in (None, ""):
                errors.append(f"{mid}: missing required field '{key}'")
        if m.get("collection") == "Apps" and not isinstance(m.get("app"), dict):
            errors.append(f"{mid}: collection='Apps' requires an 'app' metadata object")
    if errors:
        print("Validation FAILED:", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        return 1
    print(f"Validation OK: {len(items)} motions in {path.name}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Extract and analyze app motions for Motion Index.")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_lookup = sub.add_parser("lookup", help="Fetch public App Store metadata & optional preview videos")
    p_lookup.add_argument("query", help="App name to look up (e.g. 'Duolingo')")
    p_lookup.add_argument("--country", default="us")
    p_lookup.add_argument("--limit", type=int, default=1)
    p_lookup.add_argument("--slug", default="")
    p_lookup.add_argument("--download-previews", action="store_true")
    p_lookup.add_argument("--max-previews", type=int, default=2)
    p_lookup.set_defaults(func=cmd_lookup)

    p_slice = sub.add_parser("slice", help="Slice a captured video into keyframes, contact sheet & motion-draft.json")
    p_slice.add_argument("video", help="Path to .mp4 / .mov recording")
    p_slice.add_argument("--app", required=True, help="App slug (e.g. duolingo)")
    p_slice.add_argument("--motion", required=True, help="Motion slug (e.g. streak-pop)")
    p_slice.add_argument("--fps", type=float, default=15.0)
    p_slice.add_argument("--start", type=float, default=0.0, help="Start offset in seconds")
    p_slice.add_argument("--duration", type=float, default=0.0, help="Clip duration in seconds (0 = full)")
    p_slice.set_defaults(func=cmd_slice)

    p_val = sub.add_parser("validate", help="Validate a motion pack JSON file")
    p_val.add_argument("pack", help="Path to data/packs/*.json")
    p_val.set_defaults(func=cmd_validate)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
