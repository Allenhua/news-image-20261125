#!/usr/bin/env python3
"""Draw entry.png for the 25 November 2026 world-news image (make.fun bounty
news-image-20261125). Flat vector-style newspaper front page, drawn with PIL.
1024x1024, all text rendered with DejaVu fonts already on the VM."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (15, 30, 51)
NAVY2 = (24, 48, 80)
GOLD = (212, 160, 23)
WHITE = (255, 255, 255)
INK = (18, 24, 34)
GREY = (84, 96, 112)
LIGHT = (238, 242, 247)
RED = (178, 34, 34)
DARKRED = (122, 20, 20)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

# ---------- header ----------
d.rectangle([0, 0, W, 148], fill=NAVY)
d.rectangle([0, 148, W, 154], fill=GOLD)
d.text((28, 18), "WORLD NEWS  •  THE DAY IN PICTURES",
       font=font(FB, 24), fill=(150, 180, 215))
d.text((28, 48), "25 NOVEMBER 2026", font=font(FB, 66), fill=WHITE)
d.text((28, 116), "Wednesday — six stories that defined the day",
       font=font(FR, 24), fill=(200, 214, 230))
d.ellipse([W - 118, 34, W - 42, 110], outline=GOLD, width=5)
d.text((W - 80, 60), "25", font=font(FB, 32), fill=GOLD, anchor="mm")
d.text((W - 80, 92), "NOV", font=font(FB, 19), fill=GOLD, anchor="mm")

# ---------- card data: (tag, colour, headline, sublabel, icon key) ----------
cards = [
    ("RIYADH", (178, 34, 34), "Tower hit again",
     "Houthi drone hits the capital's tallest tower again — 11 hurt, the second strike in a week.",
     "tower"),
    ("CHINA", (150, 30, 30), "Shanghai chief probed",
     "China investigates Politburo member Chen Jining — the fourth of 24 top leaders to fall.",
     "probe"),
    ("COLOMBIA", (18, 110, 130), "Hostage siege in Cartagena",
     "Gunmen seize about 30 in a supermarket after a failed armoured robbery; 10 freed.",
     "shop"),
    ("GAZA", (120, 60, 20), "Hamas security chief killed",
     "Israeli air strike kills Naim Abu Nahal; seven dead in all despite the ceasefire.",
     "blast"),
    ("UNITED STATES", (24, 64, 140), "Huawei found guilty",
     "US jury convicts Huawei on 10 of 12 counts — fraud, sanctions, trade-secret theft.",
     "court"),
    ("SOUTH KOREA", (16, 120, 70), "Seoul subway strike called off",
     "Last-minute deal at 2:40 a.m.: 3.5% pay rise, 500 new hires, 2,212 job cuts shelved.",
     "train"),
]

MX, MY = 24, 170
GW, GH = 16, 16
CW = (W - 2 * MX - GW) // 2   # 480
CH = 236


def icon(draw, key, x, y, s, col):
    """Flat pictogram inside a s x s box at (x, y)."""
    if key == "tower":
        # skyscraper with a smoke burst near the top
        draw.rectangle([x + s * 0.38, y + s * 0.30, x + s * 0.62, y + s * 0.95], fill=NAVY2)
        draw.polygon([(x + s * 0.38, y + s * 0.30), (x + s * 0.50, y + s * 0.12),
                      (x + s * 0.62, y + s * 0.30)], fill=NAVY2)
        for r in range(4):
            draw.rectangle([x + s * 0.43, y + s * (0.38 + r * 0.14),
                            x + s * 0.57, y + s * (0.44 + r * 0.14)], fill=(150, 180, 215))
        # drone
        draw.ellipse([x + s * 0.72, y + s * 0.10, x + s * 0.82, y + s * 0.20], fill=col)
        draw.line([x + s * 0.68, y + s * 0.15, x + s * 0.86, y + s * 0.15], fill=col, width=4)
        # smoke puffs
        for cx, cy, rr in [(0.24, 0.30, 0.09), (0.16, 0.42, 0.11), (0.30, 0.48, 0.08)]:
            draw.ellipse([x + s * (cx - rr), y + s * (cy - rr),
                          x + s * (cx + rr), y + s * (cy + rr)], fill=(120, 128, 140))
    elif key == "probe":
        # magnifying glass over a skyline
        for bx, bw, bh in [(0.08, 0.16, 0.55), (0.28, 0.16, 0.75), (0.48, 0.16, 0.45), (0.68, 0.16, 0.65)]:
            draw.rectangle([x + s * bx, y + s * (0.95 - bh), x + s * (bx + bw), y + s * 0.95],
                           fill=NAVY2)
        draw.ellipse([x + s * 0.52, y + s * 0.06, x + s * 0.94, y + s * 0.48],
                     outline=col, width=9)
        draw.line([x + s * 0.84, y + s * 0.40, x + s * 0.98, y + s * 0.54], fill=col, width=9)
        draw.text((x + s * 0.73, y + s * 0.27), "?", font=font(FB, int(s * 0.26)),
                  fill=col, anchor="mm")
    elif key == "shop":
        # storefront with awning + shield
        draw.rectangle([x + s * 0.10, y + s * 0.30, x + s * 0.90, y + s * 0.92], fill=NAVY2)
        for i in range(5):
            c = col if i % 2 == 0 else WHITE
            draw.polygon([(x + s * (0.10 + i * 0.16), y + s * 0.30),
                          (x + s * (0.26 + i * 0.16), y + s * 0.30),
                          (x + s * (0.26 + i * 0.16), y + s * 0.46),
                          (x + s * (0.10 + i * 0.16), y + s * 0.46)], fill=c)
        draw.rectangle([x + s * 0.40, y + s * 0.58, x + s * 0.60, y + s * 0.92], fill=GOLD)
        draw.polygon([(x + s * 0.78, y + s * 0.02), (x + s * 0.98, y + s * 0.10),
                      (x + s * 0.98, y + s * 0.30), (x + s * 0.88, y + s * 0.44),
                      (x + s * 0.78, y + s * 0.30)], fill=col)
    elif key == "blast":
        # explosion star over broken buildings
        draw.rectangle([x + s * 0.08, y + s * 0.62, x + s * 0.30, y + s * 0.95], fill=NAVY2)
        draw.rectangle([x + s * 0.68, y + s * 0.55, x + s * 0.92, y + s * 0.95], fill=NAVY2)
        cx, cy, r1, r2 = x + s * 0.50, y + s * 0.38, s * 0.34, s * 0.15
        pts = []
        import math
        for i in range(16):
            r = r1 if i % 2 == 0 else r2
            a = math.pi * i / 8 - math.pi / 2
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        draw.polygon(pts, fill=col)
        draw.ellipse([cx - s * 0.07, cy - s * 0.07, cx + s * 0.07, cy + s * 0.07],
                     fill=GOLD)
    elif key == "court":
        # courthouse + gavel
        draw.polygon([(x + s * 0.10, y + s * 0.30), (x + s * 0.50, y + s * 0.08),
                      (x + s * 0.90, y + s * 0.30)], fill=NAVY2)
        for i, bx in enumerate([0.16, 0.38, 0.60, 0.80]):
            draw.rectangle([x + s * bx, y + s * 0.36, x + s * (bx + 0.06), y + s * 0.72],
                           fill=NAVY2)
        draw.rectangle([x + s * 0.10, y + s * 0.72, x + s * 0.90, y + s * 0.80], fill=NAVY2)
        draw.rectangle([x + s * 0.06, y + s * 0.82, x + s * 0.94, y + s * 0.92], fill=NAVY2)
        draw.rectangle([x + s * 0.66, y + s * 0.86, x + s * 0.94, y + s * 0.94],
                       fill=col, outline=NAVY, width=2)
        draw.line([x + s * 0.68, y + s * 0.90, x + s * 0.92, y + s * 0.90], fill=NAVY, width=3)
    elif key == "train":
        # subway front
        draw.rounded_rectangle([x + s * 0.08, y + s * 0.18, x + s * 0.92, y + s * 0.88],
                               radius=18, fill=col)
        draw.rounded_rectangle([x + s * 0.18, y + s * 0.28, x + s * 0.82, y + s * 0.52],
                               radius=10, fill=(210, 235, 245))
        draw.line([x + s * 0.50, y + s * 0.28, x + s * 0.50, y + s * 0.52], fill=NAVY2, width=4)
        for cx in (0.30, 0.70):
            draw.ellipse([x + s * (cx - 0.06), y + s * 0.60, x + s * (cx + 0.06),
                          y + s * 0.72], fill=GOLD)
        draw.rectangle([x + s * 0.08, y + s * 0.92, x + s * 0.92, y + s * 0.97], fill=NAVY2)


for i, (tag, col, head, sub, key) in enumerate(cards):
    cx = MX + (i % 2) * (CW + GW)
    cy = MY + (i // 2) * (CH + GH)
    # card
    d.rounded_rectangle([cx, cy, cx + CW, cy + CH], radius=10, fill=WHITE,
                        outline=(200, 208, 218), width=2)
    d.rectangle([cx, cy, cx + CW, cy + 8], fill=col)
    # icon panel
    d.rectangle([cx + 14, cy + 22, cx + 138, cy + 146], fill=LIGHT)
    icon(d, key, cx + 14, cy + 22, 124, col)
    # tag + headline + sub
    tx = cx + 152
    d.text((tx, cy + 24), tag, font=font(FB, 19), fill=col)
    hl = wrap(d, head, font(FB, 27), CW - 152 - 14)
    y = cy + 50
    for ln in hl[:2]:
        d.text((tx, y), ln, font=font(FB, 27), fill=INK)
        y += 33
    sl = wrap(d, sub, font(FR, 20), CW - 152 - 14)
    y += 4
    for ln in sl[:3]:
        d.text((tx, y), ln, font=font(FR, 20), fill=GREY)
        y += 25

# ---------- footer: UN femicide stat ----------
fy = MY + 3 * CH + 2 * GH + 4   # 934
d.rectangle([0, fy, W, H], fill=DARKRED)
d.text((28, fy + 14), "ALSO TODAY  •  UNITED NATIONS",
       font=font(FB, 20), fill=(245, 200, 200))
d.text((28, fy + 40),
       "5 women were killed every hour by a partner",
       font=font(FB, 25), fill=WHITE)
d.text((28, fy + 40 + 30),
       "or relative in 2025 — 47,000 in all.",
       font=font(FB, 25), fill=WHITE)
d.text((W - 28, fy + 40), "16 Days of\nActivism begins",
       font=font(FR, 19), fill=(245, 200, 200), anchor="ra")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
