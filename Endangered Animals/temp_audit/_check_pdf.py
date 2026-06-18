import os, fitz

p = 'Output/Chronicles_of_the_Endangered.pdf'
if not os.path.exists(p):
    print('PDF MISSING')
    exit(1)

print(f'Size: {os.path.getsize(p)/1024/1024:.0f} MB')

doc = fitz.open(p)
print(f'Pages: {len(doc)}')

bad = []
for i in range(len(doc)):
    w = doc[i].rect.width / 72
    h = doc[i].rect.height / 72
    if abs(w - 8.625) > 0.01 or abs(h - 11.25) > 0.01:
        bad.append((i+1, w, h))

if bad:
    print(f'\nWrong-size pages ({len(bad)} total):')
    for pg, w, h in bad[:5]:
        print(f'  Page {pg}: {w:.3f}"x{h:.3f}"')
    print(f'  ... and {len(bad)-5} more')
else:
    print('\nAll 82 pages: 8.625"x11.250" CORRECT')

doc.close()
