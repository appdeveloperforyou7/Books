#!/usr/bin/env python3
"""Check hardcover cover PDFs against KDP requirements."""
import os
import glob
from pypdf import PdfReader

COVER_DIR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\Cover"

# KDP Hardcover 5.5 x 8.5 in
# Dust jacket: front cover (5.5) + spine + back cover (5.5) + flaps + bleed
# Case wrap: front cover (5.5) + spine + back cover (5.5) + bleed
# No bleed margins: 5.5+5.5+spine = 11+spine; with 0.125 bleed all around: +0.25

print(f"{'File':<40} {'W x H (in)':<16} {'Pages':<6} {'Size(KB)':<8}")
print("-" * 75)

for pdf_path in sorted(glob.glob(os.path.join(COVER_DIR, "VAULT_B_Hardcover_*.pdf"))):
    r = PdfReader(pdf_path)
    p0 = r.pages[0]
    w = float(p0.mediabox.width) / 72
    h = float(p0.mediabox.height) / 72
    sz = os.path.getsize(pdf_path) // 1024
    name = os.path.basename(pdf_path)
    print(f"{name:<40} {w:.2f} x {h:.2f}    {len(r.pages):<6} {sz:<8}")

# Expected spine width for 366 pages
# KDP formula: pages * PPI (pages per inch)
# White paper: 444 ppi; Cream paper: 400 ppi; Color: 220 ppi
# 366 white = 0.824"; 366 cream = 0.915"
print()
print("Spine width estimates for 366 pages:")
print(f"  White paper (444 ppi): {366/444:.3f} in")
print(f"  Cream paper (400 ppi): {366/400:.3f} in")
print(f"  Color paper (220 ppi): {366/220:.3f} in")
print()
print("KDP hardcover cover (no flaps, with bleed) for 5.5x8.5:")
print(f"  White: {(5.5+5.5+0.824+0.25):.2f} x {8.5+0.25:.2f} in")
print(f"  Cream: {(5.5+5.5+0.915+0.25):.2f} x {8.5+0.25:.2f} in")