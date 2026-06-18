import re

with open('Book_v2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Page 4: Add ID and apply CSS
html = html.replace('<!-- ======= PAGE 4: TABLE OF CONTENTS ======= -->\n    <div class="page style-b-text">', 
                    '<!-- ======= PAGE 4: TABLE OF CONTENTS ======= -->\n    <div class="page style-b-text" id="page-4-toc">')

if 'id="page-4-toc"' in html:
    print('Page 4 ID added.')

# Fix Page 11: Add ID
def add_id_to_page11(match):
    return '<div class="page" id="page-11-ch4"'

html = re.sub(r'<div class="page"(?=[^>]*background: linear-gradient[^<]*<img[^<]*<div class="text-block">\s*<div class="chapter-label">Chapter Four</div>)', add_id_to_page11, html)

if 'id="page-11-ch4"' in html:
    print('Page 11 ID added.')

# Fix Page 24: Add ID
html = html.replace('<!-- ======= PAGE 24: CH10 TEXT ======= -->\n    <div class="page style-b-text">',
                    '<!-- ======= PAGE 24: CH10 TEXT ======= -->\n    <div class="page style-b-text" id="page-24-ch10">')

if 'id="page-24-ch10"' in html:
    print('Page 24 ID added.')

styles = '''
    /* Fix KDP Margins for specific pages */
    #page-4-toc .toc-item { padding: 6px 0 !important; }
    #page-4-toc .toc-section { margin-top: 14px !important; margin-bottom: 2px !important; }
    
    #page-11-ch4 .text-block { 
        padding: 90px 85px 120px 85px !important; /* give more bottom margin */
    }
    #page-11-ch4 p {
        margin-bottom: 12px !important;
        font-size: 13.5px !important;
    }
    
    #page-24-ch10 .highlight-box { 
        padding: 12px 20px !important; 
        margin: 10px 0 !important; 
    }
    #page-24-ch10 .highlight-box p {
        margin-bottom: 0 !important;
    }
</style>
'''
if '/* Fix KDP Margins for specific pages */' not in html:
    html = html.replace('</style>', styles)

with open('Book_v2.html', 'w', encoding='utf-8') as f:
    f.write(html)
