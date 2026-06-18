from PIL import Image
for p in [9,23,56]:
    img = Image.open(f'temp_audit/page_{p:02d}.jpg')
    pv = img.copy()
    pv.thumbnail((1656,2160))
    pv.save(f'temp_audit/_v21_p{p:02d}.jpg','JPEG',quality=80)
    print(f'P{p:02d} previewed')
