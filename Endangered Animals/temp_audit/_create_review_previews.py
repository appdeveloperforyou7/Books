from PIL import Image
import os

audit = 'temp_audit'
# Pages rated below 9: P3,9,16,18,19,23,31,32,39,41,44,45,50,51,52,56,59,60,62,63,68,71,74,75,77,79,80,82
pages = [3,9,16,18,19,23,31,32,39,41,44,45,50,51,52,56,59,60,62,63,68,71,74,75,77,79,80,82]

for p in pages:
    fname = f'page_{p:02d}.jpg'
    src = os.path.join(audit, fname)
    if not os.path.exists(src):
        print(f'MISSING: {src}')
        continue
    preview = Image.open(src).copy()
    preview.thumbnail((1656, 2160))
    outname = os.path.join(audit, f'_rv_p{p:02d}.jpg')
    preview.save(outname, 'JPEG', quality=80)
    print(f'P{p:02d} -> {outname} ({preview.size})')

print(f'\nCreated previews')
