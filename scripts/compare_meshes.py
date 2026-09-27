#!/usr/bin/env python3
"""compare_meshes.py — are two exports the same mesh? (MSF "3D Printing for All")

A change that only touches documentation, Customizer widgets or comments must not change a single triangle.
When every exported STL is identical to the verified version, the earlier sweep and checks carry over
(references/verification.md) — no need to run them again. Triangles are compared after sorting (vertex
order and face order do not matter), with a tolerance of 1e-4 mm.

Usage
  python3 compare_meshes.py old.stl new.stl
  python3 compare_meshes.py old_stl/ new_stl/        # every .stl present in both folders
Exit code 0 when all pairs are identical, 1 otherwise.
"""
import argparse
import os
import sys

import numpy as np


def canonical(path):
    import trimesh
    m = trimesh.load(path, force="mesh", process=False)
    tris = np.round(m.triangles.astype(np.float64), 4)                 # (n, 3, 3)
    # sort the three vertices inside each triangle, then the triangles
    tris = np.array([t[np.lexsort(t.T[::-1])] for t in tris])
    flat = tris.reshape(len(tris), -1)
    flat = flat[np.lexsort(flat.T[::-1])]
    return m, flat


def compare(a, b):
    ma, fa = canonical(a)
    mb, fb = canonical(b)
    if fa.shape == fb.shape and np.allclose(fa, fb, atol=1e-4):
        return True, f"identical ({len(fa)} triangles)"
    import trimesh
    pa, pb = trimesh.load(a, force="mesh"), trimesh.load(b, force="mesh")   # merged vertices, for the volume
    va = pa.volume if pa.is_watertight else float("nan")
    vb = pb.volume if pb.is_watertight else float("nan")
    return False, (f"different: triangles {len(fa)} vs {len(fb)}, volume {va:.2f} vs {vb:.2f} mm³, "
                   f"size {np.round(ma.extents, 2)} vs {np.round(mb.extents, 2)}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("a"); ap.add_argument("b")
    x = ap.parse_args(argv)
    if os.path.isdir(x.a) and os.path.isdir(x.b):
        names = sorted(set(f for f in os.listdir(x.a) if f.lower().endswith(".stl")) & set(os.listdir(x.b)))
        only = sorted(set(f for f in os.listdir(x.a) + os.listdir(x.b) if f.lower().endswith(".stl")) - set(names))
        pairs = [(os.path.join(x.a, n), os.path.join(x.b, n)) for n in names]
    else:
        pairs, only = [(x.a, x.b)], []
    ok = True
    for pa, pb in pairs:
        same, msg = compare(pa, pb)
        ok &= same
        print(("SAME  " if same else "DIFF  ") + os.path.basename(pb) + "  " + msg)
    for n in only:
        ok = False
        print(f"ONLY  {n} is in one folder only")
    print("RESULT:", "all identical — earlier checks carry over" if ok else "meshes changed — run the checks again")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
