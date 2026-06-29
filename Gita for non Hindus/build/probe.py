import fitz
d = fitz.open(r'D:\Kapil\Books\Gita for non Hindus\build\chapter9_FINAL_v5.pdf')
allt = ' '.join(' '.join(d[i].get_text().split()) for i in range(d.page_count))
for s in ['pronunciation, literal', 'Rāmānuja', 'Every verse appears']:
    print(repr(s), allt.count(s))
print('--- adept box line layout (page with Rāmānuja) ---')
for i in range(d.page_count):
    txt = d[i].get_text()
    if 'Rāmānuja' in txt:
        for b in d[i].get_text('dict')['blocks']:
            for l in b.get('lines', []):
                ws = [w['text'] for w in l['spans']]
                joined = ' '.join(ws)
                if 'Rāmānuja' in joined or 'prapatti' in joined or 'ignites' in joined or 'synthesis' in joined or 'Śaṅkara' in joined:
                    print('p%d y=%d x=%d ::' % (i+1, round(l['bbox'][1]), round(l['bbox'][0])), joined[:90])
