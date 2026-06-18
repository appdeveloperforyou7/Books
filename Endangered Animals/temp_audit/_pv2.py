from PIL import Image
for p in [20,21,60,61,100,101,140,141,144,145,146]:
    try:
        img = Image.open(f'temp_audit_hc/page_{p:02d}.jpg')
        pv = img.copy()
        pv.thumbnail((900, 1300))
        pv.save(f'temp_audit_hc/_chk_{p:03d}.jpg', 'JPEG', quality=70)
        print(f'Page {p:3d} previewed')
    except:
        print(f'Page {p:3d} MISSING')
