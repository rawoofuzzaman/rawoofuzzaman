#!/usr/bin/env python3
"""Blotter-style desk card. Not a neofetch clone."""
from __future__ import annotations

import json
import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))

W, H = 700, 690
BG, PANEL, STROKE = "#08090b", "#10120e", "#2a2d24"
GOLD, INK, DIM, UP = "#d4b45a", "#e6dcc0", "#8a8370", "#3dd68c"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def wrap(text: str, width: int = 34) -> list[str]:
    out, line = [], ""
    for word in text.split():
        cand = f"{line} {word}".strip()
        if len(cand) > width and line:
            out.append(line)
            line = word
        else:
            line = cand
    if line:
        out.append(line)
    return out


def main() -> None:
    static = os.environ.get("STATIC") == "1"
    rows = CFG.get("desk") or []
    name = escape(CFG.get("display_name", "RAWOOF"))
    mono = escape(CFG.get("monogram", "RUZ"))
    tag = escape(CFG.get("tagline", ""))
    handle = escape(CFG.get("x_handle", ""))
    loc = escape(CFG.get("location", ""))

    parts = [
        f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>',
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{STROKE}"/>',
        f'<rect x="22" y="22" width="64" height="36" rx="6" fill="{PANEL}" stroke="{STROKE}"/>',
        f'<text x="54" y="46" text-anchor="middle" font-size="15" font-weight="700" fill="{GOLD}" letter-spacing="2">{mono}</text>',
        f'<text x="100" y="38" font-size="16" font-weight="700" fill="{INK}">{name}</text>',
        f'<text x="100" y="56" font-size="11" fill="{DIM}" letter-spacing="1.2">{escape(tag.upper()) if tag else "DESK"}</text>',
        f'<text x="{W-28}" y="40" text-anchor="end" font-size="10" fill="{UP}">MARK</text>',
        f'<text x="{W-28}" y="56" text-anchor="end" font-size="13" fill="{UP}">OPEN</text>',
        f'<line x1="22" y1="76" x2="{W-22}" y2="76" stroke="{STROKE}"/>',
    ]

    y = 112
    for i, (key, val) in enumerate(rows):
        delay = 0.12 + i * 0.16
        cls = "" if static else ' class="row"'
        dly = "" if static else f' style="animation-delay:{delay:.2f}s"'
        parts.append(
            f'<text{cls}{dly} x="28" y="{y}" font-size="11" font-weight="700" fill="{GOLD}" letter-spacing="2">{escape(key)}</text>'
        )
        chunks = wrap(val)
        for j, chunk in enumerate(chunks):
            parts.append(
                f'<text{cls}{dly} x="28" y="{y + 22 + j * 20}" font-size="15" fill="{INK}">{escape(chunk)}</text>'
            )
        y += 22 + len(chunks) * 20 + 22
        parts.append(f'<line x1="22" y1="{y - 14}" x2="{W-22}" y2="{y - 14}" stroke="{STROKE}" stroke-dasharray="2 6"/>')

    # footer chips
    chips = [("X", f"@{handle}" if handle else "X"), ("BASE", loc), ("MODE", "BUILD + TRADE")]
    cx = 28
    for label, value in chips:
        tw = 18 + max(len(label), len(value)) * 8.2
        parts.append(f'<rect x="{cx}" y="{H-78}" width="{tw}" height="44" rx="8" fill="{PANEL}" stroke="{STROKE}"/>')
        parts.append(
            f'<text x="{cx + 12}" y="{H-60}" font-size="9" fill="{GOLD}" letter-spacing="1.4">{escape(label)}</text>'
        )
        parts.append(f'<text x="{cx + 12}" y="{H-44}" font-size="12" fill="{INK}">{escape(value)}</text>')
        cx += tw + 12

    style = "" if static else (
        "<style>"
        "@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}"
        ".row{animation:rise .5s ease both}"
        "@media (prefers-reduced-motion:reduce){.row{animation:none}}"
        "</style>"
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Desk blotter">'
        f"{style}<g font-family=\"{MONO}\">{''.join(parts)}</g></svg>"
    )
    out = ROOT / "desk-card.svg"
    out.write_text(svg, encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
