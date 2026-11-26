#!/usr/bin/env python3
"""
Lean publish + cleanup loop for Motion Index:
  1. Validate data/packs/apps-*.json and rebuild index.html + data/motions.json + data/motions-bundle.js
  2. Commit and push changes to GitHub (origin main)
  3. Deploy live to the linked Netlify site
  4. Delete local temporary recordings/frames in .cache/captures/ (and optionally uninstall captured APKs from emulator)

Example:
  python3 scripts/publish_and_clean.py -m "Add Spotify & Strava live-captured motions" --uninstall com.spotify.music com.strava
"""
import argparse
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAPTURES_DIR = ROOT / ".cache" / "captures"
SDK_ROOT = pathlib.Path(os.environ.get("ANDROID_HOME", pathlib.Path.home() / "Library" / "Android" / "sdk"))
ADB = str(SDK_ROOT / "platform-tools" / "adb")


def run(cmd: list[str], env: dict | None = None, check: bool = True) -> subprocess.CompletedProcess:
    print("+", " ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT, env=env, check=check)


def main() -> int:
    p = argparse.ArgumentParser(description="Rebuild, push to GitHub, deploy to Netlify, and clean local captures.")
    p.add_argument("-m", "--message", default="Update Motion Index apps database")
    p.add_argument("--keep-captures", action="store_true", help="Do not delete .cache/captures/")
    p.add_argument("--uninstall", nargs="*", default=[], help="Android package IDs to uninstall from emulator after publish")
    p.add_argument("--serial", default="emulator-5554")
    args = p.parse_args()

    # 1. Validate app packs and rebuild site
    for pack in sorted((ROOT / "data" / "packs").glob("apps-*.json")):
        run([sys.executable, "scripts/extract_app_motion.py", "validate", str(pack)])
    run([sys.executable, "scripts/build_site.py"])

    # 2. Commit & push to GitHub
    run(["git", "add", "index.html", "data", "scripts", "netlify.toml", ".gitignore"])
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if diff.returncode != 0:
        run(["git", "commit", "-m", args.message])
        run(["git", "push", "origin", "main"])
    else:
        print("No git changes to commit.")

    # 3. Deploy live to Netlify
    env = os.environ.copy()
    env["CI"] = "1"
    run(["netlify", "deploy", "--prod", "--dir=.", "--message", args.message], env=env)

    # 4. Clean up local captures on laptop
    if not args.keep_captures and CAPTURES_DIR.exists():
        size_bytes = sum(f.stat().st_size for f in CAPTURES_DIR.rglob("*") if f.is_file())
        shutil.rmtree(CAPTURES_DIR)
        print(f"Cleaned {CAPTURES_DIR} (freed {size_bytes / (1024 * 1024):.1f} MB)")

    # 5. Optional: uninstall captured APKs from emulator to keep AVD disk small
    if args.uninstall and pathlib.Path(ADB).exists():
        for pkg in args.uninstall:
            subprocess.run([ADB, "-s", args.serial, "uninstall", pkg], check=False)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
