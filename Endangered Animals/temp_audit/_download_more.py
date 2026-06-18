import requests, time

base = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
headers = {'User-Agent': 'Mozilla/5.0'}

# More candidates with known good quality
candidates = [
    ('Golden_Mantella', 'Mantella_aurantiaca01.jpg'),
    ('Mallorcan_Midwife_Toad', 'Alytes_muletensis.jpg'),
    ('Whooping_Crane', 'Grus_americana_-Netherlands-8.jpg'),
    ('Visayan_Warty_Pig', 'Sus_cebifrons_2.jpg'),
    ('Arabian_Oryx', 'Arabian_oryx_(ORYX_LEUCORYX).jpg'),
    ('Scimitar_Oryx', 'Oryx_dammah_1.jpg'),
    ('Kakapo_2', 'Kakapo_Sirocco_1.jpg'),
    ('Iberian_Lynx_2', 'Iberian_Lynx_Sierra_Morena.jpg'),
]

for name, filename in candidates:
    url = base + filename
    try:
        r = requests.get(url, allow_redirects=True, headers=headers, timeout=30)
        if r.status_code == 200 and len(r.content) > 50000:
            fpath = f'images/{name}.jpg'
            with open(fpath, 'wb') as f:
                f.write(r.content)
            from PIL import Image
            img = Image.open(fpath)
            rating = 'GREAT' if min(img.size) > 2000 else 'OK' if min(img.size) > 1200 else 'SMALL'
            print(f'{rating}: {fpath} {img.size[0]}x{img.size[1]} ({len(r.content)//1024}KB)')
        else:
            print(f'SKIP: {filename} (status={r.status_code})')
    except Exception as e:
        print(f'ERR: {filename}: {e}')
    time.sleep(1.5)
