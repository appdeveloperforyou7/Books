import requests, time
from PIL import Image
from io import BytesIO

base = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
headers = {'User-Agent': 'Mozilla/5.0'}

# Verified filenames from known Commons pages
final = [
    ('Pygmy_Hippo', 'Pygmy_hippopotamus_(Choeropsis_liberiensis).jpg'),
    ('Pygmy_Hippo', 'Hexaprotodon_liberiensis.JPG'),
    ('Pygmy_Hippo', 'Choeropsis_liberiensis_2012.jpg'),
    ('Pygmy_Hippo', 'Zwergflusspferd_4.jpg'),
    ('Maned_Wolf', 'Maned_wolf_2.jpg'),
    ('Fossa', 'Fossa_(animal).jpg'),
    ('Giant_Armadillo', 'Priodontes_maximus.jpg'),
    ('Baird_Tapir', "Baird's_Tapir.jpg"),
]

for name, filename in final:
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
            print(f'{rating}: {name:20s} -> {w}x{h} ({len(r.content)//1024}KB)')
            if rating == 'GREAT':
                break  # got a good one, stop for this animal
        else:
            print(f'SKIP: {filename} (status={r.status_code})')
    except Exception as e:
        print(f'ERR: {filename}: {e}')
    time.sleep(1)

print('Done')
