from PIL import Image

for p in [1,2,3,4,5,6,7,144,145,146]:
    img = Image.open(f'temp_audit_hc/page_{p:02d}.jpg')
    pv = img.copy()
    pv.thumbnail((900, 1300))
    pv.save(f'temp_audit_hc/_rv_{p:03d}.jpg', 'JPEG', quality=75)
    print(f'Page {p} previewed')
