#!/usr/bin/env python3
"""Draw the v5 front page: Friday 20 November 2026 world news in one image.

Fresh build for make.fun news-image-20261120. Draws a 1024x1024 newspaper
front page with Pillow and saves it as entry.png next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 30, 26)
DARKRED = (140, 20, 18)
NAVY = (18, 38, 74)
TEAL = (14, 90, 96)
GREY = (90, 88, 82)
LIGHT = (233, 228, 214)
RULE = (60, 58, 52)

F_SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
F_SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
F_SERIF_IT = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
F_SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
F_SANS_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    """Split text into lines that fit width pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, width, fill=INK, leading=None):
    """Draw wrapped text, return y just below the last line."""
    lh = leading or int(font.size * 1.22)
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def centre(draw, cx, y, text, font, fill=INK):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def hrule(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
MX = 28  # side margin
RX = W - MX

# ---- top bar ----
f_top = F(F_SANS_B, 13)
f_top_r = F(F_SANS, 11)
d.text((MX, 12), "THE WORLD IN ONE DAY", font=f_top, fill=RED)
right = "42 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
d.text((RX - d.textlength(right, font=f_top_r), 14), right, font=f_top_r, fill=INK)
hrule(d, MX, RX, 32, width=2)

# ---- masthead ----
f_mast = F(F_SERIF_BLACK, 60)
centre(d, W // 2, 36, "Friday 20 November 2026", f_mast)
f_sub = F(F_SERIF_IT, 17)
centre(d, W // 2, 104,
       "Russian missiles hit Kyiv\u2019s bridges \u00b7 Cyclone Akvan strikes India \u00b7 "
       "An AI sell-off sinks Asia\u2019s markets \u00b7 UK and EU seal a deal", f_sub)
hrule(d, MX, RX, 128, width=3)

# ---- key numbers strip, right under the headline ----
NUMBERS = [
    ("3", "bridges over the Dnipro damaged in Kyiv"),
    ("300,000+", "people moved to shelters before Akvan"),
    ("-6.2%", "Taiwan\u2019s share index, Friday\u2019s close"),
    ("100,000", "youth visas a year in the UK\u2013EU deal"),
    ("2.3%", "Japan consumer inflation in October"),
    ("118", "runs by Glenn Phillips against India"),
]
f_num = F(F_SERIF_BLACK, 30)
f_cap = F(F_SANS, 10)
col_w = (RX - MX) / 6
y_num = 136
for i, (num, cap) in enumerate(NUMBERS):
    x0 = MX + i * col_w
    centre(d, x0 + col_w / 2, y_num, num, f_num)
    para(d, x0 + 8, y_num + 36, cap, f_cap, col_w - 16, fill=GREY, leading=12)
    if i:
        d.line([(x0, y_num + 2), (x0, y_num + 62)], fill=(200, 194, 178), width=1)
hrule(d, MX, RX, 204, width=1)

# ---- region bars ----
REGIONS = [
    ("Europe 10", (18, 58, 110)),
    ("Asia 10", (178, 30, 26)),
    ("Middle East 4", (176, 124, 28)),
    ("Africa 5", (34, 110, 58)),
    ("Americas 7", (104, 52, 150)),
    ("Oceania 4", (14, 120, 122)),
    ("Global 2", (90, 88, 82)),
]
f_reg = F(F_SANS_B, 11)
bx = MX
bw_total = RX - MX
for label, colour in REGIONS:
    tw = d.textlength(label, font=f_reg)
    bw = tw + 22
    d.rounded_rectangle([bx, 212, bx + bw, 232], radius=4, fill=colour)
    d.text((bx + 11, 216), label, font=f_reg, fill=(255, 255, 255))
    bx += bw + 6

# ---- feature illustrations ----
def draw_kyiv(x, y, w, h):
    """Night Kyiv: dark sky, lit skyline, bridge arc, missile trails, blasts."""
    d.rectangle([x, y, x + w, y + h], fill=(13, 24, 54))
    import random
    rnd = random.Random(7)
    for _ in range(46):
        sx = x + rnd.randint(4, w - 4)
        sy = y + rnd.randint(4, int(h * 0.55))
        r = rnd.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(235, 230, 200))
    d.ellipse([x + w - 52, y + 10, x + w - 22, y + 40], fill=(238, 232, 200))
    # skyline with lit windows
    base = y + h - 34
    bx = x
    while bx < x + w:
        bw = rnd.randint(18, 34)
        bh = rnd.randint(26, 62)
        d.rectangle([bx, base - bh, bx + bw, base + 34], fill=(8, 14, 34))
        for wy in range(base - bh + 6, base + 28, 10):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 196, 66))
        bx += bw + 2
    # river + bridge arc
    d.rectangle([x, base + 30, x + w, y + h], fill=(24, 52, 96))
    d.arc([x + 8, base - 6, x + w - 8, base + 66], 180, 360, fill=(200, 200, 190), width=3)
    for px in range(x + 20, x + w - 16, 26):
        d.line([(px, base + 30), (px, base + 12)], fill=(200, 200, 190), width=2)
    # missile trails (dashed arcs) + blasts
    for tx, ty in [(x + 60, y + 46), (x + 170, y + 30), (x + 250, y + 52)]:
        for k in range(6):
            d.ellipse([tx + k * 7, ty + k * k // 3 - 14, tx + k * 7 + 3, ty + k * k // 3 - 11],
                      fill=(255, 220, 130))
        for ang in range(0, 360, 45):
            ex = tx + 16 + int(11 * __import__("math").cos(__import__("math").radians(ang)))
            ey = ty + int(11 * __import__("math").sin(__import__("math").radians(ang)))
            d.line([(tx + 16, ty), (ex, ey)], fill=(255, 166, 0), width=2)
        d.ellipse([tx + 9, ty - 7, tx + 23, ty + 7], fill=(255, 214, 90))


def draw_cyclone(x, y, w, h):
    """Cyclone Akvan: sea, coastline, spiral, landfall dot, rain."""
    d.rectangle([x, y, x + w, y + h], fill=(176, 208, 224))
    # land (top right)
    d.polygon([(x + w * 0.55, y), (x + w, y), (x + w, y + h * 0.42),
               (x + w * 0.72, y + h * 0.5), (x + w * 0.6, y + h * 0.3)],
              fill=(214, 196, 150))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(38, 110, 130))
    # spiral rings
    import math
    cx, cy = x + w * 0.42, y + h * 0.42
    for r in (52, 40, 28, 16):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    # landfall marker + dashed track
    lx, ly = x + w * 0.66, y + h * 0.34
    d.ellipse([lx - 6, ly - 6, lx + 6, ly + 6], fill=RED)
    d.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=(255, 255, 255))
    for k in range(8):
        px = lx - k * 16
        py = ly + k * 7
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    # rain streaks
    for rx in range(x + 12, x + w - 8, 18):
        d.line([(rx, y + h * 0.66), (rx - 5, y + h * 0.66 + 16)], fill=(240, 244, 246), width=2)
    # wave lines
    for wy in (y + h - 26, y + h - 14):
        for wx in range(x + 8, x + w - 20, 26):
            d.arc([wx, wy, wx + 18, wy + 10], 180, 360, fill=(220, 238, 242), width=2)


def draw_selloff(x, y, w, h):
    """AI sell-off: dark board, falling red chart, market table."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 22, 22))
    # falling line chart
    pts = [(x + 14, y + 18), (x + 70, y + 28), (x + 120, y + 26),
           (x + 175, y + 46), (x + 225, y + 60), (x + 280, y + 84)]
    d.line(pts, fill=(230, 60, 50), width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 120, 100))
    d.line([(x + 14, y + 92), (x + w - 14, y + 92)], fill=(90, 84, 78), width=1)
    # market table: 2x2 grid so rows never collide
    f_tab = F(F_SANS_B, 12)
    cells = [(("Taipei", "-6.2%"), ("Tokyo", "-5.1%")),
             (("Seoul", "-5.2%"), ("Hong Kong", "-1.9%"))]
    for r, (left, right) in enumerate(cells):
        ty = y + 98 + r * 16
        for c, (name, val) in enumerate((left, right)):
            cx0 = x + 14 + c * (w // 2)
            d.text((cx0, ty), name, font=f_tab, fill=(240, 236, 228))
            vw = d.textlength(val, font=f_tab)
            d.text((x + 14 + (c + 1) * (w // 2) - 14 - vw, ty), val,
                   font=f_tab, fill=(255, 110, 95))


FEATURES = [
    ("KYIV", "3 bridges hit", "Officials\u2019 count", draw_kyiv,
     "1 \u00b7 KYIV, UKRAINE \u00b7 WAR",
     "Russian missiles hit three Kyiv bridges",
     "An overnight barrage of about 110 missiles and 400 drones killed at least "
     "eight people across Ukraine and cut power and water in the capital.",
     "(Kyiv Independent, BBC)"),
    ("CYCLONE AKVAN", "Landfall \u00b7 8 am", "Weather office", draw_cyclone,
     "2 \u00b7 ODISHA, INDIA \u00b7 CYCLONE",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed the coast near Gopalpur from about 8 am after more than "
     "300,000 people were moved to shelters. No deaths were reported.",
     "(IMD, Deccan Herald)"),
    ("AI SELL-OFF", "Asia, Friday\u2019s close", "Closing prices", draw_selloff,
     "3 \u00b7 TAIPEI \u00b7 SEOUL \u00b7 TOKYO \u00b7 MARKETS",
     "AI sell-off sinks Asia\u2019s stock markets",
     "Taiwan\u2019s index fell 6.2% to end its worst week since 1991. Seoul lost "
     "5.2% and Tokyo 5.1% as chipmakers led the slide.",
     "(Al Jazeera, Anadolu)"),
]
f_kick = F(F_SANS_BLACK, 14)
f_imgcap = F(F_SANS, 10)
f_tag = F(F_SANS_B, 10)
f_fhead = F(F_SERIF_BOLD, 20)
f_fsum = F(F_SANS, 12)
f_src = F(F_SANS_IT, 10) if False else F(F_SERIF_IT, 11)
col_w = (RX - MX - 24) / 3
fy = 240
for i, (kick, cap, src2, draw_fn, tag, head, summ, src) in enumerate(FEATURES):
    fx = MX + i * (col_w + 12)
    ih = 148
    draw_fn(int(fx), fy, int(col_w), ih)
    # kicker label on the illustration
    kw = d.textlength(kick, font=f_kick)
    d.rectangle([fx, fy, fx + kw + 14, fy + 24], fill=RED)
    d.text((fx + 7, fy + 4), kick, font=f_kick, fill=(255, 255, 255))
    # caption strip at the bottom of the illustration
    d.rectangle([fx, fy + ih - 20, fx + col_w, fy + ih], fill=(17, 17, 17))
    d.text((fx + 6, fy + ih - 16), cap, font=f_imgcap, fill=(255, 255, 255))
    sw = d.textlength(src2, font=f_imgcap)
    d.text((fx + col_w - sw - 6, fy + ih - 16), src2, font=f_imgcap, fill=(210, 206, 196))
    ty = fy + ih + 8
    d.text((fx, ty), tag, font=f_tag, fill=RED)
    ty += 15
    ty = para(d, fx, ty, head, f_fhead, col_w, leading=23)
    ty = para(d, fx, ty + 2, summ, f_fsum, col_w, fill=(40, 38, 34), leading=15)
    d.text((fx, ty + 2), src, font=f_src, fill=GREY)

# ---- medium-story illustrations ----
def ill_flags(x, y, w, h):
    d.rectangle([x, y, x + w // 2, y + h], fill=(1, 33, 105))
    d.rectangle([x + w // 2, y, x + w, y + h], fill=(0, 51, 153))
    d.rectangle([x + 4, y + h // 2 - 4, x + w // 2 - 4, y + h // 2 + 4], fill=(255, 255, 255))
    d.rectangle([x + w // 4 - 4, y + 4, x + w // 4 + 4, y + h - 4], fill=(255, 255, 255))
    d.rectangle([x + 4, y + h // 2 - 2, x + w // 2 - 4, y + h // 2 + 2], fill=(200, 16, 46))
    d.rectangle([x + w // 4 - 2, y + 4, x + w // 4 + 2, y + h - 4], fill=(200, 16, 46))
    import math
    for k in range(12):
        a = math.radians(k * 30)
        sx = x + w * 0.75 + int(14 * math.cos(a))
        sy = y + h / 2 + int(12 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 209, 0))


def ill_globe(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    cx, cy, r = x + w * 0.32, y + h / 2, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 120, 190))
    d.ellipse([cx - 12, cy - 12, cx - 2, cy - 2], fill=(74, 160, 90))
    d.ellipse([cx + 2, cy + 2, cx + 12, cy + 10], fill=(74, 160, 90))
    d.ellipse([cx - 4, cy + 8, cx + 6, cy + 16], fill=(74, 160, 90))
    # thermometer
    tx = x + w - 34
    d.rectangle([tx, y + 8, tx + 8, y + h - 16], outline=(178, 30, 26), width=2)
    d.ellipse([tx - 3, y + h - 20, tx + 11, y + h - 6], fill=(178, 30, 26))
    d.rectangle([tx + 2, y + 14, tx + 6, y + h - 22], fill=(178, 30, 26))
    d.text((x + w - 62, y + 4), "31", font=F(F_SANS_BLACK, 16), fill=(178, 30, 26))


def ill_missile(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 196, 140))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 120, 118))
    for i in range(5):
        d.line([(x + i * 38, y + h - 12), (x + i * 38 + 14, y + h - 12)], fill=(255, 255, 255), width=2)
    mx, my = x + w // 2, y + h // 2 - 4
    d.polygon([(mx - 62, my - 5), (mx + 40, my - 5), (mx + 58, my), (mx + 40, my + 5),
               (mx - 62, my + 5)], fill=(150, 152, 148))
    d.polygon([(mx - 62, my - 5), (mx - 48, my - 14), (mx - 40, my - 5)], fill=(120, 122, 118))
    d.polygon([(mx - 62, my + 5), (mx - 48, my + 14), (mx - 40, my + 5)], fill=(120, 122, 118))
    d.ellipse([mx + 48, my - 3, mx + 58, my + 3], fill=(255, 120, 60))


def ill_tanks(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 196, 150))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(150, 128, 84))
    for tx in (x + 18, x + 96):
        d.rectangle([tx, y + h - 26, tx + 58, y + h - 12], fill=(52, 84, 52))
        d.rectangle([tx + 14, y + h - 38, tx + 40, y + h - 26], fill=(44, 72, 44))
        d.rectangle([tx + 38, y + h - 34, tx + 62, y + h - 31], fill=(44, 72, 44))
    # palm
    px = x + w - 22
    d.line([(px, y + h - 10), (px, y + 8)], fill=(110, 82, 40), width=3)
    for a in (-50, -20, 10, 40):
        import math
        ex = px + int(16 * math.cos(math.radians(a - 90)))
        ey = y + 10 + int(10 * math.sin(math.radians(a - 90)))
        d.line([(px, y + 10), (ex, ey)], fill=(46, 110, 60), width=2)


def ill_crowd(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 214))
    import random
    rnd = random.Random(11)
    for i in range(9):
        cx = x + 14 + i * 19
        cy = y + h - 26
        d.ellipse([cx - 6, cy - 16, cx + 6, cy - 4], fill=(60, 58, 52))
        d.pieslice([cx - 11, cy - 4, cx + 11, cy + 16], 180, 360, fill=(60, 58, 52))
        if i % 3 == 0:
            d.rectangle([cx - 9, y + 8, cx + 9, y + 22], fill=(178, 30, 26))
            d.line([(cx, y + 22), (cx, cy - 14)], fill=(90, 88, 82), width=2)


def ill_bars(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    vals = [10, 14, 12, 20, 26, 34]
    bw = (w - 20) // 6
    for i, v in enumerate(vals):
        bx = x + 10 + i * bw
        d.rectangle([bx, y + h - 8 - v, bx + bw - 4, y + h - 8], fill=(178, 30, 26))
    d.line([(x + 8, y + h - 8), (x + w - 8, y + h - 8)], fill=INK, width=1)
    d.text((x + w - 52, y + 4), "+2.3%", font=F(F_SANS_BLACK, 13), fill=(178, 30, 26))


def ill_parliament(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 228, 230))
    d.polygon([(x + w // 2 - 52, y + 12), (x + w // 2 + 52, y + 12),
               (x + w // 2, y + 2)], fill=(120, 122, 124))
    d.rectangle([x + w // 2 - 52, y + 12, x + w // 2 + 52, y + h - 8], fill=(180, 182, 184))
    for i in range(5):
        cx = x + w // 2 - 44 + i * 22
        d.rectangle([cx, y + 16, cx + 7, y + h - 8], fill=(245, 245, 242))
    d.rectangle([x + w - 40, y + h - 22, x + w - 8, y + h - 14], fill=(110, 82, 40))
    d.rectangle([x + w - 30, y + h - 32, x + w - 18, y + h - 22], fill=(110, 82, 40))


def ill_rig(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(246, 214, 150))
    d.ellipse([x + w - 40, y + 6, x + w - 12, y + 34], fill=(255, 176, 40))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(196, 150, 84))
    dx = x + w // 2
    d.line([(dx - 34, y + h - 10), (dx, y + 8)], fill=(90, 70, 40), width=4)
    d.line([(dx + 34, y + h - 10), (dx, y + 8)], fill=(90, 70, 40), width=4)
    d.line([(dx - 22, y + h - 34), (dx + 22, y + h - 34)], fill=(90, 70, 40), width=3)
    d.line([(dx - 12, y + h - 52), (dx + 12, y + h - 52)], fill=(90, 70, 40), width=3)
    d.rectangle([dx - 6, y + h - 30, dx + 6, y + h - 10], fill=(60, 58, 52))


def ill_ballot(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 242))
    d.rectangle([x + w // 2 - 42, y + 16, x + w // 2 + 42, y + h - 8], fill=(24, 84, 160))
    d.rectangle([x + w // 2 - 30, y + 12, x + w // 2 + 30, y + 18], fill=(255, 255, 255))
    d.rectangle([x + w // 2 - 30, y + 2, x + w // 2 + 30, y + 12], fill=(255, 255, 255),
                outline=(150, 150, 148))
    d.line([(x + w // 2 - 16, y + 26), (x + w // 2 - 6, y + 38), (x + w // 2 + 18, y + 14)],
           fill=(255, 255, 255), width=3)
    d.rectangle([x + 6, y + 6, x + 30, y + 12], fill=(178, 30, 26))
    d.rectangle([x + 6, y + 14, x + 30, y + 20], fill=(255, 255, 255))


def ill_cricket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 160, 90))
    d.rectangle([x + w // 2 - 26, y + 6, x + w // 2 + 26, y + h - 6], fill=(214, 190, 140))
    for sx in (x + w // 2 - 18, x + w // 2, x + w // 2 + 18):
        d.rectangle([sx - 2, y + 8, sx + 2, y + 22], fill=(230, 220, 180))
    d.rectangle([x + w // 2 - 26, y + h - 30, x + w // 2 + 26, y + h - 24],
                fill=(120, 100, 60))
    # bat + ball
    d.polygon([(x + 24, y + 12), (x + 34, y + 10), (x + 44, y + 34), (x + 34, y + 38)],
              fill=(222, 190, 130))
    d.ellipse([x + w - 34, y + h - 26, x + w - 22, y + h - 14], fill=(178, 30, 26))
    d.rectangle([x + 6, y + 4, x + 52, y + 20], fill=(17, 17, 17))
    d.text((x + 10, y + 7), "118", font=F(F_SANS_BLACK, 12), fill=(255, 255, 255))


MEDIUM = [
    ("UK-EU DEAL", "Agreed \u00b7 Reuters", ill_flags,
     "4 \u00b7 BRUSSELS \u00b7 DIPLOMACY", "UK and EU seal a \u201creset\u201d deal",
     "Food trade, youth visas, carbon link."),
    ("COP31: NO DEAL", "Ongoing \u00b7 UN News", ill_globe,
     "5 \u00b7 ANTALYA \u00b7 CLIMATE", "COP31 reaches its last day with no deal",
     "The draft text leaves out fossil fuels."),
    ("POLAND: MISSILE", "Minister says \u00b7 Reuters", ill_missile,
     "6 \u00b7 EASTERN POLAND \u00b7 SECURITY", "Russian cruise missile lands in Poland",
     "It fell in a field; two airports paused."),
    ("IRAQ: ARMY IN", "Witnessed \u00b7 Reuters", ill_tanks,
     "7 \u00b7 CENTRAL IRAQ \u00b7 SECURITY", "Iraqi army enters a militia stronghold",
     "Troops deploy to Jurf al-Sakhar."),
    ("ITALY: STRIKE", "Reported \u00b7 Reuters", ill_crowd,
     "8 \u00b7 ITALY \u00b7 LABOUR", "General strike over Italy\u2019s budget",
     "Workers and students march."),
    ("JAPAN: +2.3%", "Official data \u00b7 Reuters", ill_bars,
     "9 \u00b7 TOKYO \u00b7 ECONOMY", "Japan\u2019s inflation picks up to 2.3%",
     "A December rate rise stays in view."),
    ("SEOUL: IMPEACH", "Party decision \u00b7 Korea Herald", ill_parliament,
     "10 \u00b7 SEOUL \u00b7 POLITICS", "Korea\u2019s ruling party to impeach top judge",
     "It follows an overturned conviction."),
    ("KENYA: OIL", "Ceremony held \u00b7 allAfrica", ill_rig,
     "11 \u00b7 TURKANA, KENYA \u00b7 ENERGY", "Kenya starts drilling its first oil",
     "First crude is due on 1 December."),
    ("BUKELE: 3RD BID", "Filed \u00b7 AP", ill_ballot,
     "12 \u00b7 SAN SALVADOR \u00b7 POLITICS", "Bukele files to run for a third term",
     "The vote is on 28 February 2027."),
    ("PHILLIPS: 118", "Scorecard \u00b7 ICC", ill_cricket,
     "13 \u00b7 WELLINGTON \u00b7 CRICKET", "Phillips hits 118 against India",
     "Hundreds in India in all three formats."),
]
f_mkick = F(F_SANS_BLACK, 11)
f_mhead = F(F_SERIF_BOLD, 13)
f_msum = F(F_SANS, 10)
f_mcap = F(F_SANS, 8)
cell_w = (RX - MX - 4 * 8) / 5
cell_h = 106
grid_y = 526
for idx, (kick, cap, draw_fn, tag, head, summ) in enumerate(MEDIUM):
    r, c = divmod(idx, 5)
    cx0 = MX + c * (cell_w + 8)
    cy0 = grid_y + r * (cell_h + 8)
    ih = 50
    draw_fn(int(cx0), int(cy0), int(cell_w), ih)
    kw = d.textlength(kick, font=f_mkick)
    d.rectangle([cx0, cy0, cx0 + kw + 10, cy0 + 17], fill=RED)
    d.text((cx0 + 5, cy0 + 3), kick, font=f_mkick, fill=(255, 255, 255))
    d.rectangle([cx0, cy0 + ih - 13, cx0 + cell_w, cy0 + ih], fill=(17, 17, 17))
    d.text((cx0 + 4, cy0 + ih - 11), cap, font=f_mcap, fill=(230, 226, 216))
    ty = cy0 + ih + 4
    d.text((cx0, ty), tag, font=f_tag, fill=RED)
    ty += 13
    ty = para(d, cx0, ty, head, f_mhead, cell_w, leading=15)
    para(d, cx0, ty, summ, f_msum, cell_w, fill=(40, 38, 34), leading=12)

# ---- bottom: map + also-list ----
f_sec = F(F_SANS_B, 12)
f_list_b = F(F_SANS_B, 9)
f_list = F(F_SANS, 9)
f_note = F(F_SANS_IT, 9) if False else F(F_SERIF_IT, 9)
bot_y = 752
d.text((MX, bot_y), "WHERE IT HAPPENED", font=f_sec, fill=INK)
d.text((MX + 316, bot_y), "ALSO ON FRIDAY 20 NOVEMBER \u2014 29 MORE STORIES",
       font=f_sec, fill=INK)
hrule(d, MX, RX, bot_y + 16, width=1)

map_x, map_y, map_w, map_h = MX, bot_y + 22, 300, 160
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(222, 228, 226),
            outline=(160, 158, 148))
LAND = (216, 192, 138)
d.polygon([(map_x + 10, map_y + 25), (map_x + 55, map_y + 12), (map_x + 95, map_y + 18),
           (map_x + 105, map_y + 35), (map_x + 90, map_y + 55), (map_x + 65, map_y + 68),
           (map_x + 35, map_y + 60), (map_x + 12, map_y + 42)], fill=LAND)
d.polygon([(map_x + 78, map_y + 88), (map_x + 105, map_y + 88), (map_x + 112, map_y + 112),
           (map_x + 95, map_y + 142), (map_x + 80, map_y + 118)], fill=LAND)
d.polygon([(map_x + 140, map_y + 18), (map_x + 172, map_y + 12), (map_x + 182, map_y + 28),
           (map_x + 162, map_y + 44), (map_x + 142, map_y + 38)], fill=LAND)
d.polygon([(map_x + 138, map_y + 52), (map_x + 172, map_y + 50), (map_x + 190, map_y + 68),
           (map_x + 176, map_y + 98), (map_x + 152, map_y + 94), (map_x + 140, map_y + 72)],
          fill=LAND)
d.polygon([(map_x + 182, map_y + 12), (map_x + 255, map_y + 8), (map_x + 288, map_y + 22),
           (map_x + 278, map_y + 52), (map_x + 238, map_y + 68), (map_x + 208, map_y + 48),
           (map_x + 188, map_y + 32)], fill=LAND)
d.polygon([(map_x + 245, map_y + 102), (map_x + 282, map_y + 100),
           (map_x + 288, map_y + 116), (map_x + 250, map_y + 120)], fill=LAND)
PINS = {1: (172, 30), 2: (245, 55), 3: (268, 42), 4: (148, 30), 5: (168, 40),
        6: (162, 22), 7: (195, 48), 8: (156, 38), 9: (282, 32), 10: (268, 28),
        11: (168, 78), 12: (48, 62), 13: (288, 128), 15: (188, 16), 18: (258, 30),
        22: (192, 44), 24: (150, 72), 25: (168, 82), 28: (28, 48), 29: (72, 38),
        32: (278, 118), 34: (238, 62), 36: (18, 52), 38: (198, 52), 40: (160, 28)}
f_pin = F(F_SANS_B, 7)
for num, (px, py) in PINS.items():
    d.ellipse([map_x + px - 6, map_y + py - 6, map_x + px + 6, map_y + py + 6],
              fill=RED, outline=(255, 255, 255))
    t = str(num)
    d.text((map_x + px - d.textlength(t, font=f_pin) / 2, map_y + py - 4),
           t, font=f_pin, fill=(255, 255, 255))
d.text((MX, map_y + map_h + 4),
       "Each number is the story with that number on this page.",
       font=f_note, fill=GREY)

ALSO = [
    (14, "Lviv", "Strike on a railway station kills two", "BBC"),
    (15, "Moscow", "Russia declares Estonia\u2019s border closed", "Reuters"),
    (16, "Berlin", "Pupils strike against military service", "Al Jazeera"),
    (17, "London", "General says UK runs cyber attacks abroad", "Sky News"),
    (18, "Beijing", "China holds its loan rates for an 18th month", "Xinhua"),
    (19, "Tokyo", "SoftBank shares fall more than 14% in a day", "Al Jazeera"),
    (20, "Seoul", "Kospi ends the week 7.9% lower", "Anadolu"),
    (21, "Ganjam", "209 mm of rain falls as Akvan crosses Odisha", "PTI"),
    (22, "Lebanon", "Israeli air strikes hit south and east", "Anadolu"),
    (23, "Yemen", "Houthis fire on a cargo ship off the coast", "UKMTO"),
    (24, "Abuja", "Court bars new evidence against Tinubu", "Channels TV"),
    (25, "Kampala", "Police told to enforce Ebola ban on rallies", "allAfrica"),
    (26, "Malawi", "Fuel crisis brings night-long petrol queues", "Al Jazeera"),
    (27, "Africa", "AFDB says 22 countries are in debt distress", "allAfrica"),
    (28, "Las Vegas", "Russell fastest in wet Grand Prix practice", "Autosport"),
    (29, "New York", "Nasdaq futures fall 1.6% before the bell", "24/7 Wall St"),
    (30, "Washington", "Democrats query law firm\u2019s free work", "Al Jazeera"),
    (31, "Wellington", "Nicholls makes 175 in a stand of 216", "ICC"),
    (32, "Sydney", "Shares fall 1.8% in the sell-off", "Reuters"),
    (33, "Antalya", "Panama asks COP31 to cap oil output", "Anadolu"),
    (34, "Colombo", "Sri Lanka lifts its rate to 7.75%", "Anadolu"),
    (35, "Turin", "ATP backs a plan to lift player pay past $350m", "Anadolu"),
    (36, "California", "5.0 quake near Pinnacles, no injuries", "USGS"),
    (37, "Washington", "Senate blocks Iran war-powers curb, 51\u201348", "AP"),
    (38, "Riyadh", "Houthi missiles hit Riyadh again", "Reuters"),
    (39, "New York", "Indian man jailed 19 years over murder plot", "AP"),
    (40, "Budapest", "Hungary lifts its veto on EU talks for Ukraine", "Reuters"),
    (41, "Wellington", "NZ court: pay equity reform broke rights", "RNZ"),
    (42, "Beijing", "China bars Bloomberg reporter from summit", "Bloomberg"),
]
list_x = MX + 316
list_y = bot_y + 22
col2_x = list_x + 330
for j, (num, place, text, src) in enumerate(ALSO):
    lx = list_x if j < 15 else col2_x
    ly = list_y + (j if j < 15 else j - 15) * 11
    head_txt = f"{num} {place} "
    d.text((lx, ly), head_txt, font=f_list_b, fill=INK)
    hw = d.textlength(head_txt, font=f_list_b)
    d.text((lx + hw, ly), f"{text} ({src})", font=f_list, fill=(40, 38, 34))

# ---- date check + footer ----
dc_y = 946
d.rectangle([MX, dc_y, RX, dc_y + 36], outline=RED, width=2)
f_dc = F(F_SANS_B, 11)
d.text((MX + 8, dc_y + 11), "DATE CHECK", font=f_dc, fill=RED)
f_dct = F(F_SANS, 10)
dc_text = ("Left out as Thursday 19 November\u2019s news: the World Court\u2019s ruling on "
           "Myanmar, the three-leader declaration in Shenzhen, Tonga\u2019s drought "
           "emergency and the migrant boat lost off Senegal. Not yet happened, so not "
           "shown: BepiColombo\u2019s entry into orbit round Mercury and any final COP31 text.")
para(d, MX + 96, dc_y + 5, dc_text, f_dct, RX - MX - 104, leading=12)

f_foot = F(F_SERIF_IT, 10)
d.text((MX, 990),
       "Every story here happened, or was first reported, on Friday 20 November 2026. "
       "Officials\u2019 counts are attributed.", font=f_foot, fill=GREY)
foot_r = "Sources named beside each story \u00b7 original drawings"
d.text((RX - d.textlength(foot_r, font=f_foot), 990), foot_r, font=f_foot, fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG")
print("saved", out, img.size, os.path.getsize(out), "bytes")
