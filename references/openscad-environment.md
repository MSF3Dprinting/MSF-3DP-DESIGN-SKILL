# OpenSCAD environment, versions and coding conventions

*Reference file of the `msf-3dp-design` skill. Read it before the first render of a session and before writing any .scad file.* Section numbers (§) are shared by every file of the skill: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · readiness-levels.md · Appendix A glossary.md · Appendix C sources.md.

## 6. OpenSCAD environment and versions

### 6.1 Which OpenSCAD — and how fast
As of September 2026 the last *stable* release of OpenSCAD is still **2021.01**; every speed and feature improvement lives in the **development snapshots** (2025.x / 2026.x). Since the 2024.09.28 snapshot the **Manifold** geometry engine is available and since August 2025 it is the default. The difference is not cosmetic — measured in a Claude Code cloud container on 27 September 2026, median of 3 runs (wasm‑CGAL: 1 run); triangles as each engine exports them:

| Model | Triangles (Manifold / CGAL) | Native 2021.01 (CGAL) | 2025.07 wasm, CGAL | 2025.07 wasm, **Manifold** |
|---|---|---|---|---|
| `scad/example_part.scad` at defaults (pocket, back plate with tabs, fillets, teardrop holes, drain) | 3076 / 3452 | 2.8 s | 8.5 s | **0.41 s** |
| Cube 40 − sphere r 25 − 3 through‑cylinders d 10 on the axes, `$fn = 96` | 3952 / 4816 | 3.6 s | 8.6 s | **0.46 s** |
| `scad/test_coupon.scad` at defaults, 7 holes + debossed digits (fonts mounted) | 10920 / 10892 | 26.5 s | 80.1 s | **0.95 s** |
| Pocket 90 × 40 × 110, walls 2.7, floor 3, both long walls `hex_grid(8, 1.6, [80, 100])` | 5180 / 5180 | 2.1 s | 5.1 s | **0.58 s** |

The engine makes the difference (wasm‑CGAL is *slower* than native CGAL; wasm‑Manifold is 4–28× faster than native and 9–84× faster than wasm‑CGAL). Text and perforations, which cripple CGAL, become cheap. An earlier table (v1.3) measured the coupon without its digits — the wasm build had no fonts then, and `text()` produced nothing.

| Who | Version | Notes |
|---|---|---|
| You (Claude), all geometry export in the sandbox | `openscad-fast` — OpenSCAD 2025.07.18 with Manifold 3.1, from the npm package `openscad-wasm` 0.0.4 (§6.4) | STL, OFF, AMF, CSG, echo and the Customizer parameter export (`--export-format param`); no PNG (no OpenGL in wasm), no 3MF (crashes in this build — PrusaSlicer saves a 3MF project from the STL) |
| You (Claude), PNG views | native 2021.01 from apt, preview mode via `render_views.py` | preview (OpenCSG) is fast; `--full` forces a CGAL render only when needed |
| Advisor and designers on their own computers | the current development snapshot from openscad.org → Downloads → Development Snapshots (Windows, macOS, Linux); macOS `brew install openscad@snapshot`; Manifold is on by default | the MSF customizer server needs 2023.09 or newer for Manifold (its README) |
| Field laptops that only open the Customizer and export STL | any version ≥ 2021.01 | slow CGAL render, but works; recommend a snapshot |
| **Language level of every `.scad` you write** | **2021.01** | so every install opens it: no `roof()`, `textmetrics()`, `fontmetrics()`, colour export, object literals; `assert()`, `$preview`, `is_undef()`, function literals, `offset()`, `text()` are fine |

Put `assert(version_num() >= 20210100, "OpenSCAD 2021.01 or newer is required");` in `common.scad` (below the parameters) and record the exporter version in `stl/EXPORT_LOG.txt` and the DATASHEET.

### 6.2 Backend and speed
- `openscad-fast` always runs Manifold. Snapshots from August 2025 on: Manifold is the default; older snapshots: Preferences → Advanced → 3D Rendering → Backend = Manifold, or `--backend=manifold`. 2021.01: CGAL only.
- Keep `$fn` behind `facets` (Hidden) so smoothness can be traded for speed; preview low, export ≈ 96. Build shapes from 2D profiles — `offset()` then `linear_extrude()` — rather than 3D hulls of cylinders; avoid `minkowski()` (a `hull()` between two extruded profiles gives the same chamfer far more cheaply); prefer one `difference()` with many children over nested differences.

**Boolean hygiene (2021.01 / CGAL).** Never let a cutter's face coincide with the face it cuts, and never let two cutters meet on a shared plane or share a tangent line: extend cutters 0.2 mm into the void, overlap neighbouring cutters by 0.05 mm, make a chamfer 0.01 mm larger than a fillet of the same nominal size. Clip every cutter to the region it is meant to cut — a chamfer cutter wider than its channel once shaved the tops of two walls and left a crevice that every automated check missed. Build a chamfered base in a single `hull()` of all its pieces. The symptom of bad booleans is an STL that passes every overhang test and fails watertightness or has two‑face "bodies" (T4); the sweep finds the values that trigger it. Manifold is more tolerant of coincident faces than CGAL, but it still leaves them at some parameter values, and the flat Customizer file must still render in 2021.01 — keep the hygiene:
- **Solids never share a face.** Two bodies unioned along a common face (a pocket's back face on a back plate's back face) left a loose sheet at some sizes; end one body inside the other instead (the example pocket ends halfway into its back plate).
- **Nothing exactly tangent.** A fillet circle tangent to a wall, or a straight run overlapping its arc by EPS, leaves zero‑area specks; set the circle 0.05 mm off the wall (invisible in print). `stl_clean.py` removes specks below 0.01 mm² and export / sweep log it — a removal at the default parameters means the model still needs fixing.
- **Hull only adjacent slabs.** A chamfer or flare made by `hull()` spans two neighbouring slabs, never three: one hull over both face flares of a cutter widened a whole gauge notch by 1.4–1.8 mm (`flared_cutter()` does it right).
- **Features that meet a chamfered edge reach into it.** A vertical fillet or rib next to a 0.4 mm bottom chamfer extends `chamfer_bottom + 0.1` into the wall, or it stands 0.2 mm proud as a sliver at the bed; a profile meeting a sliced rounding overlaps 1 mm into its host.

### 6.3 Command line (what you run)
```bash
# geometry export — Manifold, seconds (same arguments as openscad; PNG not possible here)
tools/openscad-fast -o stl/part_holder_v1.0.stl --export-format binstl -D 'part="holder"' -D 'wall_t=2.7' part.scad
tools/openscad-fast -o stl/part_large_v1.0.stl -p part.json -P large part.scad
# PNG views — native 2021.01 in preview mode, headless (render_views.py wraps this in xvfb-run and makes the sheet)
python3 tools/render_views.py part.scad --out img --name part --context part_context.scad
# what the Customizer shows (widgets, captions, menus) — the input of lint_customizer.py
tools/openscad-fast -o part.param --export-format param part.scad
# a section drawing from the exported STL (README, design review, structural review)
python3 tools/section_from_stl.py stl/part_holder_v1.0.stl --z 20 --out img/part_section_z20.png
# a single full CGAL render image, only when a preview artefact must be ruled out
xvfb-run -a openscad -o img/part_full.png --render=true --viewall --autocenter --projection=o --camera=0,0,0,90,0,0,500 part.scad
```
Standard cameras: front `90,0,0`, side `90,0,90`, top `0,0,0` (orthographic), isometric `55,0,25`. Documentation scenes: wrap parts in `render()` before `color()`; explicit `--camera` when stand‑ins are long; render 2× and downsample; re‑save without EXIF — `render_views.py` does all of it.

### 6.4 In the sandbox — claude.ai or a Claude Code cloud container (Ubuntu 24.04)
The claude.ai sandbox is empty at the start of every conversation; a Claude Code container keeps its installs for the session. `bash tools/install_openscad.sh` does everything below, skips what is installed, and always ends with a readiness test; know what it does:
1. `rm -f /etc/apt/sources.list.d/nodesource*` — that repository returns 403 and breaks `apt-get update` in some images.
2. `timeout 600 bash -c 'apt-get update -qq && apt-get install -y --no-install-recommends openscad xvfb fonts-liberation'` in the foreground — background installs are killed when the tool call returns. Native 2021.01 (CGAL) is used only for PNG views (`xvfb-run -a`).
3. `pip install trimesh numpy scipy shapely rtree networkx pillow matplotlib --break-system-packages` (networkx: section checks; matplotlib: section drawings).
4. **Fast exporter:** `npm install --prefix "$HOME/.openscad-wasm" openscad-wasm@0.0.4` (npmjs.org is reachable; `files.openscad.org` is not) and the wrapper `tools/openscad-fast` → `openscad_manifold.mjs`. The wrapper mounts the part's folder (and 3 levels of sub‑folders — not `../`) into the wasm file system so `include <common.scad>` resolves, mounts the system Liberation and DejaVu fonts (the wasm build ships none: without them `text()` is empty and a coupon loses its digits), runs with `--backend=manifold`, prints the messages exactly like the native binary (`ECHO:`, `WARNING:`, `ERROR:` — no prefix), and writes the file back only on success. `export.sh`, `sweep.py`, `flatten_scad.py --verify` and `lint_customizer.py` use it whenever it runs, and fall back to native `openscad` when it does not.
5. Readiness test: a real export with text through the `openscad-fast` on the PATH — "fonts OK — ready".

Shell and tool facts:
- A tool call is limited (300 s in the claude.ai sandbox; up to 600 s in Claude Code), and background jobs die when the turn ends (claude.ai — sweeps died mid‑run three times). Run sweeps in the foreground in chunks (`--params a,b,c`, about 60–80 s each, one `--report` per chunk, `--resume` after an interruption) and combine them with `sweep.py --merge`.
- `/bin/sh` (dash) has no `time`, `disown`, `<<<` or brace expansion (`mkdir -p d/{a,b}` makes a literal folder) — use `bash -c`, `date +%s`, explicit paths; the scripts re‑run themselves under bash.
- Never `eval` a `-D` string (it strips the quotes of `closure="zipties"`); `pkill -f <pattern>` kills the shell whose own command line matches — use `pgrep -f "[p]attern"`.
- OpenSCAD silently ignores `-D` for a parameter that does not exist — `sweep.py` refuses unknown names.
- GitHub clones work. Printables, Thingiverse and the NIH 3D Print Exchange may be blocked by the sandbox's network policy — check once; if blocked, ask the user for the file or link and say so in the confirmation.

### 6.5 Libraries and fonts
- Dependency‑free by default. Use BOSL2 only when the system you must match already uses it (HomeRacker `support.scad`); then vendor the library at a pinned version and say so in the README.
- Font: **Liberation Sans** (`font = "Liberation Sans:style=Bold"`) — installed from the apt package `fonts-liberation` and mounted into the wasm engine by `openscad-fast`; desktop installs of OpenSCAD bundle it. Measured: capital height ≈ 0.96 × size, stroke ≈ 0.2 × size — size 5 gives 4.8 mm capitals and 1.0 mm strokes. A font that is not installed is replaced silently by another one (`WARNING: Can't get font …` in the log) — never ship text rendered in a fallback font. Other scripts need a font that supports them; keep strings as parameters.
- Measuring string widths: export the 2D text of a throw‑away file (`linear_extrude(1) text(...)`) with `openscad-fast` and read the extents with trimesh; `textmetrics()` exists in 2025.07 (`--enable=textmetrics`) but must not appear in a delivered `.scad` (language level 2021.01). Size plates for the longest string, with stated margins, before fixing plate sizes.

### 6.6 Slicer
PrusaSlicer 2.9.x is the MSF reference (kit). Give the settings in the README (§5.5). The user confirms orientation, "no supports", print time and filament use in the slicer before printing.


## 7. OpenSCAD conventions

### 7.1 File layout
Every design has a **working file** `<item>.scad` (the file you edit; it includes `common.scad` and `helpers.scad`) and, generated from it, the **Customizer file** `<item>_customizer.scad` (§7.7). Layout of the working file:
1. Design header (§7.4). **No `// @` lines** — the five‑line Customizer header belongs only in the Customizer file.
2. `include <common.scad>` and `include <helpers.scad>` (common.scad holds the version assert).
3. Customizer parameters in `/* [Group] */` blocks, in this order where they apply: `[Part selection]`, `[Main dimensions]`, `[Interface / fit]`, `[Mounting]`, `[Printability]`, `[Text]` (non‑clinical only), `[Preview]`, `[Hidden]`.
4. `// ===== Derived values =====` — computed values, clearly separated from user parameters; any derived value a user may need to override has an override parameter. Functions that a context scene needs (the device size, where it sits) are defined here too.
5. `// ===== Input validation =====` — `assert()` with plain‑language messages; `NOTE` and `HARDWARE` echoes.
6. Modules: helpers (§7.5), features, part modules, `assembled()`.
7. Main build: the `part` selector (§7.3); ghost parts behind `if ($preview && show_ghosts)`.
Reference: `scad/example_part.scad` (two parts, kit hardware, all four `part` options).

### 7.2 Customizer rules (owner, Sept 2026) — the user clicks and slides, never types what could be chosen
Checked by `lint_customizer.py` on the working file and on the Customizer file (T25); the widgets are read from OpenSCAD's own parameter export, so the check sees what the Customizer shows, and the native 2021.01 binary parses the file, because the fast 2025.07 engine accepts newer syntax (`roof()`, `textmetrics()`, `object()`) silently.
- **Help text on the line above, the widget spec alone after the value.** The comment line above a parameter is its label in the Customizer. After the value comes only the spec — `wall_t = 2.7; // [1.8:0.45:4.5]`. Text after the spec (`// [1.8:0.45:4.5] wall thickness`) silently turns the slider into a plain number box: the skill's own files did this until v1.4. `lint_customizer.py --fix` moves such text above.
- **Numbers are sliders**: `// [min:max]` or `// [min:step:max]`, with units in the help text. Where only some values are valid, a **numeric menu**: `bolt = 6; // [3:M3, 6:M6]`. A plain number box is not allowed.
- **Fixed choices are menus, with readable labels**: `part = "wing"; // [body:Body, wing:Wing, flap:Flap]`. Whenever the model compares a text parameter with fixed words (`part == "wing"`), it is a menu — the user clicks, never types a value that has a fixed list. Free text only where the value is the user's own text: the words on a keychain, a label, a bed number.
- **Checkboxes** for on/off (`true` / `false`).
- **No vector parameters** — the Customizer shows spin boxes. One slider per value (`pocket_1 … pocket_4`); build the vector in the derived values.
- Every parameter is a **literal** (a number, `true`/`false`, a quoted string) — never an expression or another variable, which the Customizer cannot show. The parameter block ends at `// ===== Derived values =====`; everything below it is not a control.
- **Internal switches are expressions** (`build_part = is_undef(ctx) ? true : false;`), never literal booleans in the parameter block — a literal would appear in the Customizer and be swept (a hidden `build_part = true` once swept to an empty STL).
- Every functional dimension is user‑definable — grip, wall, hole, clearance — never only auto‑derived from another value. Selections are menus, not extra files: the part selector, per‑side toggles (left/right wing, solid/perforated per wall), the mounting method.
- Validate with `assert()` and clear messages; fail loudly instead of producing broken geometry. Asserts on derived floats use a tolerance (`>= x - 0.001`). Guards refuse only physically impossible combinations; where the geometry can adapt (a tab widening for a larger washer, a hole moved to stay on its tab, a bend radius growing for a wider zip tie), adapt and `echo` a `NOTE` instead of refusing. The default parameter set passes every guard.
- Choose ranges so that each slider end renders with the other parameters at their defaults (`sweep.py` lists the ends stopped by a guard); narrow a range that always fails at one end. A guard at an end is acceptable only when another parameter makes that end valid.
- A parameter does what its name says. Never offer a setting whose name promises an effect the geometry cannot deliver.
- `$fn` follows `fn_preview` / `fn_export` from common.scad in the working file; the Customizer file sets `facets` under `[Hidden]` (flatten_scad.py does it). Text strings are parameters; colours are set by the filament — models never specify colours outside preview.
- Any open‑top pocket, holder or socket that can collect fluid carries a drain parameter (§8.1); any tall or narrow part carries brim ears (§5.1).

### 7.3 Structure, parts and naming
- One parametric file per item family; variants by menus. Multi‑item sets: `common.scad` holds shared values and helpers; models `include <common.scad>` and never copy its values; dependent dimensions are derived there, never retyped. Shared shapes go in a small library file.
- **The `part` menu (owner, Sept 2026).** Every item with more than one component has a `part` menu with: one entry per component, each **in its print position** on Z = 0 (the STL the user prints); **`all`** — every component in print position on one print plate that fits the MK4S bed (`print_plate()` lays them out and announces the body count to the checks); and **`assembly`** — every component in its **installed position and orientation**, to see how it goes together ("Assembled view – not for printing"; it echoes `CHECK view_only expect_bodies=N`, and `export.sh` puts it in `stl/view_only/`). Keep the components 0.1 mm apart in the assembly so they stay separate bodies. Identical copies are numbered files (`xN` in variants.txt), not plate entries.
- Names in `snake_case` with suffixes: `_d` diameter, `_r` radius, `_t` thickness, `_h` height, `_w` width, `_l` length, `_clr` clearance, `_n` count, `_deg` angle. Comments say *why* — the rule or the measurement behind a value.
- Ghost or mating parts (board, pole, device) with the `%` modifier so fit can be judged in preview; they never appear in the export.
- Model in print orientation; Z = 0 is the bed. Components that are installed in another orientation get their own rotation inside `assembled()`, never in the print export.
- When a sub‑shape can be rotated or offset by a parameter, the geometry that connects to it follows the transformed shape; always render the extreme angles and offsets in the sweep.
- Context scenes live in `<item>_context.scad` (a copy of `scad/context_scene.scad`): `use <item.scad>` (modules and functions without the top‑level build; `-D` overrides reach it), stand‑ins sized from the item's functions, stand‑in parameters named `ctx_…` so they never collide with the item's.

### 7.4 Design header (top of every working file)
```openscad
/* ===== DESIGN SUMMARY =====
 * Part / purpose:    <what it does, where it is used>
 * Version:           <x.y> <date>   Designer: Claude, msf-3dp-design skill v<version>
 * Critical part:     no | yes / unsure -> draft for review
 * Material:          PETG (white/natural/light) | PLA | TPU | PC | PP-GF  (reason)
 * Environment:       <temperature, chemicals, outdoor, disinfection method>
 * Loads:             <each load, its path, the layer direction on it; hand estimate with inputs>
 * Print orientation: <face on the plate, per component>; supports: none | built-in at <where>; brim: yes/no
 * Mating hardware:   <kit bolts / washers / nuts, or local parts with exact size>
 * Fits used:         <free/tight, printed-printed / printed-machined; clearance values>
 * Interfaces:        <what it fits, diameters, measured values and the source of each>
 * Unverified values: <placeholders that must be measured before printing, or "none">
 * Flags:             <> 50 C, watertight, smooth surface, chemicals, mains housing, user contact, sterilisation>
 * Deviations:        <any rule in sections 5, 8, 9 not met, and why>
 * Verified:          <sweep and checks, worst overhang x deg, bbox ..., exporter version>
 * Not verified:      <physical print, load test, ...>
 * Approval:          <Biomed + IPC | lab advisor | line manager>
 * ========================== */
```

### 7.5 Standard helpers and modelling recipes
`scad/common.scad` holds the defaults (print process, fits, minimum features, edges, bed size, kit hardware with `kit_*()` functions and `kit_bolt_for()`, `top_chamfer(t)`) — copy it next to the part, never retype its values. `scad/helpers.scad` implements: `rounded_rect` (radius clamped), `rounded_poly`, `teardrop2d`, `hex_grid`, `chamfered_prism`, `rounded_box`, `section_cut`, `vertical_hole`, `teardrop_hole`, `flat_top_hole`, `cone_roof_bore`, `nut_trap`, `drain_hole`, `flared_cutter`, `kit_hole`, `kit_hole_h`, `kit_counterbore`, `kit_nut_well`, `print_plate`, `brim_ear(s)`, `corner_ears`, `breakaway_support`, `tab`, `slot`, `ghost_tube / ghost_pole / ghost_device / ghost_wall`. The patterns below that are not in the library are written per project when needed.
- **Outlines and prisms:** `rounded_poly([[p, r], …])` (per‑vertex radius, convex and concave corners), `chamfered_prism(h, c_bot, c_top)` — a hull of inset slabs, **convex outlines only**; a non‑convex item is a union of convex chamfered prisms with concave fillets where they meet (the example's pocket, back plate and inside fillets). Fillet budget: two fillets on one edge need 2·r ≤ the edge length — guard it before generating the polygon (arcs that cross give a mesh with inverted faces, "not watertight" with zero open edges). Polyhedra: triangles only (quads crash CGAL 2021.01), winding clockwise seen from outside; look at one preview after writing one.
- **Transform bookkeeping:** `rotate([90, 0, 0])` maps (x, y, z) → (x, −z, y); `rotate([−90, 0, 0])` maps (x, y, z) → (x, z, −y). A feature built with the wrong one ends up buried inside its host and passes every check — verify that a feature exists with a section 1 mm in front of its host face (T19).
- **Edges:** swept edge profiles along an outline (`sweep_edge_line`, `sweep_edge_arc` with a fillet or chamfer profile) need r ≥ band width + 0.5 at every convex corner — perfect on smooth outlines, useless on stepped ones; a profile swept round a closed outline also runs along the buried back edge (give each run a flag or use a symmetric profile). For stepped outlines: a drafted core (`linear_extrude(h, scale = [sx, 1], slices = 1)` — without `slices = 1` a pure scale is cut into ~100 slices) plus inset 2D slices per face for the rounding; keep slices and `$fn` modest (8 slices × $fn 40 gave 90 k triangles — too big, §10.1 size budget). A full round on a thin plate edge = `hull(plate whose edge stops r short, rod of radius t/2 with 45° coned ends)`.
- **Revolved shapes:** build the profile as an explicit polygon — a 2D `intersection()` inside `rotate_extrude` gave an 858‑body mesh; Manifold silently accepts a profile crossing the axis that 2021.01 refuses (check the native log for ERROR).
- **Holes and features:** `teardrop_hole(d, l)` with a true point at the apex, `flat_top_hole`, `vertical_hole` adding `hole_clr`, `cone_roof_bore`, `nut_trap` / `kit_nut_well`, `kit_counterbore`, `hex_grid`, `drain_hole` (chamfered), `flared_cutter` for openings with a bottom flare and a top lead‑in, `brim_ear`, `tab()` / `slot()` (§9.4), detents copied from a standard recorded as a deviation.
- **Previews and cutters:** `ghost_tube`, `ghost_pole`, `ghost_device`, `ghost_wall`; every cutter clipped to its target region (§6.2).

### 7.6 Defaults
The defaults live in `scad/common.scad` (MSF Guideline V1.1, Hydra Research, DIN/ISO for the kit hardware, project values). Copy the file next to the part and include it; tune values only after a coupon or first article, and record what was confirmed. Values are starting points, not guarantees.

### 7.7 Customizer file — one file, exact header (MSF customizer standard, owner, Sept 2026)
Every part ships its working file and `<item>_customizer.scad`, one self‑contained file that opens unchanged in the OpenSCAD desktop Customizer and in the MSF customizer web catalogue. **Its first five lines are exactly:**
```openscad
// @name: <title>
// @description: <what the part is for and what equipment it fits>
// @category: <catalogue tab>
// @credit: <who made the model, or where it came from>
// @license: <the real licence>
```
In this order, one space after `//` and after the colon, a value on each line, nothing else on them; then a blank line. No sixth `@` line anywhere, no reordering, no other spelling — **no variations**. A Customizer file without this header is never shipped. Only the Customizer file carries it; the working file and every other `.scad` carry none. `@license` is the real licence of the design: **MIT** for a new MSF design (the MSF3Dprinting repositories are MIT); an adapted design keeps its source's licence, and a source licence that forbids the use is an open question for the advisor. This line is the only licence text in the package (§8.3).

`tools/flatten_scad.py part.scad --out part_customizer.scad --verify` builds the file: the five header lines (from `--name --description --category --credit [--license]` the first time, then reused from the existing file), a provenance comment, the design summary, the part's Customizer parameters with their groups, then `/* [Hidden] */` with `facets` (the working file's `fn_export`) and every library value (group headers turned into comments), then the part's derived values, validation, modules and build, then the library modules. It refuses to write without all five values. `--verify` exports both files and fails if the geometry differs (T22); non‑literal parameters fail. `export.sh` regenerates the file at every export and runs `lint_customizer.py` on both files; keep the working file the source of truth and never edit the Customizer file by hand.
