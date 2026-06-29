import re
with open(r"D:\Kapil\Books\Elena Vance Series\Second\manuscript.md", encoding="utf-8") as f:
    lines = f.readlines()

blocks = []
start = None
for i, line in enumerate(lines):
    s = line.strip()
    is_break = (s == "" or s.startswith("#") or s.startswith(">") or s.startswith("```")
                or s.startswith("---") or s.startswith("- ") or s.startswith("**SMS")
                or s.startswith("*") and not s.startswith("*The"))
    if is_break:
        if start is not None and (i - start) >= 6:
            sample = lines[start].strip()[:60]
            blocks.append((start+1, i, i-start, sample))
        start = None
    else:
        if start is None:
            start = i

blocks.sort(key=lambda x: x[2], reverse=True)
for start, end, count, sample in blocks[:10]:
    print(f"L{start}-{end} ({count} lines): {sample}...")
