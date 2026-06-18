#!/usr/bin/env python3
path = r'd:\Kapil\Books\Meera Desai\MD - Two Chains\Manuscript_v3.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = "A map. A 2,300-year-old map, broken into six pieces and scattered across a continent, each piece hidden in an artifact that changed hands through auction houses and private dealers and museum donations, accumulating centuries of provenance while waiting for someone to reassemble them."

new = old + """

She pulled up Priya's detailed analysis on her phone, scrolling to the numeral breakdown. The Ashokan Brahmi numeral system used only nine symbols, not ten, because the concept of zero was represented by a positional gap rather than a character. The numerals were: one (a single vertical stroke), two (two horizontal strokes), three (three horizontal strokes), four (a cross), five (a hook), six (a spiral), seven (a vertical stroke with a right-curving diagonal), eight (a figure resembling a stylized H), nine (a circular form).

The coordinates in the inscriptions were not decimal. They were sexagesimal, base-60, the same system that had traveled from Mesopotamia to India along ancient trade routes. Each inscription contributed one pair of numerals, a latitude component and a longitude component, and each pair was positioned within the sexagesimal grid according to a formula that Priya was still deciphering.

The reader could work through it themselves, if they wanted. The first inscription gave: seven, three. The second: five, eight. Put together in the sexagesimal grid, those four numerals, 7, 3, 5, 8, produced a latitudinal reading that corresponded to the northeastern coast of North America. Add the remaining four inscriptions and the location narrowed to a single point.

But the sixth inscription was the key. Without it, the grid produced a circle of uncertainty fifty miles in diameter, the difference between the right location and a costly detour."""

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Brahmi puzzle: APPLIED")
else:
    print("Brahmi puzzle: NOT FOUND")