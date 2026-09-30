#!/usr/bin/env python3
"""Cockpit-cam ASCII. CRT scan reveal — not a row-by-row typewriter clone."""
from __future__ import annotations

import html
import json
import os
import sys

from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "source-prepped.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "ascii-portrait.svg")

COLS, ROWS = 86, 48
CELL_W, CELL_H = 8.2, 14.2
RAMP = " .'`^\"-:;+*?#%@"
GAMMA = 1.12
WHITE_FLOOR = 0.84

PAD = 18
HUD_TOP = 36
HUD_BOT = 28
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = int(ART_W + PAD * 2)
CANVAS_H = int(HUD_TOP + ART_H + HUD_BOT + 10)

BG, FRAME, GOLD, INK, DIM, UP = "#08090b", "#2a2d24", "#d4b45a", "#e6dcc0", "#8a8370", "#3dd68c"
SCAN = 2.4  # seconds for the full refresh


def sample() -> list[str]:
    im = Image.open(SRC).convert("L")
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = im.resize((COLS, ROWS), Image.LANCZOS)
    px = im.load()
    rows = []
    for y in range(ROWS):
        chars = []
        for x in range(COLS):
            lum = pow(px[x, y] / 255.0, GAMMA)
            if lum >= WHITE_FLOOR:
                chars.append(" ")
                continue
            idx = int((1.0 - lum) * (len(RAMP) - 1) + 0.5)
            chars.append(RAMP[max(0, min(len(RAMP) - 1, idx))])
        rows.append("".join(chars))
    return rows


def corner(x: float, y: float, dx: int, dy: int, s: int = 14) -> str:
    return (
        f'<path d="M{x + dx * s} {y} H{x} V{y + dy * s}" fill="none" '
        f'stroke="{GOLD}" stroke-width="1.4" stroke-linecap="square"/>'
    )


def main() -> None:
    rows_txt = sample()
    static = bool(os.environ.get("STATIC"))
    name = html.escape(CFG.get("display_name", "RAWOOF UZ ZAMAN"))
    art_x, art_y = PAD, HUD_TOP
    font_size = CELL_H * 0.86

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, Menlo, Consolas, monospace">',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="{BG}"/>',
        f'<rect x=".5" y=".5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
        f'<text x="{PAD}" y="22" font-size="11" fill="{GOLD}" letter-spacing="2">CAM 01 · MARK</text>',
        f'<text x="{CANVAS_W-PAD}" y="22" font-size="11" fill="{DIM}" text-anchor="end">REC</text>',
        f'<circle cx="{CANVAS_W-PAD-28}" cy="18" r="4" fill="#d4654f">',
    ]
    if not static:
        parts.append('<animate attributeName="opacity" values="1;0.2;1" dur="1.1s" repeatCount="indefinite"/>')
    parts.append("</circle>")

    parts.append(f'<clipPath id="scan"><rect x="{art_x}" y="{art_y}" width="{ART_W}" height="0">')
    if not static:
        parts.append(
            f'<animate attributeName="height" from="0" to="{ART_H}" dur="{SCAN}s" fill="freeze"/>'
        )
    else:
        parts[-1] = f'<clipPath id="scan"><rect x="{art_x}" y="{art_y}" width="{ART_W}" height="{ART_H}">'
    parts.append("</rect></clipPath>")

    parts.append('<g clip-path="url(#scan)">')
    for i, line in enumerate(rows_txt):
        y = art_y + i * CELL_H + CELL_H * 0.78
        parts.append(
            f'<text xml:space="preserve" x="{art_x}" y="{y:.1f}" fill="{INK}" '
            f'font-size="{font_size:.1f}" textLength="{ART_W:.1f}" '
            f'lengthAdjust="spacing">{html.escape(line)}</text>'
        )
    parts.append("</g>")

    # moving scan bar
    if not static:
        parts.append(
            f'<rect x="{art_x}" width="{ART_W}" height="2" fill="{GOLD}" opacity="0.85">'
            f'<animate attributeName="y" from="{art_y}" to="{art_y + ART_H}" dur="{SCAN}s" fill="freeze"/>'
            f'<animate attributeName="opacity" from="0.9" to="0" dur="{SCAN}s" fill="freeze"/>'
            f"</rect>"
        )

    # HUD corners around the art
    parts += [
        corner(art_x - 2, art_y - 2, 1, 1),
        corner(art_x + ART_W + 2, art_y - 2, -1, 1),
        corner(art_x - 2, art_y + ART_H + 2, 1, -1),
        corner(art_x + ART_W + 2, art_y + ART_H + 2, -1, -1),
    ]

    by = CANVAS_H - 10
    parts.append(
        f'<text x="{PAD}" y="{by}" font-size="11" fill="{DIM}">IN FRAME</text>'
    )
    parts.append(
        f'<text x="{CANVAS_W/2}" y="{by}" font-size="11" fill="{INK}" text-anchor="middle">{name}</text>'
    )
    parts.append(
        f'<text x="{CANVAS_W-PAD}" y="{by}" font-size="11" fill="{UP}" text-anchor="end">IST</text>'
    )
    parts.append("</svg>")
    Path = __import__("pathlib").Path
    Path(OUT).write_text("".join(parts), encoding="utf-8")
    print("wrote", OUT, CANVAS_W, "x", CANVAS_H)


if __name__ == "__main__":
    main()
