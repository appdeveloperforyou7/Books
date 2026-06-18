import re
import subprocess
import os

def fix_html():
    with open('Book_v2.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # --- Step 1: Fix the nested @media print with @page ---
    old_nested = '''        @media print {
          @page {
            size: 700px 1000px;
            margin: 0;
          }

          body {
            background: none;
            padding: 0;
          }

          .page {
            box-shadow: none;
            page-break-after: always;
          }
        }

        /* Fix KDP Margins for specific pages */
        #page-4-toc .toc-item {
          padding: 6px 0 !important;
        }

        #page-4-toc .toc-section {
          margin-top: 14px !important;
          margin-bottom: 2px !important;
        }

        #page-11-ch4 .text-block {
          padding: 90px 85px 120px 85px !important;
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
        }'''

    if old_nested in html:
        html = html.replace(old_nested, '')
        print('Removed nested @media print from .back-cover-content')

    # --- Step 2: Remove the old top-level @media print ---
    old_top_print = '''    /* Dedicated high-specificity rule to override Edge's print meddling */
    @media print {
      @page {
        size: 700px 1000px;
        margin: 0;
      }

      .page {
        box-shadow: none;
        margin: 0;
        page-break-after: always;
      }

      .page.style-a .text-block {
        background: linear-gradient(to right, rgba(253, 251, 247, 1) 0%, rgba(253, 251, 247, 1) 60%, transparent 100%) !important;
      }

      .page.style-a.dark-overlay .text-block {
        background: linear-gradient(to right, rgba(15, 25, 45, 0.95) 0%, rgba(15, 25, 45, 0.8) 60%, transparent 100%) !important;
      }
    }'''

    if old_top_print in html:
        html = html.replace(old_top_print, '')
        print('Removed old top-level @media print')

    # --- Step 3: Fix :root variables for bleed page size ---
    html = html.replace('--page-w: 700px;', '--page-w: 7.125in;')
    html = html.replace('--page-h: 1000px;', '--page-h: 10.25in;')
    print('Updated page dimensions to 7.125in x 10.25in')

    # --- Step 4: Add new top-level @media print with correct bleed size ---
    new_print_block = '''    /* Dedicated high-specificity rule to override Edge's print meddling */
    @media print {
      @page {
        size: 7.125in 10.25in;
        margin: 0;
      }

      body {
        background: none;
        padding: 0;
      }

      .page {
        box-shadow: none;
        margin: 0;
        page-break-after: always;
      }

      .page.style-a .text-block {
        background: linear-gradient(to right, rgba(253, 251, 247, 1) 0%, rgba(253, 251, 247, 1) 60%, transparent 100%) !important;
      }

      .page.style-a.dark-overlay .text-block {
        background: linear-gradient(to right, rgba(15, 25, 45, 0.95) 0%, rgba(15, 25, 45, 0.8) 60%, transparent 100%) !important;
      }
    }

    /* KDP Bleed & Margin Fixes */
    .page {
      background: var(--cream);
    }

    #page-4-toc .toc-item {
      padding: 6px 0 !important;
    }

    #page-4-toc .toc-section {
      margin-top: 14px !important;
      margin-bottom: 2px !important;
    }

    #page-24-ch10 .highlight-box {
      padding: 12px 20px !important;
      margin: 10px 0 !important;
    }

    #page-24-ch10 .highlight-box p {
      margin-bottom: 0 !important;
    }'''

    insert_point = html.find('page-break-after: always;')
    if insert_point != -1:
        close_brace = html.find('}', insert_point)
        if close_brace != -1:
            html = html[:close_brace+1] + '\n\n' + new_print_block + html[close_brace+1:]
            print('Added new @media print with bleed size')

    # --- Step 5: Fix IDs ---
    html = html.replace(
        'id="page-11-ch4"',
        'id="page-10-ch4"'
    )
    print('Fixed page ID (page-11-ch4 -> page-10-ch4)')

    # --- Step 6: Fix style-b-photo indentation and add cream bg ---
    old_photo_css = '''    .page.style-b-photo {
    background-color: var(--cream);
      image-rendering: high-quality;'''
    new_photo_css = '''    .page.style-b-photo {
      background-color: var(--cream);
      image-rendering: high-quality;'''
    html = html.replace(old_photo_css, new_photo_css)

    if '.page.style-b-photo' in html and 'background-color: var(--cream)' not in html:
        html = html.replace(
            '.page.style-b-photo {',
            '.page.style-b-photo {\n      background-color: var(--cream);'
        )

    # --- Step 7: Clean up extra blank lines ---
    html = re.sub(r'\n\n\n\n+', '\n\n', html)

    # --- Step 8: Close .back-cover-content if it was left open ---
    html = html.replace(
        "        img.full-page {\n          width: 100%;\n          height: 100%;\n          object-fit: cover;\n          display: block;\n        }\n\n\n  </style>",
        "        img.full-page {\n          width: 100%;\n          height: 100%;\n          object-fit: cover;\n          display: block;\n        }\n      }\n\n  </style>"
    )

    with open('Book_v2.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Saved Book_v2.html')

def generate_pdf():
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    html_path = os.path.abspath('Book_v2.html')
    pdf_path = os.path.abspath('Book_v23_KDP_Bleed.pdf')
    file_url = 'file:///' + html_path.replace('\\', '/')

    subprocess.run([
        chrome,
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        '--no-pdf-header-footer',
        f'--print-to-pdf={pdf_path}',
        '--no-margins',
        file_url
    ], check=True)
    print(f'PDF generated: {pdf_path}')

if __name__ == '__main__':
    fix_html()
    generate_pdf()
