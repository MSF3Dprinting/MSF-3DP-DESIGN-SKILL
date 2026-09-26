#!/usr/bin/env python3
"""flatten_scad.py — one-file Customizer version of a part (MSF customizer standard).

The working file uses  include <common.scad>  and  include <helpers.scad>.  The catalogue and the
OpenSCAD Customizer want ONE file: header comments, then the adjustable values (literals, grouped),
then everything else hidden. This script produces that file from the working file and verifies that
both export the same geometry.

Layout of the output
  // @name: ...  // @description: ...  // @category: ...  // @credit: ...      (catalogue header)
  the working file's own header comment (design summary)
  the working file's Customizer parameters, groups kept, in their original order
  /* [Hidden] */
  facets = <n>;  and the values of every included library (group headers turned into plain comments)
  the working file's derived values, validation, modules and build
  the modules and functions of every included library

Rules the working file must follow (they are checked): parameters are literal values (no expressions,
no references to other variables — the Customizer cannot show those); the parameter block ends at the
line  // ===== Derived values =====  (or at the first module / function); includes are relative.

Usage
  python3 flatten_scad.py part.scad --out part_customizer.scad --name "Wall pocket" \
      --description "Open box screwed to a wall, holds one handheld device" --category "Hospital" --credit "MSF 3D Printing for All"
  python3 flatten_scad.py part.scad --out part_customizer.scad --verify        # renders both and compares
"""
import argparse
import os
import re
import subprocess
import sys
import time

INCLUDE_RE = re.compile(r'^\s*(include|use)\s*<([^>]+)>\s*;?\s*$')
ASSIGN_RE = re.compile(r'^\s*(\$?[A-Za-z_]\w*)\s*=\s*(.+?)\s*;\s*(//.*)?$')
GROUP_RE = re.compile(r'^\s*/\*\s*\[([^\]]*)\]\s*\*/\s*$')
DEF_RE = re.compile(r'^\s*(module|function)\s+[A-Za-z_]\w*')
LITERAL_RE = re.compile(r'^(-?\d+(\.\d+)?|true|false|"[^"]*"|\[[^\]]*\])$')


def read(path):
    return open(path, encoding='utf-8').read().splitlines()


def split_library(lines):
    """Split a library into (value lines, code lines). Group headers become comments; the leading
    assert() and blank runs are dropped from the value block; modules/functions/other statements go to code."""
    values, code, pending = [], [], []
    in_block = 0  # inside a module/function body (brace depth)
    for ln in lines:
        s = ln.strip()
        if in_block > 0:
            code.append(ln); in_block += ln.count('{') - ln.count('}'); continue
        if DEF_RE.match(ln):
            code.extend(pending); pending = []
            code.append(ln); in_block += ln.count('{') - ln.count('}')
            if in_block == 0 and s.endswith(';'):
                pass  # one-line function
            continue
        if GROUP_RE.match(ln):
            values.append(f"// -- {GROUP_RE.match(ln).group(1)} --"); continue
        if s.startswith('assert(') or s.startswith('echo('):
            continue  # top-level statements of the library are not needed in the flattened file
        if ASSIGN_RE.match(ln):
            values.extend(pending); pending = []; values.append(ln); continue
        if s.startswith('//') or s == '':
            pending.append(ln); continue
        code.append(ln)  # anything else (e.g. a top-level call) goes with the code
    return values, code


def flatten(main_path, name, description, category, credit, facets):
    base = os.path.dirname(os.path.abspath(main_path))
    lines = read(main_path)
    # 1. header comment block (before the first include / group / assignment)
    header, i = [], 0
    while i < len(lines) and not INCLUDE_RE.match(lines[i]) and not GROUP_RE.match(lines[i]) and not ASSIGN_RE.match(lines[i]):
        header.append(lines[i]); i += 1
    # 2. includes (in order) and the parameter block up to the derived-values marker
    includes, params, rest = [], [], []
    stage = 'params'
    for ln in lines[i:]:
        m = INCLUDE_RE.match(ln)
        if m and stage == 'params':
            includes.append(m.group(2)); continue
        if stage == 'params' and (ln.strip().startswith('// ===== Derived') or DEF_RE.match(ln)):
            stage = 'rest'
        (params if stage == 'params' else rest).append(ln)
    # strip old catalogue headers from the header block (they are re-emitted from the arguments)
    old = {}
    keep = []
    for ln in header:
        m = re.match(r'^\s*//\s*@(name|description|category|credit|author|source|hidden):\s*(.*)$', ln)
        if m:
            old[m.group(1)] = m.group(2).strip()
        else:
            keep.append(ln)
    name = name or old.get('name') or os.path.splitext(os.path.basename(main_path))[0].replace('_', ' ')
    description = description or old.get('description') or ''
    category = category or old.get('category') or 'General'
    credit = credit or old.get('credit') or old.get('author') or 'MSF 3D Printing for All'
    # 3. check the parameters are literals
    problems = []
    for ln in params:
        m = ASSIGN_RE.match(ln)
        if m and not m.group(1).startswith('$') and not LITERAL_RE.match(m.group(2).strip()):
            problems.append(f"{m.group(1)} = {m.group(2).strip()}  <- not a literal; the Customizer cannot show it")
    # 4. libraries
    lib_values, lib_code = [], []
    seen = set()
    for inc in includes:
        p = os.path.join(base, inc)
        if not os.path.exists(p) or inc in seen:
            continue
        seen.add(inc)
        v, c = split_library(read(p))
        lib_values += [f"// ---- from {inc} ----"] + v
        lib_code += [f"// ---- modules from {inc} ----"] + c
    out = [f"// @name: {name}", f"// @description: {description}", f"// @category: {category}", f"// @credit: {credit}",
           f"// One-file Customizer version generated by flatten_scad.py on {time.strftime('%Y-%m-%d')} from {os.path.basename(main_path)}",
           ""] + keep + params + ["", "/* [Hidden] */", f"facets = {facets};   // smoothness of curves (lower = faster)", "$fn = facets;", ""] \
          + lib_values + ["", "// ===== part (derived values, validation, modules, build) ====="] + rest + [""] + lib_code + [""]
    # the library's own $fn line would override facets: neutralise it
    out = [re.sub(r'^\s*\$fn\s*=\s*\$preview.*$', '// ($fn set by facets above)', l) for l in out]
    return "\n".join(out), problems


def export(openscad, scad, stl):
    cmd = [openscad, '-o', stl, '--export-format', 'binstl', scad]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return p.returncode == 0 and os.path.exists(stl) and os.path.getsize(stl) > 84, (p.stdout + p.stderr)[-400:]


def compare(a, b):
    import trimesh
    ma, mb = trimesh.load(a, force='mesh'), trimesh.load(b, force='mesh')
    va = ma.volume if ma.is_watertight else float('nan'); vb = mb.volume if mb.is_watertight else float('nan')
    ea, eb = ma.extents, mb.extents
    same = abs(va - vb) < max(0.5, 0.002 * abs(va)) and max(abs(ea - eb)) < 0.01
    return same, f"volume {va:.1f} vs {vb:.1f} mm3, size {ea.round(2)} vs {eb.round(2)}, triangles {len(ma.faces)} vs {len(mb.faces)}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('scad')
    ap.add_argument('--out', help='default: <name>_customizer.scad next to the input')
    ap.add_argument('--name'); ap.add_argument('--description'); ap.add_argument('--category'); ap.add_argument('--credit')
    ap.add_argument('--facets', type=int, default=96)
    ap.add_argument('--verify', action='store_true', help='export both files and compare the geometry')
    ap.add_argument('--openscad', default=None)
    a = ap.parse_args(argv)
    out = a.out or os.path.splitext(a.scad)[0] + '_customizer.scad'
    text, problems = flatten(a.scad, a.name, a.description, a.category, a.credit, a.facets)
    open(out, 'w', encoding='utf-8').write(text)
    print(f"written {out} ({text.count(chr(10))} lines)")
    for p in problems:
        print("WARN parameter", p)
    if a.verify:
        here = os.path.dirname(os.path.abspath(__file__))
        osc = a.openscad or (os.path.join(here, 'openscad-fast') if os.path.exists(os.path.join(here, 'openscad-fast')) else 'openscad')
        ok1, m1 = export(osc, a.scad, '/tmp/_flat_a.stl'); ok2, m2 = export(osc, out, '/tmp/_flat_b.stl')
        if not (ok1 and ok2):
            print("FAIL render:", m1 if not ok1 else m2); return 1
        same, msg = compare('/tmp/_flat_a.stl', '/tmp/_flat_b.stl')
        print(("PASS identical geometry — " if same else "FAIL geometry differs — ") + msg)
        return 0 if same else 1
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
