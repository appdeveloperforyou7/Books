# Endangered Animals Book - Project Progress
**Last updated**: 2026-04-06 12:30 PM

## Completed Work

### 1. Root Folder Cleanup
- Removed all obsolete scripts (20+ .py files), debug screenshots (13 .png), temp files
- Organized project into clean structure: `src/`, `templates/`, `images/`, `Output/`
- Root folder contains ONLY directories

### 2. Image Quality & Cropping - COMPLETE OVERHAUL
- **Smart pre-cropping**: All 71 images automatically cropped to page ratio (0.767) using edge-detection to find the region of interest
- **Lanczos upscaling**: All 64 sub-1500px images upscaled to 2400px+ with PIL LANCZOS
- **Result**: All 71 images at 2400px+ width, no more face/body cutoff
- Cropped images stored in `images/cropped/`, originals kept in `images/`

### 3. Cover Page Fix
- Fixed cover dimensions from `8.5in x 11in` to `8.625in x 11.25in` (matching actual page size)
- Cover content now properly centered within the full bleed page

### 4. Image Positioning
- All single pages use `background-position: center center` (images pre-cropped, no focal point guessing)
- Spread pages use `left center` / `right center` for proper two-page panorama
- Removed all focal_x/focal_y from generate_book.py (handled by pre-cropped images)

### 5. Info Box Position Adjustments (12 animals)
All adjustments from Priority 1 applied:
| Animal | Change |
|--------|--------|
| Chinese Giant Salamander | pos-top-right → pos-top-left |
| Pygmy Hog | pos-bottom-right → pos-top-left |
| Grevy's Zebra | pos-top-right + focal_x:left → pos-bottom-left + focal_x:center |
| Black-footed Ferret | pos-top-left → pos-bottom-right |
| Wild Bactrian Camel | pos-bottom-right → pos-top-right |
| Amami Rabbit | pos-top-left → pos-bottom-left |
| Dhole | pos-bottom-right + focal_x:left → pos-bottom-left + focal_x:right |
| Hirola | pos-top-right + focal_x:left → pos-top-left + focal_x:right |
| Ethiopian Wolf | pos-top-left → pos-top-right |
| Dama Gazelle | pos-bottom-right → pos-top-right (focal_y:top kept) |
| Bornean Orangutan | pos-top-right → pos-bottom-right |
| Snow Leopard | focal_y:top → focal_y:center |

### 6. Copyright/Attribution Updated
- Copyright page updated with proper Wikimedia Commons CC license attribution
- References CC BY 4.0, CC BY-SA 4.0, CC0 licenses
- Offers individual attributions upon request

### 7. Project Cleanup
- Deleted all obsolete scripts (fetch_new_images, upgrade_images_v2-v7, debug_downloads, etc.)
- Deleted all debug screenshots (verify_pdf_page*.png)
- Deleted duplicate PNG files from images/
- Deleted backup files (*_backup.png, *.tmp*)
- Deleted __pycache__
- Cleaned archive folder (kept only v15)

## Final Output
- **PDF**: `Output/Chronicles_of_the_Endangered.pdf` (82 pages, 211 MB, ~384 DPI)
- **Archive**: `Output/archive/book_premium_kdp_v15.pdf`
- **Audit pages**: `temp_audit/` (82 JPEG pages for review)

## Project Structure
```
Endangered Animals/
├── images/
│   ├── cropped/          # Pre-cropped, upscaled images (used by book)
│   ├── *.jpg             # Original images from Wikimedia
│   └── forest_cover_bg.png
├── Output/
│   ├── Chronicles_of_the_Endangered.pdf   # Final book
│   └── archive/book_premium_kdp_v15.pdf   # Archive copy
├── src/
│   ├── generate_book.py
│   ├── animals_data_verified.json
│   └── progress.md
├── templates/
│   ├── cover_page.html
│   ├── sample_page.html
│   ├── toc_page.html
│   ├── divider_page.html
│   ├── copyright_page.html
│   └── back_cover.html
└── temp_audit/           # 82 page audit images
```

## REMAINING (optional enhancements)
- Add Dedication/Acknowledgments page
- Add Photo credits/attribution page with specific photographer names
- Replace ISBN placeholder with real ISBN
- Initialize git repo
- Visual QA by human (review temp_audit/ pages)
- KDP upload test
