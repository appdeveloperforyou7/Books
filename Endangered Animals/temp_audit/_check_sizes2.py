from PIL import Image
import os

files = sorted(os.listdir('temp_audit'))
page_files = [f for f in files if f.startswith('page_') and f.endswith('.jpg')]
sizes = {}
for f in page_files:
    img = Image.open(os.path.join('temp_audit', f))
    size = img.size
    if size not in sizes:
        sizes[size] = []
    sizes[size].append(f)

print('IMAGE SIZES found:')
for size, files in sorted(sizes.items()):
    print(f'  {size[0]}x{size[1]} px = {size[0]/384:.3f}"x{size[1]/384:.3f}" : {len(files)} pages')
    if len(files) < 5:
        print(f'    {files}')

# Check first page
img1 = Image.open(os.path.join('temp_audit', 'page_01.jpg'))
print(f'\nFirst page: {img1.size}')
print(f'PAGE_W = 8.625" -> expected width: {8.625*384:.0f} px')
print(f'width matches: {img1.size[0] == int(8.625*384)}')

# Also check the in-memory images
print(f'\nThese are JPEG files saved to disk (for KDP check).')
print(f'The in-memory PIL Images used for PDF generation may differ.')
