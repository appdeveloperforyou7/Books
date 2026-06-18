"""
The Fourth Step — KDP Cover Generator
Generates all 3 formats: Kindle eBook, Paperback, Hardcover
Fully KDP-compliant with bleed, safe margins, embedded fonts.
"""

import os
import sys
import math
import numpy as np
import cv2
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = r"D:\Kapil\Books\The Fourth Step"
COVER_DIR = os.path.join(BASE, "Cover")
OUTPUT_DIR = COVER_DIR
SOURCE_IMG = os.path.join(COVER_DIR, "Paperback2.png")

TRIM_W, TRIM_H = 5.5, 8.5
DPI = 300
BLEED = 0.125
SAFE = 0.375

PAGES_WHITE = 262
SPINE_WHITE = PAGES_WHITE * 0.002252

PAGES_HARDCOVER = PAGES_WHITE
BOARD_THICKNESS = 0.063
SPINE_HARDCOVER = SPINE_WHITE + 2 * BOARD_THICKNESS

FONTS_DIR = r"C:\Windows\Fonts"

DARK_BG = (15, 12, 10)
WARM_BLACK = (22, 18, 15)
GOLD = (196, 162, 108)
OFF_WHITE = (245, 240, 232)
CREAM = (252, 248, 240)
MUTED_TEXT = (180, 172, 158)
DIM_TEXT = (120, 112, 100)


def register_fonts():
    fonts = [
        ("Georgia", os.path.join(FONTS_DIR, "georgia.ttf")),
        ("GeorgiaBold", os.path.join(FONTS_DIR, "georgiab.ttf")),
        ("GeorgiaItalic", os.path.join(FONTS_DIR, "georgiai.ttf")),
        ("Arial", os.path.join(FONTS_DIR, "arial.ttf")),
        ("ArialBold", os.path.join(FONTS_DIR, "arialbd.ttf")),
        ("Constan", os.path.join(FONTS_DIR, "constan.ttf")),
        ("ConstanBold", os.path.join(FONTS_DIR, "constanb.ttf")),
    ]
    for name, path in fonts:
        if os.path.isfile(path):
            pdfmetrics.registerFont(TTFont(name, path))


def pil_font(name, size):
    size = int(size)
    candidates = []
    font_map = {
        "Georgia": ["georgia.ttf", "Georgia.ttf"],
        "GeorgiaBold": ["georgiab.ttf", "georgiab.ttf"],
        "GeorgiaItalic": ["georgiai.ttf"],
        "Constan": ["constan.ttf", "constan.ttf"],
        "ConstanBold": ["constanb.ttf", "constanb.ttf"],
        "Arial": ["arial.ttf"],
        "ArialBold": ["arialbd.ttf"],
        "Times": ["times.ttf"],
        "TimesBold": ["timesbd.ttf"],
    }
    for variant in font_map.get(name, [name]):
        candidates.append(os.path.join(FONTS_DIR, variant))
    for path in candidates:
        if os.path.isfile(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def crop_front_art():
    img = Image.open(SOURCE_IMG).convert("RGB")
    target_ratio = TRIM_W / TRIM_H
    iw, ih = img.size
    target_w = int(ih * target_ratio)
    left = (iw - target_w) // 2
    cropped = img.crop((left, 0, left + target_w, ih))
    print(f"  Cropped front art: {cropped.size}")
    return cropped


def enhance_for_print(img, target_w_px, target_h_px):
    img = img.resize((target_w_px, target_h_px), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    img = ImageEnhance.Sharpness(img).enhance(1.3)
    img = ImageEnhance.Color(img).enhance(1.1)
    return img


def draw_gradient_overlay(img, region_box, top_alpha=0, bottom_alpha=180):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    x1, y1, x2, y2 = region_box
    steps = 80
    for i in range(steps):
        frac = i / steps
        alpha = int(top_alpha + (bottom_alpha - top_alpha) * frac)
        sy = y1 + int((y2 - y1) * i / steps)
        ey = y1 + int((y2 - y1) * (i + 1) / steps)
        od.rectangle([x1, sy, x2, ey], fill=(0, 0, 0, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def draw_top_gradient(img, gradient_height_frac=0.55, max_alpha=200):
    w, h = img.size
    grad_h = int(h * gradient_height_frac)
    return draw_gradient_overlay(img, (0, 0, w, grad_h),
                                 top_alpha=max_alpha, bottom_alpha=0)


def draw_bottom_gradient(img, gradient_height_frac=0.30, max_alpha=200):
    w, h = img.size
    grad_h = int(h * gradient_height_frac)
    return draw_gradient_overlay(img, (0, h - grad_h, w, h),
                                 top_alpha=0, bottom_alpha=max_alpha)


def draw_text_centered(draw, img_w, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (img_w - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return y + (bbox[3] - bbox[1])


def draw_text_tracked(draw, x, y, text, font, fill, tracking=0):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=font, fill=fill)
        bbox = draw.textbbox((cx, y), ch, font=font)
        cx = bbox[2] + tracking


def draw_text_centered_tracked(draw, img_w, y, text, font, fill, tracking=0):
    tw = 0
    dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for i, ch in enumerate(text):
        bb = dummy.textbbox((0, 0), ch, font=font)
        tw += bb[2] - bb[0]
        if i < len(text) - 1:
            tw += tracking
    x = (img_w - tw) // 2
    draw_text_tracked(draw, x, y, text, font, fill, tracking)
    bb = draw.textbbox((x, y), text[-1], font=font)
    return bb[3]


def render_front_cover(target_w_px, target_h_px):
    art = crop_front_art()
    art = enhance_for_print(art, target_w_px, target_h_px)

    art = draw_top_gradient(art, gradient_height_frac=0.50, max_alpha=210)
    art = draw_bottom_gradient(art, gradient_height_frac=0.25, max_alpha=190)

    draw = ImageDraw.Draw(art)
    w, h = art.size
    safe_px = int(SAFE * DPI)

    title_font = pil_font("GeorgiaBold", DPI * 0.52)
    tagline_font = pil_font("GeorgiaItalic", DPI * 0.11)
    author_font = pil_font("Constan", DPI * 0.15)

    tagline_y = int(h * 0.10)
    draw_text_centered(draw, w, tagline_y,
                       "The house remembered what she could not.",
                       tagline_font, (*GOLD, 230))

    title_y = int(h * 0.18)
    title_lines = ["THE", "FOURTH", "STEP"]
    line_spacing = DPI * 0.44
    for i, line in enumerate(title_lines):
        ly = int(title_y + i * line_spacing)
        font = title_font
        alpha = 255
        draw_text_centered(draw, w, ly, line, font, (*OFF_WHITE, alpha))

    gold_y = int(title_y + len(title_lines) * line_spacing + DPI * 0.08)
    gold_w = int(DPI * 0.8)
    gold_x = (w - gold_w) // 2
    draw.rectangle([gold_x, gold_y, gold_x + gold_w, gold_y + 2],
                   fill=(*GOLD, 200))

    author_y = h - safe_px - int(DPI * 0.15)
    draw_text_centered(draw, w, author_y, "KAPIL GUPTA",
                       author_font, (*CREAM, 220))

    return art.convert("RGB")


BACK_X1 = 0
SPINE_X1 = 723
FRONT_X1 = 836
IMG_END = 1610


def split_source():
    source_path = os.path.join(COVER_DIR, "Paperback2.png")
    cv_img = cv2.imread(source_path)
    h, w = cv_img.shape[:2]

    cv_img = cv2.convertScaleAbs(cv_img, alpha=1.0, beta=0)

    back_cv = cv_img[0:h, BACK_X1:SPINE_X1].copy()
    spine_cv = cv_img[0:h, SPINE_X1:FRONT_X1].copy()
    front_cv = cv_img[0:h, FRONT_X1:IMG_END].copy()

    front_pil = Image.fromarray(cv2.cvtColor(front_cv, cv2.COLOR_BGR2RGB))
    back_pil = Image.fromarray(cv2.cvtColor(back_cv, cv2.COLOR_BGR2RGB))
    spine_pil = Image.fromarray(cv2.cvtColor(spine_cv, cv2.COLOR_BGR2RGB))

    print(f"  Split Paperback2 ({w}x{h}): back={back_pil.size}, spine={spine_pil.size}, front={front_pil.size}")

    return back_pil, spine_pil, front_pil


def fix_f_color(front_cv):
    fh, fw = front_cv.shape[:2]
    y1 = int(fh * 0.80)
    y2 = int(fh * 0.90)

    the_region = front_cv[y1:y2, 200:260]
    _, the_bright = cv2.threshold(cv2.cvtColor(the_region, cv2.COLOR_BGR2GRAY), 100, 255, cv2.THRESH_BINARY)
    the_px = the_region[the_bright > 0]
    if len(the_px) < 10:
        print("  F fix: THE reference not found")
        return front_cv
    ref_avg = np.mean(the_px.astype(float), axis=0)

    f_region = front_cv[y1:y2, 260:290]
    _, f_bright = cv2.threshold(cv2.cvtColor(f_region, cv2.COLOR_BGR2GRAY), 100, 255, cv2.THRESH_BINARY)
    f_px = f_region[f_bright > 0]
    if len(f_px) < 5:
        print("  F fix: F pixels not found")
        return front_cv
    f_avg = np.mean(f_px.astype(float), axis=0)

    diff = np.max(np.abs(ref_avg - f_avg))
    if diff < 5:
        print(f"  F fix: already matching (diff={diff:.0f}), skipping")
        return front_cv

    ratio = ref_avg / np.maximum(f_avg, 1)
    print(f"  F fix: ref(THE)=({ref_avg[0]:.0f},{ref_avg[1]:.0f},{ref_avg[2]:.0f}) F=({f_avg[0]:.0f},{f_avg[1]:.0f},{f_avg[2]:.0f}) ratio=({ratio[0]:.3f},{ratio[1]:.3f},{ratio[2]:.3f})")

    rows, cols = np.where(f_bright > 0)
    abs_rows = y1 + rows
    abs_cols = 260 + cols
    for ch in range(3):
        front_cv[abs_rows, abs_cols, ch] = np.clip(
            front_cv[abs_rows, abs_cols, ch].astype(float) * ratio[ch], 0, 255
        ).astype(np.uint8)

    print("  F fix: recolored F to match THE")
    return front_cv


def add_barcode_box(back_img, bottom_pad=0):
    w, h = back_img.size
    bw = int(2.0 * DPI)
    bh = int(1.2 * DPI)
    margin = int(0.25 * DPI)
    bx = w - margin - bw
    by = h - bottom_pad - margin - bh
    draw = ImageDraw.Draw(back_img)
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255))
    print(f"  Barcode box: ({bx},{by}) {bw}x{bh}px, margin=0.25\" from trim right/bottom")
    return back_img


def build_paperback_from_image():
    print(f"\n=== Paperback Cover ===")
    back_img, spine_img, front_img = split_source()

    trim_w_px = int(TRIM_W * DPI)
    trim_h_px = int(TRIM_H * DPI)
    bleed_px = int(BLEED * DPI)
    spine_w_px = int(SPINE_WHITE * DPI)

    back_w = trim_w_px + bleed_px
    back_h = trim_h_px + 2 * bleed_px

    spine_w = spine_w_px
    spine_h = trim_h_px + 2 * bleed_px

    front_w = trim_w_px + bleed_px
    front_h = trim_h_px + 2 * bleed_px

    total_w = back_w + spine_w + front_w
    total_h = back_h

    print(f"  Back: {back_w}x{back_h}, Spine: {spine_w}x{spine_h}, Front: {front_w}x{front_h}")
    print(f"  Total spread: {total_w/DPI:.3f}\" x {total_h/DPI:.3f}\" ({total_w}x{total_h}px)")

    back_img = back_img.resize((back_w, back_h), Image.LANCZOS)
    spine_img = spine_img.resize((spine_w, spine_h), Image.LANCZOS)
    front_img = front_img.resize((front_w, front_h), Image.LANCZOS)

    back_img = add_barcode_box(back_img, bottom_pad=bleed_px)

    full = Image.new("RGB", (total_w, total_h))
    full.paste(back_img, (0, 0))
    full.paste(spine_img, (back_w, 0))
    full.paste(front_img, (back_w + spine_w, 0))

    temp_png = os.path.join(OUTPUT_DIR, "_cover_temp.png")
    full.save(temp_png, "PNG", dpi=(DPI, DPI))

    register_fonts()

    pdf_w = total_w / DPI * inch
    pdf_h = total_h / DPI * inch
    pdf_path = os.path.join(OUTPUT_DIR, "The_Fourth_Step_Paperback.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(pdf_w, pdf_h))
    c.drawImage(temp_png, 0, 0, width=pdf_w, height=pdf_h)
    c.showPage()
    c.save()
    os.remove(temp_png)

    fsize = os.path.getsize(pdf_path)
    print(f"  Output: {pdf_path}")
    print(f"  Size: {fsize / 1024:.0f} KB")
    return pdf_path


def build_kindle():
    print("\n=== Kindle eBook Cover ===")
    kindle_w, kindle_h = 1600, 2560
    print(f"  Target: {kindle_w}x{kindle_h} px (portrait 1.6:1)")

    _, _, front_img = split_source()
    print(f"  Front panel: {front_img.size}")

    front_img = front_img.resize((kindle_w, kindle_h), Image.LANCZOS)
    front_img = ImageEnhance.Sharpness(front_img).enhance(1.1)

    out_path = os.path.join(OUTPUT_DIR, "The_Fourth_Step_Kindle.jpg")
    front_img.save(out_path, "JPEG", quality=95)
    fsize = os.path.getsize(out_path)
    print(f"  Output: {out_path}")
    print(f"  Size: {fsize / 1024:.0f} KB ({kindle_w}x{kindle_h})")
    return out_path


def render_back_cover(target_w_px, target_h_px):
    back = Image.new("RGB", (target_w_px, target_h_px), WARM_BLACK)

    source = Image.open(SOURCE_IMG).convert("RGB")
    iw, ih = source.size
    floor_plan_region = source.crop((int(iw * 0.7), int(ih * 0.3),
                                     iw, ih))
    floor_plan_region = floor_plan_region.resize((target_w_px, target_h_px),
                                                  Image.LANCZOS)
    floor_plan_region = ImageEnhance.Brightness(floor_plan_region).enhance(0.15)
    floor_plan_region = ImageEnhance.Contrast(floor_plan_region).enhance(0.5)

    back_rgba = back.convert("RGBA")
    floor_rgba = floor_plan_region.convert("RGBA")
    floor_rgba.putalpha(60)
    back_rgba = Image.alpha_composite(back_rgba, floor_rgba)

    draw = ImageDraw.Draw(back_rgba)
    w = target_w_px
    safe = int(SAFE * DPI)

    title_font = pil_font("GeorgiaBold", int(DPI * 0.18))
    draw_text_centered(draw, w, int(DPI * 0.5), "THE FOURTH STEP",
                       title_font, (*GOLD, 200))

    sep_y = int(DPI * 0.75)
    sep_w = int(DPI * 1.5)
    sep_x = (w - sep_w) // 2
    draw.rectangle([sep_x, sep_y, sep_x + sep_w, sep_y + 2],
                   fill=(*GOLD, 150))

    body_font = pil_font("Georgia", int(DPI * 0.092))
    body_italic = pil_font("GeorgiaItalic", int(DPI * 0.092))
    leading = int(DPI * 0.14)
    text_x = safe + int(DPI * 0.15)
    max_w = w - 2 * safe - int(DPI * 0.3)

    blurb_lines = [
        ("Some houses don't forget. They wait.", True),
        ("", False),
        ("Twenty-five years ago, a girl died at a sleepover on the "
         "Mornington Peninsula. The case was closed. The house was "
         "renovated. Everyone moved on.", False),
        ("", False),
        ("Now four women have returned to the house on the coast \u2014 "
         "each remembering that night differently, each hiding "
         "something, each lying to themselves.", False),
        ("", False),
        ("Neve can't trust her own memories. Saskia measures "
         "everything because measurement doesn't lie. Imogen is "
         "running from a past that's catching up. And Rowan \u2014 "
         "the stranger among them \u2014 is documenting every crack "
         "in every story.", False),
        ("", False),
        ("Someone knows what happened to Kiera.", False),
        ("Someone has known all along.", False),
    ]

    y = int(DPI * 0.90)
    for text, is_italic in blurb_lines:
        if text == "":
            y += int(leading * 0.4)
            continue
        font = body_italic if is_italic else body_font
        words = text.split()
        line = ""
        for word in words:
            test = line + " " + word if line else word
            bb = draw.textbbox((0, 0), test, font=font)
            if bb[2] - bb[0] <= max_w:
                line = test
            else:
                if line:
                    draw.text((text_x, y), line, font=font, fill=(*CREAM, 210))
                    y += leading
                line = word
        if line:
            draw.text((text_x, y), line, font=font, fill=(*CREAM, 210))
            y += leading

    y += int(DPI * 0.15)
    comp_font = pil_font("Constan", int(DPI * 0.08))
    comp_text = "For readers of Gone Girl and The Girl on the Train."
    draw_text_centered(draw, w, y, comp_text, comp_font, (*GOLD, 180))

    barcode_w = int(2.0 * DPI)
    barcode_h = int(1.2 * DPI)
    barcode_x = w - safe - int(DPI * 0.2) - barcode_w
    barcode_y = target_h_px - safe - int(DPI * 0.1) - barcode_h
    draw.rectangle([barcode_x, barcode_y,
                     barcode_x + barcode_w, barcode_y + barcode_h],
                   fill=(255, 255, 255, 255))

    copy_font = pil_font("Arial", int(DPI * 0.06))
    copy_text = "\u00a9 2026 Kapil Gupta. All rights reserved."
    draw.text((safe + int(DPI * 0.1), target_h_px - safe - int(DPI * 0.08)),
              copy_text, font=copy_font, fill=(*DIM_TEXT, 150))

    return back_rgba.convert("RGB")


def render_spine(spine_w_px, total_h_px):
    spine = Image.new("RGB", (spine_w_px, total_h_px), DARK_BG)
    draw = ImageDraw.Draw(spine)

    gold_rgb = (GOLD[0], GOLD[1], GOLD[2])
    dim_gold = tuple(max(0, c - 80) for c in gold_rgb)

    draw.line([(2, int(DPI * 0.3)), (2, total_h_px - int(DPI * 0.3))],
              fill=dim_gold, width=1)
    draw.line([(spine_w_px - 3, int(DPI * 0.3)),
                (spine_w_px - 3, total_h_px - int(DPI * 0.3))],
              fill=dim_gold, width=1)

    if spine_w_px > 40:
        spine_font_size = min(int(DPI * 0.14), int(spine_w_px * 0.55))
        spine_font = pil_font("GeorgiaBold", spine_font_size)
        author_font_size = min(int(DPI * 0.08), int(spine_w_px * 0.35))
        author_font = pil_font("Constan", author_font_size)

        title_text = "THE FOURTH STEP"
        author_text = "KAPIL GUPTA"

        dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        tw_bbox = dummy.textbbox((0, 0), title_text, font=spine_font)
        tw = tw_bbox[2] - tw_bbox[0]
        th = tw_bbox[3] - tw_bbox[1]
        aw_bbox = dummy.textbbox((0, 0), author_text, font=author_font)
        aw = aw_bbox[2] - aw_bbox[0]
        ah = aw_bbox[3] - aw_bbox[1]

        gap = int(DPI * 0.25)
        total_text_len = tw + gap + aw
        start_x = (total_h_px - total_text_len) // 2

        text_surface_w = total_h_px
        text_surface_h = spine_w_px
        text_surface = Image.new("RGBA", (text_surface_w, text_surface_h),
                                  (0, 0, 0, 0))
        td = ImageDraw.Draw(text_surface)

        td.text((start_x, (spine_w_px - th) // 2), title_text,
                font=spine_font, fill=(*OFF_WHITE, 220))
        td.text((start_x + tw + gap, (spine_w_px - ah) // 2), author_text,
                font=author_font, fill=(*GOLD, 180))

        rotated = text_surface.rotate(-90, expand=False, resample=Image.BICUBIC)

        spine_rgba = spine.convert("RGBA")
        paste_x = max(0, (spine_w_px - rotated.width) // 2)
        paste_y = max(0, (total_h_px - rotated.height) // 2)

        temp = Image.new("RGBA", (spine_w_px, total_h_px), (0, 0, 0, 0))
        temp.paste(rotated, (paste_x, paste_y), rotated)
        spine_rgba = Image.alpha_composite(spine_rgba, temp)
        spine = spine_rgba.convert("RGB")

    return spine


HC_TOTAL_W = 13.354
HC_TOTAL_H = 9.917
HC_SPINE = 0.937


def build_hardcover():
    print(f"\n=== Hardcover Cover ===")
    back_img, spine_img, front_img = split_source()

    total_w = 4006
    total_h = int(round(HC_TOTAL_H * DPI))
    spine_px = int(round(HC_SPINE * DPI))
    trim_w_px = int(TRIM_W * DPI)
    trim_h_px = int(TRIM_H * DPI)

    back_w = (total_w - spine_px) // 2
    front_w = total_w - back_w - spine_px
    wrap_side = back_w - trim_w_px
    wrap_tb = (total_h - trim_h_px) // 2

    print(f"  Back: {back_w}x{total_h}, Spine: {spine_px}x{total_h}, Front: {front_w}x{total_h}")
    print(f"  Spine: {HC_SPINE:.3f}\" ({spine_px}px)")
    print(f"  Wrap: side={wrap_side}px ({wrap_side/DPI:.3f}\"), top/bot={wrap_tb}px ({wrap_tb/DPI:.3f}\")")
    print(f"  Total: {total_w/DPI:.3f}\" x {total_h/DPI:.3f}\" ({total_w}x{total_h}px)")

    back_trim = back_img.resize((trim_w_px, trim_h_px), Image.LANCZOS)
    spine_trim = spine_img.resize((spine_px, trim_h_px), Image.LANCZOS)
    front_trim = front_img.resize((trim_w_px, trim_h_px), Image.LANCZOS)

    full = Image.new("RGB", (total_w, total_h), WARM_BLACK)
    full.paste(back_trim, (wrap_side, wrap_tb))
    full.paste(spine_trim, (back_w, wrap_tb))
    full.paste(front_trim, (back_w + spine_px, wrap_tb))

    temp_png = os.path.join(OUTPUT_DIR, "_cover_temp.png")
    full.save(temp_png, "PNG", dpi=(DPI, DPI))

    register_fonts()

    pdf_w = total_w / DPI * inch
    pdf_h = total_h / DPI * inch
    pdf_path = os.path.join(OUTPUT_DIR, "The_Fourth_Step_Hardcover.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(pdf_w, pdf_h))
    c.drawImage(temp_png, 0, 0, width=pdf_w, height=pdf_h)
    c.showPage()
    c.save()
    os.remove(temp_png)

    fsize = os.path.getsize(pdf_path)
    print(f"  Output: {pdf_path}")
    print(f"  Size: {fsize / 1024:.0f} KB")
    return pdf_path


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("THE FOURTH STEP — KDP Cover Generator")
    print("=" * 60)
    print(f"  Trim: {TRIM_W}\" x {TRIM_H}\"")
    print(f"  Pages: ~{PAGES_WHITE}")
    print(f"  Author: Kapil Gupta")

    if len(sys.argv) > 1 and sys.argv[1] == "hardcover":
        hardcover_path = build_hardcover()
        print(f"\n  Output: {hardcover_path}")
    elif len(sys.argv) > 1 and sys.argv[1] == "kindle":
        kindle_path = build_kindle()
        print(f"\n  Output: {kindle_path}")
    elif len(sys.argv) > 1 and sys.argv[1] == "paperback":
        paperback_path = build_paperback_from_image()
        print(f"\n  Output: {paperback_path}")
    else:
        kindle_path = build_kindle()
        paperback_path = build_paperback_from_image()
        hardcover_path = build_hardcover()

        print("\n" + "=" * 60)
        print("ALL COVERS GENERATED:")
        print(f"  1. Kindle:   {kindle_path}")
        print(f"  2. Paperback: {paperback_path}")
        print(f"  3. Hardcover: {hardcover_path}")
        print("=" * 60)


if __name__ == "__main__":
    main()
