#!/usr/bin/env python3
"""Generate a 1200x630 Open Graph PNG for a project site.

Usage:
    og_make.py OUT.png "Project Name" "One-line value proposition" ACCENT ACCENT2 MONOGRAM
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (7, 9, 13)
BORDER = (30, 41, 59)


def font(spec: str, size: int):
    path, fallback = spec, spec
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        for candidate in (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            "DejaVuSans.ttf",
        ):
            try:
                return ImageFont.truetype(candidate, size)
            except Exception:
                continue
        return ImageFont.load_default()


def hex_rgb(s: str):
    s = s.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def main():
    out, name, tagline, accent, accent2, mono = sys.argv[1:7]
    accent = hex_rgb(accent)
    accent2 = hex_rgb(accent2)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # faint glow discs
    for (cx, cy, r, col) in [
        (200, 60, 420, (*accent, 26)),
        (1010, 520, 380, (*accent2, 20)),
    ]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    d.rectangle([0, 0, W - 1, H - 1], outline=BORDER, width=2)

    # monogram tile
    tile = 128
    x0, y0 = 96, 118
    d.rounded_rectangle([x0, y0, x0 + tile, y0 + tile], radius=28, fill=accent)
    fg = hex_rgb("#fff")
    f_mono = font("", 62)
    tw = d.textlength(mono, font=f_mono)
    d.text((x0 + (tile - tw) / 2, y0 + (tile - 66) / 2), mono, font=f_mono, fill=fg)

    # name
    f_name = font("", 86)
    d.text((96, 300), name, font=f_name, fill=(232, 238, 246))

    # tagline
    f_tag = font("", 34)
    d.text((96, 420), tagline, font=f_tag, fill=(148, 163, 184))

    # footer
    f_foot = font("", 28)
    d.text((96, 548), "Bittu Sharma  ·  honeyamn10-source", font=f_foot, fill=(100, 116, 139))
    d.rounded_rectangle([W - 96 - 210, 548 - 8, W - 96, 548 + 40], radius=14,
                        outline=accent, width=2)
    d.text((W - 96 - 210 + 18, 548), "github.com", font=f_foot, fill=accent)

    img.save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()