import os, sys
from PyPDF2 import PdfReader

pdf = r'D:\Kapil\Books\First\Output\Cover_KDP.pdf'
print(f'File exists: {os.path.exists(pdf)}')
print(f'Size: {os.path.getsize(pdf)} bytes')

try:
    reader = PdfReader(pdf)
    print(f'Pages: {len(reader.pages)}')
    p = reader.pages[0]
    mb = p.mediabox
    print(f'MediaBox: {float(mb.width):.1f} x {float(mb.height):.1f} pts')
    print(f'  = {float(mb.width)/72:.3f} x {float(mb.height)/72:.3f} inches')
    
    contents = p.get('/Contents', None)
    if contents:
        print(f'Content stream: present')
    else:
        print(f'Content stream: MISSING - PDF is empty!')
    
    # Check for resources (images)
    resources = p.get('/Resources', None)
    if resources:
        xobj = resources.get('/XObject', None)
        if xobj:
            print(f'XObjects (images): {len(xobj)}')
        else:
            print('No XObjects found')
    else:
        print('No Resources found')
        
except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
