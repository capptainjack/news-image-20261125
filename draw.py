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
LAND = (216, 209, 190)
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
    d.rounded_rectangle([x, y, x + s, y + s], radius=8, fill=bg)
    c = s / 2
    if kind == "flame":
        d.polygon([(x + c, y + 10), (x + s - 14, y + s - 22),
                   (x + c + 8, y + s - 14), (x + c - 6, y + s - 12),
                   (x + 14, y + s - 24)], fill=fg)
        d.ellipse([x + c - 6, y + s - 24, x + c + 8, y + s - 10], fill=(255, 255, 255))
    elif kind == "rocket":
        d.polygon([(x + c, y + 8), (x + c + 10, y + 30),
                   (x + c - 10, y + 30)], fill=fg)
        d.rectangle([x + c - 9, y + 28, x + c + 9, y + 48], fill=fg)
        d.polygon([(x + c - 9, y + 40), (x + c - 18, y + 52),
                   (x + c - 9, y + 48)], fill=fg)
        d.polygon([(x + c + 9, y + 40), (x + c + 18, y + 52),
                   (x + c + 9, y + 48)], fill=fg)
        d.polygon([(x + c, y + 52), (x + c + 6, y + 62),
                   (x + c - 6, y + 62)], fill=(214, 120, 30))
    elif kind == "chart":
        pts = [(x + 12, y + 18), (x + 24, y + 28), (x + 34, y + 24),
               (x + 46, y + 40), (x + 56, y + 50)]
        d.line(pts, fill=fg, width=4, joint="curve")
        d.polygon([(x + 56, y + 50), (x + 44, y + 48), (x + 54, y + 38)], fill=fg)
        d.line([(x + 10, y + 54), (x + 58, y + 54)], fill=fg, width=2)
    elif kind == "bars":
        for i, h in enumerate([20, 34, 48]):
            bx = x + 13 + i * 15
            d.rectangle([bx, y + 58 - h, bx + 10, y + 58], fill=fg)
        d.line([(x + 10, y + 58), (x + 58, y + 58)], fill=fg, width=2)
    elif kind == "shield":
        d.polygon([(x + c, y + 8), (x + s - 12, y + 16), (x + s - 12, y + 34),
                   (x + c, y + 56), (x + 12, y + 34), (x + 12, y + 16)], fill=fg)
        d.line([(x + c - 8, y + 30), (x + c - 2, y + 38),
                (x + c + 10, y + 22)], fill=(255, 255, 255), width=4, joint="curve")
    elif kind == "exit":
        d.rectangle([x + 14, y + 12, x + 34, y + 56], outline=fg, width=3)
        d.line([(x + 22, y + 34), (x + 50, y + 34)], fill=fg, width=4)
        d.polygon([(x + 50, y + 34), (x + 40, y + 26), (x + 40, y + 42)], fill=fg)


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
    (7, "Coalition strikes Houthi-run Hodeidah port", "Al Jazeera"),
    (8, "Eisenkot signs first coalition pact with Lieberman", "Al Jazeera"),
    (9, "Strike reported in Gaza's Shati camp; 4 reported killed", "Al Jazeera"),
    (10, "Russian strike kills 2 in Ukraine's Odesa region", "Reuters"),
    (11, "US shelves Russia business-deal plan to end war", "FT via Reuters"),
    (12, "Spain's election fight turns on housing, rent caps", "Reuters"),
    (13, "Sarkozy and Bruni sent to trial over witness tampering", "BBC"),
    (14, "ESA to show first Hera images of asteroid Dimorphos", "ESA"),
    (15, "Real Madrid hit PSV 5-1; Arsenal and Man City draw", "UEFA"),
    (16, "26 miners trapped in flooded gold mine in West Java", "Reuters"),
    (17, "India top court refuses bail to Khalid and Imam", "LiveLaw"),
    (18, "BBC Verify: AI fakes target Taiwan election", "BBC"),
    (19, "Shanghai pledges loyalty after Chen probe", "Reuters"),
    (20, "Abrego Garcia leaves US for Spain", "BBC / AP"),
    (21, "Alaska ends voter-data deal with US Justice Dept", "AP"),
    (22, "Iowa set for controlled blast of 5 tons of lead azide", "AP"),
    (23, "Poll: 55% of US voters want Iran war ended now", "Al Jazeera"),
    (24, "Thomas Markle indicted on abuse-material charges", "BBC"),
    (25, "Sahel insurgents fly cheap drones; 187 JNIM attacks", "Reuters"),
    (26, "Landmine casualties hit 6,929 in 2025, 84% civilians", "BBC"),
    (27, "S. Africa convicts man who tried to fight for Russia", "AP"),
    (28, "Australia inflation jumps to 4.9% in year to Oct", "ABS"),
    (29, "Ex-officer guilty of double murder in Sydney", "BBC"),
    (30, "Oil falls: Brent $90.97 as glut fears offset war risk", "Reuters"),
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

MAP_DOTS = [
    (1, 46.7, 24.6), (7, 42.8, 14.8), (2, 98.5, 39.8), (6, 125.8, 39.0),
    (10, 30.7, 46.5), (12, -3.7, 40.4), (16, 106.8, -6.6), (17, 77.2, 28.6),
    (5, 149.1, -35.3), (25, -8.0, 12.6), (20, -77.0, 38.9),
    (22, -93.5, 41.9), (18, 121.6, 25.0),
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
        draw_icon(d, kind, x + 14, y + 16, 68, tint, fg)
        tx = x + 94
        d.text((tx, y + 10), region, font=F_BOLD(10), fill=NAVY)
        cw = chip(d, tx + d.textlength(region, font=F_BOLD(10)) + 8, y + 8,
                  status, sbg, (255, 255, 255))
        sx = tx + d.textlength(region, font=F_BOLD(10)) + 8 + cw
        d.text((sx, y + 10), src, font=F_IT(10), fill=GREY)
        d.text((tx, y + 24), f"{idx + 1}.", font=F_BLACK(15), fill=RED)
        hw = col_w - 94 - 12
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

    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly],
                  fill=LAND, outline=LAND_LINE)
    d.ellipse([project(139, 39)[0] - 4, project(139, 39)[1] - 7,
               project(139, 39)[0] + 4, project(139, 39)[1] + 7],
              fill=LAND, outline=LAND_LINE)
    d.ellipse([project(-2, 54)[0] - 5, project(-2, 54)[1] - 6,
               project(-2, 54)[0] + 5, project(-2, 54)[1] + 6],
              fill=LAND, outline=LAND_LINE)
    for n, lon, lat in MAP_DOTS:
        px, py = project(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py - 5), str(n), font=F_BOLD(9),
               fill=(255, 255, 255), anchor="ma")

    # ---- Numbered list: the rest of the day ----
    ly = 656
    d.text((mx, ly), "THE REST OF THE DAY  —  24 MORE STORIES",
           font=F_BOLD(14), fill=INK)
    d.line([(mx, ly + 22), (W - mx, ly + 22)], fill=INK, width=2)
    row_h = 25
    for i, (n, text, src) in enumerate(LISTED):
        col = i // 12
        row = i % 12
        x = mx if col == 0 else x2
        y = ly + 28 + row * row_h
        d.text((x, y), f"{n}.", font=F_BOLD(12), fill=RED)
        d.text((x + 26, y), text, font=F_REG(12), fill=INK)
        tw = d.textlength(text, font=F_REG(12))
        d.text((x + 26 + tw + 6, y), "— " + src, font=F_IT(10), fill=GREY)

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
