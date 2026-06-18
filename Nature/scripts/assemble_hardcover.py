#!/usr/bin/env python3
"""Nature HARDCOVER edition — All images as spreads, no singles.
8.25 x 11 portrait, bleed, KDP hardcover compatible."""

import os, io, sys, warnings, math, json, random
from PIL import Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

warnings.filterwarnings("ignore")

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONT_DIR = os.path.join(BASE, "scripts", "fonts")
IMG_DIR_OUT = os.path.join(BASE, "output", "images")
IMG_DIR_SRC = os.path.join(BASE, "images")
OUT_PDF = os.path.join(BASE, "output", "Nature_Hardcover.pdf")

PAGE_W = 8.5 * inch
PAGE_H = 11.25 * inch
SPREAD_W = 17.0 * inch

CREAM = HexColor("#FAF8F5")
CHARCOAL = HexColor("#1A1A1A")
OFF_WHITE = HexColor("#F5F2ED")
TEXT_DARK = HexColor("#2C2C2C")
RULE_GRAY = HexColor("#999999")
RULE_LIGHT = HexColor("#CCCCCC")
PAGE_NUM_COLOR = HexColor("#666666")

pdfmetrics.registerFont(TTFont("GeorgiaReg", os.path.join(FONT_DIR, "Georgia-Regular.ttf")))
pdfmetrics.registerFont(TTFont("GeorgiaBold", os.path.join(FONT_DIR, "Georgia-Bold.ttf")))
pdfmetrics.registerFont(TTFont("GeorgiaIta", os.path.join(FONT_DIR, "Georgia-Italic.ttf")))
pdfmetrics.registerFont(TTFont("SegoeLight", os.path.join(FONT_DIR, "SegoeUI-Light.ttf")))
pdfmetrics.registerFont(TTFont("SegoeReg", os.path.join(FONT_DIR, "SegoeUI-Regular.ttf")))

SERIF = "GeorgiaReg"
SERIF_BOLD = "GeorgiaBold"
SERIF_ITA = "GeorgiaIta"
SANS_LIGHT = "SegoeLight"
SANS_REG = "SegoeReg"

page_count = 0
TOTAL_PAGES_TARGET = 112  # 6 front + 1 lead + 2*50 spreads + 4 back = 111, pad to 112

QUOTE_META = {}
_mp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_metadata.json")
if os.path.isfile(_mp):
    with open(_mp, encoding="utf-8") as _f:
        for _e in json.load(_f).get("images", []):
            QUOTE_META[_e["file"]] = _e


def resolve_raw(rel):
    p = os.path.join(IMG_DIR_SRC, rel)
    if os.path.isfile(p):
        return p
    for d in (IMG_DIR_OUT, IMG_DIR_SRC):
        p = os.path.join(d, rel)
        if os.path.isfile(p):
            return p
    return None


def center_crop(img, tw, th):
    sw, sh = img.size
    sr, tr = sw / sh, tw / th
    if sr > tr:
        nw, nh = int(sh * tr), sh
        left, top = (sw - nw) // 2, 0
    else:
        nw, nh = sw, int(sw / tr)
        left, top = 0, (sh - nh) // 2
    cr = img.crop((left, top, left + nw, top + nh))
    return cr.resize((int(tw), int(th)), Image.LANCZOS)


def embed(c, img, w, h):
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    buf.seek(0)
    c.drawImage(ImageReader(buf), 0, 0, width=w, height=h, preserveAspectRatio=False, mask="auto")


def next_page(c):
    global page_count
    c.showPage()
    page_count += 1


def tracked(c, text, font, size, x, y, tracking, color=None, anchor="left"):
    if color:
        c.setFillColor(color)
    c.setFont(font, size)
    if tracking == 0:
        if anchor == "center":
            tw = c.stringWidth(text, font, size)
            c.drawString(x - tw / 2, y, text)
        else:
            c.drawString(x, y, text)
        return
    tw = sum(c.stringWidth(ch, font, size) for ch in text) + tracking * (len(text) - 1)
    cx = x - tw / 2 if anchor == "center" else x
    for i, ch in enumerate(text):
        c.drawString(cx, y, ch)
        if i < len(text) - 1:
            cx += c.stringWidth(ch, font, size) + tracking


def page_num(c):
    pn = page_count + 1
    if 7 <= pn <= 108:
        c.setFillColor(PAGE_NUM_COLOR)
        c.setFont(SANS_LIGHT, 9)
        ns = str(pn)
        nw = c.stringWidth(ns, SANS_LIGHT, 9)
        c.drawString(PAGE_W - 0.5 * inch - nw, 0.5 * inch, ns)


def _render_quote(c, meta, side="full"):
    if meta is None:
        return
    pos = meta.get("position", "bottom-left")
    if side == "left" and "right" in pos:
        return
    if side == "right" and "left" in pos:
        return
    qt = meta["quote"]
    au = meta["author"]
    mq = 0.7 * inch
    sw = PAGE_W - 2 * mq
    c.setFont(SERIF_ITA, 16)
    words = qt.split()
    lines = []
    cur = ""
    for w in words:
        t = cur + (" " if cur else "") + w
        if c.stringWidth(t, SERIF_ITA, 16) <= sw - 0.5 * inch:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if not lines:
        return
    lh = 18
    gr = 10
    ga = 14
    ae = 12
    if "top" in pos:
        f_y = PAGE_H - mq - 0.15 * inch - 4
    else:
        ay = mq + 0.15 * inch + 4
        ry = ay + ga + ae
        ll_y = ry + gr
        f_y = ll_y + (len(lines) - 1) * lh
    c.setFillColor(Color(1, 1, 1, alpha=0.92))
    for i, line in enumerate(lines):
        c.drawString(mq + 22, f_y - i * lh, line)
    if "top" in pos:
        ry2 = f_y - (len(lines) - 1) * lh - gr
        ay2 = ry2 - ga - ae
    else:
        ay2 = mq + 0.15 * inch + 4
        ry2 = ay2 + ga + ae
    c.setStrokeColor(Color(1, 1, 1, alpha=0.40))
    c.setLineWidth(0.5)
    c.line(mq + 22, ry2, mq + 22 + 55, ry2)
    c.setFont(SERIF, 11)
    c.setFillColor(Color(1, 1, 1, alpha=0.60))
    c.drawString(mq + 22, ay2, f"\u2014 {au}")


def spread_page(c, rel, show_page_num=True):
    global page_count
    raw_path = resolve_raw(rel)
    if raw_path is None:
        print(f"           [WARN] Missing: {rel}")
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        if show_page_num:
            page_num(c)
        next_page(c)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        if show_page_num:
            page_num(c)
        next_page(c)
        return
    img = Image.open(raw_path).convert("RGB")
    full = center_crop(img, SPREAD_W, PAGE_H)
    mid = full.width // 2
    lh = full.crop((0, 0, mid, full.height))
    rh = full.crop((mid, 0, full.width, full.height))
    mkey = rel if rel.startswith("images/") else f"images/{rel}"
    meta = QUOTE_META.get(mkey)
    embed(c, lh.resize((int(PAGE_W), int(PAGE_H)), Image.LANCZOS), PAGE_W, PAGE_H)
    _render_quote(c, meta, side="left")
    if show_page_num:
        page_num(c)
    next_page(c)
    embed(c, rh.resize((int(PAGE_W), int(PAGE_H)), Image.LANCZOS), PAGE_W, PAGE_H)
    _render_quote(c, meta, side="right")
    if show_page_num:
        page_num(c)
    next_page(c)


def image_bg(c, rel):
    path = resolve_raw(rel)
    if path is None:
        c.setFillColor(CHARCOAL)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        return
    img = Image.open(path).convert("RGB")
    embed(c, center_crop(img, PAGE_W, PAGE_H), PAGE_W, PAGE_H)


def draw_half_title(c):
    global page_count
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    cy = PAGE_H * 0.55
    ry1 = cy + 2.0 * inch
    ry2 = cy - 2.0 * inch
    c.setStrokeColor(HexColor("#BBBBBB"))
    c.setLineWidth(0.5)
    c.line(PAGE_W * 0.15, ry1, PAGE_W * 0.85, ry1)
    c.line(PAGE_W * 0.15, ry2, PAGE_W * 0.85, ry2)
    tracked(c, "NATURE", SERIF_BOLD, 72, PAGE_W / 2, cy - 24, 6, CHARCOAL, "center")
    tracked(c, "A VISUAL JOURNEY", SERIF, 14, PAGE_W / 2, ry2 - 60, 3, RULE_GRAY, "center")
    next_page(c)


def draw_title_spread(c):
    global page_count
    path = resolve_raw("_cover_front_hero.jpg")
    if path:
        image_bg(c, "_cover_front_hero.jpg")
    else:
        c.setFillColor(CHARCOAL)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    ty = PAGE_H * 0.55
    so = 1.2
    band_y = ty - 0.75 * inch
    band_h = 2.2 * inch
    steps = 40
    for i in range(steps):
        alpha = 0.35 * (1.0 - abs(i - steps/2) / (steps/2))
        c.setFillColor(Color(0, 0, 0, alpha=alpha))
        h_slice = band_h / steps
        c.rect(0, band_y + i * h_slice, PAGE_W, h_slice, fill=1, stroke=0)
    tracked(c, "NATURE", SANS_LIGHT, 72, PAGE_W / 2 + so, ty - so + 22, 8, Color(0, 0, 0, alpha=0.2), "center")
    tracked(c, "NATURE", SANS_LIGHT, 72, PAGE_W / 2, ty + 22, 8, Color(1, 1, 1, alpha=1.0), "center")
    sy = ty - 0.5 * inch
    tracked(c, "A Visual Journey Through", SANS_REG, 13, PAGE_W / 2, sy, 2, Color(1, 1, 1, alpha=0.85), "center")
    tracked(c, "Earth's Most Stunning Landscapes", SANS_REG, 13, PAGE_W / 2, sy - 18, 2, Color(1, 1, 1, alpha=0.85), "center")
    next_page(c)


def draw_copyright(c):
    global page_count
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    ml = 1.2 * inch
    mt = 8.0 * inch
    ld = 15
    c.setFillColor(CHARCOAL)
    tracked(c, "NATURE", SERIF_BOLD, 15, ml, mt, 3, CHARCOAL)
    tw = sum(c.stringWidth(ch, SERIF_BOLD, 15) for ch in "NATURE") + 3 * len("NATURE") - 3
    c.setStrokeColor(RULE_LIGHT)
    c.setLineWidth(0.5)
    c.line(ml, mt - 7, ml + tw, mt - 7)
    lines = [
        "", "A Visual Journey Through Earth's Most Stunning Landscapes", "",
        "Published by Nature Publications",
        "\u00a9 2025 Nature Publications. All rights reserved.", "",
        "First Edition, 2025", "",
        "Printed and bound in Italy", "",
        "All photographs in this volume have been curated from",
        "professional nature photographers and are reproduced under",
        "commercial license. Every image has been selected for its",
        "capacity to transport the viewer to wild places.",
    ]
    y = mt - 26
    for line in lines:
        if line == "":
            y -= ld
            continue
        c.setFont(SERIF, 9.5)
        c.setFillColor(TEXT_DARK)
        words = line.split()
        cur = ""
        mx = PAGE_W - ml - 0.75 * inch
        for w in words:
            t = cur + (" " if cur else "") + w
            if c.stringWidth(t, SERIF, 9.5) < mx:
                cur = t
            else:
                c.drawString(ml, y, cur)
                y -= ld
                cur = w
        if cur:
            c.drawString(ml, y, cur)
            y -= ld
    next_page(c)


def draw_toc(c):
    global page_count
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    m = 1.2 * inch
    ty = PAGE_H - 2.0 * inch
    tracked(c, "THE JOURNEY", SERIF_BOLD, 22, PAGE_W / 2, ty, 5, CHARCOAL, "center")
    rw = PAGE_W * 0.7
    c.setStrokeColor(RULE_GRAY)
    c.setLineWidth(0.5)
    c.line(PAGE_W / 2 - rw / 2, ty - 12, PAGE_W / 2 + rw / 2, ty - 12)
    toc_text = (
        "This book is not a catalog. It is a wandering — a visual\n"
        "journey through Earth's most stunning landscapes, arranged\n"
        "to surprise and delight with every turn of the page.\n\n"
        "Mountains give way to oceans. Deserts yield to forests.\n"
        "Ice becomes fire. Water finds stone.\n\n"
        "There is no map here. Only wonder."
    )
    y = ty - 50
    c.setFont(SERIF, 11)
    c.setFillColor(TEXT_DARK)
    for para in toc_text.split("\n"):
        if para.strip() == "":
            y -= 14
            continue
        c.drawString(m, y, para)
        y -= 17
    next_page(c)


def draw_colophon(c):
    global page_count
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    m = 1.0 * inch
    ct = PAGE_H - m
    c.setFillColor(CHARCOAL)
    tracked(c, "ABOUT THIS BOOK", SERIF_BOLD, 14, m, ct, 2, CHARCOAL)
    c.setStrokeColor(RULE_LIGHT)
    c.setLineWidth(0.4)
    c.line(m, ct - 8, m + 200, ct - 8)
    paras = [
        "This volume presents over fifty meticulously curated photographs of Earth's most pristine wilderness — from snow-capped summits to emerald depths.",
        "The landscapes within these pages span every continent: alpine peaks older than civilization, rainforests breathing life into the atmosphere.",
        "Each photograph has been selected for its capacity to transport the viewer — not merely to a place, but to a state of wonder.",
    ]
    y = ct - 28
    lw = PAGE_W * 0.7
    ld = 15
    for para in paras:
        c.setFont(SERIF, 10)
        c.setFillColor(TEXT_DARK)
        words = para.split()
        cur = ""
        for w in words:
            t = cur + (" " if cur else "") + w
            if c.stringWidth(t, SERIF, 10) < lw:
                cur = t
            else:
                c.drawString(m, y, cur)
                y -= ld
                cur = w
        if cur:
            c.drawString(m, y, cur)
            y -= ld
        y -= 6
    cy = ct - 20
    items = [
        ("Title", "Nature"), ("Publisher", "Nature Publications"),
        ("Edition", "First, 2025"), ("Format", "Portrait, 8.25 x 11 inches"),
        ("Pages", f"{page_count + 1}"), ("Paper", "Premium Color, White Stock"),
        ("Binding", "Hardcover Case Laminate"), ("Color", "sRGB"),
    ]
    c.setFont(SERIF, 9)
    for lbl, val in items:
        c.setFillColor(CHARCOAL)
        c.drawString(PAGE_W * 0.55, cy, lbl)
        c.setFillColor(TEXT_DARK)
        c.drawString(PAGE_W * 0.55, cy - 11, val)
        cy -= 26
    c.setStrokeColor(RULE_LIGHT)
    c.setLineWidth(0.25)
    c.line(m, 0.25 * inch, PAGE_W - m, 0.25 * inch)
    page_num(c)
    next_page(c)


# ===================================================================
# ALL-SPREAD SEQUENCE — Every image is a full two-page spread
# ===================================================================
SEQUENCE = [
    "mountains/01_alpine_peak_dawn.jpg",
    "rivers/03_river_through_forest.jpg",
    "glaciers/01_glacier_ice_cave.jpg",
    "deserts/01_sahara_sand_dunes.jpg",
    "forests/02_autumn_forest_stream.jpg",
    "oceans/05_bioluminescent_ocean.jpg",
    "lakes/02_mountain_lake_panorama.jpg",
    "jungles/02_jungle_river_mist.jpg",
    "glaciers/04_glacier_lagoon_icebergs.jpg",
    "canyons/02_grand_canyon_overlook.jpg",
    "deserts/04_desert_flowers_bloom.jpg",
    "mountains/06_norwegian_fjord.jpg",
    "lakes/04_emerald_alpine_lake.jpg",
    "jungles/03_jungle_waterfall_vegetation.jpg",
    "volcanic/02_lava_field_black_sand.jpg",
    "oceans/01_dramatic_cliff_coastline.jpg",
    "forests/03_mystic_foggy_forest.jpg",
    "waterfalls/01_massive_waterfall.jpg",
    "deserts/02_desert_rock_formations.jpg",
    "mountains/02_mountain_range_sunset.jpg",
    "jungles/01_dense_rainforest_canopy.jpg",
    "oceans/02_tropical_beach_paradise.jpg",
    "forests/01_ancient_redwood_forest.jpg",
    "volcanic/01_volcanic_crater_lake.jpg",
    "rivers/01_canyon_river.jpg",
    "lakes/01_crater_lake.jpg",
    "oceans/03_stormy_ocean_waves.jpg",
    "forests/04_cherry_blossom_forest.jpg",
    "mountains/03_misty_mountain_valley.jpg",
    "rivers/02_swamp_river_cypress.jpg",
    "glaciers/03_glacier_blue_ice.jpg",
    "waterfalls/02_multi_tier_waterfall.jpg",
    "oceans/06_turquoise_cove.jpg",
    "canyons/01_antelope_slot_canyon.jpg",
    "forests/05_wildflower_meadow.jpg",
    "mountains/04_rocky_summit.jpg",
    "deserts/03_desert_stars_night.jpg",
    "oceans/07_rocky_shoreline_waves.jpg",
    "jungles/04_jungle_canopy_aerial.jpg",
    "canyons/03_canyon_riverbend.jpg",
    "waterfalls/03_hidden_waterfall_canyon.jpg",
    "oceans/04_aurora_ocean_arctic.jpg",
    "forests/06_bamboo_forest.jpg",
    "canyons/05_zion_valley.jpg",
    "mountains/07_dolomites_peaks.jpg",
    "volcanic/03_volcanic_ash_sunset.jpg",
    "volcanic/04_geothermal_hot_springs.jpg",
    "canyons/04_northern_lights_sky.jpg",
    "waterfalls/04_waterfall_forest_pool.jpg",
    "lakes/03_lotus_lily_pad_lake.jpg",
    "mountains/08_snowy_mountain_spring.jpg",
    "mountains/05_snow_mountains_lake_reflection.jpg",
]

ENDPAPER_IMG = "volcanic/04_geothermal_hot_springs.jpg"
CLOSE_IMG_1 = "forests/06_bamboo_forest.jpg"
CLOSE_IMG_2 = "oceans/07_rocky_shoreline_waves.jpg"
CLOSE_IMG_3 = "mountains/05_snow_mountains_lake_reflection.jpg"


def build():
    global page_count, QUOTE_META
    c = canvas.Canvas(OUT_PDF, pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Nature - Hardcover Edition")
    c.setAuthor("Nature Publications")
    print("=" * 64)
    print("Nature HARDCOVER Edition - All-Spread Format")
    print(f"Canvas: {PAGE_W/inch:.2f}\" x {PAGE_H/inch:.2f}\" (8.25x11 + bleed)")
    print("=" * 64)
    print("\n--- FRONT MATTER ---")
    draw_half_title(c)
    draw_title_spread(c)
    draw_copyright(c)
    image_bg(c, ENDPAPER_IMG)
    next_page(c)
    draw_toc(c)
    # Blank page (verso) for even parity
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    next_page(c)
    # Dedication page
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    cy = PAGE_H * 0.58
    tracked(c, "For those who wander", SERIF_ITA, 22, PAGE_W / 2, cy, 3, CHARCOAL, "center")
    tracked(c, "and those who wonder", SERIF_ITA, 22, PAGE_W / 2, cy - 32, 3, CHARCOAL, "center")
    c.setStrokeColor(HexColor("#CCCCCC"))
    c.setLineWidth(0.5)
    c.line(PAGE_W * 0.3, cy - 60, PAGE_W * 0.7, cy - 60)
    next_page(c)

    print(f"\n--- ALL-SPREAD SEQUENCE ({len(SEQUENCE)} spreads) ---")
    for rel in SEQUENCE:
        pp = page_count + 1
        print(f"  Pages {pp:3d}-{pp+1}: SPREAD {rel}")
        spread_page(c, rel)

    print(f"\n--- BACK MATTER (starting page {page_count+1}) ---")
    draw_colophon(c)
    image_bg(c, CLOSE_IMG_1)
    next_page(c)
    image_bg(c, CLOSE_IMG_2)
    next_page(c)
    image_bg(c, CLOSE_IMG_3)
    next_page(c)
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    next_page(c)

    c.save()
    fsz = os.path.getsize(OUT_PDF)
    ok = page_count % 2 == 0
    print("\n" + "=" * 64)
    print(f"PAGES: {page_count} | {'EVEN OK' if ok else 'ODD FAIL'}")
    print(f"Size: {fsz / (1024*1024):.1f} MB | Output: {OUT_PDF}")
    print("=" * 64)
    return ok


if __name__ == "__main__":
    sys.exit(0 if build() else 1)
