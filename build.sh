#!/usr/bin/env bash
# Build the pamphlet: QR codes, then the print PDF and previews.
# Needs Python 3 with segno, shapely, fonttools, uharfbuzz, potracer, numpy
# and pillow (pip install -r requirements.txt) and Node with playwright.
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/make_qr.py
python3 scripts/make_yard_sign.py
node scripts/render.js
