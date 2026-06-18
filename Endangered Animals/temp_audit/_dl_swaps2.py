import requests, time
from PIL import Image
from io import BytesIO

base = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
headers = {'User-Agent': 'Mozilla/5.0 (compatible; BookProject/1.0)'}

# Endangered animal swap candidates with known good images
swaps = [
    ('Visayan_Warty_Pig', 'Sus_cebifrons_2.jpg'),
    ('Markhor', 'Capra_falconeri_hepteneri.jpg'),
    ('Shoebill', 'Balaeniceps_rex_-Ueno_Zoo,_Tokyo,_Japan_-upper_body-8a.jpg'),
    ('Brown_Hyena', 'Hyaena_brunnea_1.jpg'),
    ('African_Penguin', 'African_Penguin_(_Spheniscus_demersus_).jpg'),
    ('Secretary_Bird', 'Secretary_Bird_with_open_beak.jpg'),
    ('Galapagos_Tortoise', 'Galapagos_tortoise_(Chelonoidis_nigra)_Santa_Cruz.jpg'),
    ('Golden_Snub_Nosed_Monkey', 'Rhinopithecus_roxellana.jpg'),
    ('Blue_Throated_Macaw', 'Ara_glaucogularis_-Cincinnati_Zoo-8a.jpg'),
    ('Pere_Davids_Deer', 'Elaphurus_davidianus_in_Prague_Zoo_01.jpg'),
]

for name, filename in swaps:
    url = base + filename
    try:
        r = requests.get(url, allow_redirects=True, headers=headers, timeout=30)
        if r.status_code == 200 and len(r.content) > 50000:
            img = Image.open(BytesIO(r.content))
            w, h = img.size
            rating = 'GREAT' if min(w,h) > 2000 else 'OK' if min(w,h) > 1200 else 'SMALL'
            fpath = f'images/{name}.jpg'
            with open(fpath, 'wb') as f:
                f.write(r.content)
            print(f'{rating}: {name:30s} -> {w}x{h} ({len(r.content)//1024}KB)')
        else:
            print(f'SKIP: {filename} (status={r.status_code})')
    except Exception as e:
        print(f'ERR: {filename}: {e}')
    time.sleep(1.2)
