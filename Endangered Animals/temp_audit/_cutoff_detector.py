"""
Automated face/body cutoff detector for book pages.
Analyzes each rendered page to detect if the animal's face/head is cut off at edges.
Uses pixel analysis of the edge regions to detect subject cutoff.
"""
import os
import json
from PIL import Image
import numpy as np

BASE = r"D:\Kapil\Books\Endangered Animals"
AUDIT = os.path.join(BASE, "temp_audit")

# Load page-to-animal mapping
with open(os.path.join(BASE, "animals_data_verified.json")) as f:
    animals = json.load(f)

# Build page map
pg = 4
page_map = {}
for a in animals:
    spread = a.get("is_spread", False)
    if spread:
        if pg % 2 != 0:
            page_map[pg] = ("Divider", None)
            pg += 1
        page_map[pg] = (f"{a['name']} (spread-L)", a)
        pg += 1
        page_map[pg] = (f"{a['name']} (spread-R)", a)
        pg += 1
    else:
        page_map[pg] = (a["name"], a)
        pg += 1

page_map[1] = ("Cover", None)
page_map[2] = ("Copyright", None)
page_map[3] = ("TOC", None)
page_map[5] = ("Divider", None)

# Divider pages
divider_pages = set()
pg = 4
for a in animals:
    spread = a.get("is_spread", False)
    if spread:
        if pg % 2 != 0:
            divider_pages.add(pg)
            pg += 1
        pg += 2
    else:
        pg += 1
if pg % 2 != 0:
    divider_pages.add(pg)
divider_pages.add(82)  # back cover

print("=" * 70)
print("  FACE/BODY CUTOFF AUDIT — All 82 Pages")
print("=" * 70)
print()

issues = []

for pn in range(1, 83):
    if pn in (1, 2, 3, 5) or pn in divider_pages:
        continue
    
    fpath = os.path.join(AUDIT, f"page_{pn:02d}.jpg")
    if not os.path.exists(fpath):
        continue
    
    img = Image.open(fpath).convert("RGB")
    arr = np.array(img)
    h, w = arr.shape[:2]
    
    name, animal_data = page_map.get(pn, (f"Page {pn}", None))
    
    # Analyze edges - look for non-black, non-info-box content at edges
    # The info box is typically dark/black, so we look for bright content at edges
    
    edge_width = int(w * 0.08)  # 8% from each edge
    edge_height = int(h * 0.08)
    
    # Get edge strips
    left_edge = arr[:, :edge_width, :]
    right_edge = arr[:, -edge_width:, :]
    top_edge = arr[:edge_height, :, :]
    bottom_edge = arr[-edge_height:, :, :]
    
    # Check if edges have significant non-dark content (animal body)
    # Dark = mean brightness < 40
    left_bright = np.mean(left_edge, axis=2).mean()
    right_bright = np.mean(right_edge, axis=2).mean()
    top_bright = np.mean(top_edge, axis=2).mean()
    bottom_bright = np.mean(bottom_edge, axis=2).mean()
    
    # Check if there's a sharp transition at the edge (animal cut off)
    # Compare edge brightness to center
    center = arr[edge_height:h-edge_height, edge_width:w-edge_width, :]
    center_bright = np.mean(center)
    
    # Check edge variation (high variation = content, low = uniform bg)
    left_var = np.std(np.mean(left_edge, axis=2))
    right_var = np.std(np.mean(right_edge, axis=2))
    top_var = np.std(np.mean(top_edge, axis=2))
    bottom_var = np.std(np.mean(bottom_edge, axis=2))
    
    cutoff_edges = []
    
    # If edge has significant brightness AND variation, something is there
    # and if it's brighter than typical background, it's likely a cut-off animal
    threshold_bright = 30
    threshold_var = 15
    
    if left_bright > threshold_bright and left_var > threshold_var:
        cutoff_edges.append(f"LEFT edge (brightness={left_bright:.0f}, var={left_var:.0f})")
    if right_bright > threshold_bright and right_var > threshold_var:
        cutoff_edges.append(f"RIGHT edge (brightness={right_bright:.0f}, var={right_var:.0f})")
    if top_bright > threshold_bright and top_var > threshold_var:
        cutoff_edges.append(f"TOP edge (brightness={top_bright:.0f}, var={top_var:.0f})")
    if bottom_bright > threshold_bright and bottom_var > threshold_var:
        cutoff_edges.append(f"BOTTOM edge (brightness={bottom_bright:.0f}, var={bottom_var:.0f})")
    
    if cutoff_edges:
        issues.append((pn, name, cutoff_edges))

print(f"Pages with potential cutoffs at edges: {len(issues)}")
print()
for pn, name, edges in issues:
    print(f"  P{pn:02d} — {name}")
    for e in edges:
        print(f"        {e}")

print()
print("=" * 70)
print(f"  TOTAL POTENTIAL CUTOFFS: {len(issues)} / {82 - len(diver_pages) - 4} animal pages")
print("=" * 70)
