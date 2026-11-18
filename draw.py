#!/usr/bin/env python3
"""Draw the entry image for make.fun competition news-image-20261117.

A newspaper front page summing up Tuesday 17 November 2026 in one image:
serif masthead with the date and a true story count, three hero stories
with map/flag illustrations and geographic labels, sixteen mid stories
with small illustrations and category tags, a by-the-numbers strip, a
world map drawn from real longitude/latitude outlines with a Europe &
Middle East zoom inset, an "also on Tuesday" list, and a sources footer.
Every story carries a serial number 1-40 — a badge on its panel, a number
on its map marker, and a number before its also-on line — so the list and
the map cross-reference each other. Flat shapes and crisp text only, so
the image stays legible at small sizes and the PNG stays far under the
1 MiB limit. Deterministic: same input, same bytes. Every story happened
or was first reported on Tuesday 17 November 2026; contested claims are
marked as claims.
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


def geo_chip(draw, x, y, text, fill=NAVY, fg=WHITE, size=11):
    """Small solid chip with a geographic label, top-left at (x, y)."""
    fnt = font(BOLD, size)
    w = draw.textlength(text, font=fnt) + 14
    h = size + 10
    draw.rectangle([x, y, x + w, y + h], fill=fill)
    draw.text((x + 7, y + 5), text, font=fnt, fill=fg)


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
    # geographic label
    geo_chip(draw, x + w - 78, y + 6, "CRIMEA")


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
    # geographic label, centred at the bottom over the sea
    label = "BAHRAIN · QESHM · HORMUZ"
    lfnt = font(BOLD, 11)
    lw = draw.textlength(label, font=lfnt) + 14
    geo_chip(draw, x + (w - lw) / 2, y + h - 26, label, fill=WHITE,
             fg=NAVY)


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
    # geographic label, centred on the sky
    label = "MANILA"
    lfnt = font(BOLD, 11)
    lw = draw.textlength(label, font=lfnt) + 14
    geo_chip(draw, x + (w - lw) / 2, y + 6, label)


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


def mini_serbia(draw, x, y, w, h):
    """Belgrade parliament with a ballot box: the Student List takes over."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 228, 210))
    draw.polygon([(x + w * 0.28, y + 2), (x + w * 0.50, y + 1),
                  (x + w * 0.72, y + 2)], fill=(90, 90, 90))
    draw.rectangle([x + w * 0.28, y + 2, x + w * 0.72, y + h - 2],
                   fill=(180, 175, 160))
    for fx in (0.32, 0.45, 0.58):
        draw.rectangle([x + w * fx, y + 6, x + w * fx + 6, y + h - 4],
                       fill=(251, 248, 241))
    # ballot box in front
    bx, by = x + w * 0.80, y + h - 13
    draw.rectangle([bx, by, bx + 12, by + 9], fill=NAVY)
    draw.rectangle([bx + 2, by - 3, bx + 10, by], fill=NAVY)
    draw.line([bx + 6, by - 8, bx + 6, by - 3], fill=WHITE, width=2)


def mini_bangladesh(draw, x, y, w, h):
    """Garment factory with tear-gas puffs and workers."""
    draw.rectangle([x, y, x + w, y + h], fill=(200, 205, 210))
    draw.rectangle([x + w * 0.08, y + h * 0.42, x + w * 0.52, y + h - 2],
                   fill=(120, 120, 120))
    draw.rectangle([x + w * 0.14, y + 3, x + w * 0.20, y + h * 0.42],
                   fill=(90, 90, 90))
    draw.rectangle([x + w * 0.28, y + 6, x + w * 0.34, y + h * 0.42],
                   fill=(90, 90, 90))
    # tear-gas puffs
    for fx, fy, r in ((0.66, 0.38, 6), (0.78, 0.28, 7), (0.88, 0.42, 5)):
        cx, cy = x + w * fx, y + h * fy
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 240, 240))
    # workers below the gas
    for fx in (0.66, 0.78, 0.90):
        cx = x + w * fx
        draw.ellipse([cx - 4, y + h - 12, cx + 4, y + h - 4], fill=NAVY)


def mini_prison(draw, x, y, w, h):
    """Prison bars with a figure behind them: a leader on trial."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 228, 210))
    # figure silhouette
    cx, cy = x + w * 0.50, y + h * 0.58
    draw.ellipse([cx - 6, cy - 8, cx + 6, cy + 4], fill=NAVY)
    draw.polygon([(cx - 9, cy + 4), (cx + 9, cy + 4), (cx + 7, y + h - 2),
                  (cx - 7, y + h - 2)], fill=NAVY)
    # vertical bars in front
    for fx in (0.18, 0.36, 0.54, 0.72, 0.90):
        draw.rectangle([x + w * fx - 2, y + 2, x + w * fx + 2, y + h - 2],
                       fill=(60, 60, 60))


def mini_bank(draw, x, y, w, h):
    """Bank facade with columns and a falling red line."""
    draw.rectangle([x, y, x + w, y + h], fill=(221, 235, 242))
    draw.polygon([(x + w * 0.30, y + 2), (x + w * 0.50, y + 1),
                  (x + w * 0.70, y + 2)], fill=(90, 90, 90))
    draw.rectangle([x + w * 0.30, y + 2, x + w * 0.70, y + h - 2],
                   fill=(44, 92, 110))
    for fx in (0.34, 0.47, 0.60):
        draw.rectangle([x + w * fx, y + 6, x + w * fx + 6, y + h - 4],
                       fill=(251, 248, 241))
    # falling line across the facade
    draw.line([x + w * 0.78, y + 4, x + w * 0.97, y + h - 6], fill=RED,
              width=3)
    draw.polygon([(x + w * 0.97, y + h - 6), (x + w * 0.90, y + h - 8),
                  (x + w * 0.94, y + h - 14)], fill=RED)


# ---------------------------------------------------------------------------
# World map: continents as (longitude, latitude) outlines, drawn through an
# equirectangular projection into a 446 x 220 box (lon -180..180,
# lat 75..-60). Hand-written outlines, checked against real geography:
# Alaska bulge, Hudson Bay notch, Mexico taper, Brazil bulge, Africa's
# west bulge and Gulf of Guinea notch, India peninsula, Arabia, SE Asia.
# ---------------------------------------------------------------------------

def ll_to_map(lon, lat):
    """Equirectangular projection into the 446 x 220 map box."""
    return ((lon + 180.0) / 360.0 * 446.0, (75.0 - lat) / 135.0 * 220.0)


CONTINENTS_LL = [
    # North America
    [(-168, 66), (-155, 60), (-140, 60), (-128, 50), (-124, 40),
     (-122.5, 38), (-120, 35), (-117, 32), (-109, 23), (-97, 16),
     (-88, 13), (-80, 9), (-83, 16),
     (-81, 25), (-76, 34), (-70, 42), (-64, 44), (-55, 47), (-62, 55),
     (-68, 58), (-78, 56), (-85, 60), (-92, 63), (-100, 67), (-115, 69),
     (-130, 70), (-150, 71), (-165, 68)],
    # Greenland
    [(-45, 60), (-40, 64), (-30, 68), (-22, 70), (-20, 76), (-28, 80),
     (-40, 80), (-52, 76), (-55, 70), (-52, 64)],
    # South America
    [(-79, 9), (-70, 12), (-60, 8), (-52, 5), (-50, 0), (-42, -4),
     (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-54, -34),
     (-62, -40), (-68, -50), (-70, -54), (-73, -45), (-72, -32),
     (-71, -20), (-77, -12), (-80, -4), (-81, 3)],
    # Africa
    [(-17, 15), (-13, 22), (-8, 28), (-2, 35), (6, 37), (12, 34),
     (19, 32), (26, 32), (31, 31), (34, 27), (37, 21), (40, 14),
     (46, 11), (51, 10), (45, 2), (40, -9), (37, -16), (34, -25),
     (28, -32), (20, -35), (16, -30), (13, -20), (12, -12), (10, -2),
     (8, 4), (2, 6), (-6, 5), (-13, 8), (-17, 12)],
    # Madagascar
    [(44, -16), (47, -15), (50, -17), (48, -21), (45, -25), (43, -20)],
    # Eurasia: Atlantic coast, then the Arctic coast east
    [(-6, 36), (-9, 43), (-2, 48), (2, 51), (7, 55), (10, 59),
     (18, 64), (25, 70), (45, 68), (65, 70), (85, 75), (105, 77),
     (125, 72), (145, 71), (165, 67), (175, 65), (170, 61),
     (160, 57), (152, 47), (142, 41), (136, 34), (130, 33),
     (125, 37), (121, 32), (115, 23), (108, 16), (103, 9), (98, 10),
     (94, 20), (88, 21), (82, 17), (79, 10), (76, 9), (73, 16),
     (69, 21), (64, 25), (58, 25), (53, 27), (48, 30), (42, 29),
     (37, 20), (34, 13), (38, 12), (44, 13), (50, 15), (55, 18),
     (58, 22), (56, 26), (51, 28), (46, 30), (40, 31),
     # Levant: the ring runs south of Israel, so Gaza, the West Bank and
     # Jerusalem sit on land; then the Mediterranean coast runs west
     (36, 36), (37, 32), (34, 30.5), (31, 31),
     (28, 31.5), (25, 32), (22, 33), (20, 34), (19, 36), (21, 38),
     (18, 40), (15, 38), (12, 44), (8, 44), (4, 43), (0, 39)],
    # Australia
    [(114, -22), (114, -31), (117, -35), (124, -33), (130, -32),
     (135, -35), (140, -38), (147, -39), (153, -32), (153, -27),
     (149, -21), (144, -15), (141, -12), (136, -12), (132, -12),
     (127, -14), (122, -17), (116, -20)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
     (1, 51), (-1, 50)],
    # Japan
    [(130, 31), (133, 34), (136, 34), (140, 35.5), (141, 38), (141, 42),
     (143, 44), (141, 45), (139, 41), (137, 37), (134, 34), (131, 32)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -37),
     (175, -40), (172, -43), (169, -46)],
    # Indonesia
    [(95, 5), (98, 3), (101, 0), (104, -3), (107, -6), (110, -7),
     (114, -8), (118, -9), (120, -10), (122, -9), (119, -5), (115, -2),
     (112, 1), (108, 2), (105, 3), (100, 4)],
    # Philippines
    [(116, 18), (120, 19), (122, 17), (122, 13), (121, 10), (119, 8),
     (120, 6), (118, 8), (117, 12), (116, 16)],
]

# Story locations on the map: (longitude, latitude, continent colour,
# story number). True positions for each story's place. A few markers are
# nudged a degree or two on the main map only (MAIN_SPREAD, still inside
# the right country or region) so tight clusters stay readable; the zoom
# inset below shows the Europe & Middle East cluster at true positions.
MARKERS_LL = [
    (36.5, 45.3, C_EUROPE, 1),    # Kerch Bridge, Crimea
    (50.6, 26.2, C_MIDEAST, 2),   # Bahrain (US radar) / Qeshm strikes
    (121.0, 14.6, C_ASIA, 3),     # Manila
    (23.0, -2.0, C_AFRICA, 4),    # DR Congo (Ebola)
    (-121.9, 37.4, C_AMERICAS, 5),  # Nvidia, Santa Clara
    (85.3, 27.7, C_ASIA, 6),      # Nepal
    (34.5, 31.5, C_MIDEAST, 7),   # Gaza
    (106.9, 47.9, C_ASIA, 8),     # Mongolia
    (139.7, 35.7, C_ASIA, 9),     # Japan
    (-98.5, 38.5, C_AMERICAS, 10),  # US measles (Kansas)
    (87.0, 55.4, C_EUROPE, 11),   # Siberia crash, Kemerovo
    (2.3, 48.9, C_EUROPE, 12),    # Paris (Depardieu)
    (44.2, 15.4, C_MIDEAST, 13),  # Yemen, Sanaa
    (2.3, 48.9, C_EUROPE, 14),    # Paris (France strikes)
    (30.5, 50.4, C_EUROPE, 15),   # Kyiv
    (20.5, 44.8, C_EUROPE, 16),   # Serbia, Belgrade
    (90.4, 23.8, C_ASIA, 17),     # Bangladesh, Dhaka
    (32.6, -25.9, C_AFRICA, 18),  # Mozambique, Maputo
    (8.7, 50.1, C_EUROPE, 19),    # Deutsche Bank, Frankfurt
    (28.8, 47.0, C_EUROPE, 20),   # Moldova, Chisinau
    (35.2, 32.0, C_MIDEAST, 21),  # West Bank
    (-0.1, 51.5, C_EUROPE, 22),   # London (UK sanctions)
    (51.4, 35.7, C_MIDEAST, 23),  # Iran, Tehran
    (34.5, 31.5, C_MIDEAST, 24),  # Gaza airstrikes
    (37.6, 55.8, C_EUROPE, 25),   # Russia, Moscow (drone claim)
    (2.3, 48.9, C_EUROPE, 26),    # Paris (covert op)
    (-77.0, 38.9, C_AMERICAS, 27),  # Washington DC
    (30.1, -1.9, C_AFRICA, 28),   # Rwanda, Kigali
    (-74.0, 40.7, C_AMERICAS, 29),  # New York (JPMorgan)
    (28.9, 41.0, C_EUROPE, 30),   # Istanbul (Sozcu TV)
    (35.2, 31.8, C_MIDEAST, 31),  # Jerusalem (Kahana)
    (-13.7, 9.5, C_AFRICA, 32),   # Guinea, Conakry
    (78.4, 30.4, C_ASIA, 33),     # India bus crash, Tehri Garhwal
    (28.0, -26.2, C_AFRICA, 34),  # South Africa, Johannesburg
    (-118.1, 34.1, C_AMERICAS, 35),  # Voyager 1 mission control, JPL
    (116.4, 39.9, C_ASIA, 36),    # Beijing (China-Canada)
    (100.5, 13.8, C_ASIA, 37),    # Thailand, Bangkok
    (86.0, 20.0, C_ASIA, 38),     # Cyclone Akvan, Odisha coast
    (36.8, -1.3, C_AFRICA, 39),   # Kenya, Nairobi
    (-122.0, 37.3, C_AMERICAS, 40),  # Apple, Cupertino
]

# Main-map display nudges (degrees) for tight clusters; the badge stays
# on the story's country or region, just with breathing room. Clusters
# too tight for separate dots at this scale get a leader line instead:
# MAIN_LEADERS maps a story number to a badge lon/lat, with a thin line
# back to the true anchor.
MAIN_SPREAD = {
    4: (-8.0, -4.0), 15: (1.0, 0.6), 20: (-1.3, -1.0),
    27: (-1.5, -0.9), 30: (0.6, -1.0), 38: (-1.0, 0.5),
}
MAIN_LEADERS = {
    40: (-112, 46), 35: (-110, 28), 29: (-68, 46), 39: (42, 7),
    17: (99, 26), 6: (90, 38), 14: (-8, 40), 26: (16, 60),
    21: (46, 34), 24: (22, 22), 31: (16, 34), 23: (59, 44),
}

# Europe & Middle East zoom inset: lon -12..58, lat 15..62, drawn at
# 2.0 px per degree. These stories sit inside it; the rest stay on the
# main map only. Tight pairs get a leader line from an offset badge to
# the true anchor (INSET_LEADERS: number -> badge lon/lat).
INSET_NUMBERS = [1, 2, 7, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24,
                 25, 26, 30, 31]
INSET_LEADERS = {
    14: (-2.0, 45.0), 26: (10.0, 56.0), 21: (33.0, 38.0),
    24: (28.0, 27.0), 31: (41.0, 33.0), 22: (-2.0, 53.0),
    20: (26.0, 48.0),
}

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
     "fell into the strait.",
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
     "Passes 11,000 cases; 5,400 deaths", mini_ebola),
    ("BUSINESS", "NVIDIA: $115 BILLION",
     "$115.8bn sales; Huang won't return", mini_chip),
    ("ASIA · CLIMATE", "NEPAL FIRST",
     "UN loss-and-damage funds set aside", mini_mountains),
    ("MIDDLE EAST · GAZA", "GAZA AID AT RISK",
     "Four nations urge crossings to open", mini_gaza),
    ("ASIA · POLITICS", "MONGOLIA PRESIDENT RESIGNS",
     "President quits amid corruption scandal", mini_parliament),
    ("ASIA · SECURITY", "JAPAN SCRAMBLES JETS",
     "Russian jets violate Japanese airspace", mini_jet),
    ("AMERICAS · HEALTH", "MEASLES STATUS LOST",
     "US, Mexico, Bolivia lose measles status", mini_measles),
    ("RUSSIA · AIR CRASH", "PLANE CRASH KILLS 19",
     "Military plane crash kills all 19 on board", mini_crash),
    ("EUROPE · JUSTICE", "DEPARDIEU PLEADS GUILTY",
     "Actor admits assault, drops appeal", mini_court),
    ("MIDDLE EAST · YEMEN", "HOUTHI ADVANCE",
     "Troops retreat as Houthis advance", mini_desert),
    ("EUROPE · LABOUR", "FRANCE STRIKES AGAIN",
     "Second strike over pay and terms", mini_crowd),
    ("EUROPE · UKRAINE WAR", "KYIV BRIDGES HIT",
     "Strikes hit two bridges; water, power cut", mini_kyiv),
    ("EUROPE · POLITICS", "SERBIA: STUDENTS TAKE POWER",
     "Student List sworn in; Vučić era ends", mini_serbia),
    ("ASIA · LABOUR", "BANGLADESH: TEAR GAS AT PROTEST",
     "Tear gas at protest; 37 factories shut", mini_bangladesh),
    ("AFRICA · JUSTICE", "MONDLANE ON TRIAL",
     "Mondlane on trial; up to 24 years", mini_prison),
    ("BUSINESS", "DEUTSCHE BANK SINKS",
     "Shares fall >6% after 15m-file leak", mini_bank),
]

ALSO_ON = [
    "Moldova: Sandu claims drone incursion.",
    "West Bank: settlers kill woman, 72.",
    "UK: sanctions settlement firms.",
    "Iran: blocks IAEA inspectors for now.",
    "Gaza: airstrikes go on despite truce.",
    "Russia: record drone kills claimed.",
    "France: covert Ukraine op revealed.",
    'Trump: US "looking into" bomb report.',
    "China–Canada: more tariff cuts agreed.",
    "Thailand: to scrap tariffs on US goods.",
    "Cyclone Akvan bears down on Odisha.",
    "Kenya: WFP aids 30,000 who fled.",
    "Apple: iCloud, Pay, App Store outage.",
    "Rwanda: five EU states plan return hub.",
    "JPMorgan: software bug delays Zelle.",
    "Turkey: Sözcü TV off air in dawn raid.",
    "Kahana elected speaker, 66–52.",
    "Guinea: 224 jailed over gold mining.",
    "India: bus plunges 100 m, 8 dead.",
    "South Africa: 17 killed in shootings.",
    "Voyager 1 nears one light-day.",
]

STORY_COUNT = len(HEROES) + len(MIDS) + len(ALSO_ON)  # 40

# By-the-numbers strip: four figures, each from a story on this page.
# The drone figure is a claim (the also-on line says "claimed").
STRIP = [
    ("1,441", "Russian drones claimed in one night"),
    ("$115.8bn", "Nvidia quarterly revenue"),
    ("5,400+", "US measles cases in 2026"),
    ("11,000+", "Ebola cases in DR Congo"),
]

# Number colours: the badge/marker/list number of each story takes its
# continent colour, so the number cross-references the map legend.
HERO_COLORS = [C_EUROPE, C_MIDEAST, C_ASIA]
MID_COLORS = [C_AFRICA, C_AMERICAS, C_ASIA, C_MIDEAST, C_ASIA, C_ASIA,
              C_AMERICAS, C_EUROPE, C_EUROPE, C_MIDEAST, C_EUROPE, C_EUROPE,
              C_EUROPE, C_ASIA, C_AFRICA, C_EUROPE]
ALSO_COLORS = [C_EUROPE, C_MIDEAST, C_EUROPE, C_MIDEAST, C_MIDEAST, C_EUROPE,
               C_EUROPE, C_AMERICAS, C_ASIA, C_ASIA, C_ASIA, C_AFRICA,
               C_AMERICAS, C_AFRICA, C_AMERICAS, C_EUROPE, C_MIDEAST,
               C_AFRICA, C_ASIA, C_AFRICA, C_AMERICAS]


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
    hy, hh = 116, 170
    for i, (tag, title, caption, scene) in enumerate(HEROES):
        px = margin + i * (hw + gap)
        d.rectangle([px, hy, px + hw, hy + hh], fill=WHITE,
                    outline=INK, width=2)
        scene(d, px + 2, hy + 2, hw - 4, 78)
        num_badge(d, px + 20, hy + 20, 17, i + 1, HERO_COLORS[i], 17)
        d.text((px + 10, hy + 84), tag, font=font(BOLD, 11), fill=RED)
        lines = wrap(d, title, font(BOLD, 18), hw - 20)
        ly = hy + 100
        for line in lines[:2]:
            d.text((px + 10, ly), line, font=font(BOLD, 18), fill=NAVY)
            ly += 20
        clines = wrap(d, caption, font(REG, 12), hw - 20)
        ly = hy + 142
        for line in clines[:2]:
            d.text((px + 10, ly), line, font=font(REG, 12), fill=GREY)
            ly += 12

    # ---- Mid grid: 4 columns x 4 rows, compact panels ----
    mgap = 6
    mw = (W - 2 * margin - 3 * mgap) // 4  # 246
    mh = 92
    my0 = 292
    for i, (tag, title, caption, scene) in enumerate(MIDS):
        col, row = i % 4, i // 4
        px = margin + col * (mw + mgap)
        py = my0 + row * (mh + mgap)
        d.rectangle([px, py, px + mw, py + mh], fill=WHITE,
                    outline=INK, width=2)
        scene(d, px + 2, py + 2, mw - 4, 34)
        num_badge(d, px + 14, py + 14, 12, i + 4, MID_COLORS[i], 12)
        d.text((px + 10, py + 42), tag, font=font(BOLD, 10), fill=RED)
        tfont = fit_font(d, title, BOLD, 14, mw - 20)
        lines = wrap(d, title, tfont, mw - 20)
        d.text((px + 10, py + 56), lines[0], font=tfont, fill=NAVY)
        clines = wrap(d, caption, font(REG, 11), mw - 20)
        d.text((px + 10, py + 72), clines[0], font=font(REG, 11),
               fill=GREY)

    # ---- By-the-numbers strip ----
    sy = 684
    d.rectangle([margin, sy, W - margin, sy + 44], fill=WHITE,
                outline=INK, width=1)
    sw = (W - 2 * margin) // 4
    for i, (num, label) in enumerate(STRIP):
        cx = margin + i * sw + sw // 2
        d.text((cx, sy + 5), num, font=font(BOLD, 20), fill=NAVY,
               anchor="ma")
        d.text((cx, sy + 29), label, font=font(REG, 10), fill=GREY,
               anchor="ma")
        if i:
            d.line([margin + i * sw, sy + 6, margin + i * sw, sy + 38],
                   fill=(200, 200, 200), width=1)

    # ---- Bottom band: world map (left) + also-on list (right) ----
    by = 734
    # Map panel
    mx, mw2 = margin, 450
    d.rectangle([mx, by, mx + mw2, by + 242], fill=WHITE,
                outline=INK, width=2)
    d.text((mx + 10, by + 6), "WHERE IT HAPPENED",
           font=font(BOLD, 15), fill=NAVY)
    d.text((mx + 10, by + 24), "Numbered dots match stories 1–40.",
           font=font(REG, 10), fill=GREY)
    # main map: 290 x 143, the 446 x 220 box scaled 0.65
    map_x, map_y = mx + 2, by + 40
    map_w, map_h = 290, 143
    ms = map_h / 220.0
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                fill=(226, 238, 244))
    for poly in CONTINENTS_LL:
        d.polygon([(map_x + px * ms, map_y + py * ms)
                   for px, py in (ll_to_map(lon, lat)
                                  for lon, lat in poly)],
                  fill=(170, 196, 168), outline=(120, 150, 125))
    # leader lines first (under the badges)
    for lon, lat, col, n in MARKERS_LL:
        if n in MAIN_LEADERS:
            blon, blat = MAIN_LEADERS[n]
            bcx, bcy = ll_to_map(blon, blat)
            acx, acy = ll_to_map(lon, lat)
            d.line([map_x + bcx * ms, map_y + bcy * ms,
                    map_x + acx * ms, map_y + acy * ms],
                   fill=(60, 60, 60), width=1)
    for lon, lat, col, n in MARKERS_LL:
        if n in MAIN_LEADERS:
            lon, lat = MAIN_LEADERS[n]
        else:
            dlon, dlat = MAIN_SPREAD.get(n, (0, 0))
            lon, lat = lon + dlon, lat + dlat
        cx, cy = ll_to_map(lon, lat)
        num_badge(d, map_x + cx * ms, map_y + cy * ms, 6, n, col,
                  9 if n < 10 else 8)
    # zoom inset: Europe & Middle East (lon -12..58, lat 15..62) at
    # 2.0 px per degree, drawn on its own image so coastlines clip
    inset = Image.new("RGB", (150, 143), (226, 238, 244))
    di = ImageDraw.Draw(inset)
    di.text((75, 3), "EUROPE & MIDDLE EAST", font=font(BOLD, 9),
            fill=NAVY, anchor="ma")
    iox, ioy, isc = 5, 34, 2.0
    for poly in CONTINENTS_LL:
        di.polygon([(iox + (lon + 12.0) * isc, ioy + (62.0 - lat) * isc)
                    for lon, lat in poly],
                   fill=(170, 196, 168), outline=(120, 150, 125))
    by_num = {n: (lon, lat, col) for lon, lat, col, n in MARKERS_LL}
    for n in INSET_NUMBERS:
        lon, lat, col = by_num[n]
        ax, ay = iox + (lon + 12.0) * isc, ioy + (62.0 - lat) * isc
        bx, byy = ax, ay
        if n in INSET_LEADERS:
            blon, blat = INSET_LEADERS[n]
            bx, byy = (iox + (blon + 12.0) * isc,
                       ioy + (62.0 - blat) * isc)
            di.line([bx, byy, ax, ay], fill=GREY, width=1)
        num_badge(di, bx, byy, 5, n, col, 8)
    img.paste(inset, (mx + mw2 - 152, map_y))
    d.rectangle([mx + mw2 - 152, map_y, mx + mw2 - 2, map_y + 143],
                outline=NAVY, width=1)
    # legend: 2 rows x 3 columns
    ly = by + 194
    for i, (name, col) in enumerate(LEGEND):
        lx = mx + 12 + (i % 3) * 148
        ly2 = ly + (i // 3) * 17
        d.ellipse([lx, ly2 + 2, lx + 9, ly2 + 11], fill=col)
        d.text((lx + 13, ly2), name, font=font(REG, 11), fill=INK)
    d.text((mx + 10, by + 228),
           "Dots 1–40: all stories on this page, numbered to match the list.",
           font=font(REG, 10), fill=GREY)

    # Also-on list
    ax = mx + mw2 + gap  # 468
    aw = W - margin - ax  # 546
    d.text((ax, by + 6), "ALSO ON TUESDAY 17 NOVEMBER",
           font=font(BOLD, 15), fill=NAVY)
    d.line([ax, by + 26, ax + aw, by + 26], fill=INK, width=1)
    col_w = (aw - gap) // 2  # 269
    half = (len(ALSO_ON) + 1) // 2  # 11 per column
    for ci in range(2):
        cx = ax + ci * (col_w + gap)
        for j, line in enumerate(ALSO_ON[ci * half:(ci + 1) * half]):
            n = 20 + ci * half + j
            num = "%d." % n
            nfnt = font(BOLD, 12)
            nw = d.textlength(num, font=nfnt)
            fnt = fit_font(d, line, REG, 12, col_w - nw - 6)
            d.text((cx, by + 32 + j * 19), num, font=nfnt,
                   fill=ALSO_COLORS[n - 20])
            d.text((cx + nw + 6, by + 32 + j * 19), line, font=fnt,
                   fill=INK)

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
