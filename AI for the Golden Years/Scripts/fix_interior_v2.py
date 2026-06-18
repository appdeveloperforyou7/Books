"""
Revert Google Fonts, only fix the margin issue on page 1.
KDP embeds fonts automatically - font warning is just a notice, not an error.
"""
import re, os, subprocess

HTML_PATH = r"D:\Kapil\Books\First\Source\Book_v2.html"
PDF_PATH = r"D:\Kapil\Books\First\Output\Book_v28_KDP_Fixed.pdf"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# ---- REVERT: Restore Google Fonts ----
# Restore Playfair Display references
html = html.replace("'Georgia', 'Segoe UI Emoji', serif", "'Playfair Display', 'Segoe UI Emoji', serif")
html = html.replace("'Georgia', 'Segoe UI Emoji', sans-serif", "'Playfair Display', 'Segoe UI Emoji', sans-serif")
# Restore Inter references
html = html.replace("'Arial', 'Helvetica', 'Segoe UI Emoji', sans-serif", "'Inter', 'Segoe UI Emoji', sans-serif")

# Restore Google Fonts link
old_comment = '<!-- Google Fonts removed for KDP font embedding -->'
google_font_link = '<link\n    href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap"\n    rel="stylesheet">'
html = html.replace(old_comment, google_font_link)
print("Restored Google Fonts")

# ---- KEEP: Cover page margin fixes ----
# Already applied in previous run (these are still in the HTML since we saved):
# - padding: 65px 55px 60px 55px (was 60px 45px)
# - title font-size: 46px (was 52px)
# These are good fixes, keep them.

# Also check: revert title size if needed (52px was the original design intent)
# At 46px + 55px padding on 700px page = title area is 700-110 = 590px for title
# At 96dpi, 46px = 0.48" text height. Should be within safe margins

# ---- Add @page bleed ----
if 'bleed:' not in html and '@page {' in html:
    html = html.replace(
        '@page {\n        size: 7.125in 10.25in;\n        margin: 0;\n      }',
        '@page {\n        size: 7.125in 10.25in;\n        margin: 0;\n        bleed: 0.125in;\n      }'
    )

# ---- Ensure body has var(--cream) background in print ----
html = html.replace(
    'body {\n        background: none;',
    'body {\n        background: var(--cream);'
)

# Save
with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved: {HTML_PATH}")

# Generate PDF
print("\nGenerating PDF...")
html_abs = os.path.abspath(HTML_PATH)
pdf_abs = os.path.abspath(PDF_PATH)
file_url = 'file:///' + html_abs.replace('\\', '/')

result = subprocess.run([
    CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
    '--no-pdf-header-footer', f'--print-to-pdf={pdf_abs}', '--no-margins',
    file_url
], check=False, capture_output=True, text=True, timeout=120)

if result.returncode != 0:
    print(f"ERROR: {result.returncode}")
    exit(1)

size_mb = os.path.getsize(pdf_abs) / (1024 * 1024)
print(f"PDF: {pdf_abs} ({size_mb:.1f} MB)")

# Add metadata
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

print(f"Pages: {len(reader.pages)}")
print(f"TrimBox: {TW/72:.3f}\" x {TH/72:.3f}\"")
print(f"Done: {pdf_abs}")
