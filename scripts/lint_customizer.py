#!/usr/bin/env python3
"""lint_customizer.py — check a .scad file against the MSF Customizer rules (MSF "3D Printing for All").

Two modes, chosen by the file:
  Customizer file (name ends in _customizer.scad, or --customizer): the one-file version that goes to the
    OpenSCAD Customizer and the MSF customizer catalogue.
  Working file (anything else, or --working): the file the designer edits (includes common.scad, helpers.scad).

Checks (T25)
  header     Customizer file: the first five lines are exactly
               // @name: ...  // @description: ...  // @category: ...  // @credit: ...  // @license: ...
             in this order, with a value, nothing else; no other @ line anywhere. Working file: no @ lines at
             all — the header belongs only in the Customizer file.
  one file   Customizer file: no include <> / use <>; a /* [Hidden] */ group with `facets`.
  help text  every parameter has its help text on the line above (the Customizer shows it as the label);
             after the value only the widget spec, e.g.  wall_t = 2.7; // [1.8:0.45:4.5]  — text after the spec
             turns a slider or menu into a plain box.
  numbers    every number is a slider  // [min:max]  or  // [min:step:max],  or a menu of values  // [3:M3, 6:M6].
  choices    a text parameter the model compares with fixed words (part == "wing") must be a menu
             // [body:Body, wing:Wing, flap:Flap]  — the user clicks, never types a fixed value.
             Free text (the text on a keychain, a label) stays a text box.
  vectors    no vector parameters (the Customizer shows spin boxes): one slider per value, the vector is built
             in the derived values.
  parts      a `part` menu with two or more components also offers  all  (all parts on one print plate) and
             assembly  (the assembled view).
The widgets are read from OpenSCAD's own parameter export (openscad-fast --export-format param), so the
check sees exactly what the Customizer shows.

Usage
  python3 lint_customizer.py part_customizer.scad        # Customizer file (exit 1 on any FAIL)
  python3 lint_customizer.py part.scad                    # working file
  python3 lint_customizer.py part.scad --fix              # move help text written after a spec to the line above
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HEADER_KEYS = ["name", "description", "category", "credit", "license"]
HEADER_LINE = re.compile(r'^// @(name|description|category|credit|license): (\S.*\S|\S)$')
ANY_AT = re.compile(r'^\s*//\s*@[A-Za-z]+\s*:')
INCLUDE = re.compile(r'^\s*(include|use)\s*<')
GROUP = re.compile(r'^\s*/\*\s*\[([^\]]*)\]\s*\*/\s*$')
END = re.compile(r'^\s*(//\s*=+\s*derived|module\s|function\s)', re.I)
ASSIGN = re.compile(r'^(\s*)([A-Za-z_]\w*)\s*=\s*([^;]+?)\s*;\s*(?://\s*(.*))?$')
SPEC_THEN_TEXT = re.compile(r'^(\[[^\]]*\])\s*(\S.*)$')


def pick_openscad(explicit):
    if explicit:
        return explicit
    fast = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openscad-fast")
    if os.path.exists(fast):
        try:
            if subprocess.run(["bash", fast, "--version"], capture_output=True, timeout=60).returncode == 0:
                return fast
        except Exception:
            pass
    return None   # the native 2021.01 build has no parameter export


def param_export(openscad, scad):
    tmp = tempfile.mkdtemp(prefix="lint_")
    out = os.path.join(tmp, "p.param")
    try:
        p = subprocess.run(["bash", openscad, "-o", out, "--export-format", "param", scad] if openscad.endswith("openscad-fast")
                           else [openscad, "-o", out, "--export-format", "param", scad], capture_output=True, text=True, timeout=300)
        if p.returncode != 0 or not os.path.exists(out):
            return None, (p.stdout + p.stderr)[-400:]
        return json.load(open(out)), ""
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def param_lines(lines):
    """{name: (index, spec, trailing text)} of the Customizer block (Hidden excluded)."""
    res, group = {}, ""
    for i, ln in enumerate(lines):
        if END.match(ln):
            break
        g = GROUP.match(ln)
        if g:
            group = g.group(1).strip()
            continue
        m = ASSIGN.match(ln)
        if not m or group.lower() == "hidden" or m.group(2) in res:
            continue
        comment = (m.group(4) or "").strip()
        st = SPEC_THEN_TEXT.match(comment)
        spec, text = (st.group(1), st.group(2)) if st else ((comment, "") if comment.startswith("[") else ("", comment))
        res[m.group(2)] = (i, spec, text)
    return res


def compared_words(src, name):
    words = set(re.findall(rf'\b{name}\s*[!=]=\s*"([^"]*)"', src)) | set(re.findall(rf'"([^"]*)"\s*[!=]=\s*{name}\b', src))
    return sorted(words)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scad")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--customizer", action="store_true", help="treat the file as the one-file Customizer version")
    mode.add_argument("--working", action="store_true", help="treat the file as a working file")
    ap.add_argument("--fix", action="store_true", help="move help text written after a widget spec to the line above")
    ap.add_argument("--openscad", default=None)
    a = ap.parse_args(argv)
    customizer = a.customizer or (not a.working and a.scad.endswith("_customizer.scad"))
    lines = open(a.scad, encoding="utf-8").read().splitlines()
    src = "\n".join(lines)
    fails, notes = [], []

    # header
    if customizer:
        for k, key in enumerate(HEADER_KEYS):
            ln = lines[k] if k < len(lines) else ""
            m = HEADER_LINE.match(ln)
            if not m or m.group(1) != key:
                fails.append(f"header line {k + 1} must be  // @{key}: <value>  — found: {ln!r}")
        for k, ln in enumerate(lines[5:], start=6):
            if ANY_AT.match(ln):
                fails.append(f"line {k}: an extra @ line — the header is exactly five lines, no variations: {ln.strip()!r}")
        for k, ln in enumerate(lines, start=1):
            if INCLUDE.match(ln):
                fails.append(f"line {k}: {ln.strip()} — the Customizer file must be one file (flatten_scad.py)")
        if not re.search(r'/\*\s*\[Hidden\]\s*\*/', src) or not re.search(r'^\s*facets\s*=', src, re.M):
            fails.append("no /* [Hidden] */ group with `facets` — regenerate the file with flatten_scad.py")
    else:
        for k, ln in enumerate(lines, start=1):
            if ANY_AT.match(ln):
                fails.append(f"line {k}: {ln.strip()!r} — the @ header belongs only in the Customizer file (flatten_scad.py writes it)")

    # help text above, spec alone after the value
    plines = param_lines(lines)
    fixes = []
    for name, (i, spec, text) in plines.items():
        if spec and text:
            fails.append(f"{name} (line {i + 1}): text after the widget spec {spec} turns the widget into a plain box — "
                         "put the help text on the line above")
            above = lines[i - 1].strip() if i > 0 else ""
            if not above.startswith("//") or above.startswith("// ="):
                fixes.append((i, text, spec))
    if a.fix and fixes:
        for i, text, spec in sorted(fixes, reverse=True):
            m = ASSIGN.match(lines[i])
            lines[i] = f"{m.group(1)}{m.group(2)} = {m.group(3).strip()}; // {spec}"
            lines.insert(i, f"{m.group(1)}// {text}")
        open(a.scad, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print(f"fixed {len(fixes)} parameter(s): help text moved above — run the check again")
        return 0

    # widgets as the Customizer sees them
    osc = pick_openscad(a.openscad)
    params = None
    if osc:
        data, err = param_export(osc, a.scad)
        if data is None:
            fails.append(f"OpenSCAD could not read the parameters: {err.strip()}")
        else:
            params = data.get("parameters", [])
    else:
        notes.append("openscad-fast is not installed: widget checks skipped (install_openscad.sh)")
    if params is not None:
        for p in params:
            name, t = p.get("name"), p.get("type")
            if name not in plines:
                continue   # a parameter of an included library (the working file's Customizer does not list those)
            if not p.get("caption"):
                fails.append(f"{name}: no help text on the line above")
            init = p.get("initial")
            if isinstance(init, list):
                fails.append(f"{name}: a vector shows as spin boxes — use one slider per value and build the vector in the derived values")
                continue
            if t == "number" and not p.get("options") and ("min" not in p or "max" not in p):
                fails.append(f"{name}: a number without a slider or menu — add  // [min:step:max]  or  // [3:M3, 6:M6]")
            if t == "string" and not p.get("options"):
                words = compared_words(src, name)
                if words:
                    fails.append(f"{name}: the model compares it with fixed values ({', '.join(repr(w) for w in words)}) — make it a menu "
                                 f"// [{', '.join(w + ':' + w.capitalize() for w in words)}]")
                else:
                    notes.append(f"{name}: free text box (fine for custom text such as a label; a fixed set of values needs a menu)")
            if name == "part" and p.get("options"):
                vals = [str(o.get("value")) for o in p["options"]]
                comps = [v for v in vals if v not in ("all", "assembly")]
                if len(comps) >= 2:
                    for need, what in (("all", "all parts on one print plate"), ("assembly", "the assembled view")):
                        if need not in vals:
                            fails.append(f"part: {len(comps)} components but no `{need}` option ({what})")

    kind = "Customizer file" if customizer else "working file"
    for n in notes:
        print("NOTE", n)
    for f in fails:
        print("FAIL", f)
    print(("PASS" if not fails else "FAIL") + f"  {a.scad} ({kind}, {len(plines)} parameters)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
