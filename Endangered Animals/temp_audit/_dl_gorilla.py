import requests
url = 'https://commons.wikimedia.org/wiki/Special:FilePath/Mountain_gorilla_(Gorilla_beringei_beringei)_female_with_baby.jpg'
r = requests.get(url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
print(f'Status: {r.status_code}, Type: {r.headers.get("content-type","?")}, Size: {len(r.content)} bytes')
if r.status_code == 200 and len(r.content) > 50000:
    with open('images/mountain_gorilla.jpg', 'wb') as f:
        f.write(r.content)
    print('Saved successfully')
