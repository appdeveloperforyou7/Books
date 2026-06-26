"""QA: solver-verify every puzzle + enforce the 'no Ayurveda' hard constraint."""
from __future__ import annotations
from . import config as C


def verify_all(book) -> dict:
    report = {"puzzles": 0, "passed": 0, "failed": [], "counts": {}}
    for kind in ("wordsearches", "sudokus", "scrambles", "trivias",
                 "crosswords", "mazes"):
        items = getattr(book, kind)
        report["counts"][kind] = len(items)
        for i, pz in enumerate(items):
            report["puzzles"] += 1
            ok = pz.verify()
            if ok:
                report["passed"] += 1
            else:
                report["failed"].append(f"{kind}[{i}]")
    return report


def grep_forbidden(book) -> list[str]:
    """Return any content strings containing 'Ayurveda' (must be empty)."""
    hits = []
    needle = "ayurveda"
    blobs = [book.remedies_title]
    for r in book.remedies:
        if isinstance(r, dict):
            blobs.append(r.get("condition", ""))
            blobs.append(r.get("text", ""))
        else:
            blobs.append(r)
    for ws in book.wordsearches:
        blobs += [w for w, _ in ws.words]
    for sc in book.scrambles:
        blobs.append(sc.answer)
    for t in book.trivias:
        blobs.append(t.prompt)
        blobs += t.options
        blobs.append(t.answer)
    for b in blobs:
        if needle in b.lower():
            hits.append(b)
    return hits


def assert_counts(book, counts: dict) -> list[str]:
    """Check the book matches the requested tier counts."""
    errs = []
    mapping = {"wordsearches": "wordsearch", "sudokus": "sudoku",
               "scrambles": "scramble", "trivias": "trivia",
               "crosswords": "crosswords", "mazes": "mazes"}
    for attr, key in mapping.items():
        items = getattr(book, attr)
        by_tier = {"easy": 0, "medium": 0, "challenger": 0}
        for pz in items:
            t = getattr(pz, "tier", None) or "easy"
            if t in by_tier:
                by_tier[t] += 1
        for t in C.TIERS:
            want = counts[key][t]
            if by_tier[t] != want:
                errs.append(f"{key}.{t}: want {want}, got {by_tier[t]}")
    return errs
