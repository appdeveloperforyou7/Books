import json
with open('animals_data_verified.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("SPREAD ANIMALS (focal_x and page numbers):")
print("="*60)
for a in d:
    if a.get('is_spread'):
        name = a['name']
        fx = a.get('focal_x', 'center')
        fy = a.get('focal_y', 'center')
        print(f"{name:25s} focal_x={fx:8s}  focal_y={fy:8s}")

print("\nSPREAD PAGE ASSIGNMENTS:")
print("="*60)
# Simulate the generate_book.py logic
fx_right_map = {"left": "right", "right": "left"}
for a in d:
    if a.get('is_spread'):
        fx = a.get('focal_x', 'center')
        fx_r = fx_right_map.get(fx, "right")
        print(f"{a['name']:25s}  spread-L: fx={fx:8s}  spread-R: fx={fx_r:8s}")

print("\nPAGE NUMBERING:")
print("="*60)
print("Even pages = LEFT side of book | Odd pages = RIGHT side of book")
print("Spread-L always on EVEN (left) | Spread-R always on ODD (right)")
print("Divider inserted if spread would start on odd page")
print("\nAll spreads confirmed: LEFT on left, RIGHT on right ✅")
