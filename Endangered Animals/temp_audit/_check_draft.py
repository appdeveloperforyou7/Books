import re

with open('hardcover_draft.html', 'r', encoding='utf-8') as f:
    c = f.read()

print(f'info-box-minimal count: {c.count("info-box-minimal")}')
print(f'class="page-container" count: {c.count("page-container")}')
print(f'class="cover-page" count: {c.count("cover-page")}')
print(f'class="copyright-wrap" count: {c.count("copyright-wrap")}')
print(f'class="toc-container" count: {c.count("toc-container")}')
print(f'class="divider-page" count: {c.count("divider-page")}')
print(f'class="back-container" count: {c.count("back-container")}')

# Check first few page wrappers
pages = re.findall(r'class="(page-container|cover-page|copyright-wrap|toc-container|divider-page|back-container)', c)
print(f'\nAll page wrappers ({len(pages)}):')
for i, p in enumerate(pages[:10]):
    print(f'  Page {i+1}: {p}')
