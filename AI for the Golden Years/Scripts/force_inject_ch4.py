import re
import sys

html_path = r"d:\Kapil\Books\First\Book_v2.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# First we need the base64 string
import zlib
import struct
import base64

def generate_gradient_png(width, height):
    png = b'\x89PNG\r\n\x1a\n'
    color_type = 6
    bit_depth = 8
    ihdr_data = struct.pack("!IIBBBBB", width, height, bit_depth, color_type, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    png += struct.pack("!I", len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack("!I", ihdr_crc)
    
    row_bytes = bytearray()
    for y in range(height):
        row_bytes.append(0)
        for x in range(width):
            r, g, b = 253, 251, 247
            percent_x = x / width
            if percent_x <= 0.60:
                a = 255
            elif percent_x >= 0.85:
                a = 0
            else:
                fade_percent = (percent_x - 0.60) / 0.25
                a = int(255 * (1.0 - fade_percent))
            row_bytes.extend([r, g, b, a])
            
    compressed_data = zlib.compress(row_bytes)
    idat_crc = zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff
    png += struct.pack("!I", len(compressed_data)) + b'IDAT' + compressed_data + struct.pack("!I", idat_crc)
    iend_data = b''
    iend_crc = zlib.crc32(b'IEND' + iend_data) & 0xffffffff
    png += struct.pack("!I", len(iend_data)) + b'IEND' + iend_data + struct.pack("!I", iend_crc)
    return png

b64 = base64.b64encode(generate_gradient_png(1600, 1)).decode('utf-8')
img_tag = f'<img src="data:image/png;base64,{b64}" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:5;" alt="" />'

# Find the exact chapter 4 string in Book_v2.html
match_target = '<div class="page style-a"'
target_line = -1

lines = content.split('\n')
for i, line in enumerate(lines):
    if "PAGE 11: CH4 TEXT & BACKGROUND" in line:
        target_line = i + 1 # The line AFTER the comment
        break

if target_line != -1 and match_target in lines[target_line]:
    lines.insert(target_line + 1, f"      {img_tag}")
    print("INJECTED IMAGE DIRECTLY!")
else:
    print("COULD NOT FIND TARGET LINE IN V2")

content = '\n'.join(lines)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)
