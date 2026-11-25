# draw_grid.py — DRAFT ONLY for Revision 3 (Editorial Grid layout).
# Not pushed, not submitted. The live entry ("Cogent Meridian") is untouched.
# Structure and colours follow the NEW reference the user sent
# (~/workspace/user/files/1000111860_23_ogur.png): white paper, navy top
# bar with a globe, giant black masthead, centred stats, pale-blue numbers
# band with icon + big number + two-line caption, 3 heroes side by side
# with a number + section band on top of each picture, THE DAY IN EIGHT as
# ONE ROW of 8 cards, bottom map + 3-column city-dateline list + DATE CHECK
# (navy header, 3 bullets), dark footer.
# Same 35 verified stories as Revision 2; only the layout and colours
# change. The reference's own stories (Huawei, PIF tower, hostages,
# William & Kate, Thomas Markle) are NOT used.
# Run locally with Pillow:  python3 draw_grid.py [output-path]
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/noto"

PAPER = (255, 255, 255)
INK = (20, 20, 20)
NAVY = (27, 47, 94)
RED = (196, 32, 32)
GREY = (96, 90, 78)
GREEN = (0, 140, 90)
ORANGE = (214, 120, 30)
TINT_BLUE = (226, 234, 242)
NUM_BAND = (216, 228, 240)
TINT_SAND = (240, 228, 205)
TINT_PALE = (238, 232, 218)
HAIRLINE = (200, 192, 172)
CAPTION_GREY = (196, 188, 168)
LAND = (222, 208, 172)
LAND_LINE = (120, 110, 80)
OCEAN = (214, 228, 238)
WHITE = (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("NotoSerif-Regular.ttf", s)
F_SERIF_B = lambda s: font("NotoSerif-Bold.ttf", s)
F_SERIF_BL = lambda s: font("NotoSerif-Black.ttf", s)
F_SERIF_I = lambda s: font("NotoSerif-Italic.ttf", s)
F_BLACK = lambda s: font("NotoSans-Black.ttf", s)
F_BOLD = lambda s: font("NotoSans-Bold.ttf", s)
F_REG = lambda s: font("NotoSans-Regular.ttf", s)
F_IT = lambda s: font("NotoSans-Italic.ttf", s)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_hero_scene(d, kind, x, y, w, h):
    # One large, detailed vector scene inside a panel.
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    if kind == "flame":
        d.rectangle([x, y, x + w, y + h], fill=TINT_BLUE)
        gy = y + int(h * 0.82)
        d.rectangle([x, gy, x + w, y + h], fill=TINT_SAND)
        d.ellipse([x + w - 52, y + 14, x + w - 20, y + 46], fill=(240, 200, 90))
        tw = int(w * 0.13)
        towers = [(0.10, 0.55), (0.38, 0.78), (0.66, 0.62)]
        for fx, fh in towers:
            tx = x + int(w * fx)
            th = int(h * fh)
            d.rectangle([tx, gy - th, tx + tw, gy], fill=INK)
            d.rectangle([tx + tw // 3, gy - th - 12, tx + 2 * tw // 3,
                         gy - th], fill=INK)
            for wy in range(gy - th + 12, gy - 8, 16):
                d.rectangle([tx + 4, wy, tx + tw - 4, wy + 7], fill=WHITE)
        d.line([(x + int(w * 0.10) + tw, gy - int(h * 0.30)),
                (x + int(w * 0.66), gy - int(h * 0.30))], fill=INK, width=4)
        # Flames sit on top of their own towers (tower 1: fh 0.55,
        # tower 3: fh 0.62), never above the panel.
        t1 = gy - int(h * 0.55)
        d.polygon([(x + int(w * 0.14), t1 - 14),
                   (x + int(w * 0.23), t1),
                   (x + int(w * 0.19), t1 + 6),
                   (x + int(w * 0.15), t1 + 2)],
                  fill=ORANGE)
        t3 = gy - int(h * 0.62)
        d.polygon([(x + int(w * 0.70), t3 - 12),
                   (x + int(w * 0.78), t3),
                   (x + int(w * 0.74), t3 + 5),
                   (x + int(w * 0.71), t3 + 2)],
                  fill=ORANGE)
        d.ellipse([x + int(w * 0.30), y + 16, x + int(w * 0.38), y + 28],
                  fill=WHITE)
        d.ellipse([x + int(w * 0.52), y + 10, x + int(w * 0.59), y + 21],
                  fill=WHITE)
        d.ellipse([x + int(w * 0.80), y + 22, x + int(w * 0.86), y + 31],
                  fill=WHITE)
    elif kind == "rocket":
        d.rectangle([x, y, x + w, y + h], fill=TINT_BLUE)
        gy = y + int(h * 0.88)
        d.rectangle([x, gy, x + w, y + h], fill=TINT_SAND)
        d.ellipse([x + int(w * 0.08), y + 18, x + int(w * 0.22), y + 34],
                  fill=WHITE)
        d.ellipse([x + int(w * 0.72), y + 26, x + int(w * 0.88), y + 40],
                  fill=WHITE)
        d.ellipse([x + int(w * 0.60), y + 10, x + int(w * 0.70), y + 20],
                  fill=WHITE)
        cx = x + w // 2
        d.rectangle([cx - 78, y + 30, cx - 66, gy], fill=INK)
        for by in range(y + 44, gy - 10, 18):
            d.line([(cx - 78, by), (cx - 52, by)], fill=INK, width=3)
        d.line([(cx - 66, y + 52), (cx - 52, y + 52)], fill=INK, width=3)
        d.polygon([(cx, y + 12), (cx + 20, y + 44), (cx - 20, y + 44)],
                  fill=INK)
        d.rectangle([cx - 20, y + 44, cx + 20, y + 96], fill=INK)
        d.ellipse([cx - 8, y + 56, cx + 8, y + 72], fill=WHITE)
        d.polygon([(cx - 20, y + 82), (cx - 36, y + 104), (cx - 20, y + 96)],
                  fill=INK)
        d.polygon([(cx + 20, y + 82), (cx + 36, y + 104), (cx + 20, y + 96)],
                  fill=INK)
        d.polygon([(cx - 8, y + 96), (cx + 8, y + 96), (cx, y + 122)],
                  fill=ORANGE)
        d.ellipse([cx - 22, gy - 16, cx + 22, gy - 2], fill=WHITE)
        d.ellipse([cx - 34, gy - 10, cx - 8, gy], fill=WHITE)
        d.ellipse([cx + 8, gy - 10, cx + 34, gy], fill=WHITE)
    elif kind == "bars":
        d.rectangle([x, y, x + w, y + h], fill=TINT_PALE)
        plot_top = y + 18
        plot_bot = y + h - 26
        for i in range(4):
            gy = plot_top + i * (plot_bot - plot_top) // 3
            d.line([(x + 14, gy), (x + w - 14, gy)], fill=(200, 192, 172),
                   width=1)
        d.line([(x + 14, plot_bot), (x + w - 14, plot_bot)], fill=INK, width=2)
        heights = [0.22, 0.38, 0.55, 0.72, 0.92]
        bw = int((w - 48) / 5)
        for i, fh in enumerate(heights):
            bx = x + 24 + i * (bw + 6)
            bh = int((plot_bot - plot_top) * fh)
            col = RED if i == 4 else INK
            d.rectangle([bx, plot_bot - bh, bx + bw, plot_bot], fill=col)
        d.ellipse([x + w - 34, y + 6, x + w - 24, y + 16], fill=RED)


def draw_mini(d, kind, x, y, s, bg, fg):
    # Small category glyph, drawn inside a square of side s.
    d.rectangle([x, y, x + s, y + s], fill=bg, outline=INK, width=1)
    c = s / 2
    if kind == "target":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=fg, width=2)
        d.ellipse([x + c - 2, y + c - 2, x + c + 2, y + c + 2], fill=fg)
    elif kind == "vote":
        d.rectangle([x + 3, y + 6, x + 13, y + 14], outline=fg, width=2)
        d.line([(x + 5, y + 5), (x + 7, y + 8), (x + 12, y + 2)], fill=fg, width=2)
    elif kind == "flame":
        d.polygon([(x + 8, y + 2), (x + 13, y + 9), (x + 10, y + 11),
                   (x + 12, y + 14), (x + 8, y + 15), (x + 4, y + 14),
                   (x + 6, y + 11), (x + 3, y + 9)], fill=fg)
        d.ellipse([x + 6, y + 10, x + 10, y + 14], fill=WHITE)
    elif kind == "flag":
        d.line([(x + 5, y + 2), (x + 5, y + 14)], fill=fg, width=2)
        d.polygon([(x + 5, y + 2), (x + 13, y + 4), (x + 5, y + 7)], fill=fg)
    elif kind == "home":
        d.polygon([(x + 8, y + 2), (x + 14, y + 7), (x + 2, y + 7)], fill=fg)
        d.rectangle([x + 4, y + 7, x + 12, y + 14], fill=fg)
        d.rectangle([x + 7, y + 10, x + 9, y + 14], fill=WHITE)
    elif kind == "court":
        d.line([(x + 8, y + 3), (x + 8, y + 12)], fill=fg, width=2)
        d.line([(x + 3, y + 3), (x + 13, y + 3)], fill=fg, width=2)
        d.polygon([(x + 3, y + 3), (x + 1, y + 8), (x + 5, y + 8)], fill=fg)
        d.polygon([(x + 13, y + 3), (x + 11, y + 8), (x + 15, y + 8)], fill=fg)
        d.line([(x + 4, y + 13), (x + 12, y + 13)], fill=fg, width=2)
    elif kind == "rocket":
        d.polygon([(x + 8, y + 2), (x + 11, y + 8), (x + 5, y + 8)], fill=fg)
        d.rectangle([x + 6, y + 8, x + 10, y + 12], fill=fg)
        d.polygon([(x + 8, y + 12), (x + 10, y + 15), (x + 6, y + 15)], fill=ORANGE)
    elif kind == "ball":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=fg, width=2)
        d.ellipse([x + c - 2, y + c - 2, x + c + 2, y + c + 2], fill=fg)
        d.line([(x + c, y + 2), (x + c, y + c - 2)], fill=fg, width=1)
        d.line([(x + 2, y + c), (x + c - 2, y + c)], fill=fg, width=1)
        d.line([(x + s - 2, y + c), (x + c + 2, y + c)], fill=fg, width=1)
    elif kind == "warn":
        d.polygon([(x + 8, y + 2), (x + 15, y + 14), (x + 1, y + 14)], fill=ORANGE)
        d.line([(x + 8, y + 6), (x + 8, y + 10)], fill=WHITE, width=2)
        d.ellipse([x + 7, y + 11, x + 9, y + 13], fill=WHITE)
    elif kind == "chip":
        d.rectangle([x + 4, y + 4, x + 12, y + 12], outline=fg, width=2)
        d.ellipse([x + 7, y + 7, x + 9, y + 9], fill=fg)
        for px in [6, 8, 10]:
            d.line([(x + px, y + 1), (x + px, y + 4)], fill=fg, width=1)
            d.line([(x + px, y + 12), (x + px, y + 15)], fill=fg, width=1)
    elif kind == "plane":
        d.polygon([(x + 2, y + 9), (x + 14, y + 5), (x + 14, y + 8),
                   (x + 9, y + 10), (x + 12, y + 13), (x + 9, y + 13),
                   (x + 6, y + 11), (x + 2, y + 12)], fill=fg)
    elif kind == "poll":
        for i, h in enumerate([5, 9, 13]):
            bx = x + 3 + i * 4
            d.rectangle([bx, y + 14 - h, bx + 3, y + 14], fill=fg)
    elif kind == "drop":
        d.polygon([(x + 8, y + 1), (x + 13, y + 8), (x + 3, y + 8)], fill=fg)
        d.ellipse([x + 3, y + 7, x + 13, y + 15], fill=fg)
    elif kind == "drone":
        d.rectangle([x + 6, y + 7, x + 10, y + 9], fill=fg)
        for rx, ry in [(3, 4), (13, 4), (3, 12), (13, 12)]:
            d.ellipse([x + rx - 1, y + ry - 1, x + rx + 1, y + ry + 1], fill=fg)
        d.line([(x + 4, y + 5), (x + 7, y + 7)], fill=fg, width=1)
        d.line([(x + 12, y + 5), (x + 9, y + 7)], fill=fg, width=1)
    elif kind == "bars":
        for i, bh in enumerate([5, 9, 13]):
            bx = x + 3 + i * 4
            d.rectangle([bx, y + 14 - bh, bx + 3, y + 14], fill=fg)
    elif kind == "chart":
        d.line([(x + 3, y + 12), (x + 6, y + 8), (x + 9, y + 10),
                (x + 13, y + 4)], fill=fg, width=2)
        d.polygon([(x + 13, y + 4), (x + 10, y + 4), (x + 13, y + 7)], fill=fg)
    elif kind == "exit":
        d.rectangle([x + 3, y + 3, x + 8, y + 13], outline=fg, width=1)
        d.line([(x + 6, y + 8), (x + 13, y + 8)], fill=fg, width=2)
        d.polygon([(x + 13, y + 8), (x + 10, y + 5), (x + 10, y + 11)], fill=fg)
    elif kind == "shield":
        d.polygon([(x + 8, y + 2), (x + 14, y + 4), (x + 14, y + 9),
                   (x + 8, y + 14), (x + 2, y + 9), (x + 2, y + 4)], fill=fg)
        d.line([(x + 5, y + 8), (x + 7, y + 10), (x + 11, y + 5)],
               fill=WHITE, width=2)


def draw_icon(d, kind, x, y, s, bg, fg):
    # Borderless category glyph, for the numbers band.
    tile = Image.new("RGB", (17, 17), bg)
    td = ImageDraw.Draw(tile)
    draw_mini(td, kind, 1, 1, 15, bg, fg)
    inner = tile.crop((1, 1, 16, 16))
    big = inner.resize((s, s), Image.NEAREST)
    d._image.paste(big, (x, y))


def draw_eight_card(d, n, kind, region, x, y, w, ph):
    # One of the 8 cards in a single row: a small picture panel on top
    # (red number square + navy region tab, framed glyph + caption lines),
    # then the headline and the section line below.
    d.rectangle([x, y, x + w, y + ph], fill=TINT_PALE, outline=INK, width=1)
    d.rectangle([x, y, x + w, y + 14], fill=NAVY)
    d.rectangle([x, y, x + 14, y + 14], fill=RED)
    d.text((x + 7, y + 2), str(n), font=F_BOLD(8), fill=WHITE, anchor="ma")
    d.text((x + 17, y + 3), region, font=F_BOLD(7), fill=WHITE)
    tile = Image.new("RGB", (17, 17), TINT_PALE)
    td = ImageDraw.Draw(tile)
    draw_mini(td, kind, 1, 1, 15, TINT_PALE, NAVY)
    big = tile.resize((20, 20), Image.NEAREST)
    d._image.paste(big, (x + 6, y + 20))
    lx = x + 32
    for i, lw in enumerate([66, 48]):
        ly = y + 26 + i * 10
        d.rectangle([lx, ly, lx + lw, ly + 3], fill=CAPTION_GREY)


HEROES = [
    ("flame", True,
     "Houthis claim strikes on Saudi refinery and Riyadh",
     "Group says it hit Ras Tanura refinery and the capital's "
     "financial district; coalition says it shot down 4 drones.",
     "MIDDLE EAST | CONFLICT", "MIDDLE EAST – PAGE 2"),
    ("rocket", False,
     "Shenzhou-24 lifts off with first foreign astronaut",
     "China's crew to Tiangong includes Pakistani Muhammad Zeeshan "
     "Ali, the first foreign visitor to the station.",
     "ASIA | SPACE", "ASIA – PAGE 3"),
    ("bars", False,
     "BBC: at least 490,334 Russian soldiers dead",
     "BBC and Mediazona count from leaked Rosstat records since "
     "Feb 2022; the true toll is likely higher.",
     "EUROPE | CONFLICT", "EUROPE – PAGE 4"),
]

EIGHT = [
    (4, "chart", "ASIA", "Asian markets tumble in renewed AI sell-off",
     "BUSINESS – PAGE 5"),
    (5, "shield", "OCEANIA", "Australia signs security pact with Solomons",
     "POLITICS – PAGE 6"),
    (6, "exit", "ASIA", "North Korea expels Swiss top diplomat",
     "POLITICS – PAGE 7"),
    (7, "target", "MIDDLE EAST", "Coalition strikes Hodeidah port",
     "WORLD – PAGE 8"),
    (8, "rocket", "EUROPE", "ESA to show first Hera images of Dimorphos",
     "SCIENCE – PAGE 9"),
    (9, "ball", "EUROPE", "Madrid hit PSV 5-1; Arsenal and City draw",
     "SPORT – PAGE 10"),
    (10, "warn", "ASIA", "26 miners trapped in West Java gold mine",
     "WORLD – PAGE 11"),
    (11, "court", "ASIA", "India top court refuses bail to Khalid and Imam",
     "COURTS – PAGE 12"),
]

# Numbered list, city datelines, trimmed to fit one line each.
LISTED = [
    (12, "JERUSALEM", "Eisenkot–Lieberman pact"),
    (13, "JEDDAH", "Houthis threaten ports"),
    (14, "GAZA", "Strike reported in Shati camp"),
    (15, "ISRAEL", "Palestinians face raids"),
    (16, "ODESA", "Russian strike kills 2"),
    (17, "WASHINGTON", "US shelves Russia deal"),
    (18, "MADRID", "Spain vote turns on housing"),
    (19, "PARIS", "Sarkozy and Bruni to trial"),
    (20, "TAIPEI", "AI fakes target election"),
    (21, "SHANGHAI", "Pledges loyalty to Beijing"),
    (22, "BEIJING", "Politburo down to 21"),
    (23, "MADRID", "Ábrego leaves US"),
    (24, "ALASKA", "Ends voter-data deal"),
    (25, "IOWA", "Set for lead-azide blast"),
    (26, "WASHINGTON", "55% want Iran war over"),
    (27, "MUMBAI", "Sensex rises 1.68%"),
    (28, "WASHINGTON", "AG ducks Nvidia probe"),
    (29, "SAHEL", "Insurgents fly cheap drones"),
    (30, "GLOBAL", "Landmine toll hits 6,929"),
    (31, "PRETORIA", "Convicts Russia-case man"),
    (32, "CANBERRA", "Inflation jumps to 4.9%"),
    (33, "SYDNEY", "Ex-officer guilty of murder"),
    (34, "LONDON", "Oil falls, Brent $90.97"),
    (35, "CANBERRA", "Plans duty-of-care law"),
]

NUMBERS = [
    ("chart", "-2.3%", "MSCI Asia ex-Japan", "falls in AI sell-off"),
    ("flame", "490,334", "Russian war dead,", "by the BBC's count"),
    ("drop", "$90.97", "Brent crude", "falls on glut fears"),
    ("poll", "4.9%", "Australia CPI,", "year to October"),
    ("target", "6,929", "landmine casualties", "in 2025, 84% civilians"),
    ("warn", "26", "miners trapped in", "West Java gold mine"),
]

STATS_LINE = ("35 STORIES, ALL FROM WEDNESDAY 25 NOV  •  ASIA 9  •  EUROPE 7  •  "
              "MIDDLE EAST 6  •  AMERICAS 5  •  OCEANIA 4  •  AFRICA 3  •  WORLD 1")

CONTINENTS = [
    [(-168, 66), (-150, 70), (-130, 71), (-115, 68), (-100, 69), (-90, 68),
     (-82, 66), (-76, 62), (-65, 60), (-60, 55), (-55, 47), (-60, 44),
     (-70, 42), (-75, 38), (-81, 31), (-84, 30), (-90, 21), (-97, 16),
     (-92, 15), (-86, 12), (-83, 9), (-80, 8), (-86, 13), (-92, 14),
     (-97, 16), (-105, 20), (-110, 24), (-114, 29), (-120, 34), (-124, 42),
     (-125, 49), (-132, 56), (-145, 60), (-158, 58)],
    [(-80, 8), (-77, 4), (-75, -2), (-80, -6), (-81, -12), (-77, -18),
     (-70, -23), (-65, -30), (-58, -35), (-62, -41), (-65, -45), (-68, -50),
     (-70, -54), (-66, -55), (-68, -50), (-62, -42), (-58, -34), (-52, -28),
     (-48, -22), (-41, -18), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
     (-50, 0), (-55, 4), (-60, 8), (-70, 11), (-77, 8)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50), (2, 51),
     (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (12, 62),
     (18, 66), (21, 70), (25, 71), (30, 70), (32, 68), (40, 68), (44, 68),
     (40, 64), (35, 60), (30, 60), (28, 58), (24, 58), (21, 55), (18, 54),
     (15, 54), (12, 54), (8, 54), (3, 52), (-5, 50), (-10, 48), (-9, 43)],
    [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
     (-12, 8), (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (9, 0), (12, -4),
     (13, -10), (12, -17), (14, -22), (16, -28), (19, -34), (26, -34),
     (32, -29), (35, -24), (40, -16), (40, -10), (42, -4), (46, 0), (51, 2),
     (51, 10), (48, 11), (44, 11), (40, 15), (38, 18), (37, 22), (34, 27),
     (32, 31), (25, 32), (19, 33), (11, 34), (10, 37), (5, 37)],
    [(32, 36), (36, 36), (36, 42), (40, 44), (44, 42), (48, 40), (50, 38),
     (54, 38), (57, 36), (60, 37), (62, 40), (66, 42), (70, 44), (75, 45),
     (80, 48), (85, 50), (90, 52), (95, 55), (100, 58), (105, 60),
     (110, 62), (115, 65), (120, 68), (125, 70), (130, 71), (135, 72),
     (140, 72), (145, 72), (150, 70), (155, 68), (160, 66), (162, 62),
     (158, 58), (156, 52), (150, 48), (142, 45), (140, 40), (135, 38),
     (130, 35), (127, 35), (122, 32), (120, 28), (115, 25), (110, 20),
     (108, 15), (105, 10), (103, 8), (100, 8), (98, 10), (97, 15),
     (95, 16), (92, 20), (90, 22), (88, 22), (86, 20), (84, 18), (80, 15),
     (77, 10), (76, 8), (74, 12), (72, 18), (70, 22), (68, 24), (66, 25),
     (62, 25), (60, 25), (57, 26), (54, 26), (52, 28), (50, 29), (48, 30),
     (44, 30), (42, 32), (40, 35), (36, 36)],
    [(114, -22), (114, -30), (116, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (137, -38), (140, -38), (142, -39), (145, -38),
     (147, -39), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -15), (142, -11), (140, -17), (136, -15), (135, -12), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20)],
]

MAP_DOTS = [
    (1, 56.0, 27.0), (2, 100.0, 40.0), (3, 36.0, 50.0), (5, 149.1, -35.3),
    (6, 128.0, 42.0), (7, 40.0, 13.0), (8, 10.0, 53.0), (9, -6.0, 39.0),
    (10, 106.8, -6.6), (11, 77.2, 28.6), (14, 34.5, 31.5),
    (25, -93.5, 41.6), (29, -4.0, 17.0),
]


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 24

    # ---- Navy top bar with a small globe ----
    d.rectangle([0, 0, W, 34], fill=NAVY)
    d.ellipse([16, 9, 32, 25], outline=WHITE, width=1)
    d.line([(16, 17), (32, 17)], fill=WHITE, width=1)
    d.line([(24, 9), (24, 25)], fill=WHITE, width=1)
    d.text((40, 10), "THE WORLD IN ONE DAY", font=F_BOLD(12), fill=WHITE)
    d.text((W - mx, 10), "WEDNESDAY 25 NOVEMBER 2026",
           font=F_BOLD(12), fill=WHITE, anchor="ra")

    # ---- Giant black serif masthead, centred ----
    d.text((W / 2, 42), "Wednesday 25 November 2026",
           font=F_SERIF_BL(48), fill=INK, anchor="ma")

    # ---- Stats strip, centred ----
    d.rectangle([mx, 102, W - mx, 103], fill=INK)
    d.text((W / 2, 108), STATS_LINE, font=F_BOLD(11), fill=INK, anchor="ma")
    d.rectangle([mx, 130, W - mx, 131], fill=INK)

    # ---- Numbers band: pale blue, icon + big number + 2-line caption ----
    d.rectangle([0, 134, W, 210], fill=NUM_BAND)
    for i, (icon, num, cap1, cap2) in enumerate(NUMBERS):
        cx = mx + i * 163
        if i > 0:
            d.line([(cx - 8, 140), (cx - 8, 204)], fill=WHITE, width=1)
        draw_icon(d, icon, cx + 2, 158, 30, NUM_BAND, NAVY)
        d.text((cx + 38, 144), num, font=F_SERIF_BL(24), fill=NAVY)
        d.text((cx + 38, 176), cap1, font=F_REG(9), fill=INK)
        d.text((cx + 38, 188), cap2, font=F_REG(9), fill=INK)
    d.rectangle([mx, 210, W - mx, 211], fill=INK)

    # ---- THREE HEROES side by side, one row ----
    # Hairlines in the gutters make the 3-column grid visible.
    for gx in (344, 672):
        d.line([(gx, 218), (gx, 556)], fill=HAIRLINE, width=1)
    for idx, hero in enumerate(HEROES):
        kind, is_claim, head, summ, strip, secpage = hero
        x = mx + idx * (312 + 16)
        y = 218
        # Scene below the top band (scenes are drawn for ~206 tall).
        draw_hero_scene(d, kind, x, y + 24, 312, 206)
        # Number + section band on top of the picture, as in the reference.
        d.rectangle([x, y, x + 312, y + 24], fill=NAVY)
        d.rectangle([x, y, x + 24, y + 24], fill=RED)
        d.text((x + 12, y + 4), str(idx + 1), font=F_BOLD(12), fill=WHITE,
               anchor="ma")
        d.text((x + 30, y + 5), strip, font=F_BOLD(10), fill=WHITE)
        if is_claim:
            d.rectangle([x + 312 - 58, y, x + 312, y + 24], fill=RED)
            d.text((x + 312 - 29, y + 5), "CLAIM", font=F_BOLD(10),
                   fill=WHITE, anchor="ma")
        d.rectangle([x, y, x + 312, y + 230], outline=INK, width=2)
        hy = y + 238
        for line in wrap(d, head, F_SERIF_B(20), 312)[:2]:
            d.text((x, hy), line, font=F_SERIF_B(20), fill=INK)
            hy += 24
        sy = y + 294
        for line in wrap(d, summ, F_REG(11), 312)[:2]:
            d.text((x, sy), line, font=F_REG(11), fill=(52, 48, 40))
            sy += 14
        d.text((x, y + 326), secpage, font=F_BOLD(9), fill=NAVY)

    # ---- THE DAY IN EIGHT: navy bar + ONE ROW of 8 cards ----
    ey = 568
    d.rectangle([0, ey, W, ey + 26], fill=NAVY)
    d.text((mx, ey + 6), "THE DAY IN EIGHT", font=F_BOLD(12), fill=WHITE)
    d.text((W - mx, ey + 6), "EVERY PICTURE DATED, EVERY STORY SOURCED",
           font=F_BOLD(10), fill=WHITE, anchor="ra")
    # 8 columns of 108, gutter 16, margin 24.
    for i, (n, kind, region, head, secpage) in enumerate(EIGHT):
        x = mx + i * (108 + 16)
        y = ey + 34
        draw_eight_card(d, n, kind, region, x, y, 108, 76)
        hy = y + 84
        for line in wrap(d, head, F_SERIF_B(11), 108)[:3]:
            d.text((x, hy), line, font=F_SERIF_B(11), fill=INK)
            hy += 14
        d.text((x, y + 130), secpage, font=F_BOLD(8), fill=NAVY)

    # ---- ALSO ON WEDNESDAY: navy bar, map + 3-column list + date check ----
    ay = 756
    d.rectangle([0, ay, W, ay + 26], fill=NAVY)
    d.text((mx, ay + 6), "ALSO ON WEDNESDAY — 24 MORE STORIES",
           font=F_BOLD(12), fill=WHITE)
    # Hairlines between map / list columns.
    for vx in (282, 475, 668):
        d.line([(vx, ay + 34), (vx, ay + 184)], fill=HAIRLINE, width=1)
    map_x, map_y, map_w, map_h = mx, ay + 34, 250, 150

    def project(lon, lat):
        px = map_x + (lon + 170) / 360.0 * map_w
        py = map_y + (75 - lat) / 130.0 * map_h
        return (px, py)

    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=OCEAN)
    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly],
                  fill=LAND, outline=LAND_LINE)
    d.ellipse([project(139, 39)[0] - 2, project(139, 39)[1] - 3,
               project(139, 39)[0] + 2, project(139, 39)[1] + 3],
              fill=LAND, outline=LAND_LINE)
    d.ellipse([project(-2, 54)[0] - 3, project(-2, 54)[1] - 3,
               project(-2, 54)[0] + 3, project(-2, 54)[1] + 3],
              fill=LAND, outline=LAND_LINE)
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=INK, width=2)
    for n, lon, lat in MAP_DOTS:
        px, py = project(lon, lat)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=WHITE, width=1)
        d.text((px, py - 4), str(n), font=F_BOLD(7),
               fill=WHITE, anchor="ma")

    for i, (n, city, text) in enumerate(LISTED):
        col = i // 8
        row = i % 8
        x = 290 + col * 193
        y = ay + 36 + row * 17
        d.text((x, y), f"{n}.", font=F_BOLD(9), fill=INK)
        d.text((x + 20, y), f"{city}: ", font=F_BOLD(9), fill=INK)
        cw = d.textlength(f"{city}: ", font=F_BOLD(9))
        d.text((x + 20 + cw, y), text, font=F_REG(9), fill=INK)

    # Date check box (navy header, 3 bullets + sources).
    bx, by, bw, bh = 874, ay + 34, 126, 150
    d.rectangle([bx, by, bx + bw, by + bh], fill=WHITE, outline=INK, width=2)
    d.rectangle([bx, by, bx + bw, by + 24], fill=NAVY)
    d.text((bx + 8, by + 5), "DATE CHECK", font=F_BOLD(12), fill=WHITE)
    bullets = [
        "Wed, 25 Nov: Houthis claim Saudi refinery strikes",
        "Wed, 25 Nov: Shenzhou-24 launches",
        "Wed, 25 Nov: BBC counts 490,334 war dead",
    ]
    ty = by + 30
    for b in bullets:
        for line in wrap(d, "•  " + b, F_REG(8), bw - 16):
            d.text((bx + 8, ty), line, font=F_REG(8), fill=INK)
            ty += 10
        ty += 2
    ty += 2
    d.line([(bx + 8, ty), (bx + bw - 8, ty)], fill=HAIRLINE, width=1)
    ty += 5
    for line in wrap(d, "Sources: Reuters, BBC, AP, Al Jazeera, Xinhua, "
                    "UEFA, ESA, ABS, LiveLaw.", F_REG(7), bw - 16):
        d.text((bx + 8, ty), line, font=F_REG(7), fill=GREY)
        ty += 9

    # ---- Navy footer strip ----
    d.rectangle([0, 962, W, H], fill=NAVY)
    d.text((mx, 982),
           "WORLD  |  BUSINESS  |  POLITICS  |  TECHNOLOGY  |  SCIENCE  |  "
           "HEALTH  |  SPORTS  |  ENTERTAINMENT",
           font=F_BOLD(11), fill=WHITE)
    d.text((W - mx, 982), "A more informed world. Every day.",
           font=F_SERIF_I(10), fill=(200, 196, 184), anchor="ra")

    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print("wrote", out, os.path.getsize(out), "bytes")
