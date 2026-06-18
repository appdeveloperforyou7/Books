import re

html_path = r"d:\Kapil\Books\First\Book_v1.html"
with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# Revert all curly double quotes
text = text.replace('“', '"')
text = text.replace('”', '"')

# Specifically fix the single typographic detail the user pointed out!
# "Meet the AI 'Agents'" should look elegant.
text = text.replace('Meet the AI "Agents"', 'Meet the AI &ldquo;Agents&rdquo;')

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Quotes reverted and carefully fixed!")
