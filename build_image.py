"""Draw the front page for 24 November 2026 as a 1024x1024 PNG.

A newspaper front page: masthead, one lead story with a drawn scene,
four stories in two rows of two, a bottom strip story, and a footer
ticker. Everything is drawn with Pillow shapes and text; no outside
images, no network, no randomness, so the output is deterministic.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "image.png"

PAPER = (247, 243, 234)
INK = (22, 22, 22)
MUTED = (96, 92, 84)
RED = (163, 18, 18)
NAVY = (28, 47, 87)
GREEN = (27, 120, 70)
ORANGE = (198, 88, 20)
RULE = (180, 172, 156)
SKY = (214, 228, 240)
SEA = (36, 68, 110)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, word by word."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt_path, size, width):
    """Largest font size at or below `size` that fits `text` in width."""
    while size > 10:
        fnt = font(fnt_path, size)
        if draw.textlength(text, font=fnt) <= width:
            return fnt
        size -= 1
    return font(fnt_path, size)


def para(draw, text, fnt, x, y, width, leading):
    """Draw wrapped paragraph; return y just below the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def kicker(draw, text, x, y, size=19):
    fnt = font(SANS_B, size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + size + 8


def headline(draw, text, fnt_path, size, x, y, width, leading):
    """Draw a headline wrapped to width; return y below it."""
    fnt = font(fnt_path, size)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def rule(draw, x0, x1, y, width=1, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def vrule(draw, x, y0, y1, width=1, color=RULE):
    draw.line([(x, y0), (x, y1)], fill=color, width=width)


def draw_lead_scene(draw, x, y, w, h):
    """Sea, ship and drones off Benghazi."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=SEA)
    for wy in (0.62, 0.72, 0.84):
        yy = y + int(h * wy)
        for wx in range(0, w, 46):
            draw.arc([x + wx, yy - 7, x + wx + 34, yy + 7], 180, 360,
                     fill=(120, 160, 205), width=2)
    hx, hy = x + 48, y + int(h * 0.52)
    draw.polygon([(hx, hy), (hx + 190, hy), (hx + 168, hy + 34),
                  (hx + 22, hy + 34)], fill=(38, 38, 44))
    draw.rectangle([hx + 78, hy - 34, hx + 138, hy], fill=(60, 60, 68))
    draw.line([(hx + 108, hy - 34), (hx + 108, hy - 62)], fill=(38, 38, 44),
              width=4)
    draw.polygon([(hx + 108, hy - 62), (hx + 132, hy - 54),
                  (hx + 108, hy - 46)], fill=RED)
    for dx, dy in ((x + 210, y + int(h * 0.80)),
                   (x + 236, y + int(h * 0.68)),
                   (x + 186, y + int(h * 0.90))):
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(250, 250, 250),
                     outline=INK, width=2)
        for i in range(6):
            sx = dx - 14 - i * 9
            draw.line([(sx, dy), (sx - 5, dy)], fill=(250, 250, 250),
                      width=2)


def draw_bars(draw, x, y, w, h):
    """Rising market bars for the Nvidia story."""
    vals = (0.30, 0.38, 0.34, 0.52, 1.00)
    bw = w // len(vals)
    for i, v in enumerate(vals):
        bh = int(h * v)
        bx = x + i * bw + 4
        col = GREEN if i == len(vals) - 1 else (120, 130, 140)
        draw.rectangle([bx, y + h - bh, bx + bw - 8, y + h], fill=col)


def draw_block(draw, x, y, w, h):
    """Apartment block with a damaged corner for Zaporizhzhia."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 188, 172))
    for r in range(2):
        for c in range(5):
            wx = x + 10 + c * (w // 5)
            wy = y + 8 + r * 24
            draw.rectangle([wx, wy, wx + 20, wy + 15], fill=NAVY)
    draw.polygon([(x + w, y), (x + w - 52, y), (x + w - 30, y + 30),
                  (x + w, y + 20)], fill=PAPER)
    for rx, ry in ((x + w - 46, y + 38), (x + w - 24, y + 44)):
        draw.rectangle([rx, ry, rx + 9, ry + 6], fill=(120, 112, 98))


def draw_skyline(draw, x, y, w, h):
    """Gaza skyline silhouette."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
    heights = (0.55, 0.80, 0.45, 0.95, 0.60, 0.75)
    bw = w // len(heights)
    for i, v in enumerate(heights):
        bh = int(h * v)
        bx = x + i * bw + 3
        draw.rectangle([bx, y + h - bh, bx + bw - 6, y + h], fill=(74, 74, 82))
    cx = x + int(w * 0.5)
    draw.ellipse([cx - 16, y + int(h * 0.18), cx + 16, y + int(h * 0.42)],
                 fill=(74, 74, 82))
    draw.rectangle([x + int(w * 0.78), y + int(h * 0.05),
                    x + int(w * 0.78) + 8, y + h], fill=(74, 74, 82))


def draw_factory(draw, x, y, w, h):
    """Factory with flames for the Cikande fire."""
    draw.rectangle([x, y + int(h * 0.45), x + w, y + h], fill=(150, 140, 124))
    draw.rectangle([x + 12, y + int(h * 0.58), x + 34, y + int(h * 0.80)],
                   fill=NAVY)
    draw.rectangle([x + w - 34, y + int(h * 0.58), x + w - 12,
                    y + int(h * 0.80)], fill=NAVY)
    cx = x + w // 2
    draw.polygon([(cx - 42, y + int(h * 0.55)), (cx - 14, y + int(h * 0.08)),
                  (cx + 6, y + int(h * 0.42)), (cx + 22, y + int(h * 0.12)),
                  (cx + 42, y + int(h * 0.55))], fill=ORANGE)
    draw.polygon([(cx - 18, y + int(h * 0.55)), (cx - 4, y + int(h * 0.30)),
                  (cx + 16, y + int(h * 0.55))], fill=(240, 190, 60))


def draw_burst(draw, cx, cy, r):
    """Small blast starburst for the Colombia strip."""
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=ORANGE)


def story(draw, x, y, w, kick, head, body, art=None, art_h=52):
    """One story: kicker, headline, body, art below; return bottom y."""
    y = kicker(draw, kick, x, y)
    y = headline(draw, head, SERIF_B, 27, x, y, w, 32) + 6
    y = para(draw, body, font(SANS, 18), x, y, w, 22)
    if art is not None:
        art(draw, x, y + 4, w, art_h)
        return y + 4 + art_h
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 36
    RX = W - MX
    col_w = (RX - MX - 28) // 2
    mid_x = MX + col_w + 14

    # ---- masthead ----
    rule(d, MX, RX, 26, 2, INK)
    title_f = fit(d, "THE DAY IN THE WORLD", SERIF_B, 62, RX - MX)
    tw = d.textlength("THE DAY IN THE WORLD", font=title_f)
    d.text(((W - tw) / 2, 38), "THE DAY IN THE WORLD", font=title_f,
           fill=INK)
    date_f = font(SANS_B, 21)
    dateline = "TUESDAY, 24 NOVEMBER 2026  ·  THE WORLD IN ONE PAGE"
    dw = d.textlength(dateline, font=date_f)
    d.text(((W - dw) / 2, 116), dateline, font=date_f, fill=RED)
    rule(d, MX, RX, 146, 3, INK)
    rule(d, MX, RX, 152, 1, INK)

    # ---- lead story: Ukraine / Libya ----
    y = 168
    y = kicker(d, "LEAD  ·  UKRAINE / LIBYA", MX, y, 19)
    y = headline(d, "KYIV SAYS LIBYA SHIP STRIKE WAS SELF-DEFENCE",
                 SERIF_B, 36, MX, y, 600, 44) + 6
    lead_body = ("Ukraine says its sea drones sank the Russian corvette "
                 "Merkury off Benghazi — and confirms a second strike on "
                 "the arms ship Sparta II in the Gulf of Finland. Tripoli "
                 "condemns the attack; the UN calls for an inquiry.")
    y = para(d, lead_body, font(SANS, 20), MX, y, 600, 26)
    draw_lead_scene(d, 668, 168, 320, 208)
    d.text((668, 382), "UKRAINIAN SEA DRONES OFF BENGHAZI",
           font=font(SANS, 15), fill=MUTED)
    rule(d, MX, RX, 408, 1)

    # ---- row 2: markets + war ----
    y2 = 424
    end_l = story(d, MX, y2, col_w, "MARKETS  ·  NEW YORK",
                  "NVIDIA SOARS 31% AS HUANG RETURNS",
                  "Nvidia reinstates Jensen Huang as chief executive, 11 "
                  "days after he left. Shares jump 31% — the best day "
                  "since 2003 — adding about $950bn.",
                  art=draw_bars)
    end_r = story(d, MX + col_w + 28, y2, col_w, "WAR  ·  UKRAINE",
                  "2 KILLED AS RUSSIA HITS FLATS IN ZAPORIZHZHIA",
                  "An overnight strike partly destroys a five-storey "
                  "block; 22 are wounded, including children. A Russian "
                  "drone briefly enters Poland again.",
                  art=draw_block)
    vrule(d, mid_x, y2, max(end_l, end_r))
    rule(d, MX, RX, 652, 1)

    # ---- row 3: Gaza + Indonesia ----
    y3 = 668
    end_l = story(d, MX, y3, col_w, "GAZA",
                  "AT LEAST 6 KILLED IN GAZA STRIKES",
                  "Airstrikes kill at least six Palestinians, including "
                  "two police officers. Hamas security chief Naeem Abu "
                  "Nahel is among the dead.",
                  art=draw_skyline)
    end_r = story(d, MX + col_w + 28, y3, col_w, "INDONESIA",
                  "FACTORY FIRE TOLL RISES TO 26",
                  "The toll from the candy-factory fire in Cikande, "
                  "Banten, rises to 26 as rescuers search for eight more "
                  "workers. Over 600 rescuers are on site.",
                  art=draw_factory)
    vrule(d, mid_x, y3, max(end_l, end_r))
    rule(d, MX, RX, 896, 1)

    # ---- bottom strip: Colombia ----
    y4 = 910
    draw_burst(d, MX + 18, y4 + 12, 18)
    strip_head = "COLOMBIA  ·  CAR BOMB HITS GOVERNOR'S OFFICE"
    d.text((MX + 46, y4), strip_head, font=font(SERIF_B, 23), fill=INK)
    d.text((MX + 46, y4 + 30),
           "In Villavicencio, the blast injures more than 20; no deaths "
           "reported. President rules out talks.",
           font=font(SANS, 17), fill=INK)
    rule(d, MX, RX, 962, 1)

    # ---- footer ticker ----
    tick_f = font(SANS_B, 15)
    d.text((MX, 970),
           "ALSO TODAY:  Abu Dhabi talks end — US envoys head to Moscow  ·  "
           "Nepal quake, magnitude 5.6",
           font=tick_f, fill=NAVY)
    d.text((MX, 989),
           "Pentagon holds back 60 Patriot missiles for Kyiv  ·  World Chess "
           "Championship opens in Geneva",
           font=tick_f, fill=NAVY)
    d.text((MX, 1007), "Sources: Reuters · AP · CNN · Kyiv Independent · "
           "El Tiempo · Xinhua", font=font(SANS, 12), fill=MUTED)

    img.save(OUT, "PNG", optimize=True)


if __name__ == "__main__":
    main()
