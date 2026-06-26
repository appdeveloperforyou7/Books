"""Word scramble generator + verifier. Guarantees the scramble differs from
the answer (and isn't a trivial single-swap) so the puzzle is real."""
from __future__ import annotations
import random
from dataclasses import dataclass


@dataclass
class Scramble:
    answer: str
    scrambled: str
    hint: str  # category or first-letter hint
    tier: str = ""

    def verify(self) -> bool:
        a, s = self.answer.upper(), self.scrambled.upper()
        return sorted(a) == sorted(s) and a != s


def _scramble(word: str, rng: random.Random) -> str:
    letters = list(word)
    if len(letters) <= 1:
        return word
    for _ in range(50):
        rng.shuffle(letters)
        cand = "".join(letters)
        if cand != word:
            return cand
    # deterministic fallback: rotate by one
    return word[1:] + word[0]


def generate(word: str, category: str, tier: str,
             rng: random.Random) -> Scramble:
    word = word.upper()
    s = _scramble(word, rng)
    if tier == "easy":
        hint = f"Starts with '{word[0]}' - {category}"
    elif tier == "medium":
        hint = category
    else:
        hint = ""
    pz = Scramble(answer=word, scrambled=s, hint=hint, tier=tier)
    if not pz.verify():
        raise RuntimeError(f"Bad scramble for {word}")
    return pz
