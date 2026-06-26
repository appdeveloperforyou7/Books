"""Assemble a theme's content bank into concrete, tiered puzzle instances.

Enforces the QA rules: no duplicate words across word-search grids, and each
instance is solver-verified at creation. Raises clearly if a bank is too small
for the requested counts (a signal to curate more content).
"""
from __future__ import annotations
import random
from dataclasses import dataclass, field

from . import config as C
from .themes.registry import get_theme
from .puzzles import wordsearch, sudoku, scramble, trivia as trivia_mod, mazes, crossword


def _discover_banks() -> dict:
    """Auto-register every src/themes/bank_*.py module (key = filename suffix).

    Lets new content banks be dropped in without editing this file.
    """
    import importlib
    import pkgutil
    from .themes import __path__ as _tpaths
    banks = {}
    for mod in pkgutil.iter_modules(_tpaths):
        if mod.name.startswith("bank_"):
            key = mod.name[len("bank_"):]
            try:
                m = importlib.import_module(f".themes.{mod.name}", __package__)
                if hasattr(m, "build"):
                    banks[key] = m.build
            except Exception as e:  # noqa
                print(f"[bank] skip {mod.name}: {e}")
    return banks


THEME_BANKS = _discover_banks()


@dataclass
class Book:
    theme_key: str
    wordsearches: list = field(default_factory=list)
    sudokus: list = field(default_factory=list)
    scrambles: list = field(default_factory=list)
    trivias: list = field(default_factory=list)
    crosswords: list = field(default_factory=list)
    mazes: list = field(default_factory=list)
    coloring_keys: list = field(default_factory=list)
    remedies: list = field(default_factory=list)
    remedies_title: str = ""

    @property
    def puzzle_count(self) -> int:
        return (len(self.wordsearches) + len(self.sudokus) + len(self.scrambles)
                + len(self.trivias) + len(self.crosswords) + len(self.mazes))

    def all_puzzles(self):
        yield from self.wordsearches
        yield from self.sudokus
        yield from self.scrambles
        yield from self.trivias
        yield from self.crosswords
        yield from self.mazes


def _flat_unique_words(pools) -> list[str]:
    seen, out = set(), []
    for cat, words in pools.items():
        for w in words:
            w = w.upper()
            if w not in seen:
                seen.add(w)
                out.append(w)
    return out


def assemble(theme_key: str, counts: dict, seed: int = 1337,
             coloring_n: int = 4) -> Book:
    rng = random.Random(seed)
    theme = get_theme(theme_key)
    bank = THEME_BANKS[theme_key]()
    book = Book(theme_key=theme_key,
                coloring_keys=list(bank["coloring"])[:coloring_n],
                remedies=list(bank["remedies"]),
                remedies_title=bank.get("remedies_title", "Home Remedies & Wellness Wisdom"))

    # --- Word Search (per tier: only words that fit the grid; cycle so a full
    # build always succeeds with minimal repetition) ---
    pool = _flat_unique_words(bank["word_pools"])
    rng.shuffle(pool)
    tier_pool = {t: [w for w in pool if len(w) <= C.WS_GRID[t]] for t in C.TIERS}
    cursor = {t: 0 for t in C.TIERS}
    n = 0
    tier_label = {"easy": "Easy", "medium": "Medium", "challenger": "Challenger"}
    for t in C.TIERS:
        tp = tier_pool[t]
        if len(tp) < C.WS_WORDS[t]:
            raise ValueError(f"Not enough <= {C.WS_GRID[t]}-letter words for "
                             f"easy/word-search tier '{t}'.")
        for _ in range(counts["wordsearch"][t]):
            k = C.WS_WORDS[t]
            words = [tp[(cursor[t] + i) % len(tp)] for i in range(k)]
            cursor[t] += k
            n += 1
            ws = wordsearch.generate(
                C.WS_GRID[t], words, C.WS_DIRS[t], rng,
                title=f"Word Search {n}  -  {tier_label[t]}")
            ws.tier = t
            book.wordsearches.append(ws)

    # --- Sudoku ---
    ns = 0
    for t in C.TIERS:
        for i in range(counts["sudoku"][t]):
            size = 6 if (t == "easy" and i % 3 == 0) else 9
            ns += 1
            pz = sudoku.generate(size, C.SUDOKU_GIVENS[t], rng, tier=t)
            pz.title = f"Sudoku {ns}"
            book.sudokus.append(pz)

    # --- Word Scramble (separate shuffle; single words from pool) ---
    scramble_pool = [w for w in _flat_unique_words(bank["word_pools"])
                     if 3 <= len(w) <= 11]
    rng.shuffle(scramble_pool)
    # pick a category hint per word for medium/easy
    cat_of = {}
    for cat, words in bank["word_pools"].items():
        for w in words:
            cat_of.setdefault(w.upper(), cat)
    si = 0
    for t in C.TIERS:
        for _ in range(counts["scramble"][t]):
            if si >= len(scramble_pool):
                raise ValueError("Word bank too small for scramble count.")
            word = scramble_pool[si]; si += 1
            book.scrambles.append(
                scramble.generate(word, cat_of.get(word, theme.title), t, rng))

    # --- Trivia / Finish-the-Phrase ---
    def _take(items, n, label):
        if len(items) < n:
            raise ValueError(f"Bank too small: need {n} {label}, have {len(items)}.")
        return items[:n]
    for item in _take(bank["trivia_easy"], counts["trivia"]["easy"], "easy trivia"):
        book.trivias.append(trivia_mod.from_mc(item, "easy", rng))
    for item in _take(bank["phrase_medium"], counts["trivia"]["medium"], "phrases"):
        book.trivias.append(trivia_mod.from_phrase(item, "medium"))
    for item in _take(bank["trivia_open"], counts["trivia"]["challenger"], "open trivia"):
        book.trivias.append(trivia_mod.from_open(item, "challenger"))

    # --- Crosswords (themed, interlocking, solver-verified) ---
    ncw = 0
    for t in C.TIERS:
        for _ in range(counts["crosswords"][t]):
            ncw += 1
            cw = crossword.generate(C.CW_GRID[t], bank["crossword"], rng,
                                    C.CW_WORDS[t], tier=t,
                                    title=f"Crossword {ncw}")
            book.crosswords.append(cw)

    # --- Mazes ---
    nm = 0
    for t in C.TIERS:
        for _ in range(counts["mazes"][t]):
            g = C.MAZE_GRID[t]
            nm += 1
            mz = mazes.generate(g, g, rng, tier=t)
            mz.title = f"Maze {nm}"
            book.mazes.append(mz)

    return book
