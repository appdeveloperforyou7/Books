import json
from PIL import Image

# 1. Fix the bird mistake - swap Secretary Bird for Silky Sifaka
with open('animals_data_verified.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for a in data:
    if a['name'] == 'Secretary Bird':
        a['name'] = 'Silky Sifaka'
        a['image_url'] = 'images/Silky_Sifaka.jpg'
        a['iucn_status'] = 'Critically Endangered'
        a['est_population'] = 'approx. 250'
        a['primary_threat'] = 'Habitat Loss & Hunting'
        a['where_found'] = 'Madagascar'
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        a['BOX_POSITION'] = 'pos-bottom-left'
        print(f"FIXED: Secretary Bird -> Silky Sifaka")

with open('animals_data_verified.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 2. Upscale Visayan Warty Pig and other low-res images
upscales = [
    ('images/Visayan_Warty_Pig.jpg', 2400),
    ('images/wild_bactrian_camel.jpg', 2400),
    ('images/pygmy_hog.jpg', 2400),
    ('images/siberian_tiger.jpg', 2400),
    ('images/snow_leopard.jpg', 2400),
    ('images/tapanuli_orangutan.jpg', 2400),
    ('images/amami_rabbit.jpg', 2400),
]

for path, target_w in upscales:
    img = Image.open(path)
    w, h = img.size
    if w >= target_w:
        print(f'  SKIP: {path} {w}px already')
        continue
    ratio = target_w / w
    new_size = (target_w, int(h * ratio))
    img = img.resize(new_size, Image.LANCZOS)
    img.save(path, 'JPEG', quality=92)
    print(f'  UPSCALED: {path} {w}x{h} -> {new_size[0]}x{new_size[1]}')

print("\nAll done!")
