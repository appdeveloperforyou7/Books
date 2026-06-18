"""
Optimize the book cover image for maximum quality.
Extracts the current cover from HTML, re-encodes at higher quality,
and replaces it in the HTML.
"""
import base64, re, os
from io import BytesIO
from PIL import Image

HTML_PATH = r"D:\Kapil\Books\First\Source\Book_v2.html"
OUTPUT_JPG = r"D:\Kapil\Books\First\Assets\cover_optimized.jpg"
QUALITY = 95  # JPEG quality (max 100)

def main():
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find cover image base64
    idx = html.find('PAGE 1: COVER')
    if idx == -1:
        print("ERROR: Could not find PAGE 1: COVER")
        return

    url_start = html.find('url(', idx)
    b64_start = html.find('base64,', url_start) + 7
    url_end = html.find("');", b64_start)
    b64_str = html[b64_start:url_end]

    print(f"Base64 length: {len(b64_str):,} chars")

    # Decode
    data = base64.b64decode(b64_str)
    print(f"Decoded size: {len(data)/1024:.0f} KB")

    # Load with PIL
    img = Image.open(BytesIO(data))
    print(f"Dimensions: {img.size[0]} x {img.size[1]} px")
    print(f"Mode: {img.mode}")

    # Resize to 4K proportional for 7x10 book cover
    # For a book cover: 7x10 ratio, at 400+ DPI
    # 4K equivalent: ~4000px on the long side
    target_h = 4000
    target_w = int(target_h * 7 / 10)  # 2800px
    print(f"\nUpscaling to: {target_w} x {target_h} px (400 DPI at 7x10)")

    # Use high-quality LANCZOS resampling
    img_resized = img.resize((target_w, target_h), Image.LANCZOS)

    # Save at high quality
    img_resized.save(OUTPUT_JPG, 'JPEG', quality=QUALITY, optimize=True)
    size_kb = os.path.getsize(OUTPUT_JPG) / 1024
    print(f"Saved: {OUTPUT_JPG} ({size_kb:.0f} KB)")

    # Re-encode to base64
    buffer = BytesIO()
    img_resized.save(buffer, 'JPEG', quality=QUALITY, optimize=True)
    new_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    print(f"New base64 length: {len(new_b64):,} chars (~{len(new_b64)*3/4/1024:.0f} KB)")

    # Replace in HTML
    html = html.replace(b64_str, new_b64)
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\nUpdated HTML: {HTML_PATH}")
    print("Done. Regenerate PDF with: python Scripts/fix_bleed_comprehensive.py")
    print("(or use Chrome directly to print-to-pdf)")

if __name__ == '__main__':
    main()
