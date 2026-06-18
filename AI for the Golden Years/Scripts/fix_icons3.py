import re

html_path = r"d:\Kapil\Books\First\Book_v1.html"
with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace the privacy checklist items
text = text.replace('font-size:14px; color:#333;">? Do not type your', 'font-size:14px; color:#333;">🚫 Do not type your')
text = text.replace('font-size:14px; color:#333;">? Do not share banking', 'font-size:14px; color:#333;">🚫 Do not share banking')
text = text.replace('font-size:14px; color:#333;">? Do not share highly', 'font-size:14px; color:#333;">🚫 Do not share highly')
text = text.replace('font-size:14px; color:#333;">? For financial doc review', 'font-size:14px; color:#333;">🚫 For financial doc review')

# Replace the mysterious missing Chapter icon!
# I will use regex to find margin-bottom:18px;">?</div>
text = re.sub(r'margin-bottom:18px;">\?</div>', r'margin-bottom:18px;">✅</div>', text)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Checklist icons fixed!")
