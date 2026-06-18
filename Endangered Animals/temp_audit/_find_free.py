import json, os
from PIL import Image

# Find used image paths
with open('animals_data_verified.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

used = set()
for a in data:
    path = a.get('image_url', '')
    # normalize
    used.add(os.path.basename(path))
    used.add(os.path.basename(path.replace('images/', '')))

print("USED images:")
for u in sorted(used):
    print(f"  {u}")

print("\nAll images in directory:")
all_imgs = sorted(f for f in os.listdir('images') if f.endswith(('.jpg','.png','.jpeg')))
for f in all_imgs:
    in_use = f in used
    try:
        img = Image.open(os.path.join('images', f))
        w, h = img.size
        status = 'IN USE' if in_use else 'FREE  '
        print(f"  {status} {f:40s} {w}x{h}")
    except:
        print(f"  {status} {f:40s} ??")
