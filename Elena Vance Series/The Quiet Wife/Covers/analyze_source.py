from PIL import Image

# Check what each source image actually contains
for name in ['front_cover.png', 'back_cover.png', 'spine_cover.png']:
    img = Image.open(f'D:\\Kapil\\Books\\The Quiet Wife\\covers\\{name}')
    w, h = img.size
    ratio = w / h
    print(f"{name}: {w}x{h}, ratio={ratio:.3f}")
    print(f"  If width=trim(5.5\"=1650px), height would be: {1650/ratio:.0f}px = {1650/ratio/300:.2f}\"")
    print(f"  If height=trim(8.5\"=2550px), width would be: {2550*ratio:.0f}px = {2550*ratio/300:.2f}\"")
    print()

# The source images are 1103px tall. At what DPI is that 8.5"?
print(f"1103px / 8.5\" = {1103/8.5:.0f} DPI")
print(f"659px / 5.5\" = {659/5.5:.0f} DPI")
print(f"114px / 0.449\" = {114/0.449:.0f} DPI")

# The source images are at ~129 DPI (front/back) and ~254 DPI (spine)
# They're NOT at the same DPI!
# front_cover: 659px / 5.5" = 119.8 DPI
# spine_cover: 114px / 0.449" = 253.9 DPI

# This means the spine image was extracted at a HIGHER resolution than front/back
# The front/back images are at ~120 DPI, spine at ~254 DPI

# For the template, we need all images at 300 DPI
# Front/Back at native: 659px = 2.2" at 300 DPI — WAY too small
# We need to upscale them properly

# The correct approach: scale all images to 300 DPI based on their actual print size
# Front print width = 5.5", so at 300 DPI = 1650px
# Spine print width = 0.449", so at 300 DPI = 135px
# Back print width = 5.5", so at 300 DPI = 1650px

# But the source images are only 659px wide for front/back
# That's 659/1650 = 0.4x of what we need — a 2.5x upscale is unavoidable

# The REAL issue: the source images are too low resolution
# Let's check if the Paperback image.png is the full cover at higher effective resolution
paperback = Image.open(r'D:\Kapil\Books\The Quiet Wife\covers\Paperback image.png')
print(f"\nPaperback image.png: {paperback.size}")
print(f"  If this is full cover (11.68\" wide): DPI = {paperback.size[0]/11.68:.0f}")
print(f"  If this is front only (5.5\" wide): DPI = {paperback.size[0]/5.5:.0f}")
