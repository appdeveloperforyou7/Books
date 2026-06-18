import json
with open('animals_data_verified.json','r',encoding='utf-8') as f:
    d = json.load(f)
for i, a in enumerate(d[:8]):
    print(f'{i+1}. {a["name"]:30s} spread={a.get("is_spread",False)} img={a.get("image_url","?")}')
