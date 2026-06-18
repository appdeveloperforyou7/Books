import json, shutil

with open('animals_data_verified.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# === IMAGE REPLACEMENTS ===
replacements = {
    'Polar Bear': 'images/Polar_Bear_new.jpg',
    'Grevy\'s Zebra': 'images/Zebra_new.jpg',
    'Aye-aye': 'images/Aye_aye_v2.jpg',
    'Tasmanian Devil': 'images/Tasmanian_Devil_v2.jpg',
}

for a in data:
    if a['name'] in replacements:
        old = a['image_url']
        a['image_url'] = replacements[a['name']]
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        print(f"Replaced: {a['name']}: {old} -> {a['image_url']}")

# === BOX_POSITION FIXES ===
box_fixes = {
    'Indian Rhinoceros': 'pos-middle-left',
}
for a in data:
    if a['name'] in box_fixes:
        old = a.get('BOX_POSITION', '?')
        a['BOX_POSITION'] = box_fixes[a['name']]
        print(f"Box fix: {a['name']}: {old} -> {a['BOX_POSITION']}")

# === ANIMAL SWAPS ===
for a in data:
    if a['name'] == 'Bornean Elephant':
        a['name'] = 'Secretary Bird'
        a['image_url'] = 'images/Secretary_Bird.jpg'
        a['iucn_status'] = 'Endangered'
        a['est_population'] = 'approx. 67,000'
        a['primary_threat'] = 'Habitat Loss & Grassland Degradation'
        a['where_found'] = 'Sub-Saharan Africa'
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        a['BOX_POSITION'] = 'pos-bottom-left'
        a.pop('scientific_name', None)
        print(f"SWAPPED: Bornean Elephant -> Secretary Bird")

for a in data:
    if a['name'] == 'Tamaraw':
        a['name'] = 'Visayan Warty Pig'
        a['image_url'] = 'images/Visayan_Warty_Pig.jpg'
        a['iucn_status'] = 'Critically Endangered'
        a['est_population'] = 'approx. 300'
        a['primary_threat'] = 'Habitat Loss & Hunting'
        a['where_found'] = 'Visayan Islands, Philippines'
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        a['BOX_POSITION'] = 'pos-bottom-left'
        a.pop('scientific_name', None)
        print(f"SWAPPED: Tamaraw -> Visayan Warty Pig")

# Save
with open('animals_data_verified.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nAll fixes applied!")
