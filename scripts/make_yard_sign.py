"""Build the yard sign: preview art and laser-cut stencil files.

Writes to build/yard-sign/:
  yard-sign.svg           full-size colored art (24 x 18 in), for previews
                          and for a sign shop that prints directly
  stencil-rust.svg        laser file: FREE MAKERSPACE and the gear logo
  stencil-dark.svg        laser file: the name and the website
  stencil-one-color.svg   laser file: everything, for a one-color sign

Laser files: red hairlines are the stencil cuts, the blue hairline is the
outline of a 24 x 18 in sheet (skip it if the sheet is already that size).
Units are inches.

The script checks every stencil for islands (pieces with no bridge to the
rest of the sheet, which would fall out) and fails if it finds one.
"""
import io
import pathlib
import sys

import numpy as np
import potrace
import uharfbuzz as hb
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from PIL import Image, ImageFilter
from shapely import affinity
from shapely.geometry import LineString, MultiPolygon, Polygon, box
from shapely.ops import unary_union

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "yard-sign"
FONT = ROOT / "assets" / "fonts" / "BigShouldersStencilDisplay-ExtraBold.woff"
LOGO = ROOT / "assets" / "logo" / "cgw-gear.png"

W, H = 24.0, 18.0          # sign, inches (landscape; flutes run vertically for H-stakes)
MARGIN = 1.0
RUST = "#BF4D28"           # website brand color
INK = "#1F1F23"            # website ink

# ---------------------------------------------------------------- geometry

class FlattenPen(BasePen):
    """Collects glyph contours as lists of points, curves flattened."""

    def __init__(self, glyphset, steps=12):
        super().__init__(glyphset)
        self.contours, self.cur, self.steps = [], [], steps

    def _moveTo(self, p):
        self.cur = [p]

    def _lineTo(self, p):
        self.cur.append(p)

    def _curveToOne(self, p1, p2, p3):
        p0 = self.cur[-1]
        for i in range(1, self.steps + 1):
            t = i / self.steps
            mt = 1 - t
            self.cur.append((
                mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0],
                mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1],
            ))

    def _qCurveToOne(self, p1, p2):
        p0 = self.cur[-1]
        for i in range(1, self.steps + 1):
            t = i / self.steps
            mt = 1 - t
            self.cur.append((
                mt**2 * p0[0] + 2 * mt * t * p1[0] + t**2 * p2[0],
                mt**2 * p0[1] + 2 * mt * t * p1[1] + t**2 * p2[1],
            ))

    def _closePath(self):
        if len(self.cur) >= 3:
            self.contours.append(self.cur)
        self.cur = []

    _endPath = _closePath


def contours_to_shape(contours):
    """Nonzero fill: contours wound like the largest one are solid, the
    others are holes. Handles overlapping contours, unlike even-odd."""
    polys = [Polygon(c).buffer(0) for c in contours]
    signed = [Polygon(c).exterior.is_ccw for c in contours]
    if not polys:
        return Polygon()
    outer_dir = signed[max(range(len(polys)), key=lambda i: polys[i].area)]
    solid = unary_union([p for p, d in zip(polys, signed) if d == outer_dir])
    holes = unary_union([p for p, d in zip(polys, signed) if d != outer_dir])
    return solid.difference(holes)


class Font:
    def __init__(self, path):
        self.tt = TTFont(path)
        self.upem = self.tt["head"].unitsPerEm
        self.cap = self.tt["OS/2"].sCapHeight
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        # HarfBuzz can't read WOFF; hand it the same font as plain TrueType.
        raw = io.BytesIO()
        self.tt.flavor = None
        self.tt.save(raw)
        self.hbfont = hb.Font(hb.Face(hb.Blob(raw.getvalue())))

    def text(self, s, cap_height, tracking=0.0):
        """Outline of s with its cap height scaled to cap_height inches.
        Returns a shape in SVG orientation (y down) with the baseline at y=0."""
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {"kern": True})
        x, parts = 0, []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            pen = FlattenPen(self.glyphs)
            self.glyphs[self.order[info.codepoint]].draw(pen)
            g = contours_to_shape(pen.contours)
            if not g.is_empty:
                parts.append(affinity.translate(g, x + pos.x_offset, pos.y_offset))
            x += pos.x_advance + tracking * self.upem
        k = cap_height / self.cap
        shape = unary_union(parts)
        return affinity.scale(shape, k, -k, origin=(0, 0))


def trace_logo(path):
    """Trace the gear PNG (alpha mask) to polygons, 1 unit = 1 pixel, y down."""
    # The PNG is orange on an opaque white background, and only 512 px, so:
    # mark the orange pixels, upscale, and blur before thresholding so the
    # trace follows the shape rather than the pixel stair-steps.
    rgb = np.array(Image.open(path).convert("RGB")).astype(int)
    ink = ((rgb[:, :, 0] - rgb[:, :, 2]) > 60).astype(np.uint8) * 255
    img = Image.fromarray(ink).resize((ink.shape[1] * 4, ink.shape[0] * 4), Image.LANCZOS)
    img = img.filter(ImageFilter.GaussianBlur(5))
    # potracer traces the False pixels, so the ink is passed in as False
    mask = np.array(img) <= 127
    paths = potrace.Bitmap(mask).trace(turdsize=8, alphamax=1.0, opticurve=True)
    contours = []
    xy = lambda p: (p.x, p.y)
    for curve in paths:
        pts = [xy(curve.start_point)]
        for seg in curve.segments:
            if seg.is_corner:
                pts += [xy(seg.c), xy(seg.end_point)]
            else:
                p0 = np.array(pts[-1]); c1 = np.array(xy(seg.c1)); c2 = np.array(xy(seg.c2)); p3 = np.array(xy(seg.end_point))
                for t in np.linspace(0, 1, 13)[1:]:
                    mt = 1 - t
                    pts.append(tuple(mt**3 * p0 + 3 * mt**2 * t * c1 + 3 * mt * t**2 * c2 + t**3 * p3))
        contours.append(pts)
    # potrace returns outer shapes and holes in nesting order; even-odd is exact here
    shape = Polygon()
    for c in contours:
        shape = shape.symmetric_difference(Polygon(c).buffer(0))
    return affinity.scale(shape, 0.25, 0.25, origin=(0, 0)), img.width / 4


def bridge_logo(logo, size, angles_deg, width):
    """Cut radial bridges through the gear ring so the disc inside it stays
    attached to the sheet. Angles are degrees, 0 = right, clockwise (y down)."""
    cx, cy = size / 2, size / 2
    r = size / 2
    cuts = []
    for a in angles_deg:
        t = np.radians(a)
        p0 = (cx + 0.55 * r * np.cos(t), cy + 0.55 * r * np.sin(t))
        p1 = (cx + 1.1 * r * np.cos(t), cy + 1.1 * r * np.sin(t))
        cuts.append(LineString([p0, p1]).buffer(width / 2, cap_style="flat"))
    return logo.difference(unary_union(cuts))


def bounds_size(g):
    x0, y0, x1, y1 = g.bounds
    return x1 - x0, y1 - y0


def place(g, x, y):
    """Move g so its bounding box's top-left corner is at (x, y)."""
    x0, y0, _, _ = g.bounds
    return affinity.translate(g, x - x0, y - y0)


def polygons(g):
    if g.is_empty:
        return []
    return list(g.geoms) if isinstance(g, MultiPolygon) else [g]


def islands(g):
    """Holes inside cut-outs are loose pieces of stencil."""
    return sum(len(p.interiors) for p in polygons(g))


def to_path(g):
    d = []
    for p in polygons(g):
        for ring in [p.exterior, *p.interiors]:
            pts = list(ring.coords)
            d.append("M" + " L".join(f"{x:.4f},{y:.4f}" for x, y in pts) + " Z")
    return " ".join(d)


def svg(body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}in" height="{H}in" '
            f'viewBox="0 0 {W} {H}">\n<title>{title}</title>\n{body}\n</svg>\n')

# ------------------------------------------------------------------ layout

def build():
    font = Font(FONT)
    span = W - 2 * MARGIN

    # Line 1: FREE MAKERSPACE, as wide as the sign allows
    free = font.text("FREE MAKERSPACE", 1.0, tracking=0.02)
    fw, _ = bounds_size(free)
    free = font.text("FREE MAKERSPACE", span / fw, tracking=0.02)

    # Lockup: gear logo left, name stacked right, the block as wide as line 1.
    # Solve for the cap height c of the name lines: name width scales with c,
    # and the logo is as tall as the three-line block (3c + 2 gaps of 0.36c).
    unit = font.text("COLUMBIA", 1.0, tracking=0.02)
    name_w_per_cap, _ = bounds_size(unit)
    gap_ratio, logo_gap = 0.36, 0.7
    block_per_cap = 3 + 2 * gap_ratio
    c = (span - logo_gap) / (name_w_per_cap + block_per_cap)
    logo_size = block_per_cap * c
    names = [font.text(s, c, tracking=0.02) for s in ("COLUMBIA", "GADGET", "WORKS")]

    raw_logo, px = trace_logo(LOGO)
    logo = affinity.scale(raw_logo, logo_size / px, logo_size / px, origin=(0, 0))
    # Smooth what's left of the source's pixel edges: a small close then open
    # (in inches) rounds off ripples without changing the shape.
    r = 0.04
    logo = logo.buffer(r, join_style="mitre").buffer(-2 * r, join_style="mitre").buffer(r, join_style="mitre")
    logo = logo.simplify(0.008)
    # The needle splits the disc in two; two bridges for each half.
    logo = bridge_logo(logo, logo_size, angles_deg=[-55, 15, 125, 195], width=0.2)

    url = font.text("COLUMBIAGADGETWORKS.ORG", 0.72, tracking=0.06)

    # Vertical rhythm, centered on the sign
    _, free_h = bounds_size(free)
    _, url_h = bounds_size(url)
    gap1, gap2 = 1.0, 0.85
    total = free_h + gap1 + logo_size + gap2 + url_h
    y = (H - total) / 2

    free = place(free, MARGIN, y)
    y += free_h + gap1
    logo = place(logo, MARGIN, y)
    nx = MARGIN + logo_size + logo_gap
    ny = y
    placed = []
    for n in names:
        placed.append(place(n, nx, ny))
        ny += c * (1 + gap_ratio)
    y += logo_size + gap2
    uw, _ = bounds_size(url)
    url = place(url, (W - uw) / 2, y)

    rust = unary_union([free, logo])
    dark = unary_union([*placed, url])
    return rust, dark


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rust, dark = build()

    problems = {name: islands(g) for name, g in (("rust", rust), ("dark", dark))}
    for name, n in problems.items():
        print(f"stencil-{name}: {len(polygons(rust if name == 'rust' else dark))} cut-outs, {n} islands")
    if any(problems.values()):
        sys.exit("A stencil has islands (loose pieces). Add bridges before cutting.")

    x0 = min(rust.bounds[0], dark.bounds[0]); x1 = max(rust.bounds[2], dark.bounds[2])
    y0 = min(rust.bounds[1], dark.bounds[1]); y1 = max(rust.bounds[3], dark.bounds[3])
    print(f"art spans {x1 - x0:.2f} x {y1 - y0:.2f} in, margins L{x0:.2f} R{W - x1:.2f} T{y0:.2f} B{H - y1:.2f}")

    art = (f'<rect width="{W}" height="{H}" fill="#fff"/>\n'
           f'<path fill="{RUST}" fill-rule="evenodd" d="{to_path(rust)}"/>\n'
           f'<path fill="{INK}" fill-rule="evenodd" d="{to_path(dark)}"/>')
    (OUT / "yard-sign.svg").write_text(svg(art, "Columbia Gadget Works yard sign"))

    sheet = f'<rect width="{W}" height="{H}" fill="none" stroke="#0000FF" stroke-width="0.002"/>'
    cut = '<path fill="none" stroke="#FF0000" stroke-width="0.002" d="{}"/>'
    for name, g in (("rust", rust), ("dark", dark), ("one-color", unary_union([rust, dark]))):
        body = sheet + "\n" + cut.format(to_path(g))
        (OUT / f"stencil-{name}.svg").write_text(svg(body, f"Yard sign stencil ({name})"))
    print("build/yard-sign/: yard-sign.svg, stencil-rust.svg, stencil-dark.svg, stencil-one-color.svg")


if __name__ == "__main__":
    main()
