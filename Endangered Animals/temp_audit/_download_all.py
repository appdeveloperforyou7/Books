import requests
import time

base = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
headers = {'User-Agent': 'Mozilla/5.0'}

images = [
    # Mountain Gorilla (already downloaded)
    # Tamaraw - try different filenames
    ('Tamaraw', 'Tamaraw_(Bubalus_mindorensis).jpg'),
    ('Tamaraw_alt', 'Bubalus_mindorensis_at_Mounts_Iglit-Baco_National_Park.jpg'),
    # Bleeding Toad
    ('Bleeding_Toad', 'Leptophryne_cruentata.jpg'),
    # Saola
    ('Saola', 'Pseudoryx_nghetinhensis.PNG'),
    # Javan Rhino
    ('Javan_Rhino', 'Rhinoceros_sondaicus_in_London_Zoo.jpg'),
]

for name, filename in images:
    url = base + filename
    try:
        r = requests.get(url, allow_redirects=True, headers=headers, timeout=30)
        if r.status_code == 200 and len(r.content) > 50000:
            fpath = f'images/{name}.jpg'
            with open(fpath, 'wb') as f:
                f.write(r.content)
            print(f'OK: {fpath} ({len(r.content)} bytes)')
        else:
            print(f'SKIP: {filename} status={r.status_code} len={len(r.content)}')
    except Exception as e:
        print(f'ERR: {filename}: {e}')
    time.sleep(1.5)
