import urllib.request, urllib.parse, re, os

fdir = r'D:\Kapil\Books\Gita for non Hindus\build\fonts'
ua = {'User-Agent': 'Wget/1.13.4 (linux-gnu)'}
fams = {
    'SourceSerif4': 'Source Serif 4:ital,wght@0,400;0,600;0,700;1,400',
    'NotoSerif': 'Noto Serif:ital,wght@0,400;0,700;1,400',
    'Inter': 'Inter:wght@400;500;600;700',
    'NotoSerifDevanagari': 'Noto Serif Devanagari:wght@400;500;600;700',
    'NotoSansDevanagari': 'Noto Sans Devanagari:wght@400;500;600',
}
for f in os.listdir(fdir):
    os.remove(os.path.join(fdir, f))

css_all = []
for key, spec in fams.items():
    url = 'https://fonts.googleapis.com/css2?family=' + urllib.parse.quote(spec, safe=',;:@') + '&display=swap'
    css = urllib.request.urlopen(urllib.request.Request(url, headers=ua)).read().decode()
    blocks = re.findall(r'@font-face\s*\{[^}]*\}', css, re.S)
    for b in blocks:
        wn = re.search(r'font-weight:\s*([0-9]+)', b)
        sn = re.search(r'font-style:\s*(\w+)', b)
        ur = re.search(r'url\((https://[^)]+)\)', b)
        rn = re.search(r'unicode-range:\s*([^;}]+)', b)
        if not ur or not wn:
            continue
        w = wn.group(1)
        st = sn.group(1) if sn else 'normal'
        fam_real = re.search(r"font-family:\s*'([^']+)'", b).group(1)
        src_url = ur.group(1)
        ext = 'ttf' if src_url.lower().endswith('.ttf') else ('otf' if src_url.lower().endswith('.otf') else ('woff2' if src_url.endswith('.woff2') else 'woff'))
        fn = '%s-%s%s.%s' % (key, w, ('i' if st == 'italic' else ''), ext)
        data = urllib.request.urlopen(urllib.request.Request(ur.group(1), headers=ua)).read()
        open(os.path.join(fdir, fn), 'wb').write(data)
        ur_part = (';unicode-range:' + rn.group(1).strip()) if rn else ''
        css_all.append("@font-face{font-family:'%s';font-style:%s;font-weight:%s;src:url('fonts/%s')%s;}" % (
            fam_real, st, w, fn, ur_part))
        print('OK', fn, len(data), 'bytes  w=', w, st)

open(os.path.join(os.path.dirname(fdir), 'fonts.css'), 'w', encoding='utf-8').write('\n'.join(css_all))
print('--- fonts.css written:', len(css_all), 'faces')
