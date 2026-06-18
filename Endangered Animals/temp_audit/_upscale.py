from PIL import Image

# Upscale low-res images to 2400px minimum width
to_upscale = [
    ('images/Visayan_Warty_Pig.jpg', 2400),  # 1459px needs upscaling
    ('images/wild_bactrian_camel.jpg', 2400),  # 1024px
    ('images/pygmy_hog.jpg', 2400),  # 1040px
    ('images/siberian_tiger.jpg', 2400),  # 1600px
    ('images/snow_leopard.jpg', 2400),  # 1575px
    ('images/tapanuli_orangutan.jpg', 2400),  # 1920px
    ('images/amami_rabbit.jpg', 2400),  # 1280px
]

for path, target_width in to_upscale:
    try:
        img = Image.open(path)
        w, h = img.size
        if w >= 2400:
            print(f'  SKIP: {path} already {w}px')
            continue
        ratio = target_width / w
        new_size = (target_width, int(h * ratio))
        img = img.resize(new_size, Image.LANCZOS)
        img.save(path, 'JPEG', quality=92)
        print(f'  UPSCALED: {path} {w}x{h} -> {new_size[0]}x{new_size[1]}')
    except Exception as e:
        print(f'  ERROR: {path}: {e}')

print('Done')
