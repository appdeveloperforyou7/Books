from PIL import Image
img = Image.open('temp_audit/page_35.jpg')
w, h = img.size
print(f'Page 35 image: {w}x{h} px = {w/384:.3f}"x{h/384:.3f}"')
print(f'Expected: 3312x4320 px = 8.625"x11.25"')
if w != 3312 or h != 4320:
    print(f'ERROR: Page 35 is wrong size! Differs by {w-3312}px x {h-4320}px')
else:
    print('Page 35 is correct size')

# Check all page sizes
import os
import glob
files = sorted(os.listdir('temp_audit'))
bad = []
for f in files:
    if f.startswith('page_') and f.endswith('.jpg'):
        img = Image.open(os.path.join('temp_audit', f))
        w, h = img.size
        if w != 3312 or h != 4320:
            bad.append((f, w, h))
if bad:
    print(f'\nWRONG SIZE pages:')
    for f, w, h in bad:
        print(f'  {f}: {w}x{h}')
else:
    print(f'\nAll pages 3312x4320 correct')
