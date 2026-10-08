#!/usr/bin/env bash
# Build the pamphlet: QR codes, then the print PDF and previews.
# Needs Python 3 with segno (pip install segno) and Node with playwright.
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/make_qr.py
node scripts/render.js
