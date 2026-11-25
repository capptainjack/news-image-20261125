# draw.py — renders the 25 November 2026 broadsheet front page, KOMIK NEON style.
# Run locally with Pillow:  python3 draw.py [output-path]
# The graded entrypoint is main.ts, which only copies the shipped
# entry.png into /output (Node stdlib only, no network, deterministic).
# This script is the build-time renderer; it is not run by the grader.
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/noto"

PAPER = (233, 224, 255)
INK = (12, 12, 12)
PURPLE = (128, 0, 255)
PURPLE_DARK = (90, 0, 180)
GREEN = (0, 200, 120)
GREEN_DARK = (0, 120, 70)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)
RED = (215, 25, 25)
GREY = (74, 68, 92)
ORANGE = (214, 120, 30)
TINT_PURPLE = (214, 180, 255)
TINT_GREEN = (170, 240, 210)
TINT_YELLOW = (255, 238, 140)
TINT_RED = (255, 190, 190)
LAND = (222, 205, 170)
LAND_LINE = (120, 110, 80)
OCEAN = (220, 235, 245)


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
    d.rectangle([x, y, x + tw + pad * 2, y + 14], fill=bg)
    d.text((x + pad, y + 2), text, font=f, fill=fg)
    return tw + pad * 2 + 6


def star(d, cx, cy, r, fill):
    q = r * 0.28
    d.polygon([(cx, cy - r), (cx + q, cy - q), (cx + r, cy),
               (cx + q, cy + q), (cx, cy + r), (cx - q, cy + q),
               (cx - r, cy), (cx - q, cy - q)], fill=fill)


def draw_scene(d, kind, x, y, s, fg):
    # One vector scene drawn in an 84-unit box scaled to s x s.
    k = s / 84.0
    X = lambda v: x + v * k
    Y = lambda v: y + v * k
    if kind == "flame":
        d.line([(X(10), Y(72)), (X(74), Y(72))], fill=fg, width=3)
        d.rectangle([X(16), Y(38), X(32), Y(72)], fill=fg)
        d.rectangle([X(48), Y(50), X(64), Y(72)], fill=fg)
        d.rectangle([X(21), Y(28), X(27), Y(38)], fill=fg)
        d.rectangle([X(53), Y(40), X(59), Y(50)], fill=fg)
        d.polygon([(X(24), Y(8)), (X(34), Y(26)), (X(28), Y(22)),
                   (X(20), Y(28)), (X(16), Y(22))], fill=ORANGE)
        d.polygon([(X(56), Y(22)), (X(64), Y(36)), (X(59), Y(33)),
                   (X(53), Y(38)), (X(50), Y(32))], fill=ORANGE)
        d.ellipse([X(38), Y(14), X(46), Y(22)], fill=WHITE)
        d.ellipse([X(66), Y(12), X(72), Y(18)], fill=WHITE)
    elif kind == "rocket":
        for sx, sy in [(12, 12), (70, 16), (14, 62), (68, 60), (70, 38)]:
            d.ellipse([X(sx - 2), Y(sy - 2), X(sx + 2), Y(sy + 2)], fill=WHITE)
        d.polygon([(X(42), Y(6)), (X(54), Y(32)), (X(30), Y(32))], fill=fg)
        d.rectangle([X(31), Y(30), X(53), Y(58)], fill=fg)
        d.ellipse([X(37), Y(36), X(47), Y(46)], fill=WHITE)
        d.polygon([(X(31), Y(48)), (X(20), Y(64)), (X(31), Y(58))], fill=fg)
        d.polygon([(X(53), Y(48)), (X(64), Y(64)), (X(53), Y(58))], fill=fg)
        d.polygon([(X(42), Y(58)), (X(48), Y(72)), (X(36), Y(72))], fill=ORANGE)
    elif kind == "chart":
        for gy in [22, 40, 58]:
            d.line([(X(10), Y(gy)), (X(74), Y(gy))], fill=WHITE, width=1)
        d.line([(X(10), Y(70)), (X(74), Y(70))], fill=fg, width=2)
        pts = [(X(14), Y(20)), (X(28), Y(34)), (X(40), Y(30)),
               (X(54), Y(52)), (X(68), Y(62))]
        d.line(pts, fill=fg, width=4, joint="curve")
        d.polygon([(X(68), Y(62)), (X(58), Y(60)), (X(66), Y(50))], fill=fg)
    elif kind == "bars":
        d.line([(X(10), Y(70)), (X(74), Y(70))], fill=fg, width=2)
        for i, h in enumerate([26, 40, 54]):
            bx = X(14 + i * 20)
            d.rectangle([bx, Y(70 - h), bx + 14 * k, Y(70)], fill=fg)
        d.ellipse([X(62), Y(12), X(72), Y(22)], fill=RED)
    elif kind == "shield":
        for sx, sy in [(14, 10), (70, 10)]:
            d.ellipse([X(sx - 2), Y(sy - 2), X(sx + 2), Y(sy + 2)], fill=WHITE)
        d.polygon([(X(42), Y(8)), (X(72), Y(18)), (X(72), Y(42)),
                   (X(42), Y(76)), (X(12), Y(42)), (X(12), Y(18))], fill=fg)
        d.line([(X(30), Y(42)), (X(39), Y(52)), (X(56), Y(30))],
               fill=WHITE, width=5, joint="curve")


def draw_panel(d, kind, x, y, w, h, bg, fg):
    # Neon illustration panel: solid colour, thick black frame, stars,
    # and one big vector scene centred in it.
    d.rectangle([x, y, x + w, y + h], fill=bg, outline=INK, width=3)
    star(d, x + 20, y + 18, 7, WHITE)
    star(d, x + w - 20, y + 20, 5, WHITE)
    star(d, x + 26, y + h - 18, 5, WHITE)
    star(d, x + w - 28, y + h - 22, 7, WHITE)
    s = int(min(w, h) * 0.92)
    sx = x + (w - s) // 2
    sy = y + (h - s) // 2
    draw_scene(d, kind, sx, sy, s, fg)


def draw_mini(d, kind, x, y, s, bg, fg):
    # Small 15x15 category icon for the numbered list.
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
    elif kind == "chart":
        d.line([(x + 3, y + 12), (x + 6, y + 8), (x + 9, y + 10),
                (x + 13, y + 4)], fill=fg, width=2)
        d.polygon([(x + 13, y + 4), (x + 10, y + 4), (x + 13, y + 7)], fill=fg)
    elif kind == "exit":
        d.rectangle([x + 3, y + 3, x + 8, y + 13], outline=fg, width=1)
        d.line([(x + 6, y + 8), (x + 13, y + 8)], fill=fg, width=2)
        d.polygon([(x + 13, y + 8), (x + 10, y + 5), (x + 10, y + 11)], fill=fg)


# Colour per list category: (mini icon background, foreground).
ICON_STYLE = {
    "target": (TINT_RED, RED), "flame": (TINT_RED, RED),
    "warn": (TINT_RED, RED),
    "vote": (TINT_PURPLE, PURPLE_DARK), "flag": (TINT_PURPLE, PURPLE_DARK),
    "court": (TINT_PURPLE, PURPLE_DARK), "exit": (TINT_PURPLE, PURPLE_DARK),
    "chart": (TINT_GREEN, GREEN_DARK), "drop": (TINT_GREEN, GREEN_DARK),
    "poll": (TINT_GREEN, GREEN_DARK),
    "rocket": (TINT_YELLOW, (140, 90, 0)), "ball": (TINT_YELLOW, (140, 90, 0)),
    "chip": (TINT_YELLOW, (140, 90, 0)), "drone": (TINT_YELLOW, (140, 90, 0)),
    "plane": (TINT_YELLOW, (140, 90, 0)), "home": (TINT_YELLOW, (140, 90, 0)),
}

BIG_HEROES = [
    ("MIDDLE EAST", "CLAIM", RED, "flame", PURPLE,
     "Houthis claim strikes on Saudi refinery and Riyadh",
     "Group says it hit Ras Tanura refinery and the capital's "
     "financial district; coalition says it shot down 4 drones.",
     "Reuters"),
    ("ASIA", "REPORTED", (0, 160, 95), "rocket", GREEN,
     "Shenzhou-24 lifts off with first foreign astronaut",
     "China's crew to Tiangong includes Pakistani Muhammad Zeeshan "
     "Ali, the first foreign visitor to the station.",
     "Xinhua / AP"),
]

CARDS = [
    ("WORLD", "REPORTED", (0, 160, 95), "chart", GREEN,
     "Asian markets tumble in renewed AI sell-off",
     "MSCI Asia ex-Japan falls 2.3%; Korea down 5.3%.",
     "Reuters"),
    ("EUROPE", "REPORTED", (0, 160, 95), "bars", PURPLE,
     "BBC: at least 490,334 Russian soldiers dead",
     "BBC and Mediazona count from leaked Rosstat records.",
     "BBC"),
    ("OCEANIA", "REPORTED", (0, 160, 95), "shield", YELLOW,
     "Australia signs security pact with Solomons",
     "Canberra named the primary security partner.",
     "AP"),
]

LISTED = [
    (6, "exit", "North Korea expels Switzerland's top diplomat", "AP / KCNA"),
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
    (10, 34.0, 44.0), (12, -10.0, 38.0), (16, 106.8, -6.6), (17, 77.2, 28.6),
    (5, 149.1, -35.3), (25, -8.0, 12.6), (20, -77.0, 38.9),
    (22, -95.0, 44.0), (18, 115.0, 20.0),
]

MAP_LABELS = [
    ("N. AMERICA", -128, 58), ("S. AMERICA", -60, -20),
    ("EUROPE", 8, 68), ("AFRICA", 14, -2),
    ("ASIA", 75, 60), ("OCEANIA", 118, -30),
]


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 24
    col_w = 478
    x2 = mx + col_w + 16

    # ---- Masthead: yellow bar, thick black frame, black date strip ----
    d.rectangle([mx, 16, W - mx, 100], fill=YELLOW, outline=INK, width=4)
    d.text((mx + 16, 24), "THE WORLD TODAY", font=F_BLACK(40), fill=INK)
    d.text((W - mx - 16, 34), "30 STORIES  •  6 CONTINENTS",
           font=F_BOLD(13), fill=INK, anchor="ra")
    d.rectangle([mx, 68, W - mx, 100], fill=INK)
    d.text((mx + 16, 74), "WEDNESDAY, 25 NOVEMBER 2026",
           font=F_BOLD(15), fill=YELLOW)
    d.text((W - mx - 16, 77), "ONE DAY  •  ONE PAGE  •  THE WORLD",
           font=F_BOLD(10), fill=WHITE, anchor="ra")
    sub = ("TOP OF THE DAY:  Houthis claim Saudi refinery attack  •  "
           "Shenzhou-24 carries the first foreign astronaut  •  "
           "Asian markets tumble")
    d.text((W / 2, 110), sub, font=F_BOLD(12), fill=INK, anchor="ma")

    # ---- 2 big heroes ----
    for idx, hero in enumerate(BIG_HEROES):
        region, status, sbg, kind, bg, head, summ, src = hero
        x = mx if idx == 0 else x2
        y = 136
        d.rectangle([x, y, x + col_w, y + 216], fill=WHITE, outline=INK, width=4)
        draw_panel(d, kind, x + 4, y + 4, col_w - 8, 110, bg, INK)
        tx = x + 16
        ty = y + 122
        d.text((tx, ty), region, font=F_BOLD(10), fill=PURPLE_DARK)
        cw = chip(d, tx + d.textlength(region, font=F_BOLD(10)) + 8, ty - 2,
                  status, sbg, WHITE)
        sx = tx + d.textlength(region, font=F_BOLD(10)) + 8 + cw
        d.text((sx, ty), src, font=F_IT(10), fill=GREY)
        hy = ty + 18
        for line in wrap(d, head, F_BLACK(17), col_w - 32)[:2]:
            d.text((tx, hy), line, font=F_BLACK(17), fill=INK)
            hy += 20
        sy = ty + 60
        for line in wrap(d, summ, F_REG(12), col_w - 32)[:2]:
            d.text((tx, sy), line, font=F_REG(12), fill=(52, 48, 40))
            sy += 15

    # ---- 3 story cards ----
    for idx, card in enumerate(CARDS):
        region, status, sbg, kind, bg, head, summ, src = card
        x = mx + idx * (312 + 16)
        y = 364
        d.rectangle([x, y, x + 312, y + 168], fill=WHITE, outline=INK, width=3)
        draw_panel(d, kind, x + 4, y + 4, 304, 80, bg, INK)
        tx = x + 14
        hy = y + 92
        for line in wrap(d, head, F_BOLD(14), 312 - 28)[:2]:
            d.text((tx, hy), line, font=F_BOLD(14), fill=INK)
            hy += 17
        d.text((tx, y + 130), region + "  •  " + src, font=F_BOLD(9), fill=GREY)
        d.text((tx, y + 146), summ, font=F_REG(10), fill=(52, 48, 40))

    # ---- Numbered list: the rest of the day, 25 stories ----
    ly = 544
    d.text((mx, ly), "THE REST OF THE DAY  —  25 MORE STORIES",
           font=F_BLACK(14), fill=INK)
    d.rectangle([mx, ly + 22, W - mx, ly + 25], fill=INK)
    row_h = 18
    for i, (n, kind, text, src) in enumerate(LISTED):
        col = i // 13
        row = i % 13
        x = mx if col == 0 else x2
        y = ly + 30 + row * row_h
        d.text((x, y), f"{n}.", font=F_BOLD(11), fill=RED)
        bg, fg = ICON_STYLE[kind]
        draw_mini(d, kind, x + 24, y - 1, 15, bg, fg)
        d.text((x + 44, y), text, font=F_REG(11), fill=INK)
        tw = d.textlength(text, font=F_REG(11))
        d.text((x + 44 + tw + 6, y), "— " + src, font=F_IT(9), fill=GREY)

    # ---- The day in numbers (yellow) ----
    y0 = 818
    d.rectangle([mx, y0, mx + col_w, y0 + 128], fill=YELLOW, outline=INK, width=3)
    d.text((mx + 12, y0 + 8), "THE DAY IN NUMBERS", font=F_BLACK(13), fill=INK)
    d.rectangle([mx + 12, y0 + 28, mx + col_w - 12, y0 + 30], fill=INK)
    for i, (num, label) in enumerate(NUMBERS):
        cx = mx + 12 + (i % 2) * 235
        cy = y0 + 34 + (i // 2) * 30
        d.text((cx, cy), num, font=F_BOLD(17),
               fill=RED if num.startswith("-") else PURPLE_DARK)
        d.text((cx, cy + 19), label, font=F_REG(9), fill=INK)

    # ---- Map (green) ----
    d.rectangle([x2, y0, x2 + col_w, y0 + 128], fill=GREEN, outline=INK, width=3)
    d.text((x2 + 12, y0 + 8), "WHERE IT HAPPENED", font=F_BLACK(13), fill=WHITE)
    map_x, map_y, map_w, map_h = x2 + 8, y0 + 32, col_w - 16, 90
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h],
                fill=WHITE, outline=INK, width=2)

    def project(lon, lat):
        px = map_x + (lon + 170) / 360.0 * map_w
        py = map_y + (75 - lat) / 130.0 * map_h
        return (px, py)

    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=OCEAN)
    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly],
                  fill=LAND, outline=LAND_LINE)
    d.ellipse([project(139, 39)[0] - 3, project(139, 39)[1] - 5,
               project(139, 39)[0] + 3, project(139, 39)[1] + 5],
              fill=LAND, outline=LAND_LINE)
    d.ellipse([project(-2, 54)[0] - 4, project(-2, 54)[1] - 4,
               project(-2, 54)[0] + 4, project(-2, 54)[1] + 4],
              fill=LAND, outline=LAND_LINE)
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=INK, width=2)
    for label, lon, lat in MAP_LABELS:
        lx, ly_ = project(lon, lat)
        d.text((lx, ly_), label, font=F_BOLD(8), fill=GREY, anchor="ma")
    for n, lon, lat in MAP_DOTS:
        px, py = project(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=WHITE, width=1)
        d.text((px, py - 5), str(n), font=F_BOLD(9),
               fill=WHITE, anchor="ma")

    # ---- Footer: date check ----
    fy = 958
    d.rectangle([mx, fy, W - mx, fy + 3], fill=INK)
    d.text((W / 2, fy + 10),
           "DATE CHECK:  every story above happened, or was first reported, "
           "on Wednesday 25 November 2026.",
           font=F_BOLD(11), fill=INK, anchor="ma")
    d.text((W / 2, fy + 26),
           "Claims are labelled CLAIM.  Sources: Reuters, BBC, AP, Al Jazeera, "
           "Xinhua, UEFA, ESA.",
           font=F_REG(10), fill=GREY, anchor="ma")

    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print("wrote", out, os.path.getsize(out), "bytes")
