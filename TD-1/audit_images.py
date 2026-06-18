import json, os

m = json.load(open(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json", "r", encoding="utf-8"))
IMAGES = r"D:\Kapil\Books\TD-1\Images"

CAT_DIRS = {
    "illustrations": "Illustrations",
    "strips": "Strips",
    "blip_marginalia": "Marginalia",
    "chapter_vignettes": "ChapterHeaders",
    "character_cards": "Cards",
    "maps": "Maps",
    "gadget_blueprints": "Blueprints",
    "title_page": "",
    "section_dividers": "Dividers",
    "glitch_art": "GlitchArt",
    "extra_spots": "Spots",
    "documents": "Documents",
    "endpapers": "",
}

# Marginalia don't have 'file' key
MARG_FILES = {
    "BM-01": ("blip_happy", "Marginalia"),
    "BM-02": ("blip_sad", "Marginalia"),
    "BM-03": ("blip_surprised", "Marginalia"),
    "BM-04": ("blip_thinking", "Marginalia"),
    "BM-05": ("blip_scared", "Marginalia"),
    "BM-06": ("blip_excited", "Marginalia"),
    "BM-07": ("blip_waving", "Marginalia"),
    "BM-08": ("blip_sleeping", "Marginalia"),
    "BM-09": ("blip_wink", "Marginalia"),
    "BM-10": ("blip_determined", "Marginalia"),
    "BM-11": ("blip_confused", "Marginalia"),
    "BM-12": ("blip_love", "Marginalia"),
}

total = 0
missing = []
found = 0
sizes = {}
tiny_files = []

for arr_name, items in m.items():
    if arr_name not in CAT_DIRS:
        continue
    subdir = CAT_DIRS.get(arr_name, "")
    for item in items:
        total += 1
        iid = item["id"]

        if arr_name == "blip_marginalia":
            if iid in MARG_FILES:
                fname, mdir = MARG_FILES[iid]
                path = os.path.join(IMAGES, mdir, fname + ".png")
            else:
                missing.append((iid, "no mapping"))
                continue
        else:
            f = item.get("file", "")
            if "/" in f or "\\" in f:
                path = os.path.join(IMAGES, f)
            elif subdir:
                path = os.path.join(IMAGES, subdir, f)
            else:
                path = os.path.join(IMAGES, f)

        if os.path.exists(path):
            found += 1
            sz = os.path.getsize(path)
            cat = arr_name
            if cat not in sizes:
                sizes[cat] = {"min": sz, "max": sz, "total": sz, "count": 1}
            else:
                sizes[cat]["min"] = min(sizes[cat]["min"], sz)
                sizes[cat]["max"] = max(sizes[cat]["max"], sz)
                sizes[cat]["total"] += sz
                sizes[cat]["count"] += 1
            if sz < 50000:
                tiny_files.append((iid, path, sz))
        else:
            missing.append((iid, path))

print("=" * 60)
print("FILE EXISTENCE AUDIT - BOOK 1")
print("=" * 60)
print(f"Total in manifest: {total}")
print(f"Found on disk:     {found}")
print(f"Missing:           {len(missing)}")
print()

if missing:
    print("MISSING FILES:")
    for mid, mp in missing:
        print(f"  {mid}: {mp}")
    print()

if tiny_files:
    print(f"TINY FILES (<50KB, may be low res):")
    for tid, tp, ts in tiny_files:
        print(f"  {tid}: {tp} ({ts:,} bytes)")
    print()

print("SIZE STATS BY CATEGORY:")
print("-" * 60)
for cat in ["illustrations", "strips", "blip_marginalia", "chapter_vignettes",
            "character_cards", "maps", "gadget_blueprints", "title_page",
            "section_dividers", "glitch_art", "extra_spots", "documents", "endpapers"]:
    if cat in sizes:
        s = sizes[cat]
        avg = s["total"] // s["count"]
        print(f"  {cat:25s}: {s['count']:3d} files, avg {avg//1024:5d}KB, range {s['min']//1024:5d}-{s['max']//1024:5d}KB")
    else:
        print(f"  {cat:25s}: NO FILES FOUND")

# Check actual image dimensions for a sample
print()
print("DIMENSION CHECK (reading actual pixel sizes):")
try:
    import cv2
    import numpy as np
    for arr_name, items in m.items():
        if arr_name not in CAT_DIRS:
            continue
        subdir = CAT_DIRS.get(arr_name, "")
        dims = []
        for item in items[:3]:
            iid = item["id"]
            if arr_name == "blip_marginalia":
                if iid in MARG_FILES:
                    fname, mdir = MARG_FILES[iid]
                    path = os.path.join(IMAGES, mdir, fname + ".png")
                else:
                    continue
            else:
                f = item.get("file", "")
                if "/" in f or "\\" in f:
                    path = os.path.join(IMAGES, f)
                elif subdir:
                    path = os.path.join(IMAGES, subdir, f)
                else:
                    path = os.path.join(IMAGES, f)
            if os.path.exists(path):
                img = cv2.imread(path)
                if img is not None:
                    dims.append((iid, img.shape[1], img.shape[0]))
        if dims:
            for iid, w, h in dims:
                print(f"  {iid}: {w}x{h}px")
except ImportError:
    print("  (cv2 not available for dimension check)")
