"""
Build a premium KDP paperback cover HTML and PDF.
Uses separate front/back images with proper CSS positioning.
47 pages at 0.002252" cream = ~0.106" spine.
"""
import base64, os, subprocess, sys
from io import BytesIO
from PIL import Image, ImageDraw, ImageEnhance

ASSETS = r"D:\Kapil\Books\First\Assets"
OUTPUT = r"D:\Kapil\Books\First\Output"
FRONT_IMG = os.path.join(ASSETS, "frontcover_current.jpg")
BACK_IMG = os.path.join(ASSETS, "backcover_current.png")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

TRIM_W = 7.0
TRIM_H = 10.0
SPINE = 0.106   # 47 pages × 0.002252" cream paper
BLEED = 0.125

SPREAD_W = TRIM_W * 2 + SPINE + BLEED * 2  # 14.356"
SPREAD_H = TRIM_H + BLEED * 2               # 10.25"

DPI = 400
TRIM_W_PX = int(TRIM_W * DPI)   # 2800
TRIM_H_PX = int(TRIM_H * DPI)   # 4000
SPINE_PX = int(SPINE * DPI)     # ~42


def prepare_images():
    """Load and prep images, create spine graphic."""
    print("=== Preparing Images ===")

    # Load images
    front = Image.open(FRONT_IMG).convert('RGB')
    back = Image.open(BACK_IMG).convert('RGB')

    # Resize to trim panel dimensions
    if front.size != (TRIM_W_PX, TRIM_H_PX):
        print(f"Resizing front: {front.size} -> {TRIM_W_PX}x{TRIM_H_PX}")
        front = front.resize((TRIM_W_PX, TRIM_H_PX), Image.LANCZOS)

    if back.size != (TRIM_W_PX, TRIM_H_PX):
        print(f"Resizing back: {back.size} -> {TRIM_W_PX}x{TRIM_H_PX}")
        back = back.resize((TRIM_W_PX, TRIM_H_PX), Image.LANCZOS)

    # Enhance images for more punch
    enhancer = ImageEnhance.Contrast(front)
    front = enhancer.enhance(1.08)
    enhancer = ImageEnhance.Sharpness(front)
    front = enhancer.enhance(1.3)

    enhancer = ImageEnhance.Contrast(back)
    back = enhancer.enhance(1.05)
    enhancer = ImageEnhance.Brightness(back)
    back = enhancer.enhance(0.95)  # slightly darker for text overlay

    # Save enhanced versions
    front_out = os.path.join(ASSETS, "cover_front_final.jpg")
    back_out = os.path.join(ASSETS, "cover_back_final.jpg")
    front.save(front_out, 'JPEG', quality=95)
    back.save(back_out, 'JPEG', quality=95)

    # Create spine background
    spine = Image.new('RGB', (SPINE_PX, TRIM_H_PX), (15, 28, 50))
    draw = ImageDraw.Draw(spine)
    gold = (201, 145, 61)
    # Thin gold vertical lines
    for x in [4, SPINE_PX - 5]:
        draw.line([(x, 300), (x, TRIM_H_PX - 300)], fill=gold, width=1)
    spine_out = os.path.join(ASSETS, "cover_spine_final.jpg")
    spine.save(spine_out, 'JPEG', quality=95)

    print(f"Front:  {front_out}")
    print(f"Back:   {back_out}")
    print(f"Spine:  {spine_out}")
    return front_out, back_out, spine_out


def build_html(front_img, back_img, spine_img):
    """Create the cover HTML with separate images for each panel."""
    print("\n=== Building Cover HTML ===")

    def img_to_b64(path):
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')

    front_b64 = img_to_b64(front_img)
    back_b64 = img_to_b64(back_img)
    spine_b64 = img_to_b64(spine_img)

    cover_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI for the Golden Years - KDP Cover</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --gold: #C9913D;
  --navy: #1E2A4A;
  --dark: #0A1525;
}}

body {{
  background: #333;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}}

.cover-spread {{
  width: {SPREAD_W}in;
  height: {SPREAD_H}in;
  position: relative;
  background: var(--dark);
  box-shadow: 0 10px 50px rgba(0,0,0,0.7);
  overflow: hidden;
}}

/* ===== BACK COVER (LEFT) ===== */
.back-cover {{
  position: absolute;
  top: {BLEED}in;
  left: {BLEED}in;
  width: {TRIM_W}in;
  height: {TRIM_H}in;
  overflow: hidden;
  z-index: 5;
}}

.back-bg {{
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
}}

.back-gradient {{
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: linear-gradient(135deg, rgba(10,20,40,0.95) 0%, rgba(15,28,50,0.90) 38%, rgba(15,28,50,0.40) 70%, transparent 100%);
  padding: 0.6in 0.55in;
  display: flex;
  flex-direction: column;
  justify-content: center;
}}

.back-eyebrow {{
  font-family: 'Inter', sans-serif;
  font-size: 6.5pt;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 8px;
}}

.back-title {{
  font-family: 'Playfair Display', serif;
  font-size: 16pt;
  font-weight: 900;
  color: #FFFFFF;
  line-height: 1.2;
  margin-bottom: 10px;
}}

.back-rule {{
  width: 30px;
  height: 2px;
  background: var(--gold);
  margin-bottom: 12px;
}}

.back-desc {{
  font-family: 'Inter', sans-serif;
  font-size: 7pt;
  line-height: 1.6;
  color: rgba(255,255,255,0.80);
  margin-bottom: 8px;
}}

.back-bullets {{
  list-style: none;
  padding: 0;
  margin-top: 6px;
}}

.back-bullets li {{
  font-family: 'Inter', sans-serif;
  font-size: 6.5pt;
  line-height: 1.55;
  color: rgba(255,255,255,0.72);
  padding: 2px 0 2px 9px;
  position: relative;
}}

.back-bullets li::before {{
  content: "•";
  position: absolute;
  left: 0;
  color: var(--gold);
  font-weight: 700;
}}

.back-footer {{
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 0.55in 0.55in;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}}

.barcode-box {{
  width: 1.3in;
  height: 0.8in;
  border: 1px dashed rgba(255,255,255,0.18);
  display: flex;
  align-items: center;
  justify-content: center;
}}

.barcode-label {{
  font-family: 'Inter', sans-serif;
  font-size: 5pt;
  color: rgba(255,255,255,0.25);
  text-align: center;
  line-height: 1.4;
}}

.copyright {{
  font-family: 'Inter', sans-serif;
  font-size: 5.5pt;
  color: rgba(255,255,255,0.35);
}}

/* ===== SPINE ===== */
.spine {{
  position: absolute;
  top: {BLEED}in;
  left: {BLEED + TRIM_W}in;
  width: {SPINE}in;
  height: {TRIM_H}in;
  background: linear-gradient(180deg, #060D1A 0%, #14203B 25%, #0F1C33 50%, #14203B 75%, #060D1A 100%);
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}}

.spine-line {{
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 1px;
  height: 65%;
  background: linear-gradient(180deg, transparent 0%, var(--gold) 20%, var(--gold) 80%, transparent 100%);
  opacity: 0.25;
}}

.spine-text {{
  writing-mode: vertical-rl;
  text-orientation: mixed;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  z-index: 1;
}}

.spine-title {{
  font-family: 'Playfair Display', serif;
  font-size: 7pt;
  font-weight: 900;
  color: #FFFFFF;
  letter-spacing: 2.5px;
}}

.spine-sub {{
  font-family: 'Inter', sans-serif;
  font-size: 4.5pt;
  font-weight: 600;
  color: var(--gold);
  letter-spacing: 3px;
  text-transform: uppercase;
}}

/* ===== FRONT COVER (RIGHT) ===== */
.front-cover {{
  position: absolute;
  top: {BLEED}in;
  left: {BLEED + TRIM_W + SPINE}in;
  width: {TRIM_W}in;
  height: {TRIM_H}in;
  overflow: hidden;
  z-index: 5;
}}

.front-bg {{
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
}}

.front-gradient {{
  position: absolute;
  bottom: 0; left: 0;
  width: 100%;
  background: linear-gradient(to top, rgba(253,251,247,1) 0%, rgba(253,251,247,0.92) 25%, rgba(253,251,247,0.55) 55%, transparent 100%);
  padding: 0.75in 0.6in 0.55in 0.6in;
}}

.front-tag {{
  font-family: 'Inter', sans-serif;
  font-size: 7pt;
  font-weight: 700;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 10px;
}}

.front-title {{
  font-family: 'Playfair Display', serif;
  font-size: 38pt;
  font-weight: 900;
  color: #FFFFFF;
  line-height: 1.04;
  margin-bottom: 10px;
  text-shadow: 0 2px 25px rgba(0,0,0,0.55), 0 1px 4px rgba(0,0,0,0.3);
  -webkit-font-smoothing: antialiased;
}}

.front-subtitle {{
  font-family: 'Inter', sans-serif;
  font-size: 10pt;
  font-weight: 400;
  color: rgba(255,255,255,0.88);
  letter-spacing: 0.6px;
  margin-bottom: 18px;
  text-shadow: 0 1px 10px rgba(0,0,0,0.45);
}}

.front-rule {{
  width: 48px;
  height: 2.5px;
  background: var(--gold);
  border-radius: 1px;
}}

/* ===== PRINT SETTINGS ===== */
@media print {{
  @page {{
    size: {SPREAD_W}in {SPREAD_H}in;
    margin: 0;
    bleed: {BLEED}in;
  }}
  body {{
    background: none;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .cover-spread {{ box-shadow: none; }}
}}
</style>
</head>
<body>
<div class="cover-spread">

  <!-- BACK COVER -->
  <div class="back-cover">
    <img class="back-bg" src="data:image/jpeg;base64,{back_b64}" alt="" />
    <div class="back-gradient">
      <div class="back-eyebrow">Technology for Seniors</div>
      <div class="back-title">Discover the Magic of AI<br>&mdash; Without the Confusion</div>
      <div class="back-rule"></div>
      <div class="back-desc">
        Are you hearing about <strong style="color:#fff;font-weight:600;">"AI" and "ChatGPT"</strong> everywhere but aren't sure what it means for you? Do you worry about falling behind &mdash; or being targeted by sophisticated online scams?
      </div>
      <div class="back-desc">
        This warm, easy-to-read guide breaks down complex technology into <strong style="color:#fff;font-weight:600;">simple, everyday language</strong>, tailor-made for seniors and older adults who want to embrace the digital age with confidence.
      </div>
      <ul class="back-bullets">
        <li>What AI really is &mdash; and why it's not science fiction</li>
        <li>Step-by-step guides to ChatGPT, voice assistants &amp; smart apps</li>
        <li>How to spot deepfakes, voice clones &amp; protect your privacy</li>
        <li>The foolproof "Safe Word" strategy against AI scams</li>
        <li>AI for hobbies, health, travel &amp; staying connected to loved ones</li>
      </ul>
      <div class="back-footer">
        <div class="copyright">&copy; 2025 &bull; All rights reserved</div>
        <div class="barcode-box">
          <div class="barcode-label">ISBN<br>BARCODE<br>HERE</div>
        </div>
      </div>
    </div>
  </div>

  <!-- SPINE -->
  <div class="spine">
    <div class="spine-line"></div>
    <div class="spine-text">
      <div class="spine-title">AI for the Golden Years</div>
      <div class="spine-sub">The Complete Senior's Companion</div>
    </div>
  </div>

  <!-- FRONT COVER -->
  <div class="front-cover">
    <img class="front-bg" src="data:image/jpeg;base64,{front_b64}" alt="" />
    <div class="front-gradient">
      <div class="front-tag">The Complete Senior's Companion</div>
      <div class="front-title">AI for the<br>Golden Years</div>
      <div class="front-subtitle">Your Friendly Guide to Everyday Magic &amp; Staying Safe</div>
      <div class="front-rule"></div>
    </div>
  </div>

</div>
</body>
</html>'''

    html_path = os.path.join(OUTPUT, "cover.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(cover_html)
    print(f"HTML saved: {html_path}")
    return html_path


def generate_pdf(html_path):
    """Generate PDF via Chrome headless."""
    print("\n=== Generating Cover PDF ===")
    pdf_path = os.path.join(OUTPUT, "Cover_KDP.pdf")
    html_abs = os.path.abspath(html_path)
    pdf_abs = os.path.abspath(pdf_path)
    file_url = 'file:///' + html_abs.replace('\\', '/')

    result = subprocess.run([
        CHROME,
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        '--no-pdf-header-footer',
        f'--print-to-pdf={pdf_abs}',
        '--no-margins',
        '--window-size=5800,4200',
        file_url
    ], check=False, capture_output=True, text=True, timeout=90)

    if result.returncode == 0 and os.path.exists(pdf_abs):
        size_mb = os.path.getsize(pdf_abs) / (1024 * 1024)
        print(f"Cover PDF: {pdf_abs} ({size_mb:.1f} MB)")
        return pdf_path
    else:
        print(f"ERROR generating PDF: code={result.returncode}")
        if result.stderr:
            print(result.stderr[:300])
        return None


def add_metadata(pdf_path):
    """Add TrimBox/BleedBox to cover PDF."""
    print("\n=== Adding PDF metadata ===")
    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.generic import RectangleObject

    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    bleed_w = SPREAD_W * 72
    bleed_h = SPREAD_H * 72
    trim_w = bleed_w - BLEED * 72 * 2
    trim_h = bleed_h - BLEED * 72 * 2
    ox = (bleed_w - trim_w) / 2
    oy = (bleed_h - trim_h) / 2

    for page in reader.pages:
        page.mediabox = RectangleObject([0, 0, bleed_w, bleed_h])
        page.trimbox = RectangleObject([ox, oy, ox + trim_w, oy + trim_h])
        page.bleedbox = RectangleObject([0, 0, bleed_w, bleed_h])
        writer.add_page(page)

    tmp = pdf_path + '.tmp'
    with open(tmp, 'wb') as f:
        writer.write(f)
    os.replace(tmp, pdf_path)

    mb = float(reader.pages[0].mediabox.width)
    print(f"MediaBox: {mb/72:.3f}\" x {float(reader.pages[0].mediabox.height)/72:.3f}\"")
    print(f"TrimBox: {trim_w/72:.3f}\" x {trim_h/72:.3f}\"")
    print("Metadata added.")


if __name__ == '__main__':
    print("=" * 55)
    print("  KDP Paperback Cover Builder")
    print(f"  Trim: {TRIM_W}\" x {TRIM_H}\" | Spine: {SPINE:.3f}\"")
    print(f"  Spread: {SPREAD_W:.3f}\" x {SPREAD_H:.3f}\" (+{BLEED}\" bleed)")
    print(f"  Resolution: {DPI} DPI ({SPREAD_W*DPI:.0f}x{SPREAD_H*DPI:.0f}px)")
    print("=" * 55)

    front_img, back_img, spine_img = prepare_images()
    html_path = build_html(front_img, back_img, spine_img)
    pdf_path = generate_pdf(html_path)

    if pdf_path:
        add_metadata(pdf_path)
        print(f"\n=== READY FOR KDP UPLOAD ===")
        print(f"Cover PDF: {pdf_path}")
    else:
        print("\n=== FAILED ===")
        sys.exit(1)
