#!/usr/bin/env python3
"""Premium quote overlay for the Nature coffee table book.

Design: Large elegant serif-italic quote text, thin em-dash rule,
smaller roman attribution. Adaptive contrast to image brightness.
No background box — text floats directly on the image with a
subtle shadow for legibility. Inspired by Taschen / Phaidon.
"""

import argparse
import os
import sys
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


def _load(name, size):
    path = os.path.join(FONT_DIR, name)
    if os.path.isfile(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def quote_font(size):
    return _load("Georgia-Italic.ttf", size)


def author_font(size):
    return _load("Georgia-Regular.ttf", size)


def opening_mark_font(size):
    return _load("Georgia-Regular.ttf", size)


def _line_height(font):
    a, d = font.getmetrics()
    return a + d


def _text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def get_corner_brightness(img, position, sample_pct=0.20):
    w, h = img.size
    sw, sh = int(w * sample_pct), int(h * sample_pct)
    margin = int(min(w, h) * 0.02)
    coords = {
        "top-left": (margin, margin),
        "top-right": (w - sw - margin, margin),
        "bottom-left": (margin, h - sh - margin),
        "bottom-right": (w - sw - margin, h - sh - margin),
    }
    x, y = coords[position]
    corner = img.crop((x, y, x + sw, y + sh)).convert("L")
    hist = corner.histogram()
    total = sum(hist)
    if total == 0:
        return 128
    return sum(i * count for i, count in enumerate(hist)) // total


def _wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = current + (" " if current else "") + word
        dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        if _text_width(dummy, test, font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_quote(img, position, quote_text, author_text, y_offset=0):
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size

    scale = h / 1080.0

    sz_mark = max(int(72 * scale), 36)
    sz_quote = max(int(28 * scale), 14)
    sz_author = max(int(16 * scale), 9)
    line_spacing = max(int(10 * scale), 4)

    f_mark = opening_mark_font(sz_mark)
    f_quote = quote_font(sz_quote)
    f_author = author_font(sz_author)

    lh_quote = _line_height(f_quote)
    lh_author = _line_height(f_author)

    margin_x = int(60 * scale)
    margin_y = int(50 * scale)

    max_text_w = int(min(w * 0.42, 550 * scale))

    quote_lines = _wrap_text(quote_text, f_quote, max_text_w)

    brightness = get_corner_brightness(img, position)

    if brightness < 128:
        shadow_color = (0, 0, 0, int(0.55 * 255))
        text_color = (255, 255, 255, int(0.95 * 255))
        mark_color = (255, 255, 255, int(0.25 * 255))
        rule_color = (255, 255, 255, int(0.20 * 255))
        author_color = (255, 255, 255, int(0.65 * 255))
        shadow_offset = max(int(2 * scale), 1)
    else:
        shadow_color = (0, 0, 0, int(0.25 * 255))
        text_color = (20, 20, 20, int(0.92 * 255))
        mark_color = (20, 20, 20, int(0.18 * 255))
        rule_color = (20, 20, 20, int(0.18 * 255))
        author_color = (40, 40, 40, int(0.60 * 255))
        shadow_offset = max(int(1.5 * scale), 1)

    block_h = (
        _line_height(f_mark) * 0.55
        + line_spacing
        + len(quote_lines) * (lh_quote + line_spacing)
        + int(18 * scale)
        + int(1 * scale)
        + int(10 * scale)
        + lh_author
    )
    block_w = max_text_w + int(20 * scale)

    if position == "bottom-left":
        bx = margin_x
        by = h - margin_y - block_h + y_offset
    elif position == "bottom-right":
        bx = w - margin_x - block_w
        by = h - margin_y - block_h + y_offset
    elif position == "top-left":
        bx = margin_x
        by = margin_y + y_offset
    else:
        bx = w - margin_x - block_w
        by = margin_y + y_offset

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    def _shadow_text_line(target_draw, x, y, text, font, color, shadow_col, so):
        target_draw.text((x + so, y + so), text, font=font, fill=shadow_col)
        target_draw.text((x, y), text, font=font, fill=color)

    cx = bx
    cy = by

    mark_str = "\u201C"
    od.text((cx, cy - int(sz_mark * 0.35)), mark_str, font=f_mark, fill=mark_color)

    cy += int(_line_height(f_mark) * 0.55) + line_spacing

    for line in quote_lines:
        _shadow_text_line(od, cx, cy, line, f_quote, text_color, shadow_color, shadow_offset)
        cy += lh_quote + line_spacing

    cy += int(6 * scale)

    rule_w = min(int(60 * scale), _text_width(od, quote_lines[0] if quote_lines else "", f_quote) * 0.4)
    od.line([(cx, cy), (cx + rule_w, cy)], fill=rule_color, width=max(int(1 * scale), 1))
    cy += int(14 * scale)

    author_line = f"\u2014 {author_text}"
    _shadow_text_line(od, cx, cy, author_line, f_author, author_color, shadow_color, shadow_offset)

    result = Image.alpha_composite(img.convert("RGBA"), overlay)
    return result


def main():
    p = argparse.ArgumentParser(description="Draw premium quote overlay on an image")
    p.add_argument("--image", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--position", required=True,
                   choices=["bottom-left", "bottom-right", "top-left", "top-right"])
    p.add_argument("--quote", required=True, help="Quote text")
    p.add_argument("--author", required=True, help="Attribution")
    p.add_argument("--y-offset", type=int, default=0, help="Vertical shift in pixels (negative=up, positive=down)")
    args = p.parse_args()

    if not os.path.isfile(args.image):
        print(f"Error: image not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    img = Image.open(args.image).convert("RGBA")
    result = draw_quote(img, args.position, args.quote, args.author, y_offset=args.y_offset)
    rgb = Image.new("RGB", result.size, (255, 255, 255))
    rgb.paste(result, mask=result.split()[-1])

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    rgb.save(args.output, quality=95)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
