import fitz
import os
from PIL import Image

audit = 'temp_audit'
pdf = 'Output/Chronicles_of_the_Endangered.pdf'

images = sorted([f for f in os.listdir(audit) if f.startswith('page_') and f.endswith('.jpg')])
print(f'Building PDF from {len(images)} images...')

doc = fitz.open()
for fname in images:
    path = os.path.join(audit, fname)
    page = doc.new_page(width=630, height=630)  # 8.75"x8.75" in points (bleed included)
    page.insert_image(page.rect, filename=path)
    print(f'  {fname}')

doc.save(pdf, deflate=True)
doc.close()

size = os.path.getsize(pdf) / (1024*1024)
print(f'\nPDF saved: {pdf} ({size:.0f} MB)')

# Verify
doc2 = fitz.open(pdf)
bad = []
for i in range(len(doc2)):
    w = doc2[i].rect.width / 72
    h = doc2[i].rect.height / 72
    if abs(w - 8.75) > 0.01 or abs(h - 8.75) > 0.01:
        bad.append((i+1, w, h))
doc2.close()

if bad:
    print(f'ERROR: {len(bad)} wrong-size pages:')
    for pg, w, h in bad[:5]:
        print(f'  Page {pg}: {w:.3f}"x{h:.3f}"')
else:
    print(f'All 82 pages: 8.750"x8.750" CORRECT')
