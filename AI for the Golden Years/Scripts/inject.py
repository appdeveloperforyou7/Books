import base64
import re
import os
import zlib
import struct

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

artifact_dir = r"C:\Users\Rishabh\.gemini\antigravity\brain\a839d29d-4848-4725-b956-9090f5349aa0"
html_path = r"d:\Kapil\Books\First\Book_v1.html"

def get_b64(filename):
    with open(os.path.join(artifact_dir, filename), "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

mappings = {
    "CH6 PLACEHOLDER": "ch6_three_phones_1771591880021.png",
    "CH7 PLACEHOLDER": "ch7_installing_app_1771591923607.png",
    "CH8 PLACEHOLDER": "ch8_dictating_phone_1771591946192.png",
    "CH9 PLACEHOLDER": "ch9_tablet_art_1771591967420.png",
    "CH10 PLACEHOLDER": "ch10_health_app_1771592004928.png",
    "CH12 PLACEHOLDER": "ch12_hallucination_1771592088334.png",
    "CH13 PLACEHOLDER": "ch13_deepfake_1771592112982.png",
    "CH14 PLACEHOLDER": "ch14_voice_clone_1771592161757.png",
    "CH15 PLACEHOLDER": "ch15_safe_word_1771592182284.png",
    "CH16 PLACEHOLDER": "ch16_privacy_1771592222053.png",
    "SUMMARY PLACEHOLDER": "ch17_checklist_1771592241753.png",
    "GLOSSARY PLACEHOLDER": "ch18_dictionary_1771592262484.png",
    "BEHIND SCENES PLACEHOLDER": "behind_scenes_1771592301531.png",
}

with open(html_path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Replace placeholders
for placeholder, img_file in mappings.items():
    b64 = get_b64(img_file)
    pattern = r'(<!-- ======= PAGE \d+: ' + placeholder + r' ======= -->\n)<div class="page" style="background: [^>]+>.*?</div>\n</div>'
    replacement = r'\1<div class="page style-b-photo" style="background-image: url(\'data:image/png;base64,' + b64 + r'\');"></div>'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Replace Cover Page background
new_cover_img = get_b64("cover_option_1_1771594383708.png")

start_idx = content.find('<!-- ======= PAGE 1: COVER ======= -->')
if start_idx != -1:
    url_start_idx = content.find("url('data:image/", start_idx)
    if url_start_idx != -1:
        url_end_idx = content.find("');", url_start_idx)
        if url_end_idx != -1:
            # Reconstruct the string with the new PNG base64
            content = content[:url_start_idx] + "url('data:image/png;base64," + new_cover_img + content[url_end_idx:]
            print("Successfully updated cover page.")
        else:
            print("Error: Could not find closing ');' for cover image.")
    else:
        print("Error: Could not find 'url(\"data:image/' for cover image.")
else:
    print("Error: Could not find PAGE 1: COVER marker.")

# Replace Back Cover background
new_back_cover_img = get_b64("back_cover_art_1771587536171.png")
new_back_cover_div = '<div class="page style-b-photo" style="background-image: url(\'data:image/png;base64,' + new_back_cover_img + '\'); background-size: cover; background-position: center; display:flex; flex-direction:column; justify-content:flex-end;"><div style="background: linear-gradient(to top, rgba(15, 25, 45, 0.95) 0%, rgba(15, 25, 45, 0.8) 60%, transparent 100%); width: 100%; height: 100%; display:flex; flex-direction:column; justify-content:space-between; padding:60px 55px; box-sizing: border-box;">'

relaxed_pattern = r'<div class="page"\s*style="background: linear-gradient[^>]+padding:60px 55px;">'
if re.search(relaxed_pattern, content, re.DOTALL):
    content = re.sub(relaxed_pattern, new_back_cover_div, content, flags=re.DOTALL)
    content = re.sub(r'(ISBN<br>BARCODE<br>HERE</div>\s*</div>\s*</div>\s*</div>)', r'\1\n</div>', content)
    print("Successfully updated back cover page.", flush=True)
else:
    print("Error: Could not find match for back cover div pattern.", flush=True)



# Enhance CSS for high-quality background scaling
content = content.replace(
    ".page.style-a {",
    ".page.style-a {\n    image-rendering: high-quality;\n    image-rendering: -webkit-optimize-contrast;"
)
content = content.replace(
    ".page.style-b-photo {",
    ".page.style-b-photo {\n    image-rendering: high-quality;\n    image-rendering: -webkit-optimize-contrast;"
)
content = content.replace(
    ".page.style-c {",
    ".page.style-c {\n    image-rendering: high-quality;\n    image-rendering: -webkit-optimize-contrast;"
)
content = content.replace(
    ".page.cover {",
    ".page.cover {\n    image-rendering: high-quality;\n    image-rendering: -webkit-optimize-contrast;"
)

# Apply explicit print rendering sizes and remove margins to prevent clipping
content = content.replace(
    "@media print {",
    "@media print {\n    @page { size: 700px 1000px; margin: 0; }"
)

# Insert CH11 Photo
if 'CH11 PHOTO' not in content:
    ch11_b64 = get_b64("ch11_grandfather_garden_1771592028011.png")
    ch11_photo_html = f"<!-- ======= PAGE 27: CH11 PHOTO ======= -->\n<div class=\"page style-b-photo\" style=\"background-image: url('data:image/png;base64,{ch11_b64}');\"></div>\n\n"
    content = content.replace("<!-- ======= PAGE 27: PART 3 SECTION DIVIDER ======= -->", ch11_photo_html + "<!-- ======= PAGE 28: PART 3 SECTION DIVIDER ======= -->")

# Consolidate Chapter 4 Text Over Image Layout
ch4_background = get_b64("ch4_hotel_concierge_1771589239906.png")
gradient_hack_b64 = base64.b64encode(generate_gradient_png(1200, 1)).decode('utf-8')
img_layer = f'<img src="data:image/png;base64,{gradient_hack_b64}" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:5;" alt="" />'

if '{CH4_BASE64}' in content:
    content = content.replace('{CH4_BASE64}', ch4_background)
    
# Now find the style-a page div for CH4 and slap the image layer directly inside it
ch4_marker = '<!-- ======= PAGE 11: CH4 TEXT & BACKGROUND ======= -->\n    <div class="page style-a"'
if ch4_marker in content:
    content = content.replace(ch4_marker, f'{ch4_marker}>\n      {img_layer}\n')
    print("Successfully injected Chapter 4 image stack with hack layer.", flush=True)
part2_img = get_b64("part2_city_divider_1771591862225.png")
content = re.sub(
    r'(<!-- ======= PAGE \d+: PART 2 SECTION DIVIDER ======= -->\n)<div class="page style-c" style="background: linear-gradient[^>]+>',
    r'\1<div class="page style-c" style="background: url(\'data:image/png;base64,' + part2_img + r'\'); background-size: cover; background-position: center;">',
    content
)

# Replace Part 3 Divider background
part3_img = get_b64("part3_storm_divider_1771592046421.png")
content = re.sub(
    r'(<!-- ======= PAGE \d+: PART 3 SECTION DIVIDER ======= -->\n)<div class="page style-c" style="background: linear-gradient[^>]+>',
    r'\1<div class="page style-c" style="background: url(\'data:image/png;base64,' + part3_img + r'\'); background-size: cover; background-position: center;">',
    content
)

# Replace Back Cover background
back_cover_img = get_b64("back_cover_1771592347189.png")
content = re.sub(
    r'(<!-- ======= PAGE \d+: BACK COVER ======= -->\n)<div class="page" style="background: linear-gradient[^>]+>',
    r'\1<div class="page" style="background: url(\'data:image/png;base64,' + back_cover_img + r'\'); background-size: cover; background-position: center; display:flex; flex-direction:column; justify-content:space-between; padding:0.6in 0.8in;">',
    content
)

# Update page titles to bump PAGE XX by 1 for all pages after 26
def bump_page(m):
    num = int(m.group(1))
    if num >= 27 and num < 100: # avoid replacing random stuff, though Regex is strict
        num += 1
    return f"<!-- ======= PAGE {num}:"

content = re.sub(r'<!-- ======= PAGE (\d+):', bump_page, content)

# Also update text page numbers > 26
def bump_span(m):
    head = m.group(1)
    num = int(m.group(2))
    if num >= 27:
        num += 1
    return f"{head}{num}</span>"

content = re.sub(r'(<span class="page-number[^>]*>)(\d+)</span>', bump_span, content)

# Also update TOC
def bump_toc(m):
    head = m.group(1)
    num = int(m.group(2))
    if num >= 27:
        num += 1
    return f"{head}{num}</span></div>"

content = re.sub(r'(<span class="toc-page">)(\d+)</span></div>', bump_toc, content)

out_path = r"d:\Kapil\Books\First\Book_v2.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Saved injected HTML to Book_v2.html")
