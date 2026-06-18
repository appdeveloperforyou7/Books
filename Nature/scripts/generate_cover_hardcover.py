#!/usr/bin/env python3
"""Generate KDP-compliant premium book cover for 'Nature' coffee table book.

Fixes applied:
  C2 — Legible spine text (title + publisher, vertical, white on charcoal)
  C4 — Clean barcode zone (white rect, NO label text)
  M9 — Premium front title (thin font, wide tracking, off-white, shadow)
  M10 — Coherent back cover (dark overlay, serif body text, publisher footer)
"""

import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(PROJECT_ROOT, "images")
FONTS_DIR = os.path.join(SCRIPT_DIR, "fonts")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "Nature_Hardcover_Cover.pdf")

DPI = 72

TRIM_W = 8.25 * DPI
TRIM_H = 11 * DPI

# For 80-page paperback
PAGES = 116
SPINE_W = int(PAGES * 0.00225 * DPI)
BLEED = 0.125 * DPI
SPINE_W = 0.180 * DPI

BACK_X = BLEED
BACK_W = TRIM_W
SPINE_X = BACK_X + BACK_W
FRONT_X = SPINE_X + SPINE_W
FRONT_W = TRIM_W

TOTAL_W = int(BLEED + BACK_W + SPINE_W + FRONT_W + BLEED)
TOTAL_H = int(TRIM_H + 2 * BLEED)


def _resolve_font(name_variants, size):
    candidates = []
    for v in name_variants:
        custom = os.path.join(FONTS_DIR, v)
        if os.path.isfile(custom):
            candidates.append(custom)
    if sys.platform == "win32":
        win_dir = r"C:\Windows\Fonts"
        for v in name_variants:
            candidates.append(os.path.join(win_dir, v))
    for fp in candidates:
        if os.path.isfile(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def font_thin(size):
    return _resolve_font([
        "Montserrat-Thin.ttf", "segoeuil.ttf",
    ], size)


def font_light(size):
    return _resolve_font([
        "Montserrat-Light.ttf", "segoeuil.ttf",
    ], size)


def font_regular(size):
    return _resolve_font([
        "Montserrat-Regular.ttf", "segoeui.ttf",
    ], size)


def font_bold(size):
    return _resolve_font([
        "Montserrat-Bold.ttf", "segoeuib.ttf",
    ], size)


def font_serif(size):
    return _resolve_font([
        "CormorantGaramond-Regular.ttf", "georgia.ttf",
        "Times New Roman.ttf",
    ], size)


def load_and_crop(img_path, target_w, target_h):
    img = Image.open(img_path).convert("RGB")
    iw, ih = img.size
    scale = max(target_w / iw, target_h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - target_w) // 2
    top = (nh - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def draw_text_tracking(draw, xy, text, font, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        bbox = draw.textbbox((x, y), ch, font=font)
        x = bbox[2] + tracking
    return x


def tracked_text_width(text, font, tracking=0):
    w = 0
    dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for i, ch in enumerate(text):
        bbox = dummy.textbbox((0, 0), ch, font=font)
        w += bbox[2] - bbox[0]
        if i < len(text) - 1:
            w += tracking
    return w


def render_shadow_text(canvas_img, xy, text, font, fill_color,
                       shadow_offset=(1.5, 1.5), shadow_alpha=153):
    sx, sy = xy
    sox, soy = shadow_offset
    r, g, b = fill_color
    overlay = Image.new("RGBA", canvas_img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.text((sx + sox, sy + soy), text, font=font,
            fill=(0, 0, 0, shadow_alpha))
    od.text((sx, sy), text, font=font, fill=(r, g, b, 255))
    return Image.alpha_composite(canvas_img.convert("RGBA"), overlay)


def render_tracked_shadow_text(canvas_img, xy, text, font, fill_color,
                               tracking=0, shadow_offset=(1.5, 1.5),
                               shadow_alpha=153):
    sx, sy = xy
    sox, soy = shadow_offset
    r, g, b = fill_color
    overlay = Image.new("RGBA", canvas_img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    draw_text_tracking(od, (sx + sox, sy + soy), text, font,
                       (0, 0, 0, shadow_alpha), tracking)
    draw_text_tracking(od, (sx, sy), text, font,
                       (r, g, b, 255), tracking)
    return Image.alpha_composite(canvas_img.convert("RGBA"), overlay)


# ── FRONT COVER (M9) ──────────────────────────────────────────────

OFF_WHITE = (240, 237, 232)
WARM_LIGHT_GRAY = (232, 228, 222)
DESC_COLOR = (232, 228, 222)
PUBLISHER_DIM = (204, 204, 204)
SPINE_BG = (26, 26, 26)


def draw_front_cover(canvas_img):
    front_path = os.path.join(IMAGES_DIR, "_cover_front_hero.jpg")
    fw = int(FRONT_W + BLEED)
    fh = TOTAL_H
    front_bg = load_and_crop(front_path, fw, fh)
    canvas_img.paste(front_bg, (int(FRONT_X), 0))

    # Dark gradient band behind title for legibility on bright skies
    band_y = int(TRIM_H * 0.10)
    band_h = int(TRIM_H * 0.40)
    overlay = Image.new("RGBA", canvas_img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    steps = 50
    for i in range(steps):
        alpha = int(90 * (1.0 - abs(i - steps/2) / (steps/2)))
        od.rectangle([int(FRONT_X), band_y + i * band_h // steps,
                       int(FRONT_X + FRONT_W), band_y + (i + 1) * band_h // steps],
                      fill=(0, 0, 0, alpha))
    canvas_img = Image.alpha_composite(canvas_img.convert("RGBA"), overlay)

    fc_left = FRONT_X
    fc_right = FRONT_X + FRONT_W
    fc_center_x = (fc_left + fc_right) / 2

    title_font = font_thin(75)
    subtitle_font = font_light(13.5)

    title_text = "NATURE"
    subtitle_text = (
        "A Visual Journey Through Earth's Most Stunning Landscapes"
    )

    title_w = tracked_text_width(title_text, title_font, tracking=DPI * 10 / 72)
    title_x = fc_center_x - title_w / 2
    title_y = int(TRIM_H * 0.22)

    canvas_img = render_tracked_shadow_text(
        canvas_img, (title_x, title_y), title_text, title_font,
        OFF_WHITE, tracking=int(DPI * 10 / 72),
        shadow_offset=(1.5, 1.5), shadow_alpha=153,
    )

    sub_w = tracked_text_width(subtitle_text, subtitle_font,
                               tracking=int(DPI * 2 / 72))
    sub_x = fc_center_x - sub_w / 2
    sub_y = title_y + int(0.45 * DPI) + 75

    canvas_img = render_tracked_shadow_text(
        canvas_img, (sub_x, sub_y), subtitle_text, subtitle_font,
        OFF_WHITE, tracking=int(DPI * 2 / 72),
        shadow_offset=(1.2, 1.2), shadow_alpha=140,
    )

    return canvas_img


# ── BACK COVER (M10 + C4) ────────────────────────────────────────

def draw_back_cover(canvas_img):
    back_path = os.path.join(IMAGES_DIR, "_cover_back_hero.jpg")
    bw = int(BACK_W + BLEED)
    bh = TOTAL_H
    back_bg = load_and_crop(back_path, bw, bh)
    back_bg = back_bg.convert("RGBA")
    dark_overlay = Image.new("RGBA", (bw, bh), (0, 0, 0, int(255 * 0.35)))
    back_bg = Image.alpha_composite(back_bg, dark_overlay).convert("RGB")
    canvas_img.paste(back_bg, (int(BACK_X), 0))

    draw = ImageDraw.Draw(canvas_img)
    desc_font = font_serif(10.5)

    description = (
        "From snow-capped peaks that pierce the clouds to emerald "
        "jungles breathing life into the atmosphere. From arid "
        "deserts where stars touch the earth to frozen glaciers "
        "holding memories of millennia past.\n\n"
        "Fifty-five photographs. One wandering journey. One planet.\n\n"
        "This collection captures Earth's most pristine wilderness — "
        "untouched by human presence, photographed in stunning detail. "
        "A journey across continents through the lens of artists who "
        "understand that nature, at its most wild, is also at its most "
        "beautiful."
    )

    bc_left = BACK_X
    bc_right = BACK_X + BACK_W
    text_left = bc_left + int(0.7 * DPI)
    text_top = int(1.2 * DPI)
    max_text_width = int(6.5 * DPI)

    paragraphs = description.split("\n\n")
    y = text_top
    leading = 15

    for para in paragraphs:
        words = para.split()
        line = ""
        for word in words:
            test = line + " " + word if line else word
            bbox = draw.textbbox((0, 0), test, font=desc_font)
            if bbox[2] - bbox[0] <= max_text_width:
                line = test
            else:
                if line:
                    canvas_img = render_shadow_text(
                        canvas_img, (text_left, y), line, desc_font,
                        DESC_COLOR, shadow_offset=(1, 1), shadow_alpha=130,
                    )
                    y += leading
                line = word
        if line:
            canvas_img = render_shadow_text(
                canvas_img, (text_left, y), line, desc_font,
                DESC_COLOR, shadow_offset=(1, 1), shadow_alpha=130,
            )
            y += leading
        y += 6

    barcode_w = int(2.0 * DPI)
    barcode_h = int(1.3 * DPI)
    barcode_x = int(bc_right - 0.6 * DPI - barcode_w)
    barcode_y = int(TOTAL_H - 0.5 * DPI - barcode_h)

    draw = ImageDraw.Draw(canvas_img)
    draw.rectangle(
        [barcode_x, barcode_y,
         barcode_x + barcode_w, barcode_y + barcode_h],
        fill=(255, 255, 255),
    )

    pub_font = font_regular(10)
    pub_text = "Nature Publications"
    pub_w = tracked_text_width(pub_text, pub_font, tracking=int(DPI * 2 / 72))
    pub_x = bc_left + (BACK_W - pub_w) / 2
    pub_y = int(TOTAL_H - 0.4 * DPI)

    canvas_img = render_tracked_shadow_text(
        canvas_img, (pub_x, pub_y), pub_text, pub_font,
        PUBLISHER_DIM, tracking=int(DPI * 2 / 72),
        shadow_offset=(1, 1), shadow_alpha=100,
    )

    return canvas_img


# ── SPINE (C2) ────────────────────────────────────────────────────

def draw_spine(canvas_img):
    sx = int(SPINE_X)
    sw = int(SPINE_W)
    sh = TOTAL_H

    draw = ImageDraw.Draw(canvas_img)
    draw.rectangle([sx, 0, sx + sw, sh], fill=SPINE_BG)

    # Spine is only ~13pt wide — must use tiny font that fits
    # "NATURE" at 7pt bold with tight negative tracking fits in ~12pt
    spine_title_font = font_bold(7)
    spine_pub_font = font_regular(5)

    title_text = "NATURE"
    pub_text = "Nature Pub."

    # Negative tracking to fit narrow spine
    tracking_title = -1
    tracking_pub = -1

    title_w = tracked_text_width(title_text, spine_title_font,
                                 tracking=tracking_title)
    pub_w = tracked_text_width(pub_text, spine_pub_font,
                                tracking=tracking_pub)

    dummy_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    tbbox = dummy_draw.textbbox((0, 0), "N", font=spine_title_font)
    title_h = tbbox[3] - tbbox[1]
    pbbox = dummy_draw.textbbox((0, 0), "N", font=spine_pub_font)
    pub_h = pbbox[3] - pbbox[1]

    total_h = title_h + pub_h + int(0.15 * DPI)
    start_y = (sh - total_h) // 2

    spine_surface = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spine_surface)
    draw_text_tracking(sd, ((sw - title_w) // 2, start_y),
                       title_text, spine_title_font,
                       (255, 255, 255, 255), tracking_title)
    draw_text_tracking(sd, ((sw - pub_w) // 2, start_y + title_h + int(0.15 * DPI)),
                       pub_text, spine_pub_font,
                       (200, 200, 200, 255), tracking_pub)

    rotated = spine_surface.rotate(-90, expand=True, resample=Image.BICUBIC)
    rx = sx + sw // 2 - rotated.width // 2
    ry = (sh - rotated.height) // 2
    canvas_img.paste(rotated, (rx, ry), rotated)

    return canvas_img


# ── MAIN ──────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Canvas : {TOTAL_W}pt × {TOTAL_H}pt "
          f"({TOTAL_W / DPI:.3f}\" × {TOTAL_H / DPI:.3f}\")")
    print(f"Back   : x={BACK_X / DPI:.3f}\"  w={BACK_W / DPI:.2f}\"")
    print(f"Spine  : x={SPINE_X / DPI:.3f}\"  w={SPINE_W / DPI:.3f}\"")
    print(f"Front  : x={FRONT_X / DPI:.3f}\"  w={FRONT_W / DPI:.2f}\"")

    canvas_img = Image.new("RGB", (TOTAL_W, TOTAL_H), (20, 20, 22))

    canvas_img = draw_back_cover(canvas_img)
    canvas_img = draw_spine(canvas_img)
    canvas_img = draw_front_cover(canvas_img)

    temp_png = os.path.join(OUTPUT_DIR, "_cover_temp.png")
    canvas_img.save(temp_png, "PNG", dpi=(DPI, DPI))

    c = canvas.Canvas(OUTPUT_PATH,
                      pagesize=(TOTAL_W / DPI * inch, TOTAL_H / DPI * inch))
    c.drawImage(temp_png, 0, 0,
                width=TOTAL_W / DPI * inch,
                height=TOTAL_H / DPI * inch)
    c.save()

    os.remove(temp_png)

    fsize = os.path.getsize(OUTPUT_PATH)
    print(f"\nOutput : {OUTPUT_PATH}")
    print(f"Size   : {fsize / 1024:.1f} KB ({fsize:,} bytes)")
    print(f"Dims   : {TOTAL_W / DPI:.2f}\" × {TOTAL_H / DPI:.2f}\" "
          f"({TOTAL_W}×{TOTAL_H}px @ {DPI}dpi)")


if __name__ == "__main__":
    main()
