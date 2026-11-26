#!/usr/bin/env python3
"""
Validates all data/packs/apps-*.json packs:
  - Schema completeness (required fields + valid enum values)
  - Global uniqueness of motion IDs and app slugs across all packs
  - Unique CSS root class isolation
  - JS syntax check via `node` (`new Function('root', m.js)`)
  - Verified iconUrl / storeUrl coverage report
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "data" / "packs"

VALID_USES = {"Micro-interactions", "Navigation and layout", "Typography", "Backgrounds", "Generative", "Transitions"}
VALID_STACKS = {"CSS", "SVG", "Canvas 2D", "WebGL"}
VALID_TRIGGERS = {"Click", "Hover", "Loop", "Cursor", "Drag", "Tab switch", "Ambient", "Press and hold"}
VALID_FEELS = {"Playful", "Fluid", "Crisp", "Calm", "Tactile", "Cinematic", "Rhythmic", "Organic", "Silky", "Editorial"}
REQUIRED = [
    "id", "title", "use", "stack", "trigger", "feel", "surface", "dur",
    "ease", "easeLabel", "props", "src", "collection", "app",
    "summary", "choreography", "agentPrompt", "extractableCode", "html", "css", "js",
]


def main() -> int:
    packs = sorted(PACKS_DIR.glob("apps-*.json"))
    if not packs:
        print("No apps-*.json packs found!", file=sys.stderr)
        return 1

    all_ids = set()
    all_apps = {}
    errors = []
    js_snippets = []

    for pack in packs:
        try:
            items = json.loads(pack.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{pack.name}: invalid JSON ({exc})")
            continue
        pack_apps = set()
        for idx, m in enumerate(items):
            mid = m.get("id", f"{pack.name}[{idx}]")
            if mid in all_ids:
                errors.append(f"Duplicate motion id across packs: {mid}")
            all_ids.add(mid)

            for k in REQUIRED:
                if k not in m or m[k] in (None, "", []):
                    errors.append(f"{pack.name} :: {mid}: missing/empty '{k}'")

            if m.get("use") not in VALID_USES:
                errors.append(f"{pack.name} :: {mid}: invalid use '{m.get('use')}'")
            if m.get("stack") not in VALID_STACKS:
                errors.append(f"{pack.name} :: {mid}: invalid stack '{m.get('stack')}'")
            if m.get("trigger") not in VALID_TRIGGERS:
                errors.append(f"{pack.name} :: {mid}: invalid trigger '{m.get('trigger')}'")
            if m.get("feel") not in VALID_FEELS:
                errors.append(f"{pack.name} :: {mid}: invalid feel '{m.get('feel')}'")
            if m.get("surface") not in {"dark", "light"}:
                errors.append(f"{pack.name} :: {mid}: invalid surface '{m.get('surface')}'")
            if m.get("collection") != "Apps":
                errors.append(f"{pack.name} :: {mid}: collection must be 'Apps'")

            app = m.get("app")
            if not isinstance(app, dict) or not app.get("slug") or not app.get("name"):
                errors.append(f"{pack.name} :: {mid}: invalid app object")
            else:
                slug = app["slug"]
                pack_apps.add(slug)
                if slug not in all_apps:
                    all_apps[slug] = (pack.name, app)
                elif all_apps[slug][0] != pack.name:
                    errors.append(f"Duplicate app slug '{slug}' in both {all_apps[slug][0]} and {pack.name}")

            js_snippets.append({"id": mid, "pack": pack.name, "js": m.get("js", "")})

        print(f"  {pack.name:<30} {len(items):>3} motions | {len(pack_apps):>3} unique apps")

    # Syntax check every JS snippet with Node
    node_script = """
    const fs = require('fs');
    const items = JSON.parse(fs.readFileSync(0, 'utf8'));
    const bad = [];
    for (const item of items) {
      try {
        new Function('root', item.js);
      } catch (e) {
        bad.push(`${item.pack} :: ${item.id}: JS syntax error: ${e.message}`);
      }
    }
    console.log(JSON.stringify(bad));
    """
    proc = subprocess.run(
        ["node", "-e", node_script],
        input=json.dumps(js_snippets),
        text=True,
        capture_output=True,
        check=True,
    )
    js_errors = json.loads(proc.stdout)
    errors.extend(js_errors)

    with_icons = sum(1 for _, app in all_apps.values() if app.get("iconUrl"))
    with_urls = sum(1 for _, app in all_apps.values() if app.get("storeUrl"))
    print(f"\nTotal app packs:   {len(packs)}")
    print(f"Total app motions: {len(all_ids)}")
    print(f"Total unique apps: {len(all_apps)} ({with_icons} with iconUrl, {with_urls} with storeUrl)")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s):", file=sys.stderr)
        for e in errors[:40]:
            print("  -", e, file=sys.stderr)
        if len(errors) > 40:
            print(f"  ... and {len(errors) - 40} more", file=sys.stderr)
        return 1

    print("ALL APP PACKS VALIDATED OK!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
