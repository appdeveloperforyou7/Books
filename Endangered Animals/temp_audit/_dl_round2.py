import requests, time
from PIL import Image
from io import BytesIO

base = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
headers = {'User-Agent': 'Mozilla/5.0 (compatible; BookProject/1.0)'}

# More specific, known-good filenames
candidates = [
    # Polar Bear - try USFWS photos which are public domain
    ('Polar_Bear_new', 'Polar_bear_USFWS.jpg'),
    ('Polar_Bear_new', 'Polar_Bear_2004-11-15.jpg'),
    ('Polar_Bear_new', 'Play_fight_of_polar_bears_edit.jpg'),
    # California Condor - try head portrait
    ('Condor_new', 'California_Condor_Pinnacles_NP.jpg'),
    ('Condor_new', 'California_Condor_50_Mile_Photography.jpg'),
    # Bornean Elephant
    ('Elephant_new', 'Bornean_Elephant_Sabah.jpg'),
    ('Elephant_new', 'Elephas_maximus_borneensis_2.jpg'),
    # Sumatran Rhino - try higher res
    ('Rhino_new', 'Sumatran_Rhino_(Dicerorhinus_sumatrensis)_(8680982683).jpg'),
    # Tamaraw
    ('Tamaraw_new', 'Tamaraw_Bubalus_mindorensis.jpg'),
    # Wild Bactrian Camel
    ('Camel_new', 'Wild_Bactrian_Camel.jpg'),
    ('Camel_new', 'Camelus_ferus_1.jpg'),
    # Grevy's Zebra (needs replacement at 900px)
    ('Zebra_new', 'Grevy\'s_Zebra_1.jpg'),
    ('Zebra_new', 'Grevy\'s_Zebra_Close-up.jpg'),
]

for name, filename in candidates:
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
            print(f'{rating}: {name} -> {w}x{h} ({len(r.content)//1024}KB)')
        else:
            print(f'SKIP: {filename} (status={r.status_code})')
    except Exception as e:
        print(f'ERR: {filename}: {e}')
    time.sleep(1.2)
