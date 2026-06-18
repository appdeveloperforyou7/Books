import requests, time

base = 'https://commons.wikimedia.org/wiki/Special:FilePath/'
headers = {'User-Agent': 'Mozilla/5.0'}

# Candidate replacement animals with good CC images
candidates = [
    ('Kakapo', 'Strigops_habroptilus_1.jpg'),
    ('Iberian_Lynx', 'Lynx_pardinus_in_Andujar.jpg'),
    ('Pere_Davids_Deer', 'Elaphurus_davidianus_2.jpg'),
    ('California_Condor', 'Gymnogyps_californianus_-San_Diego_Zoo-8a.jpg'),
    ('Philippine_Eagle', 'Pithecophaga_jefferyi_-1872.jpg'),
    ('Kagu', 'Rhynochetos_jubatus.jpg'),
]

for name, filename in candidates:
    url = base + filename
    try:
        r = requests.get(url, allow_redirects=True, headers=headers, timeout=30)
        if r.status_code == 200 and len(r.content) > 100000:
            fpath = f'images/{name}.jpg'
            with open(fpath, 'wb') as f:
                f.write(r.content)
            from PIL import Image
            img = Image.open(fpath)
            rating = 'GREAT' if min(img.size) > 2000 else 'OK' if min(img.size) > 1000 else 'SMALL'
            print(f'{rating}: {fpath} {img.size[0]}x{img.size[1]} ({len(r.content)//1024}KB)')
        else:
            print(f'SKIP: {filename} (status={r.status_code}, len={len(r.content)})')
    except Exception as e:
        print(f'ERR: {filename}: {e}')
    time.sleep(1.5)
