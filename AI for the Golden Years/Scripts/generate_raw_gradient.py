import zlib, struct, base64

def generate_gradient_png(width, height):
    # PNG signature
    png = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    color_type = 6 # RGBA
    bit_depth = 8
    ihdr_data = struct.pack("!IIBBBBB", width, height, bit_depth, color_type, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    png += struct.pack("!I", len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack("!I", ihdr_crc)
    
    # IDAT chunk (Image Data)
    # The gradient is a linear fade from cream (253, 251, 247, 255) at the left to fully transparent cream at the right.
    # We want it to be fully opaque for the first 50%, then fade to 0 over the next 50%.
    row_bytes = bytearray()
    
    for y in range(height):
        row_bytes.append(0) # Filter type 0
        for x in range(width):
            r, g, b = 253, 251, 247
            
            # Calculate alpha
            percent_x = x / width
            if percent_x <= 0.60:
                a = 255
            elif percent_x >= 0.85:
                a = 0
            else:
                # Fade from 1.0 to 0.0 between 60% and 85%
                fade_percent = (percent_x - 0.60) / 0.25
                a = int(255 * (1.0 - fade_percent))
                
            row_bytes.extend([r, g, b, a])
            
    compressed_data = zlib.compress(row_bytes)
    idat_crc = zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff
    png += struct.pack("!I", len(compressed_data)) + b'IDAT' + compressed_data + struct.pack("!I", idat_crc)
    
    # IEND chunk
    iend_data = b''
    iend_crc = zlib.crc32(b'IEND' + iend_data) & 0xffffffff
    png += struct.pack("!I", len(iend_data)) + b'IEND' + iend_data + struct.pack("!I", iend_crc)
    
    return png

# Generate a 1600x1200 image (high resolution for the background)
# We can make height 1 and just scale it via CSS since it's a left-to-right gradient!
gradient_raw = generate_gradient_png(1200, 1)

with open(r"d:\Kapil\Books\First\ch4_gradient_hack.png", "wb") as f:
    f.write(gradient_raw)

b64 = base64.b64encode(gradient_raw).decode('utf-8')

# Now inject this DIRECTLY right behind the text in Book_v1.html
import re
html_path = r"d:\Kapil\Books\First\Book_v1.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# We need to insert an img tag right after the `<div class="page style-a"`
img_tag = f"""<img src="data:image/png;base64,{b64}" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:5;" alt="bg" />"""

# We look for the CH4 background div we set up earlier:
target_div = r'    <div class="page style-a" style="background-image: url\(\'data:image/png;base64,.*?'
# Actually, since it has `{CH4_BASE64}` dynamically replaced by inject.py, we should replace the template string
target_pattern = r'(<div class="page style-a" style="background-image: url\(\'data:image/png;base64,\{CH4_BASE64\}\'\);">)'

if re.search(target_pattern, html):
    html = re.sub(target_pattern, rf'\1\n      {img_tag}', html)
    print("Injected raw image tag behind text for CH4")
else:
    print("Could not find CH4 block")

# Also, reset the style-a .text-block background entirely so they don't fight.
html = re.sub(
    r'background: linear-gradient.*?\}',
    r'background: transparent; z-index: 10; }',
    html, flags=re.DOTALL
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
