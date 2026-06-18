from PIL import Image

# Create previews for systematic review
# Cover, Copyright, TOC, then animal spreads at intervals
pages_to_review = [1,2,3,  # Front matter
                   4,5,6,7,8,9,10,11,  # First few spreads
                   20,21,30,31,40,41,  # Every 10th spread
                   50,51,60,61,70,71,
                   80,81,90,91,100,101,
                   110,111,120,121,130,131,
                   140,141,  # Last spread
                   144,145,146]  # Back matter

for p in pages_to_review:
    try:
        img = Image.open(f'temp_audit_hc/page_{p:02d}.jpg')
        pv = img.copy()
        pv.thumbnail((900, 1300))
        pv.save(f'temp_audit_hc/_audit_{p:03d}.jpg', 'JPEG', quality=72)
        print(f'Page {p:3d} previewed')
    except:
        print(f'Page {p:3d} MISSING')
