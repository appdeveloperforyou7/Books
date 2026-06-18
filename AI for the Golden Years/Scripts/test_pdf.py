"""Quick test: generate a minimal PDF at cover dimensions to isolate the issue."""
import os
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image

OUTPUT = r"D:\Kapil\Books\First\Output"
SPREAD_W = 14.356
SPREAD_H = 10.25

# Test 1: Blank PDF with just a rectangle
print("Test 1: Blank PDF at cover dimensions...")
pdf1 = os.path.join(OUTPUT, "test_blank.pdf")
c = canvas.Canvas(pdf1, pagesize=(SPREAD_W * inch, SPREAD_H * inch))
c.setFillColorRGB(0.8, 0.2, 0.2)
c.rect(0, 0, SPREAD_W * inch, SPREAD_H * inch, fill=1)
c.setFillColorRGB(1, 1, 1)
c.setFont("Times-Bold", 24)
c.drawString(100, SPREAD_H * inch / 2, "TEST PDF - Should open in Acrobat")
c.showPage()
c.save()
print(f"  {pdf1} ({os.path.getsize(pdf1)} bytes)")
print(f"  Open this in Acrobat first to check if dimensions work")

# Test 2: PDF with a small test image
print("\nTest 2: PDF with small test image...")
img = Image.new('RGB', (400, 300), (50, 100, 200))
buf = BytesIO()
img.save(buf, 'PNG')
buf.seek(0)

pdf2 = os.path.join(OUTPUT, "test_with_image.pdf")
c = canvas.Canvas(pdf2, pagesize=(SPREAD_W * inch, SPREAD_H * inch))
c.drawImage(ImageReader(buf), 0, 0, width=SPREAD_W * inch, height=SPREAD_H * inch)
c.showPage()
c.save()
print(f"  {pdf2} ({os.path.getsize(pdf2)} bytes)")

# Test 3: PDF with the actual cover as PNG (not JPEG)
print("\nTest 3: PDF with actual cover image as PNG...")
# Load the saved spread
spread_path = os.path.join(OUTPUT, "cover_spread_v3.jpg")
if os.path.exists(spread_path):
    spread = Image.open(spread_path)
    # Resize to smaller for test
    spread_small = spread.resize((spread.width // 3, spread.height // 3))
    buf2 = BytesIO()
    spread_small.save(buf2, 'PNG')
    buf2.seek(0)
    
    pdf3 = os.path.join(OUTPUT, "test_cover_small.pdf")
    c = canvas.Canvas(pdf3, pagesize=(SPREAD_W * inch, SPREAD_H * inch))
    c.drawImage(ImageReader(buf2), 0, 0, width=SPREAD_W * inch, height=SPREAD_H * inch)
    c.showPage()
    c.save()
    print(f"  {pdf3} ({os.path.getsize(pdf3)/1024:.0f} KB)")

print("\nTry opening test_blank.pdf in Acrobat first.")
print("If that works, the issue is with the image size/format.")
