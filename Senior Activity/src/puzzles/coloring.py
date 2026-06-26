"""Bonus coloring pages - simple bold line art (vector), keyed by name.

Each draw_* takes a reportlab canvas and a box (x0,y0 = bottom-left, w,h).
Stroke is bold (>=2pt) with large open shapes for easy shading.
"""
from __future__ import annotations
import math

LW = 2.6


def _setup(c):
    c.setLineWidth(LW)
    c.setStrokeGray(0)


def draw(c, key: str, x0: float, y0: float, w: float, h: float) -> None:
    fn = SHAPES.get(key, SHAPES["star"])
    fn(c, x0, y0, w, h)


def star(c, x0, y0, w, h):
    _setup(c)
    cx, cy = x0 + w / 2, y0 + h / 2
    r_out = min(w, h) * 0.42
    r_in = r_out * 0.45
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    c.drawPath(p, stroke=1, fill=0)


def record(c, x0, y0, w, h):
    _setup(c)
    cx, cy = x0 + w / 2, y0 + h / 2
    R = min(w, h) * 0.44
    c.circle(cx, cy, R, stroke=1, fill=0)
    c.circle(cx, cy, R * 0.62, stroke=1, fill=0)
    c.circle(cx, cy, R * 0.28, stroke=1, fill=0)
    c.circle(cx, cy, R * 0.05, stroke=1, fill=1)


def car(c, x0, y0, w, h):
    _setup(c)
    # schematic 1950s convertible side profile
    body_y = y0 + h * 0.34
    bw = w * 0.82
    bh = h * 0.22
    bx = x0 + (w - bw) / 2
    p = c.beginPath()
    p.moveTo(bx, body_y)
    p.lineTo(bx + bw, body_y)
    p.lineTo(bx + bw, body_y + bh * 0.6)
    p.lineTo(bx + bw * 0.72, body_y + bh * 0.6)
    p.lineTo(bx + bw * 0.58, body_y + bh)          # cabin front
    p.lineTo(bx + bw * 0.30, body_y + bh)          # cabin back
    p.lineTo(bx + bw * 0.10, body_y + bh * 0.6)
    p.lineTo(bx, body_y + bh * 0.6)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    # tail fin accent
    c.line(bx + bw * 0.92, body_y + bh * 0.6, bx + bw, body_y + bh * 0.95)
    # wheels
    wr = min(w, h) * 0.10
    c.circle(bx + bw * 0.22, body_y - wr * 0.2, wr, stroke=1, fill=0)
    c.circle(bx + bw * 0.78, body_y - wr * 0.2, wr, stroke=1, fill=0)


def rocket(c, x0, y0, w, h):
    _setup(c)
    cx = x0 + w / 2
    top = y0 + h * 0.88
    nose = y0 + h * 0.55
    base = y0 + h * 0.22
    rw = w * 0.16
    p = c.beginPath()
    p.moveTo(cx, top)
    p.lineTo(cx - rw, nose)
    p.lineTo(cx - rw, base)
    p.lineTo(cx + rw, base)
    p.lineTo(cx + rw, nose)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    c.circle(cx, (nose + base) / 2, rw * 0.45, stroke=1, fill=0)  # window
    # fins
    c.line(cx - rw, base, cx - rw * 1.9, y0 + h * 0.10)
    c.line(cx - rw, base, cx - rw * 1.9, y0 + h * 0.10)
    c.line(cx + rw, base, cx + rw * 1.9, y0 + h * 0.10)
    # flame
    c.line(cx, base, cx, y0 + h * 0.05)
    c.line(cx - rw * 0.6, base, cx - rw * 0.4, y0 + h * 0.08)
    c.line(cx + rw * 0.6, base, cx + rw * 0.4, y0 + h * 0.08)


def teapot(c, x0, y0, w, h):
    _setup(c)
    cx, cy = x0 + w / 2, y0 + h * 0.42
    rx, ry = w * 0.26, h * 0.22
    c.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, stroke=1, fill=0)  # body
    c.ellipse(cx - rx * 0.9, cy + ry * 0.4, cx + rx * 0.9,
              cy + ry * 1.1, stroke=1, fill=0)  # lid
    c.line(cx, cy + ry * 1.1, cx, cy + ry * 1.45)  # knob stem
    c.circle(cx, cy + ry * 1.5, w * 0.02, stroke=1, fill=1)
    # spout
    p = c.beginPath()
    p.moveTo(cx + rx * 0.8, cy + ry * 0.2)
    p.lineTo(cx + rx * 1.7, cy + ry * 0.9)
    p.lineTo(cx + rx * 1.7, cy + ry * 0.4)
    p.lineTo(cx + rx * 0.9, cy - ry * 0.1)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    # handle
    c.ellipse(cx - rx * 1.9, cy - ry * 0.5, cx - rx * 0.9, cy + ry * 0.7,
              stroke=1, fill=0)


def guitar(c, x0, y0, w, h):
    _setup(c)
    cx = x0 + w / 2
    body_cy = y0 + h * 0.34
    rx, ry = w * 0.22, h * 0.20
    c.ellipse(cx - rx, body_cy - ry, cx + rx, body_cy + ry, stroke=1, fill=0)
    c.circle(cx, body_cy + ry * 0.35, ry * 0.28, stroke=1, fill=0)  # soundhole
    # neck
    nw = w * 0.07
    c.rect(cx - nw / 2, body_cy + ry * 0.6, nw, h * 0.45, stroke=1, fill=0)
    # headstock
    c.rect(cx - nw, y0 + h * 0.92, nw * 2, h * 0.06, stroke=1, fill=0)


def flower(c, x0, y0, w, h):
    _setup(c)
    cx, cy = x0 + w / 2, y0 + h * 0.56
    pr = min(w, h) * 0.16
    for k in range(6):
        ang = k * (math.pi / 3)
        px = cx + pr * 2.0 * math.cos(ang)
        py = cy + pr * 2.0 * math.sin(ang)
        c.circle(px, py, pr, stroke=1, fill=0)
    c.circle(cx, cy, pr * 0.9, stroke=1, fill=0)
    # stem + leaves
    c.setLineWidth(LW)
    c.line(cx, cy - pr, cx, y0 + h * 0.06)
    c.ellipse(cx - pr * 2.2, y0 + h * 0.16, cx - pr * 0.4, y0 + h * 0.30,
              stroke=1, fill=0)
    c.ellipse(cx + pr * 0.4, y0 + h * 0.26, cx + pr * 2.2, y0 + h * 0.40,
              stroke=1, fill=0)


def bird(c, x0, y0, w, h):
    _setup(c)
    cx, cy = x0 + w * 0.46, y0 + h * 0.50
    rb = min(w, h) * 0.20
    c.ellipse(cx - rb, cy - rb * 0.7, cx + rb, cy + rb * 0.7, stroke=1, fill=0)
    # head
    hr = rb * 0.6
    hx, hy = cx + rb * 0.9, cy + rb * 0.4
    c.circle(hx, hy, hr, stroke=1, fill=0)
    # beak
    p = c.beginPath()
    p.moveTo(hx + hr, hy)
    p.lineTo(hx + hr * 2.2, hy + hr * 0.3)
    p.lineTo(hx + hr, hy - hr * 0.4)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    # eye
    c.circle(hx + hr * 0.4, hy + hr * 0.2, hr * 0.12, stroke=1, fill=1)
    # tail
    p = c.beginPath()
    p.moveTo(cx - rb, cy)
    p.lineTo(cx - rb * 2.4, cy - rb * 0.5)
    p.lineTo(cx - rb * 2.4, cy + rb * 0.5)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    # legs
    c.line(cx + rb * 0.1, cy - rb * 0.7, cx + rb * 0.1, y0 + h * 0.12)
    c.line(cx - rb * 0.4, cy - rb * 0.7, cx - rb * 0.4, y0 + h * 0.12)


def butterfly(c, x0, y0, w, h):
    _setup(c)
    cx, cy = x0 + w / 2, y0 + h / 2
    s = min(w, h) * 0.40
    c.ellipse(cx - s * 0.9, cy - s * 0.15, cx - s * 0.1, cy + s * 0.85,
              stroke=1, fill=0)  # upper-left wing
    c.ellipse(cx + s * 0.1, cy - s * 0.15, cx + s * 0.9, cy + s * 0.85,
              stroke=1, fill=0)  # upper-right wing
    c.ellipse(cx - s * 0.7, cy - s * 0.95, cx - s * 0.1, cy - s * 0.05,
              stroke=1, fill=0)  # lower-left wing
    c.ellipse(cx + s * 0.1, cy - s * 0.95, cx + s * 0.7, cy - s * 0.05,
              stroke=1, fill=0)  # lower-right wing
    # body
    c.ellipse(cx - s * 0.07, cy - s * 0.8, cx + s * 0.07, cy + s * 0.8,
              stroke=1, fill=1)
    # antennae
    c.line(cx, cy + s * 0.8, cx - s * 0.25, cy + s * 1.15)
    c.line(cx, cy + s * 0.8, cx + s * 0.25, cy + s * 1.15)


def wateringcan(c, x0, y0, w, h):
    _setup(c)
    cx = x0 + w * 0.42
    by = y0 + h * 0.30
    bw, bh = w * 0.40, h * 0.40
    # body (trapezoid)
    p = c.beginPath()
    p.moveTo(cx - bw / 2, by)
    p.lineTo(cx + bw / 2, by)
    p.lineTo(cx + bw / 2.6, by + bh)
    p.lineTo(cx - bw / 2.6, by + bh)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    # handle
    c.ellipse(cx - bw * 0.75, by + bh * 0.2, cx - bw * 0.35, by + bh * 0.85,
              stroke=1, fill=0)
    # spout
    p = c.beginPath()
    p.moveTo(cx + bw / 2, by + bh * 0.25)
    p.lineTo(cx + bw * 1.5, by + bh * 0.9)
    p.lineTo(cx + bw * 1.5, by + bh * 0.55)
    p.lineTo(cx + bw / 2, by + bh * 0.05)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    # rose (perforated cap)
    c.circle(cx + bw * 1.5, by + bh * 0.72, bw * 0.18, stroke=1, fill=0)


def sun(c, x0, y0, w, h):
    _setup(c)
    cx, cy = x0 + w / 2, y0 + h / 2
    r = min(w, h) * 0.26
    c.circle(cx, cy, r, stroke=1, fill=0)
    for k in range(12):
        ang = k * (math.pi / 6)
        c.line(cx + (r * 1.2) * math.cos(ang), cy + (r * 1.2) * math.sin(ang),
               cx + (r * 1.9) * math.cos(ang), cy + (r * 1.9) * math.sin(ang))


def leaf(c, x0, y0, w, h):
    _setup(c)
    cx = x0 + w / 2
    top = y0 + h * 0.88
    bot = y0 + h * 0.10
    half = w * 0.30
    # two arcs forming a pointed leaf
    p = c.beginPath()
    p.moveTo(cx, top)
    p.curveTo(cx + half, top - h * 0.25, cx + half, bot + h * 0.25, cx, bot)
    p.curveTo(cx - half, bot + h * 0.25, cx - half, top - h * 0.25, cx, top)
    c.drawPath(p, stroke=1, fill=0)
    # midrib + veins
    c.line(cx, top, cx, bot)
    for frac in (0.30, 0.50, 0.70):
        yy = top - (top - bot) * frac
        ext = half * (1 - abs(frac - 0.5) * 1.4)
        c.line(cx, yy, cx + ext, yy + h * 0.06)
        c.line(cx, yy, cx - ext, yy + h * 0.06)


SHAPES = {
    "star": star, "record": record, "car": car,
    "rocket": rocket, "teapot": teapot, "guitar": guitar,
    "flower": flower, "bird": bird, "butterfly": butterfly,
    "wateringcan": wateringcan, "sun": sun, "leaf": leaf,
}
