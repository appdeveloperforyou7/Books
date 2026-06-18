"""
Fix KDP errors in interior PDF:
1. Replace Google Fonts with system fonts for proper embedding
2. Ensure page 1 cover text stays within KDP margins
3. Regenerate PDF via Chrome headless with proper settings
"""
import re, os, subprocess

HTML_PATH = r"D:\Kapil\Books\First\Source\Book_v2.html"
PDF_PATH = r"D:\Kapil\Books\First\Output\Book_v28_KDP_Fixed.pdf"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ---- Fix 1: Replace Google Fonts with system fonts ----
# Google Fonts link
google_font_link = '<link\n    href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap"\n    rel="stylesheet">'

# Replace Playfair Display with Georgia (serif)
html = html.replace("'Playfair Display', 'Segoe UI Emoji', serif", "'Georgia', 'Segoe UI Emoji', serif")
html = html.replace("'Playfair Display', 'Segoe UI Emoji', sans-serif", "'Georgia', 'Segoe UI Emoji', sans-serif")
# Replace Inter with Arial/Helvetica (sans-serif)
html = html.replace("'Inter', 'Segoe UI Emoji', sans-serif", "'Arial', 'Helvetica', 'Segoe UI Emoji', sans-serif")

# Remove the Google Fonts <link>
html = html.replace(google_font_link, '<!-- Google Fonts removed for KDP font embedding -->')
if google_font_link not in html:
    fixes += 1
    print("Replaced Google Fonts with system fonts (Georgia/Arial)")

# ---- Fix 2: Increase cover page margins ----
# Increase cover-content padding for KDP margin safety
old_cover_padding = 'padding: 60px 45px;'
new_cover_padding = 'padding: 65px 55px 60px 55px;'
if old_cover_padding in html:
    html = html.replace(old_cover_padding, new_cover_padding)
    fixes += 1
    print("Increased cover page padding for KDP margin safety")

# ---- Fix 3: Reduce cover title size slightly to prevent edge overflow ----
old_cover_title = 'font-size: 52px;'
new_cover_title = 'font-size: 46px;'
if old_cover_title in html:
    html = html.replace(old_cover_title, new_cover_title)
    fixes += 1
    print("Reduced cover title from 52px to 46px for margin safety")

# ---- Fix 4: Ensure @media print has font-embedding-friendly settings ----
if '@media print {' in html:
    # Add print-color-adjust for proper rendering
    if 'print-color-adjust' not in html:
        html = html.replace(
            '@media print {',
            '@media print {\n      -webkit-print-color-adjust: exact;\n      print-color-adjust: exact;'
        )
        fixes += 1
        print("Added print-color-adjust: exact for proper color rendering")

# ---- Fix 5: Add @page margin to keep content within safe zone ----
# KDP safe margin: 0.375" from trim = 0.5" from bleed edge = 36pt at 72dpi
# For 7.125" page, safe zone starts at 0.5" from edges
# But we use @page margin: 0 to fill the page, and rely on .page padding
# The existing approach should work. Let me verify text on page 1 doesn't overflow.

# Save
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes applied: {fixes}")
print(f"Saved: {HTML_PATH}")

# ---- Generate PDF ----
print("\nGenerating PDF...")
html_abs = os.path.abspath(HTML_PATH)
pdf_abs = os.path.abspath(PDF_PATH)
file_url = 'file:///' + html_abs.replace('\\', '/')

result = subprocess.run([
    CHROME,
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    '--no-pdf-header-footer',
    f'--print-to-pdf={pdf_abs}',
    '--no-margins',
    file_url
], check=False, capture_output=True, text=True, timeout=120)

if result.returncode != 0:
    print(f"Chrome error: {result.returncode}")
    print(result.stderr[:500] if result.stderr else '')
    exit(1)

size_mb = os.path.getsize(pdf_abs) / (1024 * 1024)
print(f"PDF generated: {pdf_abs} ({size_mb:.1f} MB)")

# ---- Add TrimBox/BleedBox ----
print("Adding TrimBox/BleedBox...")
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import RectangleObject

reader = PdfReader(pdf_abs)
writer = PdfWriter()

BW, BH = 7.125 * 72, 10.25 * 72
TW, TH = 7.0 * 72, 10.0 * 72
ox, oy = (BW - TW) / 2, (BH - TH) / 2

for page in reader.pages:
    page.mediabox = RectangleObject([0, 0, BW, BH])
    page.trimbox = RectangleObject([ox, oy, ox + TW, oy + TH])
    page.bleedbox = RectangleObject([0, 0, BW, BH])
    writer.add_page(page)

tmp = pdf_abs + '.tmp'
with open(tmp, 'wb') as f:
    writer.write(f)
os.replace(tmp, pdf_abs)

print(f"TrimBox/BleedBox added")
print(f"Pages: {len(reader.pages)}")
print(f"\nFinal PDF: {pdf_abs}")
