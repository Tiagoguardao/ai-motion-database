#!/usr/bin/env python3
"""
Route 1 CLI: Android Play Store emulator capture helper.

Sets up and manages the dedicated `motion-capture-playstore` ARM64 AVD,
opens Play Store listings one by one from a curated queue, lists installed
apps, pulls 60fps screen recordings, and chains them into extract_app_motion.py.

Examples:
  python3 scripts/android_capture.py status
  python3 scripts/android_capture.py queue
  python3 scripts/android_capture.py play duolingo
  python3 scripts/android_capture.py record --app duolingo --motion streak-flame --duration 10
"""
import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache" / "captures"
SDK_ROOT = pathlib.Path(os.environ.get("ANDROID_HOME", pathlib.Path.home() / "Library" / "Android" / "sdk"))
ADB = str(SDK_ROOT / "platform-tools" / "adb")
AVDMANAGER = str(SDK_ROOT / "cmdline-tools" / "latest" / "bin" / "avdmanager")
SDKMANAGER = str(SDK_ROOT / "cmdline-tools" / "latest" / "bin" / "sdkmanager")
AVD_NAME = "motion-capture-playstore"
SYSTEM_IMAGE = "system-images;android-36;google_apis_playstore;arm64-v8a"

APP_QUEUE = [
    {"slug": "duolingo", "name": "Duolingo", "package": "com.duolingo", "notes": "Lesson progress surge, streak flame burst, XP celebration"},
    {"slug": "spotify", "name": "Spotify", "package": "com.spotify.music", "notes": "Mini-player expand, canvas crossfade, heart pop"},
    {"slug": "airbnb", "name": "Airbnb", "package": "com.airbnb.android", "notes": "Category tab glide, listing card sheet, wishlist heart"},
    {"slug": "notion", "name": "Notion", "package": "notion.id", "notes": "Slash menu reveal, toggle chevron cascade, drag handle"},
    {"slug": "linear", "name": "Linear", "package": "com.linear", "notes": "Command menu snap, status pill morph, swipe triage"},
    {"slug": "revolut", "name": "Revolut", "package": "com.revolut.revolut", "notes": "Balance odometer roll, card flip, currency swap"},
    {"slug": "headspace", "name": "Headspace", "package": "com.getsomeheadspace.android", "notes": "Breathing orb cadence, session completion bloom"},
    {"slug": "strava", "name": "Strava", "package": "com.strava", "notes": "Route trace draw, kudos thumb burst, record hold"},
    {"slug": "slack", "name": "Slack", "package": "com.Slack", "notes": "Reaction pill spring, channel drawer drag, unread jump"},
    {"slug": "stripe", "name": "Stripe Dashboard", "package": "com.stripe.android.dashboard", "notes": "Live revenue tick, payout confirm morph"},
]


def run(cmd: list[str], check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def get_running_devices() -> list[str]:
    if not pathlib.Path(ADB).exists():
        return []
    res = run([ADB, "devices"])
    devices = []
    for line in res.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices


def cmd_status(_args: argparse.Namespace) -> int:
    avd_dir = pathlib.Path.home() / ".android" / "avd" / f"{AVD_NAME}.avd"
    img_dir = SDK_ROOT / "system-images" / "android-36" / "google_apis_playstore" / "arm64-v8a"
    devices = get_running_devices()
    print(f"Android SDK:        {SDK_ROOT}")
    print(f"Play Store image:   {'INSTALLED' if img_dir.exists() else 'NOT INSTALLED'} ({SYSTEM_IMAGE})")
    print(f"Dedicated AVD:      {'READY' if avd_dir.exists() else 'NOT CREATED'} ({AVD_NAME})")
    print(f"Running emulators:  {', '.join(devices) if devices else 'none'}")
    if devices:
        pkgs = run([ADB, "-s", devices[0], "shell", "pm", "list", "packages", "-3"]).stdout.splitlines()
        print(f"Installed 3rd-party apps on {devices[0]}: {len(pkgs)}")
    return 0


def cmd_queue(_args: argparse.Namespace) -> int:
    devices = get_running_devices()
    installed = set()
    if devices:
        out = run([ADB, "-s", devices[0], "shell", "pm", "list", "packages", "-3"]).stdout
        installed = {line.replace("package:", "").strip() for line in out.splitlines() if line.startswith("package:")}
    print(f"{'SLUG':<12} {'STATUS':<11} {'PACKAGE':<34} SIGNATURE MOTIONS")
    print("-" * 96)
    for app in APP_QUEUE:
        st = "installed" if app["package"] in installed else "pending"
        print(f"{app['slug']:<12} {st:<11} {app['package']:<34} {app['notes']}")
    return 0


def cmd_play(args: argparse.Namespace) -> int:
    devices = get_running_devices()
    if not devices:
        print(f"No running Android emulator found. Boot '{AVD_NAME}' via T3 Device panel (device_open) first.", file=sys.stderr)
        return 1
    serial = args.serial or devices[0]
    by_slug = {a["slug"]: a["package"] for a in APP_QUEUE}
    target = args.target
    if target in by_slug:
        uri = f"market://details?id={by_slug[target]}"
    elif "." in target:
        uri = f"market://details?id={target}"
    else:
        uri = f"market://search?q={target}&c=apps"
    print(f"Opening Play Store URI on {serial}: {uri}")
    res = run([ADB, "-s", serial, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", uri])
    if res.returncode != 0:
        print(res.stderr, file=sys.stderr)
        return res.returncode
    print("Opened Play Store listing. Tap Install (after signing into your burner Google account).")
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    ad = args.agent_device
    by_slug = {a["slug"]: a["package"] for a in APP_QUEUE}
    pkg = by_slug.get(args.target, args.target)
    uri = f"market://details?id={pkg}"
    print(f"Opening Play Store listing for {pkg} ...")
    run([ad, "open", "com.android.vending", uri], check=True)
    time.sleep(3)
    snap = run([ad, "snapshot", "-i"], check=True).stdout
    m = re.search(r"(@e\d+)\s+\[(?:button|group)\]\s+\"Install\"", snap)
    if not m:
        print(f"No Install button found for {pkg} (already installed or unavailable).")
        return 0
    ref = m.group(1)
    run([ad, "press", ref, "--settle"], check=True)
    print(f"Queued install for {pkg} via {ref}.")
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    devices = get_running_devices()
    if not devices:
        print(f"No running Android emulator found. Boot '{AVD_NAME}' first.", file=sys.stderr)
        return 1
    serial = args.serial or devices[0]
    out_dir = CACHE_DIR / args.app
    out_dir.mkdir(parents=True, exist_ok=True)
    local_mp4 = out_dir / f"{args.motion}.mp4"
    remote_mp4 = f"/sdcard/motion_{args.app}_{args.motion}.mp4"

    print(f"Recording {args.duration}s from {serial} -> {local_mp4} ...")
    rec = subprocess.run([
        ADB, "-s", serial, "shell", "screenrecord",
        "--bit-rate", str(args.bitrate),
        "--time-limit", str(args.duration),
        remote_mp4,
    ])
    if rec.returncode != 0:
        print("screenrecord failed.", file=sys.stderr)
        return rec.returncode

    run([ADB, "-s", serial, "pull", remote_mp4, str(local_mp4)], check=True)
    run([ADB, "-s", serial, "shell", "rm", "-f", remote_mp4])
    print(f"Saved recording -> {local_mp4} ({local_mp4.stat().st_size:,} B)")

    if not args.no_slice:
        extractor = ROOT / "scripts" / "extract_app_motion.py"
        subprocess.run(
            [sys.executable, str(extractor), "slice", str(local_mp4), "--app", args.app, "--motion", args.motion],
            check=True,
        )
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Android Play Store emulator capture pipeline.")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_st = sub.add_parser("status", help="Show Play Store image, AVD, and running emulator status")
    p_st.set_defaults(func=cmd_status)

    p_q = sub.add_parser("queue", help="List curated target apps and install status")
    p_q.set_defaults(func=cmd_queue)

    p_play = sub.add_parser("play", help="Open an app's Google Play Store listing on the emulator")
    p_play.add_argument("target", help="Queue slug (e.g. duolingo), package ID, or search query")
    p_play.add_argument("--serial", default="")
    p_play.set_defaults(func=cmd_play)

    p_rec = sub.add_parser("record", help="Record an interaction clip from the emulator and slice it")
    p_rec.add_argument("--app", required=True)
    p_rec.add_argument("--motion", required=True)
    p_rec.add_argument("--duration", type=int, default=8)
    p_rec.add_argument("--bitrate", type=int, default=12000000)
    p_rec.add_argument("--serial", default="")
    p_rec.add_argument("--no-slice", action="store_true")
    p_rec.set_defaults(func=cmd_record)

    p_inst = sub.add_parser("install", help="Install an app from Play Store via agent-device")
    p_inst.add_argument("target", help="Queue slug (e.g. duolingo) or Android package ID")
    p_inst.add_argument("--agent-device", required=True, help="Path to bound agent-device binary from device_open")
    p_inst.set_defaults(func=cmd_install)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
