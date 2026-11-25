# draw.py — renders the 25 November 2026 broadsheet front page, CLASSIC CREAM style.
# Run locally with Pillow:  python3 draw.py [output-path]
# The graded entrypoint is main.ts, which only copies the shipped
# entry.png into /output (Node stdlib only, no network, deterministic).
# This script is the build-time renderer; it is not run by the grader.
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/noto"

PAPER = (248, 242, 228)
INK = (20, 20, 20)
NAVY = (30, 50, 90)
RED = (178, 34, 34)
GREY = (96, 90, 78)
GREEN = (0, 140, 90)
ORANGE = (214, 120, 30)
TINT_BLUE = (226, 234, 242)
TINT_SAND = (240, 228, 205)
TINT_PALE = (238, 232, 218)
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


def chip(d, x, y, text, bg, fg):
    f = F_BOLD(9)
    tw = d.textlength(text, font=f)
    pad = 5
    d.rectangle([x, y, x + tw + pad * 2, y + 14], fill=bg)
    d.text((x + pad, y + 2), text, font=f, fill=fg)
    return tw + pad * 2 + 6


def draw_hero_scene(d, kind, x, y, w, h):
    # One large, detailed vector scene inside a panel.
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    if kind == "flame":
        d.rectangle([x, y, x + w, y + h], fill=TINT_BLUE)
        gy = y + int(h * 0.82)
        d.rectangle([x, gy, x + w, y + h], fill=TINT_SAND)
        d.ellipse([x + w - 52, y + 14, x + w - 20, y + 46], fill=(240, 200, 90))
        # Three refinery towers of different heights, joined by pipes.
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
        d.polygon([(x + int(w * 0.14), gy - int(h * 0.78) - 22),
                   (x + int(w * 0.24), gy - int(h * 0.78)),
                   (x + int(w * 0.19), gy - int(h * 0.78) + 6),
                   (x + int(w * 0.15), gy - int(h * 0.78) + 2)],
                  fill=ORANGE)
        d.polygon([(x + int(w * 0.70), gy - int(h * 0.62) - 18),
                   (x + int(w * 0.79), gy - int(h * 0.62)),
                   (x + int(w * 0.74), gy - int(h * 0.62) + 5),
                   (x + int(w * 0.71), gy - int(h * 0.62) + 2)],
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
        # Launch tower on the left of the rocket.
        d.rectangle([cx - 78, y + 30, cx - 66, gy], fill=INK)
        for by in range(y + 44, gy - 10, 18):
            d.line([(cx - 78, by), (cx - 52, by)], fill=INK, width=3)
        d.line([(cx - 66, y + 52), (cx - 52, y + 52)], fill=INK, width=3)
        # Rocket body.
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


def draw_small_panel(d, kind, x, y, w, h, bg, fg):
    # Small illustration strip for THE DAY IN EIGHT: a framed, enlarged
    # category glyph on the left and abstract caption lines on the right.
    d.rectangle([x, y, x + w, y + h], fill=bg, outline=INK, width=1)
    tile = Image.new("RGB", (17, 17), bg)
    td = ImageDraw.Draw(tile)
    draw_mini(td, kind, 1, 1, 15, bg, fg)
    gs = 38
    big = tile.resize((gs, gs), Image.NEAREST)
    d._image.paste(big, (x + 8, y + (h - gs) // 2))
    lx = x + 56
    for i, lw in enumerate([150, 168, 118]):
        ly = y + 10 + i * 11
        d.rectangle([lx, ly, lx + lw, ly + 3], fill=(196, 188, 168))


HEROES = [
    ("MIDDLE EAST", "CLAIM", RED, "flame",
     "Houthis claim strikes on Saudi refinery and Riyadh",
     "Group says it hit Ras Tanura refinery and the capital's "
     "financial district; coalition says it shot down 4 drones.",
     "Reuters", "MIDDLE EAST • P. 2"),
    ("ASIA", "REPORTED", GREEN, "rocket",
     "Shenzhou-24 lifts off with first foreign astronaut",
     "China's crew to Tiangong includes Pakistani Muhammad Zeeshan "
     "Ali, the first foreign visitor to the station.",
     "Xinhua / AP", "ASIA • P. 3"),
    ("EUROPE", "REPORTED", GREEN, "bars",
     "BBC: at least 490,334 Russian soldiers dead",
     "BBC and Mediazona count from leaked Rosstat records since "
     "Feb 2022; the true toll is likely higher.",
     "BBC", "EUROPE • P. 4"),
]

EIGHT = [
    (4, "chart", "Asian markets tumble in renewed AI sell-off",
     "MSCI Asia ex-Japan falls 2.3%.", "Reuters"),
    (5, "shield", "Australia signs security pact with Solomons",
     "Canberra named the primary security partner.", "AP"),
    (6, "exit", "North Korea expels Switzerland's top diplomat",
     "Envoy out in 48 hours; office closed.", "AP / KCNA"),
    (7, "target", "Coalition strikes Houthi-run Hodeidah port",
     "Coalition hit port capabilities.", "Al Jazeera"),
    (8, "rocket", "ESA to show first Hera images of Dimorphos",
     "First close-ups of asteroid Dimorphos due.", "ESA"),
    (9, "ball", "Real Madrid hit PSV 5-1; Arsenal and Man City draw",
     "Madrid win 5-1; Arsenal and City draw.", "UEFA"),
    (10, "warn", "26 miners trapped in flooded gold mine in West Java",
     "Police say 26 trapped; media say ~30.", "Reuters"),
    (11, "court", "India top court refuses bail to Khalid and Imam",
     "Bail refused in Delhi riots case.", "LiveLaw"),
]

LISTED = [
    (12, "Eisenkot signs pact with Lieberman", "Al Jazeera"),
    (13, "Houthis threaten Jeddah ports", "Al Jazeera"),
    (14, "Strike reported in Gaza Shati camp", "Al Jazeera"),
    (15, "Palestinians face raids after vote", "Al Jazeera"),
    (16, "Russian strike kills 2 in Odesa", "Reuters"),
    (17, "US shelves Russia deal plan", "FT via Reuters"),
    (18, "Spain election turns on housing", "Reuters"),
    (19, "Sarkozy and Bruni sent to trial", "BBC"),
    (20, "AI fakes target Taiwan election", "BBC"),
    (21, "Shanghai pledges loyalty to Beijing", "Reuters"),
    (22, "China Politburo down to 21 members", "Reuters"),
    (23, "Ábrego García leaves US for Spain", "BBC / AP"),
    (24, "Alaska ends voter-data deal with DOJ", "AP"),
    (25, "Iowa set for lead-azide blast", "AP"),
    (26, "Poll: 55% want Iran war ended now", "Al Jazeera"),
    (27, "Sensex rises 1.68% to 83,821", "ReportWire"),
    (28, "US AG dodges Nvidia probe questions", "BBC"),
    (29, "Sahel insurgents fly cheap drones", "Reuters"),
    (30, "Landmine toll hits 6,929 in 2025", "BBC"),
    (31, "S. Africa convicts Russia-case man", "AP"),
    (32, "Australia inflation jumps to 4.9%", "ABS"),
    (33, "Ex-officer guilty of double murder", "BBC"),
    (34, "Oil falls: Brent $90.97 on glut fears", "Reuters"),
    (35, "Australia plans duty-of-care law", "Qatar Tribune"),
]

NUMBERS = [
    ("-2.3%", "MSCI ASIA EX-JAPAN"),
    ("490,334", "RUSSIAN DEATHS, BBC EST."),
    ("$90.97", "BRENT CRUDE"),
    ("4.9%", "AUSTRALIA CPI, YR TO OCT"),
    ("6,929", "LANDMINE CASUALTIES, 2025"),
    ("26", "MINERS TRAPPED, POLICE SAY"),
]

REGION_COUNTS = ("ASIA 9  •  EUROPE 7  •  MIDDLE EAST 6  •  AMERICAS 5  •  "
                 "OCEANIA 4  •  AFRICA 3  •  WORLD 1")

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
    (1, 54.0, 25.0), (2, 98.5, 39.8), (3, 33.0, 48.0), (5, 149.1, -35.3),
    (6, 128.0, 42.0), (7, 40.0, 13.0), (8, 12.0, 52.0), (9, -3.7, 40.4),
    (10, 106.8, -6.6), (11, 77.2, 28.6), (14, 34.5, 31.5),
    (25, -93.5, 41.6), (29, -4.0, 17.0),
]

MAP_LABELS = [
    ("N. AMERICA", -128, 58), ("S. AMERICA", -60, -20),
    ("EUROPE", 8, 68), ("AFRICA", 14, -2),
    ("ASIA", 75, 60), ("OCEANIA", 105, -32),
]


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 24

    # ---- Dark top bar ----
    d.rectangle([0, 0, W, 34], fill=INK)
    d.text((mx, 10), "THE WORLD IN ONE DAY", font=F_BOLD(12), fill=WHITE)
    d.text((W - mx, 10), "WEDNESDAY 25 NOVEMBER 2026",
           font=F_BOLD(12), fill=WHITE, anchor="ra")

    # ---- Giant serif masthead ----
    d.text((W / 2, 44), "Wednesday 25 November 2026",
           font=F_SERIF_BL(44), fill=INK, anchor="ma")

    # ---- Stats strip ----
    d.rectangle([mx, 100, W - mx, 101], fill=INK)
    d.text((mx, 106), "35 STORIES, ALL FROM WEDNESDAY 25 NOV",
           font=F_BOLD(11), fill=NAVY)
    d.text((W - mx, 108), REGION_COUNTS, font=F_BOLD(9), fill=GREY, anchor="ra")
    d.rectangle([mx, 128, W - mx, 129], fill=INK)

    # ---- Ticker: the three top headlines ----
    d.rectangle([0, 132, W, 158], fill=INK)
    ticker = ("HOUTHIS CLAIM STRIKES ON SAUDI REFINERY AND RIYADH    •    "
              "SHENZHOU-24 LIFTS OFF WITH FIRST FOREIGN ASTRONAUT    •    "
              "BBC: AT LEAST 490,334 RUSSIAN SOLDIERS DEAD")
    d.text((W / 2, 140), ticker, font=F_BOLD(11), fill=WHITE, anchor="ma")

    # ---- Six big numbers ----
    d.rectangle([mx, 162, W - mx, 163], fill=INK)
    for i, (num, label) in enumerate(NUMBERS):
        cx = mx + i * 163
        d.text((cx + 2, 168), num, font=F_SERIF_B(21),
               fill=RED if num.startswith("-") else NAVY)
        d.text((cx + 2, 196), label, font=F_BOLD(8), fill=GREY)
    d.rectangle([mx, 214, W - mx, 215], fill=INK)

    # ---- Three big heroes ----
    for idx, hero in enumerate(HEROES):
        region, status, sbg, kind, head, summ, src, secpage = hero
        x = mx + idx * (312 + 16)
        y = 222
        d.text((x, y), region, font=F_BOLD(10), fill=NAVY)
        cw = chip(d, x + d.textlength(region, font=F_BOLD(10)) + 8, y - 2,
                  status, sbg, WHITE)
        sx = x + d.textlength(region, font=F_BOLD(10)) + 8 + cw
        d.text((sx, y), src, font=F_IT(10), fill=GREY)
        draw_hero_scene(d, kind, x, y + 18, 312, 150)
        hy = y + 176
        for line in wrap(d, head, F_SERIF_B(16), 312)[:2]:
            d.text((x, hy), line, font=F_SERIF_B(16), fill=INK)
            hy += 19
        sy = y + 216
        for line in wrap(d, summ, F_REG(10), 312)[:2]:
            d.text((x, sy), line, font=F_REG(10), fill=(52, 48, 40))
            sy += 13
        d.text((x, y + 244), secpage, font=F_BOLD(9), fill=GREY)

    # ---- The day in eight ----
    ey = 490
    d.text((mx, ey), "THE DAY IN EIGHT", font=F_SERIF_B(15), fill=INK)
    d.text((W - mx, ey + 2), "EIGHT STORIES THAT SHAPED THE DAY",
           font=F_BOLD(9), fill=GREY, anchor="ra")
    d.rectangle([mx, ey + 22, W - mx, ey + 24], fill=INK)
    for i, (n, kind, head, summ, src) in enumerate(EIGHT):
        col = i % 4
        row = i // 4
        x = mx + col * (232 + 16)
        y = ey + 32 + row * 102
        draw_small_panel(d, kind, x, y, 232, 42, TINT_PALE, NAVY)
        num_w = d.textlength(f"{n}.  ", font=F_BOLD(11))
        d.text((x, y + 48), f"{n}.", font=F_BOLD(11), fill=RED)
        hy = y + 48
        for line in wrap(d, head, F_BOLD(11), 232 - num_w)[:2]:
            d.text((x + num_w, hy), line, font=F_BOLD(11), fill=INK)
            hy += 13
        d.text((x, y + 78), summ + "  — " + src, font=F_REG(9),
               fill=(52, 48, 40))

    # ---- Also on Wednesday: map + 3-column list + date check ----
    ay = 728
    d.text((mx, ay), "ALSO ON WEDNESDAY — 24 MORE STORIES",
           font=F_SERIF_B(15), fill=INK)
    d.rectangle([mx, ay + 22, W - mx, ay + 24], fill=INK)
    d.text((mx, ay + 30), "WHERE IT HAPPENED", font=F_BOLD(9), fill=NAVY)
    map_x, map_y, map_w, map_h = mx, ay + 44, 220, 140

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
    for label, lon, lat in MAP_LABELS:
        lx, ly_ = project(lon, lat)
        d.text((lx, ly_), label, font=F_BOLD(7), fill=GREY, anchor="ma")
    for n, lon, lat in MAP_DOTS:
        px, py = project(lon, lat)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=WHITE, width=1)
        d.text((px, py - 4), str(n), font=F_BOLD(7),
               fill=WHITE, anchor="ma")
    d.text((map_x, map_y + map_h + 6), "13 OF TODAY'S 35 STORIES, MAPPED",
           font=F_BOLD(8), fill=GREY)

    for i, (n, text, src) in enumerate(LISTED):
        col = i // 8
        row = i % 8
        x = 260 + col * 193
        y = ay + 30 + row * 21
        d.text((x, y), f"{n}.", font=F_BOLD(10), fill=RED)
        d.text((x + 22, y), text, font=F_REG(9), fill=INK)

    # Date check box (red header).
    bx, by, bw, bh = 844, ay + 30, 156, 154
    d.rectangle([bx, by, bx + bw, by + bh], fill=WHITE, outline=INK, width=2)
    d.rectangle([bx, by, bx + bw, by + 26], fill=RED)
    d.text((bx + 8, by + 6), "DATE CHECK", font=F_BOLD(12), fill=WHITE)
    body = ("Every story above happened, or was first reported, on "
            "Wednesday 25 November 2026. Claims are labelled CLAIM. "
            "Sources: Reuters, BBC, AP, Al Jazeera, Xinhua, UEFA, ESA, "
            "ABS, LiveLaw.")
    ty = by + 34
    for line in wrap(d, body, F_REG(9), bw - 16):
        d.text((bx + 8, ty), line, font=F_REG(9), fill=INK)
        ty += 12

    # ---- Dark footer strip ----
    d.rectangle([0, 950, W, H], fill=INK)
    d.text((W / 2, 964),
           "WORLD  |  BUSINESS  |  POLITICS  |  TECHNOLOGY  |  SCIENCE  |  "
           "HEALTH  |  SPORTS  |  ENTERTAINMENT",
           font=F_BOLD(11), fill=WHITE, anchor="ma")
    d.text((W / 2, 988), "One day. One page. The world, as it happened.",
           font=F_SERIF_I(10), fill=(200, 196, 184), anchor="ma")

    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
    print("wrote", out, os.path.getsize(out), "bytes")
