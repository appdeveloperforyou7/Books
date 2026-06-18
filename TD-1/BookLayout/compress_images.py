"""
Image Compression Pipeline for The Glitch Squad Book 1.

Converts PNGs to optimized JPEGs (where no transparency) and resizes
to print resolution (300 DPI for 5.5" x 8.25" trim).

Usage:
    python compress_images.py              # compress all
    python compress_images.py --dry-run    # preview only
"""
import argparse
import json
from pathlib import Path
from PIL import Image

PROJECT_DIR = Path(__file__).resolve().parent.parent
SERIES_DIR = PROJECT_DIR
IMAGES_DIR = SERIES_DIR / "Images"

MAX_FULL_WIDTH = 1650   # 5.5in @ 300dpi
MAX_FULL_HEIGHT = 2475  # 8.25in @ 300dpi
MAX_HALF_WIDTH = 900
MAX_HALF_HEIGHT = 1200
MAX_SPOT = 400
JPEG_QUALITY = 85


def has_alpha(img):
    return img.mode in ('RGBA', 'LA', 'PA')


def get_target_size(item_type, size_val):
    if item_type == "full-page":
        return MAX_FULL_WIDTH, MAX_FULL_HEIGHT
    elif item_type == "half-page":
        return MAX_HALF_WIDTH, MAX_HALF_HEIGHT
    elif item_type in ("spot", "marginalia"):
        return MAX_SPOT, MAX_SPOT
    elif item_type == "strip":
        return MAX_FULL_WIDTH, MAX_HALF_HEIGHT
    else:
        return MAX_HALF_WIDTH, MAX_HALF_HEIGHT


def collect_all_images(manifest):
    arrays = [
        "illustrations", "strips", "blip_marginalia_images", "chapter_vignettes",
        "character_cards", "maps", "gadget_blueprints", "title_page",
        "section_dividers", "glitch_art", "extra_spots", "documents", "endpapers",
    ]
    items = []
    for key in arrays:
        for item in manifest.get(key, []):
            items.append(item)
    return items


def compress_single(src_path, dst_path, max_w, max_h, force_jpeg=False):
    img = Image.open(src_path)

    if has_alpha(img) and not force_jpeg:
        if img.mode == 'RGBA':
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        elif img.mode in ('LA', 'PA'):
            img = img.convert('RGBA')
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        else:
            img = img.convert('RGB')

    if img.mode != 'RGB':
        img = img.convert('RGB')

    w, h = img.size
    if w > max_w or h > max_h:
        ratio = min(max_w / w, max_h / h)
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
    return dst_path.stat().st_size


def main():
    parser = argparse.ArgumentParser(description="Compress images for print PDF")
    parser.add_argument("--book", type=int, default=1, help="Book number (default: 1)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    book_dir = SERIES_DIR / f"Book{args.book}"
    output_dir = book_dir / "Output"
    compressed_dir = output_dir / "images"
    compressed_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = None
    for candidate in ["manifest_clean.json", "manifest.json"]:
        p = book_dir / candidate
        if p.exists():
            manifest_path = p
            break

    if not manifest_path:
        print(f"ERROR: No manifest found in {book_dir}")
        return

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    items = collect_all_images(manifest)
    compressed_dir.mkdir(parents=True, exist_ok=True)

    total_original = 0
    total_compressed = 0
    count = 0

    for item in items:
        file_ref = item.get('file', '')
        src = None
        for candidate in [IMAGES_DIR / file_ref] + list(IMAGES_DIR.glob('**/' + file_ref)):
            if candidate.exists():
                src = candidate
                break

        if not src:
            print(f'  MISSING: {file_ref}')
            continue

        item_type = item.get('type', '')
        max_w, max_h = get_target_size(item_type, item.get('size', 1024))

        rel = src.relative_to(IMAGES_DIR)
        dst = compressed_dir / rel.with_suffix('.jpg')

        orig_size = src.stat().st_size
        total_original += orig_size

        if args.dry_run:
            print(f'  {src.name} -> {dst.name} ({orig_size/1024:.0f} KB, max {max_w}x{max_h})')
        else:
            comp_size = compress_single(src, dst, max_w, max_h)
            total_compressed += comp_size
            count += 1
            if count % 20 == 0:
                print(f'  Processed {count} images...')

    if not args.dry_run:
        print(f'\nCompressed {count} images')
        print(f'  Original: {total_original/1024/1024:.1f} MB')
        print(f'  Compressed: {total_compressed/1024/1024:.1f} MB')
        print(f'  Savings: {(1 - total_compressed/total_original)*100:.1f}%')
        print(f'  Output: {compressed_dir}')


if __name__ == "__main__":
    main()
