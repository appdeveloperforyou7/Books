"""Theme registry - 10 EVERGREEN, all-country themes (no decade/era/nostalgia).

A theme drives the book's title/cover/keywords AND its puzzle content (word
banks, scramble, trivia, crosswords, coloring, remedies flavor). Sudoku and
mazes are theme-neutral. Only `gardens` has a full content bank so far; the
engine builds any registered theme once its bank is added.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

SUBTITLE = "Large-Print Memory Games, Brain Puzzles & Activities for Seniors"


@dataclass(frozen=True)
class Theme:
    key: str
    volume: int
    title: str
    subtitle: str = SUBTITLE
    accent_hex: str = "#333333"

    @property
    def accent(self):
        from reportlab.lib.colors import HexColor
        return HexColor(self.accent_hex)


THEMES: Dict[str, Theme] = {
    "gardens":     Theme("gardens", 1, "Gardens, Flowers & Birds", accent_hex="#2E7D32"),
    "food":        Theme("food", 2, "Food & Kitchen Favorites", accent_hex="#C62828"),
    "travel":      Theme("travel", 3, "Travel & Places Around the World", accent_hex="#1565C0"),
    "faith":       Theme("faith", 4, "Faith, Hope & Inspiration", accent_hex="#6A1B9A"),
    "holidays":    Theme("holidays", 5, "Holidays & Family Celebrations", accent_hex="#00838F"),
    "musicmovies": Theme("musicmovies", 6, "Music & Movies", accent_hex="#3949AB"),
    "nature":      Theme("nature", 7, "Nature & the Great Outdoors", accent_hex="#33691E"),
    "animals":     Theme("animals", 8, "Animals & Pets", accent_hex="#EF6C00"),
    "sports":      Theme("sports", 9, "Sports, Games & Hobbies", accent_hex="#C2185B"),
    "wellness":    Theme("wellness", 10, "Wellness & Healthy Living", accent_hex="#00695C"),
}


def get_theme(key: str) -> Theme:
    if key not in THEMES:
        raise KeyError(f"Unknown theme '{key}'. Known: {sorted(THEMES)}")
    return THEMES[key]
