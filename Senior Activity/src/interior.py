"""Orchestrate the interior PDF: front matter, sections, puzzles, remedies,
solutions."""
from __future__ import annotations
from . import config as C
from .layout import Renderer
from . import frontmatter

DIR_FULL = {"E": "right", "W": "left", "S": "down", "N": "up",
            "SE": "down-right", "SW": "down-left",
            "NE": "up-right", "NW": "up-left"}


def build_interior(theme, book, out_path: str) -> int:
    r = Renderer(out_path, theme, theme.title)
    total = book.puzzle_count

    frontmatter.render(r, theme, total)

    # Word Search
    r.section_divider("Word Search",
                      "Find each word in the grid. Words may read across, down, "
                      "or diagonally depending on the level.")
    r.one_per_page(book.wordsearches, r.draw_wordsearch, "Word Search")

    # Sudoku
    r.section_divider("Sudoku", "Fill every row, column, and box with 1-9.")
    r.two_per_page(book.sudokus, r.draw_sudoku_half, "Sudoku")

    # Crosswords
    if book.crosswords:
        r.section_divider("Crosswords", "Themed clues. Answers are at the back.")
        r.one_per_page(book.crosswords, r.draw_crossword_full, "Crossword")

    # Word Scramble
    r.section_divider("Word Scramble",
                      "Unscramble each set of letters to reveal a themed word.")
    r.two_per_page(book.scrambles, r.draw_scramble, "Word Scramble")

    # Trivia + Finish-the-Phrase
    r.section_divider("Trivia & Finish-the-Phrase",
                      "Test your knowledge. Answers are at the back.")
    r.two_per_page(book.trivias, r.draw_trivia, "Trivia & Finish-the-Phrase")

    # Mazes
    r.section_divider("Mazes", "Find your way from Start to Finish.")
    r.one_per_page(book.mazes, r.draw_maze_full, "Mazes")

    # Coloring
    if book.coloring_keys:
        r.section_divider("Coloring Pages", "Relax and color.")
        r.one_per_page(book.coloring_keys, r.draw_coloring, "Coloring")

    # Home Remedies
    r.draw_remedies(book.remedies, book.remedies_title)

    # Solutions
    r.section_divider("Solutions", "All answers grouped here at the back.")

    # Word search: no answer key (finding the listed words IS the puzzle; the
    # word list on each page is the key - standard for large-print WS books).

    r.four_per_page(book.sudokus, r.draw_sudoku_solution_half, "Solutions - Sudoku")

    if book.crosswords:
        r.four_per_page(book.crosswords, r.draw_crossword_solution_half,
                        "Solutions - Crosswords")

    scr_sections = [("Word Scramble - Answers", [
        f"{s.scrambled}  ->  {s.answer}" for s in book.scrambles])]
    r.flow_lines(scr_sections, "Solutions - Word Scramble")

    tri_sections = [("Trivia & Finish-the-Phrase - Answers", [
        f"{t.prompt}  ->  {t.answer}" for t in book.trivias])]
    r.flow_lines(tri_sections, "Solutions - Trivia")

    if book.mazes:
        r.four_per_page(book.mazes, r.draw_maze_solution_half, "Solutions - Mazes")

    r.finish()
    return r.page_num
