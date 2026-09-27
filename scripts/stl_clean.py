#!/usr/bin/env python3
"""stl_clean.py — drop zero-area specks from an exported STL (MSF "3D Printing for All").

Mesh booleans sometimes leave detached "bodies" of two degenerate faces and ~0 mm² next to a sound part
(tangent or coincident faces). They are not geometry, but they fail the body count and the watertight test.
This script removes detached bodies whose surface is below --min-area (default 0.01 mm²) and rewrites the
file only when it removed something. It never touches a body you could see or print. export.sh and
sweep.py run it on every STL before the checks and log what it removed; fix the model when it removes
anything at the default parameters (boolean hygiene, references/openscad-environment.md §6.2).

Usage
  python3 stl_clean.py part.stl [more.stl ...] [--min-area 0.01] [--quiet]
Exit code 0, or 1 when a file cannot be read or would be left empty.
"""
import argparse
import sys

sys.dont_write_bytecode = True


def clean(path, min_area=0.01):
    """Remove specks in place. Returns (removed_count, removed_area)."""
    import trimesh
    mesh = trimesh.load(path, force="mesh")
    parts = mesh.split(only_watertight=False)
    if len(parts) <= 1:
        return 0, 0.0
    keep = [p for p in parts if p.area >= min_area]
    drop = [p for p in parts if p.area < min_area]
    if not drop:
        return 0, 0.0
    if not keep:
        raise ValueError("every body is below the speck limit — nothing would be left")
    trimesh.util.concatenate(keep).export(path, file_type="stl")
    return len(drop), float(sum(p.area for p in drop))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stl", nargs="+")
    ap.add_argument("--min-area", type=float, default=0.01)
    ap.add_argument("--quiet", action="store_true", help="print only when something was removed")
    a = ap.parse_args(argv)
    rc = 0
    for path in a.stl:
        try:
            n, area = clean(path, a.min_area)
        except Exception as e:
            print(f"FAIL clean {path}: {e}"); rc = 1; continue
        if n:
            print(f"cleaned {path}: removed {n} speck(s), {area:.4f} mm² in total")
        elif not a.quiet:
            print(f"clean   {path}: nothing to remove")
    return rc


if __name__ == "__main__":
    sys.exit(main())
