from PIL import Image
pages = [3,9,16,23,45,56]
for p in pages:
    img = Image.open(f'temp_audit/page_{p:02d}.jpg')
    pv = img.copy()
    pv.thumbnail((1656,2160))
    pv.save(f'temp_audit/_v20_p{p:02d}.jpg','JPEG',quality=80)
    print(f'P{p:02d} preview created')
