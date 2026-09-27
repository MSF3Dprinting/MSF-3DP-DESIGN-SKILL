#!/usr/bin/env python3
"""check_stl.py — universal printability checks for any STL (MSF "3D Printing for All").

Works on any part: it reads only the mesh, never the design. Checks (workflow §10.1):
  T4  watertight / winding / volume / body count          T5  bounding box vs --max-size
  T6  sits on Z = 0, bed-contact % of the footprint        T7  sloped overhangs (angle from vertical)
  T8  horizontal downward faces above the bed (bridges)    T19 sections: piece count + wall thickness
  plus a size budget (triangles, file size) and a slender-part warning (brim ears)

Usage
  python3 check_stl.py part.stl [more.stl ...] [options]
  python3 check_stl.py part.stl --sections 5,12.5,30 --min-wall 1.6
  python3 check_stl.py part.stl --allow-bridges --json report.json
  python3 check_stl.py plate.stl --expect-bodies 2                # an "all parts" print plate
  python3 check_stl.py assembly.stl --view-only --expect-bodies 2  # assembled view: not a print file

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
  --sections z,z,..   heights at which to slice and measure walls: numbers (mm), NN% of the height,
                      top-D (D mm below the top face), or "auto" = every 2.5 mm from 0.3 mm plus 0.3 mm
                      below the top (every height band that holds a feature, and the top face)
  --view-only         the STL is an assembled view, not a print file: only T4 (watertight, winding,
                      bodies) and T5 run; print position, overhangs and bridges are skipped
  --allow-bridges     documented bridges do not fail the check (they are still listed)
  --single-piece      a section with more than one piece is a failure (default: a warning, because
                      legs and separate walls legitimately give several pieces)
  --json FILE         also write the results as JSON
  --quiet             one summary line per file
Needs trimesh, numpy, scipy, shapely, rtree and networkx (sections). A section that cannot be computed is
a failure, never a silent pass. Exit code 1 when any check fails, so export.sh can stop.
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


def wall_thickness(poly, max_probe=20.0, spacing=0.5, skip=0.2):
    """Thickness of a section polygon measured along inward normals at boundary samples.

    Returns (min_thickness, (x, y), n_samples). Universal: no assumption about the shape.
    Each sample casts one ray along the inward normal (left-hand normal after shapely's orient():
    exterior CCW, holes CW) and measures the distance to the first boundary it meets — exact, and
    vectorised with shapely 2. A sample whose point `skip` mm inward is not inside the polygon sits on a
    corner artefact and is left to its neighbours.
    """
    import shapely
    from shapely.geometry.polygon import orient

    poly = orient(poly, sign=1.0)
    P, N = [], []
    for ring in [poly.exterior] + list(poly.interiors):
        length = ring.length
        if length <= 0:
            continue
        count = max(8, int(length / spacing))
        d = (np.arange(count) + 0.5) / count * length
        a = shapely.get_coordinates(shapely.line_interpolate_point(ring, d))
        b = shapely.get_coordinates(shapely.line_interpolate_point(ring, np.minimum(d + 0.05, length)))
        t = b - a
        norm = np.hypot(t[:, 0], t[:, 1])
        ok = norm > 0
        P.append(a[ok])
        N.append(np.stack([-t[ok, 1] / norm[ok], t[ok, 0] / norm[ok]], axis=1))
    if not P:
        return float("inf"), None, 0
    P, N = np.vstack(P), np.vstack(N)
    shapely.prepare(poly)
    keep = shapely.contains_xy(poly, P[:, 0] + N[:, 0] * skip, P[:, 1] + N[:, 1] * skip)
    P, N = P[keep], N[keep]
    if len(P) == 0:
        return float("inf"), None, 0
    rays = shapely.linestrings(np.stack([P + N * 0.01, P + N * max_probe], axis=1))
    hits = shapely.intersection(rays, poly.boundary)
    dist = shapely.distance(shapely.points(P), hits)
    dist = np.where(np.isnan(dist) | shapely.is_empty(hits), np.inf, dist)
    i = int(np.argmin(dist))
    if not np.isfinite(dist[i]):
        return float("inf"), None, len(P)
    return float(dist[i]), (round(float(P[i, 0]), 2), round(float(P[i, 1]), 2)), len(P)


def section_report(mesh, z, min_wall):
    """Slice at z: number of pieces, area, minimum wall thickness. Any problem is returned as "error"."""
    try:
        import networkx  # noqa: F401  (trimesh needs it to close section polygons)
    except ImportError:
        return {"z": z, "error": "sections need the Python package networkx: pip install networkx (scripts/install_openscad.sh installs it)"}
    try:
        sec = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    except Exception as e:  # pragma: no cover
        return {"z": z, "error": str(e)}
    if sec is None:
        return {"z": z, "pieces": 0, "area": 0.0, "min_wall": None, "note": "no material at this height"}
    try:
        planar, to_3d = sec.to_2D() if hasattr(sec, "to_2D") else sec.to_planar()
        polys = planar.polygons_full
    except Exception as e:  # pragma: no cover
        return {"z": z, "error": f"section could not be closed: {e}"}
    polys = [p for p in polys if p.area > 0.01]
    if not polys:
        return {"z": z, "pieces": 0, "area": 0.0, "min_wall": None, "note": "no material at this height"}
    worst = (float("inf"), None)
    for p in polys:
        t, at, _ = wall_thickness(p)
        if t < worst[0]:
            worst = (t, at)
    if worst[1] is not None:   # back from the section's planar frame to part coordinates
        x, y, _z, _w = np.asarray(to_3d) @ np.array([worst[1][0], worst[1][1], 0.0, 1.0])
        worst = (worst[0], (round(float(x), 2), round(float(y), 2)))
    mw = None if worst[1] is None else round(worst[0], 2)
    return {
        "z": z,
        "pieces": len(polys),
        "area": round(sum(p.area for p in polys), 2),
        "min_wall": mw,
        "min_wall_at": worst[1],
        "wall_ok": (mw is None) or (mw >= min_wall - 0.05),
    }


def section_heights(spec, height):
    """Parse --sections: numbers (mm), NN% of the height, top-D, or auto."""
    zs = []
    for tok in [t.strip() for t in spec.split(",") if t.strip()]:
        if tok == "auto":
            z = 0.3
            while z < height - 0.3:
                zs.append(round(z, 2)); z += 2.5
            zs.append(round(height - 0.3, 2))
        elif tok.endswith("%"):
            zs.append(round(height * float(tok[:-1]) / 100.0, 2))
        elif tok.startswith("top-"):
            zs.append(round(height - float(tok[4:]), 2))
        else:
            zs.append(float(tok))
    return sorted(set(z for z in zs if 0 < z < height))


# ----------------------------------------------------------------------------- main check
def check_file(path, limit=45.0, tol=0.05, min_area=0.5, sliver=0.001, bed_tol=0.05,
               max_size=200.0, expect_bodies=1, min_wall=1.6, sections=(), allow_bridges=False,
               single_piece=False, view_only=False, max_triangles=60000, max_mb=3.0):
    """sections: a list of heights (mm) or a --sections string (see section_heights)."""
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
    if r["watertight"] and not r["winding_consistent"]:
        r["fail"].append("inconsistent winding: some faces point inward (flipped faces — check polyhedron() point order, T4)")

    # size budget: big meshes make slow checks and heavy field packages
    import os
    r["file_mb"] = round(os.path.getsize(path) / 1e6, 2)
    if r["triangles"] > max_triangles or r["file_mb"] > max_mb:
        r["warn"].append(f"{r['triangles']} triangles / {r['file_mb']} MB — above the budget of {max_triangles} triangles / {max_mb} MB per part; lower $fn / slices")

    # T5
    if max(r["size"]) > max_size:
        r["fail"].append(f"size {r['size']} exceeds {max_size} mm on an axis — split the part")

    if view_only:   # an assembled view is for looking at, not for printing: no print-position checks
        r["view_only"] = True
        r["sections"] = []
        r["bridges"] = []
        r["worst_overhang_deg"] = None
        r["ok"] = not r["fail"]
        return r

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
    # slender part: height against the narrowest width of the bed contact (a thin tower tips or lifts)
    short_side = None
    try:
        from shapely.geometry import Polygon
        from shapely.ops import unary_union
        tris = [Polygon(t) for t in mesh.triangles[on_bed][:, :, :2] if Polygon(t).area > 1e-9]
        if tris:
            rect = unary_union(tris).minimum_rotated_rectangle
            xs, ys = rect.exterior.coords.xy
            sides = [math.hypot(xs[i + 1] - xs[i], ys[i + 1] - ys[i]) for i in range(2)]
            short_side = round(min(sides), 1)
    except Exception:
        pass
    r["bed_contact_min_width"] = short_side
    if (r["bed_contact_pct"] is not None and r["bed_contact_pct"] < 15 and ext[2] > 40) or \
       (short_side is not None and ext[2] > 20 and ext[2] > 3 * short_side):
        r["warn"].append(f"slender or small bed contact (height {r['size'][2]} mm on a contact {short_side} mm wide, "
                         f"{r['bed_contact_pct']} % of the footprint) — add brim ears (brim_ear_d) or widen the base")

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
                            "longest_span": round(float(max(span[0], span[1])), 1),
                            "facets": int(len(grp))})
    r["bridges"] = bridges
    if bridges:
        # the mesh does not say where a bridge is supported, so the longest XY extent is reported as its span
        longest = max(b["longest_span"] for b in bridges)
        msg = (f"{len(bridges)} horizontal downward face group(s) above the bed (bridges/ledges), longest span {longest} mm"
               + (" — over the 10 mm limit" if longest > 10 else ""))
        if allow_bridges:
            r["warn"].append(msg + " — accepted (--allow-bridges); document them in the README")
        else:
            r["fail"].append(msg + " — avoid, or document and re-run with --allow-bridges")

    # T19 — sections
    if isinstance(sections, str):
        sections = section_heights(sections, float(hi[2] - lo[2]))
    secs = []
    for z in sections:
        s = section_report(mesh, float(z), min_wall)
        secs.append(s)
        if "error" in s:
            r["fail"].append(f"section at Z = {z}: {s['error']}")
            continue
        if s.get("pieces") == 0:
            r["warn"].append(f"section at Z = {z}: no material at this height — check the section heights")
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
    if r.get("view_only"):
        print("  assembled view (--view-only): print position, overhang, bridge and section checks skipped")
        for w in r["warn"]:
            print("  WARN:", w)
        for f in r["fail"]:
            print("  FAIL:", f)
        print("  RESULT:", "PASS" if r["ok"] else "FAIL")
        return
    print(f"  bed contact {r['bed_contact_area']} mm² = {r['bed_contact_pct']} % of the convex footprint {r['footprint_area']} mm²")
    print(f"  worst sloped overhang {r['worst_overhang_deg']}° from vertical at {r.get('worst_overhang_at')}   "
          f"facets over limit {r['overhang_facets_over_limit']} ({r['overhang_area_over_limit']} mm²)")
    if r["bridges"]:
        for b in r["bridges"]:
            print(f"  horizontal downward face at Z {b['z']}: area {b['area']} mm², XY extent {b['xy_extent']} mm (span up to {b['longest_span']} mm), {b['facets']} facets")
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
    ap.add_argument("--view-only", action="store_true", help="assembled view: only watertightness, winding, bodies and size")
    ap.add_argument("--max-triangles", type=int, default=60000)
    ap.add_argument("--max-mb", type=float, default=3.0)
    ap.add_argument("--json", type=str, default="")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    sections = a.sections   # parsed per file: auto / % / top- depend on the part height
    results = []
    for path in a.stl:
        try:
            r = check_file(path, a.limit, a.tol, a.min_area, a.sliver, a.bed_tol, a.max_size,
                           a.expect_bodies, a.min_wall, sections, a.allow_bridges, a.single_piece,
                           a.view_only, a.max_triangles, a.max_mb)
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
