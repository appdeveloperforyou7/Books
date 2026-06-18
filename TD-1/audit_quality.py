import json, os, cv2

IMAGES = r"D:\Kapil\Books\TD-1\Images"
m = json.load(open(r"D:\Kapil\Books\TD-1\Book1\manifest_clean.json", "r", encoding="utf-8"))

# Check illustration dimensions
print("=== ILLUSTRATION DIMENSIONS (40 items) ===")
for item in m["illustrations"]:
    path = os.path.join(IMAGES, item["file"])
    if not os.path.exists(path):
        path = os.path.join(IMAGES, os.path.basename(item["file"]))
    if os.path.exists(path):
        img = cv2.imread(path)
        if img is not None:
            h, w = img.shape[:2]
            sz = os.path.getsize(path)
            status = "OK" if w >= 512 else "SMALL"
            print(f"  {item['id']}: {w}x{h}px, {sz//1024}KB [{status}]")
        else:
            print(f"  {item['id']}: CANNOT READ")
    else:
        print(f"  {item['id']}: MISSING")

# Check marginalia
print("\n=== MARGINALIA ===")
marg_dir = os.path.join(IMAGES, "Marginalia")
for f in sorted(os.listdir(marg_dir)):
    if f.endswith(".png"):
        fp = os.path.join(marg_dir, f)
        img = cv2.imread(fp)
        sz = os.path.getsize(fp)
        if img is not None:
            h, w = img.shape[:2]
            print(f"  {f}: {w}x{h}px, {sz//1024}KB")

# Count total unique images
print("\n=== TOTALS ===")
total = 0
for root, dirs, files in os.walk(IMAGES):
    for f in files:
        if f.endswith(".png"):
            total += 1
print(f"Total PNG files on disk: {total}")
print(f"Total items in manifest: {sum(len(v) for v in m.values() if isinstance(v, list))}")
