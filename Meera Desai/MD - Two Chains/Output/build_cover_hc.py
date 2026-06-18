#!/usr/bin/env python3
"""TWO CHAINS - KDP Paperback Cover.
The provided image IS the complete cover (back + spine + front).
Just place it on the correct-sized PDF canvas. No overlays, no barcode box.
"""
import os
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

COVER_IMG = r"D:\Kapil\Books\Meera Desai\MD - Two Chains\Output\Covers\18Jun26\Paperback image.png"
OUT = r"D:\Kapil\Books\Meera Desai\MD - Two Chains\Output\TWO_CHAINS_Hardcover_Cover.pdf"

TRIM_W, TRIM_H = 5.5, 8.5
PAGES = 319
BLEED = 0.125
SPINE = 0.982  # hardcover spine for 319 pages

FULL_W = 13.482  # exact KDP hardcover width
FULL_H = 9.917  # exact KDP hardcover height
pts = lambda v: v * 72

def main():
    c = canvas.Canvas(OUT, pagesize=(pts(FULL_W), pts(FULL_H)))
    print(f"Cover canvas: {FULL_W:.3f} x {FULL_H:.3f} in ({pts(FULL_W):.0f} x {pts(FULL_H):.0f} pts)")

    # Load image, convert to RGB JPEG for embedding
    img = PILImage.open(COVER_IMG)
    iw, ih = img.size
    print(f"Source image: {iw} x {ih} px ({iw/300:.1f} x {ih/300:.1f} in at 300dpi)")
    print(f"Image aspect: {iw/ih:.3f}, Cover aspect: {FULL_W/FULL_H:.3f}")

    if img.mode == "RGBA":
        bg = PILImage.new("RGB", img.size, (15, 15, 20))
        bg.paste(img, mask=img.split()[3])
        img = bg
    if img.mode != "RGB":
        img = img.convert("RGB")

    temp_img = COVER_IMG.replace(".png", "_rgb.jpg")
    img.save(temp_img, "JPEG", quality=95)

    # Stretch image to fill entire cover exactly
    c.drawImage(temp_img, 0, 0, pts(FULL_W), pts(FULL_H), preserveAspectRatio=False)

    try: os.remove(temp_img)
    except: pass

    c.save()
    sz = os.path.getsize(OUT)
    print(f"PDF: {sz // 1024} KB ({sz / 1048576:.1f} MB)")

if __name__ == "__main__":
    main()