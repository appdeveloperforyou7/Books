"""Word search generator + verifier. Words placed in tier-allowed directions;
every word is confirmed placed before the grid is filled."""
from __future__ import annotations
import random
import string
from dataclasses import dataclass, field

DIRS = {
    "E": (0, 1), "W": (0, -1), "S": (1, 0), "N": (-1, 0),
    "SE": (1, 1), "SW": (1, -1), "NE": (-1, 1), "NW": (-1, -1),
}


@dataclass
class WordSearch:
    size: int
    grid: list  # list of list of single chars
    words: list  # ordered list of (word, direction)
    placements: dict  # word -> (row, col, direction)
    title: str = ""
    tier: str = ""

    def verify(self) -> bool:
        """Confirm every listed word is actually findable in its direction."""
        for word, _dir in self.words:
            if word not in self.placements:
                return False
            r, c, d = self.placements[word]
            dr, dc = DIRS[d]
            for i, ch in enumerate(word):
                rr, cc = r + i * dr, c + i * dc
                if not (0 <= rr < self.size and 0 <= cc < self.size):
                    return False
                if self.grid[rr][cc] != ch:
                    return False
        return True


def _try_place(grid, size, word, direction, rng) -> tuple | None:
    dr, dc = DIRS[direction]
    starts = [(r, c) for r in range(size) for c in range(size)]
    rng.shuffle(starts)
    for r, c in starts:
        er, ec = r + dr * (len(word) - 1), c + dc * (len(word) - 1)
        if not (0 <= er < size and 0 <= ec < size):
            continue
        ok = True
        for i, ch in enumerate(word):
            cell = grid[r + i * dr][c + i * dc]
            if cell is not None and cell != ch:
                ok = False
                break
        if ok:
            return (r, c)
    return None


def generate(size: int, words: list[str], directions: tuple[str, ...],
             rng: random.Random, title: str = "") -> WordSearch:
    words = [w.upper() for w in words]
    for attempt in range(40):
        grid = [[None] * size for _ in range(size)]
        placements = {}
        success = True
        for word in words:
            placed = False
            dirs = list(directions)
            rng.shuffle(dirs)
            for d in dirs:
                res = _try_place(grid, size, word, d, rng)
                if res is not None:
                    r, c = res
                    dr, dc = DIRS[d]
                    for i, ch in enumerate(word):
                        grid[r + i * dr][c + i * dc] = ch
                    placements[word] = (r, c, d)
                    placed = True
                    break
            if not placed:
                success = False
                break
        if success:
            for r in range(size):
                for c in range(size):
                    if grid[r][c] is None:
                        grid[r][c] = rng.choice(string.ascii_uppercase)
            ws = WordSearch(size=size, grid=grid,
                            words=[(w, placements[w][2]) for w in words],
                            placements=placements, title=title)
            if ws.verify():
                return ws
    raise RuntimeError(f"Could not place words in {size}x{size} grid: {words}")
