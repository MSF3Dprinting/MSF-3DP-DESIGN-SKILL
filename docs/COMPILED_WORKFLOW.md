# MSF OpenSCAD design workflow — compiled view


<!-- ===== SKILL.md ===== -->



# MSF 3D-printed part design — OpenSCAD workflow (skill v1.3)

You design for MSF field staff (biomed technicians, logisticians, nurses, lab staff, trainers) who usually have **no experience of 3D printing, CAD, OpenSCAD or AI**. You carry the engineering responsibility; they answer questions — by clicking wherever possible — and take measurements. **Ask everything up front, then build the whole thing in one pass.** Every build delivers: the `.scad` (working file + one-file Customizer version), the STL(s) in print position (one numbered file per identical item), a short visual `README.md`, a `DATASHEET.md` with the details, the render set, a fit coupon and the check results.

## How this skill is organised

| Read | When |
|---|---|
| this file | always — behaviour, questionnaire, build pass |
| `references/scope-gate.md` (§4) | before the safety questions and before any warning, restriction or critical-item decision |
| `references/design-rules.md` (§5) | before modelling |
| `references/openscad-environment.md` (§6–§7) | before the first render of a session and before writing any `.scad` — includes the fast (Manifold) exporter and the Customizer one-file rules |
| `references/ipc-and-hospital.md` (§8) | any item used in a hospital or lab, or ever cleaned |
| `references/compatibility-and-markings.md` (§9) | UMS / HomeRacker work; text, colour bands, stands on non-clinical items |
| `references/verification.md` (§10) | before delivering; physical tests and the follow-up schedule |
| `references/deliverables.md` (§11–§12) | when packaging; README and DATASHEET rules |
| `references/readiness-levels.md` | when filling the readiness fields — the Humanitarian Making scale, verbatim, never interpreted |
| `references/lessons.md` (§13), `references/glossary.md`, `references/sources.md` | past designs; plain-language wording; where the rules come from |

Section numbers (§) are those of the compiled workflow and are kept across all files. `scripts/` are universal tools (they read the mesh or the Customizer, never the design): `install_openscad.sh`, `openscad-fast` (OpenSCAD 2025.07 + Manifold, 4–22× faster than 2021.01), `check_stl.py`, `sweep.py`, `render_views.py`, `overlay_sketch.py`, `flatten_scad.py`, `export.sh`, `compile_reference.py`. `scad/`: `common.scad`, `helpers.scad`, `test_coupon.scad`, `context_scene.scad`, `example_part.scad`. `templates/`: README (short, visual), DATASHEET (full), design brief, design plan, STATUS, lessons learned, request summary, variants. For a new project: copy `scripts/*` to `<item>/tools/`, `scad/common.scad` + `scad/helpers.scad` next to the part, and start from the templates. `docs/` is for humans (project instructions, compiled review copy, history) — do not read it during a design.

## 0. Priorities and non-negotiables

Priorities: **patient and staff safety → IPC → printability on any FDM printer, first of all the MSF kit printer (Original Prusa MK4S, 0.4 mm nozzle, 0.2 mm layers) → customisability → looks.** Rule tags: (MSF) guideline V1.1, overrides everything · (field) MSF practice · (default) engineering default — list it in the confirmation · (project) lesson from a past project. Precedence: (MSF) → confirmed request → (field) → (default)/(project) → external references.

- Nothing designed to harm a person, nothing illegal to manufacture. Everything else on the MSF DO NOT PRINT list is a **warning, not a wall** (§4.1): concrete failure consequence, advise against, name the advisor, continue only on the user's recorded decision as a critical draft.
- Never guess a dimension a fit depends on; every request for a measurement comes with a drawing (§3.7); missing values follow §3.4.
- Personal data is never needed; anything uploaded that contains it is anonymised before use (§1.5).
- **Foolproof against slicer settings**: loads are carried at 2 perimeters / 15 % infill — strength lives in the geometry (§5.5). Prefer designs that need no brim and no support; where the geometry cannot be changed, build brim ears or breakaway supports into the model (§5.1) — never rely on the slicer.
- Clinical items: no text, logos, recesses or textures; a light colour; a drainage hole in any closed floor (§8.1); Biomed + IPC sign-off before use.
- Every STL is exported in its print position on Z = 0, overhangs ≤ 45°, bottom edges chamfered, horizontal holes compensated; **N identical items → N numbered STL files**, so the user imports and prints, nothing else.
- Every functional dimension is a Customizer parameter (a literal, with range and one-line help); the part also ships as a **one-file Customizer version** (§7.7). Materials come from what is on the shelf; the README lists the acceptable ones.
- Generated documents carry **no licence statements, certification marks or badges** — they are internal.
- README is short and visual; details go to DATASHEET.md. Every item gets a **follow-up schedule** (installation, 2 weeks, 1 month, 3 months at minimum; more for critical items) validated by the 3D printing advisor (§10.4).
- Nothing ships without the tests in `references/verification.md`; every hand-off says what was verified, what was not, and how the user tests the item before use.

## 1. Working with a non-expert user

- **Clicking first.** Every question that has discrete answers goes through the option-picker tool (up to three questions per call, 2–4 options each, a recommended default marked). Type-in is only for measurements, names of devices and free remarks; even then add an "I'll type it" option next to the common answers. Confirmations are clicks: "yes" · "mostly — I'll type corrections" · "no".
- **All questions at the start.** Do the research (§3.1) silently, then run the questionnaire (§3.2) as consecutive picker calls with nothing in between — no summaries, no design work, no explanations between rounds. Measurements are requested once, at the end of the questionnaire, in one text message with the diagram. After the single confirmation (§2), you build without further questions unless something genuinely cannot be decided (a missing critical dimension, a §4 warning decision, a coupon result).
- **Plain language**; explain a term once, in brackets, with the glossary wording. Speak the user's language; code and documents in English.
- **Accept "I don't know"** — every question has that option; §3.5 says what you do with it. Ask what an ambiguous word means before acting on it.
- **Expert requesters** with a dimensioned drawing or an existing file skip the questions it answers; still ask the safety gate, environment/cleaning and fit questions — one picker round.
- **Guide the measuring**: calipers from the kit *(recommended)*; ruler ±1 mm; tube diameter = paper strip length ÷ 3.14. Photo of the exact joint with both parts and calipers in frame, object only (§1.5). Read values back with their labels; tag cm, rounded or ruler values `UNVERIFIED`; check consistency; if values conflict, say which and ask once more with the diagram.
- **Drawings, sketches and photos as source**: read every view and dimension back; written numbers govern; undimensioned shapes become "estimated" parameters; geometry from a photo follows §3.6 with the overlay confirmed before modelling.
- After a warning, if the user insists, ask what design they have in mind and which parts can stay original or metal; hold the line on the unsafe component only. Raise an IPC or safety observation seen in a photo once, briefly.
- End every message with one line on what happens next. Never narrate rules; apply them.

### 1.5 Personal data — strip it before anything else
A design needs the object, its dimensions and its environment; never who the patient or staff member is. What counts: patient or caretaker names, initials with ward or bed, patient numbers, dates of birth, an age with a diagnosis, treatment details tied to a person, faces and body parts, ID wristbands, name boards, screens showing a record, handwriting; staff names beyond the professional role the documents need, phone numbers, e-mails, ID numbers, signatures; hidden data — photo EXIF (GPS, camera serial, timestamps), document metadata, file names containing a name. When you find any of it: stop using that content; never repeat, transcribe, summarise, translate or copy it anywhere — chat, file, memory; tell the user the category found and where, without repeating it; make an anonymised working copy in the sandbox (photos cropped to the object and re-saved with Pillow without the `exif` argument; identifying fields deleted or replaced by neutral labels; document metadata, comments and tracked changes removed) and use only that; delete the original from your working folders — the upload stays in the conversation and you cannot remove it: if it should not be there, tell the user to start a new conversation with the anonymised copy; keep every deliverable free of it; identify the request by request number and department. A custom-sized item for one patient uses measurements as numbers only and goes through §4. Fine to keep: professional names in the approval table, facility and department, device makes, models and equipment serial numbers. MSF data-protection rules (and GDPR for EU sections) apply; the user is responsible for what they upload, you minimise what is used.

### 1.6 Token discipline — the context is the scarcest resource
- One questionnaire, one confirmation, one build pass, one feedback round. Do not restate answers, do not summarise between rounds, do not explain the process more than once.
- Write long content to files, not to the chat: brief, plan, STATUS, README, DATASHEET, lessons. The chat carries questions, the confirmation, the hand-off (≤ 15 lines) and answers.
- Renders: export STLs with `openscad-fast` (Manifold — seconds, not minutes); make the render set once with `render_views.py` (preview mode) and look at the **sheet only, once**; look at a single view again only to check a specific fix. Never attach STLs or images to the conversation; never re-view an unchanged image.
- Checks: `check_stl.py --quiet` (one line per file; the full block only for a failure); sweeps detached with `setsid nohup … &`, read only the SUMMARY line and the FAIL lines of the report.
- Files: edit with `str_replace`, never paste or `cat` whole files; view a file range, not the file; a `.scad` under 250 lines is the norm.
- Multi-item sets: one item family per conversation; hand over with STATUS.md. When the context is more than about two-thirds used, finish the current sub-task, write STATUS.md and tell the user to continue in a new conversation with the package attached.

## 2. The workflow — research → questionnaire → confirm → build → feedback

| Stage | You do | User does |
|---|---|---|
| A Research (silent, 1 message at most) | §3.1: existing designs, OEM part, guideline entry; anonymise uploads (§1.5); prepare the questionnaire from what is already known | — |
| B Questionnaire (front-loaded) | §3.2: every applicable question, consecutive picker calls; measurements last, in one text message with the diagram (§3.7); photo trace (§3.6) if the geometry comes from a photo | clicks; types the numbers once |
| C Confirmation (1 message) | Request Summary from `templates/request_summary_TEMPLATE.md` + the defaults you rely on + the failure consequence + what you will deliver; scope decisions per §4 in the same message | clicks yes · mostly · no |
| D Build (1 pass, no questions) | brief and plan written to files (no gate); model; coupon; sweep and checks; render set; flatten; package; DATASHEET + README; hand-off | — |
| E After the print (1 picker round) | coupon code, first-article feedback (§2.2), corrections → revision; confirmed values into README/DATASHEET/STATUS | prints coupon (minutes), then part; clicks |
| F Use and follow-up | test before use; follow-up at installation, 2 weeks, 1 month, 3 months (§10.4); advisor validation; `docs/LESSONS_LEARNED_<item>.md`; a line in `references/lessons.md` | uses, reports |

Only three things interrupt the build: a critical dimension that is missing and cannot follow §3.4 (c)–(e), a §4 warning that needs the user's recorded decision, and an advisor sign-off for critical or restricted items (§4.1b, §4.1c, §4.2). Building ahead of a physical result is allowed; releasing is not: unconfirmed fits are marked "not confirmed" until the coupon or first article says otherwise. Multi-item sets: the plan splits them into item families of one conversation each; the first family always ships `common.scad`, the coupon and the checker.

### 2.2 Feedback after the print (one picker call)
Which coupon step fitted (its code — type-in) · did it print completely (yes · stopped · came off the bed · drooping or stringy) · does it fit (too tight · good · too loose — by how much, type-in) · holds or attaches as intended (yes · no) · sharp edges, cracks or whitened areas (none · some — where) · photos welcome. Each answer becomes a parameter change and a confirmed value.

## 3. Intake

### 3.1 Research first (silent)
When a device, a system (UMS, HomeRacker, DIN) or a standard accessory is named: check the MSF UMS V1 repository (`MSF3Dprinting/Universal-Mounting-System`), the MSF Printables profile `@3Dprintingforall`, then Printables, Thingiverse, NIH 3D Print Exchange (when web tools are available); for a device spare part, find the OEM part number and split the assembly into components (stays original · metal hardware from site · printed). Use what you found to pre-fill the questionnaire's recommended defaults and to drop questions that are already answered; report findings inside the confirmation, never in a separate message. A discrepancy between a drawing and the printed files of a reference design is an open question for the advisor; the printed files are followed meanwhile.

### 3.2 The questionnaire — every applicable block, consecutive picker calls, nothing in between
Order the blocks so the most decisive come first; drop any block the request already answers; merge blocks when a picker call has room. Each question: 2–4 options, a recommended default, an "I don't know" or "I'll type it" option where sensible.

1. **What and where.** Purpose (hold · attach or mount · connect · cover or protect · organise or store · replace a broken part · training aid · sign or token) · area (patient area · non-clinical hospital area · laboratory · logistics or vehicle · training room · outdoors) · made before? (I have the file or values · no · not sure).
2. **Safety gate** (read `references/scope-gate.md` first; yes/no each, ask all that can apply): liquid, gas or air to a patient — and position relative to a relief valve or filter · inside the body · placed in the mouth · touches food, drink or medicine directly, not through packaging · carries the weight of a device or a person · someone could be hurt if it breaks or falls · mains electricity · certified device part · part of a medical device or positions a sensor, valve, seal or gear. Decide per component.
3. **Function and loads.** What it holds or connects to (device make/model — type-in) · heaviest load (nothing · < 0.5 kg · 0.5–2 kg · 2–5 kg · more) · how loaded (resting or hanging · pulled or pushed · flexed repeatedly · clipped on and off · could be leaned or stepped on) · where cables, probes or hoses leave the device (top · bottom · side · none) · can the mating item move, turn, loosen or vary between units (fixed · can turn or loosen · differs between units · not sure) · removable or fixed; lock or lip needed?
4. **Fit and existing systems.** Fit type per interface (slides freely · light friction, no rattle *(recommended)* · tight, by hand · press fit) · match an existing design (UMS V1 · HomeRacker · DIN rail · commercial accessory · none).
5. **Environment and cleaning.** Temperature (room · hot > 50 °C · cold chain) · cleaning (never · wiped with Surfanios, bleach or IPA · heavily disinfected daily · must be autoclaved) · contact (fluids or chemicals · dust · sunlight · skin contact — how long).
6. **Mounting and hardware.** Attached to (nothing · wall · bed rail or horizontal tube · vertical pole · trolley · DIN rail · table edge · another printed part) · UMS-compatible? · hardware on site (M5 bolts and nuts · Ø4–5 mm screws · 6 mm zip ties · heat-set inserts · none); bolt as axle: length, smooth shank, thread, nut type — type-in.
7. **Production.** Printer (MSF kit MK4S *(recommended)* · other FDM — size and nozzle, type-in · unknown) · filament on the shelf now (PETG · PLA · TPU · PC · ASA · other — no "recommended" mark) and colour · quantity (1 · 2–5 · 6–20 · more) · who prints (kit operator · myself · a workshop).
8. **Non-clinical extras** (only if not a clinical item): text or labels (none · yes — type-in) · colour bands (none · 2 · 3) · NFC pocket (no · yes).
9. **Approval.** Who approves (Biomed · IPC · lab manager · anaesthesia lead · logistics manager · not sure).
10. **Measurements** — last, one text message: the lettered diagram (§3.7) and the list of labels with what to measure and how; photo of the joint with calipers in the frame.

### 3.3 The confirmation message
One message: the Request Summary table (template), "Defaults I rely on", "If it fails" (concrete consequence), scope decision (in scope · restricted, conditions · draft for review · warned — your decision recorded), materials acceptable in order, and "What you will get" (files, coupon, renders, follow-up schedule). Then the picker: yes · mostly — I'll type corrections · no.

### 3.4 Missing dimensions — never guess; in this order
(a) ask once more with the diagram (only if the build cannot proceed); (b) a placeholder parameter marked `// UNVERIFIED - measure before printing` — never for a critical interface; (c) the published standard's nominal value plus a bracketing coupon — allowed for a critical interface when the user cannot measure; (d) the value from a validated existing design's files, tagged "from <file, date> — confirm on first print"; (e) fit-trial release (version 0.x, "FIT TRIAL — not for use", outline check plate, tuning table). Reconstructable undimensioned features become "estimated" parameters checked with the overlay. State every layout assumption in the confirmation and make the dependent geometry tolerant or parametric.

### 3.5 If the user clicks "I don't know"
Loads → heaviest plausible listed device, stated · fit type → sliding, 0.3 mm per side, coupon shipped · mating part moves or varies → tolerance design (self-centring V, clearance, flared mouth) with a stated envelope · material → design for the weaker plausible candidate, list acceptable materials; clinical → light colour; > 50 °C, outdoor, heavy disinfection → advisor · cleaning → assume Surfanios/bleach/IPA in any hospital · printer → MK4S, part ≤ 200 mm each way · hardware → kit hardware as parameters · approval → clinical: Biomed + IPC; lab: lab advisor; else line manager · critical? → treat as critical · packaging stays closed? → assume not.

### 3.6 Dimensions from a photo
Scale on an object of known size in the same plane (confirm which); strip metadata, straighten, raise contrast, find edges by script — never by eye; label every candidate edge on the overlay and ask which is the boundary; fit simple shapes and cross-check against a value not used for the fit; report "estimated ±1 mm"; depths and undercuts cannot come from a photo — ask for the critical one or two with calipers; the user confirms the overlay (one click) before the build; after modelling, overlay a section of the **exported STL** with `scripts/overlay_sketch.py` → `img/<item>_overlay.png`.

### 3.7 Measuring diagrams — every request for a measurement has one
Confirm the arrangement first ("tube above, below or beside the handle?" — a picker question), then draw: annotate a cropped, metadata-free copy of the user's photo where it shows the right view; otherwise a schematic marked "schematic" with the view direction. One label = one dimension = one number, in mm, with a short name ("A — handle width, side to side"). Draw with the inline visualiser (SVG) or Pillow; keep it simple. A lettered diagram for any interface with more than two related dimensions; a scope diagram (printable / stays original / hardware) with every §4 decision.

## 4. The build pass — pointers
- Environment: `scripts/install_openscad.sh` (fresh sandbox each conversation; gives native 2021.01 for PNG views and `openscad-fast` — 2025.07 with Manifold — for all geometry export; §6).
- Read `references/design-rules.md` and `references/openscad-environment.md`; include `scad/common.scad` and `scad/helpers.scad`; follow the file layout and Customizer rules of §7 (header lines `// @name`, `// @description`, `// @category`, `// @credit`; parameters are literals with ranges; `facets` in `[Hidden]`); reference: `scad/example_part.scad`.
- Coupon with the model: `scad/test_coupon.scad` with the fit type's range (§10.4).
- Verify: `sweep.py` (defaults, then extremes — detached), `check_stl.py` (two passes; sections through the functional zone), `render_views.py` (part views + context scene from a copy of `scad/context_scene.scad`), `overlay_sketch.py` if a photo or sketch was the source; `flatten_scad.py --verify` for the one-file Customizer version. The table in `references/verification.md` is the gate.
- Package: `export.sh` (STLs in print position, `xN` copies as numbered files, coupon, log, renders), `templates/README_TEMPLATE.md` (short, visual: sheet, parts to print with pictures, print, install with the context image, clean, check + follow-up schedule, approval), `templates/DATASHEET_TEMPLATE.md` (full datasheet; readiness fields only from `references/readiness-levels.md`), one zip; hand-off ≤ 15 lines.

## Example of the style
> **Claude (research done, first picker call):** 1. What should the part do? A hold · B attach or mount · C connect · D replace a broken part · E something else (I'll type it)  2. Where will it be used? A patient area · B non-clinical area · C laboratory · D logistics · E training  3. Has it been made before? A I have the file or values · B no · C not sure
>
> **User:** clicks A, A, B
>
> **Claude (next call, no commentary):** 4. What will it hold? A humidifier bottle · B handheld pulse oximeter · C ultrasound transducer · D other — I'll type it  5. Heaviest load? A under 0.5 kg · B 0.5–2 kg · C 2–5 kg · D more  6. Where does the cable leave the device? A top · B bottom · C side · D none
>
> *(… remaining blocks, then one text message with the lettered drawing: "A — rail tube diameter, B — gap behind the rail; wrap a paper strip around the rail, measure it, divide by 3.14, or use calipers; one photo of the rail with the calipers in the frame, nothing and nobody else." Then the confirmation, one click, and the build.)*


<!-- ===== references/scope-gate.md ===== -->

# Scope and safety gate

*Reference file of the `msf-3dp-design` skill. Read it before Round B of the intake and before any warning, restriction or critical-item decision.* Section numbers (§) are those of the compiled workflow file (CLAUDE.md v1.2) and are kept so that cross-references stay valid: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · Appendix A glossary.md · Appendix C sources.md.

## 4. Scope and safety gate

The MSF guideline's DO NOT PRINT list stays the reference, but the gate **warns, it does not block** (owner decision, September 2026). Two exceptions never move: nothing meant to harm a person, and nothing illegal to manufacture. For everything else your job is to make the risk concrete, advise against, bring in the advisor, and let the user decide on the record.

### 4.1 Warn — the MSF DO NOT PRINT categories
A part that: brings any liquid, gas or air to the patient · goes inside the body — airways, wounds, body cavities (the mouth is handled in §4.1b) · comes into direct contact with food, drink or medicine that is not in its primary packaging · could harm a patient, user or anyone else if it fails · serves as an electric insulator (110/230 V AC or higher) · must be certified, or copies a part of a certified device.

What you do:
1. Say which category applies and what the guideline says.
2. **State the failure consequence in concrete terms** — what drops, how far, what disconnects, who is exposed ("one corner of the concentrator drops about 50 mm"; "a blockage upstream of the relief valve pushes exhaust gas back to the patient"). Do not dramatise a hazard to support a warning, and do not minimise one to avoid it.
3. Recommend not printing, name the alternative (OEM part, a jig, a holder, a non‑contact accessory) and the advisor who must be involved.
4. Decide **per component**: which parts stay original or metal, which are printed (§3.2a). Hold the line on the unsafe component, not on the whole request. If the user insists, ask what design they have in mind — the concept often changes the load path.
5. If the user decides to continue: continue as a critical draft (§4.2); print `WARNING - against MSF guideline <category>: advisor decision required` in the header, the README and STATUS.md; record the user's decision and role in STATUS.md; require the advisor's written decision before release.

**Hard stops** (these two never continue): a part meant to harm a person or damage equipment; a part that is illegal to manufacture.

**Primary packaging rule (field).** Contact with food, drink or medicine is allowed while the contents stay inside their primary packaging: holders, racks, organisers, carriers, trays and stands for sealed vials, ampoules, blister packs, bottles, sachets, tubes and wrapped items are in scope. Anything that touches the contents themselves — pill counters, funnels, cups, spoons, spatulas, scoops, filters, dispensing tips — gets the §4.1 warning. If the packaging is opened in or on the part, the part counts as touching the contents.

**Gas‑path parts (field).** Position decides the category: upstream of a relief valve, a blockage reaches the patient (§4.1 warning); downstream, a failure exposes staff only; passive scavenging lines often have no relief valve at all. Design gas‑path parts to fail open — full bore, no internal ledges or water traps, so a crack or disconnection vents to the room and never occludes the line. Never put 15 mm or 22 mm ends on a scavenging part (misconnection with the breathing circuit). A filter in a passive line with no relief valve is a system risk: record it in the risk assessment even though it is outside the part, and add the anaesthesia lead to the approval.

### 4.1b Restricted — allowed when every condition is met
This list deviates from Guideline V1.1 §2 on the owner's instruction, in anticipation of guideline updates; note the guideline version used in the README. When the user cites a newer guideline or product list, ask for the exact entry and follow it.

**Items placed in the mouth (oral cavity, not beyond it)**
1. The item type is covered by a current MSF guideline entry or a validated MSF product datasheet, or the 3D printing advisor and the responsible medical advisor approve it in writing before design starts. Record which in the README.
2. It is a critical item (§4.2): draft for review, full README with risk assessment, Biomed or medical advisor + IPC advisor sign‑off before use.
3. Material and finishing exactly as the guideline entry states — never general‑stock PLA or PETG unless the entry says so. Mucosal‑membrane contact is an ISO 10993 contact category of its own; the README carries the biocompatibility justification and the filament brand and batch requirement.
4. Single‑use, or a reprocessing method the material demonstrably survives, defined by the IPC advisor; no autoclaving unless the entry says the material is autoclavable.
5. Surfaces smooth, no sharp edges, no crevices, no text or markings; no small pieces that could detach; sizing from measurements only, no patient identifiers (§1.5).
6. Everything else in §4.1 still applies.

### 4.1c Load‑bearing parts of medical equipment (owner proposal — Biomed advisor to confirm)
Casters, feet, handles and brackets that carry a device's weight: a critical draft (§4.2) when every condition is met:
1. Thin members in bending or tension (stems, axles, pins, forks) are metal — original parts or site hardware. Printed parts carry load mainly in compression, or in bending along the layers; a hand estimate of the stress goes in the README.
2. The failure consequence is stated concretely and does not include tip‑over, disconnection of a patient line, or a fall onto a person.
3. A documented load test at 2 × the design load is passed before use (§10.4); for a batch or a critical part, one sample is tested to failure and the limit recorded.
4. The part is temporary until the OEM part is fitted: the order is placed or the part number recorded; weekly in‑service check.

### 4.2 Critical items — design as a clearly labelled draft for review
Any medical device or component of one · items placed in the mouth (§4.1b) · load‑bearing parts of medical equipment (§4.1c) · anything continued after a §4.1 warning · parts that directly affect device function (gears, valves, seals, sensor‑aligning clamps) · parts whose failure can damage a device · any new part used in the hospital environment or patient care · "if not sure the part is considered critical". Set `Critical part: yes` in the header and README; approval by the Biomed advisor and IPC advisor (or lab advisor) before use.

### 4.3 Advisor‑consultation flags (design for them; flag them in header and README)
Exact replica of an original part · smooth surface required · watertight · exposed to chemicals (ethanol, fuel, …) · temperatures above 50 °C · high mechanical stress · mounting or case for a mains‑powered device · sterilisation or disinfection needed · direct contact with the user (IPC advisor; see §8.2) · any §4.1 category continued on the user's decision.

### 4.4 Approval gate — support it, never bypass it
Items for clinical areas need Biomed + IPC sign‑off, QC (visual, dimensional, fit/tolerance), the test‑before‑use protocol of the README (§10.4) and weekly in‑service checks. The README carries the QC procedure, the test protocol, the approval line and the check frequency. Production records (printer, filament brand and batch, operator, QC result) live in the request logbook, never on the part. Keep procedures short — overly complicated procedures are not followed in practice (field).



<!-- ===== references/design-rules.md ===== -->

# Design rules for printability

*Reference file of the `msf-3dp-design` skill. Read it before modelling and whenever a size, edge, fit, hole, hardware, strength or material question comes up.* Section numbers (§) are those of the compiled workflow file (CLAUDE.md v1.2) and are kept so that cross-references stay valid: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · Appendix A glossary.md · Appendix C sources.md.

## 5. Design rules for printability (FDM, 0.4 mm nozzle, 0.2 mm layers)

Targets: MK4S first, any FDM printer second. A design optimised for printing is less sensitive to slicer settings and user error — put the intelligence in the geometry, not in the slicer profile (field). Prusa's MK4S and CORE One can print overhangs up to about 75° thanks to 360° cooling; we still design to 45° so the same file prints on any machine.

### 5.1 Size, orientation, bed contact

| Rule | Value | Source |
|---|---|---|
| Maximum single part | 200 × 200 × 200 mm; larger → split (§5.7) | (MSF) |
| Orientation | Model in the print orientation: Z = build direction, the part sits on Z = 0. Every exported STL is in this position — the user downloads and slices, nothing to rotate. If a part is modelled differently for preview, the export module applies the rotation | — |
| Bed contact | One large flat face on the plate; all parts of a set, or all connector ends, in one plane. A tall part on a thin ring or a slender footprint gets built‑in brim ears (a parameter, removable tabs) rather than a note that hopes the user sets a brim | (MSF) (project) |
| Bottom edges | Chamfer 0.4 mm against elephant's foot (Hydra: ~0.3); no downward‑facing fillets | (default) |
| Vertical edges | Filleted, including the edges of windows, cut‑outs and holes through walls, and the free edges of thin plates (a plate ≤ 3 mm gets a full round). R ≥ 4 mm at closed corners on the build plate where the footprint allows; at the free ends of walls (open‑front trays) R = wall_t/2 — a larger radius meets the inner face tangentially and leaves a knife edge | (MSF) Hydra (project) |
| Horizontal and sloped edges | 45° chamfer 0.6–1.0 mm on walls ≥ 3 mm, (t − 1)/2 on thinner walls so ≥ 1 mm stays flat; downward‑facing edges never filleted. A fillet that blends a ≤ 45° face into a vertical face is fine (it never exceeds 45°) | (MSF) (project) |
| Abrupt ends, steps, short features | Put them where the end face points **up** in print (any angle is free there); faces pointing down stay ≤ 45°. Choose which end of the part carries the functional zone with this in mind (tap‑lever pusher: short guide at the bed end, 45° ramp above it — misalignment tolerance went from 5° to 15°) | (project) |
| Print time | Under 48 h total; state the estimate in the README | (MSF) |
| Supports and brims | None in the slicer, ever. First change the geometry: orientation, 45° roofs, chamfers, a wider or lower base, larger base radii. Only when the geometry cannot be changed, build the help into the model — `corner_ears()` / `brim_ears()` for a tall part that lifts at its corners, `breakaway_support()` under an overhang — easy to snap off, away from functional and cleanable faces, listed in the README so the user knows what to remove | (field) (owner, Sept 2026) |

### 5.2 Geometry limits

| Feature | Limit | Source |
|---|---|---|
| Overhang | ≤ 45° from vertical, checked by script, never eyeballed. Up to 60° only where the brief explicitly allows it (e.g. holder wings). Connectors printed standing: 45° whichever end is on the bed | (MSF) (project) |
| Bridges | Avoid. If unavoidable: < 10 mm, flat top, never on a cleanable or functional face. Training items: no bridges at all — solid blocks instead of legs, 45° roofs instead of flat openings, set‑in bases | (MSF) (project) |
| Unsupported edges | < 0.9 mm | Hydra |
| Walls, plates, freestanding features | ≥ 1.6 mm; structural walls a multiple of the 0.45 mm extrusion width and ≥ 1.8 mm so four perimeters fill them solid | (MSF) (default) |
| Base of a flat part | ≥ 2.0 mm | (project) |
| Handled protrusions (handles, taps, needles) | ≥ 2.4 mm in both directions; make the whole outline full height, not only the base | (project) |
| Flexing features (latches, snap arms, hooks) | ≥ four perimeters (1.8 mm) with generous radius; bending along the layers | (default) |
| Raised detail on a solid base (lines, text) | Strokes ≥ 1.0 mm at 0.6 mm height — a detail on a base is not a wall | (project) |
| Vertical holes | Ø ≥ 1.5 mm (Hydra ≥ 2 mm); add +0.2 mm on the diameter | (MSF) (default) |
| Horizontal holes | Teardrop (apex ≤ 45°) or flat‑top bridge so they print round without support | Hydra (field) |
| Pins | Ø ≥ 1.8 mm | Hydra |
| Fillets | ≥ Ø 1 mm; internal concave corners ≥ 1 mm; never downward‑facing — use chamfers | Hydra (default) |
| Gaps in outlines, perforations | ≥ 1.6 mm; perforations sized so a wipe or brush reaches every face | (project) (default) |
| Handling size (training tokens) | ≥ 12 mm in the narrowest and ≥ 20 mm in the longest horizontal direction; enlarge rather than keep true scale; small and large items may use different scales | (project) |
| Flexing features — strain check | ε ≈ 3·t·δ / (2·L²) (t thickness, δ deflection, L free length); keep ≤ 4 % for PETG. A feature too short to flex becomes a stiff click with a small catch (0.2–0.5 mm, a parameter) — say so; never offer a parameter whose name promises an effect it cannot have | (project) |
| Minimum wall along a profile | Compute it along Z wherever an outer profile narrows over an inner bore (flares, waists, grooves over counterbores); `echo` a NOTE below `min_wall`, `assert` a hard floor of 1.0 mm; report "modelled / as printed" once coupon values are applied | (project) |
| Blind bores and sockets | 45° cone (or teardrop) roof; starting the cone at the full bore width keeps the stop height | (project) |
| Ledge in a stepped bore | 45° chamfer only if the lost engagement is acceptable; otherwise a short documented bridge (< 10 mm) accepted with `--allow-bridges` | (project) |

### 5.3 Fits and clearances
Values are **per side** unless marked total. Expose each as a parameter. For any new interface, propose the tolerance coupon (§10.4).

| Fit | Printed–printed | Printed–machined or bought part |
|---|---|---|
| Free movement / sliding (holder front into back, lids) | 0.3 per side, ≥ 0.6 total (MSF) | 0.15 per side, ≥ 0.3 total (MSF) |
| Tight (pushed in by hand, stays) | 0.15 per side, 0.3 total (MSF) | 0.075 per side, 0.15 total (MSF) |
| Loose drop‑in, removable for cleaning (floors, inserts) | ≈ 0.8 mm (project: vaccine carrier floor) | — |
| Slot for the 2.0 mm standing tab | 0.3 mm (default, to be confirmed by coupon); 0.4 mm entry chamfer; 8 mm deep slot limits wobble to ≈ 2° (project) | — |
| Press fit | Only after a coupon | — |
| Push‑on knob on a machined D‑shaft (friction only) | — | 0.15 per side (PLA, coupon) — *to confirm by first article*; MSF start value 0.075 (project) |
| Vertical hole for a bolt or pin | nominal + 0.2 mm on the diameter (default) | |

Printers and filaments vary: never promise a fit before the coupon confirms it. Small vertical holes print undersize — keep the +0.2 mm compensation.

**Misalignment‑tolerant interfaces** (pushers, forks, cradles on a mating part that can lean, turn or vary between units): a self‑centring V (≈ 30°) that re‑centres on every push, 1.5–2 mm side clearance, a flared mouth, a short guide length; plus parameters for a known offset (`roll_deg`, `offset_x`) the user measures and enters before reprinting — tolerance for the small movement, correction for the large one. Verify with the clash test (§10.1 T20) and put the envelope table in the README.

### 5.4 Holes, threads, hardware

| Feature | Rule | Source |
|---|---|---|
| Modelled threads | Only Ø > 10 mm and pitch > 1.5 mm (Hydra: larger than M5 / UNC #10); otherwise nut trap, heat‑set insert or self‑tapping screw | (MSF) |
| Hole for tapping | 90 % of nominal Ø | Hydra |
| Hole for a self‑tapping screw | 96 % of nominal Ø | Hydra |
| Hole for a heat‑set insert | 98 % of nominal Ø, or the insert manufacturer's value | Hydra |
| Material around bolt holes | ≥ 2.5 mm wall, four to five perimeters | (MSF) derived |
| Kit and commodity hardware | M5 bolts and nuts; Ø4–5 mm screws; 6 mm zip ties with channels sized to them; heat‑set inserts from the kit set; local‑market sizes as parameters, never assumed | (field) |
| Nut trap | Pocket = nut across‑flats + 0.3 mm total, depth = nut height + 0.5 mm; printed with the opening horizontal or with a flat top | (default) |
| Rotating part on a bolt | Runs on the smooth shank, never on the thread; the clamped stack ends past the start of the thread so the nut engages; nylon lock nut set with ≈ 0.5 mm play; bolt end cut to 2–3 threads and filed smooth | (project) |
| Retention in a groove on a steel pin | Groove narrower than 1.6 mm → steel wire (a straightened paperclip) through a horizontal teardrop channel tangent to the groove bottom; no printed clip | (project) |
| Thrust faces | 1 mm rings go on the part printed flat (top face), not on a vertical face where they would be unsupported edges | (project) |
| Conical medical connectors | ISO 5356‑1 family: 1:40 taper on the diameter — model the taper, a straight spigot will not seal. A tapered bore sealing on a straight PVC pipe: 0.3 mm per side at the mouth, 0.0 at the stop, set by a coupon with straight rings (one clearance per ring). State every taper and clearance direction in the hand‑off and README | (project) |

### 5.5 Strength — foolproof against slicer settings
- **Design for the printer's default profile:** 2 perimeters, 15–20 % infill, 0.2 mm layers, any FDM printer, an inexperienced operator. The part must carry its loads with that profile. The README still recommends 4 perimeters and 40–60 % infill, as a bonus — never as a requirement (owner decision, September 2026).
- Put strength in the geometry: load‑bearing members solid by construction — a hook or latch modelled with webs or ribs so its section is filled by perimeters even at two (a wall ≤ 1.8 mm is 100 % perimeter; a 1.8 mm rib is stronger than 15 % infill), T‑ and I‑sections instead of hollow slabs, gussets at hook roots, full‑radius fillets at every stress concentration, generous section on flexing features. Avoid large enclosed volumes in the load path.
- Parts break between layers ("like wood splitting along the grain"): orient so main loads, and the bending of latches and hooks, run along the layers. A slender handled part (a mop handle) prints lying flat; upright it snaps.
- Bed adhesion and support are built in, not delegated: brim ears as a parameter for tall or narrow parts, in‑built supports where unavoidable (§5.1).
- Check by hand estimate for anything load‑bearing (bending stress at the root, strain of flexing features — §5.2) and record it in the README; the physical load test (§10.4) confirms.
- Post‑processing: remove brim ears and stringing, deburr sharp edges (a deburring tool is in the kit), then QC.

### 5.6 Material selection
MSF suitability table (✓ suitable · ! moderately suitable, consult · X not suitable) (MSF):

| Requirement | PLA | PETG | PC | TPU |
|---|---|---|---|---|
| Decorative parts | ✓ | ! | X | X |
| Small detailed parts < 1 cm | ✓ | X | ✓ | X |
| Large parts > 20 cm | ✓ | ✓ | ! | ! |
| High mechanical stress | X | ✓ | ✓ | ✓ |
| High impact stress | X | ! | ! | ✓ |
| Temperature > 50 °C | X | ! | ✓ | ! |
| Temperature < 0 °C | X | ✓ | ✓ | ✓ |
| Contact with chemicals | ! | ! | ! | ! |
| Sterilization needed | ! | ! | ! | ! |
| Outdoor use | X | ✓ | ✓ | ✓ |
| Indoor use | ✓ | ✓ | ✓ | ✓ |

- **The design is not tied to one material.** Ask what is actually on the shelf (Round G), design so the part works in the weaker plausible candidate, and list the acceptable materials in the README in order of preference with the difference each makes ("PETG preferred; PLA acceptable indoors below 40 °C; TPU not needed"). Mark nothing "(recommended)" before the shelf is known; confirm the answer again before the brief — a withdrawn "TPU available" changed a wheel design after the brief was written.
- Field practice as a starting point: hospital and lab items are usually PETG in white, natural or a light colour — the light colour is an IPC rule and stays whatever the material; training and office items PLA; flexible or impact TPU; above 50 °C PC / PC Blend (advisor); heavily disinfected surfaces (Ebola treatment centres) PP‑GF (field) — some filaments such as PP‑GF survive autoclaving, advisor only; outdoor and UV PETG, or ASA via the advisor (not in the MSF table).
- MSF kit filaments: PLA and PETG (basic); ASA, PC Blend, PC‑CF, PETG V0, TPU (advanced); PP‑GF, PP‑CF and TPU 95A being added — the kit list says what could be there, the shelf says what is.
- One material family per part: PLA and PETG do not bond reliably; colour changes stay within PLA or within PETG (project).
- Fine details under 1 cm: not in PETG; heat‑exposed parts: not in PLA (MSF).
- Wording: filament "absorbs moisture from the air" — never "wet" (field). No chemical‑resistance tables in any deliverable (field).

### 5.7 Large items and modularity (MSF)
- Split anything larger than 200 mm into sections joined by glue, bolts or snap‑fit connectors, with alignment features (pins and sockets or keyed joints) at every split.
- Complex designs are modular so single parts can be reprinted. Design as simple as possible, without unnecessary features; keep material use and print time low.



<!-- ===== references/openscad-environment.md ===== -->

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



<!-- ===== references/ipc-and-hospital.md ===== -->

# IPC and hospital-environment rules

*Reference file of the `msf-3dp-design` skill. Read it for every item used in a hospital or laboratory, or that is ever cleaned.* Section numbers (§) are those of the compiled workflow file (CLAUDE.md v1.2) and are kept so that cross-references stay valid: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · Appendix A glossary.md · Appendix C sources.md.

## 8. IPC and hospital‑environment rules

### 8.1 Surfaces and geometry (clinical items and anything that gets disinfected)
- No text, logos, embossed or engraved symbols — recesses trap contaminants. Identification lives in documentation and packaging. Embossed text is fine on non‑clinical items that never need disinfecting (field).
- Rounded, smooth, wipeable geometry: no sharp internal corners, crevices, slots or pockets a wipe cannot reach; smooth waves instead of zig‑zags; fillets over sharp edges (vaccine carrier insert: rounded wavy walls, only the wave tips touch the ice packs).
- (default) Internal concave corners filleted ≥ 1 mm; no blind holes or closed cavities that can hold fluid; perforations sized for a wipe or brush; no decorative texture or fuzzy skin.
- Keep contents clear of fluids where relevant (a removable honeycomb floor keeps items above melt water).
- **Drainage:** any holder, pocket, tray or socket with a closed floor, and any blind socket that opens upward in use, carries a chamfered drainage hole as a parameter — `drain_d`, default Ø 6 mm (+0.2 mm) for pockets, Ø ≥ 2 mm for stem sockets, 0 = none — at the lowest point of the floor, unless the brief says the floor must be closed (owner decision, September 2026).
- Design for disassembly: parts that get dirty come off tool‑free for cleaning (UMS front parts slide out of the back part; removable floors and inserts with a loose fit).
- Design out knife edges and thin flashes that post‑processing would have to remove; deburring stays mandatory.
- "Design for removability and limited wear" (MSF). Layer lines trap particles — prefer smooth, open, easily wiped surfaces on anything that is cleaned.

### 8.2 Materials, colour, disinfection
- PETG default; white, natural or a light colour on purpose — soiling and defects stay visible. This is an IPC feature, not cosmetics; never recommend dark filaments for clinical parts.
- Do not autoclave PETG — it deforms. "Autoclaving 3D printed items is generally very difficult" (MSF): never design for autoclaving. PP‑GF for heavily disinfected surfaces; autoclavable filaments only via the 3D printing advisor.
- Disinfection agents at MSF: Surfanios, bleach (1:10), IPA. In new guidance prefer IPA over ethanol 70 %; where an existing document lists agents (UMS V1: Surfanios, bleach 1:10, ethanol 70 %) stay consistent with it. Choose a material that resists the intended method; UV‑C only where the requester's IPC team uses it.
- Skin contact (ISO 10993, MSF): PLA or PETG is acceptable for limited contact (up to 24 h cumulative); prolonged or long‑term exposure needs justification and testing — flag for IPC.
- Mucosal contact (items placed in the mouth): only under §4.1b. It is a separate ISO 10993 contact category — the material, its batch record, the single‑use or reprocessing regime and the biocompatibility justification come from the guideline entry, never from the general filament stock.
- Parts needing sterilisation or disinfection, and parts in direct contact with the user (below or above 5 minutes), need IPC advisor consultation — flag in header and README.

### 8.3 Application rules
- The README states the intended use **and** the out‑of‑scope uses. Mounting accessories are not patient‑support devices: never a grab bar, handhold, restraint point or lifting point.
- Compatibility is explicit: list the exact devices and interfaces with diameters (UMS V1: tubes Ø19 / 25 / 32 mm, poles 20 / 25 mm, humidifier bottles Ø49 / 56 mm); expose them as parameters; never silently round to a size.
- Falling‑equipment hazard: consider where the device lands if the part fails; prefer retention features (safety locks, latches, lips, kept front edges) that stop accidental disconnection; advise positioning away from patients, cots and walkways.
- Hardware: commodity parts only (§5.4).
- Ageing: PETG latches and hooks become brittle over time. Generous section and radius; support the in‑service check (no cracks, surface clean, latches still flexible); replacement by reprinting is the normal corrective action.
- Traceability lives in logbooks, not on the part. NFC pockets (§9.2) only on larger non‑mechanical, non‑clinical items, and only when requested.
- Generated documents (README, DATASHEET, headers, renders) carry no licence statements, certification marks, badges or UIDs — they are internal MSF documents, and such marks would mislead (owner, Sept 2026).
- Storage of spares: sealed zip‑lock bags, room temperature, away from sunlight and humidity.



<!-- ===== references/compatibility-and-markings.md ===== -->

# Compatibility systems, text, colour bands, stands

*Reference file of the `msf-3dp-design` skill. Read it for UMS or HomeRacker work, and for any non-clinical item with text, colour bands or a stand.* Section numbers (§) are those of the compiled workflow file (CLAUDE.md v1.2) and are kept so that cross-references stay valid: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · Appendix A glossary.md · Appendix C sources.md.

## 9. Compatibility systems, text, colour bands, stands

### 9.1 UMS‑compatible hooks, holders and clamps
- Every holder = **back part** (bed rail, pole, trolley, wall) + **front part** (holds one specific device), sharing the common sliding interface. Treat the interface geometry and its tolerances as a fixed standard: import or copy it from the reference design, never redraw it approximately — any change breaks interchangeability.
- Fit target: the front part slides into the back part easily yet holds firmly — no rattle, no forcing. The device seats stably and stays easily removable. Verified before installation.
- Hook back parts: tube diameter, hook opening, wall thickness and the optional 6 mm zip‑tie stabiliser are parameters; brim in the print notes.
- "Universal" attachment options as selectable modules: back holes, side wings with 3–10 mm holes (wings may use up to 60° overhang, by brief), horizontal and vertical pole clamps, zip‑tie channels, hooks, DIN rail. Holder body: rectangular with filleted vertical edges; each wall solid or hex‑perforated; front wall removable but with a retaining edge so items stay in (project).
- HomeRacker‑compatible parts: 15 mm unit pitch, 4 mm square lock‑pin holes, BOSL2 (§6.5) (project).
- **Copying the interface (extraction recipe):** clone the UMS V1 repository; cross‑section the reference STL with trimesh at several heights and read the exact values; check the STEP with a grep of `CARTESIAN_POINT`; take the print orientation of every part from the `.3mf` plate (`Slic3r_PE_model.config` maps object ids to file names). Values read from the July 2026 STEP/STL files: socket 44 × 4 mm; slot 27 / 35 × 4 mm with 45° flanks, open at the bottom, 45° closing ramp 6 → 2 mm below the top, detent dimple R1.3 sunk 0.8 mm at 33 mm below the top; tongue 31 × 4 mm, neck 26 mm, 4 mm chamfered tip, bump 1 mm. The July 2026 drawing says 40 / 30.6 mm — an open question for the advisor; the printed files are followed. Hard‑code the values in a `[Hidden]` block with the source file and date; build the mating tongue as a `%` ghost from the same numbers; ship a socket‑only coupon (`part = "socket_test"`, ≈ 40 min) that checks the site's printer, not the geometry; verify with T18. A 0.2 mm sliver in a reference STL is a CAD artefact to ignore, not geometry to copy.

### 9.2 Text, markings, NFC — non‑clinical, non‑disinfected items only

| Feature | Rule | Source |
|---|---|---|
| Font | Sans‑serif only: Liberation Sans Bold, capitals | (MSF) (project) |
| Letter height | > 6 mm (MSF). The training set uses size 5 (≈ 4.8 mm capitals, 1.0 mm strokes) where a larger plate is impossible — recorded as a deviation | (MSF) (project) |
| Depth or height | 0.6–1.0 mm; never more than 1 mm | (MSF) |
| Text on vertical faces | > 0.9 mm wide, < 2 mm high | Hydra |
| Strokes | ≥ 1.0 mm on a solid base; pictogram strokes and openings ≥ 1.2 mm; pictograms are simple filled shapes | (project) |
| Plate sizing | Measure the longest string with the real font first; enlarge the plate, never shrink the text below the stroke minimum; put labels where there is width (a nameplate, not an 18 mm chest) | (project) |
| Symbols | No cross symbols — easily confused with the protected red cross emblem | (project) |
| NFC pocket (round NTAG213, Ø18 mm) | 19 × 19 × 1 mm, tag not deeper than 1 mm below the surface; "SCAN HERE" debossed 0.2–0.4 mm; larger non‑mechanical items only | (MSF) |

### 9.3 Colour by layer bands (single extruder, manual filament changes)
- At most three colours per part; colour changes only between layers. Base ≥ 2.0 mm (10 layers); every colour after a change ≥ 0.6 mm (3 layers).
- Standard flat‑part bands: Band 1 Z 0–2.0, Band 2 Z 2.0–2.6, Band 3 Z 2.6–3.2 mm. The same heights on every flat item, so different items share a plate and one colour‑change plan.
- A detail is either raised into a higher band or shown as an opening that reveals the colour below. **Nothing may cross a colour‑change height except the detail meant to be that colour**: put raised text on the highest surface (bed number on the footboard top, with no other feature higher).
- Colour cannot be split side by side in a flat part: full‑silhouette base plus a top overlay offset ≈ 1.6 mm from the edge so the outline stays visible (blood in a culture bottle).
- Colour changing along the height of a standing object (figures, signs): print it flat and stand it in the universal stand via the standard tab.
- Slicer: insert the change on the first layer above the boundary (the layer shown as 2.20 mm for a 2.0 mm boundary); slice banded parts at 0.2 mm so boundaries fall on layer lines. A light colour over a dark base at 0.6 mm can look tinted — band heights stay parameters and are checked on the first test print.

### 9.4 Stand and tab (standing flat parts)
One universal stand for every standing flat part; every such part carries the same tab (30 × 8 mm, Band 1 only, 2.0 mm thick). Slot = tab + clearance (0.3 mm default) with a 0.4 mm entry chamfer; an 8 mm deep slot limits wobble to about 2°. Stand width matches the nameplates and signs it carries. **Test what can vary**: the tab thickness is fixed by the base band, so the coupon varies the slot width, not the tab.



<!-- ===== references/verification.md ===== -->

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



<!-- ===== references/deliverables.md ===== -->

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



<!-- ===== references/readiness-levels.md ===== -->

# Readiness levels — Humanitarian Making scale (verbatim) and the MSF interpretation

*Reference file of the `msf-3dp-design` skill. Read it when filling the readiness fields of the DATASHEET.* Source: https://humanitarianmaking.org/resource/readiness-levels (text supplied by the owner on 26 September 2026, reproduced as published). The five readiness fields of the MSF datasheet use this scale **exactly as defined here** — never paraphrased, extended, renumbered or interpreted beyond the MSF rules at the end.

## Rules
1. Quote the level's published wording next to its number in the DATASHEET, plus one line of evidence from this design (what has been tested, by whom, where).
2. Apply the MSF interpretation (last section) — it narrows the choice, it never replaces the definitions.
3. Every level is "proposed" until the 3D printing advisor confirms it. If a scale cannot be applied with what is known, write "to be assessed by the 3D printing advisor on the Humanitarian Making scale" — no guess.

## Readiness Levels (as published)
Product development encompasses a number of concerns that are not always easily captured in saying that something is "ready." Four separate readiness scales are listed for each item in this catalog along with a consideration of risk. The five categories are explained below along with the readiness scales on the following provides users of this catalog with a clear understanding of how the system works.

**Field readiness level** — This measures the degree in which an item is suitable for life saving situations. It is a key quality that sets items apart in humanitarian contexts.
**Maker readiness level** — This is an indication of the relative ease in making the item as it relates to the complication and skill involved.
**User readiness level** — This is a measure of the end users acceptability of the item considering issues such as whether it is already commonly used, if the item is in an existing catalog and when there are established standards for its use.
**Technology readiness level** — This is an indication of the development process that the item is in (e.g., whether it is at a conceptual stage or available for replication and widespread use).
**Risk level** — This is a measure of severity and likelihood of the risk involved for the maker and end user of the item. The mitigation and control measures are documented by Field Ready in separate risk assessments for

### What makes a product 'field ready'?
Five criteria determine the level of an items field readiness
- **Essential** — Needed in a humanitarian, recovery, or development context. The item is vital and there would be issues if it is not available.
- **Quality & Safety Checked** — All items are assessed for risk and reasonable standards (e.g. US FDA) should be met.
- **Easy to use** — It should be intuitively designed and exactly fit for purpose. Usable with as little training as possible, and ideally, locally repairable.
- **Robust** — Optimized to function in a field context, with design features such as strength, shock resistance and ability to survive moisture or dust.
- **Replicable** — For widespread use it should be affordable, adaptable to different contexts, well documented, and with no intellectual property restrictions.

**Field Readiness Level**
| Level | Definition |
|---|---|
| 1 | Item is not field ready, better suited to clean and stable uses or situations |
| 2 | Item meets some criteria but significant change needed |
| 3 | Item meets most criteria but still room for marked improvement |
| 4 | Item is field ready in most situations although improvement still needed |
| 5 | Item is very well suited to the field and optimized for such conditions |

### How is 'maker readiness' measured?
This category indicates the level of complication in 'making' (i.e. manufacturing or fabricating) a particular item. It captures a sense of the degree of knowledge, skill, technical input and sophistication of tools and equipment needed to reproduce the item. All levels are relative.

**Maker Readiness Level**
| Level | Definition |
|---|---|
| 1 | Expert knowledge backed with extensive experience. Highly specialized and sophisticated equipment needed. Knowledge on replication requires advanced skills |
| 2 | High degree of training or prior knowledge required. Tools or equipment needed may be a high level of sophistication. Knowledge on replication requires advanced skills |
| 3 | An increased amount of training or prior knowledge required. Tools or equipment may be needed or required. Knowledge on replication is passed on simply |
| 4 | Some training may be needed to successfully make the items. Tools may be required but may be basic or readily available. Knowledge on replication is passed on simply |
| 5 | Very little to no training or prior knowledge required. Few if any tools or equipment needed. Knowledge on replication is passed on simply |

### What makes a product 'user ready'?
Five criteria determine the level of an item's user readiness (wording as published on the site)
- **Commonly used or needed** — Needed in a humanitarian, recovery, or development context. The item is vital and there would be issues if it is not available.
- **Meets or exceeds standards and/or user demands** — All items are assessed for risk and reasonable standards (e.g. US FDA) should be met.
- **In existing catalogs** — It should be intuitively designed and exactly fit for purpose. Usable with as little training as possible, and ideally, repairable locally.
- **Suitable replacements alright** — When appropriate, the design and/or process is acceptable to the end users.
- **Desirable** — For widespread use it should be affordable, adaptable to different contexts, well documented, and with no intellectual property restrictions.

**User Readiness Levels**
| Level | Definition |
|---|---|
| 1 | Item is unlikely to accepted by end users |
| 2 | Item meets some criteria but significant work needed |
| 3 | Item meets most criteria but still room for marked improvement |
| 4 | Item is field ready in most situations although improvement still needed |
| 5 | Item is very well suited to user needs, it is highly desirable and likely to be used as intended |

### What indicates 'technology readiness'?
Technology readiness is a measure referring to the stage of an items maturity. Our Technology readiness considerations are based on a scale of 1–5 and take into consideration safety concerns. Please refer to the scale on each item.

**Technology Readiness Levels**
| Level | Definition |
|---|---|
| 1 | Basic idea is noted and recognized, beginning application of research and development. The invention is still speculative. |
| 2 | Active research and development is initiated. This includes analytical studies and laboratory studies to physically validate analytical predictions of separate elements of the technology. |
| 3 | Concept designs come to fruition through basic components that are tested first in a lab setting, than in a controlled environment. The next iteration tests the entire system in a simulated environment. |
| 4 | At this level the prototype is tested in an operational environment, in or near where it will be used (alpha and beta testing). |
| 5 | Prototype is proven through successful operations, it is available for intended users. |

### How is the degree of 'risk' measured?
A number of questions are used to assess risk for both those used in making the item and, especially, the end user:
- **What are the hazards involved?** Consider all hazards that exist, regardless of severity, likelihood or existing controls. For example, anything that is used in the preparation or transport of food or drink carries a hazardous substances risk, as it could ultimately be ingested and be toxic or cause infection.
- **What are the vulnerabilities?** How the hazard may have an outcome if there is an accident or negligent use, and what will the result may be. Examples include but are not limited to burns, cuts, falls or anything that may cause harm, including death.
- **What is the severity and likelihood?** Consider the impact and frequency the hazard may take place.
- **What are the control and mitigation measures?** What can be done to lessen or prevent the hazard. Controls that eliminate hazards are preferable to measures that create barrier, such as safety guards or personal protection equipment.
- **Additional considerations?** Is there anything else that should be considered particularly from the end users perspective such as risks that emerge through 'wear and tear' and any other unintended consequences. Is the risk of not providing the item outweigh any other risks?

**Risk Levels**
| Level | Definition |
|---|---|
| 1 | Very high risk: Item and/or process has multiple risk concerns. |
| 2 | High risk: Item and/or process has some risk concerns. Take extra measures to reduce risk. |
| 3 | Elevated: Item and/or process has a few risk concerns. |
| 4 | Moderate: There may be an concern regarding the use or making process of the item. |
| 5 | Low risk: Few if any risk concerns. |

## MSF interpretation (owner rules, 26 September 2026) — applied on top of the definitions
| Situation | Level |
|---|---|
| The item is critical (§4.2) | Risk level 3, 2 or 1 — never 4 or 5 |
| The item is a single 3D-printed part, nothing else | Maker readiness 5 or 4 |
| The item needs bolts, nuts or other easily, locally available materials | Maker readiness 4 or 3 |
| The item needs other technologies, special materials or special filaments | Maker readiness 3 or 2 |
| Very complex products | Maker readiness 2 or 1 — such items are not made in the field |

Within the band the rule gives, choose the level whose published wording fits the evidence; say which evidence. Field, user and technology readiness follow the definitions only: a first design that has not been printed at its site is at most technology readiness 3; after the first article and the follow-up checks it can be 4; 5 needs proven use.


<!-- ===== references/lessons.md ===== -->

# Lessons-learned register

*Reference file of the `msf-3dp-design` skill. Read it when a design resembles a past one, and add a line after every test print, review or user correction.* Section numbers (§) are those of the compiled workflow file (CLAUDE.md v1.2) and are kept so that cross-references stay valid: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · Appendix A glossary.md · Appendix C sources.md.

## 13. Lessons‑learned register
Add a line whenever a test print, a review or a user teaches something. Each line names the project and the rule it changed or confirmed.

| Project | Lesson → rule |
|---|---|
| Tube and hose connectors | Print standing; all connector ends in one plane; 45° whichever end is on the bed; every grip dimension user‑definable, never auto‑derived; `check_overhang.py` became the standard overhang test (§10.1 T7) |
| Universal holder | Attachment options as selectable modules; wings may need 60° — only by explicit brief; the removable front wall keeps a retaining edge; work split into sub‑tasks with outputs after a complete design plan |
| Vaccine carrier insert | Export selector menu instead of separate STLs; removable honeycomb floor (8 mm, 8 mm hexagons) with a 0.8 mm loose fit keeps contents above water; wavy walls with only the wave tips touching, rounded for IPC |
| Tabletop simulation set | Measure string widths with the real font before fixing plate sizes; record every interpretation ("1 cm bigger" = height); colour cannot split side by side in a flat part; one stand plus a standard tab; the coupon varies the slot, not the tab; slender handled parts print flat; no cross symbols; enlarge tokens for handling; stage work by context size |
| HomeRacker plate | BOSL2 only to match a system that uses it; conditional features (recess) guarded by `assert()` with the allowed ranges; ghost frame in preview |
| UMS V1 | The sliding interface is a fixed standard; light colours are an IPC feature; in‑built supports; explicit compatibility diameters; positioning advice against falling equipment; periodic checks for brittleness |
| Ebola lab pilot (Beni) | PP‑GF for heavily disinfected surfaces; autoclavable filaments only via the advisor |
| Hospital 3D printing SOP (KTP) | Procedures must be simple to be followed; keep records minimal but present |
| Field practice | No glue on print sheets; filament "absorbs moisture"; no chemical tables; IPA preferred to ethanol 70 % in new guidance |
| Training set — stage 1 test print | Slot clearance for the 2.0 mm tab: default 0.3 mm — *to be confirmed*; colour band over a dark base 0.6 mm — *to be confirmed* |
| Owner decisions, Sept 2026 | Items placed in the mouth are restricted (§4.1b), not forbidden, pending guideline updates; food, drink and medicine contact only through primary packaging; personal data in uploads is stripped before use (§1.5) |
| UMS pulse oximeter holder (Masimo Rad‑5) | Run §3.2 before Round A when a device or system is named — the UMS repository already held the F3 holder; copy a fixed interface from the printed files by cross‑section and verify numerically (drawing 40 / 30.6 vs files 44 / 31 → open question); a validated design's files are an acceptable dimension source; ask where cables exit (top, not the assumed bottom); socket‑only coupon; CGAL boolean hygiene (extend 0.2, overlap 0.05, chamfer 0.01 larger than fillet); swept edge profiles instead of body‑wide minkowski; open‑front corner R ≤ wall_t/2; defaults must pass the guards; second overhang pass at 0.02 mm²; drainage hole requested after seeing the render |
| Handwashing tap‑lever pusher | Ask whether the mating part can turn or loosen (a tap on its thread) — found late, forced a redesign; one label = one dimension; confirm the layout before drawing a measuring guide (the tube was drawn on the wrong side); abrupt ends on the upward‑facing side; self‑centring V + 2 mm clearance + flared mouth; clash test and section check; a cut‑through render caught a crevice every automated check missed; multi‑hole notched coupon for a push fit on rusty tube; asserts with float tolerance; guards only for impossible geometry |
| Concentrator twin caster (DeVilbiss 525DS) | "Make a spare wheel" → find the OEM spare first (501DZ‑603); decide scope per component — a printed stem and fork refused, a twin‑wheel body on the original steel stem with an M6 bolt axle accepted as a critical draft; state failure consequences concretely ("corner drops 50 mm", not "tips over"); ask for the user's concept rather than repeating a refusal; lettered measuring diagram and consistency check; confirm filament on the shelf; bolt shank length and nut type; wire retention for a narrow groove; drain in blind sockets; bathroom‑scale load test; building ahead of the coupon allowed, releasing not |
| OT scavenger exhaust adapter | A one‑line request took four rounds — ask "made before?" first; gas‑path position relative to relief valve and filter decides the scope; fail‑open design, no 15/22 mm ends, system risks in the risk assessment, anaesthesia lead in the approval; 1:40 taper modelled, tapered sleeve bore on straight PVC; state tapers in the hand‑off; nominal value + bracketing coupon when the user will not measure; the checker ignores CGAL slivers < 0.001 mm²; raise IPC observations seen in photos (a dark‑filament clamp in theatre) |
| Glucometer battery cover | Overlay the exported outline on the user's photo and get it confirmed before modelling (two re‑traces avoided); label nested edges and ask which is the boundary; fit primitives and cross‑check; photos give no depth; fit‑trial release with an outline check plate when the device is inaccessible; short snap features on thin covers are stiff clicks, not springs; `-D` for a removed parameter is silently ignored |
| D‑shaft knob (replica, PLA) | Read back every sketch view and dimension — hand sketches are not to scale, written numbers govern; undimensioned flare → estimated parameter + overlay; minimum wall computed along Z under the flare (1.27 modelled / ≈ 1.3–1.4 printed, accepted for a moulded replica); cone roof on blind bores, short documented bridge on the ledge to keep the D‑flat engagement; tight‑fit coupon 0.00–0.30/side — PLA D‑bore on Ø6 steel = 0.15/side (*to confirm*), counterbore +0.2 (the default hole compensation was right); implicit approval for a non‑critical item, stated; deliver a zip; context renders (installed, exploded, section) |
| Owner feedback, Sept 2026 (six test designs) | Foolproof strength — design for 2 perimeters / 15 % infill; a drawing with every request for information; the scope gate warns instead of blocking; materials from the shelf, not from the design; test‑before‑use protocols, with test to failure for critical items or batches; standard render set with context views; coupon alongside the product, never before it; STLs in print position; drainage hole option for closed holders |
| Owner feedback 2, Sept 2026 (skill v1.3) | Renders were slow → OpenSCAD 2025.07 with Manifold via npm `openscad-wasm` (`openscad-fast`), 4–22× faster, measured; ask all questions at the start and build in one pass, clicking wherever possible; no licence or certification text in generated documents; README short and visual, details in DATASHEET.md; readiness only on the Humanitarian Making scale, verbatim; context limits hit → token discipline (§1.6); every part also as a one‑file Customizer version per the MSF customizer standard; follow‑up after installation at 2 weeks, 1 month, 3 months minimum, validated by the 3D printing advisor; brims and supports built in only when the geometry cannot be changed; N identical items → N numbered STL files |



<!-- ===== references/glossary.md ===== -->

# Plain-language glossary

*Reference file of the `msf-3dp-design` skill. Read it when explaining a term to a user — reuse this wording.* Section numbers (§) are those of the compiled workflow file (CLAUDE.md v1.2) and are kept so that cross-references stay valid: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · Appendix A glossary.md · Appendix C sources.md.

## Appendix A — Plain‑language glossary (reuse this wording with users)
- **FDM / FFF printer** — a printer that melts plastic filament and lays it down in thin layers.
- **Layer height** — thickness of each layer; we use 0.2 mm.
- **Perimeter** — the outer wall lines of each layer; more perimeters = stronger part.
- **Infill** — the pattern inside the part; a percentage of solid.
- **Overhang** — a part of the model that would hang in the air while printing; up to 45° from vertical prints cleanly.
- **Bridge** — a horizontal stretch printed across a gap; short ones work, long ones sag.
- **Support** — extra material the slicer adds under overhangs; we design so it is not needed.
- **Brim** — a flat ring around the base that helps the part stick to the plate; removed after printing.
- **Elephant's foot** — the slightly widened first layers; a small chamfer at the bottom edge avoids it.
- **Chamfer** — a cut‑off edge at 45°. **Fillet** — a rounded edge.
- **Clearance / tolerance** — the small gap that lets two parts fit together; too small = forcing, too large = rattle.
- **Print orientation** — which face of the part lies on the plate; it decides strength and quality.
- **STL / 3MF** — the file the slicer reads. **Slicer** — the program (PrusaSlicer) that turns the file into printer instructions.
- **Customizer** — the panel in OpenSCAD where you change sizes with sliders and menus without touching code.
- **Manifold / watertight** — the model is a closed solid without holes; slicers need this.
- **PETG, PLA, TPU, PC** — plastics: PETG tough and disinfectable (hospital default); PLA easy but soft in heat (training); TPU flexible; PC heat‑resistant.
- **IPC** — infection prevention and control.
- **Personal data** — anything that identifies a person: names, patient numbers, dates of birth, faces, wristbands, screens with records, and hidden photo data such as GPS. Never needed for a design.
- **Primary packaging** — the sealed container that touches the medicine or food itself: vial, ampoule, blister, bottle, sachet, tube. Printed parts may touch the packaging, never the contents.
- **Outline overlay** — the planned shape drawn as a coloured line on your own photo, so you can check at a glance that it follows the real edge.
- **Coupon** — a small test piece with several sizes of the same hole or slot; you print it in minutes, find the step that fits, and tell us its code.
- **Test to failure** — loading one sample until it breaks, to learn the limit and how it breaks; done for critical parts or big batches, not for every part.
- **Brim ears** — small tabs built into the model at the base for adhesion; you snap them off after printing.
- **Manifold** — the new geometry engine inside recent OpenSCAD builds; same result as the old one, many times faster.
- **Customizer file** — the one‑file version of a part whose sliders and menus you can change in OpenSCAD or in the MSF customizer catalogue without touching code.
- **Follow‑up check** — looking at an installed part again on a schedule (2 weeks, 1 month, 3 months) for cracks, wear and loosening, before deciding to keep, reprint or redesign it.



<!-- ===== references/sources.md ===== -->

# Sources and references

*Reference file of the `msf-3dp-design` skill. Read it when citing a rule or pointing a user to further reading.* Section numbers (§) are those of the compiled workflow file (CLAUDE.md v1.2) and are kept so that cross-references stay valid: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · Appendix A glossary.md · Appendix C sources.md.

## Appendix C — References
- MSF 3D Printing Process Guideline V1.1 (internal): Part 2 Printability Assessment, Part 3 Design Acquisition, Part 4 Production.
- MSF Universal Mounting System V1: https://github.com/MSF3Dprinting/Universal-Mounting-System — MSF Printables profile @3Dprintingforall.
- OpenSCAD downloads (stable and development snapshots): https://openscad.org/downloads.html
- OpenSCAD user manual: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual — Customizer: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Customizer — cheat sheet: https://openscad.org/cheatsheet/
- OpenSCAD source and issues: https://github.com/openscad/openscad
- BOSL2 (only when matching a system that uses it): https://github.com/BelfrySCAD/BOSL2
- Hydra Research, Design Rules for FFF 3D Printing: https://www.hydraresearch3d.com/design-rules
- Prusa Knowledge Base, Modeling with 3D printing in mind: https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135
- PrusaSlicer command line: `prusa-slicer --help` (the wiki page is no longer maintained): https://github.com/prusa3d/PrusaSlicer
- trimesh (Python mesh checks): https://trimesh.org
