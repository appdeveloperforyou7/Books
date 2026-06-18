import requests
url = 'https://upload.wikimedia.org/wikipedia/commons/5/58/Ajolote_1.JPG'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, timeout=120, headers=headers)
print(f'Status: {r.status_code}, Size: {len(r.content)} bytes')
if r.status_code == 200 and len(r.content) > 500000:
    with open('images/axolotl.jpg', 'wb') as f:
        f.write(r.content)
    print('Downloaded successfully')
    from PIL import Image
    img = Image.open('images/axolotl.jpg')
    print(f'Dimensions: {img.size}')
    preview = img.copy()
    preview.thumbnail((1200, 800))
    preview.save('temp_audit/_axolotl_preview.jpg', 'JPEG', quality=90)
else:
    print(f'Failed: {r.content[:200]}')
