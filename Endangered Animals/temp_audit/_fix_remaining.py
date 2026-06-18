import json

with open('animals_data_verified.json','r',encoding='utf-8') as f:
    data = json.load(f)

fixes = {
    "Axolotl": {"focal_x": "left"},   # face on LEFT, was center -> 65% visible
    "Pygmy Hog": {"focal_x": "right"}, # snout on RIGHT, was center -> 75% visible
}

for a in data:
    if a['name'] in fixes:
        for key, val in fixes[a['name']].items():
            old = a.get(key, 'N/A')
            a[key] = val
            print(f"{a['name']:30s}: {key} {old:>8s} -> {val:>8s}")

with open('animals_data_verified.json','w',encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done")
