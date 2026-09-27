#!/usr/bin/env python3
"""section_from_stl.py — a section drawing straight from the exported STL (MSF "3D Printing for All").

Cuts the mesh with a plane and draws the cut faces filled, on a millimetre grid, with the thinnest wall
marked. Exact (it is the STL that will be printed), fast (no OpenSCAD render), and the picture the README,
the design review and the structural review (T24) need: where the material is, where it is thin, how the
layers run. Z cuts are plan views (the layers lie in the picture); X and Y cuts are side views (layers
horizontal — the build direction points up the page).

Usage
  python3 section_from_stl.py part.stl --z 10 --out img/part_section_z10.png
  python3 section_from_stl.py part.stl --x 0  --out img/part_section_x0.png --title "Through the tab"
  python3 section_from_stl.py part.stl --y 5  --min-wall 1.6
Exit code 1 when the plane misses the part.
"""
import argparse
import os
import sys

import numpy as np

sys.dont_write_bytecode = True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stl")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--z", type=float); g.add_argument("--x", type=float); g.add_argument("--y", type=float)
    ap.add_argument("--out", default=None, help="default: <stl stem>_section_<axis><value>.png next to the STL")
    ap.add_argument("--title", default="")
    ap.add_argument("--min-wall", type=float, default=1.6, help="walls thinner than this are marked red")
    a = ap.parse_args(argv)

    import trimesh
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch

    axis, val = [(k, getattr(a, k)) for k in ("z", "x", "y") if getattr(a, k) is not None][0]
    normal = {"x": [1, 0, 0], "y": [0, 1, 0], "z": [0, 0, 1]}[axis]
    origin = [val if axis == "x" else 0, val if axis == "y" else 0, val if axis == "z" else 0]
    view = {"z": (0, 1, "X (mm)", "Y (mm)"), "y": (0, 2, "X (mm)", "Z (mm) — build direction"),
            "x": (1, 2, "Y (mm)", "Z (mm) — build direction")}[axis]
    mesh = trimesh.load(a.stl, force="mesh")
    sec = mesh.section(plane_origin=origin, plane_normal=normal)
    if sec is None:
        print(f"no material at {axis} = {val} mm (part spans {np.round(mesh.bounds, 1).tolist()})")
        return 1
    planar, to_3d = sec.to_2D()
    to_3d = np.asarray(to_3d)

    def proj(coords):
        c = np.asarray(coords)
        p3 = (to_3d @ np.column_stack([c, np.zeros(len(c)), np.ones(len(c))]).T).T[:, :3]
        return p3[:, [view[0], view[1]]]

    fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
    thin = None
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from check_stl import wall_thickness
    for poly in planar.polygons_full:
        if poly.area < 0.01:
            continue
        rings = [proj(poly.exterior.coords)] + [proj(r.coords) for r in poly.interiors]
        verts = np.vstack(rings)
        codes = np.concatenate([[Path.MOVETO] + [Path.LINETO] * (len(r) - 2) + [Path.CLOSEPOLY] for r in rings])
        ax.add_patch(PathPatch(Path(verts, codes), facecolor="#d9d9d9", edgecolor="black", linewidth=1.2))
        t, at, _ = wall_thickness(poly)
        if at is not None and (thin is None or t < thin[0]):
            thin = (t, proj([at])[0])
    ax.set_aspect("equal"); ax.autoscale_view(); ax.grid(True, linewidth=0.3)
    ax.set_xlabel(view[2]); ax.set_ylabel(view[3])
    if thin:
        colour = "red" if thin[0] < a.min_wall - 0.05 else "tab:blue"
        ax.plot(*thin[1], "o", color=colour, markersize=8)
        ax.annotate(f"thinnest wall {thin[0]:.2f} mm", thin[1], textcoords="offset points", xytext=(10, 10), color=colour)
    ax.set_title(a.title or f"{os.path.basename(a.stl)} — section at {axis.upper()} = {val:g} mm (cut faces grey)")
    out = a.out or os.path.splitext(a.stl)[0] + f"_section_{axis}{val:g}.png"
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    fig.savefig(out, bbox_inches="tight", metadata={"Software": None})
    print(f"section written to {out}" + (f" — thinnest wall {thin[0]:.2f} mm" if thin else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
