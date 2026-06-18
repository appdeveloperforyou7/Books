import os
base = r"D:\Kapil\Books\First\Source"

with open(os.path.join(base, "Book_v1.html"), 'r', encoding='utf-8') as f:
    v1 = f.read()
with open(os.path.join(base, "Book_v2.html"), 'r', encoding='utf-8') as f:
    v2 = f.read()

print(f"v1: {v1.count('padding: 60px 45px;')}x padding:60px 45px, {v1.count('font-size: 52px;')}x font-size:52px")
print(f"v2: {v2.count('padding: 60px 45px;')}x padding:60px 45px, {v2.count('padding: 65px 55px 60px 55px;')}x new padding")
print(f"v2: {v2.count('font-size: 52px;')}x font-size:52px, {v2.count('font-size: 46px;')}x font-size:46px")

# Check page divs
print(f"v1 page divs: {v1.count('class=\"page ')} - v2: {v2.count('class=\"page ')}")

# Check if print-color-adjust was added
print(f"print-color-adjust in v2: {v2.count('print-color-adjust')}")
