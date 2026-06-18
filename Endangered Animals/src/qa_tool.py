#!/usr/bin/env python3
"""
Comprehensive QA Tool for Endangered Animals Book
==================================================
Audits all data, images, templates, and rendered audit pages.
Generates a detailed HTML report with findings.

Usage:
    python src/qa_tool.py
    python src/qa_tool.py --output reports/qa_report.html
    python src/qa_tool.py --verbose
"""

import json
import os
import sys
import hashlib
import argparse
import datetime
from pathlib import Path
from collections import defaultdict

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("WARNING: Pillow not installed. Image analysis will be skipped.")
    print("Install with: pip install Pillow")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "animals_data_verified.json"
IMAGES_DIR = PROJECT_ROOT / "images"
CROPPED_DIR = IMAGES_DIR / "cropped"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
AUDIT_DIR = PROJECT_ROOT / "temp_audit"
OUTPUT_DIR = PROJECT_ROOT / "Output"
REPORT_DIR = PROJECT_ROOT / "reports"

EXPECTED_PAGE_COUNT = 82
MIN_IMAGE_WIDTH = 2400  # Minimum acceptable image width in pixels
VALID_IUCN_STATUSES = {
    "Critically Endangered", "Endangered", "Vulnerable",
    "Near Threatened", "Least Concern", "Data Deficient"
}
VALID_BOX_POSITIONS = {
    "pos-top-left", "pos-top-right", "pos-top-center",
    "pos-bottom-left", "pos-bottom-right", "pos-bottom-center",
    "pos-middle-left", "pos-middle-right",
}
REQUIRED_FIELDS = ["name", "iucn_status", "est_population", "primary_threat",
                   "where_found", "image_url", "BOX_POSITION"]
OPTIONAL_FIELDS = ["focal_x", "focal_y", "is_spread"]

TEMPLATE_FILES = {
    "cover_page.html": ["{{COVER_BG_IMAGE}}"],
    "sample_page.html": [
        "{{IMAGE_URL}}", "{{ANIMAL_NAME}}", "{{IUCN_STATUS}}",
        "{{EST_POPULATION}}", "{{PRIMARY_THREAT}}", "{{WHERE_FOUND}}",
        "{{BOX_POSITION}}", "{{FOCAL_X}}", "{{FOCAL_Y}}"
    ],
    "toc_page.html": ["{{TOC_ITEMS}}"],
    "divider_page.html": ["{{QUOTE_TEXT}}", "{{QUOTE_AUTHOR}}"],
    "copyright_page.html": [],
    "back_cover.html": ["{{BACK_BG_IMAGE}}"],
}

PAGE_DIMENSIONS_INCHES = (8.625, 11.25)  # Expected page size


# ---------------------------------------------------------------------------
# Utility Helpers
# ---------------------------------------------------------------------------
def status_icon(ok: bool) -> str:
    return '<span class="pass">PASS</span>' if ok else '<span class="fail">FAIL</span>'


def warn_icon() -> str:
    return '<span class="warn">WARN</span>'


def severity_class(level: str) -> str:
    return {"critical": "fail", "warning": "warn", "info": "info"}.get(level, "info")


def file_hash(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# QA Checks
# ---------------------------------------------------------------------------

class QAResult:
    """Container for a single check result."""
    def __init__(self, category: str, check_name: str, status: str,
                 message: str, details: list = None, severity: str = "info"):
        self.category = category
        self.check_name = check_name
        self.status = status  # "pass", "fail", "warn"
        self.message = message
        self.details = details or []
        self.severity = severity


def check_json_data() -> list:
    """Validate the animals_data_verified.json file."""
    results = []

    # 1. File exists and is valid JSON
    if not DATA_FILE.exists():
        results.append(QAResult("Data", "JSON File", "fail",
                                "Data file not found", severity="critical"))
        return results

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            animals = json.load(f)
    except json.JSONDecodeError as e:
        results.append(QAResult("Data", "JSON Parse", "fail",
                                f"Invalid JSON: {e}", severity="critical"))
        return results

    results.append(QAResult("Data", "JSON Parse", "pass",
                            f"Valid JSON with {len(animals)} animal entries"))

    # 2. Required fields check
    missing_fields = []
    for i, animal in enumerate(animals):
        for field in REQUIRED_FIELDS:
            if field not in animal or not animal.get(field, "").strip():
                missing_fields.append((i, animal.get("name", f"Entry #{i}"), field))

    if missing_fields:
        details = [f"#{idx} ({name}): missing '{field}'" for idx, name, field in missing_fields]
        results.append(QAResult("Data", "Required Fields", "fail",
                                f"{len(missing_fields)} missing/empty required fields",
                                details, severity="critical"))
    else:
        results.append(QAResult("Data", "Required Fields", "pass",
                                f"All {len(animals)} entries have required fields"))

    # 3. Duplicate names
    names = [a["name"] for a in animals]
    dupes = [n for n in names if names.count(n) > 1]
    if dupes:
        results.append(QAResult("Data", "Duplicate Names", "fail",
                                f"Duplicate animal names: {set(dupes)}",
                                list(set(dupes)), severity="critical"))
    else:
        results.append(QAResult("Data", "Duplicate Names", "pass",
                                "No duplicate animal names"))

    # 4. IUCN status validity
    invalid_status = [(a["name"], a["iucn_status"]) for a in animals
                      if a.get("iucn_status") not in VALID_IUCN_STATUSES]
    if invalid_status:
        details = [f"{name}: '{status}'" for name, status in invalid_status]
        results.append(QAResult("Data", "IUCN Status", "warn",
                                f"{len(invalid_status)} non-standard IUCN statuses",
                                details, severity="warning"))
    else:
        results.append(QAResult("Data", "IUCN Status", "pass",
                                "All IUCN statuses are valid"))

    # 5. BOX_POSITION validity
    invalid_pos = [(a["name"], a["BOX_POSITION"]) for a in animals
                   if a.get("BOX_POSITION") not in VALID_BOX_POSITIONS]
    if invalid_pos:
        details = [f"{name}: '{pos}'" for name, pos in invalid_pos]
        results.append(QAResult("Data", "Box Position", "fail",
                                f"{len(invalid_pos)} invalid box positions",
                                details, severity="critical"))
    else:
        results.append(QAResult("Data", "Box Position", "pass",
                                "All box positions are valid"))

    # 6. Optional fields validation
    invalid_focal = []
    for a in animals:
        if "focal_x" in a and a["focal_x"] not in ("left", "center", "right"):
            invalid_focal.append((a["name"], "focal_x", a["focal_x"]))
        if "focal_y" in a and a["focal_y"] not in ("top", "center", "bottom"):
            invalid_focal.append((a["name"], "focal_y", a["focal_y"]))
    if invalid_focal:
        details = [f"{name}: {field}='{val}'" for name, field, val in invalid_focal]
        results.append(QAResult("Data", "Focal Point Values", "warn",
                                f"{len(invalid_focal)} invalid focal values",
                                details, severity="warning"))
    else:
        results.append(QAResult("Data", "Focal Point Values", "pass",
                                "All focal point values are valid"))

    # 7. Image reference integrity
    referenced_images = set()
    missing_images = []
    for a in animals:
        img_path = PROJECT_ROOT / a.get("image_url", "")
        referenced_images.add(img_path.name)
        if not img_path.exists():
            missing_images.append((a["name"], str(img_path)))

    if missing_images:
        details = [f"{name}: {path}" for name, path in missing_images]
        results.append(QAResult("Data", "Image References", "fail",
                                f"{len(missing_images)} referenced images not found",
                                details, severity="critical"))
    else:
        results.append(QAResult("Data", "Image References", "pass",
                                f"All {len(referenced_images)} referenced images exist"))

    # 8. Orphan images (in images/ but not referenced)
    all_jpgs = {f.name for f in IMAGES_DIR.glob("*.jpg")}
    all_pngs = {f.name for f in IMAGES_DIR.glob("*.png")}
    all_images = all_jpgs | all_pngs
    orphans = all_images - referenced_images - {"forest_cover_bg.png"}
    if orphans:
        results.append(QAResult("Data", "Orphan Images", "warn",
                                f"{len(orphans)} unreferenced images in images/",
                                sorted(orphans), severity="warning"))
    else:
        results.append(QAResult("Data", "Orphan Images", "pass",
                                "No orphan images"))

    # 9. Spread pages count
    spreads = [a["name"] for a in animals if a.get("is_spread")]
    results.append(QAResult("Data", "Spread Pages", "pass" if spreads else "warn",
                            f"{len(spreads)} spread (2-page) animals",
                            spreads, severity="info"))

    # 10. Status distribution
    status_dist = defaultdict(int)
    for a in animals:
        status_dist[a.get("iucn_status", "Unknown")] += 1
    dist_details = [f"{s}: {c}" for s, c in sorted(status_dist.items(), key=lambda x: -x[1])]
    results.append(QAResult("Data", "Status Distribution", "pass",
                            "IUCN status distribution",
                            dist_details, severity="info"))

    # 11. Data consistency - trailing comma / JSON syntax (already covered by parse)
    # Check for potential typos in names (very short or very long)
    short_names = [a["name"] for a in animals if len(a["name"]) < 5]
    long_names = [a["name"] for a in animals if len(a["name"]) > 50]
    if short_names:
        results.append(QAResult("Data", "Short Names", "warn",
                                f"{len(short_names)} unusually short names",
                                short_names, severity="warning"))
    if long_names:
        results.append(QAResult("Data", "Long Names", "warn",
                                f"{len(long_names)} unusually long names",
                                long_names, severity="warning"))

    # 12. Empty population values
    empty_pop = [a["name"] for a in animals
                 if not a.get("est_population") or a["est_population"].strip().lower() in ("", "unknown", "n/a")]
    if empty_pop:
        results.append(QAResult("Data", "Population Data", "warn",
                                f"{len(empty_pop)} entries with unknown/empty population",
                                empty_pop, severity="warning"))
    else:
        results.append(QAResult("Data", "Population Data", "pass",
                                "All entries have population data"))

    return results


def check_images() -> list:
    """Validate image files: existence, dimensions, format, file sizes."""
    results = []

    if not HAS_PILLOW:
        results.append(QAResult("Images", "Pillow", "fail",
                                "Pillow not installed, skipping image checks",
                                severity="critical"))
        return results

    # Load data for image references
    if not DATA_FILE.exists():
        results.append(QAResult("Images", "Data File", "fail",
                                "Cannot check images without data file",
                                severity="critical"))
        return results

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            animals = json.load(f)
    except json.JSONDecodeError as e:
        results.append(QAResult("Images", "Data File", "fail",
                                f"Cannot parse data file: {e}",
                                severity="critical"))
        return results

    # 1. Image dimensions check
    below_min = []
    dimension_ok = 0
    image_details = []
    for a in animals:
        img_path = PROJECT_ROOT / a["image_url"]
        if not img_path.exists():
            continue
        try:
            with Image.open(img_path) as img:
                w, h = img.size
                image_details.append({
                    "name": a["name"],
                    "file": img_path.name,
                    "width": w,
                    "height": h,
                    "format": img.format,
                    "mode": img.mode,
                    "size_mb": round(img_path.stat().st_size / (1024 * 1024), 2),
                })
                if w < MIN_IMAGE_WIDTH:
                    below_min.append((a["name"], w, h))
                else:
                    dimension_ok += 1
        except Exception as e:
            results.append(QAResult("Images", f"Read Error ({a['name']})", "fail",
                                    f"Cannot read image: {e}", severity="critical"))

    if below_min:
        details = [f"{name}: {w}x{h} (below {MIN_IMAGE_WIDTH}px min)" for name, w, h in below_min]
        results.append(QAResult("Images", "Resolution", "warn",
                                f"{len(below_min)} images below {MIN_IMAGE_WIDTH}px width",
                                details, severity="warning"))
    else:
        results.append(QAResult("Images", "Resolution", "pass",
                                f"All {dimension_ok} images >= {MIN_IMAGE_WIDTH}px wide"))

    # 2. Format consistency
    formats = defaultdict(list)
    for d in image_details:
        formats[d["format"]].append(d["file"])
    format_details = [f"{fmt}: {len(files)} files" for fmt, files in sorted(formats.items())]
    results.append(QAResult("Images", "Format", "pass",
                            "Image format distribution",
                            format_details, severity="info"))

    # 3. Color mode check
    modes = defaultdict(list)
    for d in image_details:
        modes[d["mode"]].append(d["file"])
    non_rgb = [f for mode in modes if mode not in ("RGB", "RGBA", "L")
               for f in modes[mode]]
    if non_rgb:
        results.append(QAResult("Images", "Color Mode", "warn",
                                f"{len(non_rgb)} unusual color modes",
                                non_rgb[:10], severity="warning"))
    else:
        mode_details = [f"{mode}: {len(files)} files" for mode, files in sorted(modes.items())]
        results.append(QAResult("Images", "Color Mode", "pass",
                                "All standard color modes",
                                mode_details, severity="info"))

    # 4. File size check
    total_size = sum(d["size_mb"] for d in image_details)
    tiny_files = [f"{d['name']} ({d['size_mb']} MB)" for d in image_details if d["size_mb"] < 0.1]
    huge_files = [f"{d['name']} ({d['size_mb']} MB)" for d in image_details if d["size_mb"] > 20]

    results.append(QAResult("Images", "Total Size", "pass",
                            f"Total image assets: {total_size:.1f} MB across {len(image_details)} files",
                            severity="info"))

    if tiny_files:
        results.append(QAResult("Images", "Tiny Files", "warn",
                                f"{len(tiny_files)} images under 100KB (may be low quality)",
                                tiny_files, severity="warning"))
    if huge_files:
        results.append(QAResult("Images", "Huge Files", "warn",
                                f"{len(huge_files)} images over 20MB",
                                huge_files, severity="warning"))

    # 5. Cropped images directory
    if CROPPED_DIR.exists():
        cropped_count = len(list(CROPPED_DIR.glob("*.jpg"))) + len(list(CROPPED_DIR.glob("*.png")))
        results.append(QAResult("Images", "Cropped Dir", "pass",
                                f"Cropped images directory: {cropped_count} files",
                                severity="info"))
    else:
        results.append(QAResult("Images", "Cropped Dir", "warn",
                                "No cropped/ directory found",
                                severity="warning"))

    # 6. Aspect ratio analysis
    aspect_ratios = []
    for d in image_details:
        if d["height"] > 0:
            ratio = d["width"] / d["height"]
            aspect_ratios.append((d["name"], ratio))

    target_ratio = PAGE_DIMENSIONS_INCHES[0] / PAGE_DIMENSIONS_INCHES[1]  # ~0.767
    mismatched = [(name, f"{ratio:.3f}") for name, ratio in aspect_ratios
                  if abs(ratio - target_ratio) > 0.3]
    if mismatched:
        details = [f"{name}: ratio {r} (target ~{target_ratio:.3f})" for name, r in mismatched]
        results.append(QAResult("Images", "Aspect Ratio", "warn",
                                f"{len(mismatched)} images with significantly different aspect ratio from page",
                                details[:15], severity="warning"))
    else:
        results.append(QAResult("Images", "Aspect Ratio", "pass",
                                "All images have reasonable aspect ratios"))

    return results


def check_templates() -> list:
    """Validate all HTML templates exist and contain expected placeholders."""
    results = []

    # 1. All templates exist
    missing_templates = [t for t in TEMPLATE_FILES if not (TEMPLATES_DIR / t).exists()]
    if missing_templates:
        results.append(QAResult("Templates", "Files Exist", "fail",
                                f"Missing templates: {missing_templates}",
                                missing_templates, severity="critical"))
    else:
        results.append(QAResult("Templates", "Files Exist", "pass",
                                f"All {len(TEMPLATE_FILES)} templates found"))

    # 2. Placeholder presence in each template
    for tmpl_name, placeholders in TEMPLATE_FILES.items():
        tmpl_path = TEMPLATES_DIR / tmpl_name
        if not tmpl_path.exists():
            continue

        content = tmpl_path.read_text(encoding="utf-8")
        missing_ph = [ph for ph in placeholders if ph not in content]
        if missing_ph:
            results.append(QAResult("Templates", f"Placeholders ({tmpl_name})", "fail",
                                    f"Missing placeholders: {missing_ph}",
                                    missing_ph, severity="critical"))
        else:
            results.append(QAResult("Templates", f"Placeholders ({tmpl_name})", "pass",
                                    f"All {len(placeholders)} placeholders present"))

    # 3. HTML validity (basic checks)
    for tmpl_name in TEMPLATE_FILES:
        tmpl_path = TEMPLATES_DIR / tmpl_name
        if not tmpl_path.exists():
            continue
        content = tmpl_path.read_text(encoding="utf-8")
        issues = []
        if "<!DOCTYPE html>" not in content:
            issues.append("Missing DOCTYPE")
        if "</html>" not in content:
            issues.append("Missing closing </html>")
        if 'charset="UTF-8"' not in content and "charset=UTF-8" not in content:
            issues.append("Missing charset declaration")
        if issues:
            results.append(QAResult("Templates", f"HTML Validity ({tmpl_name})", "warn",
                                    f"Issues: {issues}", issues, severity="warning"))
        else:
            results.append(QAResult("Templates", f"HTML Validity ({tmpl_name})", "pass",
                                    "Basic HTML structure OK"))

    # 4. CSS consistency - page dimensions
    expected_width = "8.625in"
    expected_height = "11.25in"
    for tmpl_name in TEMPLATE_FILES:
        tmpl_path = TEMPLATES_DIR / tmpl_name
        if not tmpl_path.exists():
            continue
        content = tmpl_path.read_text(encoding="utf-8")
        has_dims = expected_width in content or expected_height in content
        if tmpl_name in ("sample_page.html", "cover_page.html", "divider_page.html", "back_cover.html"):
            if not has_dims:
                # Check for alternative dimension references
                if "8.5in" in content and tmpl_name != "toc_page.html" and tmpl_name != "copyright_page.html":
                    results.append(QAResult("Templates", f"Page Dims ({tmpl_name})", "warn",
                                            "Uses 8.5x11 instead of 8.625x11.25",
                                            severity="warning"))

    # 5. Font loading check
    for tmpl_name in TEMPLATE_FILES:
        tmpl_path = TEMPLATES_DIR / tmpl_name
        if not tmpl_path.exists():
            continue
        content = tmpl_path.read_text(encoding="utf-8")
        if "Playfair Display" not in content or "Montserrat" not in content:
            if tmpl_name not in ("copyright_page.html",):
                results.append(QAResult("Templates", f"Fonts ({tmpl_name})", "warn",
                                        "Missing expected font references",
                                        severity="warning"))

    # 6. Check sample_page.html for all box position classes
    sample_path = TEMPLATES_DIR / "sample_page.html"
    if sample_path.exists():
        content = sample_path.read_text(encoding="utf-8")
        missing_positions = [p for p in VALID_BOX_POSITIONS if f".{p}" not in content]
        if missing_positions:
            results.append(QAResult("Templates", "CSS Position Classes", "warn",
                                    f"Missing CSS classes: {missing_positions}",
                                    missing_positions, severity="warning"))
        else:
            results.append(QAResult("Templates", "CSS Position Classes", "pass",
                                    f"All {len(VALID_BOX_POSITIONS)} position classes defined"))

    return results


def check_audit_pages() -> list:
    """Analyze the rendered audit pages for issues."""
    results = []

    if not AUDIT_DIR.exists():
        results.append(QAResult("Audit Pages", "Directory", "fail",
                                "temp_audit/ directory not found",
                                severity="critical"))
        return results

    if not HAS_PILLOW:
        results.append(QAResult("Audit Pages", "Pillow", "fail",
                                "Pillow required for audit page analysis",
                                severity="critical"))
        return results

    # 1. Page count
    audit_images = sorted(AUDIT_DIR.glob("page_*.jpg"))
    page_count = len(audit_images)
    if page_count != EXPECTED_PAGE_COUNT:
        results.append(QAResult("Audit Pages", "Page Count", "fail",
                                f"Expected {EXPECTED_PAGE_COUNT}, found {page_count}",
                                severity="critical"))
    else:
        results.append(QAResult("Audit Pages", "Page Count", "pass",
                                f"All {EXPECTED_PAGE_COUNT} audit pages present"))

    # 2. Sequential completeness
    page_numbers = []
    for p in audit_images:
        try:
            num = int(p.stem.replace("page_", ""))
            page_numbers.append(num)
        except ValueError:
            pass

    expected_range = set(range(1, page_count + 1))
    actual_set = set(page_numbers)
    missing = sorted(expected_range - actual_set)
    extra = sorted(actual_set - expected_range)

    if missing:
        results.append(QAResult("Audit Pages", "Sequential", "fail",
                                f"Missing page numbers: {missing}",
                                [f"page_{n:02d}.jpg" for n in missing],
                                severity="critical"))
    else:
        results.append(QAResult("Audit Pages", "Sequential", "pass",
                                "No gaps in page numbering"))

    if extra:
        results.append(QAResult("Audit Pages", "Extra Pages", "warn",
                                f"Unexpected page numbers: {extra}",
                                severity="warning"))

    # 3. Dimension consistency
    dimensions = {}
    inconsistent = []
    for img_path in audit_images:
        try:
            with Image.open(img_path) as img:
                w, h = img.size
                dimensions[img_path.name] = (w, h)
        except Exception as e:
            results.append(QAResult("Audit Pages", f"Read Error ({img_path.name})", "fail",
                                    f"Cannot read: {e}", severity="critical"))

    if dimensions:
        unique_dims = set(dimensions.values())
        if len(unique_dims) > 1:
            dim_groups = defaultdict(list)
            for name, dim in dimensions.items():
                dim_groups[dim].append(name)
            details = [f"{dim}: {len(files)} pages" for dim, files in sorted(dim_groups.items())]
            results.append(QAResult("Audit Pages", "Dimensions", "warn",
                                    f"{len(unique_dims)} different page dimensions found",
                                    details, severity="warning"))
        else:
            dim = list(unique_dims)[0]
            results.append(QAResult("Audit Pages", "Dimensions", "pass",
                                    f"All pages uniform: {dim[0]}x{dim[1]}"))

    # 4. Blank/near-blank page detection
    blank_pages = []
    near_blank_pages = []
    very_dark_pages = []
    page_stats = []

    for img_path in audit_images:
        try:
            with Image.open(img_path) as img:
                # Convert to RGB for analysis
                rgb = img.convert("RGB")
                # Resize for fast analysis
                small = rgb.resize((100, 130), Image.Resampling.LANCZOS)
                pixels = list(small.getdata()) if not hasattr(small, 'get_flattened_data') else list(small.get_flattened_data())

                # Calculate average brightness
                avg_brightness = sum(sum(p) for p in pixels) / (len(pixels) * 3)
                # Calculate color variance
                r_vals = [p[0] for p in pixels]
                g_vals = [p[1] for p in pixels]
                b_vals = [p[2] for p in pixels]
                import statistics
                std_dev = statistics.stdev(r_vals + g_vals + b_vals)

                # Dominant color
                avg_r = sum(r_vals) / len(r_vals)
                avg_g = sum(g_vals) / len(g_vals)
                avg_b = sum(b_vals) / len(b_vals)

                page_stats.append({
                    "file": img_path.name,
                    "brightness": round(avg_brightness, 1),
                    "std_dev": round(std_dev, 1),
                    "avg_color": (round(avg_r), round(avg_g), round(avg_b)),
                })

                if avg_brightness > 240 and std_dev < 5:
                    blank_pages.append((img_path.name, avg_brightness, std_dev))
                elif avg_brightness > 230 and std_dev < 10:
                    near_blank_pages.append((img_path.name, avg_brightness, std_dev))
                elif avg_brightness < 15 and std_dev < 8:
                    very_dark_pages.append((img_path.name, avg_brightness, std_dev))

        except Exception:
            pass

    if blank_pages:
        details = [f"{name}: brightness={b:.0f}, stddev={s:.1f}" for name, b, s in blank_pages]
        results.append(QAResult("Audit Pages", "Blank Pages", "fail",
                                f"{len(blank_pages)} potentially blank pages detected",
                                details, severity="critical"))
    else:
        results.append(QAResult("Audit Pages", "Blank Pages", "pass",
                                "No blank pages detected"))

    if near_blank_pages:
        details = [f"{name}: brightness={b:.0f}, stddev={s:.1f}" for name, b, s in near_blank_pages]
        results.append(QAResult("Audit Pages", "Near-Blank Pages", "warn",
                                f"{len(near_blank_pages)} nearly blank pages",
                                details, severity="warning"))

    if very_dark_pages:
        details = [f"{name}: brightness={b:.0f}, stddev={s:.1f}" for name, b, s in very_dark_pages]
        results.append(QAResult("Audit Pages", "Very Dark Pages", "warn",
                                f"{len(very_dark_pages)} very dark pages (may be missing content)",
                                details, severity="warning"))

    # 5. File size consistency
    file_sizes = {}
    for img_path in audit_images:
        try:
            file_sizes[img_path.name] = img_path.stat().st_size
        except Exception:
            pass

    if file_sizes:
        sizes = list(file_sizes.values())
        avg_size = sum(sizes) / len(sizes)
        min_size = min(sizes)
        max_size = max(sizes)

        tiny_pages = [name for name, size in file_sizes.items() if size < avg_size * 0.1]
        if tiny_pages:
            results.append(QAResult("Audit Pages", "Tiny File Size", "warn",
                                    f"{len(tiny_pages)} pages with suspiciously small file size",
                                    tiny_pages, severity="warning"))

        size_details = [
            f"Average: {avg_size / 1024:.0f} KB",
            f"Min: {min_size / 1024:.0f} KB ({min(file_sizes, key=lambda k: file_sizes[k])})",
            f"Max: {max_size / 1024:.0f} KB ({max(file_sizes, key=lambda k: file_sizes[k])})",
            f"Total: {sum(sizes) / (1024 * 1024):.1f} MB",
        ]
        results.append(QAResult("Audit Pages", "File Size Stats", "pass",
                                "Audit page file size summary",
                                size_details, severity="info"))

    # 6. Content variety check (MD5 hash uniqueness)
    hashes = {}
    duplicates = []
    for img_path in audit_images:
        h = file_hash(img_path)
        if h in hashes:
            duplicates.append((img_path.name, hashes[h]))
        else:
            hashes[h] = img_path.name

    if duplicates:
        details = [f"{new} appears identical to {orig}" for new, orig in duplicates]
        results.append(QAResult("Audit Pages", "Duplicate Pages", "warn",
                                f"{len(duplicates)} potentially duplicate pages",
                                details, severity="warning"))
    else:
        results.append(QAResult("Audit Pages", "Duplicate Pages", "pass",
                                "All pages are unique"))

    return results, page_stats


def check_output_files() -> list:
    """Check output PDF files."""
    results = []

    if not OUTPUT_DIR.exists():
        results.append(QAResult("Output", "Directory", "fail",
                                "Output/ directory not found", severity="critical"))
        return results

    # 1. Main PDF
    main_pdf = OUTPUT_DIR / "Chronicles_of_the_Endangered.pdf"
    if main_pdf.exists():
        size_mb = main_pdf.stat().st_size / (1024 * 1024)
        results.append(QAResult("Output", "Main PDF", "pass",
                                f"Main PDF exists ({size_mb:.1f} MB)",
                                severity="info"))
    else:
        results.append(QAResult("Output", "Main PDF", "fail",
                                "Main PDF not found", severity="critical"))

    # 2. Archive
    archive_dir = OUTPUT_DIR / "Archive"
    if archive_dir.exists():
        archive_files = list(archive_dir.glob("*.pdf"))
        archive_details = [f"{f.name}: {f.stat().st_size / (1024*1024):.1f} MB"
                           for f in archive_files]
        results.append(QAResult("Output", "Archive", "pass",
                                f"{len(archive_files)} archived PDF(s)",
                                archive_details, severity="info"))
    else:
        results.append(QAResult("Output", "Archive", "warn",
                                "No Archive directory", severity="warning"))

    # 3. Check for other output files
    other_files = []
    for f in OUTPUT_DIR.rglob("*"):
        if f.is_file() and f.suffix not in (".pdf",):
            other_files.append(f"{f.relative_to(OUTPUT_DIR)} ({f.stat().st_size / 1024:.0f} KB)")

    if other_files:
        results.append(QAResult("Output", "Other Files", "warn",
                                "Non-PDF files in Output/",
                                other_files, severity="warning"))

    return results


def check_project_structure() -> list:
    """Validate overall project structure."""
    results = []

    expected_dirs = ["images", "Output", "src", "templates", "temp_audit"]
    for d in expected_dirs:
        dir_path = PROJECT_ROOT / d
        if dir_path.exists():
            file_count = sum(1 for _ in dir_path.rglob("*") if _.is_file())
            results.append(QAResult("Structure", d, "pass",
                                    f"Directory exists ({file_count} files)",
                                    severity="info"))
        else:
            results.append(QAResult("Structure", d, "fail",
                                    f"Directory missing", severity="critical"))

    # Check for stray root files (root should only contain directories)
    root_files = [f for f in PROJECT_ROOT.iterdir() if f.is_file()]
    ignore_files = {"nul"}  # Windows artifact
    stray = [f.name for f in root_files if f.name not in ignore_files]
    if stray:
        results.append(QAResult("Structure", "Root Cleanliness", "warn",
                                f"Files in root directory: {stray}",
                                stray, severity="warning"))
    else:
        results.append(QAResult("Structure", "Root Cleanliness", "pass",
                                "Root directory is clean (only directories)"))

    return results


# ---------------------------------------------------------------------------
# Report Generator
# ---------------------------------------------------------------------------

def generate_report(all_results: list, page_stats: list = None, verbose: bool = False) -> str:
    """Generate HTML report from QA results."""

    # Organize by category
    categories = defaultdict(list)
    for r in all_results:
        categories[r.category].append(r)

    # Count totals
    total = len(all_results)
    passed = sum(1 for r in all_results if r.status == "pass")
    failed = sum(1 for r in all_results if r.status == "fail")
    warned = sum(1 for r in all_results if r.status == "warn")

    # Overall health
    if failed > 0:
        overall_status = "FAIL"
        overall_class = "fail"
    elif warned > 0:
        overall_status = "PASS WITH WARNINGS"
        overall_class = "warn"
    else:
        overall_status = "ALL PASS"
        overall_class = "pass"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QA Report - Endangered Animals Book</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0f0f0f;
            color: #e0e0e0;
            line-height: 1.6;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{
            font-size: 2rem;
            color: #d4a843;
            text-align: center;
            margin-bottom: 5px;
            letter-spacing: -0.5px;
        }}
        .subtitle {{
            text-align: center;
            color: #888;
            font-size: 0.9rem;
            margin-bottom: 30px;
        }}
        .overall-status {{
            text-align: center;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: 3px;
        }}
        .overall-status.pass {{ background: rgba(46, 204, 113, 0.15); color: #2ecc71; border: 2px solid #2ecc71; }}
        .overall-status.fail {{ background: rgba(231, 76, 60, 0.15); color: #e74c3c; border: 2px solid #e74c3c; }}
        .overall-status.warn {{ background: rgba(241, 196, 15, 0.15); color: #f1c40f; border: 2px solid #f1c40f; }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: #1a1a1a;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid #333;
        }}
        .summary-card .number {{
            font-size: 2.5rem;
            font-weight: 700;
        }}
        .summary-card .label {{
            font-size: 0.85rem;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .summary-card.total .number {{ color: #d4a843; }}
        .summary-card.passed .number {{ color: #2ecc71; }}
        .summary-card.failed .number {{ color: #e74c3c; }}
        .summary-card.warnings .number {{ color: #f1c40f; }}

        .category {{
            background: #1a1a1a;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid #2a2a2a;
            overflow: hidden;
        }}
        .category-header {{
            padding: 15px 20px;
            background: #222;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }}
        .category-header:hover {{ background: #2a2a2a; }}
        .category-name {{
            font-size: 1.2rem;
            font-weight: 600;
            color: #d4a843;
        }}
        .category-stats {{
            display: flex;
            gap: 15px;
            font-size: 0.85rem;
        }}
        .category-body {{ padding: 15px 20px; }}

        .check-row {{
            display: flex;
            align-items: flex-start;
            padding: 12px 0;
            border-bottom: 1px solid #2a2a2a;
        }}
        .check-row:last-child {{ border-bottom: none; }}
        .check-status {{
            min-width: 60px;
            font-weight: 700;
            font-size: 0.75rem;
            letter-spacing: 1px;
            text-align: center;
            padding: 4px 8px;
            border-radius: 4px;
            margin-right: 15px;
        }}
        .pass {{ color: #2ecc71; background: rgba(46, 204, 113, 0.15); }}
        .fail {{ color: #e74c3c; background: rgba(231, 76, 60, 0.15); }}
        .warn {{ color: #f1c40f; background: rgba(241, 196, 15, 0.15); }}
        .info {{ color: #3498db; background: rgba(52, 152, 219, 0.15); }}

        .check-content {{ flex: 1; }}
        .check-name {{
            font-weight: 600;
            color: #e0e0e0;
            margin-bottom: 3px;
        }}
        .check-message {{ color: #aaa; font-size: 0.9rem; }}
        .check-details {{
            margin-top: 8px;
            background: #111;
            border-radius: 6px;
            padding: 10px 15px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.8rem;
            color: #888;
            max-height: 200px;
            overflow-y: auto;
        }}
        .check-details li {{
            list-style: none;
            padding: 2px 0;
        }}
        .check-details li::before {{
            content: "  ";
        }}

        /* Page analysis heatmap */
        .page-analysis {{
            background: #1a1a1a;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #2a2a2a;
        }}
        .page-analysis h3 {{
            color: #d4a843;
            margin-bottom: 15px;
            font-size: 1.1rem;
        }}
        .page-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
            gap: 4px;
        }}
        .page-cell {{
            text-align: center;
            padding: 6px 2px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 600;
        }}
        .page-cell .pg-num {{ display: block; color: #e0e0e0; }}
        .page-cell .pg-bright {{ display: block; font-size: 0.6rem; color: #888; }}

        .footer {{
            text-align: center;
            padding: 30px;
            color: #555;
            font-size: 0.8rem;
        }}

        @media (max-width: 768px) {{
            .summary-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>Chronicles of the Endangered</h1>
    <p class="subtitle">Comprehensive QA Audit Report</p>

    <div class="overall-status {overall_class}">
        {overall_status}
    </div>

    <div class="summary-grid">
        <div class="summary-card total">
            <div class="number">{total}</div>
            <div class="label">Total Checks</div>
        </div>
        <div class="summary-card passed">
            <div class="number">{passed}</div>
            <div class="label">Passed</div>
        </div>
        <div class="summary-card failed">
            <div class="number">{failed}</div>
            <div class="label">Failed</div>
        </div>
        <div class="summary-card warnings">
            <div class="number">{warned}</div>
            <div class="label">Warnings</div>
        </div>
    </div>
"""

    # Category sections
    for cat_name, checks in categories.items():
        cat_pass = sum(1 for c in checks if c.status == "pass")
        cat_fail = sum(1 for c in checks if c.status == "fail")
        cat_warn = sum(1 for c in checks if c.status == "warn")

        html += f"""
    <div class="category">
        <div class="category-header" onclick="this.parentElement.querySelector('.category-body').classList.toggle('collapsed')">
            <span class="category-name">{cat_name}</span>
            <div class="category-stats">
                <span class="pass">{cat_pass} pass</span>
                <span class="fail">{cat_fail} fail</span>
                <span class="warn">{cat_warn} warn</span>
            </div>
        </div>
        <div class="category-body">
"""
        for check in checks:
            html += f"""
            <div class="check-row">
                <span class="check-status {check.status}">{check.status.upper()}</span>
                <div class="check-content">
                    <div class="check-name">{check.check_name}</div>
                    <div class="check-message">{check.message}</div>
"""
            if check.details and verbose:
                html += """
                    <div class="check-details">
"""
                for detail in check.details:
                    html += f"                        <li>{detail}</li>\n"
                html += """                    </div>
"""
            elif check.details and not verbose:
                # Show count only for non-verbose mode
                if len(check.details) > 3:
                    html += f"""
                    <div class="check-message" style="font-size:0.8rem; color:#666;">
                        {len(check.details)} details (use --verbose to expand)
                    </div>
"""

            html += """                </div>
            </div>
"""

        html += """        </div>
    </div>
"""

    # Page analysis heatmap
    if page_stats:
        html += """
    <div class="page-analysis">
        <h3>Page Brightness Heatmap</h3>
        <p style="color:#888; font-size:0.8rem; margin-bottom:10px;">
            Visual overview of page content. Bright pages may be blank; dark pages are photo-heavy.
        </p>
        <div class="page-grid">
"""
        for ps in page_stats:
            brightness = ps["brightness"]
            # Map brightness to background color
            if brightness < 30:
                bg_color = "#111"
                text_color = "#555"
            elif brightness < 80:
                bg_color = "#1a1a1a"
                text_color = "#888"
            elif brightness < 140:
                bg_color = "#333"
                text_color = "#ccc"
            elif brightness < 200:
                bg_color = "#666"
                text_color = "#fff"
            else:
                bg_color = "#999"
                text_color = "#fff"

            page_num = ps["file"].replace("page_", "").replace(".jpg", "")
            html += f"""            <div class="page-cell" style="background:{bg_color}; color:{text_color};">
                <span class="pg-num">{page_num}</span>
                <span class="pg-bright">{brightness:.0f}</span>
            </div>
"""

        html += """        </div>
    </div>
"""

    # Critical issues summary
    critical_issues = [r for r in all_results if r.status == "fail"]
    if critical_issues:
        html += """
    <div class="category" style="border-color: #e74c3c;">
        <div class="category-header" style="background: rgba(231, 76, 60, 0.1);">
            <span class="category-name" style="color: #e74c3c;">Critical Issues Summary</span>
            <div class="category-stats"><span class="fail">{count} issues</span></div>
        </div>
        <div class="category-body">
""".format(count=len(critical_issues))

        for issue in critical_issues:
            html += f"""
            <div class="check-row">
                <span class="check-status fail">FAIL</span>
                <div class="check-content">
                    <div class="check-name">[{issue.category}] {issue.check_name}</div>
                    <div class="check-message">{issue.message}</div>
                </div>
            </div>
"""

        html += """        </div>
    </div>
"""

    html += f"""
    <div class="footer">
        Generated by QA Tool &mdash; {timestamp}<br>
        Project: {PROJECT_ROOT}
    </div>
</div>

<script>
// Toggle category collapse
document.querySelectorAll('.category-body').forEach(el => {{
    // Expand categories with failures by default
}});
</script>
</body>
</html>
"""

    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive QA Tool for Endangered Animals Book"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output path for HTML report (default: reports/qa_report_YYYYMMDD_HHMMSS.html)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all details in report (expanded lists)"
    )
    parser.add_argument(
        "--no-image-analysis",
        action="store_true",
        help="Skip pixel-level audit page analysis (faster)"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  CHRONICLES OF THE ENDANGERED - QA AUDIT TOOL")
    print("=" * 60)
    print(f"  Project: {PROJECT_ROOT}")
    print(f"  Time:    {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    all_results = []
    page_stats = []

    # --- Data Checks ---
    print("[1/6] Checking JSON data integrity...")
    data_results = check_json_data()
    all_results.extend(data_results)
    for r in data_results:
        sym = "+" if r.status == "pass" else "!" if r.status == "fail" else "~"
        print(f"       [{sym}] {r.check_name}: {r.message}")

    # --- Image Checks ---
    print("\n[2/6] Checking image assets...")
    image_results = check_images()
    all_results.extend(image_results)
    for r in image_results:
        sym = "+" if r.status == "pass" else "!" if r.status == "fail" else "~"
        print(f"       [{sym}] {r.check_name}: {r.message}")

    # --- Template Checks ---
    print("\n[3/6] Checking HTML templates...")
    template_results = check_templates()
    all_results.extend(template_results)
    for r in template_results:
        sym = "+" if r.status == "pass" else "!" if r.status == "fail" else "~"
        print(f"       [{sym}] {r.check_name}: {r.message}")

    # --- Audit Page Checks ---
    print("\n[4/6] Analyzing audit pages...")
    if args.no_image_analysis:
        print("       (Skipped by --no-image-analysis)")
    else:
        audit_result = check_audit_pages()
        if isinstance(audit_result, tuple):
            audit_results, page_stats = audit_result
        else:
            audit_results = audit_result
        all_results.extend(audit_results)
        for r in audit_results:
            sym = "+" if r.status == "pass" else "!" if r.status == "fail" else "~"
            print(f"       [{sym}] {r.check_name}: {r.message}")

    # --- Output Checks ---
    print("\n[5/6] Checking output files...")
    output_results = check_output_files()
    all_results.extend(output_results)
    for r in output_results:
        sym = "+" if r.status == "pass" else "!" if r.status == "fail" else "~"
        print(f"       [{sym}] {r.check_name}: {r.message}")

    # --- Structure Checks ---
    print("\n[6/6] Checking project structure...")
    structure_results = check_project_structure()
    all_results.extend(structure_results)
    for r in structure_results:
        sym = "+" if r.status == "pass" else "!" if r.status == "fail" else "~"
        print(f"       [{sym}] {r.check_name}: {r.message}")

    # --- Summary ---
    total = len(all_results)
    passed = sum(1 for r in all_results if r.status == "pass")
    failed = sum(1 for r in all_results if r.status == "fail")
    warned = sum(1 for r in all_results if r.status == "warn")

    print("\n" + "=" * 60)
    print(f"  RESULTS: {passed} passed, {failed} failed, {warned} warnings ({total} total)")
    if failed > 0:
        print("  STATUS:  *** ISSUES FOUND ***")
    elif warned > 0:
        print("  STATUS:  PASSED WITH WARNINGS")
    else:
        print("  STATUS:  ALL CLEAR")
    print("=" * 60)

    # --- Generate Report ---
    print("\nGenerating HTML report...")
    report_html = generate_report(all_results, page_stats, verbose=args.verbose)

    # Determine output path
    if args.output:
        report_path = Path(args.output)
    else:
        REPORT_DIR.mkdir(exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = REPORT_DIR / f"qa_report_{ts}.html"

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_html, encoding="utf-8")
    print(f"  Report saved to: {report_path}")

    # Also save a latest symlink/copy
    latest_path = report_path.parent / "qa_report_latest.html"
    latest_path.write_text(report_html, encoding="utf-8")
    print(f"  Latest copy at:  {latest_path}")

    # Exit code
    if failed > 0:
        print("\nExit code: 1 (failures found)")
        sys.exit(1)
    else:
        print("\nExit code: 0")
        sys.exit(0)


if __name__ == "__main__":
    main()
