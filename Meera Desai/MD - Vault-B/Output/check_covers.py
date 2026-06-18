#!/usr/bin/env python3
"""Check dimensions of all cover PDFs."""
import pikepdf
import os

COVER_DIR = r"D:\Kapil\Books\Meera Desai\MD - Vault-B\Output\Cover"

print("KDP Cover Dimension Analysis:")
print(f"  Expected:  12.150 x 8.750 in")
print(f"  Submitted: 11.893 x 8.750 in")
print(f"  Width gap: {12.150 - 11.893:.3f} in")
print(f"  For 360 pages (cream): spine should be {360 * 0.0025:.3f} in")
print(f"  Current spine: {11.893 - 11.25:.3f} in (WRONG)")
print()

print(f"{'File':<50} {'Width':>8} {'Height':>8} {'Spine':>8}")
print("-" * 80)

for root, dirs, files in os.walk(COVER_DIR):
    for f in sorted(files):
        if f.lower().endswith('.pdf'):
            path = os.path.join(root, f)
            try:
                pdf = pikepdf.open(path)
                p = pdf.pages[0]
                mb = p.MediaBox
                w = float(mb[2]) / 72
                h = float(mb[3]) / 72
                spine = w - (2 * 5.5) - (2 * 0.125)
                rel = os.path.relpath(path, COVER_DIR)
                flag = " <- CORRECT" if abs(w - 12.150) < 0.01 else ""
                print(f"{rel:<50} {w:>7.3f}  {h:>7.3f}  {spine:>7.3f}{flag}")
                pdf.close()
            except Exception as e:
                print(f"{f:<50} ERROR: {e}")