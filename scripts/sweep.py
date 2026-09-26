#!/usr/bin/env python3
"""sweep.py — parameter sweep for any Customizer-ready OpenSCAD file (MSF "3D Printing for All").

Reads the Customizer parameters of a .scad file (ranges `// [min:step:max]`, dropdowns
`// [a, b, c]`, booleans), renders the default set first (T1) and then every extreme with the
other parameters at their defaults (T2 / T3), and classifies each case:
  PASS   rendered, STL written
  GUARD  an assert() stopped it — the message is recorded (a working guard is a pass)
  FAIL   any other error, a timeout, or an empty STL
It refuses to run a case whose parameter does not exist in the file (OpenSCAD would silently
ignore the -D and the case would test nothing).

Usage
  python3 sweep.py part.scad                       # auto cases from the Customizer ranges
  python3 sweep.py part.scad --params wall_t,drain # only these parameters
  python3 sweep.py part.scad --spec cases.json     # explicit cases (see below)
  python3 sweep.py part.scad --check --sections 5,20   # run check_stl.py on every PASS case
Long sweeps: run detached and poll —
  setsid nohup python3 sweep.py part.scad --check > tools/sweep_report_$(date +%F).txt 2>&1 < /dev/null &

cases.json: {"cases": [{"name": "wide", "D": {"dev_w": 150, "part": "holder"}}, ...]}
Fixed overrides for every case: --fixed 'part="holder"' --fixed 'fn_export=48'
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

PARAM_RE = re.compile(r'^\s*([A-Za-z_]\w*)\s*=\s*([^;/]+?)\s*;\s*(?://\s*(\[[^\]]*\])?)?', re.M)


def parse_params(path):
    """Return {name: {"default": str, "kind": range|dropdown|bool|number|string|other, ...}}."""
    text = open(path, encoding="utf-8").read()
    params = {}
    for m in PARAM_RE.finditer(text):
        name, default, ann = m.group(1), m.group(2).strip(), m.group(3)
        if name.startswith("$") or name in params:
            continue
        info = {"default": default, "kind": "other"}
        if default in ("true", "false"):
            info["kind"] = "bool"
        elif ann and ":" in ann:
            nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", ann)]
            if len(nums) >= 2:
                info["kind"] = "range"
                info["min"], info["max"] = nums[0], nums[-1]
        elif ann:
            opts = [o.strip() for o in ann.strip("[]").split(",") if o.strip()]
            if opts:
                info["kind"] = "dropdown"
                info["options"] = [o.split(":")[0].strip() for o in opts]
        elif re.fullmatch(r"-?\d+(?:\.\d+)?", default):
            info["kind"] = "number"
        elif default.startswith('"'):
            info["kind"] = "string"
        params[name] = info
    return params


def fmt(name, value, params):
    """Format a -D value: strings quoted, others as given."""
    v = str(value)
    kind = params.get(name, {}).get("kind")
    if kind in ("dropdown", "string") and not v.startswith('"') and v not in ("true", "false"):
        v = f'"{v}"'
    return f"{name}={v}"


def auto_cases(params, only=None):
    cases = [{"name": "defaults", "D": {}}]
    for name, info in params.items():
        if only and name not in only:
            continue
        if info["kind"] == "range":
            cases.append({"name": f"{name}=min({info['min']:g})", "D": {name: info["min"]}})
            cases.append({"name": f"{name}=max({info['max']:g})", "D": {name: info["max"]}})
        elif info["kind"] == "dropdown":
            for o in info["options"]:
                if o.strip('"') != info["default"].strip('"'):
                    cases.append({"name": f"{name}={o}", "D": {name: o}})
        elif info["kind"] == "bool":
            other = "false" if info["default"] == "true" else "true"
            cases.append({"name": f"{name}={other}", "D": {name: other}})
    return cases


def run_case(openscad, scad, case, params, fixed, outdir, timeout):
    stl = os.path.join(outdir, re.sub(r"[^\w.=-]+", "_", case["name"]) + ".stl")
    cmd = [openscad, "-o", stl, "--export-format", "binstl"]
    for k, v in case["D"].items():
        cmd += ["-D", fmt(k, v, params)]
    for f in fixed:
        cmd += ["-D", f]
    cmd.append(scad)
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = p.stdout + p.stderr
        rc = p.returncode
    except subprocess.TimeoutExpired:
        return {"name": case["name"], "status": "FAIL", "reason": f"timeout after {timeout} s", "stl": None, "seconds": timeout}
    secs = round(time.time() - t0, 1)
    if rc == 0 and os.path.exists(stl) and os.path.getsize(stl) > 84:
        warn = [l for l in out.splitlines() if l.startswith("WARNING")]
        return {"name": case["name"], "status": "PASS", "reason": "; ".join(warn[:3]), "stl": stl, "seconds": secs}
    m = re.search(r"ERROR: Assertion.*?(?:\n|$)", out)
    if m:
        return {"name": case["name"], "status": "GUARD", "reason": m.group(0).strip(), "stl": None, "seconds": secs}
    err = [l for l in out.splitlines() if "ERROR" in l or "error" in l.lower()]
    return {"name": case["name"], "status": "FAIL", "reason": (err[-1] if err else out.strip()[-300:]) or "no STL written", "stl": None, "seconds": secs}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scad")
    ap.add_argument("--spec", help="JSON file with explicit cases")
    ap.add_argument("--params", help="comma list: only sweep these parameters")
    ap.add_argument("--fixed", action="append", default=[], help="-D override applied to every case, e.g. 'part=\"holder\"'")
    ap.add_argument("--openscad", default=None, help="default: tools/openscad-fast (Manifold) if installed, else openscad")
    ap.add_argument("--out", default="sweep_out")
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--check", action="store_true", help="run check_stl.py on every PASS case")
    ap.add_argument("--sections", default="", help="passed to check_stl.py")
    ap.add_argument("--allow-bridges", action="store_true")
    ap.add_argument("--report", default="", help="write the text report here as well")
    a = ap.parse_args(argv)

    if a.openscad is None:
        fast = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openscad-fast")
        wasm = os.path.join(os.path.expanduser("~"), ".openscad-wasm", "node_modules", "openscad-wasm", "openscad.js")
        a.openscad = fast if (os.path.exists(fast) and os.path.exists(wasm)) else "openscad"
    params = parse_params(a.scad)
    if a.spec:
        cases = json.load(open(a.spec))["cases"]
    else:
        only = set(a.params.split(",")) if a.params else None
        cases = auto_cases(params, only)
    unknown = sorted({k for c in cases for k in c["D"] if k not in params})
    if unknown:
        print("REFUSED: these parameters do not exist in the file (OpenSCAD would ignore them):", ", ".join(unknown))
        return 2
    os.makedirs(a.out, exist_ok=True)
    results = []
    lines = [f"sweep of {a.scad} — {len(cases)} cases — {time.strftime('%Y-%m-%d %H:%M')}"]
    for c in cases:
        r = run_case(a.openscad, a.scad, c, params, a.fixed, a.out, a.timeout)
        if r["status"] == "PASS" and a.check:
            try:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from check_stl import check_file
                secs = [float(z) for z in a.sections.split(",") if z.strip()] if a.sections else []
                chk = check_file(r["stl"], sections=secs, allow_bridges=a.allow_bridges)
                if not chk["ok"]:
                    r["status"] = "FAIL"
                    r["reason"] = "check_stl: " + "; ".join(chk["fail"])
                elif chk["warn"]:
                    r["reason"] = "check_stl warn: " + "; ".join(chk["warn"])
            except Exception as e:  # pragma: no cover
                r["reason"] = f"check_stl could not run: {e}"
        results.append(r)
        line = f"{r['status']:5s}  {r['name']:40s} {r['seconds']:>6}s  {r['reason']}"
        lines.append(line)
        print(line, flush=True)
    n = {s: sum(1 for r in results if r["status"] == s) for s in ("PASS", "GUARD", "FAIL")}
    summary = f"SUMMARY: {n['PASS']} PASS, {n['GUARD']} GUARD, {n['FAIL']} FAIL of {len(results)}"
    lines.append(summary)
    print(summary)
    if a.report:
        with open(a.report, "w") as f:
            f.write("\n".join(lines) + "\n")
    with open(os.path.join(a.out, "sweep_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    return 1 if n["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
