# Changelog — msf-3dp-design skill

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
