import re
import os

html_path = r"d:\Kapil\Books\First\Book_v1.html"

with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace unknown replacement characters \ufffd
# 1. \ufffd surrounded by spaces = em-dash
text = text.replace(" \ufffd ", " — ")

# 2. \ufffd followed by 's', 't', 're', 've', 'll', 'm', 'd' etc inside words = apostrophe
text = re.sub(r'([a-zA-Z])\ufffd([a-zA-Z])', r"\1'\2", text)

# 3. \ufffd surrounded by non-word/space = quotes (we can just fall back to standard double quotes)
text = text.replace("\ufffd", '"')

# Also fix the weird apostrophes that might still be left over
text = text.replace("â€™", "'").replace("â€œ", '"').replace("â€", '"').replace("â€“", "—").replace("â€”", "—")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Punctuation fixed.")
