#!/usr/bin/env python3
"""sweep.py — parameter sweep for any Customizer-ready OpenSCAD file (MSF "3D Printing for All").

Reads the Customizer parameters of a .scad file — the block before `// ===== Derived values =====` (or the
first module / function), [Hidden] excluded — with their widgets: slider `// [min:max]` or
`// [min:step:max]`, menu `// [a, b]` / `// [a:Label, b:Label]` / `// [3:M3, 6:M6]`, checkbox (true/false).
Renders the default set first (T1), then every slider end and every other menu value and checkbox state
with the other parameters at their defaults (T2 / T3), and classifies each case:
  PASS   rendered, STL written
  GUARD  an assert() stopped it — the message is recorded (a working guard is a pass; a GUARD at a slider
         end is also counted separately: narrow the range unless another parameter makes that end valid)
  FAIL   any other error, a timeout, or an empty STL
It refuses to run a case whose parameter is not a Customizer parameter of the file (OpenSCAD would
silently ignore the -D and the case would test nothing) — for --spec, --params and --fixed alike.
A model may announce what its STL is:  echo("CHECK expect_bodies=2")  for an all-parts print plate, or
echo("CHECK view_only expect_bodies=2")  for an assembled view; --check passes that to check_stl.py.

Usage
  python3 sweep.py part.scad                       # auto cases from the Customizer
  python3 sweep.py part.scad --params wall_t,drain # only these parameters
  python3 sweep.py part.scad --spec cases.json     # explicit cases (see below)
  python3 sweep.py part.scad --check --sections auto --report tools/sweep_report_$(date +%F).txt
  python3 sweep.py part.scad --check --report r.txt --resume      # skip the cases already in r.txt
  python3 sweep.py --merge r1.txt r2.txt --report all.txt       # one report and SUMMARY over chunked runs
The report is written line by line, so a run that is stopped keeps what it did; --resume continues it.
Long sweeps: run in the foreground in chunks (--params a,b,c), one report per chunk, then --merge.
Every PASS STL is cleaned of zero-area specks (stl_clean.py) before check_stl.py runs; the reason column says so.

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

sys.dont_write_bytecode = True   # no __pycache__ next to the scripts (it breaks `cp scripts/* tools/`)

ASSIGN = re.compile(r'^\s*([A-Za-z_]\w*)\s*=\s*([^;]+?)\s*;\s*(?://\s*(.*))?$')
GROUP = re.compile(r'^\s*/\*\s*\[([^\]]*)\]\s*\*/\s*$')
END = re.compile(r'^\s*(//\s*=+\s*derived|module\s|function\s)', re.I)
NUM = r'-?(?:\d+\.?\d*|\.\d+)(?:[eE]-?\d+)?'
RANGE = re.compile(rf'^\[\s*{NUM}\s*(?::\s*{NUM}\s*){{1,2}}\]$')
CHECK_RE = re.compile(r'CHECK((?:\s+\w+(?:=[\d.]+)?)+)')


def parse_params(path):
    """Customizer parameters: {name: {"default", "kind": range|dropdown|bool|number|string|other, ...}}."""
    params, group = {}, ""
    for line in open(path, encoding="utf-8"):
        if END.match(line):
            break
        g = GROUP.match(line)
        if g:
            group = g.group(1).strip()
            continue
        if group.lower() == "hidden":
            continue
        m = ASSIGN.match(line)
        if not m or m.group(1) in params:
            continue
        name, default, ann = m.group(1), m.group(2).strip(), (m.group(3) or "").strip()
        spec = ann.split("]")[0] + "]" if ann.startswith("[") else ""
        info = {"default": default, "kind": "other", "string": default.startswith('"')}
        if default in ("true", "false"):
            info["kind"] = "bool"
        elif spec and RANGE.match(spec):
            nums = [float(x) for x in re.findall(NUM, spec)]
            info.update(kind="range", min=nums[0], max=nums[-1])
        elif spec:
            opts = [o.strip() for o in spec[1:-1].split(",") if o.strip()]
            info.update(kind="dropdown", options=[o.split(":")[0].strip().strip('"') for o in opts])
        elif re.fullmatch(NUM, default):
            info["kind"] = "number"
        elif info["string"]:
            info["kind"] = "string"
        params[name] = info
    return params


def fmt(name, value, params):
    """Format a -D value: quoted only when the parameter is a string."""
    v = str(value)
    if isinstance(value, float) and value.is_integer():
        v = str(int(value))
    if params.get(name, {}).get("string") and not v.startswith('"'):
        v = f'"{v}"'
    return f"{name}={v}"


def auto_cases(params, only=None):
    cases = [{"name": "defaults", "D": {}}]
    for name, info in params.items():
        if only and name not in only:
            continue
        if info["kind"] == "range":
            cases.append({"name": f"{name}=min({info['min']:g})", "D": {name: info["min"]}, "end": True})
            cases.append({"name": f"{name}=max({info['max']:g})", "D": {name: info["max"]}, "end": True})
        elif info["kind"] == "dropdown":
            for o in info["options"]:
                if o != info["default"].strip('"'):
                    cases.append({"name": f"{name}={o}", "D": {name: o}})
        elif info["kind"] == "bool":
            other = "false" if info["default"] == "true" else "true"
            cases.append({"name": f"{name}={other}", "D": {name: other}})
    return cases


def check_args_from(out):
    """Parse `ECHO: "CHECK expect_bodies=2 view_only"` into check_stl keyword arguments."""
    m = CHECK_RE.search(out)
    if not m:
        return {}
    ca = {}
    for tok in m.group(1).split():
        if tok.startswith("expect_bodies="):
            ca["expect_bodies"] = int(float(tok.split("=")[1]))
        elif tok.startswith("max_size="):
            ca["max_size"] = float(tok.split("=")[1])
        elif tok == "view_only":
            ca["view_only"] = True
    return ca


def run_case(openscad, scad, case, params, fixed, outdir, timeout):
    stl = os.path.join(outdir, re.sub(r"[^\w.=-]+", "_", case["name"]) + ".stl")
    if os.path.exists(stl):
        os.remove(stl)
    cmd = [openscad, "-o", stl, "--export-format", "binstl"]
    for k, v in case["D"].items():
        cmd += ["-D", fmt(k, v, params)]
    for f in fixed:
        cmd += ["-D", f]
    cmd.append(scad)
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out, rc = p.stdout + p.stderr, p.returncode
    except subprocess.TimeoutExpired:
        return {"name": case["name"], "status": "FAIL", "reason": f"timeout after {timeout} s", "stl": None, "seconds": timeout}
    secs = round(time.time() - t0, 1)
    lines = [re.sub(r"^\[OpenSCAD[^\]]*\]:\s*", "", l) for l in out.splitlines()]   # tolerate an older wrapper's prefix
    if rc == 0 and os.path.exists(stl) and os.path.getsize(stl) > 84:
        warn = [l for l in lines if l.startswith("WARNING")]
        return {"name": case["name"], "status": "PASS", "reason": "; ".join(warn[:3]), "stl": stl, "seconds": secs,
                "check_args": check_args_from(out)}
    m = next((l for l in lines if "Assertion" in l and "ERROR" in l), None)
    if m:
        return {"name": case["name"], "status": "GUARD", "reason": m.strip()[:300], "stl": None, "seconds": secs}
    err = [l for l in lines if l.startswith(("ERROR", "WARNING")) or "FAILED" in l]
    reason = err[0] if err else ("no geometry: " + next((l for l in lines if "empty" in l.lower()), "no STL written"))
    return {"name": case["name"], "status": "FAIL", "reason": reason.strip()[:300], "stl": None, "seconds": secs}


def done_cases(report):
    """Case names already recorded in an earlier (possibly interrupted) report."""
    names = {}
    if report and os.path.exists(report):
        for line in open(report, encoding="utf-8"):
            m = RESULT_LINE.match(line)
            if m:
                names[m.group(2).strip()] = line.rstrip("\n")
    return names


RESULT_LINE = re.compile(r"^(PASS|GUARD|FAIL)\s+(\S+)\s+[\d.]+s(?:\s|$)")


def merge(reports, out):
    """Combine chunk reports: the last line per case wins; one SUMMARY for all."""
    cases, heads = {}, []
    for r in reports:
        for line in open(r, encoding="utf-8"):
            line = line.rstrip("\n")
            m = RESULT_LINE.match(line)
            if m:
                cases[m.group(2)] = line
            elif line.startswith("sweep of"):
                heads.append(line)
    n = {s: sum(1 for l in cases.values() if l.startswith(s)) for s in ("PASS", "GUARD", "FAIL")}
    ends = [c for c, l in cases.items() if l.startswith("GUARD") and ("=min(" in c or "=max(" in c)]
    lines = [f"merged report of {len(reports)} chunk(s):"] + ["  " + h for h in heads] + list(cases.values())
    lines.append(f"SUMMARY: {n['PASS']} PASS, {n['GUARD']} GUARD, {n['FAIL']} FAIL of {len(cases)}")
    if ends:
        lines.append(f"SLIDER ENDS STOPPED BY A GUARD ({len(ends)}): {', '.join(ends)} — narrow these ranges unless another "
                     "parameter makes the end valid (T3)")
    text = "\n".join(lines) + "\n"
    if out:
        open(out, "w", encoding="utf-8").write(text)
    print(text, end="")
    return 1 if n["FAIL"] else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scad", nargs="?")
    ap.add_argument("--merge", nargs="+", metavar="REPORT", help="combine chunk reports into --report")
    ap.add_argument("--spec", help="JSON file with explicit cases")
    ap.add_argument("--params", help="comma list: only sweep these parameters")
    ap.add_argument("--fixed", action="append", default=[], help="-D override applied to every case, e.g. 'part=\"holder\"'")
    ap.add_argument("--openscad", default=None, help="default: openscad-fast (Manifold) if it works, else openscad")
    ap.add_argument("--out", default="sweep_out")
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--check", action="store_true", help="run check_stl.py on every PASS case")
    ap.add_argument("--sections", default="", help="passed to check_stl.py (numbers, NN%%, top-D or auto)")
    ap.add_argument("--allow-bridges", action="store_true")
    ap.add_argument("--report", default="", help="write the text report here, line by line")
    ap.add_argument("--resume", action="store_true", help="skip the cases already recorded in --report and append")
    a = ap.parse_args(argv)
    if a.merge:
        return merge(a.merge, a.report)
    if not a.scad:
        ap.error("give the .scad file (or --merge REPORT ...)")

    if a.openscad is None:
        here = os.path.dirname(os.path.abspath(__file__))
        fast = os.path.join(here, "openscad-fast")
        a.openscad = "openscad"
        if os.path.exists(fast):
            try:
                if subprocess.run(["bash", fast, "--version"], capture_output=True, timeout=60).returncode == 0:
                    a.openscad = fast
            except Exception:
                pass
    if a.openscad.endswith("openscad-fast") and not os.access(a.openscad, os.X_OK):
        os.chmod(a.openscad, 0o755)   # git does not always keep the executable bit
    params = parse_params(a.scad)
    if a.spec:
        spec = json.load(open(a.spec))
        if not isinstance(spec, dict) or not isinstance(spec.get("cases"), list):
            print('REFUSED: --spec must be a JSON object {"cases": [{"name": ..., "D": {...}}, ...]}')
            return 2
        cases = spec["cases"]
    else:
        only = set(p.strip() for p in a.params.split(",") if p.strip()) if a.params else None
        if only and only - set(params):
            print("REFUSED: --params names that are not Customizer parameters of the file:", ", ".join(sorted(only - set(params))))
            return 2
        cases = auto_cases(params, only)
    fixed_names = {f.split("=", 1)[0].strip() for f in a.fixed}
    unknown = sorted(({k for c in cases for k in c["D"]} | fixed_names) - set(params))
    if unknown:
        print("REFUSED: these are not Customizer parameters of the file (OpenSCAD would ignore them):", ", ".join(unknown))
        return 2
    os.makedirs(a.out, exist_ok=True)
    previous = done_cases(a.report) if a.resume else {}
    rep = open(a.report, "a" if a.resume else "w", encoding="utf-8") if a.report else None

    def emit(line):
        print(line, flush=True)
        if rep:
            rep.write(line + "\n"); rep.flush()

    emit(f"sweep of {a.scad} — {len(cases)} cases — {time.strftime('%Y-%m-%d %H:%M')} — engine {os.path.basename(a.openscad)}"
         + (f" — resuming, {len(previous)} cases already done" if previous else ""))
    results = []
    for c in cases:
        if c["name"] in previous:
            st = previous[c["name"]].split()[0]
            results.append({"name": c["name"], "status": st, "end": c.get("end", False),
                            "reason": previous[c["name"]], "resumed": True})
            continue
        r = run_case(a.openscad, a.scad, c, params, a.fixed, a.out, a.timeout)
        r["end"] = c.get("end", False)
        if r["status"] == "PASS" and a.check:
            try:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from check_stl import check_file
                from stl_clean import clean
                nspeck, _ = clean(r["stl"])
                if nspeck:
                    r["reason"] = (r["reason"] + "; " if r["reason"] else "") + f"{nspeck} speck(s) removed by stl_clean"
                chk = check_file(r["stl"], sections=a.sections, allow_bridges=a.allow_bridges, **r.get("check_args", {}))
                if not chk["ok"]:
                    r["status"] = "FAIL"
                    r["reason"] = "check_stl: " + "; ".join(chk["fail"])
                elif chk["warn"]:
                    r["reason"] = (r["reason"] + "; " if r["reason"] else "") + "check_stl warn: " + "; ".join(chk["warn"])
            except Exception as e:  # pragma: no cover
                r["status"] = "FAIL"
                r["reason"] = f"check_stl could not run: {e}"
        results.append(r)
        emit(f"{r['status']:5s}  {r['name']:40s} {r['seconds']:>6}s  {r['reason']}")
    n = {s: sum(1 for r in results if r["status"] == s) for s in ("PASS", "GUARD", "FAIL")}
    ends = [r["name"] for r in results if r["status"] == "GUARD" and r.get("end")]
    emit(f"SUMMARY: {n['PASS']} PASS, {n['GUARD']} GUARD, {n['FAIL']} FAIL of {len(results)}")
    if ends:
        emit(f"SLIDER ENDS STOPPED BY A GUARD ({len(ends)}): {', '.join(ends)} — narrow these ranges unless another "
             "parameter makes the end valid (T3)")
    if rep:
        rep.close()
    with open(os.path.join(a.out, "sweep_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    return 1 if n["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
