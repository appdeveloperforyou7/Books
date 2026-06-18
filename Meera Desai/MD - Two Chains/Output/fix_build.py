#!/usr/bin/env python3
"""Fix build_interior.py: remove ISBN line and fix clean_para escaping."""
import os

path = os.path.join(os.path.dirname(__file__), "build_interior.py")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: Remove ISBN lines (the Spacer before it + the ISBN Paragraph)
# Find the pattern and remove it
isbn_block = """    story.append(Spacer(1, 0.5 * INCH))
    story.append(Paragraph("ISBN: [to be assigned]", copyright_style))"""
content = content.replace(isbn_block, "")

# Fix 2: Fix clean_para - the auto-formatter corrupted the HTML entity escaping
# Current corrupted code uses plain & and < > which are no-ops
# We need proper escaping. Use chr() to avoid editor corruption.
old_clean = """    text = text.replace("&", "&")
    text = text.replace("<b>", "<b>").replace("</b>", "</b>")
    text = text.replace("<i>", "<i>").replace("</i>", "</i>")"""

# Build the replacement using chr codes to survive any auto-formatting
amp = chr(38)
lt = chr(60)
gt = chr(62)

new_clean = (
    '    text = text.replace("' + amp + '", "' + amp + 'amp;")\n'
    '    text = text.replace("' + lt + 'lt;b' + gt + '", "' + lt + 'b' + gt + '").replace("' + lt + 'lt;/b' + gt + '", "' + lt + '/b' + gt + '")\n'
    '    text = text.replace("' + lt + 'lt;i' + gt + '", "' + lt + 'i' + gt + '").replace("' + lt + 'lt;/i' + gt + '", "' + lt + '/i' + gt + '")'
)

if old_clean in content:
    content = content.replace(old_clean, new_clean)
    print("Fixed clean_para escaping")
else:
    print("WARNING: Could not find corrupted clean_para to fix")
    # Show what's actually in the file
    import re
    m = re.search(r'text = text\.replace.*return text', content, re.DOTALL)
    if m:
        print("Current content:", repr(m.group()[:200]))

# Fix 3: Fix the safe fallback line
old_safe = 'safe = para.replace("<","<").replace(">",">").replace("&","&")'
new_safe = 'safe = para.replace(chr(60),chr(60)+"lt;").replace(chr(62),chr(62)+"gt;")'
if old_safe in content:
    content = content.replace(old_safe, new_safe)
    print("Fixed safe fallback")

# Remove duplicate safe line
dup_safe = '    safe = safe.replace("&","&")'
content = content.replace(dup_safe, "")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("ISBN removed:", "ISBN" not in content)
print("chr(38) present:", "chr(38)" in content)
print("Done")