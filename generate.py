#!/usr/bin/env python3
"""Generate entry.png: flat world-map infographic of 17 Nov 2026 world news.

Draws simplified continent outlines with PIL, 7 numbered pins at the
story locations, and a legend strip with the date and short headlines.
Only the verified facts supplied in the build brief are used.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# --- colours ---------------------------------------------------------------
NAVY = (13, 32, 61)
NAVY2 = (24, 52, 92)
GOLD = (232, 176, 44)
SEA = (214, 232, 240)
LAND = (176, 205, 178)
LAND_EDGE = (110, 150, 118)
INK = (18, 28, 40)
MUTED = (70, 84, 100)
WHITE = (255, 255, 255)
ROW_A = (246, 248, 250)
ROW_B = (232, 238, 243)
PIN_RED = (198, 40, 40)

# --- map projection: equirectangular over the map band ----------------------
MAP_TOP, MAP_BOT = 132, 596
MAP_LEFT, MAP_RIGHT = 16, 1008


def proj(lon, lat):
    x = MAP_LEFT + (lon + 170.0) / 360.0 * (MAP_RIGHT - MAP_LEFT)
    y = MAP_TOP + (75.0 - lat) / 130.0 * (MAP_BOT - MAP_TOP)
    return (x, y)


# Simplified continent outlines (lon, lat) — recognisable, not geographic.
CONTINENTS = {
    "north_america": [
        (-168, 66), (-158, 71), (-140, 70), (-128, 71), (-115, 68), (-100, 69),
        (-85, 66), (-80, 62), (-70, 58), (-60, 52), (-65, 45), (-75, 39),
        (-80, 32), (-84, 30), (-90, 21), (-97, 16), (-105, 20), (-112, 28),
        (-120, 34), (-125, 40), (-125, 49), (-135, 58), (-150, 60), (-165, 60),
    ],
    "greenland": [(-58, 64), (-45, 60), (-32, 68), (-22, 70), (-30, 76), (-55, 76), (-62, 70)],
    "south_america": [
        (-78, 9), (-72, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
        (-35, -8), (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -52),
        (-73, -44), (-73, -30), (-70, -18), (-80, -6), (-81, 0), (-80, 6),
    ],
    "europe": [
        (-10, 36), (-9, 43), (-2, 48), (-4, 50), (2, 51), (5, 53), (8, 57),
        (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (32, 70),
        (40, 68), (45, 68), (50, 69), (55, 68), (58, 64), (52, 60), (48, 58),
        (44, 55), (40, 50), (38, 47), (34, 45), (30, 46), (28, 44), (24, 40),
        (23, 36), (19, 40), (16, 38), (12, 44), (8, 44), (3, 42), (0, 39),
        (-2, 37), (-6, 36),
    ],
    "africa": [
        (-6, 35), (10, 37), (20, 32), (30, 31), (32, 31), (35, 28), (39, 22),
        (43, 12), (51, 11), (51, 2), (46, -2), (40, -10), (36, -18), (33, -26),
        (28, -33), (20, -35), (16, -29), (12, -18), (9, -1), (9, 4), (-8, 5),
        (-13, 8), (-17, 15), (-17, 21), (-16, 28), (-10, 31),
    ],
    "asia": [
        (32, 36), (36, 36), (40, 38), (44, 39), (48, 38), (52, 37), (54, 39),
        (58, 39), (61, 37), (66, 37), (70, 41), (74, 40), (78, 43), (82, 45),
        (88, 48), (95, 50), (100, 52), (108, 53), (115, 53), (122, 53), (128, 52),
        (135, 44), (140, 40), (142, 46), (142, 52), (142, 59), (158, 60), (162, 56),
        (170, 60), (178, 65), (180, 66), (178, 64), (170, 60), (162, 58),
        (156, 51), (150, 59), (142, 55), (141, 45), (140, 39), (135, 34),
        (130, 33), (127, 35), (126, 38), (122, 39), (120, 32), (122, 28),
        (118, 25), (110, 20), (108, 18), (105, 9), (103, 7), (100, 8),
        (98, 10), (94, 16), (92, 21), (89, 22), (86, 20), (80, 13), (77, 8),
        (73, 16), (70, 21), (66, 25), (62, 25), (58, 25), (56, 26), (52, 26),
        (50, 29), (48, 30), (44, 29), (40, 30), (36, 36),
    ],
    "australia": [
        (114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
        (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
        (153, -27), (153, -24), (146, -19), (142, -11), (137, -12), (132, -12),
        (126, -14), (122, -17), (118, -20),
    ],
    # Japan as a small island chain so pin 6 sits on land, not open sea.
    "japan": [
        (139.5, 41), (141.5, 39), (141.0, 36), (139.5, 34), (137.0, 34),
        (136.0, 35.5), (138.0, 38.5),
    ],
    "united_kingdom": [
        (-5.5, 50), (-3, 53), (-5, 56), (-3, 58.5), (-1, 57), (0.5, 53),
        (1.5, 51), (-1, 50.5),
    ],
}

# Small-caps region labels placed on open sea/land (lon, lat, text).
REGION_LABELS = [
    (-100, 47, "NORTH AMERICA"),
    (-60, -14, "SOUTH AMERICA"),
    (12, 48, "EUROPE"),
    (18, 2, "AFRICA"),
    (88, 52, "ASIA"),
    (134, -25, "AUSTRALIA"),
]

# (number, lon, lat, short headline) — facts exactly as supplied in the brief.
STORIES = [
    (1, 33.5, 45.3,
     "Ukraine hits Kerch Bridge for a second day; Russia strikes Kyiv bridges"),
    (2, 50.5, 26.2,
     "Iran drone targets US radar in Bahrain, intercepted, no casualties; "
     "tanker hit by mine near Hormuz"),
    (3, 114.1, 22.5,
     "China confirms Xi-Trump-Putin three-way in Shenzhen, Thu 19 Nov, at "
     "APEC; Trump in Manila for ASEAN"),
    (4, 24.7, 59.4,
     "Estonia to shut all Russia border crossings from 1 Dec after alleged "
     "drone-factory arson plot"),
    (5, 35.4, 31.9,
     "UK sanctions 8 Israeli construction firms in the West Bank; settler "
     "kills 72-year-old woman in Jericho"),
    (6, 139.7, 36.2,
     "Japan scrambles fighter jets after two Russian planes suspected of "
     "airspace violation"),
    (7, 45.0, 13.5,
     "Houthis advance toward Aden, Yemen; drone hits Saudi East-West "
     "oil pipeline"),
]


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # --- header ------------------------------------------------------------
    d.rectangle([0, 0, W, 124], fill=NAVY)
    d.rectangle([0, 124, W, 132], fill=GOLD)
    d.text((32, 18), "WORLD NEWS IN ONE IMAGE", font=font(F_BOLD, 34), fill=WHITE)
    d.text((32, 66), "TUESDAY 17 NOVEMBER 2026", font=font(F_BOLD, 40), fill=GOLD)
    d.text((W - 32, 30), "7 STORIES", font=font(F_BOLD, 30), fill=WHITE, anchor="ra")
    d.text((W - 32, 72), "ONE DAY", font=font(F_REG, 24), fill=(180, 200, 220), anchor="ra")

    # --- map ---------------------------------------------------------------
    d.rectangle([0, 132, W, MAP_BOT], fill=SEA)
    for pts in CONTINENTS.values():
        d.polygon([proj(lon, lat) for lon, lat in pts], fill=LAND,
                  outline=LAND_EDGE, width=2)
    for lon, lat, label in REGION_LABELS:
        d.text(proj(lon, lat), label, font=font(F_BOLD, 15),
               fill=(96, 122, 104), anchor="mm")
    d.text((MAP_LEFT + 8, MAP_BOT - 30), "WORLD MAP  •  17 NOV 2026",
           font=font(F_REG, 18), fill=MUTED)

    pin_pos = {}
    for num, lon, lat, _ in STORIES:
        x, y = proj(lon, lat)
        pin_pos[num] = (x, y)
    # leader offsets so pins do not overlap in crowded Europe/Middle East
    offsets = {1: (34, -30), 2: (40, 26), 3: (36, -34), 4: (30, -34),
               5: (42, 30), 6: (30, -30), 7: (44, 22)}
    for num, lon, lat, _ in STORIES:
        x, y = pin_pos[num]
        ox, oy = offsets[num]
        cx, cy = x + ox, y + oy
        d.line([(x, y), (cx, cy)], fill=PIN_RED, width=3)
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=PIN_RED)
        d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=PIN_RED,
                  outline=WHITE, width=3)
        d.text((cx, cy - 1), str(num), font=font(F_BOLD, 22), fill=WHITE,
               anchor="mm")

    # --- legend ------------------------------------------------------------
    legend_top = MAP_BOT + 8
    d.rectangle([0, legend_top, W, H], fill=WHITE)
    d.text((32, legend_top + 8), "THE DAY'S NEWS",
           font=font(F_BOLD, 26), fill=NAVY)
    rows_top = legend_top + 48
    row_h = (H - rows_top) // len(STORIES)
    f_head = font(F_REG, 21)
    for i, (num, _lon, _lat, text) in enumerate(STORIES):
        y0 = rows_top + i * row_h
        d.rectangle([0, y0, W, y0 + row_h],
                    fill=ROW_A if i % 2 == 0 else ROW_B)
        d.ellipse([26, y0 + 10, 58, y0 + 42], fill=PIN_RED)
        d.text((42, y0 + 25), str(num), font=font(F_BOLD, 20), fill=WHITE,
               anchor="mm")
        lines = wrap(d, text, f_head, W - 110)
        ly = y0 + 7
        for ln in lines[:2]:
            d.text((72, ly), ln, font=f_head, fill=INK)
            ly += 25

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
