"""Trivia + Finish-the-Phrase. Data-driven; multiple-choice options are shuffled
(with the correct index recorded) so each render is fresh but verifiable."""
from __future__ import annotations
import random
from dataclasses import dataclass


@dataclass
class Trivia:
    kind: str          # "mc" | "phrase" | "open"
    prompt: str        # question or "I Love ____"
    options: list      # [] for phrase/open
    answer: str
    tier: str = ""

    def verify(self) -> bool:
        if self.kind == "mc":
            return bool(self.options) and self.answer in self.options
        return bool(self.answer.strip())


def from_mc(item: dict, tier: str, rng: random.Random) -> Trivia:
    opts = list(item["options"])
    rng.shuffle(opts)
    return Trivia(kind="mc", prompt=item["q"], options=opts,
                  answer=item["answer"], tier=tier)


def from_phrase(item: dict, tier: str) -> Trivia:
    return Trivia(kind="phrase", prompt=item["prompt"], options=[],
                  answer=item["answer"], tier=tier)


def from_open(item: dict, tier: str) -> Trivia:
    return Trivia(kind="open", prompt=item["q"], options=[],
                  answer=item["answer"], tier=tier)
