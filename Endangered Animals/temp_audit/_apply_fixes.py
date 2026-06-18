import json

with open('animals_data_verified.json','r',encoding='utf-8') as f:
    data = json.load(f)

fixes = {
    "Malayan Tiger": {"focal_x": "center"},  # face in center, fx=right cropped it
    "Pygmy Hog": {"focal_x": "center"},     # illustration, was fx=left
    "Roloway Monkey": {"focal_x": "left"},  # face on LEFT, was fx=right -> 0% visible
    "Sunda Pangolin": {"focal_x": "left"},  # face on LEFT, was fx=right -> 0% visible
    "Chinese Alligator": {"focal_x": "right"}, # face on RIGHT, was fx=left -> 0% visible
    "Radiated Tortoise": {"focal_x": "left", "focal_y": "bottom"}, # face lower-left, cut at bottom
    "Cuban Crocodile": {"focal_x": "center"}, # was fx=right, try center
    "Chinese Giant Salamander": {"focal_x": "left"}, # face at left edge, was fx=center -> 85%
    "African Wild Dog": {"focal_x": "left", "focal_y": "center"}, # face on LEFT, was fx=right -> 0%
    "Okapi": {"focal_x": "left"},            # face on LEFT, was fx=right -> 0% visible
    "Giant Panda": {"focal_x": "center"},    # face in center, was fx=right -> 75% visible
    "Red Panda": {"focal_x": "center"},      # was fx=right -> 65% visible
    "Axolotl": {"focal_x": "center"},        # was fx=left -> 60% visible
    "Bog Turtle": {"focal_x": "center"},     # was fx=right
    "Dhole": {"focal_x": "left"},            # face on LEFT, was fx=right -> 0% visible
    "Numbat": {"focal_x": "center"},         # multiple animals, was fx=right
    "Hirola": {"focal_x": "left"},           # face on LEFT, was fx=right -> 0% visible
    "Asian Elephant": {"focal_x": "center"}, # was fx=right -> 65% visible
    "Malayan Tapir": {"focal_x": "left"},    # face on LEFT, was fx=center -> 20% visible
    "Black-footed Ferret": {"focal_x": "center"}, # face center-left, was fx=right -> 0%
    "Amami Rabbit": {"focal_x": "left", "focal_y": "top"}, # face upper-left, cut at top
}

count = 0
for a in data:
    if a['name'] in fixes:
        for key, val in fixes[a['name']].items():
            old = a.get(key, 'N/A')
            a[key] = val
            print(f"{a['name']:30s}: {key} {old:>8s} -> {val:>8s}")
        count += 1

with open('animals_data_verified.json','w',encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nFixed {count} animals")
