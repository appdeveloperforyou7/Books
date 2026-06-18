import sys
sys.path.insert(0, r"D:\Kapil\Books\TD-1")
from manifest_batch_client import build_full_prompt, detect_characters, _count_kids, _count_robots

tests = [
    "Daadi in warm kitchen making samosas. Lace curtains with sunlight.",
    "Maya at dark desk. Blip flickering to life with cyan glow on faces.",
    "Four kids Maya, Leo, Zara and Sam in cozy underground lab headquarters. String lights.",
    "Dark basement corridor with rough concrete walls.",
]

for raw in tests:
    chars = detect_characters(raw)
    n_kids = _count_kids(chars)
    n_bots = _count_robots(chars)
    full = build_full_prompt(raw)
    has_crit = "CRITICAL" in full
    print(f"Chars: {chars} | Kids: {n_kids} | Bots: {n_bots} | Has CRITICAL: {has_crit}")
    if has_crit:
        idx = full.index("CRITICAL")
        print(f"  Constraint: {full[idx:idx+200]}")
    print()
