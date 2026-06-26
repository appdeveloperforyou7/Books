"""Build the covers for ALL 10 themes as a consistent family.

Covers don't need a finished interior - only the theme (title/accent), the hero
art, and consistent series stats (puzzle count + page count for the spine).
This lets us generate and review the whole cover family before every interior
content bank is written.
"""
from __future__ import annotations
from . import config as C
from .themes.registry import THEMES
from .cover import build_cover

FULL_PUZZLES = 180
FULL_PAGES_FALLBACK = 172  # used only if an interior PDF isn't present yet


def _actual_pages(theme_key) -> int:
    """Read the real interior page count so the cover spine always matches."""
    interior = C.OUTPUT_DIR / theme_key / f"{theme_key}-interior.pdf"
    if interior.exists():
        try:
            import fitz
            return fitz.open(str(interior)).page_count
        except Exception:
            pass
    return FULL_PAGES_FALLBACK


def main():
    for key, theme in THEMES.items():
        out_dir = C.OUTPUT_DIR / key
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{key}-cover.pdf"
        pages = _actual_pages(key)
        build_cover(theme, pages, FULL_PUZZLES, str(path))
        print(f"cover: {path}  (spine for {pages} pp)")
    print(f"Built {len(THEMES)} covers (family).")


if __name__ == "__main__":
    main()
