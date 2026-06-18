from PIL import Image
from os import path

# Check some actual animal page images
for p in [4, 5, 10, 11, 50, 100]:
    fname = f'temp_audit_hc/page_{p:02d}.jpg'
    if path.exists(fname):
        img = Image.open(fname)
        print(f'Page {p}: {img.size[0]}x{img.size[1]}  {path.getsize(fname)//1024}KB')
        # Check if it looks right - any actual image content?
        # Sample a few pixels
        r, g, b = img.getpixel((100, 100))
        print(f'  pixel(100,100) = RGB({r},{g},{b})')
