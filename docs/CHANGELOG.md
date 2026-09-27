# Changelog — msf-3dp-design skill

## 1.4.0 — 27 September 2026 (owner feedback 3, lessons from the tube drying holder and the pipe cross clamp, toolchain review)
- Workflow: a design review before documentation — the user approves pictures (render sheet, assembled view, section of the load-bearing zone) before any Customizer file, release STL, README or DATASHEET; the confirmation carries a concept card (principle, three numbers, what the answers exclude); rejected concepts are recorded and the requester's own idea asked for; questionnaire asks how it is done today, what may touch the item, whether the held item is soft.
- Customizer (owner): sliders for numbers, menus for every fixed choice, free text only for the user's own text, help text on the line above; several components → `part` menu with each part in print position, all parts on one print plate, and the assembled view. The Customizer file starts with exactly five lines (@name, @description, @category, @credit, @license — MIT for new MSF designs), only that file, never varied, never shipped without them. New `lint_customizer.py` checks it from OpenSCAD's own parameter export; `flatten_scad.py` writes and reuses the header; `export.sh` regenerates and checks the file every run.
- Strength (owner + pipe clamp): loads run along the layers, never pull them apart; fastener pattern, no bolt load into thin wings, V-apex material, boss sizing, adaptive corner radius; structural review T24 with section drawings (`section_from_stl.py`).
- Hardware (owner): MSF kit hardware first (stainless DIN 912 M3/M6 bolts, DIN 125A washers, DIN 985 and DIN 934 nuts) with its dimensions and `kit_bolt_for()` in common.scad; anything else exact, with two local alternatives and where it can be taken from — medical and non-medical sources listed, the staff decide. Replaces the M5 and heat-set-insert defaults.
- Soft or hollow parts (tube holder): ring-bending rule of thumb, four holding options, tube weights, hold limits in numbers.
- README credits Claude and the skill with its link for verification and accountability; the Customizer header's @license line is the only licence text in a package.
- Toolchain review (all confirmed by running the scripts): the fast exporter's messages carried a prefix, so warnings and the coupon table never reached the logs; the wasm build had no fonts, so coupon digits were missing (the v1.3 speed table's coupon row too); section checks never ran (networkx missing) yet reported PASS; executable bits were not in git; the skill's own files wrote help text after the Customizer spec, which kills the sliders. All fixed; scripts fail loudly. New `stl_clean.py`, `compare_meshes.py`, `sweep.py --resume/--merge`, `check_stl.py --sections auto / --view-only`, `render_views.py` section camera per axis and readable sheets.
- Library: `common.scad` kit hardware and `top_chamfer()`; `helpers.scad` `flared_cutter`, `kit_*` cutters, `print_plate`; example rebuilt as a two-part item (wall pocket + floor insert) that passes its own rules (45 of 45 sweep cases); coupon with a preset menu; context scene sized from the part.
- Speed table re-measured: openscad-fast is 4–28× faster than native 2021.01 (the v1.3 table said 4–22×).
- Docs: stale v1.2 references removed (Rounds, §3.2a, §2.5, staged plan); section numbers shared by every file; evals with checkable expectations (11 evals, a synthetic test photo); Claude Code facts (AskUserQuestion, tool limits, installation).

## 1.3.1 — 26 September 2026
- references/readiness-levels.md now holds the Humanitarian Making scale verbatim (all five scales, criteria and risk questions, as published) plus the MSF interpretation rules for risk and maker readiness.

## 1.3.0 — 26 September 2026 (owner feedback 2 after testing the package)
- Speed: `openscad-fast` — OpenSCAD 2025.07.18 with the Manifold engine from the npm package `openscad-wasm`, installable in the sandbox; measured 4–22× faster than native 2021.01 CGAL on MSF parts (table in references/openscad-environment.md §6.1). Used by export.sh, sweep.py and flatten_scad.py; native 2021.01 kept for PNG views (preview mode by default).
- Workflow: research → one front-loaded questionnaire (option-picker calls, nothing in between) → one confirmation → one build pass → one feedback round. Gates for intermediate documents removed; advisor sign-off kept for critical/restricted items.
- Clicking first: every discrete question through the picker; type-in only for measurements and names.
- Token discipline (SKILL.md §1.6): files not chat, sheet viewed once, quiet checks, detached sweeps, STATUS.md hand-over.
- Documents: README short and visual (parts table with pictures, context and exploded views, follow-up table); DATASHEET.md holds the full record; no licence, certification mark or badge anywhere.
- Readiness: Humanitarian Making scale only, verbatim, from references/readiness-levels.md.
- Customizer: every part also as a one-file version per the MSF customizer standard (`@name/@description/@category/@credit` header, literal parameters, `facets` in Hidden); `flatten_scad.py --verify` (T22).
- QC: follow-up after installation, 2 weeks, 1 month, 3 months minimum (critical: 6 and 12 months, then every 6 months), validated by the 3D printing advisor.
- Printability: brims and supports built into the model only when geometry cannot be changed (`corner_ears`, `breakaway_support` helpers); designs without them preferred.
- Export: N identical items → N numbered STL files (`variants.txt`: `rib | part="rib" | x10`), T23.
- Structure unchanged: one top-level folder with SKILL.md (installs directly as a zip).

## 1.2.0 — 25 September 2026
- First skill package cut from CLAUDE.md v1.2 (owner feedback 1 and six test designs).
