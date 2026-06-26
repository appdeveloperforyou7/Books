"""Batch runner: assemble -> QA -> interior PDF -> cover PDF -> metadata CSV.

Run from the project root:
    python run.py --theme gardens --preset slice
    python -m src.build --theme gardens --preset full
"""
from __future__ import annotations
import argparse
import sys

from . import config as C
from .content_assembler import assemble
from . import qa as qa_mod
from .interior import build_interior
from .cover import build_cover
from .metadata import export as export_metadata


def build_one(theme_key: str, preset: str, seed: int = 1337) -> dict:
    counts = C.PRESETS[preset]
    book = assemble(theme_key, counts, seed=seed, coloring_n=C.COLORING[preset])

    # --- QA (fail fast if anything is broken/forbidden) ---
    ver = qa_mod.verify_all(book)
    if ver["failed"]:
        raise RuntimeError(f"QA failures (puzzles not verified): {ver['failed']}")
    forbidden = qa_mod.grep_forbidden(book)
    if forbidden:
        raise RuntimeError(f"Forbidden term found: {forbidden}")
    count_errs = qa_mod.assert_counts(book, counts)
    if count_errs:
        raise RuntimeError(f"Count mismatch: {count_errs}")

    total = book.puzzle_count

    out_dir = C.OUTPUT_DIR / theme_key
    out_dir.mkdir(parents=True, exist_ok=True)
    interior_path = out_dir / f"{theme_key}-interior.pdf"
    cover_path = out_dir / f"{theme_key}-cover.pdf"
    meta_path = out_dir / f"{theme_key}-metadata.csv"

    pages = build_interior(book.theme if hasattr(book, "theme") else
                           _theme(theme_key), book, str(interior_path))
    theme = _theme(theme_key)
    build_cover(theme, pages, total, str(cover_path))
    export_metadata(theme, total, str(meta_path))

    return {
        "theme": theme_key, "preset": preset, "puzzles": total,
        "pages": pages, "verified": ver["passed"],
        "interior": str(interior_path), "cover": str(cover_path),
        "metadata": str(meta_path),
    }


def _theme(theme_key):
    from .themes.registry import get_theme
    return get_theme(theme_key)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build a Bright Mind activity book.")
    ap.add_argument("--theme", default="gardens")
    ap.add_argument("--preset", choices=list(C.PRESETS), default="slice")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args(argv)

    res = build_one(args.theme, args.preset, seed=args.seed)
    print("=" * 60)
    print(f"Built: {res['theme']}  ({res['preset']} preset)")
    print(f"Puzzles: {res['puzzles']}  |  Verified: {res['verified']}")
    print(f"Interior pages: {res['pages']}")
    print(f"Interior: {res['interior']}")
    print(f"Cover:    {res['cover']}")
    print(f"Metadata: {res['metadata']}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
