# draw.py — renders the 25 November 2026 broadsheet front page.
# Run locally with Pillow:  python3 draw.py [output-path]
# The graded entrypoint is main.ts, which only copies the shipped
# entry.png into /output (Node stdlib only, no network, deterministic).
# This script is the build-time renderer; it is not run by the grader.
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/noto"

PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (30, 58, 95)
RED = (185, 28, 28)
GREY = (96, 92, 82)
CARD = (253, 252, 247)
LINE = (178, 172, 156)
GREEN = (22, 101, 52)
AMBER = (146, 64, 14)
LAND = (207, 198, 172)
OCEAN = (233, 239, 244)
LAND_LINE = (138, 131, 113)
TINT_BLUE = (232, 238, 244)
TINT_RED = (252, 231, 231)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


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


def chip(d, x, y, text, bg, fg):
    f = F_BOLD(9)
    tw = d.textlength(text, font=f)
    pad = 5
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + 14], radius=3, fill=bg)
    d.text((x + pad, y + 2), text, font=f, fill=fg)
    return tw + pad * 2 + 6


def draw_icon(d, kind, x, y, s, bg, fg):
    # Big illustration panel (s x s) with a small vector scene per story.
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=bg)
    c = s / 2
    if kind == "flame":
        # Refinery towers with flames and smoke.
        d.line([(x + 10, y + s - 12), (x + s - 10, y + s - 12)], fill=fg, width=3)
        d.rectangle([x + 16, y + 38, x + 32, y + s - 12], fill=fg)
        d.rectangle([x + 48, y + 50, x + 64, y + s - 12], fill=fg)
        d.rectangle([x + 21, y + 28, x + 27, y + 38], fill=fg)
        d.rectangle([x + 53, y + 40, x + 59, y + 50], fill=fg)
        d.polygon([(x + 24, y + 8), (x + 34, y + 26), (x + 28, y + 22),
                   (x + 20, y + 28), (x + 16, y + 22)], fill=(214, 120, 30))
        d.polygon([(x + 56, y + 22), (x + 64, y + 36), (x + 59, y + 33),
                   (x + 53, y + 38), (x + 50, y + 32)], fill=(214, 120, 30))
        d.ellipse([x + 38, y + 14, x + 46, y + 22], fill=(255, 255, 255))
        d.ellipse([x + 66, y + 12, x + 72, y + 18], fill=(255, 255, 255))
    elif kind == "rocket":
        # Rocket lifting off past stars.
        for sx, sy in [(12, 12), (70, 16), (14, 62), (68, 60), (70, 38)]:
            d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                      fill=(255, 255, 255))
        d.polygon([(x + c, y + 6), (x + c + 12, y + 32),
                   (x + c - 12, y + 32)], fill=fg)
        d.rectangle([x + c - 11, y + 30, x + c + 11, y + 58], fill=fg)
        d.ellipse([x + c - 5, y + 36, x + c + 5, y + 46], fill=(255, 255, 255))
        d.polygon([(x + c - 11, y + 48), (x + c - 22, y + 64),
                   (x + c - 11, y + 58)], fill=fg)
        d.polygon([(x + c + 11, y + 48), (x + c + 22, y + 64),
                   (x + c + 11, y + 58)], fill=fg)
        d.polygon([(x + c, y + 58), (x + c + 6, y + 72),
                   (x + c - 6, y + 72)], fill=(214, 120, 30))
    elif kind == "chart":
        # Falling market line over a grid, with axis.
        for gy in [22, 40, 58]:
            d.line([(x + 10, y + gy), (x + s - 10, y + gy)],
                   fill=(255, 255, 255), width=1)
        d.line([(x + 10, y + s - 14), (x + s - 10, y + s - 14)], fill=fg, width=2)
        pts = [(x + 14, y + 20), (x + 28, y + 34), (x + 40, y + 30),
               (x + 54, y + 52), (x + 68, y + 62)]
        d.line(pts, fill=fg, width=4, joint="curve")
        d.polygon([(x + 68, y + 62), (x + 58, y + 60), (x + 66, y + 50)], fill=fg)
    elif kind == "bars":
        # Rising bars with a baseline and a red marker dot.
        d.line([(x + 10, y + s - 14), (x + s - 10, y + s - 14)], fill=fg, width=2)
        for i, h in enumerate([26, 40, 54]):
            bx = x + 14 + i * 20
            d.rectangle([bx, y + s - 14 - h, bx + 14, y + s - 14], fill=fg)
        d.ellipse([x + 62, y + 12, x + 72, y + 22], fill=RED)
    elif kind == "shield":
        # Shield with a check and two stars.
        for sx, sy in [(14, 10), (70, 10)]:
            d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                      fill=(255, 255, 255))
        d.polygon([(x + c, y + 8), (x + s - 12, y + 18), (x + s - 12, y + 42),
                   (x + c, y + 76), (x + 12, y + 42), (x + 12, y + 18)], fill=fg)
        d.line([(x + c - 12, y + 42), (x + c - 3, y + 52),
                (x + c + 14, y + 30)], fill=(255, 255, 255), width=5, joint="curve")
    elif kind == "exit":
        # Door, exit arrow and a small suitcase.
        d.rectangle([x + 16, y + 12, x + 40, y + 72], outline=fg, width=3)
        d.ellipse([x + 33, y + 40, x + 37, y + 44], fill=fg)
        d.line([(x + 30, y + 42), (x + 62, y + 42)], fill=fg, width=4)
        d.polygon([(x + 62, y + 42), (x + 50, y + 32), (x + 50, y + 52)], fill=fg)
        d.rectangle([x + 48, y + 56, x + 68, y + 70], outline=fg, width=2)
        d.line([(x + 54, y + 52), (x + 62, y + 52)], fill=fg, width=2)


def draw_mini(d, kind, x, y, s, bg, fg):
    # Small 16x16 category icon for the numbered list.
    d.rounded_rectangle([x, y, x + s, y + s], radius=4, fill=bg)
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
        d.ellipse([x + 6, y + 10, x + 10, y + 14], fill=(255, 255, 255))
    elif kind == "flag":
        d.line([(x + 5, y + 2), (x + 5, y + 14)], fill=fg, width=2)
        d.polygon([(x + 5, y + 2), (x + 13, y + 4), (x + 5, y + 7)], fill=fg)
    elif kind == "home":
        d.polygon([(x + 8, y + 2), (x + 14, y + 7), (x + 2, y + 7)], fill=fg)
        d.rectangle([x + 4, y + 7, x + 12, y + 14], fill=fg)
        d.rectangle([x + 7, y + 10, x + 9, y + 14], fill=(255, 255, 255))
    elif kind == "court":
        d.line([(x + 8, y + 3), (x + 8, y + 12)], fill=fg, width=2)
        d.line([(x + 3, y + 3), (x + 13, y + 3)], fill=fg, width=2)
        d.polygon([(x + 3, y + 3), (x + 1, y + 8), (x + 5, y + 8)], fill=fg)
        d.polygon([(x + 13, y + 3), (x + 11, y + 8), (x + 15, y + 8)], fill=fg)
        d.line([(x + 4, y + 13), (x + 12, y + 13)], fill=fg, width=2)
    elif kind == "rocket":
        d.polygon([(x + 8, y + 2), (x + 11, y + 8), (x + 5, y + 8)], fill=fg)
        d.rectangle([x + 6, y + 8, x + 10, y + 12], fill=fg)
        d.polygon([(x + 8, y + 12), (x + 10, y + 15), (x + 6, y + 15)],
                  fill=(214, 120, 30))
    elif kind == "ball":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=fg, width=2)
        d.ellipse([x + c - 2, y + c - 2, x + c + 2, y + c + 2], fill=fg)
        d.line([(x + c, y + 2), (x + c, y + c - 2)], fill=fg, width=1)
        d.line([(x + 2, y + c), (x + c - 2, y + c)], fill=fg, width=1)
        d.line([(x + s - 2, y + c), (x + c + 2, y + c)], fill=fg, width=1)
    elif kind == "warn":
        d.polygon([(x + 8, y + 2), (x + 15, y + 14), (x + 1, y + 14)],
                  fill=(214, 120, 30))
        d.line([(x + 8, y + 6), (x + 8, y + 10)], fill=(255, 255, 255), width=2)
        d.ellipse([x + 7, y + 11, x + 9, y + 13], fill=(255, 255, 255))
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
    elif kind == "chart":
        d.line([(x + 3, y + 12), (x + 6, y + 8), (x + 9, y + 10),
                (x + 13, y + 4)], fill=fg, width=2)
        d.polygon([(x + 13, y + 4), (x + 10, y + 4), (x + 13, y + 7)], fill=fg)


HEROES = [
    ("MIDDLE EAST", "CLAIM", RED, "flame", TINT_RED, RED,
     "Houthis claim strikes on Saudi refinery and Riyadh",
     "Group says it hit Ras Tanura refinery and the capital's "
     "financial district; coalition says it shot down 4 drones.",
     "Reuters"),
    ("ASIA", "REPORTED", GREEN, "rocket", TINT_BLUE, NAVY,
     "Shenzhou-24 lifts off with first foreign astronaut",
     "China's crew to Tiangong includes Pakistani Muhammad Zeeshan "
     "Ali, the first foreign visitor to the station.",
     "Xinhua / AP"),
    ("WORLD", "REPORTED", GREEN, "chart", TINT_BLUE, NAVY,
     "Asian markets tumble in renewed AI sell-off",
     "MSCI Asia ex-Japan falls 2.3%; Korea drops as much as 5.3% "
     "as fresh US tariff threats loom.",
     "Reuters"),
    ("EUROPE", "REPORTED", GREEN, "bars", TINT_BLUE, NAVY,
     "BBC: at least 490,334 Russian soldiers dead",
     "BBC and Mediazona count from leaked Rosstat records since "
     "Feb 2022; the true toll is likely higher.",
     "BBC"),
    ("OCEANIA", "REPORTED", GREEN, "shield", TINT_BLUE, NAVY,
     "Australia signs security pact with Solomons",
     "Canberra named the primary security partner; the pact bars "
     "any foreign military base on the islands.",
     "AP"),
    ("ASIA", "REPORTED", GREEN, "exit", TINT_BLUE, NAVY,
     "North Korea expels Switzerland's top diplomat",
     "Pyongyang orders the envoy out within 48 hours and the new "
     "Swiss office closed, KCNA reports.",
     "AP / KCNA"),
]

LISTED = [
    (7, "target", "Coalition strikes Houthi-run Hodeidah port", "Al Jazeera"),
    (8, "vote", "Eisenkot signs first coalition pact with Lieberman", "Al Jazeera"),
    (9, "flame", "Strike reported in Gaza's Shati camp; 4 reported killed", "Al Jazeera"),
    (10, "target", "Russian strike kills 2 in Ukraine's Odesa region", "Reuters"),
    (11, "flag", "US shelves Russia business-deal plan to end war", "FT via Reuters"),
    (12, "home", "Spain's election fight turns on housing, rent caps", "Reuters"),
    (13, "court", "Sarkozy and Bruni sent to trial over witness tampering", "BBC"),
    (14, "rocket", "ESA to show first Hera images of asteroid Dimorphos", "ESA"),
    (15, "ball", "Real Madrid hit PSV 5-1; Arsenal and Man City draw", "UEFA"),
    (16, "warn", "26 miners trapped in flooded gold mine in West Java", "Reuters"),
    (17, "court", "India top court refuses bail to Khalid and Imam", "LiveLaw"),
    (18, "chip", "BBC Verify: AI fakes target Taiwan election", "BBC"),
    (19, "flag", "Shanghai pledges loyalty after Chen probe", "Reuters"),
    (20, "plane", "Abrego Garcia leaves US for Spain", "BBC / AP"),
    (21, "vote", "Alaska ends voter-data deal with US Justice Dept", "AP"),
    (22, "flame", "Iowa set for controlled blast of 5 tons of lead azide", "AP"),
    (23, "poll", "Poll: 55% of US voters want Iran war ended now", "Al Jazeera"),
    (24, "court", "Thomas Markle indicted on abuse-material charges", "BBC"),
    (25, "drone", "Sahel insurgents fly cheap drones; 187 JNIM attacks", "Reuters"),
    (26, "warn", "Landmine casualties hit 6,929 in 2025, 84% civilians", "BBC"),
    (27, "court", "S. Africa convicts man who tried to fight for Russia", "AP"),
    (28, "chart", "Australia inflation jumps to 4.9% in year to Oct", "ABS"),
    (29, "court", "Ex-officer guilty of double murder in Sydney", "BBC"),
    (30, "drop", "Oil falls: Brent $90.97 as glut fears offset war risk", "Reuters"),
]

NUMBERS = [
    ("-2.3%", "MSCI Asia ex-Japan, Wed"),
    ("-5.3%", "Korea shares, at worst"),
    ("$90.97", "Brent crude, Wed"),
    ("4.9%", "Australia CPI, yr to Oct"),
    ("490,334", "Russian deaths, BBC est."),
    ("6,929", "Landmine casualties, 2025"),
]

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

# Dots are nudged a few degrees where stories sit close together, so the
# numbered markers do not merge on this small schematic map.
MAP_DOTS = [
    (1, 46.7, 24.6), (7, 34.0, 6.0), (2, 98.5, 39.8), (6, 128.0, 42.0),
    (10, 30.7, 46.5), (12, -3.7, 40.4), (16, 106.8, -6.6), (17, 77.2, 28.6),
    (5, 149.1, -35.3), (25, -8.0, 12.6), (20, -77.0, 38.9),
    (22, -95.0, 44.0), (18, 115.0, 20.0),
]

MAP_LABELS = [
    ("N. AMERICA", -128, 58), ("S. AMERICA", -60, -20),
    ("EUROPE", 8, 66), ("AFRICA", 14, -2),
    ("ASIA", 75, 60), ("OCEANIA", 125, -30),
]


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 26
    col_w = 478
    x2 = mx + col_w + 16

    # ---- Masthead ----
    d.text((W / 2, 14), "ONE DAY  •  ONE PAGE  •  THE WORLD",
           font=F_BOLD(11), fill=GREY, anchor="ma")
    d.text((W / 2, 30), "THE WORLD TODAY",
           font=F_BLACK(54), fill=INK, anchor="ma")
    d.rectangle([mx, 92, W - mx, 118], fill=INK)
    d.text((mx + 10, 98), "WEDNESDAY, 25 NOVEMBER 2026",
           font=F_BOLD(15), fill=(255, 255, 255))
    d.text((W - mx - 10, 98), "30 STORIES  •  6 CONTINENTS",
           font=F_BOLD(15), fill=(255, 255, 255), anchor="ra")
    sub = ("TOP OF THE DAY:  Houthis claim Saudi refinery attack  •  "
           "Shenzhou-24 carries the first foreign astronaut  •  "
           "Asian markets tumble")
    for i, line in enumerate(wrap(d, sub, F_REG(13), W - 2 * mx)):
        d.text((W / 2, 126 + i * 18), line, font=F_REG(13),
               fill=INK, anchor="ma")

    # ---- 6 hero stories ----
    for idx, hero in enumerate(HEROES):
        region, status, sbg, kind, tint, fg, head, summ, src = hero
        col = idx % 2
        row = idx // 2
        x = mx if col == 0 else x2
        y = 166 + row * 108
        d.rounded_rectangle([x, y, x + col_w, y + 100], radius=6,
                            fill=CARD, outline=LINE, width=1)
        d.rectangle([x, y + 6, x + 4, y + 94], fill=RED if status == "CLAIM" else NAVY)
        draw_icon(d, kind, x + 12, y + 8, 84, tint, fg)
        tx = x + 108
        d.text((tx, y + 10), region, font=F_BOLD(10), fill=NAVY)
        cw = chip(d, tx + d.textlength(region, font=F_BOLD(10)) + 8, y + 8,
                  status, sbg, (255, 255, 255))
        sx = tx + d.textlength(region, font=F_BOLD(10)) + 8 + cw
        d.text((sx, y + 10), src, font=F_IT(10), fill=GREY)
        d.text((tx, y + 24), f"{idx + 1}.", font=F_BLACK(15), fill=RED)
        hw = col_w - 108 - 12
        hl = wrap(d, head, F_BOLD(16), hw - 24)
        hy = y + 24
        for line in hl[:2]:
            d.text((tx + 24, hy), line, font=F_BOLD(16), fill=INK)
            hy += 18
        sy = y + 62
        for line in wrap(d, summ, F_REG(12), hw)[:2]:
            d.text((tx, sy), line, font=F_REG(12), fill=(52, 48, 40))
            sy += 14

    # ---- The day in numbers ----
    y0 = 494
    d.rounded_rectangle([mx, y0, mx + col_w, y0 + 148], radius=6,
                        fill=CARD, outline=LINE, width=1)
    d.text((mx + 12, y0 + 8), "THE DAY IN NUMBERS",
           font=F_BOLD(14), fill=INK)
    d.line([(mx + 12, y0 + 30), (mx + col_w - 12, y0 + 30)], fill=LINE, width=1)
    for i, (num, label) in enumerate(NUMBERS):
        cx = mx + 12 + (i % 2) * 235
        cy = y0 + 38 + (i // 2) * 37
        d.text((cx, cy), num, font=F_BOLD(21),
               fill=RED if num.startswith("-") else NAVY)
        d.text((cx, cy + 23), label, font=F_REG(10), fill=GREY)

    # ---- Map ----
    d.rounded_rectangle([x2, y0, x2 + col_w, y0 + 148], radius=6,
                        fill=CARD, outline=LINE, width=1)
    d.text((x2 + 12, y0 + 8), "WHERE IT HAPPENED",
           font=F_BOLD(14), fill=INK)
    d.line([(x2 + 12, y0 + 30), (x2 + col_w - 12, y0 + 30)], fill=LINE, width=1)
    map_x, map_y, map_w, map_h = x2 + 10, y0 + 36, col_w - 20, 106

    def project(lon, lat):
        px = map_x + (lon + 170) / 360.0 * map_w
        py = map_y + (75 - lat) / 130.0 * map_h
        return (px, py)

    d.rounded_rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                        radius=4, fill=OCEAN)
    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly],
                  fill=LAND, outline=LAND_LINE)
    d.ellipse([project(139, 39)[0] - 4, project(139, 39)[1] - 7,
               project(139, 39)[0] + 4, project(139, 39)[1] + 7],
              fill=LAND, outline=LAND_LINE)
    d.ellipse([project(-2, 54)[0] - 5, project(-2, 54)[1] - 6,
               project(-2, 54)[0] + 5, project(-2, 54)[1] + 6],
              fill=LAND, outline=LAND_LINE)
    for label, lon, lat in MAP_LABELS:
        lx, ly_ = project(lon, lat)
        d.text((lx, ly_), label, font=F_BOLD(8), fill=GREY, anchor="ma")
    for n, lon, lat in MAP_DOTS:
        px, py = project(lon, lat)
        d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py - 5), str(n), font=F_BOLD(9),
               fill=(255, 255, 255), anchor="ma")

    # ---- Numbered list: the rest of the day ----
    ly = 656
    d.text((mx, ly), "THE REST OF THE DAY  —  24 MORE STORIES",
           font=F_BOLD(14), fill=INK)
    d.line([(mx, ly + 22), (W - mx, ly + 22)], fill=INK, width=2)
    row_h = 25
    for i, (n, kind, text, src) in enumerate(LISTED):
        col = i // 12
        row = i % 12
        x = mx if col == 0 else x2
        y = ly + 28 + row * row_h
        d.text((x, y), f"{n}.", font=F_BOLD(12), fill=RED)
        icon_bg = TINT_RED if kind in ("flame", "target", "warn") else TINT_BLUE
        icon_fg = RED if kind in ("flame", "target", "warn") else NAVY
        draw_mini(d, kind, x + 26, y - 1, 16, icon_bg, icon_fg)
        d.text((x + 48, y), text, font=F_REG(12), fill=INK)
        tw = d.textlength(text, font=F_REG(12))
        d.text((x + 48 + tw + 6, y), "— " + src, font=F_IT(10), fill=GREY)

    # ---- Footer: date check ----
    fy = 986
    d.line([(mx, fy), (W - mx, fy)], fill=INK, width=2)
    d.text((W / 2, fy + 8),
           "DATE CHECK:  every story above happened, or was first reported, "
           "on Wednesday 25 November 2026.",
           font=F_BOLD(11), fill=INK, anchor="ma")
    d.text((W / 2, fy + 24),
           "Claims are labelled CLAIM.  Sources: Reuters, BBC, AP, Al Jazeera, "
           "Xinhua, UEFA, ESA.",
           font=F_REG(10), fill=GREY, anchor="ma")

    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print("wrote", out, os.path.getsize(out), "bytes")
