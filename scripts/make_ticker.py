#!/usr/bin/env python3
"""Wide identity tape. Scrolls once like a pit ticker, then holds the mark."""
from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))

W, H = 860, 64
GOLD, INK, DIM, BG, STROKE = "#d4b45a", "#e6dcc0", "#8a8370", "#08090b", "#2a2d24"
items = CFG.get("ticker") or ["RUZ"]
tape = "   ·   ".join(items) + "   ·   " + "   ·   ".join(items)


def main() -> None:
    name = escape(CFG.get("display_name", "RAWOOF UZ ZAMAN"))
    mono = escape(CFG.get("monogram", "RUZ"))
    loc = escape(CFG.get("location", "IST"))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{name}">
  <defs>
    <linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{BG}" stop-opacity="1"/>
      <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fadeR" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="{BG}" stop-opacity="1"/>
      <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="tape"><rect x="118" y="22" width="620" height="28"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" rx="10" fill="{BG}"/>
  <rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{STROKE}"/>
  <rect x="12" y="12" width="88" height="40" rx="6" fill="#12140f" stroke="{STROKE}"/>
  <text x="56" y="38" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="16" font-weight="700" fill="{GOLD}" letter-spacing="3">{mono}</text>
  <g clip-path="url(#tape)">
    <text id="run" x="118" y="42" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13" fill="{INK}" letter-spacing="1.4">{escape(tape)}
      <animate attributeName="x" from="118" to="-520" dur="22s" repeatCount="indefinite"/>
    </text>
  </g>
  <rect x="118" y="22" width="36" height="28" fill="url(#fadeL)"/>
  <rect x="702" y="22" width="36" height="28" fill="url(#fadeR)"/>
  <circle cx="768" cy="32" r="4" fill="#3dd68c">
    <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
  </circle>
  <text x="780" y="28" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="9" fill="#3dd68c">LIVE</text>
  <text x="780" y="42" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="9" fill="{DIM}">{loc}</text>
</svg>'''
    out = ROOT / "banner-ticker.svg"
    out.write_text(svg, encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
