#!/usr/bin/env python3
"""Prep a portrait for ASCII conversion using only Pillow.

The original tutorial uses rembg + OpenCV CLAHE. Those packages are heavy
and often fail for non-coders, so this version does the same job with
Pillow: grayscale, contrast, a slight crop toward the face, white-ish
background lift. Good enough for a clean monochrome portrait.

    python scripts/prep_photo.py source-photo.jpg
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")


def main() -> None:
    im = Image.open(INP).convert("RGB")
    w, h = im.size
    # Prefer a square around the head. On tall portraits, lock to full
    # width and start near the top so hair and glasses stay in frame.
    side = min(w, h)
    left = (w - side) // 2
    if h >= w:
        top = min(int(h * 0.03), h - side)
    else:
        top = (h - side) // 2
    im = im.crop((left, top, left + side, top + side))

    gray = ImageOps.grayscale(im)
    gray = ImageOps.autocontrast(gray, cutoff=2)
    gray = ImageEnhance.Contrast(gray).enhance(1.35)
    gray = ImageEnhance.Brightness(gray).enhance(1.12)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1.6, percent=120, threshold=3))

    # Lift near-white pixels so the background becomes spaces in the ramp.
    px = gray.load()
    ww, hh = gray.size
    for y in range(hh):
        for x in range(ww):
            v = px[x, y]
            if v > 210:
                px[x, y] = 255
            elif v > 185:
                px[x, y] = min(255, v + 25)

    gray.save(OUT)
    print("wrote", OUT, gray.size)


if __name__ == "__main__":
    main()
