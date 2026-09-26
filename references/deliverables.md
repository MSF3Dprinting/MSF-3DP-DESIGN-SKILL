# Deliverables, README datasheet and documentation style

*Reference file of the `msf-3dp-design` skill. Read it when packaging a build stage and when writing or updating the README.* Section numbers (§) are those of the compiled workflow file (CLAUDE.md v1.2) and are kept so that cross-references stay valid: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · Appendix A glossary.md · Appendix C sources.md.

## 11. Deliverables

### 11.1 Package (every build)
```
<item-slug>_v<x.y>.zip                 the whole folder, one download                                    required
<item-slug>/
  README.md                            short and visual (templates/README_TEMPLATE.md)                   required
  DATASHEET.md                         full datasheet (templates/DATASHEET_TEMPLATE.md)                  required
  <item>.scad                          working file: include <common.scad>, <helpers.scad>                required
  <item>_customizer.scad               one-file Customizer version (flatten_scad.py --verify)             required
  <item>_context.scad                  context scene: use <item.scad> + stand-ins, never exported
  common.scad  helpers.scad            next to the part
  stl/<item>_<variant>_v<x.y>.stl      binary, mm, IN PRINT POSITION on Z = 0                              required
  stl/<item>_<variant>_<k>_v<x.y>.stl  N identical items -> N numbered files (k = 1..N), ready to import  required when N > 1
  stl/<item>_coupon_v<x.y>.stl         tolerance / interface coupon, same orientation as the part         when a fit is new
  stl/<item>_outline_check_v<x.y>.stl  when 3.6 or 3.4 (e) applies
  stl/EXPORT_LOG.txt                   exporter version (Manifold), date, parameter set per STL
  img/<item>_sheet.png                 captioned overview = README picture                                required
  img/<item>_front/_top/_side/_iso.png  img/<item>_context.png  _section.png  _exploded.png  _coupon.png  _overlay.png (when a photo/sketch was the source)
  tools/                               check_stl.py sweep.py render_views.py overlay_sketch.py flatten_scad.py export.sh openscad-fast openscad_manifold.mjs install_openscad.sh sweep_report_<date>.txt
  brief/design_brief.md  design_plan.md
  STATUS.md                            multi-item projects
  docs/LESSONS_LEARNED_<item>.md       at release, or when the user asks
```
- STL: binary, millimetres, in the print position (the part sits on Z = 0 as it is printed — nothing to rotate). One item per file; **N identical items → N numbered files** (`variants.txt`: `rib | part="rib" | x10`). The README's parts table lists every file with its quantity and a picture. Offer a `.3mf` when the user slices in PrusaSlicer.
- `export.sh` reproduces every STL (via `openscad-fast`), the copies, the coupon, the checks and the renders, and writes `stl/EXPORT_LOG.txt`; `flatten_scad.py --verify` regenerates the Customizer file.
- No licence file, no licence lines, no certification marks anywhere in the package (internal documents). No personal data anywhere (§1.5); the request is identified by request number and department.
- Hand‑off message, ≤ 15 lines: what was built · the sheet · one line per verification group with pass/fail · what was not verified · unverified values · warnings and the advisor decision needed · how to print (coupon first, its code, then the parts) · the follow‑up schedule in one line · what to click after the print.

### 11.2 README.md — short and visual
People in the field will not read a long document. The README is one screen plus pictures, from `templates/README_TEMPLATE.md`: the sheet; what it is, where it is used, what it is not for, what it fits, whether it is critical and who approves; **parts to print** (a table: file, quantity, picture per part, coupon first); print (materials in order, settings in one line, print time); install/use with the context render and the exploded view; clean; **check** — before use and the follow‑up table (installation, 2 weeks, 1 month, 3 months; critical items 6 and 12 months, then every 6 months), each visit validated by the 3D printing advisor; the approval table; version and skill version. Everything else goes to `DATASHEET.md`.

### 11.3 DATASHEET.md — the full record
`templates/DATASHEET_TEMPLATE.md`: the MSF product technical specification datasheet — general information, form (dimensions, intended use and out‑of‑scope uses, readiness on the Humanitarian Making scale taken verbatim from `references/readiness-levels.md`, justification, approval), fit (compatibility, parameters table, tolerance envelope, manufacturing instructions, QC with the follow‑up schedule), function (description, notes, cleaning, storage, safety, Spaulding class, risk assessment), verification results, attachments, signatures, version history. Plain language; "N/A" only when true; "to be assessed by <owner>" rather than an invented value; no licence or certification text.

## 12. Documentation style
- Plain, short language for field staff; one idea per step; checklists over prose for QC and cleaning.
- README always includes: what it is and is not for, what it fits, parts to print with pictures, acceptable materials, print settings in one line, install steps with the context image, cleaning agents and "do not autoclave", the before‑use check and the follow‑up schedule, approval. DATASHEET always includes the rest: parameters, tests, tapers and clearance directions, risk assessment, readiness, version history.
- Never include: chemical‑resistance tables; identification marks on clinical parts; the word "wet" for filament; licence statements, certification marks, badges or UIDs.
- README in English; offer translations of the user‑facing sections.

