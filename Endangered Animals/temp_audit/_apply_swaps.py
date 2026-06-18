import json, shutil, os

# Load current data
with open('animals_data_verified.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Copy replacement images to correct filenames
shutil.copy2('images/mountain_gorilla.jpg', 'images/mountain_gorilla_new.jpg')
shutil.copy2('images/California_Condor.jpg', 'images/california_condor.jpg')
shutil.copy2('images/Kakapo_2.jpg', 'images/kakapo.jpg')

# Fix Mountain Gorilla - use new image
for a in data:
    if a['name'] == 'Mountain Gorilla':
        a['image_url'] = 'images/mountain_gorilla_new.jpg'
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        print(f"Updated: {a['name']} -> {a['image_url']}")

# Swap Javan Rhinoceros -> California Condor
for a in data:
    if a['name'] == 'Javan Rhinoceros':
        a['name'] = 'California Condor'
        a['image_url'] = 'images/california_condor.jpg'
        a['iucn_status'] = 'Critically Endangered'
        a['est_population'] = 'approx. 560'
        a['primary_threat'] = 'Lead Poisoning & Habitat Loss'
        a['where_found'] = 'California, Arizona, Utah (USA)'
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        a['BOX_POSITION'] = 'pos-bottom-left'
        a.pop('scientific_name', None)
        print(f"Swapped: Javan Rhinoceros -> {a['name']}")

# Swap Saola -> Kakapo
for a in data:
    if a['name'] == 'Saola':
        a['name'] = 'Kakapo'
        a['image_url'] = 'images/kakapo.jpg'
        a['iucn_status'] = 'Critically Endangered'
        a['est_population'] = 'approx. 247'
        a['primary_threat'] = 'Predation by Invasive Species'
        a['where_found'] = 'New Zealand'
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        a['BOX_POSITION'] = 'pos-bottom-left'
        a.pop('scientific_name', None)
        print(f"Swapped: Saola -> {a['name']}")

# Save
with open('animals_data_verified.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nAll swaps complete. Verify with:")
for a in data:
    if a['name'] in ['California Condor', 'Kakapo', 'Mountain Gorilla']:
        print(f"  {a['name']}: {a['image_url']} fx={a.get('focal_x')} status={a.get('iucn_status')}")
