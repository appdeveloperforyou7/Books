import requests, time
from PIL import Image

base = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
headers = {'User-Agent': 'Mozilla/5.0 (compatible; BookProject/1.0)'}

candidates = [
    # Polar Bear alternatives
    ('Polar_Bear_v2', 'Polar_Bear_-_Alaska_(cropped).jpg'),
    ('Polar_Bear_v2', 'Ursus_maritimus_4.jpg'),
    ('Polar_Bear_v2', 'Polar_Bear_2004-11-15.jpg'),
    # Bornean Elephant
    ('Bornean_Elephant_v2', 'Elephas_maximus_borneensis.jpg'),
    ('Bornean_Elephant_v2', 'Borneo-elephant-PLoS_Biology.jpg'),
    # California Condor - frontal
    ('California_Condor_v2', 'California_condor_(Gymnogyps_californianus)_head.jpg'),
    ('California_Condor_v2', 'Gymnogyps_californianus_-San_Diego_Zoo-8a_(cropped).jpg'),
    # Northern Hoolock Gibbon
    ('Hoolock_Gibbon_v2', 'Hoolock_gibbon.jpg'),
    ('Hoolock_Gibbon_v2', 'Hoolock_hoolock_001.jpg'),
    # Balkan Lynx
    ('Balkan_Lynx_v2', 'Lynx_lynx_poecilinus.jpg'),
    ('Balkan_Lynx_v2', 'Lynx_lynx_1_(Martin_Mecnarowski).jpg'),
    # Tasmanian Devil
    ('Tasmanian_Devil_v2', 'Tasmanian_Devil_resting.jpg'),
    ('Tasmanian_Devil_v2', 'Sarcophilus_harrisii_taranna.jpg'),
    # Sumatran Rhino
    ('Sumatran_Rhino_v2', 'Sumatran_Rhinoceros_at_Sumatran_Rhino_Sanctuary_Lampung_Indonesia_2013.JPG'),
    ('Sumatran_Rhino_v2', 'Sumatran_Rhino_2.jpg'),
    # Tamaraw
    ('Tamaraw_v2', 'Bubalus_mindorensis.jpg'),
    ('Tamaraw_v2', 'Mindoro_dwarf_buffalo.jpg'),
    # Wild Bactrian Camel
    ('Camel_v2', 'Camelus_ferus_at_The_Wilds.jpg'),
    ('Camel_v2', 'Wild_Bactrian_camel_on_road.jpg'),
    # Aye-aye
    ('Aye_aye_v2', 'Aye-aye_at_night_in_the_wild_in_Madagascar.jpg'),
    ('Aye_aye_v2', 'Wild_aye_aye.jpg'),
]

downloaded = {}
for name, filename in candidates:
    if name in downloaded:  # already got one for this animal
        continue
    url = base + filename
    try:
        r = requests.get(url, allow_redirects=True, headers=headers, timeout=30)
        if r.status_code == 200 and len(r.content) > 50000:
            from PIL import Image
            from io import BytesIO
            img = Image.open(BytesIO(r.content))
            w, h = img.size
            rating = 'GREAT' if min(w,h) > 2000 else 'OK' if min(w,h) > 1200 else 'SMALL'
            fpath = f'images/{name}.jpg'
            with open(fpath, 'wb') as f:
                f.write(r.content)
            print(f'{rating}: {name} from {filename[:40]} -> {w}x{h} ({len(r.content)//1024}KB)')
            downloaded[name] = fpath
        else:
            print(f'SKIP: {filename[:50]} (status={r.status_code})')
    except Exception as e:
        print(f'ERR: {filename[:50]}: {e}')
    time.sleep(1.5)

print(f'\nDownloaded {len(downloaded)} images:')
for name, path in downloaded.items():
    print(f'  {name}: {path}')
