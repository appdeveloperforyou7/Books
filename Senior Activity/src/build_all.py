"""Build a full (180-puzzle) interior + cover + metadata for EVERY theme that
has a content bank. Run after the fan-out bank sessions finish:

    python -m src.build_all
"""
from __future__ import annotations
import sys

from .content_assembler import THEME_BANKS
from .build import build_one


def main():
    keys = sorted(THEME_BANKS.keys())
    print(f"Themes with a content bank ({len(keys)}): {keys}")
    if len(keys) < 10:
        print(f"Note: {10 - len(keys)} theme bank(s) still missing "
              f"(fan-out sessions may still be running).")
    ok, fail = [], []
    for key in keys:
        try:
            res = build_one(key, "full", seed=1337)
            ok.append(key)
            print(f"  OK   {key:12} {res['puzzles']} puzzles, "
                  f"{res['pages']} pp, verified {res['verified']}")
        except Exception as e:  # noqa
            fail.append((key, str(e)[:120]))
            print(f"  ERR  {key:12} {e}")
    print("-" * 50)
    print(f"Built {len(ok)}/{len(keys)} books." +
          (f"  Failed: {fail}" if fail else ""))
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
