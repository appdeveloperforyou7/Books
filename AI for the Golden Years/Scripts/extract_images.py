import base64, re, os

HTML_PATH = r"D:\Kapil\Books\First\Source\Book_v2.html"
ASSETS = r"D:\Kapil\Books\First\Assets"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract back cover image
idx = html.find('BACK COVER')
url_start = html.find('url(', idx)
b64_start = html.find('base64,', url_start) + 7
url_end = html.find("');", b64_start)
b64_str = html[b64_start:url_end]

data = base64.b64decode(b64_str)
path = os.path.join(ASSETS, 'backcover_current.png')
with open(path, 'wb') as f:
    f.write(data)
print(f'Back cover: {len(data)/1024:.0f} KB -> {path}')

# Check dimensions
from PIL import Image
from io import BytesIO
img = Image.open(BytesIO(data))
print(f'Back cover dimensions: {img.size[0]} x {img.size[1]}')

# Extract front cover image
idx = html.find('PAGE 1: COVER')
url_start = html.find('url(', idx)
b64_start = html.find('base64,', url_start) + 7
url_end = html.find("');", b64_start)
b64_str = html[b64_start:url_end]
data = base64.b64decode(b64_str)
path = os.path.join(ASSETS, 'frontcover_current.jpg')
with open(path, 'wb') as f:
    f.write(data)
img = Image.open(BytesIO(data))
print(f'Front cover: {len(data)/1024:.0f} KB, {img.size[0]} x {img.size[1]} -> {path}')
