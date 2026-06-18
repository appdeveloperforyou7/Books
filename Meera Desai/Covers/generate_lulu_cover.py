"""
Generate Lulu-specific paperback cover for TWO_CHAINS.
Lulu dimensions: 11.848" x 8.75", spine 0.598"
"""
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pikepdf

OUT_DIR = r"D:\Kapil\Books\Meera Desai\Covers\TWO_CHAINS"
ARTWORK = r"D:\Kapil\Books\Meera Desai\Covers\TWO_CHAINS\artwork\processed_v3.png"
FONTS_DIR = r"C:\Windows\Fonts"

TRIM_W, TRIM_H = 5.5, 8.5
BLEED_IN = 0.125
LULU_SPINE_IN = 0.598
DPI = 300

FONT_BOLD = FONTS_DIR + "\\georgiab.ttf"
FONT_REG = FONTS_DIR + "\\georgia.ttf"
FONT_ITALIC = FONTS_DIR + "\\georgiai.ttf"
FONT_DEVANAGARI = FONTS_DIR + "\\mangal.ttf"

CREAM_BGR = (225, 218, 205)
DARK_BGR = (30, 25, 20)
DIM_BGR = (45, 35, 20)
GOLD_BGR = (140, 165, 200)
GOLD_RGB = (200, 165, 140)

CFG = {
    "title": "TWO CHAINS",
    "tagline": "The guardianship\nhas followed her home.",
    "series": "A Meera Desai Thriller  |  Book 2",
    "author": "KAPIL",
    "sanskrit": "\u0926\u094d\u0935\u0947 \u0936\u0943\u0919\u094d\u0916\u0932\u093e \u090f\u0915\u0902 \u0927\u0930\u094d\u092e",
    "sanskrit_latn": "Dve shrankhala ekam dharma",
    "sanskrit_meaning": "Two chains, one sacred duty",
    "accent_bgr": (20, 50, 120),
    "accent_rgb": (120, 50, 20),
}

BACK_TEXT = (
    "Six months after the Padmanabhaswamy vault opening,\n"
    "FBI agent Meera Desai investigates the murder of a\n"
    "Harvard Sanskrit scholar and discovers six stolen\n"
    "Indian artifacts scattered across America.\n"
    "\n"
    "Each artifact is a piece of a puzzle pointing to a\n"
    "second ancient repository hidden beneath the\n"
    "Newport Tower in Rhode Island for 500 years."
)


def in2px(inches):
    return int(round(inches * DPI))


def paper_bg(h, w, base=CREAM_BGR):
    bg = np.full((h, w, 3), base, dtype=np.uint8)
    noise = np.random.normal(0, 6, (h, w, 3)).astype(np.float32)
    return np.clip(bg.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def smart_crop(img, tw, th):
    h, w = img.shape[:2]
    s = max(tw / w, th / h)
    nw, nh = max(1, int(w * s)), max(1, int(h * s))
    r = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    sx, sy = max(0, (nw - tw) // 2), max(0, (nh - th) // 2)
    return r[sy:sy + th, sx:sx + tw]


def _text_width(text, font_path, font_size, letter_spacing=0):
    font = ImageFont.truetype(font_path, font_size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1), (0, 0, 0, 0)))
    if letter_spacing > 0:
        total = 0
        for ch in list(text):
            bb = tmp.textbbox((0, 0), ch, font=font)
            total += (bb[2] - bb[0]) + letter_spacing
        total -= letter_spacing
        return total
    bb = tmp.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]


def _autofit_font(text, font_path, max_width, start_size, letter_spacing=0, min_size=20):
    lines = text.split("\n")
    size = start_size
    while size > min_size:
        widest = max(_text_width(line.strip(), font_path, size, letter_spacing) for line in lines)
        if widest <= max_width:
            return size
        size -= 2
    return max(min_size, size)


def overlay_text_pro(img_bgr, text, x, y, font_path, font_size, color_rgb,
                     anchor="lt", shadow=True, glow=True, stroke=True,
                     shadow_blur=6, shadow_alpha=0.5, stroke_width=1,
                     glow_alpha=0.2, letter_spacing=0):
    h, w = img_bgr.shape[:2]
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    base = Image.fromarray(img_rgb).convert("RGBA")
    font = ImageFont.truetype(font_path, font_size)

    if letter_spacing > 0:
        chars = list(text)
        char_widths = []
        tmp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1), (0, 0, 0, 0)))
        for ch in chars:
            bb = tmp_draw.textbbox((0, 0), ch, font=font)
            char_widths.append(bb[2] - bb[0])
        total_w = sum(char_widths) + letter_spacing * (len(chars) - 1)
        bb_full = tmp_draw.textbbox((0, 0), text, font=font)
        th = bb_full[3] - bb_full[1]
    else:
        tmp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1), (0, 0, 0, 0)))
        bb = tmp_draw.textbbox((0, 0), text, font=font)
        total_w = bb[2] - bb[0]
        th = bb[3] - bb[1]

    dx, dy = x, y
    if "m" in anchor or "c" in anchor:
        dx = x - total_w // 2
    if "r" in anchor:
        dx = x - total_w
    if "b" in anchor:
        dy = y - th
    if ("m" in anchor or "c" in anchor) and "t" not in anchor and "b" not in anchor:
        dy = y - th // 2

    def draw_text_at(canvas, tx, ty, fill):
        if letter_spacing > 0:
            cx = tx
            for i, ch in enumerate(chars):
                ImageDraw.Draw(canvas).text((cx, ty), ch, font=font, fill=fill)
                cx += char_widths[i] + letter_spacing
        else:
            ImageDraw.Draw(canvas).text((tx, ty), text, font=font, fill=fill)

    composite = base

    if glow:
        for alpha_frac, blur_r in [(glow_alpha * 0.3, 10), (glow_alpha * 0.6, 5), (glow_alpha, 2)]:
            layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            draw_text_at(layer, dx, dy, (*color_rgb, int(255 * alpha_frac)))
            if blur_r > 0:
                layer = layer.filter(ImageFilter.GaussianBlur(radius=blur_r))
            composite = Image.alpha_composite(composite, layer)

    if shadow:
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw_text_at(layer, dx + shadow_blur, dy + shadow_blur,
                     (0, 0, 0, int(255 * shadow_alpha)))
        layer = layer.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
        composite = Image.alpha_composite(composite, layer)

    if stroke:
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sc = (20, 15, 10)
        for sdx in range(-stroke_width, stroke_width + 1):
            for sdy in range(-stroke_width, stroke_width + 1):
                if sdx * sdx + sdy * sdy <= stroke_width * stroke_width:
                    draw_text_at(layer, dx + sdx, dy + sdy, (*sc, 180))
        composite = Image.alpha_composite(composite, layer)

    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text_at(layer, dx, dy, (*color_rgb, 255))
    composite = Image.alpha_composite(composite, layer)

    return cv2.cvtColor(np.array(composite.convert("RGB")), cv2.COLOR_RGB2BGR)


def render_lines(canvas, text, cx, y, font_path, size, color_rgb, lh=None, **kw):
    lines = text.split("\n")
    if lh is None:
        lh = int(size * 1.3)
    for i, line in enumerate(lines):
        canvas = overlay_text_pro(canvas, line.strip(), cx, y + i * lh,
                                  font_path, size, color_rgb, anchor="mt", **kw)
    return canvas


def accent_line(canvas, cx, y, half_w, color_bgr, thick=2):
    cv2.line(canvas, (cx - half_w, y), (cx + half_w, y), color_bgr, thick, cv2.LINE_AA)
    return canvas


def compose_front(art, cfg, w, h):
    cover = smart_crop(art, w, h)
    cx = w // 2
    sw = w
    st = 0
    sb = h
    sh = sb - st
    accent = cfg["accent_rgb"]
    dark = (30, 25, 20)
    dim = (45, 35, 20)
    gold = (80, 65, 35)

    y = st + int(sh * 0.05)
    cover = overlay_text_pro(cover, cfg["series"].upper(), cx, y,
                             FONT_REG, max(18, int(sw * 0.028)), dim,
                             anchor="mt", shadow=False, glow=False, stroke=False)
    y = st + int(sh * 0.085)
    accent_line(cover, cx, y, int(sw * 0.22), cfg["accent_bgr"], 2)

    y = st + int(sh * 0.11)
    cover = overlay_text_pro(cover, cfg["sanskrit"], cx, y,
                             FONT_DEVANAGARI, max(16, int(sw * 0.026)), gold,
                             anchor="mt", shadow=False, glow=False, stroke=False)

    max_title_w = int(sw * 0.88)
    title_ls = max(2, int(sw * 0.005))
    title_fs = _autofit_font(cfg["title"], FONT_BOLD, max_title_w, max(50, int(sw * 0.10)), title_ls)
    y = st + int(sh * 0.16)
    cover = render_lines(cover, cfg["title"], cx, y, FONT_BOLD, title_fs, dark,
                         lh=int(title_fs * 1.15),
                         letter_spacing=title_ls,
                         shadow=False, glow=False, stroke=False)
    n_title = len(cfg["title"].split("\n"))
    y += n_title * int(title_fs * 1.15) + int(sh * 0.015)

    cover = overlay_text_pro(cover, cfg["author"], cx, y,
                             FONT_BOLD, max(24, int(sw * 0.05)), accent,
                             anchor="mt",
                             letter_spacing=max(3, int(sw * 0.01)),
                             shadow=False, glow=False, stroke=False)
    y += int(sh * 0.04)
    accent_line(cover, cx, y, int(sw * 0.18), cfg["accent_bgr"], 1)

    tag_fs = max(22, int(sw * 0.035))
    tag_y = st + int(sh * 0.78)
    cover = render_lines(cover, cfg["tagline"], cx, tag_y, FONT_ITALIC, tag_fs, dim,
                         shadow=False, glow=False, stroke=False)

    cover = overlay_text_pro(cover, "A NOVEL", cx, st + int(sh * 0.92),
                             FONT_REG, max(16, int(sw * 0.024)), dim,
                             anchor="mt", shadow=False, glow=False, stroke=False)
    return cover


def compose_back(art, cfg, w, h):
    cover = smart_crop(art, w, h)
    cx = w // 2
    sw = w
    st = 0
    sb = h
    sh = sb - st
    accent = cfg["accent_rgb"]
    dim = (45, 35, 20)
    dark = (30, 25, 20)

    y = st + int(sh * 0.10)
    cover = overlay_text_pro(cover, cfg["author"], cx, y,
                             FONT_BOLD, max(16, int(sw * 0.035)), accent,
                             anchor="mt", shadow=False, glow=False, stroke=False,
                             letter_spacing=max(2, int(sw * 0.006)))
    y += int(sh * 0.04)
    accent_line(cover, cx, y, int(sw * 0.18), cfg["accent_bgr"], 1)

    fs = max(12, int(sw * 0.024))
    y += int(sh * 0.03)
    lines = BACK_TEXT.split("\n")
    for line in lines:
        if line.strip() == "":
            y += int(fs * 0.5)
            continue
        cover = overlay_text_pro(cover, line, cx, y, FONT_REG, fs, dim,
                                 anchor="mt", shadow=False, glow=False, stroke=False)
        y += int(fs * 1.4)

    y += int(sh * 0.02)
    accent_line(cover, cx, y, int(sw * 0.12), cfg["accent_bgr"], 1)
    y += int(sh * 0.015)
    cover = overlay_text_pro(cover, cfg["sanskrit"], cx, y,
                             FONT_DEVANAGARI, max(10, int(sw * 0.018)),
                             (80, 65, 35), anchor="mt",
                             shadow=False, glow=False, stroke=False)
    y += int(sh * 0.025)
    cover = overlay_text_pro(cover, f'"{cfg["sanskrit_meaning"]}"', cx, y,
                             FONT_ITALIC, max(9, int(sw * 0.016)), dim,
                             anchor="mt", shadow=False, glow=False, stroke=False)

    bw, bh = int(sw * 0.32), int(sh * 0.10)
    bx = w - bw - int(sw * 0.06)
    by = sb - bh - int(sh * 0.04)
    cv2.rectangle(cover, (bx, by), (bx + bw, by + bh), (235, 228, 218), -1)
    cv2.rectangle(cover, (bx, by), (bx + bw, by + bh), dim, 1, cv2.LINE_AA)
    cover = overlay_text_pro(cover, "BARCODE", bx + bw // 2, by + bh // 2,
                             FONT_REG, max(8, int(sw * 0.012)), (180, 170, 155),
                             anchor="mm", shadow=False, glow=False, stroke=False)

    return cover


def compose_spine(w, h, cfg):
    cream = paper_bg(h, w)
    cx = w // 2
    dark = (30, 25, 20)
    accent = cfg["accent_rgb"]

    sfs = max(7, min(20, int(w * 0.30)))
    title = cfg["title"].replace("\n", " ")
    ch = max(7, int(sfs * 0.85))
    total = len(title) * ch + 50
    ys = (h - total) // 2
    for i, c in enumerate(title):
        cream = overlay_text_pro(cream, c, cx, ys + i * ch, FONT_BOLD, sfs, dark,
                                 anchor="mt", shadow=False, glow=False, stroke=False)

    cream = overlay_text_pro(cream, cfg["author"], cx, h - 40,
                             FONT_BOLD, max(5, int(sfs * 0.5)), accent,
                             anchor="mt", shadow=False, glow=False, stroke=False,
                             letter_spacing=max(1, int(sfs * 0.08)))
    return cream


def main():
    spine_px = in2px(LULU_SPINE_IN)
    tw = in2px(TRIM_W)
    th = in2px(TRIM_H)
    bl = in2px(BLEED_IN)

    full_w = 2 * (tw + bl) + spine_px
    full_h = th + 2 * bl

    expected_w = in2px(11.848)
    expected_h = in2px(8.75)

    print(f"Lulu cover specs:")
    print(f"  Spine: {LULU_SPINE_IN}\" ({spine_px}px)")
    print(f"  Full cover: {full_w}px x {full_h}px = {full_w/DPI:.3f}\" x {full_h/DPI:.3f}\"")
    print(f"  Expected:    {expected_w}px x {expected_h}px = 11.848\" x 8.750\"")

    if full_w != expected_w or full_h != expected_h:
        print(f"  WARNING: Calculated dimensions don't match expected!")
        print(f"  Adjusting to exact Lulu dimensions...")
        full_w = expected_w
        full_h = expected_h

    back_x = bl
    back_w = tw
    sp_x = bl + tw
    sp_w = full_w - 2 * tw - 2 * bl
    front_x = bl + tw + sp_w
    front_w = tw

    print(f"  Back: x={back_x}, w={back_w}")
    print(f"  Spine: x={sp_x}, w={sp_w} ({sp_w/DPI:.3f}\")")
    print(f"  Front: x={front_x}, w={front_w}")

    print("Loading artwork...")
    art = cv2.imread(ARTWORK)
    if art is None:
        print(f"ERROR: Could not load {ARTWORK}")
        sys.exit(1)
    print(f"  Artwork: {art.shape[1]}x{art.shape[0]}")

    canvas = paper_bg(full_h, full_w, CREAM_BGR)

    print("Composing front cover...")
    front = compose_front(art, CFG, front_w, full_h)
    print("Composing back cover...")
    back = compose_back(art, CFG, back_w, full_h)
    print("Composing spine...")
    spine = compose_spine(sp_w, full_h, CFG)

    canvas[:, front_x:front_x + front_w] = front
    canvas[:, back_x:back_x + back_w] = back
    canvas[:, sp_x:sp_x + sp_w] = spine

    cv2.line(canvas, (sp_x, 0), (sp_x, full_h), CFG["accent_bgr"], 1, cv2.LINE_AA)
    cv2.line(canvas, (front_x, 0), (front_x, full_h), CFG["accent_bgr"], 1, cv2.LINE_AA)

    png_path = f"{OUT_DIR}/TWO_CHAINS_Lulu_Paperback.png"
    cv2.imwrite(png_path, canvas)
    print(f"Saved PNG: {png_path}")

    pdf_path = f"{OUT_DIR}/TWO_CHAINS_Lulu_Paperback.pdf"
    tmp_pdf = f"{OUT_DIR}/TWO_CHAINS_Lulu_Paperback_tmp.pdf"
    img_rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    lulu_w_in = 11.848
    lulu_h_in = 8.75
    pil_img.save(tmp_pdf, "PDF", resolution=DPI, quality=95)

    lulu_w_pts = lulu_w_in * 72
    lulu_h_pts = lulu_h_in * 72
    pdf = pikepdf.open(tmp_pdf)
    page = pdf.pages[0]
    page.MediaBox = [0, 0, lulu_w_pts, lulu_h_pts]
    page.TrimBox = [0, 0, lulu_w_pts, lulu_h_pts]
    page.CropBox = [0, 0, lulu_w_pts, lulu_h_pts]
    pdf.save(pdf_path)
    pdf.close()

    import os
    os.remove(tmp_pdf)
    print(f"Saved PDF: {pdf_path}")
    print(f"Final PDF dimensions: {lulu_w_in:.3f}\" x {lulu_h_in:.3f}\" ({full_w}px x {full_h}px @ {DPI} DPI)")
    print("DONE")


if __name__ == "__main__":
    main()
