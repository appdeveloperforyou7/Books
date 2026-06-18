import re, os
from PIL import Image
from io import BytesIO
import base64

ASSETS = r"D:\Kapil\Books\First\Assets"

with open(r"D:\Kapil\Books\First\Source\Book_v2.html", 'r', encoding='utf-8') as f:
    html = f.read()

# Find BACK COVER section
idx = html.find('BACK COVER')
# Get the surrounding context
chunk = html[idx:idx+2000]
print("=== BACK COVER HTML ===")
print(chunk[:300])

# Count all page numbers
all_pages = re.findall(r'page-number[^>]*>(\d+)<', html)
print(f"\nPage range: {min(int(x) for x in all_pages)} to {max(int(x) for x in all_pages)}")
print(f"Total pages: {len(all_pages)}")

# Find all image URLs
urls = re.findall(r"url\('data:image/(png|jpeg);base64,(.+?)'\)", html)
print(f"\nTotal embedded images: {len(urls)}")

# Find the LAST embedded image (should be back cover)
last_url = None
for m in re.finditer(r"url\('data:image/(\w+);base64,(.+?)'\)", html):
    last_url = (m.group(1), m.group(2), m.start())

if last_url:
    fmt, b64_str, pos = last_url
    print(f"\nLast image: {fmt}, position {pos}, near page end? {pos > len(html)*0.9}")
    
    # Decode and check
    data = base64.b64decode(b64_str)
    img = Image.open(BytesIO(data))
    print(f"Last image: {img.size[0]}x{img.size[1]} {img.mode}")
    
    # Save for inspection
    path = os.path.join(ASSETS, "last_image.png")
    img.save(path)
    print(f"Saved to {path}")
