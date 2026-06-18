"""
Meera Desai Series — Bestseller Cover Generator v3
Light/cream DVC-style covers. Local Bonsai server. ALL text overlaid programmatically.
KDP-compliant dimensions. OpenCV + NumPy + PIL.
"""
from __future__ import annotations
import sys, os, time, textwrap, hashlib
from pathlib import Path
import requests
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = Path(r"D:\Kapil\Books\Meera Desai\Covers")
FONTS_DIR = Path(r"C:\Windows\Fonts")
SERVER = "http://192.168.29.7:8765"

TRIM_W, TRIM_H = 5.5, 8.5
BLEED_IN = 0.125
HC_WRAP_IN = 0.7085
HC_SPINE_EXTRA = 0.288
PPI_WHITE = 0.002252
DPI = 300
FLAP_IN = 3.5
BOARD_IN = 0.065

FONT_BOLD = str(FONTS_DIR / "georgiab.ttf")
FONT_REG = str(FONTS_DIR / "georgia.ttf")
FONT_ITALIC = str(FONTS_DIR / "georgiai.ttf")
FONT_SERIF = str(FONTS_DIR / "CENTURY.TTF")
FONT_DEVANAGARI = str(FONTS_DIR / "mangal.ttf")

HC_SAFE_MARGIN_IN = 0.716
HC_SAFE_SPINE_IN = 0.4

BOOKS = {
    "VAULT_B": {
        "title": "VAULT B",
        "tagline": "They sealed it for 2,300 years.\nNow everyone wants in.",
        "series": "A Meera Desai Thriller  |  Book 1",
        "author": "KAPIL",
        "pages": 258,
        "kdp_pb_spine": 0.642,
        "kdp_hc_spine": None,
        "sanskrit": "\u0935\u093f\u0926\u094d\u092f\u093e \u0926\u093e\u0928\u0902 \u0938\u0930\u094d\u0935\u0938\u094d\u0935 \u092a\u0930\u093f\u0930\u0915\u094d\u0937\u0923\u0940\u092f",
        "sanskrit_latn": "Vidya danam sarvasva parirakshaniyam",
        "sanskrit_meaning": "Knowledge is the greatest treasure to protect",
        "prompts": [
            "ancient Indian temple gopuram tower in warm golden hour sunlight, intricate stone carvings of Hindu deities clearly visible, warm sepia and amber tones, pale cream sky background, archaeological photography style, museum quality lighting, no text no letters no words, professional 8k",
            "ancient stone vault door with ornate carvings, warm amber side-lighting, stone surface texture detail, archaeological artifact, warm cream and gold palette, museum display, no text no letters no words, 8k quality",
        ],
        "accent_bgr": (30, 55, 140),
        "accent_rgb": (140, 55, 30),
        "brightness": 1.15,
        "overlay_alpha": 0.35,
    },
    "TWO_CHAINS": {
        "title": "TWO CHAINS",
        "tagline": "The guardianship\nhas followed her home.",
        "series": "A Meera Desai Thriller  |  Book 2",
        "author": "KAPIL",
        "pages": 239,
        "kdp_pb_spine": 0.760,
        "kdp_hc_spine": 1.031,
        "sanskrit": "\u0926\u094d\u0935\u0947 \u0936\u0943\u0919\u094d\u0916\u0932\u093e \u090f\u0915\u0902 \u0927\u0930\u094d\u092e",
        "sanskrit_latn": "Dve shrankhala ekam dharma",
        "sanskrit_meaning": "Two chains, one sacred duty",
        "prompts": [
            "six ancient Indian copper artifacts and brass vessels on warm sandstone surface, golden museum lighting from above, archaeological photography, warm sepia and copper tones, cream colored background, detailed metalwork, no text no letters no words, 8k",
            "old stone tower in warm autumn sunlight, colonial stone architecture, golden hour, warm amber and cream tones, historical landmark photography, autumn trees, no text no letters no words, 8k quality",
        ],
        "accent_bgr": (20, 50, 120),
        "accent_rgb": (120, 50, 20),
    },
    "THE_THIRD_CHAIN": {
        "title": "THE THIRD CHAIN",
        "tagline": "The vault is open.\nThe knowledge is loose.\nThe world isn't ready.",
        "series": "A Meera Desai Thriller  |  Book 3  |  The Final Novel",
        "author": "KAPIL",
        "pages": 261,
        "kdp_pb_spine": 0.653,
        "kdp_hc_spine": 0.999,
        "sanskrit": "\u0924\u0943\u0924\u0940\u092f\u0902 \u0936\u0943\u0919\u094d\u0916\u0932\u093e \u0935\u093f\u0938\u0943\u092f\u0924\u093f",
        "sanskrit_latn": "Tritiyam shrankhala visrjati",
        "sanskrit_meaning": "The third chain is released",
        "prompts": [
            "ancient Ashoka stone pillar with four lions capital in warm golden light, Sarnath India, warm sepia tones, archaeological site, warm cream and gold palette, professional monument photography, no text no letters no words, 8k quality",
            "antique world map showing trade routes across Asia, warm aged parchment paper, golden amber tones, historical cartography style, cream background, aged paper texture, no text no letters no words, 8k quality",
        ],
        "accent_bgr": (50, 60, 100),
        "accent_rgb": (100, 60, 50),
    },
}

CREAM_BGR = (225, 218, 205)
DARK_BGR = (30, 25, 20)
DIM_BGR = (100, 85, 65)
GOLD_BGR = (140, 165, 200)
GOLD_RGB = (200, 165, 140)
ACCENT_GOLD_RGB = (160, 130, 70)


def in2px(inches: float) -> int:
    return int(round(inches * DPI))


def calc_specs(pages: int, spine_pb_in: float = None, spine_hc_in: float = None):
    sp_pb = spine_pb_in if spine_pb_in else pages * PPI_WHITE
    sp_hc = spine_hc_in if spine_hc_in else pages * PPI_WHITE + HC_SPINE_EXTRA
    tw = in2px(TRIM_W)
    th = in2px(TRIM_H)
    hc_wrap = in2px(HC_WRAP_IN)
    spb = in2px(sp_pb)
    shc = in2px(sp_hc)
    pb_w_in = 2 * (TRIM_W + BLEED_IN) + sp_pb
    pb_h_in = TRIM_H + 2 * BLEED_IN
    pb_w = int(round(pb_w_in * DPI))
    pb_h = int(round(pb_h_in * DPI))
    pb_bl = (pb_h - th) // 2
    pb_sp = pb_w - 2 * tw - 2 * pb_bl
    return {
        "kindle": {"w": 1600, "h": 2560},
        "paperback": {
            "w": pb_w, "h": pb_h,
            "tw": tw, "th": th, "bl": pb_bl, "sp": pb_sp,
            "back_x": pb_bl, "back_w": tw,
            "sp_x": pb_bl + tw, "sp_w": pb_sp,
            "front_x": pb_bl + tw + pb_sp, "front_w": tw,
            "size_in": (pb_w_in, pb_h_in),
        },
        "hardcover": {
            "w": 2 * (tw + hc_wrap) + shc, "h": th + 2 * hc_wrap,
            "tw": tw, "th": th, "bl": hc_wrap, "sp": shc,
            "back_x": hc_wrap, "back_w": tw,
            "sp_x": hc_wrap + tw, "sp_w": shc,
            "front_x": hc_wrap + tw + shc, "front_w": tw,
        },
        "spine_pb_in": sp_pb,
        "spine_hc_in": sp_hc,
    }


def gen_bonsai(prompt: str, seed: int = 42, size: int = 1024) -> np.ndarray:
    r = requests.post(f"{SERVER}/generate", json={
        "prompt": prompt, "negative_prompt": "",
        "width": size, "height": size,
        "seed": seed, "guidance_scale": 3.5,
        "num_inference_steps": 28,
    }, timeout=180)
    if r.status_code == 200:
        arr = np.frombuffer(r.content, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is not None:
            return img
    raise RuntimeError(f"Bonsai error: status={r.status_code}")


def smart_crop(img: np.ndarray, tw: int, th: int) -> np.ndarray:
    h, w = img.shape[:2]
    s = max(tw / w, th / h)
    nw, nh = max(1, int(w * s)), max(1, int(h * s))
    r = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    sx, sy = max(0, (nw - tw) // 2), max(0, (nh - th) // 2)
    return r[sy:sy + th, sx:sx + tw]


def paper_bg(h: int, w: int, base: tuple = CREAM_BGR) -> np.ndarray:
    bg = np.full((h, w, 3), base, dtype=np.uint8)
    noise = np.random.normal(0, 6, (h, w, 3)).astype(np.float32)
    return np.clip(bg.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def _text_width(text: str, font_path: str, font_size: int, letter_spacing: int = 0) -> int:
    font = ImageFont.truetype(font_path, font_size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1), (0, 0, 0, 0)))
    if letter_spacing > 0:
        total = 0
        chars = list(text)
        for ch in chars:
            bb = tmp.textbbox((0, 0), ch, font=font)
            total += (bb[2] - bb[0]) + letter_spacing
        total -= letter_spacing
        return total
    bb = tmp.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]


def _autofit_font(text: str, font_path: str, max_width: int,
                  start_size: int, letter_spacing: int = 0,
                  min_size: int = 20) -> int:
    lines = text.split("\n")
    size = start_size
    while size > min_size:
        widest = max(_text_width(line.strip(), font_path, size, letter_spacing) for line in lines)
        if widest <= max_width:
            return size
        size -= 2
    return max(min_size, size)


def _save_pdf(img_bgr: np.ndarray, path: Path, dpi: int = 300,
              page_size_in: tuple = None):
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    if page_size_in:
        w_in, h_in = page_size_in
    else:
        h_px, w_px = pil_img.size[1], pil_img.size[0]
        w_in = w_px / dpi
        h_in = h_px / dpi
    pil_img.save(str(path), "PDF", resolution=dpi,
                 page_size=(w_in, h_in), quality=95)


def sepia_warm(img: np.ndarray, strength: float = 0.35) -> np.ndarray:
    img_f = img.astype(np.float32)
    b, g, r = img_f[:, :, 0], img_f[:, :, 1], img_f[:, :, 2]
    out_b = np.clip(b * 0.272 + g * 0.534 + r * 0.131, 0, 255)
    out_g = np.clip(b * 0.349 + g * 0.686 + r * 0.168, 0, 255)
    out_r = np.clip(b * 0.393 + g * 0.769 + r * 0.189, 0, 255)
    sepia = np.stack([out_b, out_g, out_r], axis=2)
    return cv2.addWeighted(img, 1.0 - strength, sepia.astype(np.uint8), strength, 0)


def brighten(img: np.ndarray, f: float = 1.2) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * f, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def desaturate(img: np.ndarray, f: float = 0.65) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] *= f
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def fade_to_cream(img: np.ndarray, top_pct: float = 0.25, bot_pct: float = 0.30) -> np.ndarray:
    h, w = img.shape[:2]
    cream = paper_bg(h, w)
    top_h = int(h * top_pct)
    bot_h = int(h * bot_pct)
    for y in range(top_h):
        a = 1.0 - (y / top_h) * 0.9
        img[y] = cv2.addWeighted(cream[y], 1 - a, img[y], a, 0)
    for y in range(h - bot_h, h):
        a = ((y - (h - bot_h)) / bot_h) * 0.85
        img[y] = cv2.addWeighted(cream[y], a, img[y], 1 - a, 0)
    return img


def process_art(imgs: list, tw: int, th: int, extra_bright: float = 1.0) -> np.ndarray:
    resized = [smart_crop(im, tw, th) for im in imgs]
    if len(resized) > 1:
        base = np.mean([r.astype(np.float64) for r in resized], axis=0).astype(np.uint8)
    else:
        base = resized[0].copy()
    base = desaturate(base, 0.75)
    base = sepia_warm(base, 0.15)
    base = brighten(base, 1.05 * extra_bright)
    return base


def overlay_text_pro(img_bgr, text, x, y, font_path, font_size, color_rgb,
                     anchor="lt", shadow=True, glow=True, stroke=True,
                     shadow_blur=6, shadow_alpha=0.5, stroke_width=1,
                     glow_alpha=0.2, letter_spacing=0,
                     halo=False, halo_color=(225, 218, 205)):
    h, w = img_bgr.shape[:2]
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    base = Image.fromarray(img_rgb).convert("RGBA")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception:
        font = ImageFont.load_default()

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

    if halo:
        for blur_r, a in [(6, 0.55), (3, 0.45), (1, 0.35)]:
            layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            draw_text_at(layer, dx, dy, (*halo_color, int(255 * a)))
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


def compose_front(art, cfg, w, h, margins_in=None):
    cover = smart_crop(art, w, h)
    if margins_in:
        mt, mb, ml, mr = (in2px(m) for m in margins_in)
    else:
        mt, mb, ml, mr = 0, 0, 0, 0
    cx = ml + (w - ml - mr) // 2
    sw = w - ml - mr
    st = mt
    sb = h - mb
    sh = sb - st
    accent = cfg["accent_rgb"]
    dark = (30, 25, 20)
    dim = (45, 35, 20)
    gold = (80, 65, 35)

    y = st + int(sh * 0.05)
    cover = overlay_text_pro(cover, cfg["series"].upper(), cx, y,
                             FONT_REG, max(18, int(sw * 0.028)), dim,
                             anchor="mt", shadow=False, glow=False, stroke=False,
                             halo=True)
    y = st + int(sh * 0.085)
    accent_line(cover, cx, y, int(sw * 0.22), cfg["accent_bgr"], 2)

    y = st + int(sh * 0.11)
    cover = overlay_text_pro(cover, cfg["sanskrit"], cx, y,
                             FONT_DEVANAGARI, max(16, int(sw * 0.026)), gold,
                             anchor="mt", shadow=False, glow=False, stroke=False,
                             halo=True)

    max_title_w = int(sw * 0.88)
    title_ls = max(2, int(sw * 0.005))
    title_fs = _autofit_font(cfg["title"], FONT_BOLD, max_title_w, max(50, int(sw * 0.10)), title_ls)
    y = st + int(sh * 0.16)
    cover = render_lines(cover, cfg["title"], cx, y, FONT_BOLD, title_fs, dark,
                         lh=int(title_fs * 1.15),
                         letter_spacing=title_ls,
                         shadow=False, glow=False, stroke=False,
                         halo=True)
    n_title = len(cfg["title"].split("\n"))
    y += n_title * int(title_fs * 1.15) + int(sh * 0.015)

    cover = overlay_text_pro(cover, cfg["author"], cx, y,
                             FONT_BOLD, max(24, int(sw * 0.05)), accent,
                             anchor="mt",
                             letter_spacing=max(3, int(sw * 0.01)),
                             shadow=False, glow=False, stroke=False,
                             halo=True)
    y += int(sh * 0.04)
    accent_line(cover, cx, y, int(sw * 0.18), cfg["accent_bgr"], 1)

    tag_fs = max(22, int(sw * 0.035))
    tag_y = st + int(sh * 0.78)
    cover = render_lines(cover, cfg["tagline"], cx, tag_y, FONT_ITALIC, tag_fs, dim,
                         shadow=False, glow=False, stroke=False,
                         halo=True)

    cover = overlay_text_pro(cover, "A NOVEL", cx, st + int(sh * 0.92),
                             FONT_REG, max(16, int(sw * 0.024)), dim,
                             anchor="mt", shadow=False, glow=False, stroke=False,
                             halo=True)
    return cover


BACK_TEXT = {
    "VAULT_B": (
        "When India's Supreme Court orders the opening of\n"
        "a sealed temple vault rumored to hold a trillion\n"
        "dollars in treasure, FBI art-crime specialist Meera\n"
        "Desai discovers that the gold is a smokescreen.\n"
        "\n"
        "The real treasure \u2014 a repository of ancient scientific\n"
        "knowledge that could reshape the modern world \u2014\n"
        "is hidden in a chamber no one knows exists.\n"
        "\n"
        "She has twelve days to decide its fate."
    ),
    "TWO_CHAINS": (
        "Six months after the Padmanabhaswamy vault opening,\n"
        "FBI agent Meera Desai investigates the murder of a\n"
        "Harvard Sanskrit scholar and discovers six stolen\n"
        "Indian artifacts scattered across America.\n"
        "\n"
        "Each artifact is a piece of a puzzle pointing to a\n"
        "second ancient repository hidden beneath the\n"
        "Newport Tower in Rhode Island for 500 years."
    ),
    "THE_THIRD_CHAIN": (
        "Eighteen months after becoming the unified guardian,\n"
        "Meera Desai discovers that Ashoka's ancient knowledge\n"
        "has been scattering along the Silk Road for two\n"
        "thousand years.\n"
        "\n"
        "A rogue guardian from a forgotten lineage is assembling\n"
        "every fragment for simultaneous global release.\n"
        "The vault is open. The knowledge is loose."
    ),
}


def compose_back(art, cfg, w, h, book_id, margins_in=None):
    cover = smart_crop(art, w, h)
    if margins_in:
        mt, mb, ml, mr = (in2px(m) for m in margins_in)
    else:
        mt, mb, ml, mr = 0, 0, 0, 0
    cx = ml + (w - ml - mr) // 2
    sw = w - ml - mr
    st = mt
    sb = h - mb
    sh = sb - st
    accent = cfg["accent_rgb"]
    dim = (45, 35, 20)
    dark = (30, 25, 20)

    y = st + int(sh * 0.10)
    cover = overlay_text_pro(cover, cfg["author"], cx, y,
                             FONT_BOLD, max(16, int(sw * 0.035)), accent,
                             anchor="mt", shadow=False, glow=False, stroke=False,
                             letter_spacing=max(2, int(sw * 0.006)),
                             halo=True)
    y += int(sh * 0.04)
    accent_line(cover, cx, y, int(sw * 0.18), cfg["accent_bgr"], 1)

    desc = BACK_TEXT.get(book_id, BACK_TEXT["VAULT_B"])
    fs = max(12, int(sw * 0.024))
    y += int(sh * 0.03)
    lines = desc.split("\n")
    for i, line in enumerate(lines):
        if line.strip() == "":
            y += int(fs * 0.5)
            continue
        cover = overlay_text_pro(cover, line, cx, y, FONT_REG, fs, dim,
                                 anchor="mt", shadow=False, glow=False, stroke=False,
                                 halo=True)
        y += int(fs * 1.4)

    y += int(sh * 0.02)
    accent_line(cover, cx, y, int(sw * 0.12), cfg["accent_bgr"], 1)
    y += int(sh * 0.015)
    cover = overlay_text_pro(cover, cfg["sanskrit"], cx, y,
                             FONT_DEVANAGARI, max(10, int(sw * 0.018)),
                              (80, 65, 35), anchor="mt",
                             shadow=False, glow=False, stroke=False,
                             halo=True)
    y += int(sh * 0.025)
    cover = overlay_text_pro(cover, f'"{cfg["sanskrit_meaning"]}"', cx, y,
                             FONT_ITALIC, max(9, int(sw * 0.016)), dim,
                             anchor="mt", shadow=False, glow=False, stroke=False,
                             halo=True)

    bw, bh = int(sw * 0.32), int(sh * 0.10)
    bx = (w - mr) - bw - int(sw * 0.06)
    by = sb - bh - int(sh * 0.04)
    cv2.rectangle(cover, (bx, by), (bx + bw, by + bh), (235, 228, 218), -1)
    cv2.rectangle(cover, (bx, by), (bx + bw, by + bh), dim, 1, cv2.LINE_AA)
    cover = overlay_text_pro(cover, "BARCODE", bx + bw // 2, by + bh // 2,
                             FONT_REG, max(8, int(sw * 0.012)), (180, 170, 155),
                             anchor="mm", shadow=False, glow=False, stroke=False)

    return cover


def compose_spine(w, h, cfg, margin_px=0):
    cream = paper_bg(h, w)
    cx = w // 2
    dark = (30, 25, 20)
    accent = cfg["accent_rgb"]

    sfs = max(7, min(20, int(w * 0.30)))
    title = cfg["title"].replace("\n", " ")
    ch = max(7, int(sfs * 0.85))
    author_fs = max(5, int(sfs * 0.5))
    author_ls = max(1, int(sfs * 0.08))
    author_h = author_fs + 10
    gap = 40
    title_h = len(title) * ch
    total_h = title_h + gap + author_h

    safe_top = margin_px
    safe_bot = h - margin_px
    ys = safe_top + max(0, (safe_bot - safe_top - total_h) // 2)

    for i, c in enumerate(title):
        cream = overlay_text_pro(cream, c, cx, ys + i * ch, FONT_BOLD, sfs, dark,
                                 anchor="mt", shadow=False, glow=False, stroke=False)

    cream = overlay_text_pro(cream, cfg["author"], cx, ys + title_h + gap,
                             FONT_BOLD, author_fs, accent,
                             anchor="mt", shadow=False, glow=False, stroke=False,
                             letter_spacing=author_ls)
    return cream


def compose_paperback(art, cfg, specs, book_id):
    sp = specs["paperback"]
    tw, th = sp["w"], sp["h"]
    canvas = paper_bg(th, tw, CREAM_BGR)

    front = compose_front(art, cfg, sp["front_w"], th)
    back = compose_back(art, cfg, sp["back_w"], th, book_id)
    spine = compose_spine(sp["sp_w"], th, cfg)

    canvas[:, sp["front_x"]:sp["front_x"] + sp["front_w"]] = front
    canvas[:, sp["back_x"]:sp["back_x"] + sp["back_w"]] = back
    canvas[:, sp["sp_x"]:sp["sp_x"] + sp["sp_w"]] = spine

    cv2.line(canvas, (sp["sp_x"], 0), (sp["sp_x"], th), cfg["accent_bgr"], 1, cv2.LINE_AA)
    cv2.line(canvas, (sp["front_x"], 0), (sp["front_x"], th), cfg["accent_bgr"], 1, cv2.LINE_AA)
    return canvas


def compose_hardcover(art, cfg, specs, book_id):
    sp = specs["hardcover"]
    tw, th = sp["w"], sp["h"]
    canvas = paper_bg(th, tw, CREAM_BGR)

    hc_art = art.copy()
    overlay_alpha = cfg.get("overlay_alpha", 0)
    if overlay_alpha > 0:
        cream_flat = np.full_like(hc_art, CREAM_BGR, dtype=np.uint8)
        hc_art = cv2.addWeighted(hc_art, 1 - overlay_alpha, cream_flat, overlay_alpha, 0)

    front = compose_front(hc_art, cfg, sp["front_w"], th,
                          margins_in=(HC_SAFE_MARGIN_IN, HC_SAFE_MARGIN_IN,
                                      HC_SAFE_SPINE_IN, HC_SAFE_MARGIN_IN))
    back = compose_back(hc_art, cfg, sp["back_w"], th, book_id,
                        margins_in=(HC_SAFE_MARGIN_IN, HC_SAFE_MARGIN_IN,
                                    HC_SAFE_MARGIN_IN, HC_SAFE_SPINE_IN))
    spine = compose_spine(sp["sp_w"], th, cfg,
                          margin_px=in2px(HC_SAFE_MARGIN_IN))

    canvas[:, sp["front_x"]:sp["front_x"] + sp["front_w"]] = front
    canvas[:, sp["back_x"]:sp["back_x"] + sp["back_w"]] = back
    canvas[:, sp["sp_x"]:sp["sp_x"] + sp["sp_w"]] = spine

    cv2.line(canvas, (sp["sp_x"], 0), (sp["sp_x"], th), cfg["accent_bgr"], 1, cv2.LINE_AA)
    cv2.line(canvas, (sp["front_x"], 0), (sp["front_x"], th), cfg["accent_bgr"], 1, cv2.LINE_AA)
    return canvas


def generate_all():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for book_id, cfg in BOOKS.items():
        print(f"\n{'='*60}")
        print(f"  {book_id} | {cfg['pages']} pages | {TRIM_W}x{TRIM_H} trim")
        specs = calc_specs(cfg["pages"],
                           spine_pb_in=cfg.get("kdp_pb_spine"),
                           spine_hc_in=cfg.get("kdp_hc_spine"))
        sp = specs["paperback"]
        hc = specs["hardcover"]
        print(f"  PB spine: {specs['spine_pb_in']:.3f}\" ({sp['sp_w']}px) | cover: {sp['w']}x{sp['h']}")
        print(f"  HC spine: {specs['spine_hc_in']:.3f}\" ({hc['sp_w']}px) | cover: {hc['w']}x{hc['h']}")
        print(f"{'='*60}")

        art_dir = OUT_DIR / book_id / "artwork"
        art_dir.mkdir(parents=True, exist_ok=True)

        imgs = []
        for i, prompt in enumerate(cfg["prompts"]):
            path = art_dir / f"art_v3_{i}.png"
            if path.exists():
                print(f"  Cached: {path.name}")
                imgs.append(cv2.imread(str(path)))
            else:
                print(f"  Generating art {i+1}/{len(cfg['prompts'])}...")
                try:
                    seed = int(hashlib.md5(f"{book_id}_v3_{i}".encode()).hexdigest()[:8], 16) % 2147483647
                    img = gen_bonsai(prompt, seed=seed, size=1024)
                    cv2.imwrite(str(path), img)
                    imgs.append(img)
                    print(f"  Saved: {path.name}")
                except Exception as e:
                    print(f"  ERROR: {e}")
                    fb = art_dir / "art_v3_0.png"
                    if fb.exists():
                        print(f"  Fallback: {fb.name}")
                        imgs.append(cv2.imread(str(fb)))

        if not imgs:
            print(f"  SKIP {book_id} -- no art")
            continue

        print("  Processing artwork (light sepia warm)...")
        processed = process_art(imgs, 1600, 2560, cfg.get("brightness", 1.0))
        cv2.imwrite(str(art_dir / "processed_v3.png"), processed)

        print("  Kindle cover...")
        kindle = compose_front(processed, cfg, 1600, 2560)
        kp = OUT_DIR / book_id / f"{book_id}_Kindle.jpg"
        cv2.imwrite(str(kp), kindle, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(f"  -> {kp}")

        print("  Paperback cover...")
        pb = compose_paperback(processed, cfg, specs, book_id)
        pp_png = OUT_DIR / book_id / f"{book_id}_Paperback.png"
        cv2.imwrite(str(pp_png), pb)
        pp_pdf = OUT_DIR / book_id / f"{book_id}_Paperback.pdf"
        _save_pdf(pb, pp_pdf, page_size_in=specs["paperback"].get("size_in"))
        print(f"  -> {pp_pdf}")

        print("  Hardcover dust jacket...")
        hc_img = compose_hardcover(processed, cfg, specs, book_id)
        hp_png = OUT_DIR / book_id / f"{book_id}_Hardcover.png"
        cv2.imwrite(str(hp_png), hc_img)
        hp_pdf = OUT_DIR / book_id / f"{book_id}_Hardcover.pdf"
        _save_pdf(hc_img, hp_pdf)
        print(f"  -> {hp_pdf}")

        print(f"  DONE {book_id}")

    print(f"\n{'='*60}")
    print("  ALL COVERS COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    generate_all()
