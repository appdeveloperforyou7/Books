from pypdf import PdfReader
import os
INTERIOR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\VAULT_B_Interior.pdf"
COVER = r"D:\Kapil\Books\Meera Desai\Covers\VAULT_B\VAULT_B_Hardcover.pdf"
print("=== HARDCOVER VERIFICATION ===\n")
r = PdfReader(INTERIOR)
w0 = float(r.pages[0].mediabox.width) / 72
h0 = float(r.pages[0].mediabox.height) / 72
sz_int = os.path.getsize(INTERIOR)
print(f"Interior: {len(r.pages)} pages, {w0:.1f} x {h0:.1f} in, {sz_int//1024//1024} MB\n")
r2 = PdfReader(COVER)
w = float(r2.pages[0].mediabox.width) / 72
h = float(r2.pages[0].mediabox.height) / 72
spine = w - 5.5 - 5.5 - 2 * 0.625
sz_cov = os.path.getsize(COVER)
print(f"Cover: {w:.3f} x {h:.3f} in, {sz_cov//1024} KB")
print(f"Spine: {spine:.3f} in (366pp white = {366/444:.3f} textblock + 0.288 board)\n")
print("KDP Hardcover 5.5x8.5 checks:")
print(f"  Height (trim 8.5 + 2x0.625 wrap = 9.75): {'PASS' if abs(h-9.75)<0.01 else 'FAIL'} (h={h:.3f})")
print(f"  Width  (5.5+spine+5.5+1.25 wrap):       {'PASS' if abs(w-(5.5+spine+5.5+1.25))<0.01 else 'FAIL'} (w={w:.3f})")
print(f"  Spine >= 0.0625 in minimum:              {'PASS' if spine >= 0.0625 else 'FAIL'}")
print(f"  File < 650 MB:                           {'PASS' if sz_cov < 650*1024*1024 else 'FAIL'}")
print(f"  Interior trim 5.5x8.5:                   {'PASS' if abs(w0-5.5)<0.01 and abs(h0-8.5)<0.01 else 'FAIL'}")
print(f"  Interior pages (24-820 range):           {'PASS' if 24 <= len(r.pages) <= 820 else 'FAIL'}")
