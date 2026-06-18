import os, fitz

# Check actual JPEG files
for f in ['page_01.jpg', 'page_50.jpg', 'page_100.jpg', 'page_142.jpg']:
    path = os.path.join('temp_audit_hc', f)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f'{f}: {size//1024}KB ({size/1024/1024:.1f}MB)')

# Check PDF
doc = fitz.open('Output/Chronicles_of_the_Endangered_Hardcover.pdf')
print(f'\nPDF pages: {len(doc)}')
p0 = doc[0]
imgs = p0.get_images(full=True)
if imgs:
    data = doc.extract_image(imgs[0][0])
    print(f'Image type: {data["ext"]}, size: {len(data["image"])//1024}KB')
doc.close()

pdf_size = os.path.getsize('Output/Chronicles_of_the_Endangered_Hardcover.pdf')
print(f'PDF file size: {pdf_size//1024}KB ({pdf_size/1024/1024:.1f}MB)')
