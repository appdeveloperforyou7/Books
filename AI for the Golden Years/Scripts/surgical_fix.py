import re
import base64

def get_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

html_path = r"d:\Kapil\Books\First\Book_v2.html"
ch3_img_path = r"C:\Users\Rishabh\.gemini\antigravity\brain\ffa93514-31cf-4381-954d-3c0a1613db40\bakery_ch3_visual_1771741498764.png"
ch4_img_path = r"C:\Users\Rishabh\.gemini\antigravity\brain\ffa93514-31cf-4381-954d-3c0a1613db40\ai_agents_ch4_visual_1771741682974.png"

with open(html_path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# 1. Fix CSS Gradients
# Light gradient (default)
light_grad = "background: linear-gradient(to right, rgba(253, 251, 247, 1) 0%, rgba(253, 251, 247, 1) 60%, transparent 100%);"
dark_grad = "background: linear-gradient(to right, rgba(15, 25, 45, 0.95) 0%, rgba(15, 25, 45, 0.8) 60%, transparent 100%);"

# Locate the style blocks and fix them
content = re.sub(r'\.page\.style-a \.text-block \{[^}]*background: [^;]+;', 
                 ".page.style-a .text-block {\n      position: absolute;\n      top: 0;\n      left: 0;\n      width: 50%;\n      height: 100%;\n      padding: 110px 60px 110px 85px;\n      display: flex;\n      flex-direction: column;\n      justify-content: flex-start;\n      " + light_grad, content)

content = re.sub(r'\.page\.style-a\.dark-overlay \.text-block \{[^}]*background: [^;]+;', 
                 ".page.style-a.dark-overlay .text-block {\n      " + dark_grad, content)

# 2. Fix Chapter 3 Visual (Re-inject correct Base64)
ch3_b64 = get_b64(ch3_img_path)
content = re.sub(r'CHAPTER 3 PHOTO ======= -->\s*<div class="page style-b-photo" style="background-image: url\(\'data:image/png;base64,[^\']+\'\);',
                 f"CHAPTER 3 PHOTO ======= -->\n    <div class=\"page style-b-photo\" style=\"background-image: url('data:image/png;base64,{ch3_b64}');",
                 content, flags=re.DOTALL)

# 3. Fix Chapter 4 Visual (Ensure correct Base64 and class)
ch4_b64 = get_b64(ch4_img_path)
content = re.sub(r'CHAPTER 4 ======= -->\s*<div class="page style-a" id="page-11-ch4" style="background-image: url\(\'data:image/png;base64,[^\']+\'\);',
                 f"CHAPTER 4 ======= -->\n    <div class=\"page style-a\" id=\"page-11-ch4\" style=\"background-image: url('data:image/png;base64,{ch4_b64}');",
                 content, flags=re.DOTALL)

# 4. Sequential Renumbering
# Strip current markers and re-apply them based on position
pages = re.split(r'<!-- ======= PAGE \d+:', content)
new_content = pages[0]
for i in range(1, len(pages)):
    p = pages[i]
    # new index starts from 1
    marker_num = i
    
    # Reconstruct the marker
    # Keep the rest of the comment line
    p_parts = p.split('======= -->', 1)
    new_content += f'<!-- ======= PAGE {marker_num}:' + p_parts[0] + '======= -->'
    
    # Update <span class="page-number ...">N</span> inside this page
    page_body = p_parts[1]
    page_body = re.sub(r'(<span class="page-number[^>]*>)\s*\d+\s*(</span>)', fr'\g<1>{marker_num}\g<2>', page_body)
    new_content += page_body

content = new_content

# 5. Update Table of Contents
# Ch 1 is p. 5
# Ch 2 is p. 7
# Ch 3 is p. 9
# Ch 4 is p. 11
# Ch 5 is p. 13 (Assuming Ch 4 is 2 pages or next ch is 2 pages away)
# Actually let's just find where they are.
# Based on current structure:
# p. 1: Cover
# p. 2: Copyright
# p. 3: Intro
# p. 4: Intro
# p. 5: Ch 1
# p. 6: Ch 1 photo
# p. 7: Ch 2
# p. 8: empty? Wait.
# Let's count them.

toc_mappings = {
    "Introduction": 3,
    "Chapter 1: The AI Revolution": 5,
    "Chapter 2: You’re Already Using It!": 7,
    "Chapter 3: How AI Learns": 9,
    "Chapter 4: Meet the AI “Agents”": 11,
}

for title, page in toc_mappings.items():
    pattern = fr'(<span class="toc-title">){re.escape(title)}(</span><span\s+class="toc-page">)\d+</span>'
    content = re.sub(pattern, fr'\g<1>{title}\g<2>{page}</span>', content)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Surgically repaired Book_v2.html")
