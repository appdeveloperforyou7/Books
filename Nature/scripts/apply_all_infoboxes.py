#!/usr/bin/env python3
"""Apply premium quote overlays to all images using image_metadata.json."""

import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
METADATA_PATH = os.path.join(SCRIPT_DIR, "image_metadata.json")
OVERLAY_SCRIPT = os.path.join(SCRIPT_DIR, "infobox_overlay.py")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")


def main():
    if not os.path.isfile(METADATA_PATH):
        print(f"Error: metadata file not found: {METADATA_PATH}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(OVERLAY_SCRIPT):
        print(f"Error: overlay script not found: {OVERLAY_SCRIPT}", file=sys.stderr)
        sys.exit(1)

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    images = data.get("images", [])
    total = len(images)
    ok = 0
    fail = 0

    print(f"Processing {total} images...\n")

    for i, entry in enumerate(images, 1):
        src = os.path.join(PROJECT_ROOT, entry["file"])
        rel_out = entry["file"]
        dst = os.path.join(OUTPUT_DIR, rel_out)

        tag = f"[{i}/{total}]"
        print(f"  {tag} {entry['file']:<50s} -> output/{rel_out}  ", end="")

        if not os.path.isfile(src):
            print("SKIP (source missing)")
            fail += 1
            continue

        cmd = [
            sys.executable,
            OVERLAY_SCRIPT,
            "--image", src,
            "--output", dst,
            "--position", entry["position"],
            "--quote", entry["quote"],
            "--author", entry["author"],
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("OK")
            ok += 1
        else:
            print(f"FAIL ({result.stderr.strip()})")
            fail += 1

    print(f"\nDone: {ok} succeeded, {fail} failed out of {total}")


if __name__ == "__main__":
    main()
