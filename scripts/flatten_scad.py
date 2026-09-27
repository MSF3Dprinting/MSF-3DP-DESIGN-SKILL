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
import shutil
import subprocess
import sys
import tempfile
import time

INCLUDE_RE = re.compile(r'^\s*(include|use)\s*<([^>]+)>\s*;?\s*$')
ASSIGN_RE = re.compile(r'^\s*(\$?[A-Za-z_]\w*)\s*=\s*(.+?)\s*;\s*(//.*)?$')
GROUP_RE = re.compile(r'^\s*/\*\s*\[([^\]]*)\]\s*\*/\s*$')
DEF_RE = re.compile(r'^\s*(module|function)\s+[A-Za-z_]\w*')
NUM_RE = re.compile(r'^-?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$')
DERIVED_RE = re.compile(r'^\s*//\s*=+\s*derived', re.I)
FN_EXPORT_RE = re.compile(r'^\s*fn_export\s*=\s*(\d+)\s*;', re.M)


def is_literal(v):
    """A value the Customizer can show: a number, true/false, a quoted string, or a vector of literals."""
    v = v.strip()
    if NUM_RE.match(v) or v in ("true", "false") or re.fullmatch(r'"[^"]*"', v):
        return True
    if v.startswith("[") and v.endswith("]"):
        items, depth, cur, quoted = [], 0, "", False
        for ch in v[1:-1]:
            if ch == '"':
                quoted = not quoted
            if not quoted and ch in "[":
                depth += 1
            if not quoted and ch in "]":
                depth -= 1
            if ch == "," and depth == 0 and not quoted:
                items.append(cur); cur = ""
            else:
                cur += ch
        if cur.strip():
            items.append(cur)
        return all(is_literal(i) for i in items)
    return False


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
            values.extend(pending); pending = []   # keep the comments that precede a group header in front of it
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
            includes.append((m.group(1), m.group(2))); continue
        if stage == 'params' and (DERIVED_RE.match(ln) or DEF_RE.match(ln)):
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
        if m and not m.group(1).startswith('$') and not is_literal(m.group(2)):
            problems.append(f"{m.group(1)} = {m.group(2).strip()}  <- not a literal; the Customizer cannot show it")
    # 4. libraries
    lib_values, lib_code = [], []
    seen = set()
    for kind, inc in includes:
        p = os.path.join(base, inc)
        if not os.path.exists(p):
            problems.append(f"{kind} <{inc}> not found next to the file")
            continue
        if inc in seen:
            continue
        seen.add(inc)
        v, c = split_library(read(p))
        if kind == 'include':   # include brings values and modules; use brings modules and functions only
            lib_values += [f"// ---- from {inc} ----"] + v
        lib_code += [f"// ---- modules from {inc} ({kind}) ----"] + c
    out = [f"// @name: {name}", f"// @description: {description}", f"// @category: {category}", f"// @credit: {credit}",
           f"// One-file Customizer version generated by flatten_scad.py on {time.strftime('%Y-%m-%d')} from {os.path.basename(main_path)}",
           ""] + keep + params + ["", "/* [Hidden] */", f"facets = {facets};   // smoothness of curves (lower = faster)", "$fn = facets;", ""] \
          + lib_values + ["", "// ===== part (derived values, validation, modules, build) ====="] + rest + [""] + lib_code + [""]
    # the library's own $fn line would override facets: neutralise it
    out = [re.sub(r'^\s*\$fn\s*=\s*\$preview.*$', '// ($fn set by facets above)', l) for l in out]
    return "\n".join(out), problems


def export(openscad, scad, stl):
    cmd = [openscad, '-o', stl, '--export-format', 'binstl', scad]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except FileNotFoundError:
        return False, f"OpenSCAD binary not found: {openscad}"
    except subprocess.TimeoutExpired:
        return False, "timeout after 600 s"
    return p.returncode == 0 and os.path.exists(stl) and os.path.getsize(stl) > 84, (p.stdout + p.stderr)[-400:]


def default_facets(main_path):
    """The flat file's facets equal the working file's export resolution (fn_export), so both give one mesh."""
    base = os.path.dirname(os.path.abspath(main_path))
    texts = [open(main_path, encoding='utf-8').read()]
    for ln in read(main_path):
        m = INCLUDE_RE.match(ln)
        if m and os.path.exists(os.path.join(base, m.group(2))):
            texts.append(open(os.path.join(base, m.group(2)), encoding='utf-8').read())
    for t in texts:
        m = FN_EXPORT_RE.search(t)
        if m:
            return int(m.group(1))
    return 96


def pick_openscad(explicit):
    """openscad-fast when it actually runs, else the native binary."""
    if explicit:
        return explicit
    fast = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openscad-fast')
    if os.path.exists(fast):
        try:
            if subprocess.run(['bash', fast, '--version'], capture_output=True, timeout=60).returncode == 0:
                os.chmod(fast, 0o755)
                return fast
        except Exception:
            pass
    return shutil.which('openscad') or 'openscad'


def compare(a, b):
    import trimesh
    ma, mb = trimesh.load(a, force='mesh'), trimesh.load(b, force='mesh')
    va = ma.volume if ma.is_watertight else float('nan'); vb = mb.volume if mb.is_watertight else float('nan')
    ea, eb = ma.extents, mb.extents
    same = abs(va - vb) < max(0.5, 0.002 * abs(va)) and max(abs(ea - eb)) < 0.01 and len(ma.faces) == len(mb.faces)
    return same, f"volume {va:.1f} vs {vb:.1f} mm3, size {ea.round(2)} vs {eb.round(2)}, triangles {len(ma.faces)} vs {len(mb.faces)}" + \
        ("" if len(ma.faces) == len(mb.faces) else " — the resolution differs: set --facets to the working file's fn_export")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('scad')
    ap.add_argument('--out', help='default: <name>_customizer.scad next to the input')
    ap.add_argument('--name'); ap.add_argument('--description'); ap.add_argument('--category'); ap.add_argument('--credit')
    ap.add_argument('--facets', type=int, default=None, help="default: the working file's fn_export (96 in common.scad)")
    ap.add_argument('--verify', action='store_true', help='export both files and compare the geometry')
    ap.add_argument('--openscad', default=None)
    a = ap.parse_args(argv)
    out = a.out or os.path.splitext(a.scad)[0] + '_customizer.scad'
    facets = a.facets or default_facets(a.scad)
    text, problems = flatten(a.scad, a.name, a.description, a.category, a.credit, facets)
    open(out, 'w', encoding='utf-8').write(text)
    print(f"written {out} ({text.count(chr(10))} lines)")
    for p in problems:
        print("FAIL", p)
    if a.verify:
        osc = pick_openscad(a.openscad)
        tmp = tempfile.mkdtemp(prefix='flatten_')
        try:
            sa, sb = os.path.join(tmp, 'working.stl'), os.path.join(tmp, 'flat.stl')
            ok1, m1 = export(osc, a.scad, sa); ok2, m2 = export(osc, out, sb)
            if not (ok1 and ok2):
                print(f"FAIL render ({os.path.basename(osc)}):", m1 if not ok1 else m2); return 1
            same, msg = compare(sa, sb)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        print(("PASS identical geometry — " if same else "FAIL geometry differs — ") + msg + f"  ({os.path.basename(osc)})")
        return 0 if (same and not problems) else 1
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
