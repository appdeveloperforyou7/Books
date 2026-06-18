import os
from PIL import Image
import numpy as np

audit_dir = r"D:\Kapil\Books\Endangered Animals\temp_audit"
live_files = sorted([f for f in os.listdir(audit_dir) if f.startswith("_live_p") and f.endswith(".png")])

print(f"Found {len(live_files)} live screenshots")
print(f"{'Page':<8} {'File':<20} {'Size':<10} {'Dim':<16} {'MeanB':<8} {'StdDev':<8} {'Dark%':<8} {'Notes'}")
print("-"*90)

for f in live_files:
    path = os.path.join(audit_dir, f)
    size_kb = os.path.getsize(path) / 1024
    img = Image.open(path).convert("RGB")
    w, h = img.size
    arr = np.array(img)
    mean_brightness = arr.mean()
    std_dev = arr.std()
    dark_pct = (arr.mean(axis=2) < 30).mean() * 100
    
    notes = []
    if size_kb < 300: notes.append("VERY SMALL FILE")
    if std_dev < 20: notes.append("LOW CONTRAST")
    if dark_pct > 70: notes.append("VERY DARK")
    if dark_pct < 1: notes.append("VERY BRIGHT")
    if w > 2000: notes.append(f"WIDE={w}")
    
    pn = f.replace("_live_p", "").replace(".png", "")
    notes_str = "; ".join(notes) if notes else ""
    print(f"{pn:<8} {f:<20} {size_kb:<10.0f} {w}x{h:<12} {mean_brightness:<8.0f} {std_dev:<8.0f} {dark_pct:<8.1f} {notes_str}")
