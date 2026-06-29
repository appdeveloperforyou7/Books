import fitz, os, re
P = r'D:\Kapil\Books\Gita for non Hindus\build\chapter9_FINAL_v4.pdf'
d = fitz.open(P)
allt = ' '.join(d[i].get_text() for i in range(d.page_count))
allt = ' '.join(allt.split())
# check all 34 verse refs present (badges '9.1'..'9.34')
missing = [f"9.{i}" for i in range(1,35) if f"GĪTĀ 9.{i}" not in allt and f"9.{i}" not in allt]
print('verses 1-34 present:', all((f"9.{i}" in allt) for i in range(1,35)))
# sanskrit integrity
JUNK='ȫȬȪȨȱȰȴăȳȭɂ'
bad=0
for i in range(d.page_count):
    for ln in d[i].get_text().split('\n'):
        dev=[c for c in ln if '\u0900'<=c<='\u097F']
        if len(dev)>5 and any(c in JUNK for c in ln): bad+=1; print('CORRUPT p%d'%(i+1),ln[:40])
print('SANSKRIT:', 'CLEAN' if bad==0 else f'{bad} corrupt')
print('pages:', d.page_count)
os.makedirs(r'D:\Kapil\Books\Gita for non Hindus\build\v4audit', exist_ok=True)
for i in range(d.page_count):
    d[i].get_pixmap(dpi=140).save(rf'D:\Kapil\Books\Gita for non Hindus\build\v4audit\p{i+1:02d}.png')
print('rendered images')
