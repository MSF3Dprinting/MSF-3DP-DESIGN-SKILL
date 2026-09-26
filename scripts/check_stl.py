#!/usr/bin/env python3
"""check_stl.py — universal printability checks for any STL (MSF "3D Printing for All").

Works on any part: it reads only the mesh, never the design. Checks (workflow §10.1):
  T4  watertight / winding / volume / body count          T5  bounding box vs --max-size
  T6  sits on Z = 0, bed-contact % of the footprint        T7  sloped overhangs (angle from vertical)
  T8  horizontal downward faces above the bed (bridges)    T19 sections: piece count + wall thickness

Usage
  python3 check_stl.py part.stl [more.stl ...] [options]
  python3 check_stl.py part.stl --sections 5,12.5,30 --min-wall 1.6
  python3 check_stl.py part.stl --allow-bridges --json report.json

Options
  --limit 45          overhang limit, degrees from vertical (60 only where the brief allows it)
  --tol 0.05          angle tolerance (float32 STL rounding puts exact 45° faces at 45.02°)
  --min-area 0.5      ignore facets smaller than this (mm²) in the overhang report; run a second pass
                      with --min-area 0.02 to catch small ledges and thin sheets
  --sliver 0.001      facets below this area are CGAL slivers and always ignored
  --bed-tol 0.05      a vertex within this height of the lowest point counts as on the bed
  --max-size 200      maximum size per axis (mm)
  --expect-bodies 1   number of separate bodies the STL should contain
  --min-wall 1.6      wall thickness the sections must reach (mm)
  --sections z,z,..   heights (mm) at which to slice and measure walls
  --allow-bridges     documented bridges do not fail the check (they are still listed)
  --single-piece      a section with more than one piece is a failure (default: a warning, because
                      legs and separate walls legitimately give several pieces)
  --json FILE         also write the results as JSON
  --quiet             one summary line per file
Exit code 1 when any check fails, so export.sh can stop.
"""
import argparse
import json
import math
import sys

import numpy as np

try:
    import trimesh
except ImportError:  # pragma: no cover
    sys.exit("check_stl.py needs trimesh:  pip install trimesh numpy scipy shapely rtree --break-system-packages")


# ----------------------------------------------------------------------------- helpers
def footprint_area(points_xy):
    """Area of the convex hull of the XY points (the part's footprint)."""
    try:
        from scipy.spatial import ConvexHull
        pts = np.unique(np.round(points_xy, 4), axis=0)
        if len(pts) < 3:
            return 0.0
        return float(ConvexHull(pts).volume)  # in 2D, .volume is the area
    except Exception:
        return 0.0


def wall_thickness(poly, step=0.1, max_probe=20.0, spacing=0.5):
    """Thickness of a section polygon measured along inward normals at boundary samples.

    Returns (min_thickness, (x, y), n_samples). Universal: no assumption about the shape.
    The inward normal is the left-hand normal after shapely's orient(): exterior CCW, holes CW.
    """
    from shapely.geometry import Point
    from shapely.geometry.polygon import orient
    from shapely.prepared import prep

    poly = orient(poly, sign=1.0)
    inside = prep(poly)
    rings = [poly.exterior] + list(poly.interiors)
    best = (float("inf"), None)
    n = 0
    for ring in rings:
        length = ring.length
        if length <= 0:
            continue
        count = max(8, int(length / spacing))
        for i in range(count):
            d = (i + 0.5) / count * length
            p = ring.interpolate(d)
            q = ring.interpolate(min(d + 0.05, length))
            tx, ty = q.x - p.x, q.y - p.y
            norm = math.hypot(tx, ty)
            if norm == 0:
                continue
            nx, ny = -ty / norm, tx / norm  # left-hand normal = inward after orient()
            # march inward until the probe leaves the polygon
            t = 0.2
            if not inside.contains(Point(p.x + nx * t, p.y + ny * t)):
                continue  # a corner artefact; the neighbouring samples measure this wall
            while t < max_probe:
                t2 = t + step
                if not inside.contains(Point(p.x + nx * t2, p.y + ny * t2)):
                    break
                t = t2
            n += 1
            if t < best[0]:
                best = (t, (round(p.x, 2), round(p.y, 2)))
    thickness = best[0] + step / 2 if best[1] is not None else float("inf")
    return thickness, best[1], n


def section_report(mesh, z, min_wall):
    """Slice at z: number of pieces, area, minimum wall thickness."""
    try:
        sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    except Exception as e:  # pragma: no cover
        return {"z": z, "error": str(e)}
    if sec is None:
        return {"z": z, "pieces": 0, "area": 0.0, "min_wall": None, "note": "no material at this height"}
    try:
        planar, _ = sec.to_2D() if hasattr(sec, "to_2D") else sec.to_planar()
        polys = planar.polygons_full
    except Exception as e:  # pragma: no cover
        return {"z": z, "error": f"section could not be closed: {e}"}
    polys = [p for p in polys if p.area > 0.01]
    worst = (float("inf"), None)
    for p in polys:
        t, at, _ = wall_thickness(p)
        if t < worst[0]:
            worst = (t, at)
    mw = None if worst[1] is None else round(worst[0], 2)
    return {
        "z": z,
        "pieces": len(polys),
        "area": round(sum(p.area for p in polys), 2),
        "min_wall": mw,
        "min_wall_at": worst[1],
        "wall_ok": (mw is None) or (mw >= min_wall - 0.05),
    }


# ----------------------------------------------------------------------------- main check
def check_file(path, limit=45.0, tol=0.05, min_area=0.5, sliver=0.001, bed_tol=0.05,
               max_size=200.0, expect_bodies=1, min_wall=1.6, sections=(), allow_bridges=False,
               single_piece=False):
    r = {"file": path, "fail": [], "warn": []}
    mesh = trimesh.load(path, force="mesh")
    if mesh.is_empty or len(mesh.faces) == 0:
        r["fail"].append("empty mesh")
        return r

    r["triangles"] = int(len(mesh.faces))
    lo, hi = mesh.bounds
    ext = hi - lo
    r["size"] = [round(float(v), 2) for v in ext]
    r["min_z"] = round(float(lo[2]), 3)
    r["watertight"] = bool(mesh.is_watertight)
    r["winding_consistent"] = bool(mesh.is_winding_consistent)
    r["volume"] = round(float(mesh.volume), 2) if mesh.is_watertight else None
    try:
        r["bodies"] = int(len(mesh.split(only_watertight=False)))
    except Exception:
        r["bodies"] = None

    # T4
    if not r["watertight"]:
        r["fail"].append("not watertight (open edges or duplicated faces — check boolean hygiene, T4)")
    if r["bodies"] is not None and r["bodies"] != expect_bodies:
        r["fail"].append(f"{r['bodies']} bodies, expected {expect_bodies} (stray specks or a detached feature)")
    if r["volume"] is not None and r["volume"] <= 0:
        r["fail"].append("volume is not positive (inverted faces)")

    # T5
    if max(r["size"]) > max_size:
        r["fail"].append(f"size {r['size']} exceeds {max_size} mm on an axis — split the part")

    # T6 — print position and bed contact
    if abs(r["min_z"]) > 0.01:
        r["fail"].append(f"lowest point at Z = {r['min_z']} mm, not on the bed (export in print position on Z = 0)")
    normals = mesh.face_normals
    areas = mesh.area_faces
    vz = mesh.vertices[:, 2]
    face_min_z = vz[mesh.faces].min(axis=1)
    face_max_z = vz[mesh.faces].max(axis=1)
    on_bed = (face_max_z <= lo[2] + bed_tol) & (normals[:, 2] < -0.99)
    contact = float(areas[on_bed].sum())
    foot = footprint_area(mesh.vertices[:, :2])
    r["bed_contact_area"] = round(contact, 1)
    r["footprint_area"] = round(foot, 1)
    r["bed_contact_pct"] = round(100.0 * contact / foot, 1) if foot > 0 else None
    if r["bed_contact_pct"] is not None and r["bed_contact_pct"] < 15 and ext[2] > 40:
        r["warn"].append("small bed contact for a tall part — add brim ears (brim_ear_d) or widen the base")

    # T7 / T8 — downward-facing facets above the bed
    down = (normals[:, 2] < -1e-6) & ~on_bed & (areas >= sliver)
    angle = np.degrees(np.arcsin(np.clip(-normals[:, 2], 0, 1)))  # angle of the face from vertical
    sloped = down & (angle < 89.9)
    horizontal = down & (angle >= 89.9)
    sig = sloped & (areas >= min_area)
    if sig.any():
        i = int(np.argmax(np.where(sig, angle, -1)))
        worst = float(angle[i])
        c = mesh.triangles_center[i]
        r["worst_overhang_deg"] = round(worst, 2)
        r["worst_overhang_at"] = [round(float(v), 1) for v in c]
        over = sig & (angle > limit + tol)
        r["overhang_facets_over_limit"] = int(over.sum())
        r["overhang_area_over_limit"] = round(float(areas[over].sum()), 2)
        if over.any():
            r["fail"].append(f"sloped overhang {worst:.1f}° from vertical at {r['worst_overhang_at']} (limit {limit}°), "
                             f"{int(over.sum())} facets / {r['overhang_area_over_limit']} mm²")
    else:
        r["worst_overhang_deg"] = 0.0
        r["overhang_facets_over_limit"] = 0
        r["overhang_area_over_limit"] = 0.0

    bridges = []
    if horizontal.any():
        idx = np.where(horizontal)[0]
        zs = np.round(face_min_z[idx] / 0.05) * 0.05
        for z in np.unique(zs):
            grp = idx[zs == z]
            a = float(areas[grp].sum())
            if a < min_area:
                continue
            pts = mesh.vertices[mesh.faces[grp]].reshape(-1, 3)
            span = pts.max(axis=0) - pts.min(axis=0)
            bridges.append({"z": round(float(z), 2), "area": round(a, 2),
                            "xy_extent": [round(float(span[0]), 1), round(float(span[1]), 1)],
                            "facets": int(len(grp))})
    r["bridges"] = bridges
    if bridges:
        widest = max(min(b["xy_extent"]) for b in bridges)
        msg = f"{len(bridges)} horizontal downward face group(s) above the bed (bridges/ledges), widest short span {widest} mm"
        if allow_bridges:
            r["warn"].append(msg + " — accepted (--allow-bridges); document them in the README")
        else:
            r["fail"].append(msg + " — avoid, or document and re-run with --allow-bridges")

    # T19 — sections
    secs = []
    for z in sections:
        s = section_report(mesh, float(z), min_wall)
        secs.append(s)
        if s.get("pieces", 1) > 1:
            msg = f"section at Z = {z}: {s['pieces']} separate pieces — expected if the part has several legs or walls here, a defect if the zone should be one piece"
            (r["fail"] if single_piece else r["warn"]).append(msg)
        if s.get("min_wall") is not None and not s.get("wall_ok", True):
            r["fail"].append(f"section at Z = {z}: wall {s['min_wall']} mm at {s['min_wall_at']} is below {min_wall} mm")
    r["sections"] = secs
    r["ok"] = not r["fail"]
    return r


def print_report(r, quiet=False):
    name = r["file"]
    if quiet:
        status = "PASS" if r.get("ok") else "FAIL"
        extra = "" if r.get("ok") else " — " + "; ".join(r["fail"])
        print(f"{status}  {name}{extra}")
        return
    print(f"=== {name}")
    if "triangles" not in r:
        print("  FAIL:", "; ".join(r["fail"]))
        return
    print(f"  triangles {r['triangles']}   size X/Y/Z {r['size']} mm   min Z {r['min_z']}")
    print(f"  watertight {r['watertight']}   winding {r['winding_consistent']}   bodies {r['bodies']}   volume {r['volume']} mm³")
    print(f"  bed contact {r['bed_contact_area']} mm² = {r['bed_contact_pct']} % of footprint {r['footprint_area']} mm²")
    print(f"  worst sloped overhang {r['worst_overhang_deg']}° from vertical at {r.get('worst_overhang_at')}   "
          f"facets over limit {r['overhang_facets_over_limit']} ({r['overhang_area_over_limit']} mm²)")
    if r["bridges"]:
        for b in r["bridges"]:
            print(f"  horizontal downward face at Z {b['z']}: area {b['area']} mm², XY extent {b['xy_extent']} mm, {b['facets']} facets")
    else:
        print("  horizontal downward faces above the bed: none")
    for s in r["sections"]:
        if "error" in s:
            print(f"  section Z {s['z']}: {s['error']}")
        elif s["pieces"] == 0:
            print(f"  section Z {s['z']}: no material")
        else:
            print(f"  section Z {s['z']}: {s['pieces']} piece(s), area {s['area']} mm², min wall {s['min_wall']} mm at {s['min_wall_at']}")
    for w in r["warn"]:
        print("  WARN:", w)
    for f in r["fail"]:
        print("  FAIL:", f)
    print("  RESULT:", "PASS" if r["ok"] else "FAIL")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stl", nargs="+")
    ap.add_argument("--limit", type=float, default=45.0)
    ap.add_argument("--tol", type=float, default=0.05)
    ap.add_argument("--min-area", type=float, default=0.5)
    ap.add_argument("--sliver", type=float, default=0.001)
    ap.add_argument("--bed-tol", type=float, default=0.05)
    ap.add_argument("--max-size", type=float, default=200.0)
    ap.add_argument("--expect-bodies", type=int, default=1)
    ap.add_argument("--min-wall", type=float, default=1.6)
    ap.add_argument("--sections", type=str, default="")
    ap.add_argument("--allow-bridges", action="store_true")
    ap.add_argument("--single-piece", action="store_true", help="fail when a section has more than one piece")
    ap.add_argument("--json", type=str, default="")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    sections = [float(z) for z in a.sections.split(",") if z.strip()] if a.sections else []
    results = []
    for path in a.stl:
        try:
            r = check_file(path, a.limit, a.tol, a.min_area, a.sliver, a.bed_tol, a.max_size,
                           a.expect_bodies, a.min_wall, sections, a.allow_bridges, a.single_piece)
        except Exception as e:
            r = {"file": path, "fail": [f"could not check: {e}"], "warn": [], "ok": False}
        results.append(r)
        print_report(r, a.quiet)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(results, f, indent=2)
    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
