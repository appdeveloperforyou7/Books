from PIL import Image
import numpy as np

img = Image.open(r'D:\Kapil\Books\The Quiet Wife\covers\hardcover_cover.png')
arr = np.array(img)

content_mask = (arr[:,:,:3] < 250).any(axis=2)
rows_with_content = content_mask.any(axis=1)
cols_with_content = content_mask.any(axis=0)

top = np.argmax(rows_with_content)
bottom = len(rows_with_content) - np.argmax(rows_with_content[::-1]) - 1
left = np.argmax(cols_with_content)
right = len(cols_with_content) - np.argmax(cols_with_content[::-1]) - 1

DPI = 300
print(f"Canvas: {img.size}")
print(f"Content bounds: top={top}, bottom={bottom}, left={left}, right={right}")
print(f"Gap top: {top}px ({top/DPI:.3f}\"), Gap bottom: {img.size[1]-bottom-1}px ({(img.size[1]-bottom-1)/DPI:.3f}\")")
print(f"Gap left: {left}px ({left/DPI:.3f}\"), Gap right: {img.size[0]-right-1}px ({(img.size[0]-right-1)/DPI:.3f}\")")

# Expected: content_offset = (10.417 - 8.75)/2 = 0.8335" = 250px
print(f"\nExpected top/bottom gap: 250px (0.833\")")
print(f"Expected left gap (back flap): {round((14.115 - 5.625 - 0.449 - 5.625)/2 * 300)}px")
