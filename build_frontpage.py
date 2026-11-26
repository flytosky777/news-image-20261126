#!/usr/bin/env python3
"""Build the 26 November 2026 news front page (1024x1024) for the
make.fun news-image-20261126 bounty. Photos are local files in assets/;
the script writes entry.png next to itself. No network is used here."""
import io
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (163, 22, 33)
GREY = (90, 86, 76)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def paste_cover(page, name, box):
    img = Image.open(os.path.join(ASSETS, name)).convert("RGB")
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    scale = max(tw / img.width, th / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = (img.width - tw) // 2
    top = (img.height - th) // 2
    page.paste(img.crop((left, top, left + tw, top + th)), (x0, y0))
    d = ImageDraw.Draw(page)
    d.rectangle(box, outline=(40, 40, 40), width=2)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # --- masthead ------------------------------------------------------
    mast = font(SERIF_B, 60)
    d.text((W // 2, 30), "THE WORLD IN ONE DAY", font=mast, fill=INK, anchor="ma")
    date_f = font(SANS_B, 21)
    d.text((W // 2, 100), "THURSDAY, 26 NOVEMBER 2026", font=date_f, fill=RED, anchor="ma")
    d.line([(28, 132), (996, 132)], fill=INK, width=3)
    d.line([(28, 138), (996, 138)], fill=INK, width=1)

    # --- hero: US tariffs ----------------------------------------------
    paste_cover(page, "hero.jpg", (28, 156, 628, 576))
    d.text((28, 582), "Containers wait at a port: the new duties target subsidised factory goods.",
           font=font(SANS, 14), fill=GREY)
    x = 652
    d.text((x, 156), "TRADE", font=font(SANS_B, 20), fill=RED)
    head = font(SERIF_B, 40)
    lines = wrap(d, "US hits China, EU and Brazil with new tariffs", head, 996 - x)
    y = 188
    for line in lines:
        d.text((x, y), line, font=head, fill=INK)
        y += 48
    body = font(SANS, 19)
    stand = ("Trump proposes 20% on Chinese goods and levies on "
             "14 trading partners. Brazil is singled out for extra "
             "duties on sugar and aircraft. A hearing is set for "
             "January; the tariffs would bite from February.")
    y += 8
    for line in wrap(d, stand, body, 996 - x):
        d.text((x, y), line, font=body, fill=INK)
        y += 26

    # --- divider ---------------------------------------------------------
    d.line([(28, 622), (996, 622)], fill=INK, width=2)

    # --- five smaller stories -------------------------------------------
    stories = [
        ("fire.jpg", "EGYPT", "Tanker fire kills 31 on Cairo ring road",
         "Fuel truck overturns and explodes; 27 vehicles charred, 21 people hurt."),
        ("court.jpg", "ISRAEL", "Judges urge dropping Netanyahu bribery case",
         "Court says a conviction in Case 4000 is unlikely; a second case to be reconsidered."),
        ("jets.jpg", "UKRAINE", "Ukraine hits five Russian jets at airfield",
         "Three MiG-31s and two Su-34s damaged at Savasleyka, 300 km east of Moscow."),
        ("warship.jpg", "LIBYA", "Two Libyan officers die after drone strike",
         "Wounded in Ukraine's attack on a Russian warship at Benghazi; the Libyan army vows retaliation."),
        ("space.jpg", "SPACE", "Pakistan's first astronaut reaches Tiangong",
         "Shenzhou-24 docks; Zeeshan Ali is the first foreign visitor to China's station."),
    ]
    col_w, gap, x0, thumb_h = 184, 12, 28, 122
    for i, (img, kicker, headline, summary) in enumerate(stories):
        cx = x0 + i * (col_w + gap)
        paste_cover(page, img, (cx, 644, cx + col_w, 644 + thumb_h))
        y = 644 + thumb_h + 10
        d.text((cx, y), kicker, font=font(SANS_B, 14), fill=RED)
        y += 22
        hf = font(SERIF_B, 19)
        for line in wrap(d, headline, hf, col_w):
            d.text((cx, y), line, font=hf, fill=INK)
            y += 24
        y += 4
        sf = font(SANS, 14)
        for line in wrap(d, summary, sf, col_w):
            d.text((cx, y), line, font=sf, fill=(40, 40, 40))
            y += 19

    d.text((W // 2, 994), "Photos: Wikimedia Commons (illustrative)",
           font=font(SANS, 12), fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    buf = io.BytesIO()
    page.save(buf, format="PNG", optimize=True)
    data = buf.getvalue()
    fmt = "PNG"
    if len(data) > 1048576:
        buf = io.BytesIO()
        page.save(buf, format="JPEG", quality=88, optimize=True)
        data = buf.getvalue()
        fmt = "JPEG"
    with open(out, "wb") as f:
        f.write(data)
    print(f"wrote {out} ({len(data)} bytes, {fmt})")


if __name__ == "__main__":
    main()
