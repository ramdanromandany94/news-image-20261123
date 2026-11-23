#!/usr/bin/env python3
"""Draw the one-page newspaper image for 23 November 2026.

Fresh build for make.fun bounty news-image-20261123, written from scratch
with PIL and the DejaVu fonts. No network, no external assets: every pixel
is drawn here, so the output is byte-identical on every run.

Layout (1024 x 1024, newspaper front page):
  masthead + dateline, a drawn hero scene of the Strait of Hormuz,
  the hero headline and deck, a 2x2 grid of the next stories,
  two short-news strips, an ALSO TODAY strip, and a sources footer.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36

PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (163, 18, 18)
NAVY = (16, 42, 67)
SEA = (10, 30, 52)
GREY = (85, 85, 85)
LIGHT_LINE = (120, 110, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    """Load a DejaVu font, falling back to the sans face if a file is missing."""
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(text, fnt, max_w):
    """Split text into lines that fit max_w pixels, word by word."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, leading, fill=INK):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, y, weight=2, color=INK, x0=None, x1=None):
    draw.line([(x0 or MARGIN, y), (x1 or W - MARGIN, y)], fill=color, width=weight)


def hero_scene(draw):
    """Stylised Strait of Hormuz at dusk: sea, tanker, mine blast, smoke."""
    x0, y0, x1, y1 = MARGIN, 136, W - MARGIN, 330
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    # dusk band on the horizon
    draw.rectangle([x0, 216, x1, 238], fill=(214, 96, 32))
    draw.rectangle([x0, 238, x1, y1], fill=SEA)
    # low sun
    draw.ellipse([x0 + 60, 176, x0 + 116, 232], fill=(232, 164, 60))
    # explosion: a wide, uneven fireball — no symmetric rings, no face.
    # Every element stays inside the picture frame (y 136-330).
    cx, cy = 640, 224
    draw.ellipse([cx - 118, cy - 52, cx + 118, cy + 44], fill=(176, 32, 22))
    draw.ellipse([cx - 92, cy - 40, cx + 96, cy + 36], fill=(232, 96, 26))
    draw.ellipse([cx - 62, cy - 26, cx + 70, cy + 28], fill=(244, 176, 52))
    draw.ellipse([cx - 34, cy - 12, cx + 44, cy + 20], fill=(255, 226, 120))
    # flame tongues licking upward, uneven heights, tips kept below y=148
    draw.polygon([(cx - 108, cy - 30), (cx - 96, cy - 70), (cx - 72, cy - 44),
                  (cx - 52, cy - 76), (cx - 28, cy - 52), (cx - 6, cy - 70),
                  (cx + 18, cy - 46), (cx + 44, cy - 74), (cx + 62, cy - 50),
                  (cx + 88, cy - 68), (cx + 104, cy - 34), (cx + 78, cy - 8),
                  (cx + 30, cy - 18), (cx - 30, cy - 10), (cx - 78, cy - 12)],
                 fill=(232, 96, 26))
    # smoke drifting off to the right, irregular puffs, inside the frame
    for sx, sy, sr in [(742, 172, 26), (788, 190, 20), (712, 158, 16),
                       (826, 172, 14)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(58, 58, 58))
    # tanker hull
    draw.polygon([(x0 + 130, 300), (x0 + 130, 272), (x0 + 760, 272),
                  (x0 + 812, 300), (x0 + 780, 304), (x0 + 160, 304)],
                 fill=(8, 8, 8))
    # deck, bridge and funnels
    draw.rectangle([x0 + 700, 236, x0 + 758, 272], fill=(240, 240, 240))
    draw.rectangle([x0 + 180, 248, x0 + 210, 272], fill=RED)
    draw.rectangle([x0 + 226, 248, x0 + 256, 272], fill=RED)
    draw.rectangle([x0 + 180, 242, x0 + 210, 248], fill=(17, 17, 17))
    draw.rectangle([x0 + 226, 242, x0 + 256, 248], fill=(17, 17, 17))
    # container stacks
    for i, cx0 in enumerate(range(x0 + 300, x0 + 640, 84)):
        col = (176, 64, 32) if i % 2 == 0 else (36, 96, 120)
        draw.rectangle([cx0, 244, cx0 + 72, 272], fill=col)
    # waves
    for wx in range(x0 + 20, x1 - 20, 64):
        draw.arc([wx, 308, wx + 44, 322], 180, 360, fill=(200, 214, 228), width=2)
    # caption at the top-left corner, clear of waves and hull
    cap = SANS_B(15)
    draw.text((x0 + 12, y0 + 10), "THE STRAIT OF HORMUZ — SUNDAY",
              font=cap, fill=(255, 255, 255))


def grid_cell(draw, x, y, w, kicker, headline, body):
    """One of the four grid stories: kicker, headline, body."""
    draw.text((x, y), kicker, font=SANS_B(15), fill=RED)
    y = draw_wrapped(draw, headline, SERIF_B(27), x, y + 22, w, 32)
    y = draw_wrapped(draw, body, SANS(16), x, y + 4, w, 21)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    rule(d, 26, 3)
    d.text((W // 2, 34), "THE WORLD IN ONE IMAGE", font=SERIF_B(56),
           fill=INK, anchor="ma")
    d.text((MARGIN, 102), "MONDAY 23 NOVEMBER 2026", font=SANS_B(18), fill=INK)
    d.text((W - MARGIN, 102), "ONE DAY · ONE PAGE", font=SANS_B(18),
           fill=INK, anchor="ra")
    rule(d, 128, 2)

    # --- hero picture ---
    hero_scene(d)

    # --- hero headline and deck ---
    d.text((W // 2, 338), "HORMUZ IN FLAMES", font=SERIF_B(64),
           fill=INK, anchor="ma")
    draw_wrapped(d, "Two more tankers hit mines on Sunday as Iran claims a sixth "
                 "struck — the US blockade tightens and Trump warns American "
                 "warships will fire on vessels that defy it.",
                 SANS(19), MARGIN + 30, 412, W - 2 * (MARGIN + 30), 25)
    rule(d, 470, 2)

    # --- 2 x 2 grid ---
    col_w = (W - 2 * MARGIN - 28) // 2
    gx = [MARGIN, MARGIN + col_w + 28]
    gy = [482, 626]
    cells = [
        ("BENGHAZI, LIBYA", "Warship sunk off Libya",
         "Suspected Ukrainian sea drones hit the Russian corvette Merkury at "
         "Benghazi; it burned, capsized and sank. Ten people hurt."),
        ("CLIMATE · ANTALYA", "COP31 collapses",
         "Two weeks of talks end with no deal as the EU rejects a pact that "
         "never mentions fossil fuels — the longest COP ever."),
        ("UKRAINE", "Drone flattens Kyiv flats",
         "A Russian drone destroys a five-storey block in Dymer; four killed "
         "and ten missing under the rubble."),
        ("AMERICA", "Democrats sweep Congress",
         "258 House seats — the biggest majority since 1992 — and the Senate "
         "too, as the final midterm races fall."),
    ]
    for i, (kick, head, body) in enumerate(cells):
        grid_cell(d, gx[i % 2], gy[i // 2], col_w, kick, head, body)
    # vertical divider between the grid columns
    d.line([(W // 2, 482), (W // 2, 758)], fill=LIGHT_LINE, width=1)
    rule(d, 770, 2)

    # --- short-news strips, two columns ---
    strips = [
        ("JAVA FIRE — ", "24 body bags recovered at the Cikande candy factory; "
         "dozens still missing."),
        ("WEST BANK — ", "Settlers torch 12 cars near Ramallah; Eisenkot calls "
         "it \u201cJewish terrorism\u201d."),
        ("SUDAN — ", "Drones kill four near Khartoum and damage a UN building."),
        ("TRUMP ON IRAN — ", "A \u201cpermanent\u201d deal, or strikes after the "
         "New Year."),
    ]
    sy = 782
    for i, (lead, rest) in enumerate(strips):
        x = gx[i % 2]
        y = sy + (i // 2) * 52
        d.text((x, y), lead, font=SANS_B(15), fill=INK)
        lw = SANS_B(15).getlength(lead)
        draw_wrapped(d, rest, SANS(15), x + lw, y, col_w - lw, 19)
    rule(d, 896, 1, color=LIGHT_LINE)

    # --- also today ---
    d.text((MARGIN, 908), "ALSO TODAY", font=SANS_B(14), fill=RED)
    draw_wrapped(d, "Lahore AQI 538, the world\u2019s most polluted city · FIFA "
                 "set to confirm the UK as 2035 Women\u2019s World Cup host · "
                 "A second ship hit off Benghazi hours later",
                 SANS(14), MARGIN + 118, 908, W - MARGIN - (MARGIN + 118), 18)
    rule(d, 950, 2)

    # --- footer ---
    d.text((W // 2, 962), "Sources: Reuters · AP · CNN · Al Jazeera · AFP · IQAir",
           font=SANS(12), fill=GREY, anchor="ma")
    d.text((W // 2, 982), "Built by an AI agent for make.fun — Sum up 23 November\u2019s "
           "world news in one image", font=SANS(12), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
