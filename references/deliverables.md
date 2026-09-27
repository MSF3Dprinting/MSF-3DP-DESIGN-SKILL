# Deliverables, README datasheet and documentation style

*Reference file of the `msf-3dp-design` skill. Read it before the design review and when packaging, and when writing or updating the README or DATASHEET.* Section numbers (§) are shared by every file of the skill: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · readiness-levels.md · Appendix A glossary.md · Appendix C sources.md.

## 11. Deliverables

### 11.0 Order of work — design review before documentation (owner, Sept 2026)
Model → automated checks and structural review → **design review**: the user sees pictures, not files — the render sheet, the assembled view (`part="assembly"`) and a section of the load‑bearing zone (`section_from_stl.py`) — and clicks "looks right — make the files" or "change something — I'll type it". Only after that click: the Customizer file, the STLs of the release, README, DATASHEET, zip. A change asked at the review costs a model edit and a new sheet, never a documentation rewrite. Each rejected concept and its reason go into the brief and the DATASHEET version history.

### 11.1 Package (every build)
```
<item-slug>_v<x.y>.zip                   the whole folder, one download                                        required
<item-slug>/
  README.md                              short and visual (templates/README_TEMPLATE.md)                       required
  DATASHEET.md                           full datasheet (templates/DATASHEET_TEMPLATE.md)                      required
  <item>.scad                            working file: include <common.scad>, <helpers.scad>; no @ header        required
  <item>_customizer.scad                 one-file Customizer version, exact five-line header (§7.7)             required
  <item>_context.scad                    context scene: use <item.scad> + stand-ins, never exported
  common.scad  helpers.scad              next to the part
  variants.txt                           what export.sh exports
  stl/<item>_<variant>_v<x.y>.stl        binary, mm, IN PRINT POSITION on Z = 0, one per component             required
  stl/<item>_plate_v<x.y>.stl            all components on one print plate (part="all")                       required for several components
  stl/<item>_<variant>_<k>_v<x.y>.stl    N identical items -> N numbered files (k = 1..N)                     required when N > 1
  stl/<item>_coupon_v<x.y>.stl           tolerance / interface coupon, same orientation as the part           when a fit is new
  stl/<item>_outline_check_v<x.y>.stl    when §3.6 or §3.4 (e) applies
  stl/view_only/<item>_assembly_v<x.y>.stl  assembled view — for looking, not for printing
  stl/EXPORT_LOG.txt                     exporter version, date, parameter set, check result and HARDWARE per STL, coupon steps
  img/<item>_<variant>_sheet.png         captioned overview = README picture                                  required
  img/<item>_<variant>_front/_top/_side/_iso.png   _context.png (installed)   _exploded.png   _section.png
  img/<item>_assembly_iso.png            assembled view                                                       several components
  img/<item>_coupon.png                  coupon, top view
  img/<item>_section_<axis><mm>.png      section drawings of the load-bearing zone (section_from_stl.py)
  img/<item>_overlay.png                 when a photo or sketch was the source
  tools/                                 every script of the skill's scripts/ + sweep_report_<date>.txt
  brief/design_brief.md  design_plan.md
  STATUS.md                              multi-item projects, or when a conversation ends before release
  docs/LESSONS_LEARNED_<item>.md         at release, or when the user asks
```
- STL: binary, millimetres, in the print position (the part sits on Z = 0 as it is printed — nothing to rotate). One item per file; **N identical items → N numbered files** (`variants.txt`: `rib | part="rib" | x10`); several components → one file each **and** the plate with all of them. The README's parts table lists every file with its quantity and a picture. The assembled view never goes into `stl/` itself. Offer a `.3mf` project saved from PrusaSlicer when the user slices there (the fast exporter cannot write 3MF).
- `export.sh` reproduces every STL, the copies, the coupon, the checks, the renders and the Customizer file, and writes `stl/EXPORT_LOG.txt`.
- **Licence text appears once**: the `@license` line of the Customizer file header (§7.7) — MIT for a new MSF design, the source's licence for an adapted one. No licence file, no licence lines anywhere else, no certification marks or badges (internal documents). No personal data anywhere (§1.5); the request is identified by request number and department.
- **Attribution for verification and accountability**: the README (and the DATASHEET) state that the design was made by Claude with the msf-3dp-design skill, its version, and the link https://github.com/MSF3Dprinting/MSF-3DP-DESIGN-SKILL — the exact wording is in the templates.
- **Hardware**: every fastener and other material is listed with quantity; kit hardware by its kit name (e.g. "2 × bolt M6 × 40 DIN 912 from the kit"); anything else exactly, with two local alternatives and where it can be taken from (§5.4.2).
- Hand‑off message, ≤ 15 lines: what was built · the sheet · one line per verification group with pass/fail · what was not verified · unverified values · warnings and the advisor decision needed · hardware in one line · how to print (coupon first, its code, then the parts) · the follow‑up schedule in one line · what to click after the print.
- A conversation that is about to end (context or tool‑call limit) before release delivers what is verified — the model, the checks, the sheet — and a STATUS.md, never an unchecked package; the next turn first compares the working files with the last delivered package and treats any unknown change as an unverified draft.
- Before zipping: `grep -rn PLACEHOLDER` returns nothing; the section heights quoted match the check JSON; every number in the README matches the DATASHEET and the export log.

### 11.2 README.md — short and visual
People in the field will not read a long document. The README is one screen plus pictures, from `templates/README_TEMPLATE.md`: the sheet; what it is, where it is used, what it is not for, what it fits, whether it is critical and who approves; **parts to print** (a table: file, quantity, picture per part, the all‑parts plate, coupon first); **hardware** (kit parts, or exact local parts with alternatives and sources); print (materials in order, settings in one line, print time); install/use with the context render, the assembled view and the exploded view; clean; **check** — before use, the hold limits in numbers, and the follow‑up table (installation, 2 weeks, 1 month, 3 months; critical items 6 and 12 months, then every 6 months), each visit validated by the 3D printing advisor; the approval table; the attribution line with the skill version and link. Everything else goes to `DATASHEET.md`.

### 11.3 DATASHEET.md — the full record
`templates/DATASHEET_TEMPLATE.md`: the MSF product technical specification datasheet — general information, form (dimensions, intended use and out‑of‑scope uses, readiness on the Humanitarian Making scale taken verbatim from `references/readiness-levels.md`, justification, approval), fit (compatibility, parameters table, tolerance envelope, hardware, manufacturing instructions, QC with the follow‑up schedule), function (description, the structural review with its hand estimates and hold limits, notes, cleaning, storage, safety, Spaulding class, risk assessment), verification results, attachments with the attribution line, signatures, version history including rejected concepts and why. Plain language; "N/A" only when true; "to be assessed by <owner>" rather than an invented value; no licence or certification text.

## 12. Documentation style
- Plain, short language for field staff; one idea per step; checklists over prose for QC and cleaning.
- README always includes: what it is and is not for, what it fits, parts to print with pictures, hardware, acceptable materials, print settings in one line, install steps with the context image, cleaning agents and "do not autoclave", the before‑use check with hold limits in numbers and the follow‑up schedule, approval, attribution. DATASHEET always includes the rest: parameters, tests, structural review, tapers and clearance directions, risk assessment, readiness, version history.
- Never include: chemical‑resistance tables; identification marks on clinical parts; the word "wet" for filament; licence statements (except the Customizer header's `@license` line), certification marks, badges or UIDs.
- README in English; offer translations of the user‑facing sections.
