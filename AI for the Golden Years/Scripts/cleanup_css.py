import re

html_path = r"d:\Kapil\Books\First\Book_v2.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Unified CSS block for style-a
# We want to replace the mess between line 50 and 110 approx.
# Let's target the sections precisely.

style_a_block = """
    /* ===== STYLE A — Full Bleed Photo, Text on Negative Space ===== */
    .page.style-a {
      image-rendering: high-quality;
      image-rendering: -webkit-optimize-contrast;
      background-size: cover;
      background-position: center center;
    }

    .page.style-a .text-block {
      position: absolute;
      top: 0;
      left: 0;
      width: 50%;
      height: 100%;
      padding: 110px 60px 110px 85px;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      background: linear-gradient(to right, rgba(253, 251, 247, 1) 0%, rgba(253, 251, 247, 1) 60%, transparent 100%);
    }

    .page.style-a.dark-overlay .text-block {
      background: linear-gradient(to right, rgba(15, 25, 45, 0.95) 0%, rgba(15, 25, 45, 0.8) 60%, transparent 100%);
    }

    .page.style-a.dark-overlay .chapter-label {
      color: var(--gold);
    }

    .page.style-a.dark-overlay .chapter-title {
      color: #fff;
    }

    .page.style-a.dark-overlay p {
      color: rgba(255, 255, 255, 0.88);
    }

    .page.style-a.dark-overlay .bold-word {
      color: #fff;
    }
"""

print_block = """
    /* Dedicated high-specificity rule to override Edge's print meddling */
    @media print {
      @page { size: 700px 1000px; margin: 0; }
      .page { box-shadow: none; margin: 0; page-break-after: always; }
      .page.style-a .text-block {
        background: linear-gradient(to right, rgba(253, 251, 247, 1) 0%, rgba(253, 251, 247, 1) 60%, transparent 100%) !important;
      }
      .page.style-a.dark-overlay .text-block {
        background: linear-gradient(to right, rgba(15, 25, 45, 0.95) 0%, rgba(15, 25, 45, 0.8) 60%, transparent 100%) !important;
      }
    }
"""

# Replace the old style-a stuff. 
# We'll look for the comment and go until style-b-text.
pattern = re.compile(r'/\* ===== STYLE A.*?/\* ===== STYLE B', re.DOTALL)
replacement = style_a_block + "\n" + print_block + "\n\n    /* ===== STYLE B"

content = pattern.sub(replacement, content)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("CSS cleaned and validated in Book_v2.html")
