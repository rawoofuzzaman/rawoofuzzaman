#!/usr/bin/env python3
"""Year tape — contribution calendar drawn as candles, gold/olive book."""
from __future__ import annotations

import datetime
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
USER = os.environ.get("GH_PROFILE_USER", CFG.get("github_username", "rawoofzaman"))
JSON_PATH = os.path.join(ROOT, "data", "contributions.json")
OUT = os.path.join(ROOT, "year-tape.svg")

PALETTE = ["#14160f", "#2a3320", "#4a5c32", "#8a7a28", "#c4a035", "#f0d56a"]
INK, DIM, BG, STROKE = "#e6dcc0", "#8a8370", "#08090b", "#2a2d24"
GOLD = "#d4b45a"
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
CELL, GAP, RAD, LEFT, TOP = 11, 3.2, 1.6, 40, 48


def load_days():
    if os.path.exists(JSON_PATH):
        data = json.load(open(JSON_PATH, encoding="utf-8"))
        days = data.get("days") or []
        if days:
            total = data.get("total_contributions", sum(d.get("count", 0) for d in days))
            return days, total
    url = f"https://github-contributions-api.jogruber.de/v4/{USER}?y=last"
    with urllib.request.urlopen(url, timeout=25) as r:
        payload = json.loads(r.read().decode())
    contribs = payload["contributions"]
    days = [{"date": c["date"], "count": c["count"], "level": c["level"]} for c in contribs]
    total = payload.get("total", {}).get("lastYear", sum(c["count"] for c in contribs))
    return days, total


def level_of(day: dict) -> int:
    if "level" in day:
        return max(0, min(5, int(day["level"])))
    c = int(day.get("count", 0))
    return 0 if c <= 0 else 1 if c == 1 else 2 if c <= 3 else 3 if c <= 6 else 4 if c <= 9 else 5


def main() -> None:
    days, total = load_days()
    days = sorted(days, key=lambda d: d["date"])
    first = datetime.date.fromisoformat(days[0]["date"])
    sunday_pad = (first.weekday() + 1) % 7
    padded = [{"date": None, "count": 0, "level": 0}] * sunday_pad + days
    n = len(padded)
    nw = (n + 6) // 7
    w = int(LEFT + nw * (CELL + GAP) + 22)
    h = int(TOP + 7 * (CELL + GAP) + 52)
    reveal, dur = 4.2, 0.55
    maxorder = max(1.0, (nw - 1) + 6 * 0.5)

    labels = [
        f'<text fill="{GOLD}" font-size="12" font-weight="700" letter-spacing="2" x="{LEFT}" y="22">YEAR TAPE</text>',
        f'<text fill="{DIM}" font-size="11" x="{w-22}" y="22" text-anchor="end">{USER.upper()} · VOLUME</text>',
    ]
    last_m = None
    start = first - datetime.timedelta(days=sunday_pad)
    for wk in range(nw):
        d = start + datetime.timedelta(days=wk * 7)
        if d.month != last_m:
            last_m = d.month
            labels.append(
                f'<text fill="{DIM}" font-size="9" letter-spacing="1" x="{LEFT + wk * (CELL + GAP)}" y="{TOP - 10}">{MONTHS[d.month - 1]}</text>'
            )
    for name, r in [("MON", 1), ("WED", 3), ("FRI", 5)]:
        labels.append(
            f'<text fill="{DIM}" font-size="8" x="8" y="{TOP + r * (CELL + GAP) + CELL - 2}">{name}</text>'
        )

    rects = []
    for i, c in enumerate(padded):
        wk, row = i // 7, i % 7
        lvl = level_of(c)
        x = LEFT + wk * (CELL + GAP)
        y = TOP + row * (CELL + GAP)
        delay = round((wk + row * 0.5) / maxorder * reveal, 3)
        cls = "cdle lit" if lvl else "cdle"
        rects.append(
            f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RAD}" '
            f'fill="{PALETTE[lvl]}" style="animation-delay:{delay}s"/>'
        )

    legend_y = TOP + 7 * (CELL + GAP) + 22
    legend = [f'<text fill="{DIM}" font-size="10" x="{LEFT}" y="{legend_y}">THIN</text>']
    for i, col in enumerate(PALETTE):
        legend.append(
            f'<rect x="{LEFT + 40 + i * (CELL + 3)}" y="{legend_y - 10}" width="{CELL}" height="{CELL}" rx="2" fill="{col}"/>'
        )
    legend.append(
        f'<text fill="{DIM}" font-size="10" x="{LEFT + 40 + 6 * (CELL + 3) + 4}" y="{legend_y}">THICK</text>'
    )
    total_text = f"{total:,} PRINTS · LAST 12 MONTHS"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="ui-monospace, Menlo, Consolas, monospace">
<style>
  .cdle {{ transform-box: fill-box; transform-origin: center bottom; opacity: 0; animation: candle {dur}s cubic-bezier(.2,.8,.2,1) both; }}
  .lit {{ animation: candle {dur}s cubic-bezier(.2,.8,.2,1) both, wick .35s ease-out both; }}
  @keyframes candle {{ 0% {{ opacity:0; transform: scaleY(.15); }} 70% {{ opacity:1; transform: scaleY(1.08); }} 100% {{ opacity:1; transform: scaleY(1); }} }}
  @keyframes wick {{ 0% {{ filter: brightness(1.8); }} 100% {{ filter: brightness(1); }} }}
  @media (prefers-reduced-motion: reduce) {{ .cdle {{ opacity:1 !important; animation:none !important; }} }}
</style>
<rect width="{w}" height="{h}" rx="12" fill="{BG}"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="none" stroke="{STROKE}"/>
{''.join(labels)}
{''.join(rects)}
<text fill="{INK}" font-size="12" font-weight="700" x="{LEFT}" y="{h - 12}">{total_text}</text>
{''.join(legend)}
</svg>'''
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    with open(os.path.join(ROOT, "contrib-heatmap.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT}: {len(days)} days, {total:,} contributions")


if __name__ == "__main__":
    main()
