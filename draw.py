#!/usr/bin/env python3
"""Draw the 21 November 2026 front page (1024x1024 PNG).

Run:  python3 draw.py [output-path]   (default: entry.png)
Pure PIL + DejaVu fonts, no network, no randomness.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (163, 22, 33)
NAVY = (20, 33, 61)
GRAY = (107, 107, 107)
CARD = (255, 253, 246)
BORDER = (216, 210, 192)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)   # noqa: E731
REG = lambda s: font("DejaVuSans.ttf", s)        # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines):
    """Shrink font until `text` wraps into at most max_lines; return (font, lines)."""
    size = fnt.size
    while size > 10:
        f = font("DejaVuSans-Bold.ttf", size)
        lines = wrap(draw, text, f, width)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    return font("DejaVuSans-Bold.ttf", 10), wrap(draw, text,
                                                font("DejaVuSans-Bold.ttf", 10),
                                                width)


def starburst(draw, cx, cy, r, colour):
    """Eight-point explosion star."""
    pts = []
    for i in range(16):
        ang = i * 3.14159265 / 8
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang),
                    cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=colour)
    draw.ellipse([cx - r * 0.18, cy - r * 0.18, cx + r * 0.18, cy + r * 0.18],
                 fill=(255, 214, 64))


def arc_points(x0, y0, x1, y1, lift, n=26):
    """Points along a quadratic arc from (x0,y0) to (x1,y1)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) * (1 - t) * x0 + 2 * (1 - t) * t * ((x0 + x1) / 2) + t * t * x1
        y = (1 - t) * (1 - t) * y0 + 2 * (1 - t) * t * (min(y0, y1) - lift) + t * t * y1
        pts.append((x, y))
    return pts


def draw_hero_graphic(d, x, y, w, h):
    """Dark panel: missile arcs over Ukraine, impacts at Kyiv and Poland."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=NAVY)
    # faint grid dots
    for gx in range(x + 24, x + w - 10, 34):
        for gy in range(y + 24, y + h - 10, 34):
            d.ellipse([gx, gy, gx + 2, gy + 2], fill=(58, 74, 110))
    # arcs: from right edge (east) to Kyiv and Poland
    d.line(arc_points(x + w - 14, y + h - 60, x + 118, y + 128, 90),
           fill=(255, 255, 255), width=2)
    d.line(arc_points(x + w - 14, y + h - 30, x + 236, y + 84, 70),
           fill=(255, 255, 255), width=2)
    d.line(arc_points(x + w - 14, y + 60, x + 118, y + 128, 60),
           fill=(200, 210, 235), width=2)
    starburst(d, x + 118, y + 128, 26, RED)
    starburst(d, x + 236, y + 84, 20, RED)
    f_lab = BOLD(17)
    f_sub = REG(14)
    d.text((x + 96, y + 162), "KYIV", font=f_lab, fill=WHITE)
    d.text((x + 214, y + 112), "POLAND", font=f_lab, fill=WHITE)
    d.text((x + 18, y + h - 30), "UKRAINE  •  400+ DRONES, 110 MISSILES",
           font=f_sub, fill=(178, 190, 215))


def icon_chart(d, x, y, s):
    d.line([(x, y + s), (x, y)], fill=INK, width=3)
    d.line([(x, y + s), (x + s, y + s)], fill=INK, width=3)
    pts = [(x + 6, y + 14), (x + 18, y + 24), (x + 30, y + 20),
           (x + 42, y + 38), (x + s - 6, y + s - 8)]
    d.line(pts, fill=RED, width=4)
    d.polygon([(x + s - 6, y + s - 8), (x + s - 14, y + s - 8),
               (x + s - 6, y + s - 16)], fill=RED)


def icon_lock(d, x, y, s):
    d.rounded_rectangle([x + 8, y + s // 2, x + s - 8, y + s - 4], radius=6,
                        outline=INK, width=4)
    d.arc([x + 14, y + 6, x + s - 14, y + s // 2 + 8], 180, 360,
          fill=INK, width=4)
    d.ellipse([x + s // 2 - 4, y + s // 2 + 8, x + s // 2 + 4, y + s // 2 + 16],
              fill=RED)


def icon_globe(d, x, y, s):
    d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], outline=INK, width=4)
    d.ellipse([x + s // 2 - 8, y + 4, x + s // 2 + 8, y + s - 4],
              outline=INK, width=3)
    d.line([(x + 4, y + s // 2), (x + s - 4, y + s // 2)], fill=INK, width=3)
    d.line([(x + 10, y + 14), (x + s - 10, y + 14)], fill=INK, width=2)
    d.line([(x + 10, y + s - 14), (x + s - 10, y + s - 14)], fill=INK, width=2)
    d.ellipse([x + s - 16, y + s - 18, x + s - 6, y + s - 8], fill=RED)


def icon_pill(d, x, y, s):
    d.rounded_rectangle([x + 2, y + s // 2 - 11, x + s - 2, y + s // 2 + 11],
                        radius=11, fill=WHITE, outline=INK, width=3)
    d.rounded_rectangle([x + 2, y + s // 2 - 11, x + s // 2, y + s // 2 + 11],
                        radius=11, fill=RED)
    d.line([(x + s // 2, y + s // 2 - 11), (x + s // 2, y + s // 2 + 11)],
           fill=INK, width=3)


def icon_rings(d, x, y, s):
    d.ellipse([x + 2, y + 10, x + s // 2 + 6, y + s - 10], outline=INK, width=4)
    d.ellipse([x + s // 2 - 6, y + 10, x + s - 2, y + s - 10], outline=INK,
              width=4)
    d.line([(x + s // 2 - 2, y + s // 2 - 4), (x + s // 2 + 2, y + s // 2 + 4)],
           fill=RED, width=4)


def icon_planet(d, x, y, s):
    d.ellipse([x + 10, y + 10, x + s - 14, y + s - 14], fill=(150, 150, 150),
              outline=INK, width=3)
    d.ellipse([x + 18, y + 18, x + 24, y + 24], fill=INK)
    d.ellipse([x + 30, y + 30, x + 35, y + 35], fill=INK)
    d.ellipse([x + 8, y + s // 2 - 4, x + s - 6, y + s // 2 + 4],
              outline=RED, width=3)
    d.rectangle([x + s - 12, y + 2, x + s - 4, y + 10], fill=RED)


ICONS = [icon_chart, icon_lock, icon_globe, icon_pill, icon_rings, icon_planet]


def draw_card(d, x, y, w, h, icon, kicker, headline, deck):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD,
                        outline=BORDER, width=1)
    pad = 14
    ix, iy, isize = x + pad, y + pad, 52
    icon(d, ix, iy, isize)
    tx = x + pad + isize + 12
    tw = w - pad - (tx - x)
    d.text((tx, y + pad + 2), kicker, font=BOLD(13), fill=RED)
    f_head, lines = fit_lines(d, headline, BOLD(25), tw, 2)
    ly = y + pad + 22
    for ln in lines:
        d.text((tx, ly), ln, font=f_head, fill=INK)
        ly += f_head.size + 3
    f_deck = REG(15)
    dlines = wrap(d, deck, f_deck, tw)
    for ln in dlines[:3]:
        d.text((tx, ly), ln, font=f_deck, fill=(58, 58, 58))
        ly += 19


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- masthead ----
    d.text((W // 2, 18), "THE WORLD IN ONE DAY", font=BOLD(54), fill=INK,
           anchor="ma")
    d.line([(M, 92), (W - M, 92)], fill=INK, width=3)
    d.line([(M, 98), (W - M, 98)], fill=INK, width=1)
    d.text((W // 2, 108), "SATURDAY  21  NOVEMBER  2026",
           font=BOLD(30), fill=RED, anchor="ma")
    d.text((W // 2, 146), "One day's world news, on one page",
           font=REG(17), fill=GRAY, anchor="ma")

    # ---- hero ----
    hy, hh = 182, 252
    d.line([(M, hy - 12), (W - M, hy - 12)], fill=INK, width=2)
    gx = M + 566
    gw = W - M - gx
    draw_hero_graphic(d, gx, hy, gw, hh)
    d.text((M, hy + 6), "WAR IN EUROPE  •  LEAD STORY", font=BOLD(15),
           fill=RED)
    f_h, hlines = fit_lines(d, "RUSSIAN MISSILES LAND IN POLAND",
                            BOLD(46), 540, 2)
    ly = hy + 30
    for ln in hlines:
        d.text((M, ly), ln, font=f_h, fill=INK)
        ly += f_h.size + 4
    deck = ("Russia fires 400+ drones and 110 missiles at Ukraine; at least "
            "8 killed in Kyiv as bridges and power sites are hit. Two "
            "missiles and a drone come down in Poland — NATO calls it a "
            "grave violation of its airspace.")
    f_deck = REG(19)
    for ln in wrap(d, deck, f_deck, 540):
        d.text((M, ly), ln, font=f_deck, fill=(48, 48, 48))
        ly += 25

    # ---- grid: 3 cols x 2 rows ----
    gy, gap = 452, 14
    cw = (W - 2 * M - 2 * gap) // 3
    ch = 218
    stories = [
        ("MARKETS  •  GLOBAL", "STOCKS SLIDE WORLDWIDE",
         "S&P 500 falls into correction; Nikkei drops 5.1% in an AI-led sell-off."),
        ("CYBER  •  UNITED STATES", "FBI DATABASE HACKED",
         "Hackers breach the FBI crime database and a USDA payment system."),
        ("CLIMATE  •  TURKEY", "CLIMATE TALKS MISS DEADLINE",
         "COP31 in Antalya passes its deadline with no fossil-fuel deal."),
        ("HEALTH  •  SCIENCE", "PILL MAKES TUMOURS VANISH",
         "Daraxonrasib: cancer undetectable in 1 in 12 patients in a 61-patient trial."),
        ("CRIME  •  MEXICO", "MEXICO NABS EL CHAPO ISIDRO",
         "FBI most-wanted cartel boss Fausto Isidro Meza Flores captured in Sinaloa."),
        ("SPACE  •  ESA / JAXA", "BEPICOLOMBO AT MERCURY",
         "Twin orbiters enter orbit after an eight-year journey; a first for two craft."),
    ]
    for i, (kicker, head, deck) in enumerate(stories):
        cx = M + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + gap)
        draw_card(d, cx, cy, cw, ch, ICONS[i], kicker, head, deck)

    # ---- footer ----
    fy = 920
    d.line([(M, fy), (W - M, fy)], fill=INK, width=2)
    d.text((M, fy + 12), "ALSO TODAY", font=BOLD(14), fill=RED)
    also = ("6.8 quake off Timor-Leste  •  UK and EU sign three post-Brexit "
            "deals  •  Denmark expels Russian diplomat  •  Trump weighs new "
            "strikes on Iran")
    alines = wrap(d, also, REG(15), W - 2 * M - 120)
    ay = fy + 11
    for ln in alines[:2]:
        d.text((M + 118, ay), ln, font=REG(15), fill=INK)
        ay += 19
    d.text((M, fy + 58),
           "Sources: BBC, CNN, AP, ESA, The Guardian, PBS NewsHour, France 24 — "
           "21 November 2026",
           font=REG(13), fill=GRAY)
    d.text((W - M, fy + 58), "THE WORLD IN ONE DAY", font=BOLD(13),
           fill=GRAY, anchor="ra")

    img.save(out, "PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
