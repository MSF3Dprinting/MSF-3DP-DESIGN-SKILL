# Verification — required tests before shipping

*Reference file of the `msf-3dp-design` skill. Read it before any STL or package is delivered, and when planning the physical tests.* Section numbers (§) are those of the compiled workflow file (CLAUDE.md v1.2) and are kept so that cross-references stay valid: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · Appendix A glossary.md · Appendix C sources.md.

## 10. Verification — required tests before shipping

Nothing ships until every test below has a recorded result. Report them in the hand‑off as a table: test · result · evidence (file or number) · pass / fail / n.a. Physical tests (§10.4) are done by the user; you write the protocol and record what came back.

### 10.1 Automated tests (you run them in the sandbox)

| # | Test | How | Pass |
|---|---|---|---|
| T1 | Render at defaults, then every variant | `openscad -o … --export-format binstl` at the default parameter set first, then each `part` / `type` value and preset | Exit 0; no WARNING or ERROR in the log; the defaults pass every guard |
| T2 | Parameter sweep | Render at the min and max of every ranged geometric parameter with the others at default, plus the extreme angles and offsets of any movable sub‑shape; check first that every parameter named in the sweep exists (OpenSCAD ignores unknown `-D`); run detached and save `tools/sweep_report_<date>.txt` with PASS / GUARD (message) / FAIL (reason) per case | Every case renders or a guard stops it with its message; no FAIL |
| T3 | Guards | Out‑of‑range values and invalid combinations, names checked as in T2 | `assert()` stops with its plain‑language message; no over‑strict guard (a range end that fails at defaults is a bug) |
| T4 | Manifold / watertight | `check_stl.py`: trimesh `is_watertight`, `is_volume`, body count | Watertight; one body per intended part; positive volume — this is the test that catches boolean artefacts |
| T5 | Bounding box | `check_stl.py` against the brief | Within 0.1 mm; ≤ 200 mm per axis, or split |
| T6 | Print position | min Z = 0 ± 0.01 mm; the STL is in its print orientation with nothing to rotate; bed‑contact area as % of the footprint | Sits flat, ready to slice; narrow footprints get brim ears |
| T7 | Overhang scan | `check_stl.py`: for every downward‑facing facet above the bed, angle from vertical = asin(−n_z); tolerance 0.05° (float32 STL rounding); ignore facets at Z ≈ 0 and below 0.001 mm² (CGAL slivers); run once at `--min-area 0.5` and once at `--min-area 0.02` for small ledges and sheets | Worst sloped angle ≤ 45° (≤ 60° only where the brief allows); report the worst angle and where |
| T8 | Bridges and unsupported spans | Horizontal downward faces above the bed listed separately with their XY extent; teardrop tips excluded | None, or each < 10 mm, documented and accepted with `--allow-bridges` |
| T9 | Minimum features | Customizer values against §5.2; minimum wall along Z computed in the model (`echo`), reported as modelled and as printed once coupon values are applied; spot check of the preview | All at or above the minimums, or a recorded deviation |
| T10 | Hole compensation | Horizontal holes teardrop or flat‑top; vertical holes carry `hole_clr` | Yes |
| T11 | Ghost parts and scenes excluded | Export with defaults and with `scene` at each value | STL contains only the part; scene values other than `none` are refused by the guard |
| T12 | Colour bands (banded parts) | Band heights on 0.2 mm steps; base ≥ 2.0; each colour ≥ 0.6; nothing else crosses a boundary | Yes |
| T13 | Text fits (non‑clinical) | Measured string width + margins ≤ plate | Yes |
| T14 | Render set | `render_views.py` (preview mode, 2× downsampled): front, top, side (orthographic), isometric, context of use with the wall / rail / pole / device as stand‑ins, cut‑through of the functional zone, extremes (min / max), coupon, and a captioned overview sheet; misalignment views where T20 applies; exploded view where there is an assembly | Produced; you look at the sheet once; the sheet is the README picture; no stand‑in in any STL |
| T15 | Slicer dry run (when PrusaSlicer runs) | `prusa-slicer --info`; with a profile, `--export-gcode` for time and filament | Manifold OK; no supports needed; time under 48 h |
| T16 | Documentation and data | Header complete (§7.4); README complete (§11.2) including test‑before‑use and acceptable materials; deviations, flags, tapers, clearance directions and unverified values listed; no personal data in any file, file name, render or comment (§1.5) | Yes |
| T17 | Pre‑export checklist (§10.3) | Walk it | Every box ticked or explained |
| T18 | Interface identity (copied interfaces) | Cross‑sections of the exported STL compared with the reference file at ≥ 5 heights | Widths, depths and detents agree within 0.05 mm |
| T19 | Section check | Slices at several Z heights through the functional zone and at one edge of each type (vertical fillet, horizontal chamfer, sloped chamfer, hole) | Each slice is one piece; smallest wall ≥ 1.6 mm; edge sizes as the brief promises |
| T20 | Clash test (moving or misaligned mating parts) | Intersect the part with the ghost mating part at every tolerance case (lean, shift, angle, tilt, combinations) | Empty = clear, 0 mm³ = touching, > 0 = clash; envelope table in the README, no clash inside the stated envelope |
| T21 | Overlay check (source is a photo or drawing) | Section of the exported STL at the seating height drawn over the anonymised, scaled, straightened image | Topology matches; every deviation explained by a written dimension or a recorded interpretation; image delivered |
| T22 | Customizer one‑file identity | `flatten_scad.py part.scad --verify`: both files exported with the same engine and compared | Same volume (±0.2 %) and size (±0.01 mm); no non‑literal parameter warnings |
| T23 | Copies | For every `xN` variant the numbered files exist and are identical | N files, one per item |

### 10.2 The check tooling — shipped with this skill in `scripts/`, copied into the project's `tools/`
All scripts are universal — they read the mesh or the Customizer, never the design — so the same files serve every product.

| Script | Does | Typical call |
|---|---|---|
| `check_stl.py` | T4 – T8, T19 on any STL: watertight, bodies, bbox, print position, bed‑contact %, sloped overhangs (tolerance 0.05°, slivers < 0.001 mm² ignored) and horizontal downward faces reported separately, per‑section piece count and wall thickness measured along inward normals; exit 1 on failure; `--json` | `python3 tools/check_stl.py stl/part.stl --sections 5,20 --min-wall 1.6` then a second pass `--min-area 0.02`; `--allow-bridges` for documented ledges; `--single-piece` when the zone must be one piece |
| `sweep.py` | T1 – T3: parses the Customizer ranges and dropdowns, renders the defaults first, then every extreme with the others at default; PASS / GUARD (assert message) / FAIL; refuses unknown parameter names; `--check` runs check_stl on every PASS | `setsid nohup python3 tools/sweep.py part.scad --check --sections 20 --report tools/sweep_report_$(date +%F).txt > /dev/null 2>&1 < /dev/null &` then poll |
| `render_views.py` | T14: front / top / side (orthographic), isometric, and `--context` installed / exploded / section scenes; headless via xvfb‑run; 2× render downsampled; no metadata; captioned sheet | `python3 tools/render_views.py part.scad --out img --name part --context part_context.scad` |
| `overlay_sketch.py` | T21: section (`--z`) or silhouette (`--view`) of the exported STL drawn over the anonymised photo or sketch; `--calib` gives px/mm from two points | `python3 tools/overlay_sketch.py photo.png --stl stl/part.stl --z 3 --scale 18.4 --origin 700,500 --rot 12 --out img/part_overlay.png` |
| `export.sh` | Every variant from `variants.txt`: STL in print position via `openscad-fast` (Manifold) when installed, `xN` copies as numbered files, check_stl, render set, coupon, `stl/EXPORT_LOG.txt`; exit 1 on any failure | `SECTIONS=20 COUPON=test_coupon.scad bash tools/export.sh part.scad 1.0 variants.txt part_context.scad` |
| `openscad-fast` | OpenSCAD 2025.07 with the Manifold engine (npm `openscad-wasm`), same arguments as `openscad` for geometry export; 4–22× faster than 2021.01 CGAL | `tools/openscad-fast -o stl/part.stl --export-format binstl -D 'part="holder"' part.scad` |
| `flatten_scad.py` | One‑file Customizer version per the MSF customizer standard; `--verify` compares the geometry (T22) | `python3 tools/flatten_scad.py part.scad --out part_customizer.scad --name "…" --category "…" --verify` |
| `install_openscad.sh` | Sandbox setup: apt OpenSCAD 2021.01 + xvfb, python tooling, optional snapshot | `bash tools/install_openscad.sh` |
| `test_coupon.scad` (scad/) | Universal tolerance coupon: round / square / rect / slot / D‑shaft openings at stepped clearances, numbered row + lettered row, deboss or notch labels | `openscad -o stl/part_coupon_v1.0.stl -D 'feature="dshaft"' -D nominal=6 -D flat=4 test_coupon.scad` |

### 10.3 Pre‑export checklist
- [ ] Not in §4.1; if restricted, every §4.1b condition met and recorded; criticality and advisor flags set
- [ ] ≤ 200 × 200 × 200 mm, or split with alignment features
- [ ] Modelled in print orientation and exported in print position; large flat face on the plate or brim ears; base edges chamfered or rounded
- [ ] No overhang > 45° from vertical without planned built‑in support; no bridges (or < 10 mm, documented)
- [ ] Walls ≥ 1.6 mm (structural ≥ 1.8 mm); vertical holes ≥ Ø1.5 mm + 0.2; pins ≥ Ø1.8 mm
- [ ] Horizontal holes compensated; clearances match fit type and mating material; each is a parameter
- [ ] Threads only if Ø > 10 mm and pitch > 1.5 mm; otherwise inserts, nut traps or tapping
- [ ] Hardware sizes are parameters and match kit or local hardware
- [ ] Loads run along the layers; strength holds at 2 perimeters / 15 % infill (§5.5); enough material around bolt holes; flexing features ≥ four perimeters and within the strain limit
- [ ] Acceptable materials listed from what is on the shelf; the geometry does not depend on one material; clinical → light colour
- [ ] Clinical: no text or recesses; cleanable surfaces; no sharp edges; removable parts for cleaning; drainage hole in every closed floor (or the brief says why not)
- [ ] Every cutter clipped to its target; no coincident faces — T4 clean at every sweep case
- [ ] Render set complete (front, top, side, isometric, context, section, sheet); coupon exported alongside the part
- [ ] Failure consequence and test‑before‑use protocol in the README
- [ ] Non‑clinical text: sans‑serif, size per §9.2, 0.6–1 mm deep
- [ ] As simple as possible; modular if complex; print time estimated
- [ ] Header and README complete, including deviations and unverified values
- [ ] Verification table filled in
- [ ] No personal data in any file, file name, render, comment or log (§1.5)

### 10.4 Physical tests (the user prints; you write the protocol)

**Coupons travel with the product.** The coupon is designed in the same stage as the part and shipped in the same package; it prints in 10–40 minutes; the user replies with its code ("B4"); the value is entered as a parameter; then the part is printed. Never make the product wait for the coupon, and never mark a fit confirmed before the coupon or the first article says so.

| Test | When | What the user prints and reports |
|---|---|---|
| Tolerance coupon | Any new fit, new material or new printer | A flat plate printed in the part's orientation with the mating feature at stepped clearances, bottom chamfer and top lead‑in on every hole, steps marked by digits and letters (debossed size ≥ 6.5, 0.6 mm — a non‑clinical test piece) or by notches. Range by fit type: **sliding** −0.1 to +0.8 mm in 0.1 steps; **tight or push‑on onto a machined part** 0.00 to +0.30 mm per side in 0.05 steps; **clearance features** (counterbore over a bushing, nut or head) +0 / +0.2 / +0.4 on the diameter; **push fit on rusty or variable metal** three holes at 0.075 / 0.15 / 0.25 mm per side marked by 1–3 notches, plus "wire‑brush the tube end" in the assembly steps; **tapered bores** straight rings, one clearance per ring. The reply is the step code |
| Interface coupon | Any copied interface (UMS socket, HomeRacker) | The interface only (`part = "socket_test"`, ≈ 40 min): checks the site's printer, not the geometry |
| Outline check plate | Any outline or slot positions not measured with calipers (§3.6, §3.4 e) | The part outline at full thickness with windows at the openings and the tabs that enter them, ≈ 10 min. Report: drops in without force, gaps under 0.5 mm, windows over the openings |
| Overhang / colour coupon | Overhangs above 45° allowed by the brief; colour bands; a light colour over a dark base | Report drooping and tinting |
| First article | Every new design | Print at the README settings; measure the critical dimensions the README lists; fit it to the real device; photos; feedback questions (§2.5) |
| **Test before use** | Every item — the README carries a protocol proportional to the risk | Function: does what it must, 10 cycles (attach, load, remove; slide, latch). Fit: no rattle, no forcing, the device stays put. Cleaning: wipe with the site agent, look for residue in corners. Edges: nothing sharp on skin or glove. The approver signs the result |
| Load test | Every load‑bearing part (§4.1c) and any holder for more than 2 kg | Static: part on a bathroom scale, load through a steel rod of the mating diameter to 2 × the design load, hold 1 min, 3 times. Rolling or functional: 20 cycles over a 10–15 mm doorstep or the equivalent use. Pass: no cracks, no white stress marks, no deformation, no wobble, hardware in place |
| Drop test | Anything that can fall onto a floor or a person | The loaded part dropped from its mounting height onto concrete, 3 times; no fragments, no sharp break, still holds |
| Test to failure (not always) | Critical items; batches of 10 or more; anywhere the limit matters (owner decision, September 2026) | One sample loaded to failure the way it is loaded in use: increase in steps, note the load at the first crack and at break, the failure mode, and whether it failed safe. Set the stated working limit at ≤ ⅓ of the failure load (default) and record load, mode and a photo in the README. Skip it for low‑load, non‑critical items — say why |
| QC per README | Every production part | Visual · dimensional · fit/tolerance · safety validation by the approver |
| Follow‑up after installation (minimum standard) | Every installed item; more often for critical items | Installation day · + 2 weeks · + 1 month · + 3 months (critical items: + 6 and + 12 months, then every 6 months): cracks, whitened areas, loosening, wear at contact points, hardware tight, latches flexible, surface cleanliness, still in intended use; at 3 months the decision keep / reprint / redesign. Each visit recorded in the README table and validated by the 3D printing advisor (owner, Sept 2026) |

Record confirmed values in a "Confirmed by test print" table in the README and STATUS.md. A value is confirmed only after a physical result: a coupon confirms a clearance, the first article confirms the part.

