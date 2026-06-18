from PIL import Image, ImageStat
import os, json
import numpy as np

audit_dir = "temp_audit"
files = sorted([f for f in os.listdir(audit_dir) if f.endswith(".jpg")])
print("=== VISUAL QA REPORT ===")
print("Analyzing %d audit pages..." % len(files))

with open("animals_data_verified.json") as f:
    animals = json.load(f)

page_map = {}
page_map[1] = "Cover"
page_map[2] = "Copyright"
page_map[3] = "TOC"
pg = 4
for a in animals:
    if a.get("is_spread"):
        if pg % 2 != 0:
            page_map[pg] = "DIVIDER"
            pg += 1
        page_map[pg] = a["name"] + " (spread-L)"
        page_map[pg + 1] = a["name"] + " (spread-R)"
        pg += 2
    else:
        page_map[pg] = a["name"]
        pg += 1
if pg % 2 != 0:
    page_map[pg] = "DIVIDER"
    pg += 1
page_map[pg] = "Back Cover"

issues = []
for f in files:
    pn = int(f.replace("page_", "").replace(".jpg", ""))
    img = Image.open(os.path.join(audit_dir, f)).convert("RGB")
    stat = ImageStat.Stat(img)
    arr = np.array(img)
    total_px = float(arr.size)
    mean_b = stat.mean[0]
    dark_count = float(np.sum(arr < 30)) / 3.0
    black_pct = dark_count / total_px * 100
    light_count = float(np.sum(arr > 220)) / 3.0
    white_pct = light_count / total_px * 100
    r_std = float(arr[:, :, 0].std())
    g_std = float(arr[:, :, 1].std())
    b_std = float(arr[:, :, 2].std())
    color_var = (r_std + g_std + b_std) / 3.0
    desc = page_map.get(pn, "Unknown")[:50]
    flags = []
    if black_pct > 85:
        flags.append("BLANK(%d%%)" % int(black_pct))
    if black_pct > 60 and black_pct <= 85:
        flags.append("DARK(%d%%)" % int(black_pct))
    if white_pct > 40:
        flags.append("WASHED(%d%%)" % int(white_pct))
    if color_var < 10 and mean_b < 200:
        flags.append("NO_DETAIL")
    status = "OK" if not flags else " | ".join(flags)
    if status != "OK":
        issues.append("P%02d %s [%s]" % (pn, status, desc))
    print("P%02d bright=%3d black=%2d%% var=%2d %-6s %-50s" % (pn, int(mean_b), int(black_pct), int(color_var), status, desc))

print()
print("=== SUMMARY ===")
print("Issues found: %d" % len(issues))
for i in issues:
    print("  " + i)
if len(issues) == 0:
    print("  All pages pass automated checks!")
