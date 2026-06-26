"""Maze generator (recursive backtracker -> perfect maze) + BFS solver.

A perfect maze has exactly one path between any two cells, so it is always
solvable; the solver confirms the entrance->exit path and supplies it."""
from __future__ import annotations
import random
from collections import deque
from dataclasses import dataclass, field

# wall bits per cell
N, E, S, W = 1, 2, 4, 8
OPP = {N: S, S: N, E: W, W: E}
DMOVE = {N: (-1, 0), S: (1, 0), E: (0, 1), W: (0, -1)}


@dataclass
class Maze:
    rows: int
    cols: int
    walls: list  # list[list[int]] bitmask of walls present
    solution: list  # list[(r,c)] entrance->exit
    tier: str = ""
    title: str = ""

    def verify(self) -> bool:
        return len(self.solution) > 0 and self.solution[0] == (0, 0) \
            and self.solution[-1] == (self.rows - 1, self.cols - 1)


def generate(rows: int, cols: int, rng: random.Random, tier: str = "") -> Maze:
    walls = [[N | E | S | W for _ in range(cols)] for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]
    stack = [(0, 0)]
    visited[0][0] = True
    while stack:
        r, c = stack[-1]
        neigh = []
        for b in (N, E, S, W):
            dr, dc = DMOVE[b]
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                neigh.append((b, nr, nc))
        if neigh:
            b, nr, nc = rng.choice(neigh)
            walls[r][c] &= ~b
            walls[nr][nc] &= ~OPP[b]
            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()

    # open entrance (top of start) and exit (bottom of end)
    walls[0][0] &= ~N
    walls[rows - 1][cols - 1] &= ~S

    sol = _solve(walls, rows, cols)
    pz = Maze(rows=rows, cols=cols, walls=walls, solution=sol, tier=tier)
    if not pz.verify():
        raise RuntimeError("Maze not solvable")
    return pz


def _solve(walls, rows, cols) -> list:
    start, end = (0, 0), (rows - 1, cols - 1)
    q = deque([start])
    prev = {start: None}
    while q:
        r, c = q.popleft()
        if (r, c) == end:
            break
        for b in (N, E, S, W):
            if walls[r][c] & b:
                continue
            dr, dc = DMOVE[b]
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in prev:
                prev[(nr, nc)] = (r, c)
                q.append((nr, nc))
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    return path
