"""Themed crossword generator (interlocking, black-square) + verifier.

Words come from a themed clue bank and interlock on shared letters. Every cell
that is not part of a placed word stays a black square, so every across/down
entry is a real themed word (no random fill, no gibberish). verify() confirms
every white run (len>=2) is exactly one of the placed words.
"""
from __future__ import annotations
import random
from dataclasses import dataclass, field


@dataclass
class Crossword:
    size: int
    grid: list              # list[list[str|None]]  None = black
    numbers: dict           # (r,c) -> clue number
    entries: list           # [{number, word, clue, direction, row, col}]
    tier: str = ""
    title: str = ""

    def verify(self) -> bool:
        n = self.size
        # 1) each entry's letters match the grid
        for e in self.entries:
            dr, dc = (0, 1) if e["direction"] == "across" else (1, 0)
            for i, ch in enumerate(e["word"]):
                rr, cc = e["row"] + i * dr, e["col"] + i * dc
                if self.grid[rr][cc] != ch:
                    return False
        # 2) every white run (len>=2) must be one of the placed entries
        entry_keys = {(e["direction"], e["row"], e["col"]): e["word"]
                      for e in self.entries}
        # across runs
        for r in range(n):
            c = 0
            while c < n:
                if self.grid[r][c] is not None:
                    s = c
                    while c < n and self.grid[r][c] is not None:
                        c += 1
                    if c - s >= 2:
                        if ("across", r, s) not in entry_keys:
                            return False
                else:
                    c += 1
        # down runs
        for c in range(n):
            r = 0
            while r < n:
                if self.grid[r][c] is not None:
                    s = r
                    while r < n and self.grid[r][c] is not None:
                        r += 1
                    if r - s >= 2:
                        if ("down", s, c) not in entry_keys:
                            return False
                else:
                    r += 1
        return len(self.entries) >= 4


def _put(grid, word, r, c, direction):
    dr, dc = (0, 1) if direction == "across" else (1, 0)
    for ch in word:
        grid[r][c] = ch
        r += dr
        c += dc


def _can_place(grid, n, word, r, c, direction, need_intersection):
    dr, dc = (0, 1) if direction == "across" else (1, 0)
    # cell before start must be black/off-grid
    br, bc = r - dr, c - dc
    if 0 <= br < n and 0 <= bc < n and grid[br][bc] is not None:
        return False
    # cell after end must be black/off-grid
    er, ec = r + dr * len(word), c + dc * len(word)
    if 0 <= er < n and 0 <= ec < n and grid[er][ec] is not None:
        return False
    intersects = False
    for i, ch in enumerate(word):
        rr, cc = r + i * dr, c + i * dc
        if not (0 <= rr < n and 0 <= cc < n):
            return False
        cell = grid[rr][cc]
        if cell is None:
            # reject perpendicular adjacency that would form an orphan run
            if direction == "across":
                for nr, nc in ((rr - 1, cc), (rr + 1, cc)):
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] is not None:
                        return False
            else:
                for nr, nc in ((rr, cc - 1), (rr, cc + 1)):
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] is not None:
                        return False
        elif cell == ch:
            intersects = True
        else:
            return False
    return (not need_intersection) or intersects


def _find_placement(grid, n, word, occupied, rng):
    """Try to cross `word` with an existing letter; return (r,c,dir) or None."""
    idxs = list(range(len(word)))
    rng.shuffle(idxs)
    for i in idxs:
        ch = word[i]
        cells = list(occupied.get(ch, []))
        rng.shuffle(cells)
        for (r, c) in cells:
            for direction in ("across", "down"):
                dr, dc = (0, 1) if direction == "across" else (1, 0)
                sr, sc = r - i * dr, c - i * dc
                if _can_place(grid, n, word, sr, sc, direction, True):
                    return (sr, sc, direction)
    return None


def generate(size: int, bank: list, rng: random.Random, target: int,
             tier: str = "", title: str = "") -> Crossword:
    # normalize + dedupe bank; keep single-token alpha words that fit
    seen, clean = set(), []
    for word, clue in bank:
        w = word.upper()
        if w.isalpha() and 3 <= len(w) <= size and w not in seen:
            seen.add(w)
            clean.append((w, clue))

    best = None
    for _ in range(80):
        rng.shuffle(clean)
        anchor = sorted(clean, key=lambda x: -len(x[0]))[0]
        w0, clue0 = anchor
        grid = [[None] * size for _ in range(size)]
        r0, c0 = size // 2, (size - len(w0)) // 2
        _put(grid, w0, r0, c0, "across")
        placed = [{"word": w0, "clue": clue0, "row": r0, "col": c0,
                   "direction": "across"}]
        used = {w0}
        occupied = {}
        for i, ch in enumerate(w0):
            occupied.setdefault(ch, set()).add((r0, i + c0))

        rest = [x for x in clean if x[0] != w0]
        for w, clue in rest:
            if len(placed) >= target:
                break
            if w in used:
                continue
            res = _find_placement(grid, size, w, occupied, rng)
            if res is None:
                continue
            sr, sc, direction = res
            _put(grid, w, sr, sc, direction)
            placed.append({"word": w, "clue": clue, "row": sr, "col": sc,
                           "direction": direction})
            used.add(w)
            dr, dc = (0, 1) if direction == "across" else (1, 0)
            for i, ch in enumerate(w):
                occupied.setdefault(ch, set()).add((sr + i * dr, sc + i * dc))

        if len(placed) < max(4, target - 3):
            continue
        numbers, numbered_entries = _number(grid, size, placed)
        cw = Crossword(size=size, grid=grid, numbers=numbers,
                       entries=numbered_entries, tier=tier, title=title)
        if cw.verify():
            if best is None or len(cw.entries) > len(best.entries):
                best = cw
            if len(cw.entries) >= target - 1:
                break
    if best is None:
        raise RuntimeError("Could not build a valid crossword from the bank")
    return best


def _number(grid, n, placed):
    num = 0
    numbers = {}
    by_pos = {(p["direction"], p["row"], p["col"]): p for p in placed}
    out = []
    for r in range(n):
        for c in range(n):
            if grid[r][c] is None:
                continue
            starts_across = (c == 0 or grid[r][c - 1] is None) and \
                (c + 1 < n and grid[r][c + 1] is not None)
            starts_down = (r == 0 or grid[r - 1][c] is None) and \
                (r + 1 < n and grid[r + 1][c] is not None)
            if starts_across or starts_down:
                num += 1
                numbers[(r, c)] = num
                if starts_across and ("across", r, c) in by_pos:
                    p = by_pos[("across", r, c)]
                    out.append({**p, "number": num})
                if starts_down and ("down", r, c) in by_pos:
                    p = by_pos[("down", r, c)]
                    out.append({**p, "number": num})
    return numbers, out
