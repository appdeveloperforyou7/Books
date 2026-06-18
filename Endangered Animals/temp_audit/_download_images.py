import requests
import time

session = requests.Session()
session.headers.update({
    'User-Agent': 'KDP_Book_Project/1.0 (educational; contact@example.com)',
    'Accept': 'image/jpeg,image/*',
    'Accept-Language': 'en-US'
})

images_to_try = [
    {
        'name': 'mountain_gorilla_new',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/5/50/Mountain_gorilla_%28Gorilla_beringei_beringei%29_female_with_baby.jpg',
    },
    {
        'name': 'mountain_gorilla_alt',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Mountain_gorilla_%28Gorilla_beringei_beringei%29_female_with_baby.jpg/1920px-Mountain_gorilla_%28Gorilla_beringei_beringei%29_female_with_baby.jpg',
    },
]

downloaded = 0
for img in images_to_try:
    try:
        r = session.get(img['url'], timeout=30)
        if r.status_code == 200 and len(r.content) > 50000:
            fname = f'images/{img["name"]}.jpg'
            with open(fname, 'wb') as f:
                f.write(r.content)
            print(f'DOWNLOADED: {fname} ({len(r.content)} bytes)')
            downloaded += 1
        else:
            print(f'FAILED: {img["url"][:60]}... status={r.status_code} len={len(r.content)}')
    except Exception as e:
        print(f'ERROR: {e}')
    time.sleep(2)

print(f'\nDownloaded {downloaded}/{len(images_to_try)} images')
