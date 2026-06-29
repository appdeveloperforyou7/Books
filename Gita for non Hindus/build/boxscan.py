import fitz
d = fitz.open(r'D:\Kapil\Books\Gita for non Hindus\build\content.pdf')
allt = ' '.join(' '.join(d[i].get_text().split()) for i in range(d.page_count))
probes = {
 '9.10 bridge': ['conductor','symphony'],
 '9.10 sadhana': ['plant growing','overseer'],
 '9.10 adept': ['primordial','dualism'],
 '9.22 bridge': ['small child','rent'],
 '9.22 sadhana': ['hand one worry','anxiety'],
 '9.22 warn': ['prosperity','cosmic ATM'],
 '9.26 bridge': ['crayon','stranger'],
 '9.26 sadhana': ['cup of tea','secret'],
 '9.29 warn': ['indifference','rationed'],
 '9.30 bridge': ['recovery','powerlessness'],
 '9.30 sadhana': ['too far gone','prodigal'],
 '9.30 adept': ['salvation','partners'],
}
for k,ws in probes.items():
    found=[w for w in ws if w in allt]
    print(('OK  ' if len(found)==len(ws) else 'BROKEN'), k, '->', found)
