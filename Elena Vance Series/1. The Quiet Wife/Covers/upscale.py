from PIL import Image, ImageFilter, ImageEnhance
import os

covers_dir = r'D:\Kapil\Books\The Quiet Wife\covers'
out_dir = os.path.join(covers_dir, 'upscaled')
os.makedirs(out_dir, exist_ok=True)

def upscale_image(input_path, output_path, target_w, target_h):
    """Upscale image using LANCZOS + sharpening for best non-AI quality."""
    img = Image.open(input_path).convert("RGB")
    
    # Step 1: LANCZOS resize (best traditional upscaling)
    upscaled = img.resize((target_w, target_h), Image.LANCZOS)
    
    # Step 2: Unsharp mask to recover edges lost in upscaling
    sharpened = upscaled.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=3))
    
    # Step 3: Slight contrast boost
    enhancer = ImageEnhance.Contrast(sharpened)
    enhanced = enhancer.enhance(1.05)
    
    enhanced.save(output_path, 'PNG', optimize=True)
    print(f"Saved: {output_path} ({target_w}x{target_h})")

# Target sizes for KDP hardcover at 300 DPI
# Template: 14.115" x 10.417" = 4234 x 3125 px
# Front/Back panel: 5.625" wide, 8.75" tall = 1688 x 2625 px
# Spine panel: 0.449" wide, 8.75" tall = 135 x 2625 px

# Upscale individual covers to their target panel sizes
upscale_image(
    os.path.join(covers_dir, 'front_cover.png'),
    os.path.join(out_dir, 'front_cover.png'),
    1688, 2625
)

upscale_image(
    os.path.join(covers_dir, 'back_cover.png'),
    os.path.join(out_dir, 'back_cover.png'),
    1688, 2625
)

upscale_image(
    os.path.join(covers_dir, 'spine_cover.png'),
    os.path.join(out_dir, 'spine_cover.png'),
    135, 2625
)

# Also upscale the full combined image for reference
upscale_image(
    os.path.join(covers_dir, 'Paperback image.png'),
    os.path.join(out_dir, 'Paperback_image.png'),
    4234, 3125
)

print("\nAll images upscaled!")
