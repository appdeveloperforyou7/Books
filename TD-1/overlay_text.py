import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

FONT_DIR = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Fonts")

FONT_ROUNDED = os.path.join(FONT_DIR, "ARLRDBD.TTF")
FONT_COMIC = os.path.join(FONT_DIR, "comic.ttf")
FONT_CALIBRI = os.path.join(FONT_DIR, "calibri.ttf")
FONT_GEORGIA = os.path.join(FONT_DIR, "georgia.ttf")


def _sample_region(img_bgr, cx, cy, radius=50):
    h, w = img_bgr.shape[:2]
    y1, y2 = max(0, cy - radius), min(h, cy + radius)
    x1, x2 = max(0, cx - radius), min(w, cx + radius)
    region = img_bgr[y1:y2, x1:x2]
    if region.size == 0:
        return 128, (128, 128, 128)
    avg = region.mean(axis=(0, 1))
    return float(avg.mean()), tuple(int(c) for c in avg)


def _auto_color(brightness):
    if brightness < 90:
        return (255, 255, 240)
    elif brightness > 170:
        return (45, 35, 25)
    else:
        return (255, 248, 230)


def _derive_glow(avg_bgr, brighten=50):
    r = min(255, int(avg_bgr[2]) + brighten)
    g = min(255, int(avg_bgr[1]) + brighten)
    b = min(255, int(avg_bgr[0]) + brighten)
    return (r, g, b)


def _make_blurred_shadow(w, h, text, font, anchor_x, anchor_y, blur_r=6, alpha=0.55):
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.text((anchor_x + blur_r, anchor_y + blur_r), text, font=font, fill=(0, 0, 0, int(255 * alpha)))
    if blur_r > 1:
        layer = layer.filter(ImageFilter.GaussianBlur(radius=blur_r))
    return layer


def _make_multilayer_glow(w, h, text, font, anchor_x, anchor_y, glow_color, base_alpha=0.25):
    layers = []
    configs = [
        (base_alpha * 0.3, 12),
        (base_alpha * 0.5, 6),
        (base_alpha * 0.8, 3),
    ]
    for alpha_frac, blur_r in configs:
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        draw.text(
            (anchor_x, anchor_y),
            text,
            font=font,
            fill=(*glow_color, int(255 * alpha_frac)),
        )
        if blur_r > 0:
            layer = layer.filter(ImageFilter.GaussianBlur(radius=blur_r))
        layers.append(layer)
    return layers


def _make_stroke(w, h, text, font, anchor_x, anchor_y, stroke_color, stroke_width=2):
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text(
                    (anchor_x + dx, anchor_y + dy),
                    text,
                    font=font,
                    fill=(*stroke_color, 200),
                )
    return layer


def overlay_text(
    img_bgr,
    text,
    x,
    y,
    font_size=32,
    color=None,
    font_path=None,
    anchor="lt",
    shadow=True,
    glow=True,
    stroke=True,
    glow_color=None,
    glow_alpha=0.25,
    shadow_blur=6,
    shadow_alpha=0.55,
    stroke_color=None,
    stroke_width=2,
    line_spacing=1.2,
):
    h, w = img_bgr.shape[:2]
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    base = Image.fromarray(img_rgb).convert("RGBA")

    if font_path is None:
        font_path = FONT_ROUNDED
    font = ImageFont.truetype(font_path, font_size)

    brightness, avg_color = _sample_region(img_bgr, x, y)
    if color is None:
        color = _auto_color(brightness)
    text_rgb = tuple(color[:3])

    if glow and glow_color is None:
        glow_color = _derive_glow(avg_color)
    if stroke and stroke_color is None:
        stroke_color = (0, 0, 0) if brightness > 120 else (30, 25, 15)

    anchor_x, anchor_y = x, y
    if anchor == "mm":
        tmp = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        td = ImageDraw.Draw(tmp)
        bbox = td.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        anchor_x = x - tw // 2
        anchor_y = y - th // 2
    elif anchor == "mt":
        tmp = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        td = ImageDraw.Draw(tmp)
        bbox = td.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        anchor_x = x - tw // 2

    composite = base

    if glow:
        glow_layers = _make_multilayer_glow(
            w, h, text, font, anchor_x, anchor_y, glow_color, glow_alpha
        )
        for gl in glow_layers:
            composite = Image.alpha_composite(composite, gl)

    if shadow:
        shadow_layer = _make_blurred_shadow(
            w, h, text, font, anchor_x, anchor_y, blur_r=shadow_blur, alpha=shadow_alpha
        )
        composite = Image.alpha_composite(composite, shadow_layer)

    if stroke:
        stroke_layer = _make_stroke(
            w, h, text, font, anchor_x, anchor_y, stroke_color, stroke_width
        )
        composite = Image.alpha_composite(composite, stroke_layer)

    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(text_layer).text(
        (anchor_x, anchor_y), text, font=font, fill=(*text_rgb, 255)
    )
    composite = Image.alpha_composite(composite, text_layer)

    result_rgb = composite.convert("RGB")
    return cv2.cvtColor(np.array(result_rgb), cv2.COLOR_RGB2BGR)


def overlay_text_centered(
    img_bgr,
    text,
    y=None,
    font_size=48,
    color=None,
    font_path=None,
    shadow=True,
    glow=True,
    stroke=True,
    glow_color=None,
    glow_alpha=0.25,
    shadow_blur=6,
    shadow_alpha=0.55,
    stroke_color=None,
    stroke_width=2,
):
    h, w = img_bgr.shape[:2]
    if y is None:
        y = h // 2
    return overlay_text(
        img_bgr, text, w // 2, y,
        font_size=font_size, color=color, font_path=font_path,
        anchor="mt", shadow=shadow, glow=glow, stroke=stroke,
        glow_color=glow_color, glow_alpha=glow_alpha,
        shadow_blur=shadow_blur, shadow_alpha=shadow_alpha,
        stroke_color=stroke_color, stroke_width=stroke_width,
    )


def overlay_multiline(
    img_bgr, lines, x, y,
    font_size=28, color=None, font_path=None,
    line_spacing=1.3, shadow=True, glow=True, stroke=True, anchor="lt",
):
    if font_path is None:
        font_path = FONT_ROUNDED
    font = ImageFont.truetype(font_path, font_size)
    current_y = y
    result = img_bgr.copy()
    for line in lines:
        result = overlay_text(
            result, line, x, current_y,
            font_size=font_size, color=color, font_path=font_path,
            anchor=anchor, shadow=shadow, glow=glow, stroke=stroke,
        )
        bbox = font.getbbox(line)
        current_y += int((bbox[3] - bbox[1]) * line_spacing)
    return result


def overlay_label(
    img_bgr, text, target_x, target_y,
    font_size=18, color=(60, 30, 10), font_path=None,
    leader=True, leader_offset=(15, -5),
):
    if font_path is None:
        font_path = FONT_ROUNDED
    font = ImageFont.truetype(font_path, font_size)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    label_x = target_x + leader_offset[0]
    label_y = target_y + leader_offset[1] - th

    result = img_bgr.copy()
    if leader:
        cv2.line(result, (target_x, target_y), (label_x, label_y + th), (80, 50, 20), 1, cv2.LINE_AA)
        cv2.line(result, (label_x, label_y + th), (label_x + tw, label_y + th), (80, 50, 20), 1, cv2.LINE_AA)

    result = overlay_text(
        result, text, label_x, label_y,
        font_size=font_size, color=color, font_path=font_path,
        shadow=True, glow=False, stroke=False,
    )
    return result


def test_overlay():
    test = np.zeros((300, 600, 3), dtype=np.uint8)
    grad = np.linspace(30, 220, 600, dtype=np.uint8)
    test[:, :, 0] = 80
    test[:, :, 1] = 50 + (grad // 3).astype(np.uint8)
    test[:, :, 2] = grad[np.newaxis, :]

    result = overlay_text_centered(
        test, "Hello World!", y=80, font_size=48,
        color=(255, 220, 50), shadow_blur=8, shadow_alpha=0.5,
        stroke_width=2, glow_alpha=0.3,
    )
    result = overlay_text(
        result, "Auto color text", 50, 170, font_size=30,
        shadow_blur=4, stroke_width=1,
    )
    result = overlay_text(
        result, "Glow + Stroke", 350, 170, font_size=30,
        color=(255, 255, 240), glow_alpha=0.35, shadow_blur=5,
        stroke_width=1,
    )
    result = overlay_text(
        result, "No glow", 50, 240, font_size=24,
        glow=False, shadow_blur=3, stroke_width=1, color=(200, 180, 50),
    )
    out_path = r"E:\Temp\kilo\overlay_test_v2.png"
    cv2.imwrite(out_path, result)
    print(f"Test v2 saved to {out_path}")


if __name__ == "__main__":
    test_overlay()
