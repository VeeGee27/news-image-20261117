#!/usr/bin/env python3
"""Draw the entry image for make.fun competition news-image-20261117.

A newspaper front page summing up Tuesday 17 November 2026 in one image:
masthead with the date, six panels (one per verified story), footer with the
date. Flat shapes and crisp text only, so the image stays legible at small
sizes and the PNG stays far under the 1 MiB limit. Deterministic: same
input, same bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (251, 248, 241)
NAVY = (16, 36, 62)
GOLD = (232, 185, 74)
RED = (179, 39, 30)
INK = (24, 24, 24)
GREY = (58, 58, 58)
WHITE = (255, 255, 255)


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
    import math

    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def scene_strikes(draw, x, y, w, h):
    """US jets strike a missile site on Qeshm Island; Iran drones hit a US
    radar in Bahrain."""
    draw.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
    # sea
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=(46, 107, 138))
    # island
    draw.polygon([(x + 30, y + h - 30), (x + 120, y + h - 62),
                  (x + 260, y + h - 58), (x + 360, y + h - 30)],
                 fill=(74, 94, 58))
    # explosion starburst on the island
    starburst(draw, x + 190, y + h - 62, 26, 12, 8, fill=(232, 185, 74))
    starburst(draw, x + 190, y + h - 62, 15, 7, 8, fill=(232, 120, 40))
    # missile arcs (white trails)
    draw.arc([x + 40, y + 8, x + 200, y + 78], 200, 330, fill=WHITE, width=4)
    draw.arc([x + 250, y + 2, x + 420, y + 70], 210, 340, fill=WHITE, width=4)
    draw.ellipse([x + 192, y + 66, x + 200, y + 74], fill=(232, 120, 40))
    draw.ellipse([x + 412, y + 58, x + 420, y + 66], fill=(232, 120, 40))
    # a small drone (Iran fired drones at the radar) top right
    dx, dy = x + 400, y + 30
    draw.rectangle([dx - 14, dy - 4, dx + 14, dy + 4], fill=WHITE)
    draw.line([dx - 20, dy - 10, dx + 20, dy - 10], fill=WHITE, width=3)
    for rx in (dx - 20, dx + 20):
        draw.ellipse([rx - 4, dy - 14, rx + 4, dy - 6], fill=WHITE)
    draw.line([dx - 20, dy + 12, dx + 20, dy + 12], fill=WHITE, width=3)
    for rx in (dx - 20, dx + 20):
        draw.ellipse([rx - 4, dy + 8, rx + 4, dy + 16], fill=WHITE)


def scene_bridge(draw, x, y, w, h):
    """Kerch Bridge: a road section falls into the strait."""
    draw.rectangle([x, y, x + w, y + h], fill=(191, 217, 232))
    # water
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(46, 107, 138))
    # piers
    for px in (x + 70, x + 380):
        draw.rectangle([px, y + 62, px + 14, y + h - 30], fill=(90, 90, 90))
    # deck, left half intact
    draw.rectangle([x + 10, y + 52, x + 218, y + 66], fill=(120, 120, 120))
    # deck, right half tilted down into the water
    draw.polygon([(x + 268, y + 54), (x + 478, y + 66),
                  (x + 478, y + 80), (x + 268, y + 68)], fill=(120, 120, 120))
    # fallen section in the water
    draw.polygon([(x + 240, y + h - 34), (x + 330, y + h - 34),
                  (x + 322, y + h - 18), (x + 248, y + h - 18)],
                 fill=(90, 90, 90))
    # smoke puffs over the gap
    for cx, cy, r in ((x + 240, y + 40, 12), (x + 258, y + 30, 15),
                      (x + 280, y + 42, 10)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))


def scene_nvidia(draw, x, y, w, h):
    """Nvidia chip with its record revenue."""
    draw.rectangle([x, y, x + w, y + h], fill=(14, 122, 61))
    # chip body
    cx, cy = x + w // 2, y + h // 2
    draw.rectangle([cx - 78, cy - 42, cx + 78, cy + 42], fill=(16, 36, 62))
    draw.rectangle([cx - 58, cy - 24, cx + 58, cy + 24], fill=(27, 58, 92))
    # pins
    for i in range(6):
        px = cx - 68 + i * 27
        draw.rectangle([px, cy - 56, px + 12, cy - 42], fill=(200, 200, 200))
        draw.rectangle([px, cy + 42, px + 12, cy + 56], fill=(200, 200, 200))
    fnt = font(BOLD, 40)
    draw.text((cx, cy), "$115B", font=fnt, fill=WHITE, anchor="mm")


def scene_asia(draw, x, y, w, h):
    """Shenzhen skyline under the sun for the APEC talks."""
    draw.rectangle([x, y, x + w, y + h], fill=(242, 193, 78))
    # sun
    draw.ellipse([x + w - 78, y + 10, x + w - 28, y + 60], fill=(232, 120, 40))
    # skyline
    base = y + h
    towers = [(0, 62), (52, 92), (110, 70), (168, 104), (226, 78),
              (284, 96), (342, 66), (398, 88)]
    for tx, th in towers:
        draw.rectangle([x + tx, base - th, x + tx + 46, base], fill=NAVY)
    # windows
    for tx, th in towers:
        for wy in range(base - th + 10, base - 12, 16):
            draw.rectangle([x + tx + 8, wy, x + tx + 16, wy + 7],
                           fill=(232, 185, 74))
            draw.rectangle([x + tx + 28, wy, x + tx + 36, wy + 7],
                           fill=(232, 185, 74))
    # three summit flags on the shorter towers (US, China, Russia)
    for tx, th, kind in ((110, 70, "us"), (226, 78, "cn"),
                         (342, 66, "ru")):
        top = base - th
        pole_x = x + tx + 23
        draw.line([pole_x, top - 24, pole_x, top], fill=NAVY, width=2)
        fx, fy = pole_x + 2, top - 24
        if kind == "us":
            draw.rectangle([fx, fy, fx + 26, fy + 15], fill=(179, 39, 30))
            for sy in (fy + 5, fy + 11):
                draw.rectangle([fx, sy, fx + 26, sy + 2], fill=WHITE)
            draw.rectangle([fx, fy, fx + 10, fy + 7], fill=(16, 36, 62))
        elif kind == "cn":
            draw.rectangle([fx, fy, fx + 26, fy + 15], fill=(222, 41, 16))
            draw.ellipse([fx + 4, fy + 4, fx + 10, fy + 10],
                         fill=(255, 222, 0))
        else:
            draw.rectangle([fx, fy, fx + 26, fy + 5], fill=WHITE)
            draw.rectangle([fx, fy + 5, fx + 26, fy + 10], fill=(0, 57, 166))
            draw.rectangle([fx, fy + 10, fx + 26, fy + 15],
                           fill=(179, 39, 30))


def scene_ebola(draw, x, y, w, h):
    """Virus shapes for the Ebola surge in DR Congo."""
    draw.rectangle([x, y, x + w, y + h], fill=(122, 31, 31))
    import math

    def virus(cx, cy, r):
        for i in range(10):
            a = 2 * math.pi * i / 10
            x1 = cx + (r - 4) * math.cos(a)
            y1 = cy + (r - 4) * math.sin(a)
            x2 = cx + (r + 12) * math.cos(a)
            y2 = cy + (r + 12) * math.sin(a)
            draw.line([x1, y1, x2, y2], fill=(232, 120, 40), width=4)
            draw.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=(232, 120, 40))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(192, 57, 43))
        draw.ellipse([cx - r + 10, cy - r + 8, cx - r + 26, cy - r + 24],
                     fill=(220, 110, 90))

    virus(x + 130, y + 62, 34)
    virus(x + 330, y + 58, 26)
    virus(x + 420, y + 92, 16)


def scene_nepal(draw, x, y, w, h):
    """Mountains and flood waves for Nepal."""
    draw.rectangle([x, y, x + w, y + h], fill=(221, 235, 242))
    # mountains
    draw.polygon([(x + 10, y + h - 34), (x + 130, y + 12), (x + 250, y + h - 34)],
                 fill=(44, 92, 110))
    draw.polygon([(x + 180, y + h - 34), (x + 320, y + 30), (x + 460, y + h - 34)],
                 fill=(27, 58, 92))
    # snow caps
    draw.polygon([(x + 112, y + 30), (x + 130, y + 12), (x + 148, y + 30),
                  (x + 139, y + 38), (x + 130, y + 30), (x + 121, y + 38)],
                 fill=WHITE)
    # flood waves
    for i, wy in enumerate((y + h - 34, y + h - 20, y + h - 8)):
        col = (46, 107, 138) if i % 2 == 0 else (70, 140, 175)
        draw.rectangle([x, wy, x + w, wy + 10], fill=col)
    # small house roof above the water
    draw.polygon([(x + 330, y + h - 52), (x + 360, y + h - 72),
                  (x + 390, y + h - 52)], fill=(179, 39, 30))


PANELS = [
    ("U.S. STRIKES IRAN",
     "Jets hit a missile site on Qeshm Island after Iran fired drones "
     "at a U.S. radar in Bahrain",
     scene_strikes),
    ("KERCH BRIDGE HIT",
     "Ukraine drones hit the Crimea bridge a second day; a road section "
     "fell into the strait",
     scene_bridge),
    ("NVIDIA: $115 BILLION",
     "Record revenue \u2014 but ousted CEO Jensen Huang will not return",
     scene_nvidia),
    ("TRUMP TO SHENZHEN",
     "APEC talks with Xi and Putin ahead",
     scene_asia),
    ("EBOLA IN DR CONGO",
     "Cases in DR Congo pass 11,000, with 5,400 deaths",
     scene_ebola),
    ("NEPAL FIRST",
     "First UN loss-and-damage funding set aside after floods",
     scene_nepal),
]


def fit_font(draw, text, path, size, max_width):
    """Largest font size at or below `size` that fits the text in max_width."""
    while size > 18:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_width:
            return fnt
        size -= 1
    return font(path, 18)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 132], fill=NAVY)
    centered(d, 16, "THE WORLD IN ONE PICTURE", font(BOLD, 46), WHITE)
    centered(d, 72, "TUESDAY, 17 NOVEMBER 2026", font(BOLD, 42), GOLD)
    d.rectangle([0, 132, W, 138], fill=RED)
    centered(d, 146, "SIX STORIES FROM A SINGLE DAY", font(BOLD, 23), INK)

    # Grid of panels: 2 columns x 3 rows
    margin, gap = 16, 14
    pw = (W - 2 * margin - gap) // 2
    ph = 258
    top = 178
    for i, (title, caption, scene) in enumerate(PANELS):
        col, row = i % 2, i // 2
        px = margin + col * (pw + gap)
        py = top + row * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], fill=WHITE,
                    outline=INK, width=2)
        scene(d, px + 2, py + 2, pw - 4, 112)
        tfont = fit_font(d, title, BOLD, 31, pw - 24)
        d.text((px + 12, py + 122), title, font=tfont, fill=NAVY)
        lines = wrap(d, caption, font(REG, 24), pw - 24)
        ly = py + 158
        for line in lines[:3]:
            d.text((px + 12, ly), line, font=font(REG, 24), fill=GREY)
            ly += 29

    # Footer
    d.rectangle([0, 976, W, H], fill=NAVY)
    centered(d, 988, "TUESDAY, 17 NOVEMBER 2026", font(BOLD, 24), WHITE)

    img.save("entry.png", format="PNG")
    print("saved entry.png")


if __name__ == "__main__":
    main()
