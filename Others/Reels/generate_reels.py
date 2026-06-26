"""ReelGen — generate vertical book marketing reels & shorts from ReelGen.md.

Pipeline:
  ReelGen.md  ->  parse config  ->  extract brand palette from reference image
              ->  compose 9:16 frames with PIL  ->  image shorts (PNG)
              ->  optional video reels (MP4, Ken Burns + fade) via moviepy 2.x
              ->  copy outputs into each target_projects/reels/ folder

Designed to be project-agnostic: edit ReelGen.md, run the script, ship.
"""

import argparse
import json
import math
import os
import random
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

try:
    from moviepy import ImageClip, vfx
    HAS_MOVIEPY = True
except Exception:
    HAS_MOVIEPY = False


# --------------------------------------------------------------------------- #
# Config parsing
# --------------------------------------------------------------------------- #

DEFAULTS: Dict[str, Any] = {
    "reel_settings": {
        "count": "1",
        "formats": "image",
        "duration_seconds": "15",
        "aspect_ratio": "9:16",
        "resolution": "1080p",
        "style": "cinematic",
        "call_to_action": "Link in bio",
        "ken_burns": "true",
        "cinematic": "false",
        "intro_seconds": "1",
        "outro_seconds": "2",
        "audio": "none",
        "brightness": "1.0",
        "reel_type": "teaser",
    },
    "branding": {"mode": "auto", "font_family": "arial"},
    "video_generation": {
        "provider": "moviepy",
        "preset": "medium",
        "fade_seconds": "0.4",
        "zoom": "0.07",
    },
}

ASPECTS = {
    "9:16": (9, 16),
    "1:1": (1, 1),
    "16:9": (16, 9),
    "4:5": (4, 5),
}

SHORT_EDGE = {"480p": 480, "720p": 720, "1080p": 1080}


def parse_reelgen(md_path: Path) -> Dict[str, Any]:
    """Parse a ReelGen.md into a nested dict.

    Sections are `## name`. A section of only `- item` lines becomes a list;
    otherwise it becomes a dict of `key: value` pairs.
    """
    sections: Dict[str, List[str]] = {}
    current: Optional[str] = None
    for raw in md_path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("## "):
            current = stripped[3:].strip().lower()
            sections[current] = []
            continue
        if stripped.startswith("#"):
            continue
        if current is None:
            continue
        sections[current].append(stripped)

    config: Dict[str, Any] = {}
    for name, lines in sections.items():
        if lines and all(ln.startswith("- ") for ln in lines):
            config[name] = [ln[2:].strip() for ln in lines]
        else:
            section: Dict[str, str] = {}
            for ln in lines:
                if ln.startswith("- "):
                    ln = ln[2:].strip()
                if ":" in ln:
                    key, value = ln.split(":", 1)
                    section[key.strip()] = value.strip()
            config[name] = section
    return config


def _as_int(value: str, fallback: int) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return fallback


def _as_float(value: str, fallback: float) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return fallback


def _as_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def compute_size(resolution: str, aspect: str) -> Tuple[int, int]:
    short = SHORT_EDGE.get(resolution, 1080)
    aw, ah = ASPECTS.get(aspect, (9, 16))
    if aw <= ah:
        w = short
        h = round(short * ah / aw)
    else:
        h = short
        w = round(short * aw / ah)
    return w, h


def normalize_config(raw: Dict[str, Any], root: Path) -> Dict[str, Any]:
    settings = {**DEFAULTS["reel_settings"], **(raw.get("reel_settings") or {})}
    branding = {**DEFAULTS["branding"], **(raw.get("branding") or {})}
    video = {**DEFAULTS["video_generation"], **(raw.get("video_generation") or {})}
    book = raw.get("book") or {}

    for key in ("title", "author"):
        if not book.get(key):
            raise ValueError(f"book.{key} is required in ReelGen.md")

    resolution = settings.get("resolution", "1080p").strip()
    aspect = settings.get("aspect_ratio", "9:16").strip()
    if resolution not in SHORT_EDGE:
        raise ValueError(f"resolution '{resolution}' not in {sorted(SHORT_EDGE)}")
    if aspect not in ASPECTS:
        raise ValueError(f"aspect_ratio '{aspect}' not in {sorted(ASPECTS)}")

    cover = _resolve(book.get("cover_image"), root)
    reference = _resolve(book.get("reference_image"), root) or cover
    if not cover:
        raise ValueError(
            "book.cover_image is required (drop the Kindle cover image in this folder)"
        )
    if not Path(cover).exists():
        raise FileNotFoundError(f"cover_image not found: {cover}")
    if reference and not Path(reference).exists():
        print(f"[warn] reference_image not found, using cover: {reference}")
        reference = cover

    formats = {f.strip().lower() for f in (settings.get("formats") or "image").split(",") if f.strip()}
    if not formats:
        formats = {"image"}

    hooks = raw.get("hooks") if isinstance(raw.get("hooks"), list) else []
    if not hooks:
        hooks = [book.get("tagline") or book["title"]]

    targets_raw = raw.get("target_projects") or []
    targets: List[Path] = []
    for t in targets_raw:
        p = Path(os.path.expandvars(os.path.expanduser(str(t)))).expanduser()
        if not p.is_absolute():
            p = (root / p).resolve()
        targets.append(p)

    return {
        "root": root,
        "book": {
            "title": book.get("title", "").strip(),
            "author": book.get("author", "").strip(),
            "tagline": (book.get("tagline") or "").strip(),
            "kdp_link": (book.get("kdp_link") or "").strip(),
            "cover_image": cover,
            "reference_image": reference,
        },
        "settings": {
            "count": max(1, _as_int(settings.get("count", "1"), 1)),
            "formats": formats,
            "duration_seconds": max(3, _as_int(settings.get("duration_seconds", "15"), 15)),
            "aspect_ratio": aspect,
            "resolution": resolution,
            "style": (settings.get("style") or "cinematic").strip(),
            "call_to_action": (settings.get("call_to_action") or "Link in bio").strip(),
            "ken_burns": _as_bool(settings.get("ken_burns", "true")),
            "cinematic": _as_bool(settings.get("cinematic", "false")),
            "intro_seconds": max(0.0, _as_float(settings.get("intro_seconds", "1"), 1.0)),
            "outro_seconds": max(0.0, _as_float(settings.get("outro_seconds", "2"), 2.0)),
            "audio": (settings.get("audio", "none")).strip().lower(),
            "brightness": _as_float(settings.get("brightness", "1.0"), 1.0),
            "reel_type": (settings.get("reel_type", "teaser")).strip().lower(),
        },
        "branding": {"mode": (branding.get("mode") or "auto").strip().lower(),
                     "font_family": (branding.get("font_family") or "arial").strip().lower()},
        "video": {
            "provider": (video.get("provider") or "moviepy").strip().lower(),
            "preset": (video.get("preset") or "medium").strip(),
            "fade_seconds": _as_float(video.get("fade_seconds", "0.4"), 0.4),
            "zoom": _as_float(video.get("zoom", "0.07"), 0.07),
        },
        "size": compute_size(resolution, aspect),
        "hooks": [h.strip() for h in hooks if h and h.strip()],
        "scenes": [s.strip() for s in (raw["scenes"] if isinstance(raw.get("scenes"), list) else []) if s and s.strip()],
        "slug": re.sub(r"[^a-z0-9]+", "_", str(book.get("title", "reel")).lower()).strip("_") or "reel",
        "target_projects": targets,
    }


def _resolve(value: Any, root: Path) -> Optional[str]:
    if not value:
        return None
    p = Path(os.path.expandvars(os.path.expanduser(str(value)))).expanduser()
    if not p.is_absolute():
        p = (root / p).resolve()
    return str(p)


def format_hook(hook: str, book: Dict[str, str], index: int) -> str:
    return hook.format(
        title=book.get("title", ""),
        author=book.get("author", ""),
        tagline=book.get("tagline", ""),
        kdp_link=book.get("kdp_link", ""),
        index=index + 1,
    )


# --------------------------------------------------------------------------- #
# Brand palette
# --------------------------------------------------------------------------- #

def extract_palette(image_path: str, n: int = 6) -> List[Tuple[int, int, int]]:
    im = Image.open(image_path).convert("RGB").resize((160, 160))
    quantized = im.quantize(colors=n, method=Image.MEDIANCUT).convert("RGB")
    counts = quantized.getcolors(160 * 160) or []
    counts.sort(key=lambda c: -c[0])
    return [tuple(c[1]) for c in counts]


def choose_brand(palette: List[Tuple[int, int, int]]) -> Dict[str, Tuple[int, int, int]]:
    def brightness(c):
        return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

    def saturation(c):
        mx, mn = max(c), min(c)
        return 0 if mx == 0 else (mx - mn) / mx

    bg = min(palette, key=brightness) if palette else (12, 12, 28)
    candidates = [c for c in palette if brightness(c) > 60 and brightness(c) < 210]
    accent = max(candidates, key=saturation) if candidates else (
        max(palette, key=saturation) if palette else (220, 170, 60)
    )
    accent_light = lighten(accent, 0.35)
    return {"bg": bg, "accent": accent, "accent_light": accent_light}


def lighten(color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
    return tuple(min(255, int(c + (255 - c) * factor)) for c in color)


# --------------------------------------------------------------------------- #
# Typography helpers
# --------------------------------------------------------------------------- #

def load_font(size: int, font_family: str = "arial", bold: bool = False,
              italic: bool = False) -> ImageFont.FreeTypeFont:
    family = (font_family or "arial").lower()
    candidates: List[str] = []
    if family == "arial":
        if bold and italic:
            candidates += ["arialbi.ttf", "ariblk.ttf"]
        if bold:
            candidates += ["arialbd.ttf", "ariblk.ttf"]
        if italic:
            candidates += ["ariali.ttf"]
        candidates += ["arial.ttf"]
    elif family == "segoe":
        candidates += ["segoeuib.ttf", "seguisb.ttf", "seguib.ttf", "segoeuil.ttf",
                       "segoeui.ttf"]
    else:
        candidates += [f"{family}bd.ttf", f"{family}.ttf"]
    candidates += ["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"]

    fonts_dir = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    for name in candidates:
        for base in (fonts_dir, fonts_dir / Path(name).name):
            if base.exists():
                try:
                    return ImageFont.truetype(str(base), size)
                except Exception:
                    continue
    return ImageFont.load_default()


def line_height(font: ImageFont.FreeTypeFont) -> int:
    return font.getbbox("Ag")[3]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
              max_width: int) -> List[str]:
    if not text:
        return []
    words = re.split(r"\s+", text.strip())
    lines: List[str] = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if draw.textlength(test, font=font) <= max_width or not current:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [text]


def draw_centered(draw: ImageDraw.ImageDraw, lines: List[str],
                  font: ImageFont.FreeTypeFont, center_x: int, top: int,
                  fill, leading: float = 1.15, shadow: bool = False) -> int:
    lh = int(line_height(font) * leading)
    y = top
    for ln in lines:
        w = draw.textlength(ln, font=font)
        x = int(center_x - w / 2)
        if shadow:
            draw.text((x + max(2, lh // 16), y + max(2, lh // 16)), ln,
                      font=font, fill=(0, 0, 0, 200))
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def short_link(url: str) -> str:
    if not url:
        return "amazon.com"
    m = re.search(r"/dp/([A-Z0-9]{10})", url)
    if m:
        return "amazon.com/dp/" + m.group(1)
    return url.replace("https://", "").replace("http://", "").rstrip("/")


def draw_persistent_link_bar(canvas: Image.Image, cfg: Dict[str, Any],
                             brand: Dict[str, Any]) -> None:
    """Prominent CTA bar pinned to the bottom; always visible on every frame."""
    w, h = canvas.size
    settings = cfg["settings"]
    family = cfg["branding"]["font_family"]
    bar_h = int(h * 0.085)
    by = h - bar_h
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rectangle([0, by, w, h], fill=brand["accent"] + (255,))
    d.rectangle([0, by, w, by + max(3, int(h * 0.004))], fill=brand["accent_light"] + (255,))

    text = settings.get("call_to_action") or "Get the book"
    size = int(w * 0.052)
    f = load_font(size, family, bold=True)
    while d.textlength(text, font=f) > w * 0.92 and size > 16:
        size -= 2
        f = load_font(size, family, bold=True)
    tw = d.textlength(text, font=f)
    th = line_height(f)
    d.text((w / 2 - tw / 2, by + (bar_h - th) / 2), text, font=f, fill=(255, 255, 255, 255))


# --------------------------------------------------------------------------- #
# Frame composition
# --------------------------------------------------------------------------- #

def compose_frame(cfg: Dict[str, Any], cover_path: str, brand: Dict[str, Any],
                  hook_text: str) -> Image.Image:
    w, h = cfg["size"]
    book = cfg["book"]
    settings = cfg["settings"]
    side = int(w * 0.08)
    inner_w = w - 2 * side

    canvas = _build_background(cover_path, w, h, brand["bg"])
    canvas = canvas.convert("RGBA")
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw.rectangle([0, 0, w, int(h * 0.012)], fill=brand["accent"])

    family = cfg["branding"]["font_family"]
    f_title = load_font(int(w * 0.085), family, bold=True)
    f_hook = load_font(int(w * 0.052), family, bold=True)
    f_author = load_font(int(w * 0.045), family, italic=True)
    f_cta = load_font(int(w * 0.05), family, bold=True)

    title_lines = wrap_text(draw, book["title"], f_title, inner_w)
    hook_lines = wrap_text(draw, hook_text, f_hook, inner_w)
    author_line = f"by {book['author']}".strip()

    bar_h = int(h * 0.09)
    gap = int(h * 0.022)
    title_h = int(line_height(f_title) * 1.15) * len(title_lines)
    hook_h = int(line_height(f_hook) * 1.15) * len(hook_lines)
    author_h = int(line_height(f_author) * 1.2)
    top = int(h * 0.05)
    used = top + title_h + gap + hook_h + gap + author_h + gap + bar_h
    cover_h = max(int(h * 0.16), min(int(h * 0.42), h - used))

    y = top
    y = draw_centered(draw, title_lines, f_title, w // 2, y, "white", shadow=True)
    y += gap

    cover_top = y
    try:
        cover_img = Image.open(cover_path).convert("RGBA")
    except Exception:
        cover_img = Image.new("RGBA", (int(cover_h * 0.66), cover_h), brand["accent"])
    cw, ch = cover_img.size
    scale = cover_h / ch
    disp_w = int(cw * scale)
    disp_h = cover_h
    if disp_w > inner_w:
        s2 = inner_w / disp_w
        disp_w = int(disp_w * s2)
        disp_h = int(disp_h * s2)
    disp = cover_img.resize((disp_w, disp_h), Image.LANCZOS)
    cx = (w - disp_w) // 2

    pad = max(6, int(w * 0.012))
    shadow_layer = Image.new("RGBA", (disp_w + 2 * pad, disp_h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(shadow_layer).rounded_rectangle(
        [0, 0, disp_w + 2 * pad - 1, disp_h + 2 * pad - 1],
        radius=int(pad * 0.6), fill=(0, 0, 0, 150))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(pad * 0.5))
    canvas.paste(shadow_layer,
                 (cx - pad + int(pad * 0.35), cover_top - pad + int(pad * 0.35)),
                 shadow_layer)
    ImageDraw.Draw(canvas, "RGBA").rounded_rectangle(
        [cx - pad, cover_top - pad, cx + disp_w + pad, cover_top + disp_h + pad],
        radius=int(pad * 0.6), fill=brand["accent"])
    canvas.paste(disp, (cx, cover_top), disp)
    y = cover_top + disp_h + gap

    y = draw_centered(draw, hook_lines, f_hook, w // 2, y, brand["accent_light"], shadow=True)
    y += int(h * 0.012)
    draw_centered(draw, [author_line], f_author, w // 2, y, "white", leading=1.2)

    by = h - bar_h
    draw_persistent_link_bar(canvas, cfg, brand)
    return canvas.convert("RGB")


def compose_scene_frame(cfg: Dict[str, Any], cover_path: str,
                        brand: Dict[str, Any], beat_text: str) -> Image.Image:
    """A cinematic teaser beat: blurred cover bg + the cover art + one beat line."""
    w, h = cfg["size"]
    book = cfg["book"]
    side = int(w * 0.09)
    inner_w = w - 2 * side

    canvas = _build_background(cover_path, w, h, brand["bg"])
    canvas = canvas.convert("RGBA")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle([0, 0, w, int(h * 0.012)], fill=brand["accent"])

    family = cfg["branding"]["font_family"]
    f_beat = load_font(int(w * 0.072), family, bold=True)
    f_author = load_font(int(w * 0.04), family, italic=True)

    bar_h = int(h * 0.09)
    cover_top = int(h * 0.10)
    cover_h = int(h * 0.36)
    cover_img = Image.open(cover_path).convert("RGBA")
    cw, chh = cover_img.size
    scale = cover_h / chh
    dw = int(cw * scale)
    dh = cover_h
    if dw > inner_w:
        s2 = inner_w / dw
        dw = int(dw * s2)
        dh = int(dh * s2)
    disp = cover_img.resize((dw, dh), Image.LANCZOS)
    cx = (w - dw) // 2
    pad = max(6, int(w * 0.012))

    shadow_layer = Image.new("RGBA", (dw + 2 * pad, dh + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(shadow_layer).rounded_rectangle(
        [0, 0, dw + 2 * pad - 1, dh + 2 * pad - 1],
        radius=int(pad * 0.6), fill=(0, 0, 0, 150))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(pad * 0.5))
    canvas.paste(shadow_layer, (cx - pad + int(pad * 0.35), cover_top - pad + int(pad * 0.35)),
                 shadow_layer)
    ImageDraw.Draw(canvas, "RGBA").rounded_rectangle(
        [cx - pad, cover_top - pad, cx + dw + pad, cover_top + dh + pad],
        radius=int(pad * 0.6), fill=brand["accent"])
    canvas.paste(disp, (cx, cover_top), disp)

    y = cover_top + dh + int(h * 0.04)
    beat_lines = wrap_text(draw, beat_text, f_beat, inner_w)
    y = draw_centered(draw, beat_lines, f_beat, w // 2, y, brand["accent_light"], shadow=True)
    author_y = h - bar_h - int(h * 0.055)
    draw_centered(draw, [f"by {book['author']}"], f_author, w // 2, author_y,
                  "white", leading=1.0)
    draw_persistent_link_bar(canvas, cfg, brand)
    return canvas.convert("RGB")


def _apply_motion(clip, motion: str, duration: float, w: int, h: int,
                  intensity: float = 0.08):
    amt = max(0.02, intensity)
    if motion == "out":
        clip = clip.resized(lambda t: (1.0 + amt) - amt * (t / duration))
    else:
        clip = clip.resized(lambda t: 1.0 + amt * (t / duration))
    return clip.cropped(x_center=w / 2, y_center=h / 2, width=w, height=h)


def _build_background(cover_path: str, w: int, h: int,
                      bg_color: Tuple[int, int, int]) -> Image.Image:
    base = Image.new("RGBA", (w, h), bg_color + (255,))
    try:
        cover = Image.open(cover_path).convert("RGB").resize((w, h))
        blurred = cover.filter(ImageFilter.GaussianBlur(radius=w * 0.05))
        blurred = blurred.convert("RGBA")
        dark = Image.new("RGBA", (w, h), (0, 0, 0, 168))
        base = Image.alpha_composite(blurred, dark)
    except Exception:
        pass
    vignette = Image.new("L", (w, h), 0)
    vdraw = ImageDraw.Draw(vignette)
    vdraw.ellipse([-w * 0.3, -h * 0.1, w * 1.3, h * 1.1], fill=0)
    base.putalpha(Image.composite(
        Image.new("L", (w, h), 255),
        Image.new("L", (w, h), 60),
        _radial_mask(w, h),
    ))
    return base.convert("RGB")


def _radial_mask(w: int, h: int) -> Image.Image:
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    for i in range(0, 120, 4):
        alpha = int(255 * (1 - i / 120))
        md.ellipse([-w * 0.3 + i, -h * 0.1 + i, w * 1.3 - i, h * 1.1 - i], fill=alpha)
    return mask


# --------------------------------------------------------------------------- #
# Output generation
# --------------------------------------------------------------------------- #

def generate_image_short(cfg: Dict[str, Any], cover_path: str,
                         brand: Dict[str, Any], hook_text: str,
                         out_path: Path) -> None:
    frame = compose_frame(cfg, cover_path, brand, hook_text)
    frame.save(out_path, "PNG", optimize=True)


def generate_video_reel(cfg: Dict[str, Any], frame_path: Path,
                        out_path: Path) -> None:
    if not HAS_MOVIEPY:
        raise RuntimeError(
            "moviepy is required for video output. Install with: pip install moviepy"
        )
    w, h = cfg["size"]
    duration = cfg["settings"]["duration_seconds"]
    video = cfg["video"]
    fade = video["fade_seconds"]
    zoom = video["zoom"]
    ken_burns = cfg["settings"]["ken_burns"]

    clip = ImageClip(str(frame_path)).with_duration(duration).with_fps(24)
    if ken_burns and zoom > 0:
        base = 1.0 + zoom * 0.4
        clip = clip.resized(lambda t: base + zoom * (t / duration))
        clip = clip.cropped(x_center=w / 2, y_center=h / 2, width=w, height=h)
    if fade > 0:
        clip = clip.with_effects([vfx.FadeIn(fade), vfx.FadeOut(fade)])
    clip.write_videofile(
        str(out_path),
        fps=24,
        codec="libx264",
        audio=False,
        preset=video["preset"],
        ffmpeg_params=["-pix_fmt", "yuv420p"],
        logger=None,
    )


def generate_teaser(cfg: Dict[str, Any], cover_path: str, brand: Dict[str, Any],
                    scenes: List[str], out_path: Path) -> None:
    """Multi-scene teaser: each beat is a frame with Ken Burns motion, then a title reveal."""
    from moviepy import ImageClip, vfx, concatenate_videoclips
    if not HAS_MOVIEPY:
        raise RuntimeError("moviepy is required for teaser output. pip install moviepy")

    w, h = cfg["size"]
    total = cfg["settings"]["duration_seconds"]
    fade = cfg["video"]["fade_seconds"]
    intensity = cfg["video"]["zoom"]

    n_frames = len(scenes) + 1
    dur_each = total / n_frames

    frames = [compose_scene_frame(cfg, cover_path, brand, beat) for beat in scenes]
    title_hook = cfg["book"].get("tagline") or (cfg["hooks"][0] if cfg["hooks"] else "")
    frames.append(compose_frame(cfg, cover_path, brand, title_hook))

    clips = []
    tmp_files: List[Path] = []
    for i, frame in enumerate(frames):
        tmp = out_path.parent / f".{cfg['slug']}_frm{i}.png"
        frame.save(tmp, "PNG")
        tmp_files.append(tmp)
        clip = ImageClip(str(tmp)).with_duration(dur_each).with_fps(24)
        motion = "out" if i % 2 else "in"
        clips.append(_apply_motion(clip, motion, dur_each, w, h, intensity))

    video = concatenate_videoclips(clips, method="chain").with_fps(24)
    if fade > 0:
        f = min(fade, dur_each * 0.5)
        video = video.with_effects([vfx.FadeIn(f), vfx.FadeOut(f)])
    try:
        video.write_videofile(str(out_path), fps=24, codec="libx264", audio=False,
                              preset=cfg["video"]["preset"],
                              ffmpeg_params=["-pix_fmt", "yuv420p"], logger=None)
    finally:
        for tmp in tmp_files:
            if tmp.exists():
                tmp.unlink()


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _interp_camera(waypoints, nt: float):
    nt = _clamp(nt, 0.0, 1.0)
    for i in range(len(waypoints) - 1):
        t0, cx0, cy0, f0 = waypoints[i]
        t1, cx1, cy1, f1 = waypoints[i + 1]
        if t0 <= nt <= t1:
            p = 0.0 if t1 == t0 else (nt - t0) / (t1 - t0)
            return (_lerp(cx0, cx1, p), _lerp(cy0, cy1, p), _lerp(f0, f1, p))
    last = waypoints[-1]
    return (last[1], last[2], last[3])


def _hex(color: Tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % color


def _cover_fill(cover: Image.Image, cw: int, chh: int, base_w: int, base_h: int,
                cx_f: float, cy_f: float, f: float, w: int, h: int,
                brightness: float = 1.0) -> Image.Image:
    rw = base_w * f
    rh = base_h * f
    minx, maxx = rw / 2, cw - rw / 2
    miny, maxy = rh / 2, chh - rh / 2
    cx = minx + (maxx - minx) * cx_f
    cy = miny + (maxy - miny) * cy_f
    x0 = max(0, int(cx - rw / 2))
    y0 = max(0, int(cy - rh / 2))
    x1 = min(cw, int(cx + rw / 2))
    y1 = min(chh, int(cy + rh / 2))
    img = cover.crop((x0, y0, x1, y1)).resize((w, h), Image.LANCZOS)
    if brightness and brightness != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brightness)
    return img


def synth_thriller_audio(duration: float, sr: int = 44100):
    """Original, royalty-free LIGHT CONTINUOUS thriller bed: a sustained A-minor
    pad that breathes/evolves, airy shimmer that opens up over time, soft sub
    weight, a gentle end swell. No percussion - smooth and continuous."""
    import numpy as np
    from moviepy import AudioArrayClip
    n = int(sr * duration)
    t = np.arange(n) / sr
    out = np.zeros(n, dtype=np.float64)

    partials = [
        (110.00, 0.34, 0.07),
        (110.45, 0.20, 0.09),
        (164.81, 0.26, 0.05),
        (220.00, 0.30, 0.11),
        (261.63, 0.22, 0.13),
        (329.63, 0.16, 0.17),
        (440.00, 0.07, 0.23),
    ]
    pad = np.zeros(n, dtype=np.float64)
    for f, amp, lr in partials:
        lfo = 0.5 + 0.5 * np.sin(2 * np.pi * lr * t + f)
        pad += amp * lfo * np.sin(2 * np.pi * f * t)
    out += 0.30 * pad

    out += 0.10 * np.sin(2 * np.pi * 55.0 * t)

    noise = np.random.RandomState(11).randn(n)
    k = 300
    kernel = np.exp(-(np.arange(-k, k + 1) ** 2) / (2 * (k / 3.0) ** 2))
    kernel /= kernel.sum()
    lp = np.convolve(noise, kernel, mode="same")
    open_env = np.clip((t - 1.0) / (duration * 0.6), 0, 1)
    out += 0.05 * lp * (0.5 + 0.5 * np.sin(2 * np.pi * 0.2 * t)) * open_env

    rs, re = 0.70 * duration, 0.90 * duration
    prog = np.clip((t - rs) / (re - rs), 0, 1)
    freq = 160.0 + 260.0 * prog
    phase = 2 * np.pi * np.cumsum(freq) / sr
    swell = (prog ** 2) * np.clip((duration - 0.8 - t) / 0.8, 0, 1)
    out += 0.10 * np.sin(phase) * swell
    out += 0.05 * lp * swell

    end_env = np.exp(-((t - (duration - 0.7)) / 0.5) ** 2)
    out += 0.12 * end_env * np.sin(2 * np.pi * 130.81 * t)

    env = np.ones(n)
    fi = int(1.2 * sr)
    fo = int(2.0 * sr)
    if fi:
        env[:fi] = np.linspace(0, 1, fi)
    if fo:
        env[-fo:] *= np.linspace(1, 0, fo)
    out *= env

    peak = np.max(np.abs(out))
    if peak > 0:
        out = 0.72 * out / peak

    left = out * (1 + 0.05 * np.sin(2 * np.pi * 0.06 * t))
    right = out * (1 - 0.05 * np.sin(2 * np.pi * 0.06 * t))
    stereo = np.stack([left, right], axis=1).astype(np.float32)
    return AudioArrayClip(stereo, fps=sr)


def build_audio(cfg: Dict[str, Any], total: float):
    """Return a moviepy audio clip for the reel (synth bed, file, or None)."""
    mode = str(cfg["settings"].get("audio", "none")).strip().lower()
    if mode in ("auto", "synth"):
        try:
            print("  -> audio  synthesized thriller bed")
            return synth_thriller_audio(total)
        except Exception as exc:
            print(f"  [warn] audio synth failed: {exc}")
            return None
    if mode and mode not in ("none", "off", ""):
        ap = Path(mode)
        if not ap.is_absolute():
            ap = (cfg["root"] / ap)
        if ap.exists():
            try:
                from moviepy import AudioFileClip
                print(f"  -> audio  {ap.name}")
                return AudioFileClip(str(ap)).with_duration(total)
            except Exception as exc:
                print(f"  [warn] audio load failed: {exc}")
    return None


def write_with_audio(clip, out_path: Path, cfg: Dict[str, Any], audio_clip) -> None:
    params = ["-pix_fmt", "yuv420p"]
    if audio_clip is not None:
        clip.with_audio(audio_clip).write_videofile(
            str(out_path), fps=24, codec="libx264", audio=True, audio_codec="aac",
            preset=cfg["video"]["preset"], ffmpeg_params=params, logger=None)
    else:
        clip.write_videofile(
            str(out_path), fps=24, codec="libx264", audio=False,
            preset=cfg["video"]["preset"], ffmpeg_params=params, logger=None)


def generate_cinematic_teaser(cfg: Dict[str, Any], cover_path: str,
                              brand: Dict[str, Any], scenes: List[str],
                              out_path: Path) -> None:
    """3-act cinematic teaser: cover (intro) -> 7s story with moving elements
    -> cover (outro). Continuous camera move across the artwork, animated gold
    particles, light sweep, line-by-line text reveal. KDP link bar is drawn last
    at a fixed location on every frame (superimposed)."""
    import numpy as np
    from moviepy import VideoClip
    if not HAS_MOVIEPY:
        raise RuntimeError("moviepy is required for cinematic teaser. pip install moviepy")

    w, h = cfg["size"]
    total = float(cfg["settings"]["duration_seconds"])
    intro = float(cfg["settings"].get("intro_seconds", 1.0))
    outro = float(cfg["settings"].get("outro_seconds", 2.0))
    family = cfg["branding"]["font_family"]
    book = cfg["book"]
    accent = brand["accent"]
    accent_light = brand["accent_light"]

    if intro + outro >= total:
        intro = outro = 0.0
    intro_end = intro
    outro_start = total - outro
    story_len = max(0.1, outro_start - intro_end)

    cover = Image.open(cover_path).convert("RGB")
    cw, chh = cover.size
    out_ar = w / h
    if cw / chh >= out_ar:
        base_h = chh
        base_w = max(1, int(round(chh * out_ar)))
    else:
        base_w = cw
        base_h = max(1, int(round(cw / out_ar)))

    f_beat = load_font(int(w * 0.072), family, bold=True)
    f_sub = load_font(int(w * 0.052), family, bold=True)
    f_auth = load_font(int(w * 0.045), family, italic=True)
    f_label = load_font(int(w * 0.034), family, bold=True)
    f_link = load_font(int(w * 0.05), family, bold=True)

    side = int(w * 0.09)
    inner_w = w - 2 * side

    grad = np.zeros((h, w, 4), dtype=np.uint8)
    top0 = int(h * 0.52)
    for y in range(top0, h):
        a = int(195 * _clamp((y - top0) / (h - top0)) ** 1.2)
        grad[y, :, 3] = a
    lower_third = Image.fromarray(grad)

    ps = 40
    psprite = Image.new("RGBA", (ps, ps), (0, 0, 0, 0))
    pd = ImageDraw.Draw(psprite)
    for r in range(ps // 2, 0, -1):
        a = int(255 * (1 - r / (ps / 2)) ** 2 * 0.5)
        pd.ellipse([ps / 2 - r, ps / 2 - r, ps / 2 + r, ps / 2 + r],
                   fill=accent_light + (a,))
    rng = random.Random(2024)
    parts = [{
        "x": rng.random() * w, "y": rng.random() * h,
        "v": 18 + rng.random() * 55, "amp": 6 + rng.random() * 34,
        "fr": 0.5 + rng.random() * 1.6, "ph": rng.random() * 6.28,
        "r": 0.4 + rng.random() * 1.4, "tw": 1.2 + rng.random() * 3.0,
    } for _ in range(75)]

    sw = int(w * 0.55)
    strip = Image.new("L", (sw, h), 0)
    sd = ImageDraw.Draw(strip)
    for x in range(sw):
        a = int(58 * math.exp(-((x - sw / 2) / (sw / 6)) ** 2))
        sd.line([(x, 0), (x, h)], fill=a)

    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    vig = Image.fromarray((np.clip((dist - 0.55) / 0.8, 0, 1) * 130).astype("uint8"))

    story_wp = [
        (0.00, 0.30, 0.55, 0.92),
        (0.30, 0.58, 0.50, 0.86),
        (0.55, 0.72, 0.44, 0.84),
        (0.80, 0.42, 0.55, 0.87),
        (1.00, 0.50, 0.50, 0.90),
    ]

    bar_h = int(h * 0.085)
    by = h - bar_h
    cta_text = cfg["settings"].get("call_to_action") or "Get the book"
    brightness = float(cfg["settings"].get("brightness", 1.0))

    def draw_link_bar(img: Image.Image) -> None:
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([0, by, w, h], fill=accent + (250,))
        d.rectangle([0, by, w, by + max(3, int(h * 0.004))], fill=accent_light + (255,))
        size = int(w * 0.052)
        f = load_font(size, family, bold=True)
        while d.textlength(cta_text, font=f) > w * 0.92 and size > 16:
            size -= 2
            f = load_font(size, family, bold=True)
        tw = d.textlength(cta_text, font=f)
        th = line_height(f)
        d.text((w / 2 - tw / 2, by + (bar_h - th) / 2), cta_text, font=f,
               fill=(255, 255, 255, 255))

    def add_motion_layers(frame: Image.Image, t: float) -> None:
        for p in parts:
            py = (p["y"] - p["v"] * t) % h
            px = (p["x"] + p["amp"] * math.sin(p["fr"] * t + p["ph"])) % w
            tw = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(p["tw"] * t + p["ph"]))
            sz = max(2, int(p["r"] * 18))
            spr = psprite.resize((sz, sz), Image.LANCZOS)
            spr.putalpha(spr.split()[3].point(lambda v: int(v * tw)))
            frame.alpha_composite(spr, (int(px - sz / 2), int(py - sz / 2)))
        sx = int(((t / 4.2) * (w + sw)) - sw)
        if -sw < sx < w:
            mask = Image.new("L", (w, h), 0)
            mask.paste(strip, (sx, 0))
            sweep = Image.new("RGBA", (w, h), (255, 248, 230, 0))
            sweep.putalpha(mask)
            frame.alpha_composite(sweep)
        frame.paste(Image.new("RGBA", (w, h), (0, 0, 0, 255)), (0, 0), vig)

    def story_text(frame: Image.Image, t: float) -> None:
        slt = t - intro_end
        n_seg = max(1, len(scenes))
        seg = min(int(slt / (story_len / n_seg)), n_seg - 1)
        local = slt - seg * (story_len / n_seg)
        seg_dur = story_len / n_seg
        s_alpha = _clamp(local / 0.3) * _clamp((seg_dur - local) / 0.3)
        if s_alpha <= 0.01:
            return
        d = ImageDraw.Draw(frame, "RGBA")
        lines = wrap_text(d, scenes[seg], f_beat, inner_w)
        lh = int(line_height(f_beat) * 1.18)
        yy = int(h * 0.60)
        for i, ln in enumerate(lines):
            appear = i * 0.16
            prog = _clamp((local - appear) / 0.3)
            la = prog * s_alpha
            if la <= 0.01:
                yy += lh
                continue
            rise = (1 - prog) * 24
            tw = d.textlength(ln, font=f_beat)
            x = w / 2 - tw / 2
            d.text((x + 2, yy + 2 + rise), ln, font=f_beat, fill=(0, 0, 0, int(la * 170)))
            d.text((x, yy + rise), ln, font=f_beat, fill=accent_light + (int(la * 255),))
            yy += lh

    def outro_text(frame: Image.Image, t: float) -> None:
        local = t - outro_start
        out_len = total - outro_start
        glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gp = 0.5 + 0.5 * math.sin(t * 2.2)
        gd.ellipse([w * 0.2, h * 0.32, w * 0.8, h * 0.60], fill=accent + (int(35 + 45 * gp),))
        frame.alpha_composite(glow.filter(ImageFilter.GaussianBlur(w * 0.05)))
        d = ImageDraw.Draw(frame, "RGBA")
        sub = book.get("tagline") or ""
        slines = wrap_text(d, sub, f_sub, inner_w)
        yy = int(h * 0.40)
        lh = int(line_height(f_sub) * 1.2)
        for i, ln in enumerate(slines):
            la = _clamp((local - i * 0.18) / 0.35)
            if la <= 0.01:
                yy += lh
                continue
            tw = d.textlength(ln, font=f_sub)
            x = w / 2 - tw / 2
            d.text((x + 2, yy + 2), ln, font=f_sub, fill=(0, 0, 0, int(la * 170)))
            d.text((x, yy), ln, font=f_sub, fill=(255, 255, 255, int(la * 255)))
            yy += lh
        au = f"by {book['author']}"
        la2 = _clamp((local - 0.5) / 0.4)
        if la2 > 0.01:
            tw = d.textlength(au, font=f_auth)
            x = w / 2 - tw / 2
            d.text((x, yy + int(h * 0.02)), au, font=f_auth,
                   fill=accent_light + (int(la2 * 255),))

    def make_frame(t):
        if t < intro_end:
            p = t / max(intro_end, 0.001)
            frame = _cover_fill(cover, cw, chh, base_w, base_h, 0.5, 0.5,
                                _lerp(1.0, 0.96, p), w, h, brightness).convert("RGBA")
        elif t < outro_start:
            sp = (t - intro_end) / story_len
            cx_f, cy_f, f = _interp_camera(story_wp, sp)
            frame = _cover_fill(cover, cw, chh, base_w, base_h, cx_f, cy_f, f, w, h, brightness).convert("RGBA")
            frame.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 0, 45)))
            frame.alpha_composite(lower_third)
            story_text(frame, t)
        else:
            p = (t - outro_start) / max((total - outro_start), 0.001)
            frame = _cover_fill(cover, cw, chh, base_w, base_h, 0.5, 0.5,
                                _lerp(0.97, 1.0, p), w, h, brightness).convert("RGBA")
            outro_text(frame, t)

        add_motion_layers(frame, t)

        gf = _clamp(t / 0.4) * _clamp((total - t) / 0.5)
        if gf < 0.999:
            frame.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 0, int((1 - gf) * 255))))

        draw_link_bar(frame)
        return np.array(frame.convert("RGB"))

    clip = VideoClip(make_frame, duration=total)
    audio_clip = build_audio(cfg, total)
    write_with_audio(clip, out_path, cfg, audio_clip)


def generate_quote_reel(cfg: Dict[str, Any], cover_path: str, brand: Dict[str, Any],
                        quote_text: str, out_path: Path) -> None:
    """Text-forward 'pull-quote' reel: an evocative line fading/rising in over a
    dark, gold-tinted blurred cover, with a big quotation mark, slow drift,
    attribution and the persistent CTA bar. Distinct from the cover-pan teaser."""
    import numpy as np
    from moviepy import VideoClip
    if not HAS_MOVIEPY:
        raise RuntimeError("moviepy is required. pip install moviepy")

    w, h = cfg["size"]
    total = float(cfg["settings"]["duration_seconds"])
    family = cfg["branding"]["font_family"]
    book = cfg["book"]
    accent = brand["accent"]
    accent_light = brand["accent_light"]
    brightness = float(cfg["settings"].get("brightness", 1.0))

    cover = Image.open(cover_path).convert("RGB")
    cw, chh = cover.size
    out_ar = w / h
    if cw / chh >= out_ar:
        base_h = chh
        base_w = max(1, int(round(chh * out_ar)))
    else:
        base_w = cw
        base_h = max(1, int(round(cw / out_ar)))

    f_q = load_font(int(w * 0.078), family, bold=True)
    f_att = load_font(int(w * 0.05), family, bold=True)
    f_auth = load_font(int(w * 0.042), family, italic=True)
    f_qm = load_font(int(w * 0.5), family, bold=True)
    side = int(w * 0.1)
    inner_w = w - 2 * side

    qm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(qm).text((side, int(h * 0.05)), "\u201c", font=f_qm, fill=accent + (45,))
    qm = qm.filter(ImageFilter.GaussianBlur(2))

    rng = random.Random(99)
    psprite = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    pd = ImageDraw.Draw(psprite)
    for r in range(20, 0, -1):
        a = int(255 * (1 - r / 20) ** 2 * 0.5)
        pd.ellipse([20 - r, 20 - r, 20 + r, 20 + r], fill=accent_light + (a,))
    parts = [{
        "x": rng.random() * w, "y": rng.random() * h,
        "v": 10 + rng.random() * 35, "amp": 5 + rng.random() * 28,
        "fr": 0.4 + rng.random() * 1.3, "ph": rng.random() * 6.28,
        "r": 0.4 + rng.random() * 1.2, "tw": 1.0 + rng.random() * 2.5,
    } for _ in range(40)]

    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    vig = Image.fromarray((np.clip((dist - 0.55) / 0.8, 0, 1) * 120).astype("uint8"))

    tmp = Image.new("RGB", (w, h))
    qlines = wrap_text(ImageDraw.Draw(tmp), quote_text, f_q, inner_w)
    lh = int(line_height(f_q) * 1.25)
    auth = f"by {book['author']}"
    block_h = lh * len(qlines) + int(h * 0.05) + line_height(f_att) + int(h * 0.015) + line_height(f_auth)
    start_y = max(int(h * 0.12), int(h * 0.42) - block_h // 2)
    appear_base = len(qlines) * 0.55

    def make_frame(t):
        p = t / total
        frame = _cover_fill(cover, cw, chh, base_w, base_h, 0.5, 0.5,
                            _lerp(1.0, 0.95, p), w, h, brightness).convert("RGBA")
        frame.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 0, 155)))
        frame.alpha_composite(Image.new("RGBA", (w, h), accent + (16,)))
        frame.alpha_composite(qm)

        for pt in parts:
            py = (pt["y"] - pt["v"] * t) % h
            px = (pt["x"] + pt["amp"] * math.sin(pt["fr"] * t + pt["ph"])) % w
            tw = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(pt["tw"] * t + pt["ph"]))
            sz = max(2, int(pt["r"] * 18))
            spr = psprite.resize((sz, sz), Image.LANCZOS)
            spr.putalpha(spr.split()[3].point(lambda v: int(v * tw)))
            frame.alpha_composite(spr, (int(px - sz / 2), int(py - sz / 2)))

        d = ImageDraw.Draw(frame, "RGBA")
        y = start_y
        for i, ln in enumerate(qlines):
            prog = _clamp((t - i * 0.55) / 0.6)
            if prog <= 0:
                y += lh
                continue
            rise = (1 - prog) * 30
            tw = d.textlength(ln, font=f_q)
            x = w / 2 - tw / 2
            d.text((x + 2, y + 2 + rise), ln, font=f_q, fill=(0, 0, 0, int(prog * 170)))
            d.text((x, y + rise), ln, font=f_q, fill=(255, 255, 255, int(prog * 255)))
            y += lh

        y += int(h * 0.04)
        a_div = _clamp((t - (appear_base + 0.4)) / 0.5)
        if a_div > 0:
            dwid = int(w * 0.18)
            dx = w / 2 - dwid / 2
            d.rectangle([dx, y, dx + dwid, y + 3], fill=accent + (int(a_div * 255),))
        y += int(h * 0.03)

        a_att = _clamp((t - (appear_base + 0.7)) / 0.6)
        if a_att > 0:
            title = book.get("title", "")
            tw = d.textlength(title, font=f_att)
            d.text((w / 2 - tw / 2, y), title, font=f_att, fill=accent_light + (int(a_att * 255),))
            y += int(line_height(f_att) * 1.2)
            tw = d.textlength(auth, font=f_auth)
            d.text((w / 2 - tw / 2, y), auth, font=f_auth, fill=(235, 235, 235, int(a_att * 255)))

        frame.paste(Image.new("RGBA", (w, h), (0, 0, 0, 255)), (0, 0), vig)

        gf = _clamp(t / 0.5) * _clamp((total - t) / 0.6)
        if gf < 0.999:
            frame.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 0, int((1 - gf) * 255))))

        draw_persistent_link_bar(frame, cfg, brand)
        return np.array(frame.convert("RGB"))

    clip = VideoClip(make_frame, duration=total)
    write_with_audio(clip, out_path, cfg, build_audio(cfg, total))


def generate_story_reel(cfg: Dict[str, Any], brand: Dict[str, Any],
                        scene_paths: List[str], beats: List[str], out_path: Path) -> None:
    """Multi-scene 'story' reel: sequences the book's artwork panels (temple,
    character, treasure, cover) as distinct cinematic scenes, each narrated by a
    story beat. Uses the cover/artwork as the visual reference for the story."""
    import numpy as np
    from moviepy import VideoClip
    if not HAS_MOVIEPY:
        raise RuntimeError("moviepy is required. pip install moviepy")

    w, h = cfg["size"]
    total = float(cfg["settings"]["duration_seconds"])
    family = cfg["branding"]["font_family"]
    book = cfg["book"]
    accent = brand["accent"]
    accent_light = brand["accent_light"]
    brightness = float(cfg["settings"].get("brightness", 1.0))
    out_ar = w / h

    scenes = []
    for sp in scene_paths:
        try:
            im = Image.open(sp).convert("RGB")
        except Exception as exc:
            print(f"  [warn] scene unreadable: {sp}: {exc}")
            continue
        cw, chh = im.size
        if cw / chh >= out_ar:
            base_h = chh
            base_w = max(1, int(round(chh * out_ar)))
        else:
            base_w = cw
            base_h = max(1, int(round(cw * out_ar)))
        scenes.append((im, cw, chh, base_w, base_h))
    if not scenes:
        raise RuntimeError("no usable scene images for story reel")

    n = max(1, len(scenes))
    per = total / n

    f_beat = load_font(int(w * 0.07), family, bold=True)
    side = int(w * 0.09)
    inner_w = w - 2 * side

    grad = np.zeros((h, w, 4), dtype=np.uint8)
    top0 = int(h * 0.55)
    for y in range(top0, h):
        grad[y, :, 3] = int(185 * _clamp((y - top0) / (h - top0)) ** 1.2)
    lower_third = Image.fromarray(grad)

    rng = random.Random(7)
    psprite = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    pd = ImageDraw.Draw(psprite)
    for r in range(20, 0, -1):
        a = int(255 * (1 - r / 20) ** 2 * 0.5)
        pd.ellipse([20 - r, 20 - r, 20 + r, 20 + r], fill=accent_light + (a,))
    parts = [{
        "x": rng.random() * w, "y": rng.random() * h,
        "v": 15 + rng.random() * 45, "amp": 6 + rng.random() * 30,
        "fr": 0.5 + rng.random() * 1.5, "ph": rng.random() * 6.28,
        "r": 0.4 + rng.random() * 1.3, "tw": 1.2 + rng.random() * 2.8,
    } for _ in range(70)]

    yy, xx = np.mgrid[0:h, 0:w]
    dist = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    vig = Image.fromarray((np.clip((dist - 0.55) / 0.8, 0, 1) * 125).astype("uint8"))

    def make_frame(t):
        i = min(int(t / per), n - 1)
        local = t - i * per
        p = local / per
        im, cw, chh, bw, bh = scenes[i]
        f = (0.92 - 0.08 * p) if i % 2 == 0 else (0.84 + 0.08 * p)
        frame = _cover_fill(im, cw, chh, bw, bh, 0.5, 0.5, f, w, h, brightness).convert("RGBA")
        frame.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 0, 60)))
        frame.alpha_composite(lower_third)

        for pt in parts:
            py = (pt["y"] - pt["v"] * t) % h
            px = (pt["x"] + pt["amp"] * math.sin(pt["fr"] * t + pt["ph"])) % w
            tw = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(pt["tw"] * t + pt["ph"]))
            sz = max(2, int(pt["r"] * 18))
            spr = psprite.resize((sz, sz), Image.LANCZOS)
            spr.putalpha(spr.split()[3].point(lambda v: int(v * tw)))
            frame.alpha_composite(spr, (int(px - sz / 2), int(py - sz / 2)))

        d = ImageDraw.Draw(frame, "RGBA")
        beat = beats[i] if i < len(beats) else ""
        s_alpha = _clamp(local / 0.4) * _clamp((per - local) / 0.4)
        if beat and s_alpha > 0.01:
            lines = wrap_text(d, beat, f_beat, inner_w)
            lh = int(line_height(f_beat) * 1.18)
            y = int(h * 0.62)
            for ln in lines:
                tw = d.textlength(ln, font=f_beat)
                x = w / 2 - tw / 2
                d.text((x + 2, y + 2), ln, font=f_beat, fill=(0, 0, 0, int(s_alpha * 170)))
                d.text((x, y), ln, font=f_beat, fill=accent_light + (int(s_alpha * 255),))
                y += lh

        frame.paste(Image.new("RGBA", (w, h), (0, 0, 0, 255)), (0, 0), vig)
        gf = _clamp(t / 0.4) * _clamp((total - t) / 0.5)
        if gf < 0.999:
            frame.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 0, int((1 - gf) * 255))))
        draw_persistent_link_bar(frame, cfg, brand)
        return np.array(frame.convert("RGB"))

    clip = VideoClip(make_frame, duration=total)
    write_with_audio(clip, out_path, cfg, build_audio(cfg, total))


def generate_html_player(out_path: Path, mp4_name: str, poster_name: Optional[str],
                         kdp_link: str, brand: Dict[str, Any], cfg: Dict[str, Any]) -> None:
    """Self-contained HTML5 player: plays the MP4 with a clickable KDP link
    pinned to the same fixed location as the in-video bar (opens site on click)."""
    book = cfg["book"]
    cta = (cfg["settings"].get("call_to_action") or "Get the book").replace("<", "").replace(">", "")
    accent = _hex(brand["accent"])
    accent_light = _hex(brand["accent_light"])
    title = (book.get("title") or "Book").replace("<", "").replace(">", "")
    poster_attr = f' poster="{poster_name}"' if poster_name else ""
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - Reel</title>
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; height: 100%; background: #050505;
    font-family: Arial, Helvetica, sans-serif; }}
  body {{ display: flex; align-items: center; justify-content: center; }}
  .stage {{ position: relative; height: 100%; aspect-ratio: 9 / 16; max-width: 100vw;
    background: #000; overflow: hidden; box-shadow: 0 0 60px rgba(0,0,0,.6); }}
  video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .hint {{ position: absolute; top: 10px; left: 0; right: 0; text-align: center;
    color: #fff; font-size: 13px; letter-spacing: .08em; opacity: .8;
    text-shadow: 0 1px 3px #000; }}
  a.link {{ position: absolute; left: 0; right: 0; bottom: 0; height: 9%;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 2px; text-decoration: none; background: {accent};
    border-top: 3px solid {accent_light}; cursor: pointer; }}
  a.link:hover {{ filter: brightness(1.12); }}
  a.link small {{ font-size: clamp(9px, 1.7vw, 15px); letter-spacing: .14em;
    color: #f7f2e8; text-shadow: 0 1px 2px rgba(0,0,0,.5); }}
  a.link b {{ font-size: clamp(13px, 2.7vw, 24px); font-weight: 800; color: #fff;
    text-shadow: 0 1px 3px rgba(0,0,0,.6); }}
</style>
</head>
<body>
  <div class="stage">
    <video src="{mp4_name}"{poster_attr} autoplay muted loop playsinline controls></video>
    <div class="hint">Tap below to read on Amazon</div>
    <a class="link" href="{kdp_link}" target="_blank" rel="noopener">
      <b>{cta}</b>
    </a>
  </div>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")


def copy_outputs(output_dir: Path, targets: List[Path]) -> List[Path]:
    copied: List[Path] = []
    assets = [p for p in output_dir.iterdir() if p.is_file()
              and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".mp4", ".gif", ".webp"}]
    for target in targets:
        try:
            reels_dir = target / "reels"
            reels_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            print(f"[warn] could not create {target}/reels: {exc}")
            continue
        for asset in assets:
            dest = reels_dir / asset.name
            shutil.copy2(asset, dest)
            copied.append(dest)
    return copied


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate vertical book marketing reels & shorts from ReelGen.md")
    parser.add_argument("--config", default="ReelGen.md", help="Path to ReelGen.md")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--formats", default=None,
                        help="Override formats (comma list: image,video)")
    parser.add_argument("--no-copy", action="store_true",
                        help="Do not copy outputs into target_projects")
    parser.add_argument("--no-audio", action="store_true",
                        help="Render the teaser without an audio track")
    parser.add_argument("--suffix", default="",
                        help="Filename suffix for teaser/html (e.g. _nomusic)")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    if not config_path.exists():
        print(f"[error] config not found: {config_path}", file=sys.stderr)
        return 2
    root = config_path.parent

    raw = parse_reelgen(config_path)
    cfg = normalize_config(raw, root)

    if args.formats:
        cfg["settings"]["formats"] = {f.strip().lower() for f in args.formats.split(",") if f.strip()}

    book = cfg["book"]
    settings = cfg["settings"]
    formats = settings["formats"]

    print(f"Book        : {book['title']} — {book['author']}")
    print(f"Size        : {cfg['size'][0]}x{cfg['size'][1]} ({settings['aspect_ratio']}, {settings['resolution']})")
    print(f"Formats     : {', '.join(sorted(formats))}")
    print(f"Reels       : {settings['count']} (hooks available: {len(cfg['hooks'])})")

    if "video" in formats and not HAS_MOVIEPY:
        print("[warn] moviepy not available — video output disabled. Install: pip install moviepy")
        formats.discard("video")
        if "image" not in formats:
            formats.add("image")

    output_dir = (root / args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    reference = book["reference_image"] or book["cover_image"]
    try:
        palette = extract_palette(reference)
    except Exception as exc:
        print(f"[warn] could not extract palette from {reference}: {exc}")
        palette = []
    brand = choose_brand(palette)
    print(f"Brand       : bg={brand['bg']} accent={brand['accent']}")

    if cfg["settings"].get("reel_type") == "quote":
        q = raw.get("quote")
        quote_text = (q.get("text") if isinstance(q, dict) else None) or \
                     (cfg["hooks"][0] if cfg["hooks"] else book["title"])
        slug = cfg["slug"]
        sfx = args.suffix or ""
        if args.no_audio:
            cfg["settings"]["audio"] = "none"
        quote_mp4 = output_dir / f"{slug}_quote{sfx}.mp4"
        print(f"Quote reel  : \"{quote_text[:60]}{'...' if len(quote_text) > 60 else ''}\" "
              f"({cfg['settings']['duration_seconds']}s)")
        print(f"  -> video  {quote_mp4.name}")
        generate_quote_reel(cfg, book["cover_image"], brand, quote_text, quote_mp4)
        (output_dir / "_manifest.json").write_text(json.dumps({
            "book": {k: book[k] for k in ("title", "author", "tagline", "kdp_link")},
            "mode": "quote", "quote": quote_text,
            "files": [quote_mp4.name],
        }, indent=2), encoding="utf-8")
        copied: List[Path] = []
        if not args.no_copy and cfg["target_projects"]:
            copied = copy_outputs(output_dir, cfg["target_projects"])
        print(f"\nDone. Output: {output_dir}")
        if copied:
            print(f"Copied {len(copied)} file(s) to {len(cfg['target_projects'])} project(s)")
        return 0

    if cfg["settings"].get("reel_type") == "story":
        story_scenes: List[str] = []
        for s in (raw.get("story_scenes") or []):
            sp = Path(os.path.expandvars(os.path.expanduser(str(s))))
            if not sp.is_absolute():
                sp = (root / sp)
            story_scenes.append(str(sp))
        story_beats = [b.strip() for b in (raw.get("story_beats") or []) if b.strip()]
        if not story_scenes:
            story_scenes = [book["cover_image"]]
        slug = cfg["slug"]
        sfx = args.suffix or ""
        if args.no_audio:
            cfg["settings"]["audio"] = "none"
        story_mp4 = output_dir / f"{slug}_story{sfx}.mp4"
        print(f"Story reel  : {len(story_scenes)} scenes / {len(story_beats)} beats "
              f"({cfg['settings']['duration_seconds']}s)")
        print(f"  -> video  {story_mp4.name}")
        generate_story_reel(cfg, brand, story_scenes, story_beats, story_mp4)
        (output_dir / "_manifest.json").write_text(json.dumps({
            "book": {k: book[k] for k in ("title", "author", "tagline", "kdp_link")},
            "mode": "story", "beats": story_beats,
            "files": [story_mp4.name],
        }, indent=2), encoding="utf-8")
        copied: List[Path] = []
        if not args.no_copy and cfg["target_projects"]:
            copied = copy_outputs(output_dir, cfg["target_projects"])
        print(f"\nDone. Output: {output_dir}")
        if copied:
            print(f"Copied {len(copied)} file(s) to {len(cfg['target_projects'])} project(s)")
        return 0

    if cfg.get("scenes"):
        if not HAS_MOVIEPY:
            print("[error] teaser mode needs moviepy. Install: pip install moviepy",
                  file=sys.stderr)
            return 1
        slug = cfg["slug"]
        sfx = args.suffix or ""
        if args.no_audio:
            cfg["settings"]["audio"] = "none"
        poster_path = output_dir / f"{slug}_poster.png"
        teaser_path = output_dir / f"{slug}_teaser{sfx}.mp4"
        cinematic = cfg["settings"].get("cinematic")
        print(f"Teaser mode : {len(cfg['scenes'])} beats + title reveal "
              f"({cfg['settings']['duration_seconds']}s total)"
              + (" [cinematic]" if cinematic else ""))
        print(f"  -> poster {poster_path.name}")
        generate_image_short(cfg, book["cover_image"], brand,
                             book.get("tagline") or "", poster_path)
        files = [poster_path.name]
        print(f"  -> video  {teaser_path.name}")
        if cinematic:
            generate_cinematic_teaser(cfg, book["cover_image"], brand, cfg["scenes"], teaser_path)
        else:
            generate_teaser(cfg, book["cover_image"], brand, cfg["scenes"], teaser_path)
        files.append(teaser_path.name)
        (output_dir / "_manifest.json").write_text(json.dumps({
            "book": {k: book[k] for k in ("title", "author", "tagline", "kdp_link")},
            "size": list(cfg["size"]),
            "mode": "cinematic" if cinematic else "teaser",
            "scenes": cfg["scenes"],
            "files": files,
        }, indent=2), encoding="utf-8")

        copied: List[Path] = []
        if not args.no_copy and cfg["target_projects"]:
            copied = copy_outputs(output_dir, cfg["target_projects"])
        print(f"\nDone. Output: {output_dir}")
        if copied:
            print(f"Copied {len(copied)} file(s) to {len(cfg['target_projects'])} project(s):")
            for t in cfg["target_projects"]:
                print(f"  - {t / 'reels'}")
        return 0

    count = settings["count"]
    hooks = cfg["hooks"]
    manifest: List[Dict[str, Any]] = []

    for i in range(count):
        hook = format_hook(hooks[i % len(hooks)], book, i)
        tag = f"reel_{i + 1:02d}"
        record: Dict[str, Any] = {"index": i + 1, "hook": hook, "files": []}

        if "image" in formats:
            img_path = output_dir / f"{tag}.png"
            print(f"  -> image  {img_path.name}")
            generate_image_short(cfg, book["cover_image"], brand, hook, img_path)
            record["files"].append(str(img_path.name))

        if "video" in formats:
            frame_for_video = output_dir / f".{tag}_frame.png"
            generate_image_short(cfg, book["cover_image"], brand, hook, frame_for_video)
            vid_path = output_dir / f"{tag}.mp4"
            print(f"  -> video  {vid_path.name}")
            try:
                generate_video_reel(cfg, frame_for_video, vid_path)
                record["files"].append(str(vid_path.name))
            except Exception as exc:
                print(f"  [warn] video failed for {tag}: {exc}")
            finally:
                if frame_for_video.exists():
                    frame_for_video.unlink()

        manifest.append(record)

    (output_dir / "_manifest.json").write_text(
        json.dumps({
            "book": {k: book[k] for k in ("title", "author", "tagline", "kdp_link")},
            "size": list(cfg["size"]),
            "reels": manifest,
        }, indent=2), encoding="utf-8")

    copied: List[Path] = []
    if not args.no_copy and cfg["target_projects"]:
        copied = copy_outputs(output_dir, cfg["target_projects"])

    print(f"\nDone. Output: {output_dir}")
    if copied:
        print(f"Copied {len(copied)} file(s) to {len(cfg['target_projects'])} project(s):")
        for t in cfg["target_projects"]:
            print(f"  - {t / 'reels'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
