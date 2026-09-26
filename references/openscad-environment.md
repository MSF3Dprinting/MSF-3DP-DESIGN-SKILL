# OpenSCAD environment, versions and coding conventions

*Reference file of the `msf-3dp-design` skill. Read it before the first render of a session and before writing any .scad file.* Section numbers (§) are those of the compiled workflow file (CLAUDE.md v1.2) and are kept so that cross-references stay valid: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · Appendix A glossary.md · Appendix C sources.md.

## 6. OpenSCAD environment and versions

### 6.1 Which OpenSCAD — and how fast
As of September 2026 the last *stable* release of OpenSCAD is still **2021.01**; every speed and feature improvement lives in the **development snapshots** (2025.x / 2026.x). Since the 2024.09.28 snapshot the **Manifold** geometry engine is available and since August 2025 it is the default. The difference is not cosmetic — measured in this sandbox on real MSF parts (September 2026):

| Model | Triangles | Native 2021.01 (CGAL) | 2025.07 wasm, CGAL | 2025.07 wasm, **Manifold** |
|---|---|---|---|---|
| Example wall pocket (rounded box, teardrop holes, drain) | 2568 | 2.6 s | 8.9 s | **0.7 s** |
| Cube − sphere − 6 cylinders (benchmark) | 3536 | 2.7 s | 6.7 s | **0.7 s** |
| Tolerance coupon, 7 holes + debossed digits | 6200 | 24.8 s | 49.1 s | **1.1 s** |
| Hex‑perforated wall pocket 90 × 40 × 110, both walls | 5954 | 4.2 s | 19.1 s | **0.8 s** |

The engine makes the difference (wasm‑CGAL is *slower* than native CGAL; wasm‑Manifold is 4–22× faster than both). A 50‑case sweep drops from ~10 minutes to ~1 minute; text and perforations, which cripple CGAL, become cheap.

| Who | Version | Notes |
|---|---|---|
| You (Claude), all geometry export in the sandbox | `openscad-fast` — OpenSCAD 2025.07.18 with Manifold, from the npm package `openscad-wasm` (§6.4) | STL / 3MF / OFF only; no PNG (no OpenGL in wasm) |
| You (Claude), PNG views | native 2021.01 from apt, preview mode via `render_views.py` | preview (OpenCSG) is fast; `--full` forces a CGAL render only when needed |
| Advisor and designers on their own computers | the current development snapshot from openscad.org → Downloads → Development Snapshots (Windows, macOS, Linux); macOS `brew install openscad@snapshot`; Manifold is on by default | the MSF customizer server needs 2023.09 or newer for Manifold (its README) |
| Field laptops that only open the Customizer and export STL | any version ≥ 2021.01 | slow CGAL render, but works; recommend a snapshot |
| **Language level of every `.scad` you write** | **2021.01** | so every install opens it: no `roof()`, `textmetrics()`, `fontmetrics()`, colour export, object literals; `assert()`, `$preview`, `is_undef()`, function literals, `offset()`, `text()` are fine |

Put `assert(version_num() >= 20210100, "OpenSCAD 2021.01 or newer is required");` in `common.scad` (below the parameters) and record the exporter version in `stl/EXPORT_LOG.txt` and the DATASHEET.

### 6.2 Backend and speed
- `openscad-fast` always runs Manifold. Snapshots from August 2025 on: Manifold is the default; older snapshots: Preferences → Advanced → 3D Rendering → Backend = Manifold, or `--backend=manifold`. 2021.01: CGAL only.
- Keep `$fn` behind `facets` (Hidden) so smoothness can be traded for speed; preview low, export ≈ 96. Build shapes from 2D profiles — `offset()` then `linear_extrude()` — rather than 3D hulls of cylinders; avoid `minkowski()` (a `hull()` between two extruded profiles gives the same chamfer far more cheaply); prefer one `difference()` with many children over nested differences.

**Boolean hygiene (2021.01 / CGAL).** Never let a cutter's face coincide with the face it cuts, and never let two cutters meet on a shared plane or share a tangent line: extend cutters 0.2 mm into the void, overlap neighbouring cutters by 0.05 mm, make a chamfer 0.01 mm larger than a fillet of the same nominal size. Clip every cutter to the region it is meant to cut — a chamfer cutter wider than its channel once shaved the tops of two walls and left a crevice that every automated check missed. Build a chamfered base in a single `hull()` of all its pieces. The symptom of bad booleans is an STL that passes every overhang test and fails watertightness or has two‑face "bodies" (T4); the sweep finds the values that trigger it. Manifold is more tolerant of coincident faces than CGAL, but the flat Customizer file must still render in 2021.01 — keep the hygiene.

### 6.3 Command line (what you run)
```bash
# geometry export — Manifold, seconds (same arguments as openscad; PNG not possible here)
tools/openscad-fast -o stl/part_holder_v1.0.stl --export-format binstl -D 'part="holder"' -D 'wall_t=2.7' part.scad
tools/openscad-fast -o stl/part_large_v1.0.stl -p part.json -P large part.scad
# PNG views — native 2021.01 in preview mode, headless (render_views.py wraps this in xvfb-run and makes the sheet)
python3 tools/render_views.py part.scad --out img --name part --context part_context.scad
# a single full CGAL render image, only when a preview artefact must be ruled out
xvfb-run -a openscad -o img/part_full.png --render=true --viewall --autocenter --projection=o --camera=0,0,0,90,0,0,500 part.scad
```
Standard cameras: front `90,0,0`, side `90,0,90`, top `0,0,0` (orthographic), isometric `55,0,25`. Documentation scenes: wrap parts in `render()` before `color()`; explicit `--camera` when stand‑ins are long; render 2× and downsample; re‑save without EXIF — `render_views.py` does all of it.

### 6.4 In the Claude sandbox (empty at the start of every conversation)
`bash tools/install_openscad.sh` does everything below; know what it does:
1. `rm -f /etc/apt/sources.list.d/nodesource*` — that repository returns 403 and breaks `apt-get update`.
2. `timeout 600 bash -c 'apt-get update -qq && apt-get install -y --no-install-recommends openscad xvfb'` in the foreground — background installs are killed when the tool call returns. Native 2021.01 (CGAL) is used only for PNG views (`xvfb-run -a`).
3. `pip install trimesh numpy scipy shapely rtree pillow --break-system-packages`.
4. **Fast exporter:** `npm install --prefix "$HOME/.openscad-wasm" openscad-wasm@0.0.4` (npmjs.org is on the sandbox allow‑list; `files.openscad.org` is not) and the wrapper `tools/openscad-fast` → `openscad_manifold.mjs`, which mounts the part's folder into the wasm file system so `include <common.scad>` resolves, runs with `--backend=manifold` and writes the STL back. `export.sh`, `sweep.py` and `flatten_scad.py --verify` use it automatically when it is present and fall back to native `openscad` when it is not.

Shell facts: one tool call is limited to 300 s — run sweeps detached (`setsid nohup python3 tools/sweep.py part.scad --check > tools/sweep_report_<date>.txt 2>&1 < /dev/null &`) and poll; `/bin/sh` has no `time`, `disown` or brace expansion (`mkdir -p d/{a,b}` makes a literal folder) — use `date +%s`, `setsid nohup`, explicit paths or `bash -c`; pass absolute paths to `-o`; OpenSCAD silently ignores `-D` for a parameter that does not exist, so check names before a sweep or a guard test (`sweep.py` refuses unknown names). GitHub clones work; Printables model pages fetch, their images do not.

### 6.5 Libraries and fonts
- Dependency‑free by default. Use BOSL2 only when the system you must match already uses it (HomeRacker `support.scad`); then vendor the library at a pinned version and say so in the README.
- Font: **Liberation Sans**, bundled with OpenSCAD (`font = "Liberation Sans:style=Bold"`). Measured in 2021.01: capital height ≈ 0.96 × size, stroke ≈ 0.2 × size — size 5 gives 4.8 mm capitals and 1.0 mm strokes. Other scripts need a font that supports them; keep strings as parameters.
- Measuring string widths: in 2021.01 export the 2D text to SVG (`openscad -o t.svg -D 'S="TEXT"' measure_text.scad`) and read the extents with a few lines of Python; in snapshots use `textmetrics()` with `--enable=textmetrics`. Size plates for the longest string, with stated margins, before fixing plate sizes.

### 6.6 Slicer
PrusaSlicer 2.9.x is the MSF reference (kit). Give the settings in the README (§5.5). The user confirms orientation, "no supports", print time and filament use in the slicer before printing.


## 7. OpenSCAD conventions

### 7.1 File layout (every `.scad`)
0. Catalogue header lines, first in the file: `// @name: <title>`, `// @description: <one sentence>`, `// @category: <catalogue tab>`, `// @credit: MSF 3D Printing for All` (the MSF customizer standard; no `@license` line — internal).
1. Design header (§7.4).
2. `assert(version_num() >= 20210100, …)`.
3. Customizer parameters in `/* [Group] */` blocks, in this order where they apply: `[Part selection]`, `[Main dimensions]`, `[Interface / fit]`, `[Mounting]`, `[Printability]`, `[Text]` (non‑clinical only), `[Preview]`, `[Hidden]`.
4. `// ===== Derived values =====` — computed values, clearly separated from user parameters; any derived value a user may need to override has an override parameter.
5. `// ===== Input validation =====` — `assert()` with plain‑language messages.
6. Modules: helpers (§7.5), features, part modules, ghost modules.
7. Main build: the `part` selector; ghost parts behind `if ($preview && show_ghosts)`.

### 7.2 Customizer rules
- Every parameter is a **literal** (a number, `true`/`false`, a quoted string or a vector) — never an expression or another variable, which the Customizer cannot show. It has units (mm; degrees), a one‑line help comment on the line above (the customizer shows it), and a range with step or a dropdown: `wall_t = 1.8; // [1.6:0.1:4]`. Menus: `part = "insert"; // [insert, floor, both]`, readable labels `// [screw:Screw hole, adhesive:Adhesive pad]`, text boxes `// 12`. The parameter block ends at `// ===== Derived values =====`; everything below it is not a control.
- Every functional dimension is user‑definable — grip, wall, hole, clearance — never only auto‑derived from another value. Derived values live in their own section below.
- Selections are menus, not extra files: export selector; per‑side toggles (left/right wing, solid/perforated per wall).
- Validate with `assert()` and clear messages ("Recess is only allowed for thickness 3.5–5 mm and plates of 3 units or more"); fail loudly instead of producing broken geometry.
- `$fn`, `$fa`, `$fs` are parameters: low for preview, high enough for export that holes and fillets are faithful (`fn_export = 96; fn_preview = 32; $fn = $preview ? fn_preview : fn_export;`).
- Text strings are parameters. Colours are set by the filament at print time — models never specify colours; each colour band is its own module so the preview shows it.
- Asserts on derived floats use a tolerance (`>= x - 0.001`); `2.7 >= 2.7` has failed. Guards refuse only physically impossible combinations; where the geometry can adapt (a channel wider than its sleeve merging with the sleeve sides), adapt instead of refusing. The default parameter set must itself pass every guard — T1 at defaults is the first test.
- Choose ranges so that each extreme renders with the other parameters at their defaults wherever the geometry allows; narrow a range that always fails at one end (`roof_deg` 40–45). A guard stopping an extreme is a pass, reported as such.
- A parameter does what its name says. Never offer a setting whose name promises an effect the geometry cannot deliver (`latch_extra` on a catch too short to flex was removed).
- Documentation views come from a preview‑only `scene` parameter (`none, print, installed, exploded, section`) guarded by `assert($preview, …)`; colours only inside scene modules, so nothing decorative can reach an STL.
- Any open‑top pocket, holder or socket that can collect fluid carries `drain_d` (§8.1); any tall or narrow part carries `brim_ear_d` (§5.1).

### 7.3 Structure and naming
- One model produces one item; copies are made in the slicer. One parametric file per item family; variants by a string parameter (`role`, `type`, `part`, `version`).
- Multi‑item sets: `common.scad` holds shared values (layer and band heights, minimum sizes, clearances, font, shared dimensions such as the bed) and helpers; models `include <common.scad>` and never copy its values; dependent dimensions are derived there (screen height = bed height + 10 mm), never retyped. Shared shapes go in a small library file (`bucket_lib.scad`, `pictogram_lib.scad`).
- Names in `snake_case` with suffixes: `_d` diameter, `_r` radius, `_t` thickness, `_h` height, `_w` width, `_l` length, `_clr` clearance, `_n` count, `_deg` angle. Comments say *why* — the rule or the measurement behind a value.
- Ghost or mating parts (frame, back part, pole, device) with the `%` modifier so fit can be judged in preview; they never appear in the export.
- Model in print orientation; Z = 0 is the bed. Never rotate the exported geometry for looks.
- When a sub‑shape can be rotated or offset by a parameter, the geometry that connects to it follows the transformed shape (a tilted channel once cut its wall to 0.1 mm); always render the extreme angles and offsets in the sweep.
- Context scenes live in `<item>_context.scad`: `use <item.scad>` (modules without the top‑level build) plus generic stand‑ins sized to the interfaces (panel, wall, rail, pole, device) labelled "illustration only" — never exported.

### 7.4 Design header (top of every file)
```openscad
/* ===== DESIGN SUMMARY =====
 * Part / purpose:    <what it does, where it is used>
 * Version:           <x.y> <date>   Designer: <name>
 * Critical part:     no | yes / unsure -> draft for review
 * Material:          PETG (white/natural/light) | PLA | TPU | PC | PP-GF  (reason)
 * Environment:       <temperature, chemicals, outdoor, disinfection method>
 * Loads:             <type and direction; layer orientation chosen accordingly>
 * Print orientation: <face on the plate>; supports: none | built-in at <where>; brim: yes/no
 * Mating hardware:   <bolts/nuts/inserts/zip ties and sizes>
 * Fits used:         <free/tight, printed-printed / printed-machined; clearance values>
 * Interfaces:        <what it fits, diameters, measured values and the source of each>
 * Unverified values: <placeholders that must be measured before printing, or "none">
 * Flags:             <> 50 C, watertight, smooth surface, chemicals, mains housing, user contact, sterilisation>
 * Deviations:        <any rule in sections 5, 8, 9 not met, and why>
 * Verified:          <render OK, manifold, worst overhang x deg, bbox ..., OpenSCAD version>
 * Not verified:      <physical print, load test, ...>
 * Approval:          <Biomed + IPC | lab advisor | line manager>
 * ========================== */
```

### 7.5 Standard helpers (dependency‑free)
`scad/helpers.scad` implements: `rounded_rect`, `rounded_poly`, `teardrop2d`, `hex_grid`, `chamfered_prism`, `rounded_box`, `section_cut`, `vertical_hole`, `teardrop_hole`, `flat_top_hole`, `cone_roof_bore`, `nut_trap`, `drain_hole`, `brim_ear(s)`, `corner_ears`, `breakaway_support`, `tab`, `slot`, `ghost_tube / ghost_pole / ghost_device / ghost_wall` — include it next to the part. The patterns below that are not in the library (swept edge profiles, chamfer caps, detents) are written per project when needed; reference implementations exist in `pulse_oximeter_holder_ums.scad` v1.1, the tap‑lever pusher and the D‑shaft knob.
- **Outlines and prisms:** `rounded_poly([[p, r], …])` (convex and concave corners, rotation and offsets), `inset()`, `chamfered_prism(z0, z1, c_bot, c_top)` — a hull of inset slabs for convex outlines; for non‑convex outlines a triangulated polyhedron with a 45° bottom chamfer, no minkowski. Polyhedra: **triangles only** (quads crash CGAL 2021.01), winding clockwise seen from outside, every convex radius ≥ chamfer + 0.1 mm, consecutive fillet tangent lengths must fit on the edge; look at one preview after writing one (inside‑out faces export fine and show nothing).
- **Edges:** `sweep_edge_line(p0, p1)` and `sweep_edge_arc(centre, R, a0, a1)` with `edge_profile_fillet(r)` / `edge_profile_chamfer(c)` — the profile starts 0.2 mm inside the void and ends r + 0.01 into the material; `chamfer_cap(z_top, c)` (minkowski of the inset outline with a cone, for non‑convex outlines; extend the outline into the wall it sits on, or a V‑groove appears at the junction); a swept U wall from one 2D cross‑section (`linear_extrude` runs, `rotate_extrude(angle = 90)` corners, `rotate_extrude(angle = 180)` full‑round ends); a full round on a thin plate edge = `hull(plate whose edge stops r short, rod of radius t/2 with 45° coned ends)` — a rod unioned onto an already chamfered edge does nothing.
- **Holes and features:** `teardrop_hole(d, l, angle = 45)` with a true point at the apex, `flat_top_hole(d, l)`, `vertical_hole(d)` adding `hole_clr`, `cone_roof_bore(d, depth)`, `nut_trap(af, h)`, `hex_grid(cell, wall, area)`, `wave_wall(...)`, `drain_hole(d)` (chamfered), `brim_ear(d, t)`, `tab()` / `slot()` (§9.4), `detent_dimple(R, sink)` / `detent_bump(R, h)` — small > 45° features copied from a standard are recorded as a deviation, not "fixed".
- **Previews and cutters:** `ghost_tube(d, l)`, `ghost_pole(d)`, `ghost_device(size)`; `yz_prism()` for cutters — every cutter clipped to its target region (§6.2).

### 7.6 MSF defaults block (copy into `common.scad`; tune after test prints)
```openscad
/* [MSF defaults - MSF Process Guideline V1.1 Parts 2-4; Hydra Research; project values] */
layer_h        = 0.2;    // [0.1:0.05:0.3] layer height, SPEED preset
ext_w          = 0.45;   // extrusion width with a 0.4 mm nozzle
clr_free_pp    = 0.3;    // [0.2:0.05:0.5] sliding fit, per side, printed-printed (MSF: >= 0.6 total)
clr_free_pm    = 0.15;   // sliding fit, per side, printed-machined (MSF: >= 0.3 total)
clr_tight_pp   = 0.15;   // tight fit, per side, printed-printed (MSF: 0.3 total)
clr_tight_pm   = 0.075;  // tight fit, per side, printed-machined (MSF: 0.15 total)
clr_dropin     = 0.8;    // loose drop-in, removable for cleaning (vaccine carrier floor)
hole_clr       = 0.2;    // added to vertical hole diameters
min_wall       = 1.6;    // MSF minimum wall
struct_wall    = 4 * ext_w; // 1.8 mm, four perimeters
min_base       = 2.0;    // base of flat parts
min_handle     = 2.4;    // handled protrusions, both directions
min_hole_v     = 1.5;    // vertical hole diameter
min_pin_d      = 1.8;    // pin diameter
max_bridge     = 10;     // avoid bridges; hard limit if unavoidable
max_overhang   = 45;     // degrees from vertical (60 only where the brief allows)
chamfer_bottom = 0.4;    // elephant's foot
chamfer_top    = 0.8;    // [0.6:0.1:1.0] exposed edges
fillet_min     = 1.0;    // internal corners, IPC
base_corner_r  = 4;      // vertical edge radius at the plate where the footprint allows
bolt_wall      = 2.5;    // material around bolt holes (four to five perimeters)
max_part       = [200, 200, 200];
min_thread_d   = 10;     // modelled threads only above this diameter ...
min_thread_p   = 1.5;    // ... and this pitch
tap_factor     = 0.90;   // hole for tapping (Hydra)
selftap_factor = 0.96;   // hole for a self-tapping screw (Hydra)
insert_factor  = 0.98;   // hole for a heat-set insert (Hydra)
font           = "Liberation Sans:style=Bold";
text_size_min  = 6;      // letter height (MSF > 6 mm); training set used size 5 (4.8 mm capitals)
text_depth     = 0.8;    // [0.6:0.1:1.0] emboss/deboss depth
band_base      = 2.0;    // colour band base
band_min       = 3 * layer_h; // 0.6 mm per colour
nfc_pocket     = [19, 19, 1];
drain_d        = 6;      // [0:1:12] drainage hole in closed floors, 0 = none (blind sockets >= 2)
brim_ear_d     = 0;      // [0:1:15] built-in brim ears for tall or narrow parts, 0 = none
overhang_tol   = 0.05;   // degrees, float32 STL rounding on exact 45 deg faces
```
Values are starting points, not guarantees — validate with a test print.

### 7.7 Customizer one‑file version (MSF customizer standard)
Every part ships twice: the working file (`<item>.scad`, includes `common.scad` and `helpers.scad`) and `<item>_customizer.scad`, one self‑contained file that opens unchanged in the OpenSCAD desktop Customizer and in the MSF customizer web catalogue, whose `include` resolves only against its own library folder. `tools/flatten_scad.py part.scad --out part_customizer.scad --verify` builds it: catalogue header lines first, the design summary, the part's Customizer parameters with their groups, then `/* [Hidden] */` with `facets` (drives `$fn`) and every library value (group headers turned into comments), then the part's derived values, validation, modules and build, then the library modules. `--verify` exports both files and fails if the geometry differs (T22). The flattener warns about any parameter that is not a literal. Keep the working file the source of truth; regenerate the flat file at every export.

