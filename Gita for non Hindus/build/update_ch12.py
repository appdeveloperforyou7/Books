import os
path = r'D:\Kapil\Books\Gita for non Hindus\build\gen_ch12.py'
src = open(path, encoding='utf-8').read()

# Add xrefs to each deep-dive
xref_map = {
    'adept_h="sagu': 'xrefs="7.16-19, 9.13-15, 11.54", adept_h="sagu',
    'adept_h="the embodied': 'xrefs="7.13-14, 8.21-22, 13.12", adept_h="the embodied',
    'adept_h="\u0101dhatsva': 'xrefs="8.7, 9.34, 18.65", adept_h="\u0101dhatsva',
    'adept_h="the four-step': 'xrefs="6.35, 3.19, 9.27, 18.11-12", adept_h="the four-step',
    'adept_h="adro\u1e63\u1e6d\u0101': 'xrefs="5.18, 6.9, 13.28, 2.55-72", adept_h="adro\u1e53\u1e63\u1e6d\u0101',
    'adept_h="udvij': 'xrefs="2.56, 4.10, 5.20-21", adept_h="udvij',
    'adept_h="\u015bubh\u0101\u015bubha': 'xrefs="2.38, 2.48, 4.22, 14.24-25", adept_h="\u015bubh\u0101\u015bubha',
    'adept_h="aniketa': 'xrefs="2.69-71, 4.22, 14.24-25", adept_h="aniketa',
}
count = 0
for old, new in xref_map.items():
    if old in src and new not in src:
        src = src.replace(old, new, 1)
        count += 1
print(f'Added xrefs to {count} deep-dives')

# Add life_app and sanskrit_vocab after sadhana_text
old_end = "'sadhana_text': '<p><b>Step 12 of 18"
idx = src.find(old_end)
if idx > -1:
    # find the closing of that line
    line_end = src.find('\n', idx)
    # find the closing } of the data dict (next } after sadhana_text)
    brace_idx = src.find('}', line_end)
    insert_point = brace_idx
    new_fields = """
 'life_app': [
  '<b>At work:</b> Devotion is not a spiritual add-on; it is the quality of attention you bring to what you do. A doctor devoted to healing, a teacher devoted to students -- all are practising bhakti. The question is not whether your work is spiritual but whether your spirit is in your work.',
  '<b>In relationships:</b> The marks of the devotee (12.13-19) are the world\\'s best relationship ethic: hate none, be friendly, compassionate, forgiving. Bring these to even one difficult relationship.',
  '<b>In decision-making:</b> When you cannot decide, ask: which option lets me fix my mind more steadily on what matters most? The answer is usually the simpler one.',
  '<b>In grief and loss:</b> Santustho yena kenacit -- content with whatever comes. Not resignation but trust.',
 ],
 'sanskrit_vocab': [
  '<b>bhakti</b> -- loving devotion, the path of the heart.',
  '<b>saguna / nirguna</b> -- with attributes (personal) / without attributes (impersonal).',
  '<b>abhyasa</b> -- repeated practice, the discipline of returning.',
  '<b>phala-tyaga</b> -- relinquishing the fruit of action.',
  '<b>aniketah</b> -- homeless, inwardly unrooted, at home everywhere.',
  '<b>adveshta</b> -- non-hating, the first mark of the devotee.',
 ],
"""
    src = src[:insert_point] + new_fields + src[insert_point:]
    print('Added life_app and sanskrit_vocab')

open(path, 'w', encoding='utf-8').write(src)
print('Saved gen_ch12.py')
