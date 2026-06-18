import json
with open('animals_data_verified.json','r',encoding='utf-8') as f:
    data = json.load(f)
for a in data:
    if a['name'] == 'Axolotl':
        print(f"Before: fx={a.get('focal_x')}, fy={a.get('focal_y')}")
        a['focal_x'] = 'center'
        a['focal_y'] = 'center'
        print(f"After: fx={a.get('focal_x')}, fy={a.get('focal_y')}")
with open('animals_data_verified.json','w',encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("Done")
