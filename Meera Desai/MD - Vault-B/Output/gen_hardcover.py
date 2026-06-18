import os, numpy as np
from PIL import Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

BASE = r"D:\Kapil\Books\Meera Desai\Covers\VAULT_B"
ARTWORK = os.path.join(BASE, "artwork")
DPI = 300
TRIM_W, TRIM_H = 5.5, 8.5
PAGES = 366
SPINE = PAGES * 0.002252 + 0.4375   # = 1.262 in (KDP hardcover white)
WRAP = 0.7085                        # per side (18mm) - KDP hardcover
WARM_BLACK = (22, 18, 15)

# Load pre-split artwork
back = Image.open(os.path.join(ARTWORK, "split_back.png")).convert("RGB")
spine_img = Image.open(os.path.join(ARTWORK, "split_spine.png")).convert("RGB")
front = Image.open(os.path.join(ARTWORK, "split_front.png")).convert("RGB")

trim_w_px = int(TRIM_W * DPI)
trim_h_px = int(TRIM_H * DPI)
sp_w_px = int(round(SPINE * DPI))
wrap_px = int(round(WRAP * DPI))

total_w = wrap_px + trim_w_px + sp_w_px + trim_w_px + wrap_px
total_h = wrap_px + trim_h_px + wrap_px

print(f"Spine: {SPINE:.3f} in ({sp_w_px} px)")
print(f"Wrap per side: {WRAP:.4f} in ({wrap_px} px)")
print(f"Total: {total_w}x{total_h} px = {total_w/DPI:.3f}x{total_h/DPI:.3f} in")
print(f"KDP expected: 13.679 x 9.917 in")

# Build cover
full = Image.new("RGB", (total_w, total_h), WARM_BLACK)
x = wrap_px
full.paste(back.resize((trim_w_px, trim_h_px), Image.LANCZOS), (x, wrap_px))
x += trim_w_px
full.paste(spine_img.resize((sp_w_px, trim_h_px), Image.LANCZOS), (x, wrap_px))
x += sp_w_px
full.paste(front.resize((trim_w_px, trim_h_px), Image.LANCZOS), (x, wrap_px))

# Save PNG preview
png_out = os.path.join(BASE, "VAULT_B_Hardcover.png")
full.save(png_out, dpi=(DPI, DPI))
print(f"PNG: {png_out} ({os.path.getsize(png_out)//1024} KB)")

# Save PDF at exact KDP dimensions
exact_w = WRAP + TRIM_W + SPINE + TRIM_W + WRAP
exact_h = TRIM_H + 2 * WRAP
tmp = os.path.join(BASE, "_hc_temp.png")
full.save(tmp, "PNG", dpi=(DPI, DPI))
pdf_out = os.path.join(BASE, "VAULT_B_Hardcover.pdf")
c = canvas.Canvas(pdf_out, pagesize=(exact_w * inch, exact_h * inch))
c.drawImage(tmp, 0, 0, width=exact_w * inch, height=exact_h * inch)
c.showPage()
c.save()
os.remove(tmp)
print(f"PDF: {pdf_out} ({os.path.getsize(pdf_out)//1024} KB)")
print(f"PDF dimensions: {exact_w:.3f} x {exact_h:.3f} in")
