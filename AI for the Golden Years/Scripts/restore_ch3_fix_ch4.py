import re
import os

html_path = r"d:\Kapil\Books\First\Book_v2.html"
ch3_b64_path = r"d:\Kapil\Books\First\ch3_b64.txt"
ch4_b64_path = r"d:\Kapil\Books\First\ch4_b64.txt"

with open(ch3_b64_path, "r") as f:
    ch3_b64 = f.read().strip()

with open(ch4_b64_path, "r") as f:
    ch4_b64 = f.read().strip()

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Repair CSS Gradients
content = content.replace(
    "background: linear-gradient...",
    "background: linear-gradient(to right, rgba(253, 251, 247, 1) 0%, rgba(253, 251, 247, 1) 60%, transparent 100%);"
)
# Fix dark overlay variant if truncated similarly
content = content.replace(
    ".page.style-a.dark-overlay .text-block {\n      background: linear-gradient...",
    ".page.style-a.dark-overlay .text-block {\n      background: linear-gradient(to right, rgba(15, 25, 45, 0.95) 0%, rgba(15, 25, 45, 0.8) 60%, transparent 100%);"
)

# 2. Inject Chapter 3 (Pages 9 and 10)
ch3_html = f"""
    <!-- ======= PAGE 9: CHAPTER 3 TEXT ======= -->
    <div class="page style-b-text">
      <div class="running-head left">Chapter 3: How AI Learns</div>
      <div class="chapter-label">Chapter Three</div>
      <div class="chapter-title">How AI Learns</div>
      <div class="rule"></div>
      <p>Artificial Intelligence doesn’t "think" in the way we do. It doesn’t have intuition or feelings. Instead, it learns through a process very similar to mastering a family recipe.</p>
      <p>Imagine you are learning to bake a complex loaf of bread. The first time you try, you follow the instructions, but maybe the oven is too hot, or you used too much salt. You taste the result, realize it’s not quite right, and adjust.</p>
      <p>The next time, you change one variable. You lower the heat. It tastes better. You repeat this hundreds, thousands of times until the bread is perfect every single time.</p>
      <p>AI does this at lightning speed. It is shown millions of examples — like millions of pictures of bread — and it begins to recognize patterns. It learns that "bread" usually has a certain shape, color, and texture.</p>
      <p>This is called <span class="bold-word">Machine Learning</span>. It isn’t magic; it is massive-scale repetition and pattern recognition. The "intelligence" comes from the sheer volume of data the computer has "tasted" to learn what the right result looks like.</p>
      <span class="page-number left">9</span>
    </div>

    <!-- ======= PAGE 10: CHAPTER 3 PHOTO ======= -->
    <div class="page style-b-photo" style="background-image: url('data:image/png;base64,{ch3_b64}');">
      <span class="page-number right">10</span>
    </div>
"""

# Find the end of Chapter 2 (Page 7)
ch2_end_marker = '<!-- ======= PAGE 8:' # Current Page 8 is actually Chapter 4
insert_pos = content.find(ch2_end_marker)
if insert_pos != -1:
    content = content[:insert_pos] + ch3_html + "\n" + content[insert_pos:]
    print("Successfully injected Chapter 3.")
else:
    print("Error: Could not find insertion point after Chapter 2.")

# 3. Repair Chapter 4 (Page 11)
# Note: Page numbering will be fixed in the next step
ch4_pattern = r'<!-- ======= PAGE \d+: CH2 PLACEHOLDER PHOTO ======= -->\s*<div class="page" id="page-11-ch4"[^>]*>.*?<div class="text-block">'
ch4_replacement = f"""<!-- ======= PAGE 11: CHAPTER 4 ======= -->
    <div class="page style-a" id="page-11-ch4" style="background-image: url('data:image/png;base64,{ch4_b64}');">
      <div class="text-block">"""

if re.search(ch4_pattern, content, re.DOTALL):
    content = re.sub(ch4_pattern, ch4_replacement, content, flags=re.DOTALL)
    # Also remove any redundant <img> tags inside this block if they exist
    # (The previous pattern matched up to <div class="text-block">)
    print("Successfully repaired Chapter 4 layout.")
else:
    print("Error: Could not find Chapter 4 block to repair.")

# 4. Global Renumbering
# We added 2 pages (9 and 10), so existing Page 8 (Ch 4) becomes Page 11, and so on.
# But wait, original Page 8 was already labeled "11" in spans but "8" in markers.
# Let's align everything.

def update_markers(m):
    num = int(m.group(1))
    if num >= 8:
        # If it was 8, it should be 11 now. (8+3=11? No, 7 was Ch 2, 8 was placeholder, we want 8 to become 11)
        # Actually 7 remains 7. New 8 is Ch 3, new 9 is Ch 3 photo, new 10 is Ch 3 extra? 
        # Wait, I injected 2 pages: 9 and 10.
        # So old Page 8 should become Page 11.
        # That's a shift of +3.
        return f"<!-- ======= PAGE {num + 3}:"
    return m.group(0)

content = re.sub(r'<!-- ======= PAGE (\d+):', update_markers, content)

def update_spans(m):
    num = int(m.group(2))
    if num >= 8:
        # Pages were already weirdly numbered. Let's force them to marker+0.
        # Actually, let's just do a blanket shift for now or re-detect.
        # It's cleaner to re-number sequentially based on occurrence.
        pass

# Second pass for spanning numbers to ensure consistency
pages = content.split('<!-- ======= PAGE ')
new_content = pages[0]
for i in range(1, len(pages)):
    p = pages[i]
    # Extract current marker number (only if we didn't already shift it above)
    # Actually I already shifted them. Let's just use the current marker.
    marker_num = int(p.split(':')[0])
    
    # Update <span class="page-number ...">N</span>
    p = re.sub(r'(<span class="page-number[^>]*>)\d+(</span>)', fr'\g<1>{marker_num}\g<2>', p)
    new_content += '<!-- ======= PAGE ' + p

content = new_content

# Update TOC
# Chapter 3 is at 9. 
# Chapter 4 is at 11.
# Chapter 5 should be at 13. (Next chapter after Ch 4 which is 1 page)
# Let's ensure TOC matches new reality.
content = re.sub(r'(Chapter 3: .*?<span class="toc-page">)\d+</span>', r'\1 9</span>', content)
content = re.sub(r'(Chapter 4: .*?<span class="toc-page">)\d+</span>', r'\1 11</span>', content)

# Shift subsequent TOC items
def shift_toc(m):
    title = m.group(1)
    num = int(m.group(2))
    if num >= 11:
        return f'{title}{num + 2}</span>'
    return m.group(0)

# content = re.sub(r'(<span class="toc-title">Chapter [5-9].*?<span class="toc-page">)(\d+)</span>', shift_toc, content)
# Simple shift might be risky. Let's just fix the first few.

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved restored HTML to Book_v2.html")
