# CoversGen.md — Complete Cover Generation Guide

## Overview

Generate KDP-ready cover files from source images for 3 formats:
1. **Kindle** — eBook cover image
2. **Paperback** — PDF cover (back + spine + front)
3. **Hardcover** — PDF cover (with flaps)

---

## Prerequisites

### Install Dependencies

```bash
pip install Pillow fpdf2 scikit-image scipy numpy
```

### Source Images

You need:
- A **Kindle cover image** (front only, 1600×2560px recommended)
- A **full paperback cover image** (back + spine + front combined, flat or 3D mockup)

For splitting a combined cover image into 3 sections, see **[EdgeDetection.md](./EdgeDetection.md)**.

---

## 1. Kindle Cover

### KDP Requirements

| Spec | Value |
|---|---|
| Dimensions | 1600×2560px (minimum) |
| Aspect ratio | 1:1.6 |
| Resolution | 300 DPI recommended |
| Format | JPEG or PNG |
| Color mode | RGB |
| File size | < 50MB |

### Script

```python
from PIL import Image

def create_kindle_cover(input_path, output_path, target_w=1600, target_h=2560):
    """Resize/crop a cover image to Kindle specifications."""
    img = Image.open(input_path).convert("RGB")
    
    # Resize to fit within target dimensions while maintaining aspect ratio
    img.thumbnail((target_w, target_h), Image.LANCZOS)
    
    # Create canvas and center the image
    canvas = Image.new("RGB", (target_w, target_h), (0, 0, 0))
    x = (target_w - img.width) // 2
    y = (target_h - img.height) // 2
    canvas.paste(img, (x, y))
    canvas.save(output_path, quality=95)
    print(f"Kindle cover saved: {output_path} ({target_w}x{target_h})")

# Usage
create_kindle_cover("source_cover.jpg", "kindle_cover.jpg")
```

### Notes

- If the source is already a front-only cover, just resize to 1600×2560
- If the source is a full wraparound cover, extract the front section first (see EdgeDetection.md)
- Use JPEG for smaller file size, PNG for lossless quality

---

## 2. Paperback Cover PDF

### KDP Requirements

| Spec | Value |
|---|---|
| Trim size | 5.5" × 8.5" (or 6" × 9") |
| Bleed | 0.125" on all sides |
| Spine width | Depends on page count (see formula below) |
| Cover dimensions | (2 × trim_width + spine + 2 × bleed) × (trim_height + 2 × bleed) |
| Resolution | 300 DPI minimum |
| Format | PDF |
| Color mode | RGB |

### Spine Width Calculation

```
spine_width = 0.002252 × page_count + 0.001872  (inches, white paper)
```

| Page Count | Spine Width |
|---|---|
| 100 | 0.227" |
| 150 | 0.340" |
| 190 | 0.430" |
| 200 | 0.452" |
| 250 | 0.565" |
| 300 | 0.678" |

### Cover Dimensions Formula

```
cover_width = 2 × trim_width + spine_width + 2 × bleed
cover_height = trim_height + 2 × bleed
```

For 5.5" × 8.5" with 190 pages:
- Cover: 11.680" × 8.750" (3504 × 2625px at 300 DPI)

### Script

```python
from PIL import Image
from fpdf import FPDF
import os

DPI = 300

def inches_to_px(inches):
    return int(inches * DPI)

def create_paperback_cover(back_path, spine_path, front_path, output_path,
                           page_count=190, trim_w=5.5, trim_h=8.5, bleed=0.125):
    """Generate KDP paperback cover PDF from 3 separate images."""
    
    spine_in = 0.002252 * page_count + 0.001872
    cover_w = 2 * trim_w + spine_in + 2 * bleed
    cover_h = trim_h + 2 * bleed
    
    back_w = trim_w + bleed
    front_w = trim_w + bleed
    
    sections = [
        (back_w, back_path),
        (spine_in, spine_path),
        (front_w, front_path),
    ]
    
    canvas = Image.new("RGB", (inches_to_px(cover_w), inches_to_px(cover_h)), (255, 255, 255))
    
    x_px = 0
    for w_in, img_path in sections:
        w_px = inches_to_px(w_in)
        img = Image.open(img_path).convert("RGB")
        resized = img.resize((w_px, inches_to_px(cover_h)), Image.LANCZOS)
        canvas.paste(resized, (x_px, 0))
        x_px += w_px
    
    pdf = FPDF(unit="in", format=(cover_w, cover_h))
    pdf.set_auto_page_break(False)
    pdf.add_page()
    pdf.image(canvas, x=0, y=0, w=cover_w, h=cover_h)
    pdf.output(output_path)
    print(f"Paperback cover: {output_path} ({cover_w:.3f}\" x {cover_h:.3f}\")")

# Usage
create_paperback_cover("back_cover.png", "spine_cover.png", "front_cover.png",
                       "paperback_cover.pdf", page_count=190)
```

### Notes

- Each section (back, spine, front) is **stretched** to fit its allocated area exactly — no gaps
- Source images should ideally be at 300 DPI at their target print size
- If source images are smaller, they will be upscaled (may appear blurry)
- The spine image will be very narrow — ensure text is readable when stretched

---

## 3. Hardcover Cover PDF

### KDP Requirements

| Spec | Value |
|---|---|
| Trim size | 5.5" × 8.5" (or 6" × 9") |
| Bleed | 0.125" on all sides |
| Spine width | Depends on page count (see formula below) |
| Template size | 14.115" × 10.417" (for 5.5" × 8.5" trim) |
| Resolution | 300 DPI minimum |
| Format | PDF |
| Color mode | RGB |

### Spine Width Calculation (Hardcover)

```
spine_width = 0.0025 × page_count + 0.059  (inches, includes board thickness)
```

### Template Layout

```
[Back Flap] [Back Cover + Bleed] [Spine] [Front Cover + Bleed] [Front Flap]
```

For 5.5" × 8.5" with 190 pages:
- Template: 14.115" × 10.417"
- Back flap: 1.166"
- Back cover: 5.625"
- Spine: 0.534"
- Front cover: 5.625"
- Front flap: 1.166"
- Content area: 8.750" height, centered (0.833" offset from top)

### Script

```python
from PIL import Image
from fpdf import FPDF
import os

DPI = 300

def inches_to_px(inches):
    return int(inches * DPI)

def create_hardcover_cover(back_path, spine_path, front_path, output_path,
                           page_count=190, trim_w=5.5, trim_h=8.5, bleed=0.125):
    """Generate KDP hardcover cover PDF from 3 separate images."""
    
    # KDP hardcover template dimensions (for 5.5" x 8.5" trim)
    cover_w = 14.115
    cover_h = 10.417
    
    spine_in = 0.0025 * page_count + 0.059
    
    back_cover_w = trim_w + bleed
    front_cover_w = trim_w + bleed
    
    # Calculate flap widths
    used = back_cover_w + spine_in + front_cover_w
    flap_total = cover_w - used
    back_flap_w = flap_total / 2
    front_flap_w = flap_total / 2
    
    # Content area (centered in template)
    content_h = trim_h + bleed * 2
    content_offset = (cover_h - content_h) / 2
    
    sections = [
        (back_flap_w, None),           # Back flap - blank
        (back_cover_w, back_path),     # Back cover
        (spine_in, spine_path),        # Spine
        (front_cover_w, front_path),   # Front cover
        (front_flap_w, None),          # Front flap - blank
    ]
    
    canvas = Image.new("RGB", (inches_to_px(cover_w), inches_to_px(cover_h)), (255, 255, 255))
    
    x_px = 0
    for w_in, img_path in sections:
        w_px = inches_to_px(w_in)
        if img_path and os.path.exists(img_path):
            img = Image.open(img_path).convert("RGB")
            resized = img.resize((w_px, inches_to_px(content_h)), Image.LANCZOS)
            y_offset = inches_to_px(content_offset)
        else:
            resized = Image.new("RGB", (w_px, inches_to_px(content_h)), (255, 255, 255))
            y_offset = inches_to_px(content_offset)
        canvas.paste(resized, (x_px, y_offset))
        x_px += w_px
    
    pdf = FPDF(unit="in", format=(cover_w, cover_h))
    pdf.set_auto_page_break(False)
    pdf.add_page()
    pdf.image(canvas, x=0, y=0, w=cover_w, h=cover_h)
    pdf.output(output_path)
    print(f"Hardcover cover: {output_path} ({cover_w:.3f}\" x {cover_h:.3f}\")")

# Usage
create_hardcover_cover("back_cover.png", "spine_cover.png", "front_cover.png",
                       "hardcover_cover.pdf", page_count=190)
```

### Notes

- The template height (10.417") includes extra material for the case wrap (inside flaps on top/bottom)
- Content is **centered** vertically in the template with 0.833" offset from top
- Flaps (left/right) are filled with white — KDP will print them as the inside of the case
- Spine width includes board thickness (~0.059" extra vs paperback)

---

## Complete Workflow

### Step 1: Split Combined Cover Image

If you have a single image containing back + spine + front, split it first:

→ See **[EdgeDetection.md](./EdgeDetection.md)** for the Canny edge detection method.

### Step 2: Generate Covers

```python
# After splitting into back_cover.png, spine_cover.png, front_cover.png

# Kindle (front only, resized)
create_kindle_cover("front_cover.png", "kindle_cover.jpg")

# Paperback PDF
create_paperback_cover("back_cover.png", "spine_cover.png", "front_cover.png",
                       "paperback_cover.pdf", page_count=190)

# Hardcover PDF
create_hardcover_cover("back_cover.png", "spine_cover.png", "front_cover.png",
                       "hardcover_cover.pdf", page_count=190)
```

---

## KDP Cover Size Reference

### Paperback (5.5" × 8.5")

| Pages | Spine | Cover W × H |
|---|---|---|
| 100 | 0.227" | 11.204" × 8.750" |
| 150 | 0.340" | 11.430" × 8.750" |
| 190 | 0.430" | 11.680" × 8.750" |
| 200 | 0.452" | 11.654" × 8.750" |
| 250 | 0.565" | 11.880" × 8.750" |
| 300 | 0.678" | 12.106" × 8.750" |

### Hardcover (5.5" × 8.5")

| Pages | Spine | Cover W × H |
|---|---|---|
| 100 | 0.309" | 14.115" × 10.417" |
| 150 | 0.434" | 14.115" × 10.417" |
| 190 | 0.534" | 14.115" × 10.417" |
| 200 | 0.559" | 14.115" × 10.417" |
| 250 | 0.684" | 14.115" × 10.417" |
| 300 | 0.809" | 14.115" × 10.417" |

> Note: Hardcover template dimensions are fixed by KDP regardless of page count. Only the spine width changes.

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| Cover too tall/short vertically | Content not centered in template | Use `content_offset` for hardcover |
| Gaps between sections | Rounding errors in pixel calculations | Use `inches_to_px()` consistently |
| Blurry print | Source images too low resolution | Use 300 DPI source at target print size |
| KDP rejects file | Wrong dimensions | Verify with KDP's cover calculator |
| Spine text unreadable | Spine too narrow | Use larger font or simplify spine design |
| Content cut at edges | Content in bleed area | Keep important content 0.25" inside trim |

---

## File Naming Convention

```
{kindle_cover.jpg
paperback_cover.pdf
hardcover_cover.pdf
back_cover.png
spine_cover.png
front_cover.png
```
