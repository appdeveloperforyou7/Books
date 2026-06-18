import re

html_path = r"d:\Kapil\Books\First\Book_v1.html"
with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update font-families to include Segoe UI Emoji so emojis render on Windows/Edge!
text = text.replace("font-family: 'Inter', sans-serif;", "font-family: 'Inter', 'Segoe UI Emoji', sans-serif;")
text = text.replace("font-family: 'Playfair Display', serif;", "font-family: 'Playfair Display', 'Segoe UI Emoji', serif;")

# Also in inline styles
text = text.replace("font-family:'Playfair Display',serif;", "font-family: 'Playfair Display', 'Segoe UI Emoji', serif;")

# 2. Fix the padding to be a bit looser strictly on left/right for style-b-text to match v10 better
text = text.replace("padding: 110px 100px;", "padding: 110px 85px;")

# 3. Restore smart quotes around words!
# A straight quote followed by word -> open quote
text = re.sub(r'(^|\s)"(\w)', r'\1“\2', text)
# A word followed by straight quote -> close quote
text = re.sub(r'(\w)"(\s|[.,!?;:<]|$)', r'\1”\2', text)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Typography and fonts fixed!")
