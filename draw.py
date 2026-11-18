#!/usr/bin/env python3
"""Draw the entry image for make.fun competition news-image-20261117.

A newspaper front page summing up Tuesday 17 November 2026 in one image:
serif masthead with the date and a true story count, three hero stories
with map/flag illustrations, twelve mid stories with small illustrations
and category tags, a world-map panel, an "also on Tuesday" list, and a
sources footer. Every story carries a serial number 1-33 — a badge on its
panel, a number on its map marker, and a number before its also-on line —
so the list and the map cross-reference each other. Flat shapes and crisp text only, so the image stays
legible at small sizes and the PNG stays far under the 1 MiB limit.
Deterministic: same input, same bytes. Every story happened or was first
reported on Tuesday 17 November 2026; contested claims are marked as
claims.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

PAPER = (251, 248, 241)
NAVY = (16, 36, 62)
GOLD = (232, 185, 74)
RED = (179, 39, 30)
INK = (24, 24, 24)
GREY = (58, 58, 58)
WHITE = (255, 255, 255)
SKY = (191, 217, 232)
SEA = (46, 107, 138)

# Continent colours for the map dots and legend.
C_AMERICAS = (204, 51, 51)
C_EUROPE = (43, 106, 184)
C_MIDEAST = (232, 120, 40)
C_ASIA = (20, 130, 80)
C_AFRICA = (128, 60, 160)
C_OCEANIA = (0, 150, 170)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Wrap text to fit max_width, returning a list of lines."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centered(draw, y, text, fnt, fill, width=W):
    draw.text((width / 2, y), text, font=fnt, fill=fill, anchor="ma")


def starburst(draw, cx, cy, r_outer, r_inner, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def fit_font(draw, text, path, size, max_width):
    """Largest font size at or below `size` that fits the text in max_width."""
    while size > 10:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_width:
            return fnt
        size -= 1
    return font(path, 10)


def num_badge(draw, cx, cy, r, n, fill, size):
    """Numbered circle badge: continent colour, bold white number, ring."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
                 outline=WHITE, width=2)
    draw.text((cx, cy), str(n), font=font(BOLD, size), fill=WHITE,
              anchor="mm")


def virus(draw, cx, cy, r, spike, body, light):
    """A flat virus shape."""
    for i in range(10):
        a = 2 * math.pi * i / 10
        x1 = cx + (r - 4) * math.cos(a)
        y1 = cy + (r - 4) * math.sin(a)
        x2 = cx + (r + 10) * math.cos(a)
        y2 = cy + (r + 10) * math.sin(a)
        draw.line([x1, y1, x2, y2], fill=spike, width=3)
        draw.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=spike)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=body)
    draw.ellipse([cx - r + 8, cy - r + 6, cx - r + 20, cy - r + 18],
                 fill=light)


def flag(draw, x, y, w, h, kind):
    """Tiny US / China / Russia flag, w x h."""
    if kind == "us":
        draw.rectangle([x, y, x + w, y + h], fill=(179, 39, 30))
        for i in range(3):
            draw.rectangle([x, y + (2 * i + 1) * h / 7, x + w,
                            y + (2 * i + 2) * h / 7], fill=WHITE)
        draw.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=NAVY)
    elif kind == "cn":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        draw.ellipse([x + w * 0.15, y + h * 0.18, x + w * 0.42,
                      y + h * 0.45], fill=(255, 222, 0))
    else:  # ru
        draw.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
        draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3],
                       fill=(0, 57, 166))
        draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(179, 39, 30))


# ---------------------------------------------------------------------------
# Hero scenes (drawn to fit any w x h box)
# ---------------------------------------------------------------------------

def scene_bridge(draw, x, y, w, h):
    """Kerch Bridge: a road section falls into the strait."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h * 0.68, x + w, y + h], fill=SEA)
    for fx in (0.14, 0.80):
        px = x + w * fx
        draw.rectangle([px, y + h * 0.55, px + 12, y + h * 0.68],
                       fill=(90, 90, 90))
    # deck, left half intact
    draw.rectangle([x + 4, y + h * 0.46, x + w * 0.44, y + h * 0.56],
                   fill=(120, 120, 120))
    # deck, right half tilted down
    draw.polygon([(x + w * 0.54, y + h * 0.47), (x + w - 4, y + h * 0.56),
                  (x + w - 4, y + h * 0.66), (x + w * 0.54, y + h * 0.57)],
                 fill=(120, 120, 120))
    # fallen section in the water
    draw.polygon([(x + w * 0.47, y + h * 0.70), (x + w * 0.62, y + h * 0.70),
                  (x + w * 0.61, y + h * 0.82), (x + w * 0.48, y + h * 0.82)],
                 fill=(90, 90, 90))
    # smoke puffs over the gap
    for fx, fy, r in ((0.48, 0.34, 10), (0.53, 0.26, 13), (0.58, 0.35, 9)):
        cx, cy = x + w * fx, y + h * fy
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))


def scene_strikes(draw, x, y, w, h):
    """US jets strike a missile site on Qeshm Island; Iran drones hit a US
    radar in Bahrain."""
    draw.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
    draw.rectangle([x, y + h * 0.70, x + w, y + h], fill=SEA)
    draw.polygon([(x + w * 0.06, y + h * 0.70), (x + w * 0.30, y + h * 0.42),
                  (x + w * 0.62, y + h * 0.46), (x + w * 0.86, y + h * 0.70)],
                 fill=(74, 94, 58))
    starburst(draw, x + w * 0.42, y + h * 0.44, 20, 9, 8, fill=GOLD)
    starburst(draw, x + w * 0.42, y + h * 0.44, 11, 5, 8, fill=(232, 120, 40))
    draw.arc([x + w * 0.08, y + h * 0.06, x + w * 0.44, y + h * 0.62],
             200, 330, fill=WHITE, width=3)
    draw.arc([x + w * 0.56, y + h * 0.02, x + w * 0.94, y + h * 0.58],
             210, 340, fill=WHITE, width=3)
    # a small drone top right
    dx, dy = x + w * 0.88, y + h * 0.24
    draw.rectangle([dx - 11, dy - 3, dx + 11, dy + 3], fill=WHITE)
    draw.line([dx - 16, dy - 8, dx + 16, dy - 8], fill=WHITE, width=2)
    draw.line([dx - 16, dy + 10, dx + 16, dy + 10], fill=WHITE, width=2)
    for rx in (dx - 16, dx + 16):
        draw.ellipse([rx - 3, dy - 11, rx + 3, dy - 5], fill=WHITE)
        draw.ellipse([rx - 3, dy + 7, rx + 3, dy + 13], fill=WHITE)


def scene_asia(draw, x, y, w, h):
    """Shenzhen skyline under the sun for the APEC talks."""
    draw.rectangle([x, y, x + w, y + h], fill=(242, 193, 78))
    draw.ellipse([x + w - 52, y + 6, x + w - 12, y + 46], fill=(232, 120, 40))
    base = y + h
    towers = [(0.01, 0.62), (0.14, 0.86), (0.27, 0.68), (0.40, 0.96),
              (0.53, 0.74), (0.66, 0.88), (0.79, 0.64), (0.90, 0.82)]
    for fx, fh in towers:
        tx = x + w * fx
        draw.rectangle([tx, base - h * fh, tx + w * 0.105, base], fill=NAVY)
    for fx, fh in towers:
        tx = x + w * fx
        for wy in range(int(base - h * fh + 8), int(base - 10), 13):
            draw.rectangle([tx + 5, wy, tx + 11, wy + 5], fill=GOLD)
            draw.rectangle([tx + 20, wy, tx + 26, wy + 5], fill=GOLD)
    # summit flags on three towers (US, China, Russia)
    for fx, fh, kind in ((0.27, 0.68, "us"), (0.53, 0.74, "cn"),
                         (0.79, 0.64, "ru")):
        top = base - h * fh
        pole_x = x + w * fx + w * 0.05
        draw.line([pole_x, top - 20, pole_x, top], fill=NAVY, width=2)
        flag(draw, pole_x + 2, top - 20, 22, 13, kind)


# ---------------------------------------------------------------------------
# Mid-panel mini scenes (drawn into a small strip, w x h)
# ---------------------------------------------------------------------------

def mini_virus_bg(draw, x, y, w, h, bg, spike, body, light):
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    virus(draw, x + w * 0.28, y + h * 0.52, 11, spike, body, light)
    virus(draw, x + w * 0.68, y + h * 0.48, 8, spike, body, light)
    virus(draw, x + w * 0.88, y + h * 0.62, 5, spike, body, light)


def mini_ebola(draw, x, y, w, h):
    mini_virus_bg(draw, x, y, w, h, (122, 31, 31), (232, 120, 40),
                  (192, 57, 43), (220, 110, 90))


def mini_measles(draw, x, y, w, h):
    mini_virus_bg(draw, x, y, w, h, (14, 90, 96), (140, 220, 210),
                  (24, 140, 150), (120, 200, 200))
    draw.rectangle([x + w * 0.44, y + 6, x + w * 0.44 + 5, y + h - 6],
                   fill=WHITE)
    draw.rectangle([x + w * 0.44 - 5, y + h // 2 - 2, x + w * 0.44 + 10,
                    y + h // 2 + 3], fill=WHITE)


def mini_chip(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(14, 122, 61))
    cx, cy = x + w // 2, y + h // 2
    draw.rectangle([cx - 52, cy - 13, cx + 52, cy + 13], fill=NAVY)
    for i in range(5):
        px = cx - 44 + i * 18
        draw.rectangle([px, cy - 17, px + 7, cy - 13], fill=(200, 200, 200))
        draw.rectangle([px, cy + 13, px + 7, cy + 17], fill=(200, 200, 200))
    draw.text((cx, cy), "$115B", font=font(BOLD, 15), fill=WHITE, anchor="mm")


def mini_mountains(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(221, 235, 242))
    draw.polygon([(x + 4, y + h), (x + w * 0.32, y + 4),
                  (x + w * 0.62, y + h)], fill=(44, 92, 110))
    draw.polygon([(x + w * 0.45, y + h), (x + w * 0.72, y + 10),
                  (x + w - 4, y + h)], fill=(27, 58, 92))
    draw.rectangle([x, y + h - 8, x + w, y + h], fill=SEA)
    draw.rectangle([x, y + h - 15, x + w, y + h - 11], fill=(70, 140, 175))


def mini_gaza(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(233, 220, 186))
    # road at the bottom
    draw.rectangle([x, y + h - 9, x + w, y + h], fill=(120, 120, 120))
    # border wall with a gate gap in the middle
    draw.rectangle([x + 6, y + 4, x + w * 0.40, y + h - 9],
                   fill=(150, 150, 150))
    draw.rectangle([x + w * 0.60, y + 4, x + w - 6, y + h - 9],
                   fill=(150, 150, 150))
    # aid truck passing through the gate
    tx, ty = x + w * 0.44, y + h - 22
    draw.rectangle([tx, ty, tx + 16, ty + 12], fill=WHITE)
    draw.rectangle([tx + 16, ty + 4, tx + 24, ty + 12], fill=(179, 39, 30))
    draw.rectangle([tx + 7, ty + 1, tx + 9, ty + 11], fill=RED)
    draw.rectangle([tx + 4, ty + 4, tx + 12, ty + 8], fill=RED)
    draw.ellipse([tx + 2, ty + 12, tx + 7, ty + 17], fill=INK)
    draw.ellipse([tx + 17, ty + 12, tx + 22, ty + 17], fill=INK)


def mini_parliament(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(233, 228, 210))
    draw.polygon([(x + w * 0.30, y + 6), (x + w * 0.50, y + 2),
                  (x + w * 0.70, y + 6)], fill=(90, 90, 90))
    draw.rectangle([x + w * 0.30, y + 6, x + w * 0.70, y + h - 6],
                   fill=(180, 175, 160))
    for fx in (0.34, 0.47, 0.60):
        draw.rectangle([x + w * fx, y + 10, x + w * fx + 6, y + h - 8],
                       fill=(251, 248, 241))
    # flag on top
    draw.line([x + w * 0.50, y - 8, x + w * 0.50, y + 2], fill=INK, width=2)
    draw.rectangle([x + w * 0.50 + 2, y - 8, x + w * 0.50 + 16, y - 1],
                   fill=(204, 51, 51))


def mini_jet(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(158, 196, 224))
    draw.ellipse([x + w - 30, y + 4, x + w - 8, y + 26], fill=(232, 120, 40))
    # jet silhouette
    cx, cy = x + w * 0.42, y + h * 0.55
    draw.polygon([(cx - 34, cy), (cx + 26, cy - 7), (cx + 40, cy),
                  (cx + 26, cy + 7)], fill=NAVY)
    draw.polygon([(cx - 8, cy - 4), (cx + 2, cy - 16), (cx + 8, cy - 4)],
                 fill=NAVY)
    draw.polygon([(cx - 8, cy + 4), (cx + 2, cy + 15), (cx + 8, cy + 4)],
                 fill=NAVY)
    draw.line([cx - 34, cy, cx - 46, cy], fill=WHITE, width=2)


def mini_crash(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(176, 190, 200))
    draw.polygon([(x + 4, y + h), (x + w * 0.30, y + h - 14),
                  (x + w * 0.60, y + h)], fill=(240, 244, 246))
    # tilted plane falling
    cx, cy = x + w * 0.60, y + h * 0.42
    draw.polygon([(cx - 26, cy + 8), (cx + 22, cy - 10), (cx + 30, cy - 4),
                  (cx - 18, cy + 14)], fill=(60, 60, 60))
    for fx, fy, r in ((0.74, 0.30, 6), (0.79, 0.22, 8), (0.84, 0.32, 5)):
        px, py = x + w * fx, y + h * fy
        draw.ellipse([px - r, py - r, px + r, py + r], fill=(120, 120, 120))


def mini_court(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(233, 228, 210))
    draw.polygon([(x + w * 0.28, y + 8), (x + w * 0.50, y + 2),
                  (x + w * 0.72, y + 8)], fill=(90, 90, 90))
    draw.rectangle([x + w * 0.30, y + 8, x + w * 0.70, y + h - 6],
                   fill=(200, 196, 182))
    for fx in (0.34, 0.47, 0.60):
        draw.rectangle([x + w * fx, y + 12, x + w * fx + 6, y + h - 8],
                       fill=(251, 248, 241))
    # gavel
    draw.rectangle([x + w * 0.80, y + h - 12, x + w * 0.86, y + h - 4],
                   fill=(90, 60, 30))
    draw.rectangle([x + w * 0.78, y + h - 18, x + w * 0.88, y + h - 12],
                   fill=(90, 60, 30))


def mini_desert(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 214, 160))
    draw.ellipse([x + w - 34, y + 3, x + w - 12, y + 25], fill=(232, 185, 74))
    draw.polygon([(x, y + h), (x + w * 0.35, y + h * 0.45),
                  (x + w * 0.70, y + h)], fill=(214, 178, 110))
    draw.polygon([(x + w * 0.55, y + h), (x + w * 0.85, y + h * 0.55),
                  (x + w, y + h)], fill=(196, 158, 92))
    # flag on a pole
    draw.line([x + w * 0.16, y + 6, x + w * 0.16, y + h - 8], fill=INK, width=2)
    draw.rectangle([x + w * 0.16 + 2, y + 6, x + w * 0.16 + 18, y + 14],
                   fill=(204, 51, 51))


def mini_crowd(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(220, 226, 232))
    # placard
    draw.rectangle([x + w * 0.42, y + 4, x + w * 0.62, y + 16],
                   fill=WHITE, outline=INK, width=1)
    draw.line([x + w * 0.52, y + 16, x + w * 0.52, y + h - 10], fill=INK,
              width=2)
    # crowd dots
    for i, fx in enumerate((0.12, 0.24, 0.36, 0.66, 0.78, 0.90)):
        cy = y + h - 10 - (4 if i % 2 else 0)
        draw.ellipse([x + w * fx - 5, cy - 5, x + w * fx + 5, cy + 5],
                     fill=NAVY)
        draw.ellipse([x + w * fx - 3, cy - 12, x + w * fx + 3, cy - 6],
                     fill=NAVY)


def mini_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(191, 217, 232))
    draw.rectangle([x, y + h * 0.68, x + w, y + h], fill=SEA)
    draw.rectangle([x + 6, y + h * 0.40, x + w * 0.48, y + h * 0.50],
                   fill=(120, 120, 120))
    draw.polygon([(x + w * 0.56, y + h * 0.42), (x + w - 6, y + h * 0.52),
                  (x + w - 6, y + h * 0.62), (x + w * 0.56, y + h * 0.52)],
                 fill=(120, 120, 120))
    for fx, fy, r in ((0.52, 0.30, 6), (0.57, 0.22, 8)):
        px, py = x + w * fx, y + h * fy
        draw.ellipse([px - r, py - r, px + r, py + r], fill=(150, 150, 150))


# ---------------------------------------------------------------------------
# World map (simplified continents in a 446 x 220 box)
# ---------------------------------------------------------------------------

CONTINENTS = [
    # North America
    [(30, 26), (66, 16), (116, 22), (130, 44), (116, 66), (94, 82),
     (68, 88), (46, 74), (26, 54)],
    # Greenland
    [(126, 8), (148, 6), (150, 20), (130, 22)],
    # South America
    [(106, 114), (136, 108), (150, 124), (144, 154), (126, 192),
     (112, 172), (102, 142)],
    # Europe
    [(210, 36), (242, 28), (256, 42), (248, 60), (226, 64), (210, 54)],
    # Africa
    [(214, 80), (250, 76), (270, 92), (266, 124), (248, 160), (228, 146),
     (212, 112)],
    # Asia
    [(260, 24), (328, 16), (398, 22), (426, 42), (418, 72), (390, 86),
     (358, 94), (328, 80), (298, 90), (270, 74), (256, 50)],
    # SE Asia islands
    [(358, 104), (382, 100), (388, 114), (364, 118)],
    # Australia
    [(370, 154), (412, 148), (426, 164), (410, 182), (376, 178)],
]

# Story locations on the map (x, y in the 446 x 220 box, continent colour,
# story number 1-33). Positions are approximate for the stylised map and
# spread just enough to keep the numbered circles from touching.
MAP_MARKERS = [
    (272, 50, C_EUROPE, 1),    # Kerch Bridge
    (292, 77, C_MIDEAST, 2),   # Qeshm Island
    (373, 92, C_ASIA, 3),      # Manila
    (246, 110, C_AFRICA, 4),   # DR Congo
    (78, 72, C_AMERICAS, 5),   # Nvidia, California
    (327, 76, C_ASIA, 6),      # Nepal
    (260, 66, C_MIDEAST, 7),   # Gaza
    (354, 52, C_ASIA, 8),      # Mongolia
    (395, 66, C_ASIA, 9),      # Japan
    (114, 78, C_AMERICAS, 10), # US measles
    (353, 34, C_EUROPE, 11),   # Siberia crash
    (222, 42, C_EUROPE, 12),   # Paris
    (282, 96, C_MIDEAST, 13),  # Yemen
    (200, 44, C_EUROPE, 14),   # France strikes
    (258, 38, C_EUROPE, 15),   # Kyiv
    (244, 58, C_EUROPE, 16),   # Moldova
    (252, 82, C_MIDEAST, 17),  # West Bank
    (190, 26, C_EUROPE, 18),   # UK
    (302, 58, C_MIDEAST, 19),  # Iran
    (272, 80, C_MIDEAST, 20),  # Gaza airstrikes
    (300, 22, C_EUROPE, 21),   # Russia
    (212, 62, C_EUROPE, 22),   # France covert op
    (104, 58, C_AMERICAS, 23), # Trump, US
    (100, 90, C_AMERICAS, 24), # Cuba
    (336, 44, C_ASIA, 25),     # China–Canada
    (352, 96, C_ASIA, 26),     # Thailand
    (312, 90, C_ASIA, 27),     # India
    (264, 122, C_AFRICA, 28),  # Kenya
    (112, 140, C_AMERICAS, 29),  # Peru
    (58, 58, C_AMERICAS, 30),  # Apple, California
    (132, 54, C_AMERICAS, 31), # US Congress
    (372, 62, C_ASIA, 32),     # China electric plane
    (304, 94, C_MIDEAST, 33),  # Oil, Gulf
]

LEGEND = [
    ("Americas", C_AMERICAS),
    ("Europe", C_EUROPE),
    ("Middle East", C_MIDEAST),
    ("Asia", C_ASIA),
    ("Africa", C_AFRICA),
    ("Oceania", C_OCEANIA),
]


# ---------------------------------------------------------------------------
# Stories
# ---------------------------------------------------------------------------

HEROES = [
    ("EUROPE · UKRAINE WAR",
     "Ukraine hits Kerch Bridge again",
     "Ukrainian drones hit the bridge for a second day; a road section "
     "fell into the strait, cutting a key supply route to Crimea.",
     scene_bridge),
    ("MIDDLE EAST · IRAN WAR",
     "US strikes Iran after drone attacks",
     "US jets hit a missile site on Qeshm Island after Iran fired drones "
     "at a US radar in Bahrain — its third attack there in five days.",
     scene_strikes),
    ("ASIA · DIPLOMACY",
     "Trump heads to Asia for APEC talks",
     "Trump starts in Manila for the ASEAN–US summit, then heads to "
     "Shenzhen for APEC talks with China's Xi and Russia's Putin.",
     scene_asia),
]

MIDS = [
    ("AFRICA · HEALTH", "EBOLA IN DR CONGO",
     "Outbreak passes 11,000 cases and 5,400 deaths", mini_ebola),
    ("BUSINESS", "NVIDIA: $115 BILLION",
     "Record $115B sales, yet ousted CEO Huang will not return", mini_chip),
    ("ASIA · CLIMATE", "NEPAL FIRST",
     "First UN loss-and-damage funds set aside after floods", mini_mountains),
    ("MIDDLE EAST · GAZA", "GAZA AID AT RISK",
     "UK, Australia, Canada, Italy urge Israel to open crossings",
     mini_gaza),
    ("ASIA · POLITICS", "MONGOLIA PRESIDENT RESIGNS",
     "President Khürelsükh quits amid a corruption scandal", mini_parliament),
    ("ASIA · SECURITY", "JAPAN SCRAMBLES JETS",
     "Russian aircraft violate Japanese airspace", mini_jet),
    ("AMERICAS · HEALTH", "MEASLES STATUS LOST",
     "US, Mexico, Bolivia lose status; 5,400+ US cases", mini_measles),
    ("RUSSIA · AIR CRASH", "PLANE CRASH KILLS 19",
     "Military plane crashes in Siberia; all on board die", mini_crash),
    ("EUROPE · JUSTICE", "DEPARDIEU PLEADS GUILTY",
     "French actor admits assault charge, drops appeal", mini_court),
    ("MIDDLE EAST · YEMEN", "HOUTHI ADVANCE",
     "Government troops retreat from Red Sea coast", mini_desert),
    ("EUROPE · LABOUR", "FRANCE STRIKES AGAIN",
     "Second nationwide strike over pay and conditions", mini_crowd),
    ("EUROPE · UKRAINE WAR", "KYIV BRIDGES HIT",
     "Russian strikes hit two bridges, disrupting water and power", mini_kyiv),
]

ALSO_ON = [
    "Moldova: drone claim by president Sandu.",
    "West Bank: settlers kill woman, 72.",
    "UK: sanctions settlement firms.",
    "Iran: blocks IAEA inspectors for now.",
    "Gaza: airstrikes go on despite truce.",
    "Russia: record drone kills claimed.",
    "France: covert Ukraine op revealed.",
    'Trump: US "looking into" bomb report.',
    "Cuba: fuel crisis aids US exports.",
    "China–Canada: more tariff cuts agreed.",
    "Thailand: to scrap tariffs on US goods.",
    "India: Cyclone Alvan, Odisha evacuates.",
    "Kenya: WFP aids 30,000 who fled.",
    "Pope Leo: hit by object in Peru.",
    "Apple: iCloud, Pay, App Store outage.",
    "US: Huang to testify before Congress.",
    "China: tests 250-mile electric plane.",
    "Oil: prices slide on glut fears.",
]

STORY_COUNT = len(HEROES) + len(MIDS) + len(ALSO_ON)  # 33

# Number colours: the badge/marker/list number of each story takes its
# continent colour, so the number cross-references the map legend.
HERO_COLORS = [C_EUROPE, C_MIDEAST, C_ASIA]
MID_COLORS = [C_AFRICA, C_AMERICAS, C_ASIA, C_MIDEAST, C_ASIA, C_ASIA,
              C_AMERICAS, C_EUROPE, C_EUROPE, C_MIDEAST, C_EUROPE, C_EUROPE]
ALSO_COLORS = [C_EUROPE, C_MIDEAST, C_EUROPE, C_MIDEAST, C_MIDEAST, C_EUROPE,
               C_EUROPE, C_AMERICAS, C_AMERICAS, C_ASIA, C_ASIA, C_ASIA,
               C_AFRICA, C_AMERICAS, C_AMERICAS, C_AMERICAS, C_ASIA, C_MIDEAST]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 84], fill=NAVY)
    centered(d, 6, "THE WORLD'S NEWS IN ONE PICTURE", font(BOLD, 18), GOLD)
    centered(d, 26, "Tuesday 17 November 2026", font(SERIF, 50), WHITE)
    d.rectangle([0, 84, W, 88], fill=RED)
    centered(d, 92, "%d STORIES · 6 CONTINENTS · ALL FROM TUESDAY"
             % STORY_COUNT, font(BOLD, 19), NAVY)

    # ---- Hero row: 3 panels ----
    margin, gap = 10, 8
    hw = (W - 2 * margin - 2 * gap) // 3  # 328
    hy, hh = 116, 200
    for i, (tag, title, caption, scene) in enumerate(HEROES):
        px = margin + i * (hw + gap)
        d.rectangle([px, hy, px + hw, hy + hh], fill=WHITE,
                    outline=INK, width=2)
        scene(d, px + 2, hy + 2, hw - 4, 92)
        num_badge(d, px + 20, hy + 20, 17, i + 1, HERO_COLORS[i], 17)
        d.text((px + 10, hy + 98), tag, font=font(BOLD, 11), fill=RED)
        lines = wrap(d, title, font(BOLD, 18), hw - 20)
        ly = hy + 114
        for line in lines[:2]:
            d.text((px + 10, ly), line, font=font(BOLD, 18), fill=NAVY)
            ly += 21
        clines = wrap(d, caption, font(REG, 12), hw - 20)
        ly = hy + 156
        for line in clines[:3]:
            d.text((px + 10, ly), line, font=font(REG, 12), fill=GREY)
            ly += 13

    # ---- Mid grid: 4 columns x 3 rows ----
    mw = (W - 2 * margin - 3 * gap) // 4  # 244
    mh = 124
    my0 = 324
    for i, (tag, title, caption, scene) in enumerate(MIDS):
        col, row = i % 4, i // 4
        px = margin + col * (mw + gap)
        py = my0 + row * (mh + gap)
        d.rectangle([px, py, px + mw, py + mh], fill=WHITE,
                    outline=INK, width=2)
        scene(d, px + 2, py + 2, mw - 4, 40)
        num_badge(d, px + 16, py + 16, 13, i + 4, MID_COLORS[i], 13)
        d.text((px + 10, py + 46), tag, font=font(BOLD, 10), fill=RED)
        tfont = fit_font(d, title, BOLD, 15, mw - 20)
        lines = wrap(d, title, tfont, mw - 20)
        ly = py + 60
        for line in lines[:2]:
            d.text((px + 10, ly), line, font=tfont, fill=NAVY)
            ly += 18
        clines = wrap(d, caption, font(REG, 11), mw - 20)
        ly = py + 98
        for line in clines[:2]:
            d.text((px + 10, ly), line, font=font(REG, 11), fill=GREY)
            ly += 13

    # ---- Bottom band: world map (left) + also-on list (right) ----
    by = 720
    # Map panel
    mx, mw2 = margin, 450
    d.rectangle([mx, by, mx + mw2, by + 250], fill=WHITE,
                outline=INK, width=2)
    d.text((mx + 10, by + 6), "WHERE IT HAPPENED",
           font=font(BOLD, 15), fill=NAVY)
    map_x, map_y = mx + 2, by + 28
    d.rectangle([map_x, map_y, map_x + 446, map_y + 176], fill=(226, 238, 244))
    # the 446 x 220 map is scaled uniformly (0.8x) to fit the shorter panel
    ms = 176 / 220
    ox = (446 - 446 * ms) / 2
    for poly in CONTINENTS:
        d.polygon([(map_x + ox + px * ms, map_y + py * ms)
                   for px, py in poly],
                  fill=(170, 196, 168), outline=(120, 150, 125))
    for dx, dy, col, n in MAP_MARKERS:
        cx, cy = map_x + ox + dx * ms, map_y + dy * ms
        num_badge(d, cx, cy, 7, n, col, 11 if n < 10 else 9)
    # legend: 2 rows x 3 columns
    ly = by + 210
    for i, (name, col) in enumerate(LEGEND):
        lx = mx + 12 + (i % 3) * 148
        ly2 = ly + (i // 3) * 18
        d.ellipse([lx, ly2 + 2, lx + 9, ly2 + 11], fill=col)
        d.text((lx + 13, ly2), name, font=font(REG, 11), fill=INK)

    # Also-on list
    ax = mx + mw2 + gap  # 468
    aw = W - margin - ax  # 546
    d.text((ax, by + 6), "ALSO ON TUESDAY 17 NOVEMBER",
           font=font(BOLD, 15), fill=NAVY)
    d.line([ax, by + 28, ax + aw, by + 28], fill=INK, width=1)
    col_w = (aw - gap) // 2  # 269
    half = (len(ALSO_ON) + 1) // 2  # 15 per column
    for ci in range(2):
        cx = ax + ci * (col_w + gap)
        for j, line in enumerate(ALSO_ON[ci * half:(ci + 1) * half]):
            n = 16 + ci * half + j
            num = "%d." % n
            nfnt = font(BOLD, 12)
            nw = d.textlength(num, font=nfnt)
            fnt = fit_font(d, line, REG, 12, col_w - nw - 6)
            d.text((cx, by + 36 + j * 23), num, font=nfnt,
                   fill=ALSO_COLORS[n - 16])
            d.text((cx + nw + 6, by + 36 + j * 23), line, font=fnt, fill=INK)

    # ---- Footer ----
    d.rectangle([0, 976, W, H], fill=NAVY)
    centered(d, 982, "Every story here happened or was first reported on "
             "Tuesday 17 November 2026. Contested claims are marked as "
             "claims.", font(REG, 13), WHITE)
    centered(d, 1002, "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. "
             "Original drawings. — Tuesday, 17 November 2026",
             font(REG, 12), GOLD)

    img.save("entry.png", format="PNG")
    print("saved entry.png, stories:", STORY_COUNT)


if __name__ == "__main__":
    main()
