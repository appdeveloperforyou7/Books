import fitz, os
P = r'D:\Kapil\Books\Gita for non Hindus\build\chapter9_FINAL_v3.pdf'
d = fitz.open(P)
JUNK = 'ȫȬȪȨȱȰȴăȳȭɂ'
bad = 0
for i in range(d.page_count):
    for ln in d[i].get_text().split('\n'):
        dev = [c for c in ln if '\u0900' <= c <= '\u097F']
        if len(dev) > 5 and any(c in JUNK for c in ln):
            bad += 1
            print('CORRUPT p%d:' % (i+1), ln.strip()[:55])
print('SANSKRIT:', 'CLEAN' if bad == 0 else '%d corrupt' % bad)
# render images
out = r'D:\Kapil\Books\Gita for non Hindus\build\v3audit'
os.makedirs(out, exist_ok=True)
for i in range(d.page_count):
    d[i].get_pixmap(dpi=140).save(os.path.join(out, 'p%02d.png' % (i+1)))
print('rendered', d.page_count, '->', out)
# check header/folio presence
for i in range(d.page_count):
    t = d[i].get_text()
    has_hdr = 'The Bhagavad Gītā' in t
    has_folio = any(str(n) in t.split('\n')[-3:] for n in (i+1, i+2))
    print('p%d hdr=%s folio_guess=%s' % (i+1, has_hdr, 'Y' if (str(i+1) in t or str(i+2) in t) else 'n'))
