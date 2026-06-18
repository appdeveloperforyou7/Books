import json
import os
import pathlib
import base64
import mimetypes
from playwright.sync_api import sync_playwright
from PIL import Image
import io

PAGE_W = 8.75
PAGE_H = 8.75
VP_W = 875
VP_H = 875
SCALE = 4
# Bleed: 0.125" beyond trim (8.5"). PDF page = 8.75".
# Trim area: 8.5"×8.5" centered within 8.75"×8.75" bleed page.

ROOT = pathlib.Path(__file__).parent.resolve()
TEMPLATES = ROOT / "templates"
IMAGES = ROOT / "images"
OUTPUT = ROOT / "Output"


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def data_url(path):
    p = pathlib.Path(path).absolute()
    if not p.exists():
        return "none"
    mime = mimetypes.guess_type(str(p))[0] or "image/png"
    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"


def iucn_class(status):
    s = status.lower()
    if "critically" in s:
        return ""
    elif "endangered" in s:
        return " iucn-endangered"
    elif "vulnerable" in s:
        return " iucn-vulnerable"
    return ""


def extract_style(html):
    s = html.find("<style>")
    e = html.find("</style>")
    return html[s + 7:e] if s >= 0 and e >= 0 else ""


def extract_body(html):
    s = html.find("<body>")
    e = html.find("</body>")
    return html[s + 6:e] if s >= 0 and e >= 0 else html


def generate_book():
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(OUTPUT / "archive", exist_ok=True)

    animals = json.load(open(ROOT / "animals_data_verified.json"))
    for a in animals:
        a.setdefault("is_spread", False)
        a.setdefault("focal_x", "center")
        a.setdefault("focal_y", "center")

    sample_tpl = read(TEMPLATES / "sample_page.html")
    cover_tpl = read(TEMPLATES / "cover_page.html")
    toc_tpl = read(TEMPLATES / "toc_page.html")
    divider_tpl = read(TEMPLATES / "divider_page.html")
    copyright_tpl = read(TEMPLATES / "copyright_page.html")
    back_tpl = read(TEMPLATES / "back_cover.html")

    quotes = [
        ("The greatness of a nation and its moral progress can be judged by the way its animals are treated.", "Mahatma Gandhi"),
        ("Wildlife is something which man cannot construct. Once it is gone, it is gone forever.", "Joy Adamson"),
        ("The only way to save a rhinoceros is to save the environment in which it lives.", "David Attenborough"),
        ("Nature provides a free lunch, but only if we control our appetites.", "William Ruckelshaus"),
        ("Every creature is a word of God.", "Meister Eckhart"),
        ("The more clearly we can focus our attention on the wonders and realities of the universe about us, the less taste we shall have for destruction.", "Rachel Carson"),
        ("In nature, nothing is perfect and everything is perfect.", "Alice Walker"),
        ("Until one has loved an animal, a part of one's soul remains unawakened.", "Anatole France"),
        ("The love for all living creatures is the most noble attribute of man.", "Charles Darwin"),
        ("Look deep into nature, and then you will understand everything better.", "Albert Einstein"),
        ("The earth has music for those who listen.", "William Shakespeare"),
        ("Plans to protect air and water, wilderness and wildlife are in fact plans to protect man.", "Stewart Udall"),
        ("Conservation is a cause that has no end. There is no point at which we will say our work is finished.", "Rachel Carson"),
        ("The animal world has much to teach us, and some of it is about being human.", "Robert Brault"),
        ("Heaven is under our feet as well as over our heads.", "Henry David Thoreau"),
        ("Earth provides enough to satisfy every man's needs, but not every man's greed.", "Mahatma Gandhi"),
        ("Nature is not a place to visit. It is home.", "Gary Snyder"),
        ("An animal's eyes have the power to speak a great language.", "Martin Buber"),
        ("Wild animals are less wild and more human than many humans of this world.", "Munia Khan"),
        ("The wildness of our souls meets the wildness of the world.", "Nature"),
    ]
    qi = 0

    pages = []

    # 1) Cover
    bg = data_url(IMAGES / "forest_cover_bg.png")
    pages.append(cover_tpl.replace("{{COVER_BG_IMAGE}}", bg))

    # 2) Copyright
    pages.append(copyright_tpl)

    # 3) TOC
    toc_entries = []
    pg = 4
    for a in animals:
        if a["is_spread"]:
            if pg % 2 != 0:
                pg += 1
        toc_entries.append(
            f'<div class="toc-item"><span class="toc-name">{a["name"]}</span>'
            f'<div class="toc-dots"></div>'
            f'<span class="toc-page">{pg}</span></div>'
        )
        pg += 2 if a["is_spread"] else 1
    pages.append(toc_tpl.replace("{{TOC_ITEMS}}", "\n".join(toc_entries)))

    # Animal pages
    pg = 4
    for a in animals:
        img_path = ROOT / a["image_url"]
        if not img_path.exists():
            print(f"  MISSING: {a['name']} -> {a['image_url']}")
        abs_img = f"file:///{img_path.absolute().as_posix()}"
        box = a.get("BOX_POSITION", "pos-bottom-right")
        fx = a.get("focal_x", "center")
        fy = a.get("focal_y", "center")
        iucn_cls = iucn_class(a.get("iucn_status", ""))

        if a["is_spread"]:
            if pg % 2 != 0:
                qt, qa = quotes[qi % len(quotes)]
                qi += 1
                pages.append(divider_tpl.replace("{{QUOTE_TEXT}}", qt).replace("{{QUOTE_AUTHOR}}", qa))
                pg += 1

            # Left page - full-bleed photo with minimal name label, face-centered
            left = sample_tpl
            left = left.replace("{{IMAGE_URL}}", abs_img)
            left = left.replace("{{ANIMAL_NAME}}", a["name"])
            left = left.replace("{{IUCN_STATUS}}", a.get("iucn_status", ""))
            left = left.replace("{{IUCN_CLASS}}", iucn_cls)
            left = left.replace("{{EST_POPULATION}}", a.get("est_population", ""))
            left = left.replace("{{PRIMARY_THREAT}}", a.get("primary_threat", ""))
            left = left.replace("{{WHERE_FOUND}}", a.get("where_found", ""))
            left = left.replace("{{BOX_POSITION}}", box)
            left = left.replace("{{FOCAL_X}}", "center")
            left = left.replace("{{FOCAL_Y}}", "center")
            left = left.replace("{{IMAGE_FIT}}", "cover")
            left = left.replace("{{SPREAD_OVERLAY}}", "")
            left = left.replace('class="info-box', 'class="info-box info-box-minimal')

            # Right page - photo with different focal point + compact info box
            right = sample_tpl
            right = right.replace("{{IMAGE_URL}}", abs_img)
            right = right.replace("{{ANIMAL_NAME}}", a["name"])
            right = right.replace("{{IUCN_STATUS}}", a.get("iucn_status", ""))
            right = right.replace("{{IUCN_CLASS}}", iucn_cls)
            right = right.replace("{{EST_POPULATION}}", a.get("est_population", ""))
            right = right.replace("{{PRIMARY_THREAT}}", a.get("primary_threat", ""))
            right = right.replace("{{WHERE_FOUND}}", a.get("where_found", ""))
            right = right.replace("{{BOX_POSITION}}", "pos-bottom-right")
            fx_right = {"left":"right","right":"left","center":"center"}.get(fx,"right")
            right = right.replace("{{FOCAL_X}}", fx_right)
            right = right.replace("{{FOCAL_Y}}", fy)
            right = right.replace("{{IMAGE_FIT}}", "cover")
            right = right.replace("{{SPREAD_OVERLAY}}", '<div class="spread-right-overlay"></div>')
            right = right.replace('class="info-box', 'class="info-box info-box-spread')

            pages.append(left)
            pages.append(right)
            pg += 2
        else:
            h = sample_tpl
            h = h.replace("{{IMAGE_URL}}", abs_img)
            h = h.replace("{{ANIMAL_NAME}}", a["name"])
            h = h.replace("{{IUCN_STATUS}}", a.get("iucn_status", ""))
            h = h.replace("{{IUCN_CLASS}}", iucn_cls)
            h = h.replace("{{EST_POPULATION}}", a.get("est_population", ""))
            h = h.replace("{{PRIMARY_THREAT}}", a.get("primary_threat", ""))
            h = h.replace("{{WHERE_FOUND}}", a.get("where_found", ""))
            h = h.replace("{{BOX_POSITION}}", box)
            h = h.replace("{{FOCAL_X}}", fx)
            h = h.replace("{{FOCAL_Y}}", fy)
            h = h.replace("{{IMAGE_FIT}}", a.get("image_fit", "cover"))
            h = h.replace("{{SPREAD_OVERLAY}}", "")
            pages.append(h)
            pg += 1

    # Pad to even
    if pg % 2 != 0:
        qt, qa = quotes[qi % len(quotes)]
        qi += 1
        pages.append(divider_tpl.replace("{{QUOTE_TEXT}}", qt).replace("{{QUOTE_AUTHOR}}", qa))
        pg += 1

    # Back cover
    bg2 = data_url(IMAGES / "forest_cover_bg.png")
    pages.append(back_tpl.replace("{{BACK_BG_IMAGE}}", bg2))
    pg += 1
    total = pg - 1

    # Assemble HTML
    all_css = "\n".join(extract_style(p) for p in pages)
    bodies = [extract_body(p) for p in pages]

    full = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Chronicles of the Endangered</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
{all_css}
@page {{ size: {PAGE_W}in {PAGE_H}in; margin: 0; }}
body,html {{ margin:0!important; padding:0!important; background:#000!important; overflow:visible!important; width:{PAGE_W}in!important; height:auto!important; font-family:'Montserrat',sans-serif!important; }}
.pw {{ width:{PAGE_W}in!important; height:{PAGE_H}in!important; margin:0!important; padding:0!important; position:relative!important; overflow:hidden!important; background:#111!important; display:block!important; box-sizing:border-box!important; page-break-after:always; }}
</style>
</head>
<body>
{"".join(f'<div class="pw">{b}</div>' for b in bodies)}
</body>
</html>"""

    draft = ROOT / "book_draft.html"
    draft.write_text(full, encoding="utf-8")
    print(f"Generated {total} pages to {draft}")

    # Render PDF
    pdf = OUTPUT / "Chronicles_of_the_Endangered.pdf"
    print(f"Rendering {pdf}...")
    try:
        url = "file://" + draft.absolute().as_posix()
        with sync_playwright() as pw:
            br = pw.chromium.launch(args=["--disable-dev-shm-usage", "--no-sandbox"])
            tab = br.new_page(viewport={"width": VP_W, "height": VP_H}, device_scale_factor=SCALE)
            tab.goto(url, wait_until="networkidle", timeout=120000)
            tab.wait_for_timeout(5000)
            wraps = tab.query_selector_all(".pw")
            imgs = []
            audit = ROOT / "temp_audit"
            audit.mkdir(exist_ok=True)
            print(f"Capturing {len(wraps)} pages...")
            for i, w in enumerate(wraps):
                print(f"  {i+1}/{len(wraps)}...", end="\r")
                w.scroll_into_view_if_needed(timeout=60000)
                tab.wait_for_timeout(300)
                raw = w.screenshot(type="jpeg", quality=92)
                pil_img = Image.open(io.BytesIO(raw))
                pil_img.save(audit / f"page_{i+1:02d}.jpg", "JPEG", quality=92)
                imgs.append(pil_img)
            print(f"\nGenerating PDF...")
            import fitz as fp
            pdf_doc = fp.open()
            for i, img in enumerate(imgs):
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=92)
                page = pdf_doc.new_page(width=630, height=630)
                page.insert_image(page.rect, stream=buf.getvalue())
            pdf_doc.save(str(pdf), deflate=True)
            pdf_doc.close()
        print(f"SUCCESS! {pdf} ({total} pages)")
        import shutil
        v = 15
        while (OUTPUT / "archive" / f"book_premium_kdp_v{v}.pdf").exists():
            v += 1
        shutil.copy2(str(pdf), str(OUTPUT / "archive" / f"book_premium_kdp_v{v}.pdf"))
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    generate_book()
