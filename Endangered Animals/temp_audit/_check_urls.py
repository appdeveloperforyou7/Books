import re
with open('hardcover_draft.html','r',encoding='utf-8') as f:
    content = f.read()
imgs = re.findall(r'src="([^"]+)"', content)
print(f'Found {len(imgs)} image URLs')
for u in imgs[:5]:
    print(f'  {u[:100]}')
