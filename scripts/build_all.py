#!/usr/bin/env python3
"""Rebuild every SVG from config + photo. Safe to run locally or in Actions."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

order = [
    "prep_photo.py",
    "make_ascii_svg.py",
    "make_desk_card.py",
    "make_ticker.py",
    "render_heatmap_svg.py",
]
for name in order:
    print("—", name)
    runpy.run_path(str(SCRIPTS / name), run_name="__main__")
