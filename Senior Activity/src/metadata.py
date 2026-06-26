"""KDP metadata CSV exporter (title, subtitle, keywords, categories, pricing)."""
from __future__ import annotations
import csv
from . import config as C
from .frontmatter import DISCLAIMER


def _keywords(theme) -> list[str]:
    key = theme.key if hasattr(theme, "key") else theme.title
    return KEYWORDS.get(key, KEYWORDS["_default"])


CATEGORIES = [
    "Humor & Entertainment > Puzzles & Games > Word Search",
    "Humor & Entertainment > Puzzles & Games > Word Games",
    "Humor & Entertainment > Puzzles & Games > Puzzles",
]


# The shared factual backbone inserted into every description.
_BACKBONE = (
    "- Extra-large, high-contrast print that is easy on the eyes\n"
    "- Three gentle levels: Easy, Medium, and Challenger\n"
    "- Every solution grouped at the back of the book\n"
    "- A roomy 8.5 x 11 layout with one big puzzle per page\n"
    "- Word search, sudoku, crosswords, word scrambles, trivia,\n"
    "  finish-the-phrase, mazes, and relaxing coloring pages\n"
    "- A bonus page of traditional Home Remedies & Wellness Wisdom"
)


def _desc(theme, total_puzzles: int, lead: str, hook: str, close: str) -> str:
    return (
        lead
        + f"{total_puzzles}+ large-print brain games and puzzles for adults and seniors. "
        + hook
        + "\n\n"
        + "Inside you will find:\n"
        + _BACKBONE
        + "\n\n"
        + close
    )


def _description(theme, total_puzzles: int) -> str:
    key = theme.key if hasattr(theme, "key") else theme.title
    variant = DESCRIPTIONS.get(key, DESCRIPTIONS["_default"])
    return _desc(theme, total_puzzles,
                 variant["lead"], variant["hook"], variant["close"])


KEYWORDS: dict[str, list[str]] = {
    "gardens": [
        "large print puzzle book seniors",
        "gardens flowers birds word search large print",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "giant print word search adults",
        "garden themed sudoku crossword seniors",
        "cognitive puzzles for seniors gardening",
    ],
    "food": [
        "large print puzzle book seniors",
        "food kitchen cooking word search large print",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "nostalgia food trivia puzzles seniors",
        "jumbo print sudoku crosswords adults",
        "kitchen themed brain games elderly",
    ],
    "travel": [
        "large print puzzle book seniors",
        "travel places world word search large print",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "armchair travel trivia puzzles seniors",
        "giant print sudoku crossword adults",
        "world geography puzzles large print elderly",
    ],
    "faith": [
        "large print puzzle book seniors",
        "faith inspiration scripture word search large print",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "uplifting christian puzzles seniors",
        "jumbo print sudoku crosswords adults",
        "faith based brain games elderly",
    ],
    "holidays": [
        "large print puzzle book seniors",
        "holidays christmas celebration word search large print",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "festive holiday trivia puzzles seniors",
        "giant print sudoku crossword adults",
        "holiday themed brain games elderly",
    ],
    "musicmovies": [
        "large print puzzle book seniors",
        "classic movies music word search large print",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "nostalgia music movie trivia seniors",
        "jumbo print sudoku crosswords adults",
        "golden era brain games elderly",
    ],
    "nature": [
        "large print puzzle book seniors",
        "nature outdoors wildlife word search large print",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "nature themed trivia puzzles seniors",
        "giant print sudoku crossword adults",
        "great outdoors brain games elderly",
    ],
    "animals": [
        "large print puzzle book seniors",
        "animals pets word search large print",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "pets animals trivia puzzles seniors",
        "jumbo print sudoku crosswords adults",
        "animal themed brain games elderly",
    ],
    "sports": [
        "large print puzzle book seniors",
        "sports games hobbies word search large print",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "sports trivia puzzles seniors",
        "giant print sudoku crossword adults",
        "game day brain games elderly",
    ],
    "wellness": [
        "large print puzzle book seniors",
        "wellness healthy living word search large print",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "home remedies wellness wisdom seniors",
        "jumbo print sudoku crosswords adults",
        "healthy living brain games elderly",
    ],
    "_default": [
        "large print puzzle book seniors",
        "brain games elderly adults",
        "memory activity book seniors gift",
        "giant print word search adults",
        "large print sudoku crossword seniors",
        "cognitive puzzles for seniors",
        "activity book elderly large print",
    ],
}


DESCRIPTIONS: dict[str, dict] = {
    "gardens": {
        "lead": "Step into a calmer, greener state of mind. ",
        "hook": (
            "Gardens, Flowers & Birds celebrates everything that blooms and "
            "sings - from favourite flowers and garden birds to the simple "
            "pleasure of a sunny afternoon outdoors. Every page invites you "
            "to slow down, reminisce, and give your mind a gentle, joyful "
            "workout."
        ),
        "close": (
            "Perfect for a quiet morning with a cup of tea, a rehab or "
            "recovery stay, or as a thoughtful gift for a parent, partner, "
            "or grandparent who loves the garden."
        ),
    },
    "food": {
        "lead": "Pull up a chair and dig in. ",
        "hook": (
            "Food & Kitchen Favorites serves up the comfort of the family "
            "table - classic dishes, beloved ingredients, and the memories "
            "that come with them. It is warm, nostalgic fun that keeps the "
            "mind busy and the memories close."
        ),
        "close": (
            "A delightful companion for a slow afternoon, a hospital or "
            "care visit, or a feel-good gift for the food lover in your life."
        ),
    },
    "travel": {
        "lead": "Pack your imagination and set off. ",
        "hook": (
            "Travel & Places Around the World takes you on an armchair "
            "adventure across famous cities, landmarks, and dream "
            "destinations - no passport required. Spark happy memories of "
            "past trips and plan a few daydreams along the way."
        ),
        "close": (
            "Ideal for the curious traveller, the housebound explorer, or "
            "anyone who loves a big, satisfying puzzle and a trip down "
            "memory lane."
        ),
    },
    "faith": {
        "lead": "A little peace for the heart and a gentle stretch for the mind. ",
        "hook": (
            "Faith, Hope & Inspiration gathers uplifting themes of comfort, "
            "gratitude, and encouragement into puzzles that soothe as they "
            "challenge. It is quiet, meaningful brain exercise rooted in "
            "hope."
        ),
        "close": (
            "A comforting gift for a loved one in recovery, a church or "
            "care community, or anyone who enjoys a thoughtful, faith-filled "
            "puzzle."
        ),
    },
    "holidays": {
        "lead": "Celebrate all year round. ",
        "hook": (
            "Holidays & Family Celebrations recaptures the magic of special "
            "days - the songs, the foods, the traditions, and the gatherings "
            "that bring families together. Each puzzle is a warm wave of "
            "nostalgia."
        ),
        "close": (
            "Wonderful for holiday visits, festive gift-giving, or brightening "
            "a loved one's day in any season."
        ),
    },
    "musicmovies": {
        "lead": "Turn up the memories. ",
        "hook": (
            "Music & Movies rewinds to the songs you sang and the films you "
            "loved. From golden-era stars to chart-topping hits, these "
            "puzzles are pure nostalgia designed to spark stories and smiles."
        ),
        "close": (
            "A brilliant conversation-starter for family visits, care homes, "
            "or anyone who treasures the classics."
        ),
    },
    "nature": {
        "lead": "Breathe in the great outdoors. ",
        "hook": (
            "Nature & the Great Outdoors wanders through forests, mountains, "
            "rivers, and wildlife - the landscapes and creatures that calm "
            "the spirit. Gentle, refreshing puzzles keep the mind engaged "
            "and the mood lifted."
        ),
        "close": (
            "A soothing choice for nature lovers, gardeners at heart, or "
            "anyone who finds peace under a wide open sky."
        ),
    },
    "animals": {
        "lead": "For everyone who has ever loved a pet. ",
        "hook": (
            "Animals & Pets celebrates our furry, feathered, and four-legged "
            "friends - the companions who make life warmer. Heart-warming "
            "puzzles and gentle brain games bring on the smiles and the "
            "stories."
        ),
        "close": (
            "A charming gift for an animal lover, a pet owner, or a loved "
            "one who lights up at the mention of a favourite companion."
        ),
    },
    "sports": {
        "lead": "Game on. ",
        "hook": (
            "Sports, Games & Hobbies relives the thrill of game day and the "
            "joy of favourite pastimes - legendary moments, famous players, "
            "and the hobbies that filled happy weekends."
        ),
        "close": (
            "A winning pick for the sports fan, the hobbyist, or the "
            "grandparent with a lifetime of match-day memories."
        ),
    },
    "wellness": {
        "lead": "Feel good, stay sharp. ",
        "hook": (
            "Wellness & Healthy Living blends gentle brain exercise with "
            "real wellbeing wisdom - from simple home remedies to everyday "
            "habits for a calmer, healthier life. It cares for the mind and "
            "the body together."
        ),
        "close": (
            "An encouraging gift for anyone focused on healthy aging, "
            "recovery, or simply living well, one puzzle at a time."
        ),
    },
    "_default": {
        "lead": "Keep the mind active and the spirit bright. ",
        "hook": (
            "This large-print collection is packed with the brain games and "
            "puzzles adults and seniors love most - relaxing, rewarding, and "
            "easy on the eyes."
        ),
        "close": (
            "A thoughtful gift for mom, dad, or grandparents."
        ),
    },
}


def export(theme, total_puzzles: int, out_path: str) -> None:
    row = {
        "title": f"{theme.subtitle} : {theme.title}",
        "subtitle": f"Volume {theme.volume} of the {C.SERIES}",
        "author": C.IMPRINT,
        "imprint": C.IMPRINT,
        "series": C.SERIES,
        "volume": theme.volume,
        "description": _description(theme, total_puzzles),
        "keywords": " ; ".join(_keywords(theme)),
        "categories": " ; ".join(CATEGORIES),
        "list_price_usd": "14.99",
        "launch_price_usd": "12.99-13.99",
        "trim": "8.5 x 11",
        "interior": "black & white, cream paper",
        "language": "English",
        "disclaimer": DISCLAIMER,
    }
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader()
        w.writerow(row)
