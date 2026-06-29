import fitz
P = r'D:\Kapil\Books\Gita for non Hindus\build\chapter9_v2.pdf'
d = fitz.open(P)
print('pages:', d.page_count)
for i in range(d.page_count):
    t = ' '.join(d[i].get_text().split())
    print('p%2d | %s' % (i+1, t[:66]))

JUNK = 'ȫȬȪȨȱȰȴăȳȭɂ'
bad = 0
for i in range(d.page_count):
    for ln in d[i].get_text().split('\n'):
        dev = [c for c in ln if '\u0900' <= c <= '\u097F']
        if len(dev) > 5:
            if any(c in JUNK for c in ln):
                bad += 1
                print('CORRUPT p%d:' % (i+1), ln.strip()[:55])
print('SANSKRIT:', 'CLEAN' if bad == 0 else ('%d corrupt lines' % bad))
