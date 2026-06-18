import requests, time, json
from PIL import Image
from io import BytesIO

base = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
headers = {'User-Agent': 'Mozilla/5.0'}

# Land animals with good face portraits
land = [
    ('Giant_Anteater_v2', 'Myrmecophaga_tridactyla_2.jpg'),
    ('Maned_Wolf_v2', 'Chrysocyon_brachyurus_1.jpg'),
    ('Fossa_v2', 'Cryptoprocta_ferox_Montagne_dAmbre_National_Park.jpg'),
    ('Okapi_v2', 'Okapi_(Okapia_johnstoni)_(19895126163).jpg'),
    ('Binturong', 'Arctictis_binturong_1.jpg'),
    ('Sun_Bear', 'Helarctos_malayanus_1.jpg'),
    ('Clouded_Leopard', 'Neofelis_nebulosa_1.jpg'),
    ('Giant_Pangolin', 'Smutsia_gigantea.jpg'),
    ('Mountain_Nyala', 'Tragelaphus_buxtoni.jpg'),
]

for name, filename in land:
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
        else:
            print(f'SKIP: {filename} (status={r.status_code})')
    except Exception as e:
        print(f'ERR: {filename}: {e}')
    time.sleep(1)
