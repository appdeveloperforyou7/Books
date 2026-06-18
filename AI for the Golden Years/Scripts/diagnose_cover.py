"""Diagnose and fix cover PDF issues."""
import os, sys
from PyPDF2 import PdfReader
import struct

pdf = r'D:\Kapil\Books\First\Output\Cover_KDP.pdf'

print("=== PDF Diagnostics ===")
print(f"File size: {os.path.getsize(pdf):,} bytes")

# Check PDF header
with open(pdf, 'rb') as f:
    header = f.read(20)
    print(f"Header: {header}")

# Read with PyPDF2
try:
    reader = PdfReader(pdf)
    print(f"Pages: {len(reader.pages)}")
    p = reader.pages[0]
    mb = p.mediabox
    print(f"MediaBox: {float(mb.width):.1f} x {float(mb.height):.1f} pts")
    print(f"  = {float(mb.width)/72:.3f} x {float(mb.height)/72:.3f} in")
    
    # Check contents
    contents = p.get('/Contents', None)
    if contents:
        print(f"Content stream type: {type(contents).__name__}")
    else:
        print("NO Content stream!")
    
    # Check resources
    res = p.get('/Resources', None)
    if res:
        xobj = res.get('/XObject', None)
        if xobj:
            for name, obj in xobj.items():
                subtype = obj.get('/Subtype', '?')
                w = obj.get('/Width', '?')
                h = obj.get('/Height', '?')
                print(f"  XObject '{name}': {subtype}, {w}x{h}")
    else:
        print("NO Resources!")
        
except Exception as e:
    print(f"PyPDF2 error: {e}")
    import traceback
    traceback.print_exc()

# Try opening with pikepdf for better diagnostics
print("\n--- pikepdf check ---")
try:
    import pikepdf
    pdf2 = pikepdf.open(pdf)
    p2 = pdf2.pages[0]
    print(f"pikepdf page OK, MediaBox: {p2.MediaBox}")
    print(f"TrimBox: {p2.TrimBox if '/TrimBox' in p2 else 'NOT SET'}")
except Exception as e:
    print(f"pikepdf error: {e}")
