import requests, time
from PIL import Image
from io import BytesIO

base = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
headers = {'User-Agent': 'Mozilla/5.0 (compatible; BookProject/1.0)'}

# LAND animals only
land_animals = [
    ('Pygmy_Hippo', 'Choeropsis_liberiensis_1.jpg'),
    ('Pygmy_Hippo', 'Hexaprotodon_liberiensis_1.jpg'),
    ('Maned_Wolf', 'Chrysocyon_brachyurus_in_Serra_da_Canastra_National_Park.jpg'),
    ('Maned_Wolf', 'Maned_wolf_at_Beardsley_Zoo.jpg'),
    ('Fossa', 'Cryptoprocta_ferox_01.jpg'),
    ('Mountain_Tapir', 'Tapirus_pinchaque_1.jpg'),
    ('Gelada', 'Gelada_Baboon_(Theropithecus_gelada)_(18420114199).jpg'),
    ('Giant_Anteater', 'Myrmecophaga_tridactyla_-_Phoenix_Zoo.jpg'),
    ('Arabian_Oryx', 'Arabian_oryx_(Oryx_leucoryx).jpg'),
    ('Scimitar_Oryx', 'Oryx_dammah_at_Honolulu_Zoo.jpg'),
    ('Cotton_Top_Tamarin', 'Saguinus_oedipus_2.jpg'),
    ('Silky_Sifaka', 'Propithecus_candidus_001.jpg'),
    ('Pere_Davids_Deer', 'Milu_group.jpg'),
    ('Brown_Hyena', 'Brown_hyena_(Hyaena_brunnea)_2.jpg'),
]

downloaded = {}
for name, filename in land_animals:
    if name in downloaded:
        continue
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
            print(f'{rating}: {name:25s} -> {w}x{h} ({len(r.content)//1024}KB)')
            downloaded[name] = fpath
        else:
            print(f'SKIP: {filename} (status={r.status_code})')
    except Exception as e:
        print(f'ERR: {filename}: {e}')
    time.sleep(1)

print(f'\nDownloaded {len(downloaded)} land animals')
