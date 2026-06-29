import re
src = open(r'D:\Kapil\Books\Gita for non Hindus\build\gen_ch12.py', encoding='utf-8').read()
# Replace all problematic inner double quotes with <em> tags
replacements = [
    ('there is no "other" to hate', 'there is no <em>other</em> to hate'),
    ('can accept "bad" outcomes', 'can accept <em>bad</em> outcomes'),
    ('let go of "good" ones', 'let go of <em>good</em> ones'),
    ('the "good and bad" that are held', 'the <em>good and bad</em> that are held'),
    # catch any remaining: replace "...".( inside string values
    ('"address"', '<em>address</em>'),
]
for old, new in replacements:
    if old in src:
        src = src.replace(old, new)
        print(f'Fixed: {old[:40]}...')
# also find any remaining inner double quotes that aren't at string boundaries
# Look for patterns like = "...X"Y..." where X,Y are inside the value
# Simple heuristic: find lines with >2 double quotes that aren't dict keys
lines = src.split('\n')
issues = []
for i, line in enumerate(lines, 1):
    s = line.strip()
    if s.startswith('#') or not s:
        continue
    dq = s.count('"')
    # A normal value line has exactly 2 double quotes (opening and closing of the string)
    # If there are more, there might be inner quotes
    if dq > 2 and ('=' in s or '"' in s):
        # check if it's a dict key (like "12.2":) - those are fine
        if not re.match(r'^\s*"\d+\.\d+":', s):
            issues.append((i, dq, s[:60]))
if issues:
    print(f'\nPotential remaining issues ({len(issues)}):')
    for ln, dq, txt in issues:
        print(f'  Line {ln} ({dq} quotes): {txt}')
else:
    print('\nNo remaining issues detected.')
open(r'D:\Kapil\Books\Gita for non Hindus\build\gen_ch12.py', 'w', encoding='utf-8').write(src)
print('Saved.')
