import os, fitz

audit = 'temp_audit_hc'
pdf = 'Output/Chronicles_of_the_Endangered_Hardcover.pdf'
images = sorted(f for f in os.listdir(audit) if f.startswith('page_') and f.endswith('.jpg'))
print(f'Building hardcover PDF from {len(images)} images...')
doc = fitz.open()
for fname in images:
    path = os.path.join(audit, fname)
    page = doc.new_page(width=450, height=666)  # 6.25"x9.25" in points
    page.insert_image(page.rect, filename=path)
doc.save(pdf, deflate=True)
doc.close()
size = os.path.getsize(pdf) / (1024*1024)
print(f'PDF saved: {pdf} ({size:.0f} MB)')
# Verify
doc2 = fitz.open(pdf)
print(f'Pages: {len(doc2)}, Size: {doc2[0].rect.width/72:.2f}"x{doc2[0].rect.height/72:.2f}"')
doc2.close()
