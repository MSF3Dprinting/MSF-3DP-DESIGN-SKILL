#!/usr/bin/env python3
"""overlay_sketch.py — draw an STL section or silhouette over the user's photo or sketch.

The overlay check (workflow §3.6 / T21): the modelled outline, taken from the EXPORTED STL,
is drawn as a coloured line on the (anonymised, metadata-free) image so that anyone can see
whether it follows the real edge. Works with any STL and any image; you supply the mapping.

Usage
  # 1. calibrate: two pixel points on the image whose real distance you know (e.g. a ruler)
  python3 overlay_sketch.py photo.png --calib 412,880,1330,884,50        # -> px per mm
  # 2. overlay a section at Z = 3 mm, STL origin at pixel (700, 500), part rotated 12° in the image
  python3 overlay_sketch.py photo.png --stl part.stl --z 3 --scale 18.36 --origin 700,500 --rot 12 --out img/part_overlay.png
  # or the outline seen from above / the front / the side
  python3 overlay_sketch.py sketch.png --stl part.stl --view top --scale 18.36 --origin 700,500 --out img/part_overlay.png
  # a grid every 10 mm helps to judge scale and alignment
  python3 overlay_sketch.py ... --grid 10

Mapping: pixel = origin + scale * R(rot) * (u, v), with the image Y axis pointing down. For --z the
outline coordinates are the part's (x, y); for --view front they are (x, z), for --view side (y, z).
Strip metadata first (Pillow re-save without exif) — this script re-saves without metadata too.
"""
import argparse
import math
import sys

import numpy as np


def calibrate(spec):
    x1, y1, x2, y2, mm = (float(v) for v in spec.split(","))
    px = math.hypot(x2 - x1, y2 - y1)
    scale = px / mm
    print(f"{px:.1f} px over {mm:g} mm  ->  scale {scale:.3f} px/mm")
    return scale


def section_polylines(mesh, z):
    """Closed polylines (in x, y) of the mesh cut at height z."""
    sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if sec is None:
        return []
    lines = []
    for ent in sec.entities:
        pts = sec.vertices[ent.points][:, :2]
        lines.append(pts)
    return lines


def silhouette_polylines(mesh, view):
    """Outline of the mesh projected on a plane: union of the projected triangles."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    axes = {"top": (0, 1), "front": (0, 2), "side": (1, 2)}[view]
    tris = mesh.triangles[:, :, axes]
    polys = [Polygon(t) for t in tris if Polygon(t).area > 1e-6]
    u = unary_union(polys).buffer(0)
    geoms = getattr(u, "geoms", [u])
    lines = []
    for g in geoms:
        lines.append(np.array(g.exterior.coords))
        for hole in g.interiors:
            lines.append(np.array(hole.coords))
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--calib", help="x1,y1,x2,y2,mm — print the scale and exit")
    ap.add_argument("--stl")
    ap.add_argument("--z", type=float, help="section height in mm")
    ap.add_argument("--view", choices=["top", "front", "side"], help="silhouette instead of a section")
    ap.add_argument("--scale", type=float, help="px per mm")
    ap.add_argument("--origin", help="pixel x,y of the part origin")
    ap.add_argument("--rot", type=float, default=0.0, help="rotation of the part in the image, degrees (counter-clockwise on screen)")
    ap.add_argument("--flip-y", action="store_true", help="mirror the part's second axis (use when the image shows the underside)")
    ap.add_argument("--color", default="#ff00cc")
    ap.add_argument("--width", type=int, default=3)
    ap.add_argument("--grid", type=float, default=0.0, help="draw a grid every N mm around the origin")
    ap.add_argument("--out", default="overlay.png")
    a = ap.parse_args(argv)

    if a.calib:
        calibrate(a.calib)
        return 0
    if not (a.stl and a.scale and a.origin and (a.z is not None or a.view)):
        ap.error("need --stl, --scale, --origin and either --z or --view (or --calib)")

    import trimesh
    from PIL import Image, ImageDraw
    mesh = trimesh.load(a.stl, force="mesh")
    lines = section_polylines(mesh, a.z) if a.z is not None else silhouette_polylines(mesh, a.view)
    if not lines:
        print("no outline at that height / view")
        return 1

    ox, oy = (float(v) for v in a.origin.split(","))
    c, s = math.cos(math.radians(a.rot)), math.sin(math.radians(a.rot))
    sy = -1.0 if a.flip_y else 1.0

    def to_px(u, v):
        v = v * sy
        x = ox + a.scale * (c * u - s * v)
        y = oy - a.scale * (s * u + c * v)  # image Y points down
        return (x, y)

    im = Image.open(a.image).convert("RGB")
    d = ImageDraw.Draw(im)
    if a.grid > 0:
        n = int(max(im.width, im.height) / (a.scale * a.grid)) + 1
        for k in range(-n, n + 1):
            d.line([to_px(k * a.grid, -n * a.grid), to_px(k * a.grid, n * a.grid)], fill="#88888866", width=1)
            d.line([to_px(-n * a.grid, k * a.grid), to_px(n * a.grid, k * a.grid)], fill="#88888866", width=1)
    for pts in lines:
        px = [to_px(float(u), float(v)) for u, v in pts]
        if len(px) > 1:
            d.line(px + [px[0]], fill=a.color, width=a.width)
    r = 5
    d.ellipse([ox - r, oy - r, ox + r, oy + r], outline=a.color, width=2)
    im.save(a.out)  # no metadata carried over
    print(f"overlay written to {a.out}: {len(lines)} outline(s), scale {a.scale} px/mm, origin ({ox:g}, {oy:g}), rot {a.rot}°")
    return 0


if __name__ == "__main__":
    sys.exit(main())
