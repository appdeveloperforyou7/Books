#!/usr/bin/env python3
"""Check Kindle cover image against KDP requirements."""
from PIL import Image

img = Image.open("VAULT_B_Kindle_Cover.jpg")
w, h = img.size
ratio = h / w
min_ok = w >= 625 and h >= 1000
ratio_ok = 1.55 <= ratio <= 1.65

print(f"Kindle Cover: {w} x {h} px")
print(f"Aspect ratio: {ratio:.2f}:1 (KDP ideal: 1.6:1)")
print(f"Min size check: {'PASS' if min_ok else 'FAIL'} (need >= 625x1000)")
print(f"Ideal ratio check: {'PASS' if ratio_ok else 'WARN'}")
print(f"Format: {img.format}, Mode: {img.mode}")
import os
sz = os.path.getsize("VAULT_B_Kindle_Cover.jpg")
print(f"File size: {sz//1024} KB (KDP max: 65000 KB)")