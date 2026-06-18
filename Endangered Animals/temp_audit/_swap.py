import json

with open('animals_data_verified.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for a in data:
    if a['name'] == 'Javan Rhinoceros':
        a['name'] = 'California Condor'
        a['image_url'] = 'images/California_Condor.jpg'
        a['iucn_status'] = 'Critically Endangered'
        a['est_population'] = 'approx. 560'
        a['primary_threat'] = 'Lead Poisoning & Habitat Loss'
        a['where_found'] = 'California, Arizona, Utah (USA)'
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        a['BOX_POSITION'] = 'pos-bottom-left'
        a.pop('scientific_name', None)
        print(f"Swapped: Javan Rhino -> California Condor")

for a in data:
    if a['name'] == 'Saola':
        a['name'] = 'Kakapo'
        a['image_url'] = 'images/Kakapo_2.jpg'
        a['iucn_status'] = 'Critically Endangered'
        a['est_population'] = 'approx. 247'
        a['primary_threat'] = 'Predation by Invasive Species'
        a['where_found'] = 'New Zealand'
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        a['BOX_POSITION'] = 'pos-bottom-left'
        a.pop('scientific_name', None)
        print(f"Swapped: Saola -> Kakapo")

for a in data:
    if a['name'] == 'Mountain Gorilla':
        a['image_url'] = 'images/mountain_gorilla.jpg'
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        print(f"Updated: Mountain Gorilla image")

with open('animals_data_verified.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nVerification:")
for a in data:
    if a['name'] in ['California Condor', 'Kakapo', 'Mountain Gorilla']:
        print(f"  {a['name']}: {a['image_url']}")
