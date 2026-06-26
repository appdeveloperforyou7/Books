"""Sudoku generator (6x6 mini and 9x9) with a UNIQUE-solution guarantee.

A full valid solution is built by randomized backtracking, then cells are
removed one at a time; a removal is kept only if the puzzle still has exactly
one solution. So every puzzle we ship is solver-verified to be unique.
"""
from __future__ import annotations
import random
from copy import deepcopy
from dataclasses import dataclass, field

BLOCK = {6: (2, 3), 9: (3, 3)}  # size -> (block rows, block cols)


@dataclass
class Sudoku:
    size: int
    cells: list  # list[list[int]], 0 = blank
    given: list  # list[list[bool]] True = clue shown to solver
    solution: list
    tier: str = ""
    title: str = ""

    def verify(self) -> bool:
        sols = _count_solutions(self.cells, self.size, limit=2)
        return sols == 1


def _block_dims(n):
    return BLOCK[n]


def _valid(cells, r, c, val, n, br, bc):
    if val in cells[r]:
        return False
    if any(cells[i][c] == val for i in range(n)):
        return False
    br0, bc0 = (r // br) * br, (c // bc) * bc
    for i in range(br0, br0 + br):
        for j in range(bc0, bc0 + bc):
            if cells[i][j] == val:
                return False
    return True


def _solve_fill(cells, n, br, bc, rng) -> bool:
    for r in range(n):
        for c in range(n):
            if cells[r][c] == 0:
                vals = list(range(1, n + 1))
                rng.shuffle(vals)
                for v in vals:
                    if _valid(cells, r, c, v, n, br, bc):
                        cells[r][c] = v
                        if _solve_fill(cells, n, br, bc, rng):
                            return True
                        cells[r][c] = 0
                return False
    return True


def _count_solutions(cells, n, limit=2) -> int:
    br, bc = _block_dims(n)
    work = deepcopy(cells)
    count = 0

    def bt() -> bool:
        nonlocal count
        for r in range(n):
            for c in range(n):
                if work[r][c] == 0:
                    for v in range(1, n + 1):
                        if _valid(work, r, c, v, n, br, bc):
                            work[r][c] = v
                            if bt():
                                work[r][c] = 0
                                return True
                            work[r][c] = 0
                    return False
        count += 1
        return count >= limit

    bt()
    return count


def generate(size: int, givens_frac: float, rng: random.Random,
             tier: str = "") -> Sudoku:
    br, bc = _block_dims(size)
    sol = [[0] * size for _ in range(size)]
    _solve_fill(sol, size, br, bc, rng)

    cells = deepcopy(sol)
    positions = [(r, c) for r in range(size) for c in range(size)]
    rng.shuffle(positions)

    target_givens = max(size, round(size * size * givens_frac))
    clue_count = size * size
    for r, c in positions:
        if clue_count <= target_givens:
            break
        saved = cells[r][c]
        cells[r][c] = 0
        if _count_solutions(cells, size, limit=2) == 1:
            clue_count -= 1
        else:
            cells[r][c] = saved

    given = [[cells[r][c] != 0 for c in range(size)] for r in range(size)]
    pz = Sudoku(size=size, cells=cells, given=given, solution=sol, tier=tier)
    if not pz.verify():
        raise RuntimeError("Sudoku failed uniqueness check")
    return pz
