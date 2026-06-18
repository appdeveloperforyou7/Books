import cv2
import numpy as np

IMG = r"D:\Kapil\Books\TD-1\Images\title_page.png"
OUT = r"D:\Kapil\Books\TD-1\Images\title_page.png"

img = cv2.imread(IMG)
if img is None:
    print(f"ERROR: Cannot read {IMG}")
    exit(1)

h, w = img.shape[:2]
print(f"Image size: {w}x{h}")

overlay = img.copy()

text_line1 = "THE GLITCH SQUAD"
font = cv2.FONT_HERSHEY_SIMPLEX

font_scale = w / 300.0
thickness = max(2, int(font_scale * 2.5))

(tw1, th1), _ = cv2.getTextSize(text_line1, font, font_scale, thickness)
print(f"Text size: {tw1}x{th1}, font_scale={font_scale:.2f}, thickness={thickness}")

margin_top = int(h * 0.06)
text_x1 = (w - tw1) // 2
text_y1 = margin_top + th1

padding = int(th1 * 0.4)
rx1 = text_x1 - padding
ry1 = margin_top - padding // 2
rx2 = text_x1 + tw1 + padding
ry2 = text_y1 + padding
cv2.rectangle(overlay, (rx1, ry1), (rx2, ry2), (10, 10, 30), -1)
alpha_rect = 0.75
cv2.addWeighted(overlay, alpha_rect, img, 1 - alpha_rect, 0, img)

outline_color = (0, 0, 0)
fill_color = (60, 220, 255)

for dx in range(-thickness, thickness + 1):
    for dy in range(-thickness, thickness + 1):
        if dx * dx + dy * dy <= thickness * thickness:
            cv2.putText(img, text_line1, (text_x1 + dx, text_y1 + dy), font, font_scale, outline_color, thickness + 2, cv2.LINE_AA)

cv2.putText(img, text_line1, (text_x1, text_y1), font, font_scale, fill_color, thickness, cv2.LINE_AA)

cv2.imwrite(OUT, img)
print(f"Saved with title overlay -> {OUT}")
