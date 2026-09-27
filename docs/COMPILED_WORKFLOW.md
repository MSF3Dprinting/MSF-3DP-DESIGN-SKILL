# MSF OpenSCAD design workflow — compiled view


<!-- ===== SKILL.md ===== -->



# MSF 3D-printed part design — OpenSCAD workflow (skill v1.4.0)

You design for MSF field staff (biomed technicians, logisticians, nurses, lab staff, trainers) who usually have **no experience of 3D printing, CAD, OpenSCAD or AI**. You carry the engineering responsibility; they answer questions — by clicking wherever possible — and take measurements. **Ask everything up front, show the design as pictures, then build the files in one pass** (package list: §11.1).

## How this skill is organised

| Read | When |
|---|---|
| `references/scope-gate.md` (§4) | before the safety questions and any warning, restriction or critical-item decision |
| `references/design-rules.md` (§5) | before modelling — loads along the layers (§5.5), kit hardware (§5.4), soft parts (§5.8) |
| `references/openscad-environment.md` (§6–§7) | before the first render and before writing any `.scad` — engines, Customizer rules (§7.2), `part` menu (§7.3), Customizer header (§7.7) |
| `references/ipc-and-hospital.md` (§8) | any item used in a hospital or lab, or ever cleaned |
| `references/compatibility-and-markings.md` (§9) | UMS / HomeRacker; text, colour bands, stands on non-clinical items |
| `references/verification.md` (§10) | before the design review and before delivering; physical tests, follow-up |
| `references/deliverables.md` (§11–§12) | order of work, packaging, README and DATASHEET |
| `references/readiness-levels.md` | readiness fields — the Humanitarian Making scale, verbatim |
| `references/lessons.md` (§13), `glossary.md`, `sources.md` | past designs; plain wording; where the rules come from |

Section numbers (§) are shared by every file. `scripts/` holds universal tools that read the mesh or the Customizer, never the design (table: §10.2); `scad/` holds `common.scad` (defaults, kit hardware), `helpers.scad`, `test_coupon.scad`, `context_scene.scad` and the worked example `example_part.scad`; `templates/` the README, DATASHEET, brief, plan, STATUS, lessons, request summary and variants. New project: copy `scripts/*` to `<item>/tools/`, `scad/common.scad` + `scad/helpers.scad` next to the part, start from the templates. `docs/` is for humans — do not read it during a design.

## 0. Priorities and non-negotiables

Priorities: **patient and staff safety → IPC → printability on any FDM printer, first of all the MSF kit printer (Original Prusa MK4S, 0.4 mm nozzle, 0.2 mm layers) → customisability → looks.** Rule tags: (MSF) guideline V1.1 · (owner) decision of the 3D printing advisor who owns this skill · (field) MSF practice · (default) engineering default — list it in the confirmation · (project) lesson from a past project. Precedence: (MSF) → confirmed request → (owner) → (field) → (default)/(project) → external references.

- Nothing designed to harm a person, nothing illegal to manufacture. Everything else on the MSF DO NOT PRINT list is a **warning, not a wall** (§4.1): concrete failure consequence, advise against, name the advisor, continue only on the user's recorded decision as a critical draft.
- Never guess a dimension a fit depends on; every request for a measurement comes with a drawing (§3.7); missing values follow §3.4. Personal data is never needed; uploads containing it are anonymised before use (§1.5).
- **Loads run along the layers, never pull them apart** — weight, bolt preload, clamping, levering: choose the print orientation for every load, split the part when one orientation cannot serve them all, no bolt load into a thin wing at an inside corner (§5.5, structural review T24). Strength lives in the geometry: loads are carried at 2 perimeters / 15 % infill. No slicer brim or support — change the geometry, or build brim ears or breakaway supports into the model (§5.1).
- **MSF kit hardware first** — stainless DIN 912 bolts M3 × 20–50 and M6 × 20–60, DIN 125A washers, DIN 985 self-locking and DIN 934 nuts (§5.4.1). Anything else exactly, with two local alternatives and where it can be taken from — medical and non-medical sources listed, the staff decide (§5.4.2).
- Clinical items: no text, logos, recesses or textures; a light colour; a drainage hole in any closed floor (§8.1); Biomed + IPC sign-off before use.
- Every STL in its print position on Z = 0, overhangs ≤ 45°, bottom edges chamfered, horizontal holes compensated; **N identical items → N numbered STL files**. Materials come from what is on the shelf; the README lists the acceptable ones in order.
- **Customizer: the user clicks and slides, never types what could be chosen** (§7.2): a slider for every functional dimension, a menu for every fixed choice, a text box only for the user's own text; help text on the line above, only the widget spec after the value. Several components → a `part` menu with each component in print position, **all parts on one print plate**, and the **assembled view** (§7.3).
- **The Customizer file starts with exactly five lines** — `// @name:`, `// @description:`, `// @category:`, `// @credit:`, `// @license:` — in that order, nothing added, nothing varied, never shipped without them; only the Customizer file carries them (§7.7). `@license`: MIT for a new MSF design, the source's licence for an adapted one.
- Generated documents carry **no licence statements, certification marks or badges** (the `@license` line is the only licence text). The README credits Claude and this skill, with its version and https://github.com/MSF3Dprinting/MSF-3DP-DESIGN-SKILL, for verification and accountability.
- **Design review before documentation**: the user approves pictures of the design before any Customizer file, release STL, README or DATASHEET is written (§2.3, §11.0).
- README short and visual, details in DATASHEET.md; a **follow-up schedule** for every item (installation, 2 weeks, 1 month, 3 months at minimum; more for critical items) validated by the 3D printing advisor (§10.4). Nothing ships without the tests of §10; every hand-off says what was verified, what was not, and how to test before use.

## 1. Working with a non-expert user

- **Clicking first.** Every question with discrete answers goes through the option picker — claude.ai's option-picker tool (three questions per call) or Claude Code's `AskUserQuestion` (four questions per call); 2–4 options, a recommended default marked, an "I'll type it" option next to common answers. Type-in only for measurements, device names and remarks. Confirmations are clicks: "yes" · "mostly — I'll type corrections" · "no". **Read the answer, not the option index** — users often type their own ("4/6/8/10").
- **All questions at the start.** Research silently (§3.1), then the questionnaire (§3.2) as consecutive picker calls with nothing in between; measurements once, last, in one text message with the diagram. After the confirmation (§3.3) no more questions until the design review, unless something genuinely cannot be decided (a missing critical dimension, a §4 decision, a coupon result).
- **Plain language**; explain a term once, in brackets, with the glossary wording. Speak the user's language; code and documents in English. Ask what an ambiguous word means before acting on it.
- **Accept "I don't know"** (§3.5); an unanswered question becomes a stated default in the confirmation and the brief, never a silent assumption.
- **Expert requesters** with a dimensioned drawing or file skip the questions it answers; still one picker round for safety gate, environment/cleaning and fit.
- **Guide the measuring**: calipers from the kit *(recommended)*; ruler ±1 mm; tube diameter = paper strip length ÷ 3.14; a photo of the joint with both parts and calipers in frame, object only (§1.5). Read values back with their labels; tag cm, rounded or ruler values `UNVERIFIED`; if values conflict, say which and ask once more with the diagram.
- **Drawings, sketches, photos**: read every view and dimension back; written numbers govern; undimensioned shapes become "estimated" parameters; photo geometry follows §3.6, overlay confirmed before modelling.
- **A rejected concept is data**: record it with the reason in the brief and the DATASHEET history, and ask for the requester's own idea before the next one — a rejection means the model of the need was wrong, not the geometry. After a warning, if the user insists, ask what design they have in mind and which parts can stay original or metal; hold the line on the unsafe component only. Raise an IPC or safety observation seen in a photo once, briefly.
- End every message with one line on what happens next. Never narrate rules; apply them.

### 1.5 Personal data — strip it before anything else
A design needs the object, its dimensions and its environment, never who the patient or staff member is. Personal data: patient or caretaker names, initials with ward or bed, patient numbers, dates of birth, an age with a diagnosis, treatment tied to a person, faces and body parts, ID wristbands, name boards, screens showing a record, handwriting; staff names beyond the professional role, phone numbers, e-mails, ID numbers, signatures; hidden data — photo EXIF (GPS, camera serial, timestamps), document metadata, file names containing a name. When you find any: stop using that content; never repeat, transcribe, summarise, translate or copy it — chat, file, memory; tell the user the category and where, without repeating it; work only on an anonymised copy (photos cropped to the object and re-saved with Pillow without `exif`; identifying fields removed or neutral; metadata, comments and tracked changes removed); delete the original from your working folders — the upload stays in the conversation, so if it should not be there, tell the user to start a new conversation with the anonymised copy; keep every deliverable free of it; identify the request by request number and department. A custom-sized item for one patient uses measurements as numbers only and goes through §4. Fine to keep: professional names in the approval table, facility and department, device makes, models and equipment serial numbers. MSF data-protection rules (GDPR for EU sections) apply; you minimise what is used.

### 1.6 Token discipline — the context is the scarcest resource
- One questionnaire, one confirmation, one design review, one build pass, one feedback round; never restate answers, summarise between rounds or explain the process twice. Long content goes to files (brief, plan, STATUS, README, DATASHEET, lessons); the chat carries questions, confirmation, design review, the hand-off (≤ 15 lines) and answers.
- Renders: STLs with `openscad-fast` (seconds); look at the render **sheet only, once** per design revision; pictures go to the user only at the design review; never attach STLs or re-send an unchanged image.
- Checks: `check_stl.py --quiet`; sweeps in the foreground in chunks of about a minute (`--resume`, `--merge`) — background jobs die when a turn ends; read only SUMMARY and FAIL lines. A revision that changes no geometry reuses the checks once `compare_meshes.py` shows the STLs identical.
- Files: edit with the edit tool (`str_replace` in claude.ai, `Edit` in Claude Code), view ranges, never paste or `cat` whole files; a `.scad` under 250 lines is the norm.
- At the start of every turn compare the working files with the last delivered package; an unknown change is an unverified draft, never shipped silently. Multi-item sets: one item family per conversation. When the context or a turn's tool calls run out, finish the sub-task, deliver only what is verified, write STATUS.md and ask the user to continue in a new conversation with the package attached.

## 2. The workflow — research → questionnaire → confirm → model → design review → build → feedback

| Stage | You do | User does |
|---|---|---|
| A Research (silent) | §3.1; anonymise uploads (§1.5); pre-fill the questionnaire | — |
| B Questionnaire | §3.2, consecutive picker calls; measurements last with the diagram (§3.7); photo trace (§3.6) | clicks; types the numbers once |
| C Confirmation (1 message) | §3.3: Request Summary + concept card + defaults + failure consequence + scope decision (§4) | clicks yes · mostly · no |
| D Model | brief and plan to files; working file with its Customizer rules; coupon; sweep and checks; structural review (T24); render sheet, assembled view, section | — |
| E Design review | pictures only (§2.3) | clicks "looks right — make the files" · "change something — I'll type it" |
| F Build pass | Customizer file, release export, DATASHEET + README, zip, hand-off (§2.1) | — |
| G After the print | coupon code and first-article feedback (§2.2) → revision; confirmed values into README/DATASHEET/STATUS | prints coupon, then part; clicks |
| H Use and follow-up | test before use; follow-up schedule (§10.4); `docs/LESSONS_LEARNED_<item>.md`; a line in `references/lessons.md` | uses, reports |

Between confirmation and delivery only these interrupt: a missing critical dimension that cannot follow §3.4 (c)–(e), a §4 warning needing the user's recorded decision, the design review click, and advisor sign-off for critical or restricted items (§4.1b, §4.1c, §4.2). A change asked at the design review loops back to D and costs no documentation. Building ahead of a physical result is allowed, releasing is not: fits stay "not confirmed" until the coupon or first article says otherwise. Multi-item sets: one item family per conversation; the first ships `common.scad`, the coupon and the checker.

### 2.1 The build — pointers
- Environment: `scripts/install_openscad.sh` (claude.ai: each conversation; Claude Code: once per session) — native OpenSCAD 2021.01 for PNG views, `openscad-fast` (2025.07, Manifold) for every export (§6).
- Model: include `scad/common.scad` and `scad/helpers.scad`; follow §7 (design header, no `@` lines in the working file, sliders and menus, `all` and `assembly`, kit hardware through `kit_bolt_for()` with a `HARDWARE` echo); reference `scad/example_part.scad`. Coupon: `scad/test_coupon.scad` with the preset for the fit type (§10.4).
- Verify before the review: `sweep.py`, `check_stl.py` (sections `auto`, two overhang passes), structural review with `section_from_stl.py`, `render_views.py` with a copy of `scad/context_scene.scad`, `overlay_sketch.py` when a photo or sketch was the source. §10 is the gate.
- After the review: `flatten_scad.py --name … --description … --category … --credit … --license MIT --verify` once (then `export.sh` regenerates it), `lint_customizer.py` (T25), `export.sh` for the release (STLs, plate, copies, `stl/view_only/`, coupon, renders, log), README and DATASHEET from the templates (readiness only from `references/readiness-levels.md`), one zip, hand-off ≤ 15 lines (§11).

### 2.2 Feedback after the print (one picker call)
Which coupon step fitted (its code) · printed completely (yes · stopped · came off the bed · drooping or stringy) · fit (too tight · good · too loose — by how much) · holds or attaches as intended (yes · no) · sharp edges, cracks, whitened areas or layers opening (none · some — where) · photos welcome. Each answer becomes a parameter change and a confirmed value.

### 2.3 The design review message
Three pictures: the render sheet; the assembled view (several components) or the context view; a section of the load-bearing zone with the layer direction. Four lines: what it is · how it holds or fixes, with the hardware (kit parts by name) · the check result · for load-bearing items, "where could it bend, where could layers open?". Then the picker. No `.scad`, STL or document before the click.

## 3. Intake

### 3.1 Research first (silent)
When a device, a system (UMS, HomeRacker, DIN) or a standard accessory is named: the MSF UMS V1 repository (`MSF3Dprinting/Universal-Mounting-System`), the MSF Printables profile `@3Dprintingforall`, then Printables, Thingiverse, NIH 3D Print Exchange (when reachable — the sandbox may block them; then ask for the file or link). For a spare part, find the OEM part number and split the assembly into components (stays original · metal hardware from the kit or site · printed). Pre-fill the questionnaire's defaults, drop answered questions, report findings inside the confirmation. A discrepancy between a drawing and a reference design's printed files goes to the advisor; the printed files are followed meanwhile.

### 3.2 The questionnaire — every applicable block, consecutive picker calls, nothing in between
Most decisive blocks first; drop what the request answers; merge blocks when a call has room. Each question: 2–4 options, a recommended default, an "I don't know" or "I'll type it" option where sensible.

1. **What and where.** Purpose (hold · attach or mount · connect · cover or protect · organise or store · replace a broken part · training aid · sign or token) · area (patient area · non-clinical hospital area · laboratory · logistics or vehicle · training room · outdoors) · made before? (I have the file or values · no · not sure) · how is it done today, what goes wrong? (type-in, optional — the requester's own idea often wins).
2. **Safety gate** (read `references/scope-gate.md` first; yes/no, all that can apply): liquid, gas or air to a patient — and position relative to a relief valve or filter · inside the body · placed in the mouth · touches food, drink or medicine directly, not through packaging · carries the weight of a device or a person · someone could be hurt if it breaks or falls · mains electricity · certified device part · part of a medical device or positions a sensor, valve, seal or gear. Decide per component.
3. **Function and loads.** What it holds or connects to (make/model — type-in) · heaviest load (nothing · < 0.5 kg · 0.5–2 kg · 2–5 kg · more) · how loaded (resting or hanging · pulled or pushed · flexed repeatedly · clipped on and off · could be leaned or stepped on) · held item rigid or soft (rigid · soft or flexible tube · thin-walled or a bag · not sure — then size and wall, §5.8) · where cables, probes or hoses leave (top · bottom · side · none) · can the mating item move, turn, loosen or vary between units (fixed · can turn or loosen · differs · not sure) · removable or fixed; lock or lip?
4. **Fit and existing systems.** Fit per interface (slides freely · light friction, no rattle *(recommended)* · tight, by hand · press fit) · match a design (UMS V1 · HomeRacker · DIN rail · commercial accessory · none).
5. **Environment and cleaning.** Temperature (room · hot > 50 °C · cold chain) · cleaning (never · wiped with Surfanios, bleach or IPA · heavily disinfected daily · must be autoclaved) · contact (fluids or chemicals · dust · sunlight · skin — how long) · reprocessed items (CSSD, lab): which surfaces may be touched, may anything enter an opening or lumen, does it stay in the clean area.
6. **Mounting and hardware.** Attached to (nothing · wall · board or panel · bed rail or tube · vertical pole · trolley · DIN rail · table edge · another printed part) · UMS-compatible? · hardware (MSF kit bolts M3 / M6 with nuts and washers *(recommended)* · zip ties · wall screws and plugs · other — I'll type it); a masonry wall: the wall material; a bolt as axle: length, smooth shank, thread, nut type.
7. **Production.** Printer (MSF kit MK4S *(recommended)* · other FDM — size and nozzle · unknown) · filament on the shelf now (PETG · PLA · TPU · PC · ASA · other — no "recommended" mark) and colour · quantity (1 · 2–5 · 6–20 · more) · who prints (kit operator · myself · a workshop).
8. **Non-clinical extras** (only if not clinical): text (none · yes — type-in) · colour bands (none · 2 · 3) · NFC pocket (no · yes).
9. **Approval.** Biomed · IPC · lab manager · anaesthesia lead · logistics manager · not sure.
10. **Measurements** — last, one text message: the lettered diagram (§3.7), what to measure and how; a photo of the joint with calipers in the frame.

### 3.3 The confirmation message
One message: the Request Summary (template); the **concept card** — one drawing, the principle in one sentence (what holds it when nobody pushes, what the held item feels, how it is fixed), three numbers (hold or strength against the load; what the mating part experiences; how and where it fails) and **what the current answers exclude** ("a 12 mm tube would then not be held at all"); "Defaults I rely on" (unanswered questions included); "If it fails" (concrete consequence); scope decision (§4); hardware; acceptable materials in order; "What you will get" (pictures first, then the files). Picker: yes · mostly — I'll type corrections · no — the click confirms the principle as well as the sizes.

### 3.4 Missing dimensions — never guess; in this order
(a) ask once more with the diagram (only if the build cannot proceed); (b) a placeholder parameter marked `// UNVERIFIED - measure before printing` — never for a critical interface; (c) the published standard's nominal value plus a bracketing coupon — allowed for a critical interface when the user cannot measure; (d) the value from a validated design's files, tagged "from <file, date> — confirm on first print"; (e) fit-trial release (version 0.x, "FIT TRIAL — not for use", outline check plate, tuning table). Reconstructable undimensioned features become "estimated" parameters checked with the overlay. State every layout assumption in the confirmation; make dependent geometry tolerant or parametric.

### 3.5 If the user clicks "I don't know"
Loads → heaviest plausible listed device, stated · fit → sliding, 0.3 mm per side, coupon shipped · mating part moves or varies → tolerance design (self-centring V, clearance, flared mouth), stated envelope · soft or rigid → soft for tubes, bags and gloves, with numbers (§5.8) · material → the weaker plausible candidate, acceptable list; clinical → light colour; > 50 °C, outdoor, heavy disinfection → advisor · cleaning → Surfanios/bleach/IPA in any hospital · printer → MK4S, part ≤ 200 mm each way · hardware → kit M6 for load, M3 for light parts · approval → clinical: Biomed + IPC; lab: lab advisor; else line manager · critical? → treat as critical · packaging stays closed? → assume not.

### 3.6 Dimensions from a photo
Scale on an object of known size in the same plane (confirm which); strip metadata, straighten, raise contrast, find edges by script, never by eye; label every candidate edge on the overlay and ask which is the boundary; fit simple shapes and cross-check against a value not used for the fit; report "estimated ±1 mm"; depths and undercuts cannot come from a photo — ask for the critical ones with calipers; the user confirms the overlay before the build; after modelling, overlay a section of the exported STL (`overlay_sketch.py` → `img/<item>_overlay.png`).

### 3.7 Measuring diagrams — every request for a measurement has one
Confirm the arrangement first ("tube above, below or beside the handle?" — a picker question), then draw: annotate a cropped, metadata-free copy of the user's photo where it shows the right view, else a schematic marked "schematic" with the view direction. One label = one dimension = one number, in mm, with a short name ("A — handle width, side to side"). An SVG (claude.ai's inline visualiser) or a Pillow image saved as a file you show; keep it simple. A lettered diagram for any interface with more than two related dimensions; a scope diagram (printable / stays original / hardware) with every §4 decision.

## Example of the style
> **Claude (research done, first picker call):** 1. What should the part do? A hold · B attach or mount · C connect · D replace a broken part · E something else (I'll type it)  2. Where will it be used? A patient area · B non-clinical area · C laboratory · D logistics · E training  3. Has it been made before? A I have the file or values · B no · C not sure
>
> **User:** clicks A, A, B
>
> **Claude (next call, no commentary):** 4. What will it hold? A humidifier bottle · B handheld pulse oximeter · C ultrasound transducer · D other — I'll type it  5. Heaviest load? A under 0.5 kg · B 0.5–2 kg · C 2–5 kg · D more  6. How will it be fixed? A kit M6 bolts through a board *(recommended)* · B wall screws and plugs · C zip ties to a rail · D I'll type it
>
> *(… remaining blocks, the lettered drawing, the confirmation with its concept card, the model and checks, three pictures for the design review, one click, the build.)*


<!-- ===== references/scope-gate.md ===== -->

# Scope and safety gate

*Reference file of the `msf-3dp-design` skill. Read it before the safety questions of the questionnaire (§3.2 block 2) and before any warning, restriction or critical-item decision.* Section numbers (§) are shared by every file of the skill: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · readiness-levels.md · Appendix A glossary.md · Appendix C sources.md.

## 4. Scope and safety gate

The MSF guideline's DO NOT PRINT list stays the reference, but the gate **warns, it does not block** (owner decision, September 2026). Two exceptions never move: nothing meant to harm a person, and nothing illegal to manufacture. For everything else your job is to make the risk concrete, advise against, bring in the advisor, and let the user decide on the record.

### 4.1 Warn — the MSF DO NOT PRINT categories
A part that: brings any liquid, gas or air to the patient · goes inside the body — airways, wounds, body cavities (the mouth is handled in §4.1b) · comes into direct contact with food, drink or medicine that is not in its primary packaging · could harm a patient, user or anyone else if it fails · serves as an electric insulator (110/230 V AC or higher) · must be certified, or copies a part of a certified device.

What you do:
1. Say which category applies and what the guideline says.
2. **State the failure consequence in concrete terms** — what drops, how far, what disconnects, who is exposed ("one corner of the concentrator drops about 50 mm"; "a blockage upstream of the relief valve pushes exhaust gas back to the patient"). Do not dramatise a hazard to support a warning, and do not minimise one to avoid it.
3. Recommend not printing, name the alternative (OEM part, a jig, a holder, a non‑contact accessory) and the advisor who must be involved.
4. Decide **per component**: which parts stay original or metal, which are printed (§3.1). Hold the line on the unsafe component, not on the whole request. If the user insists, ask what design they have in mind — the concept often changes the load path.
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

*Reference file of the `msf-3dp-design` skill. Read it before modelling and whenever a size, edge, fit, hole, hardware, strength or material question comes up.* Section numbers (§) are shared by every file of the skill: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · readiness-levels.md · Appendix A glossary.md · Appendix C sources.md.

## 5. Design rules for printability (FDM, 0.4 mm nozzle, 0.2 mm layers)

Targets: MK4S first, any FDM printer second. A design optimised for printing is less sensitive to slicer settings and user error — put the intelligence in the geometry, not in the slicer profile (field). Prusa's MK4S and CORE One can print overhangs up to about 75° thanks to 360° cooling; we still design to 45° so the same file prints on any machine.

### 5.1 Size, orientation, bed contact

| Rule | Value | Source |
|---|---|---|
| Maximum single part | 200 × 200 × 200 mm; larger → split (§5.7) | (MSF) |
| Orientation | Model in the print orientation: Z = build direction, the part sits on Z = 0. Every exported STL is in this position — the user downloads and slices, nothing to rotate. If a part is modelled differently for preview, the export module applies the rotation | — |
| Bed contact | One large flat face on the plate; all parts of a set, or all connector ends, in one plane. A tall part on a thin ring or a slender footprint gets built‑in brim ears (a parameter, removable tabs) rather than a note that hopes the user sets a brim | (MSF) (project) |
| Bottom edges | Chamfer 0.4 mm against elephant's foot (Hydra: ~0.3); no downward‑facing fillets | (default) |
| Vertical edges | Filleted, including the edges of windows, cut‑outs and holes through walls, and the free edges of thin plates (a plate ≤ 3 mm gets a full round). R ≥ 4 mm at closed corners on the build plate where the footprint allows; at the free ends of walls (open‑front trays) R = wall_t/2 — a larger radius meets the inner face tangentially and leaves a knife edge. A corner radius near a seat, slot or hole is the largest value up to `corner_r` that keeps `struct_wall` to it — compute it, never fix it (a fixed R4 once left 0.25 mm at a seat end); the end rounding of a bolted tab keeps `bolt_wall` round the hole | (MSF) Hydra (project) |
| Horizontal and sloped edges | 45° chamfer 0.6–1.0 mm on walls ≥ 3 mm, (t − 1)/2 on thinner walls so ≥ 1 mm stays flat — `top_chamfer(t)` in common.scad; where a plate is thinner behind a pocket, chamfer for the thinner wall; two chamfers never eat the same wall (a well's lead‑in and the outline's top chamfer: boss = well radius + `bolt_wall` + 2 × chamfer); downward‑facing edges never filleted. A fillet that blends a ≤ 45° face into a vertical face is fine (it never exceeds 45°) | (MSF) (project) |
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
| Kit hardware first | The MSF 3D printing kit hardware (§5.4.1) is the default for every bolted joint; anything else is listed as in §5.4.2. Sizes are parameters or menus, never assumed | (owner, Sept 2026) |
| Nut trap | Pocket = nut across‑flats + 0.3 mm total, depth = nut height + 0.5 mm; printed with the opening horizontal or with a flat top | (default) |
| Rotating part on a bolt | Runs on the smooth shank, never on the thread; the clamped stack ends past the start of the thread so the nut engages; nylon lock nut set with ≈ 0.5 mm play; bolt end cut to 2–3 threads and filed smooth | (project) |
| Retention in a groove on a steel pin | Groove narrower than 1.6 mm → steel wire (a straightened paperclip) through a horizontal teardrop channel tangent to the groove bottom; no printed clip | (project) |
| Thrust faces | 1 mm rings go on the part printed flat (top face), not on a vertical face where they would be unsupported edges | (project) |
| Conical medical connectors | ISO 5356‑1 family: 1:40 taper on the diameter — model the taper, a straight spigot will not seal. A tapered bore sealing on a straight PVC pipe: 0.3 mm per side at the mouth, 0.0 at the stop, set by a coupon with straight rings (one clearance per ring). State every taper and clearance direction in the hand‑off and README | (project) |

#### 5.4.1 MSF 3D printing kit hardware — use it first (owner, Sept 2026)
Every kit carries, in stainless steel:

| Item | Standard | Sizes in the kit | Quantity |
|---|---|---|---|
| Socket‑head (Allen) bolt | DIN 912 | M3 × 20, 30, 40, 50 · M6 × 20, 30, 40, 50, 60 | 20 of each |
| Washer | DIN 125A | M3 (3.2) · M6 (6.4) | 40 of each |
| Self‑locking nut | DIN 985 | M3 · M6 | 40 of each |
| Nut | DIN 934 | M3 (40) · M6 (50) | |

`common.scad` holds their dimensions (`kit_clear_d`, `kit_head_d`, `kit_cbore_d`, `kit_nut_af`, `kit_nyloc_h`, `kit_washer_d`, …) and `kit_bolt_for(m, grip)`, which returns the shortest kit bolt for a clamped stack with 2 threads past the nut, or 0 when none is long enough; `helpers.scad` has `kit_hole`, `kit_hole_h`, `kit_counterbore` and `kit_nut_well`. Rules:
- **M6 for anything that carries a load, M3 for light parts, covers and alignment.** Let the model choose the length with `kit_bolt_for()` and echo it (`HARDWARE:` line); the README lists the exact parts and quantities.
- A washer under every bolt head and nut that bears on plastic; a self‑locking nut on anything that moves, vibrates or is cleaned often; plain nuts in captive wells (DIN 934 is lower, so the well is shallower).
- Bolt heads in counterbores, nuts in captive wells, both opening upward in print (no support) — one hex key, no spanner.
- Clearance holes: ISO 273 medium (M3 3.4 mm, M6 6.6 mm) + `hole_clr` when vertical, teardrop when horizontal.

#### 5.4.2 Hardware that is not in the kit — exact, with alternatives
When a joint cannot use kit hardware (a masonry wall needs screws and plugs; a longer bolt; an axle), assume nothing can be bought easily where the item is used. The README's hardware table gives, for each item:
1. **The exact part**: standard, size, length, material, quantity (e.g. "2 × wood screw 4.5 × 35 mm, zinc‑plated, with 2 wall plugs 6 mm for the wall material").
2. **At least two local alternatives** that fit the same holes (another screw type, a kit bolt with a nut through a board, a zip tie, wire).
3. **Where it can be taken from** — medical and non‑medical equipment both listed; the staff on site decide what to use. The skill proposes sources, it does not choose them.

| Need | Buy | Local alternatives | Where it can be taken from |
|---|---|---|---|
| Fixing to a masonry wall | Wood screws Ø4–5 × 35–50 + plugs to suit the wall | Kit M6 bolts through a board screwed to the wall; strong double‑sided tape (light items) | Furniture, shelving and cabinet fittings; packing crates; screws of written‑off equipment carts |
| Bolt longer than 60 mm, or M4 / M5 | DIN 912 or ISO 4017, stainless | Threaded rod M6 with two kit nuts; kit M6 through a spacer printed to length | Bed frames, trolleys, IV poles, bicycles (M5 bottle‑cage and rack bolts), office chairs, medical equipment carts and frames |
| Axle or pin Ø2–8 mm | Steel pin or bolt shank of that diameter | Kit bolt shank (smooth part) as axle; nail (Ø2–4) cut to length | Bicycle spokes (Ø2), door hinge pins, stands and frames of medical or office equipment, printers and copiers |
| Zip tie | 4.8 × 200 mm nylon | Galvanised binding wire; cord; kit M3 bolt through a strap | Cable bundles, equipment packaging, construction sites |
| Heat‑set insert | Avoid — use a kit nut in a captive well | Self‑tapping screw into a 96 % hole | — |
| Spring | — | Printed flexure (TPU or a thin PETG arm within the strain limit, §5.2) | Ballpoint pens, spray pumps, clothes pegs, printers, medical device mechanisms |
| Magnet | Neodymium disc of the stated size | Kit M3 bolt and nut as a latch | Loudspeakers, hard disks, fridge magnets, cabinet catches, medical equipment covers and holders |
| Rubber pad or grip | Self‑adhesive rubber feet | TPU print; cut inner tube | Bicycle inner tubes, packaging foam, equipment feet |
| Wire retention for a groove | Spring steel wire of the groove width | Straightened paperclip (§5.4) | Paperclips, binding wire |

### 5.5 Strength — foolproof against slicer settings, loads along the layers
- **Loads run along the layers, never across them (owner, Sept 2026).** Every load — the weight the part carries, bolt preload, clamping, levering, a push or a knock — runs in the plane of the layers or presses the layers together; it never pulls layers apart or peels them. Parts break between layers "like wood splitting along the grain", at about half the in‑plane strength and often less. For every load, draw its path through the part in print orientation and check the layer direction at each loaded section; choose the print orientation for it; when one orientation cannot serve every load, split the part and join the pieces with kit bolts. If no orientation and no split avoids a load across the layers, the hand estimate states it with a margin of at least 10 on the layer bond and the advisor is told. This is checked in the structural review (§10.1 T24) and shown to the requester as a section at the design review.
- **Bolts and clamps.** A bolt's preload must press layers together (bolt axis across the layers, head and nut bearing on material that is compressed through its thickness) or act in the layer plane. Never put bolt or clamp load into a thin wing or flange that joins a taller block at an inside corner — tightening bends the wing about that root and peels the layers (pipe clamp: cap wings delaminated). Make the part one solid convex body, seat heads in counterbores and nuts in captive wells, and load the body, not a lobe.
- **Fastener pattern.** A clamped part gets at least two fasteners on each side of each clamped member; never three collinear with the clamp axis, never two on a diagonal (the part rocks about that line); the resultant passes through the clamped centre.
- **Thinnest loaded section.** The minimum‑wall rule is not a strength check. Name the section that carries the load and estimate its stress by hand: a 90° V‑seat clamp needs ≥ 10 mm of material over the apex by default (4 mm gave ≈ 50 MPa from the wedge spreading the halves, 10 mm ≈ 9 MPa).
- **Design for the printer's default profile:** 2 perimeters, 15–20 % infill, 0.2 mm layers, any FDM printer, an inexperienced operator. The part must carry its loads with that profile. The README still recommends 4 perimeters and 40–60 % infill, as a bonus — never as a requirement (owner decision, September 2026).
- Put strength in the geometry: load‑bearing members solid by construction — a hook or latch modelled with webs or ribs so its section is filled by perimeters even at two (a wall ≤ 1.8 mm is 100 % perimeter; a 1.8 mm rib is stronger than 15 % infill), T‑ and I‑sections instead of hollow slabs, gussets at hook roots, full‑radius fillets at every stress concentration, generous section on flexing features. Avoid large enclosed volumes in the load path.
- Parts break between layers ("like wood splitting along the grain"): orient so main loads, and the bending of latches and hooks, run along the layers. A slender handled part (a mop handle) prints lying flat; upright it snaps.
- Bed adhesion and support are built in, not delegated: brim ears as a parameter for tall or narrow parts, in‑built supports where unavoidable (§5.1).
- Check by hand estimate for anything load‑bearing (bending stress at the root, strain of flexing features — §5.2) and record it in the DATASHEET with its inputs; the physical load test (§10.4) confirms. Template for a bolted clamp: preload per bolt F ≈ T / (0.2 · d) (T tightening torque — hand‑tight with a hex key ≈ 1 N·m on M6 into plastic, so F ≈ 800 N); holding force ≈ μ · n · F (μ ≈ 0.3 printed on steel); bearing under a washer σ = F / (π/4 · (d_w² − d_h²)) ≤ 10 MPa; bending of a loaded member σ = M / (b · t² / 6), across the layers only with the margin above. State the stated working limit (≤ ⅓ of the estimated failure load) in numbers.
- Reusable patterns (project): a 90° V‑seat centres round and oval tubes and prints on any face without support; through‑bolt positions computed for any clamp angle; captive nuts in the top part so one hex key does everything; square seat ends (each seat in a block whose ends are square to it) with a 45° transition sized from the exact rounded outline (rounded corners shrink an outline diagonally by up to r(√2 − 1)); gabled (45° roof) internal channels for zip ties and wires instead of flat‑topped ones; full‑height side tabs to fix a holder to a wall or board (the load stays in the layer plane).
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

- **The design is not tied to one material.** Ask what is actually on the shelf (§3.2 block 7), design so the part works in the weaker plausible candidate, and list the acceptable materials in the README in order of preference with the difference each makes ("PETG preferred; PLA acceptable indoors below 40 °C; TPU not needed"). Mark nothing "(recommended)" before the shelf is known; confirm the answer in the confirmation message — a withdrawn "TPU available" changed a wheel design after the brief was written.
- Field practice as a starting point: hospital and lab items are usually PETG in white, natural or a light colour — the light colour is an IPC rule and stays whatever the material; training and office items PLA; flexible or impact TPU; above 50 °C PC / PC Blend (advisor); heavily disinfected surfaces (Ebola treatment centres) PP‑GF (field) — some filaments such as PP‑GF survive autoclaving, advisor only; outdoor and UV PETG, or ASA via the advisor (not in the MSF table).
- MSF kit filaments: PLA and PETG (basic); ASA, PC Blend, PC‑CF, PETG V0, TPU (advanced); PP‑GF, PP‑CF and TPU 95A being added — the kit list says what could be there, the shelf says what is.
- One material family per part: PLA and PETG do not bond reliably; colour changes stay within PLA or within PETG (project).
- Fine details under 1 cm: not in PETG; heat‑exposed parts: not in PLA (MSF).
- Wording: filament "absorbs moisture from the air" — never "wet" (field). No chemical‑resistance tables in any deliverable (field).

### 5.7 Large items and modularity (MSF)
- Split anything larger than 200 mm into sections joined by glue, bolts or snap‑fit connectors, with alignment features (pins and sockets or keyed joints) at every split.
- Complex designs are modular so single parts can be reprinted. Design as simple as possible, without unnecessary features; keep material use and print time low.

### 5.8 Holding soft or hollow parts (project: tube drying holder)
Before designing around a soft or thin‑walled mating part (silicone or PVC tube, bag, glove, cable), put numbers on it — three full builds of a tube holder failed on physics a ten‑minute estimate would have shown.
- **Weigh it first.** The load is usually tiny: 1 m of silicone tube 8 × 12 mm ≈ 75 g, 5 × 8 mm ≈ 37 g, 2 × 4 mm ≈ 11 g.
- **Ring bending.** A thin tube squeezed from outside deflects δ ≈ 0.15 · F · R³ / (E · I) per unit length (E ≈ 3 MPa for silicone, I = t³ / 12): about 1 mm per newton on a 12 mm tube over a 12 mm contact. Friction on the outside therefore needs a squeeze the user will see, and a rigid wedge under the tube's own weight squeezes it 10–20 %. Grip from inside (hoop tension, E · t) is about 100 × stiffer — that is why connectors hold.
- **The four honest options**, strongest first: an end feature (collar, flange, connector) resting on a seat; an inside grip where the item may be touched inside; long contact with a spring (a flexure along the tube); a bounded pocket relying on friction (weakest — state the limit).
- **Ask what may touch it** before choosing (§3.2): for reprocessed items (CSSD, lab) whether anything may enter a lumen, which surfaces may be touched, whether the item stays in the clean area.
- **State the hold limits in numbers** in the README and DATASHEET (which size holds how many times its weight, which one does not), never "should hold".



<!-- ===== references/openscad-environment.md ===== -->

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


<!-- ===== references/ipc-and-hospital.md ===== -->

# IPC and hospital-environment rules

*Reference file of the `msf-3dp-design` skill. Read it for every item used in a hospital or laboratory, or that is ever cleaned.* Section numbers (§) are shared by every file of the skill: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · readiness-levels.md · Appendix A glossary.md · Appendix C sources.md.

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
- Hardware: MSF kit hardware first (stainless M3 / M6); anything else exact, with local alternatives and sources (§5.4).
- Ageing: PETG latches and hooks become brittle over time. Generous section and radius; support the in‑service check (no cracks, surface clean, latches still flexible); replacement by reprinting is the normal corrective action.
- Traceability lives in logbooks, not on the part. NFC pockets (§9.2) only on larger non‑mechanical, non‑clinical items, and only when requested.
- Generated documents (README, DATASHEET, headers, renders) carry no licence statements, certification marks, badges or UIDs — they are internal MSF documents, and such marks would mislead (owner, Sept 2026). One exception: the `@license` line of the Customizer file header, which the MSF customizer standard requires (§7.7). The attribution line of the README (made by Claude with the msf-3dp-design skill, with its link) is accountability, not a mark.
- Storage of spares: sealed zip‑lock bags, room temperature, away from sunlight and humidity.



<!-- ===== references/compatibility-and-markings.md ===== -->

# Compatibility systems, text, colour bands, stands

*Reference file of the `msf-3dp-design` skill. Read it for UMS or HomeRacker work, and for any non-clinical item with text, colour bands or a stand.* Section numbers (§) are shared by every file of the skill: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · readiness-levels.md · Appendix A glossary.md · Appendix C sources.md.

## 9. Compatibility systems, text, colour bands, stands

### 9.1 UMS‑compatible hooks, holders and clamps
- Every holder = **back part** (bed rail, pole, trolley, wall) + **front part** (holds one specific device), sharing the common sliding interface. Treat the interface geometry and its tolerances as a fixed standard: import or copy it from the reference design, never redraw it approximately — any change breaks interchangeability.
- Fit target: the front part slides into the back part easily yet holds firmly — no rattle, no forcing. The device seats stably and stays easily removable. Verified before installation.
- Hook back parts: tube diameter, hook opening, wall thickness and the optional 6 mm zip‑tie stabiliser are parameters; brim ears built into the model where the footprint is narrow (§5.1), never left to the print notes.
- "Universal" attachment options as selectable modules: back holes, side wings with 3–10 mm holes (wings may use up to 60° overhang, by brief), horizontal and vertical pole clamps, zip‑tie channels, hooks, DIN rail. Holder body: rectangular with filleted vertical edges; each wall solid or hex‑perforated; front wall removable but with a retaining edge so items stay in (project).
- HomeRacker‑compatible parts: 15 mm unit pitch, 4 mm square lock‑pin holes, BOSL2 (§6.5) (project).
- A holder with a back part and a front part is a multi‑part item: its `part` menu offers each part, `all` (both on one print plate) and `assembly` (the front part slid into the back part, installed orientation) (§7.3).
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

*Reference file of the `msf-3dp-design` skill. Read it before any STL or package is delivered, and when planning the physical tests.* Section numbers (§) are shared by every file of the skill: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · readiness-levels.md · Appendix A glossary.md · Appendix C sources.md.

## 10. Verification — required tests before shipping

Nothing ships until every test below has a recorded result. Report them in the hand‑off as a table: test · result · evidence (file or number) · pass / fail / n.a. Physical tests (§10.4) are done by the user; you write the protocol and record what came back.

### 10.1 Automated tests (you run them in the sandbox)

| # | Test | How | Pass |
|---|---|---|---|
| T1 | Render at defaults, then every variant | `openscad-fast -o … --export-format binstl` (export.sh) at the default parameter set first, then each `part` value and preset | Exit 0; no WARNING or ERROR in the log; the defaults pass every guard; the `HARDWARE` echo names every fastener |
| T2 | Parameter sweep | `sweep.py --check --sections auto`: every slider end, every other menu value and checkbox state with the others at default, plus the extreme angles and offsets of any movable sub‑shape; unknown names are refused; run in the foreground in chunks with one report each and `--merge` them into `tools/sweep_report_<date>.txt` | Every case renders or a guard stops it with its message; no FAIL; no specks removed at the defaults |
| T3 | Guards | Out‑of‑range values and invalid combinations, names checked as in T2; the sweep's "slider ends stopped by a guard" line | `assert()` stops with its plain‑language message; no over‑strict guard: a slider end stopped at defaults is narrowed unless another parameter makes it valid |
| T4 | Closed solid (watertight) | `check_stl.py` after `stl_clean.py`: watertight, consistent winding (no flipped faces), body count (`CHECK expect_bodies=N` for plates and assembled views), positive volume | Watertight; one body per intended part; positive volume — this is the test that catches boolean artefacts |
| T5 | Bounding box and size budget | `check_stl.py` against the brief | Within 0.1 mm; ≤ 200 mm per axis, or split; ≤ 60 000 triangles and ≤ 3 MB per STL (a field package travels by e‑mail and slow links; big meshes also make the checks slow) |
| T6 | Print position | min Z = 0 ± 0.01 mm; the STL is in its print orientation with nothing to rotate; bed‑contact area as % of the convex footprint; height against the narrowest bed contact | Sits flat, ready to slice; slender or narrow footprints get brim ears |
| T7 | Overhang scan | `check_stl.py`: for every downward‑facing facet above the bed, angle from vertical = asin(−n_z); tolerance 0.05° (float32 STL rounding); ignore facets at Z ≈ 0 and below 0.001 mm² (CGAL slivers); run once at `--min-area 0.5` and once at `--min-area 0.02` for small ledges and sheets | Worst sloped angle ≤ 45° (≤ 60° only where the brief allows); report the worst angle and where |
| T8 | Bridges and unsupported spans | Horizontal downward faces above the bed listed separately with their XY extent and longest span (the mesh does not say where a bridge rests, so the longest extent counts); teardrop tips excluded | None, or each < 10 mm, documented and accepted with `--allow-bridges` |
| T9 | Minimum features | Customizer values against §5.2; minimum wall along Z computed in the model (`echo`), reported as modelled and as printed once coupon values are applied; spot check of the preview | All at or above the minimums, or a recorded deviation |
| T10 | Hole compensation | Horizontal holes teardrop or flat‑top; vertical holes carry `hole_clr` | Yes |
| T11 | Ghost parts and scenes excluded | Export with defaults and each `part` value; export the context scene file | STL contains only the part; the context scene refuses to render outside preview (its `assert($preview)` guard) |
| T12 | Colour bands (banded parts) | Band heights on 0.2 mm steps; base ≥ 2.0; each colour ≥ 0.6; nothing else crosses a boundary | Yes |
| T13 | Text fits (non‑clinical) | Measured string width + margins ≤ plate | Yes |
| T14 | Render set | `render_views.py` via export.sh (preview mode, 2× downsampled) per variant: `<item>_<variant>_front/_top/_side/_iso.png`, `_context.png` (installed, stand‑ins), `_exploded.png`, `_section.png` (camera follows `--section-axis`; these three once per set of overrides other than `part` — holder, insert and plate share them) and the captioned `_sheet.png`; `<item>_coupon.png` (top view); section drawings from the STL with `section_from_stl.py` for the load‑bearing zone; by hand where they apply: extremes (`-D` min/max, `--name <item>_min`), misalignment views (T20), the assembled view (`-D 'part="assembly"'`) | Produced; you look at the sheet once per design revision; the sheet, the assembled view and a section are shown at the design review (§2); the sheet is the README picture; no stand‑in in any STL |
| T15 | Slicer dry run (when PrusaSlicer runs) | `prusa-slicer --info` (`manifold = yes`); `--export-gcode` with the default profile values (0.2 mm layers, 2 perimeters, 15 % infill) for time and filament | Closed mesh; no supports needed; time under 48 h — the estimate goes in the README |
| T16 | Documentation and data | Header complete (§7.4); README complete (§11.2) including the attribution line, test‑before‑use, acceptable materials and the hardware table (kit parts, or exact local parts with alternatives and sources, §5.4.2); deviations, flags, tapers, clearance directions and unverified values listed; hold limits in numbers; README numbers match the DATASHEET and the export log; no `PLACEHOLDER` left (`grep -rn PLACEHOLDER`); no personal data in any file, file name, render or comment (§1.5) | Yes |
| T17 | Pre‑export checklist (§10.3) | Walk it | Every box ticked or explained |
| T18 | Interface identity (copied interfaces) | Cross‑sections of the exported STL compared with the reference file at ≥ 5 heights | Widths, depths and detents agree within 0.05 mm |
| T19 | Section check | `check_stl.py --sections auto` (every 2.5 mm from 0.3 mm and 0.3 mm below the top: every height band that holds a feature, and the top face where two chamfers meet) or chosen heights (`5,50%,top-0.3`); heights in straight zones, not through the oblique cut of an acute edge (a 60° V edge cut at an angle reads as a 0.95 mm "wall"); one section 1 mm in front of each face that should carry a feature (a feature built with the wrong rotation hides inside its host); quote the heights from the check JSON, not from memory | Every section computes (a section that cannot be computed is a FAIL); smallest wall ≥ 1.6 mm; pieces as intended; features exist |
| T20 | Clash test (moving or misaligned mating parts) | Intersect the part with the ghost mating part at every tolerance case (lean, shift, angle, tilt, combinations) | Empty = clear, 0 mm³ = touching, > 0 = clash; envelope table in the README, no clash inside the stated envelope |
| T21 | Overlay check (source is a photo or drawing) | `overlay_sketch.py`: section of the exported STL at the seating height drawn over the anonymised, scaled, straightened image (EXIF orientation applied, output without metadata) | Topology matches; every deviation explained by a written dimension or a recorded interpretation; image delivered |
| T22 | Customizer file: header and identity | `flatten_scad.py part.scad --out part_customizer.scad --verify` (export.sh does it) | Exactly the five header lines (§7.7); same volume (±0.2 %), size (±0.01 mm) and triangle count as the working file; no non‑literal parameter |
| T23 | Copies | For every `xN` variant the numbered files exist and are identical | N files, one per item |
| T24 | Structural review (by hand; the automated checks are geometric, not structural) | For every load (weight, bolt preload, clamping, lever, knock): its path through the part, the layer direction at each loaded section, the thinnest *loaded* section and its stress by hand with the inputs (§5.5 template); the fastener pattern (≥ 2 per side of each clamped member, never collinear or diagonal); no bolt load into a thin wing at an inside corner; a section drawing of the load‑bearing zone (`section_from_stl.py`) | Every load runs along the layers or presses them together (or the stated exception with a margin ≥ 10); stresses and the stated working limit in the DATASHEET; the section shown at the design review with the question "where does it bend, where could layers peel?" |
| T25 | Customizer check | `lint_customizer.py <item>.scad` and `lint_customizer.py <item>_customizer.scad` (export.sh does both) | Header exact in the Customizer file and absent from the working file; help text above every parameter; every number a slider or numeric menu; every fixed choice a menu; no vector parameter; a multi‑part `part` menu offers `all` and `assembly`; the file opens in native OpenSCAD 2021.01 without an unknown function or module (language level) |
| T26 | Parts together | Export `part="all"` and `part="assembly"` | The plate holds every component in print position, fits the MK4S bed and passes T4–T8 with its body count; the assembled view shows every component in its installed position, passes T4 (`--view-only`) and is kept in `stl/view_only/` |

**Carrying checks over.** When a revision changes only documentation, Customizer widgets or comments, prove that every exported STL is identical to the verified version with `compare_meshes.py old_stl/ new_stl/`; the earlier sweep and checks then carry over (say so in the verification table). Any "DIFF" means the checks run again.

### 10.2 The check tooling — shipped with this skill in `scripts/`, copied into the project's `tools/`
All scripts are universal — they read the mesh or the Customizer, never the design — so the same files serve every product.

| Script | Does | Typical call |
|---|---|---|
| `install_openscad.sh` | Sandbox setup: native OpenSCAD 2021.01 + xvfb + fonts-liberation (PNG views), `openscad-fast` (2025.07 + Manifold, every export), Python tooling; ends with a readiness test (an export with text) | `bash tools/install_openscad.sh` |
| `openscad-fast` | OpenSCAD 2025.07 with the Manifold engine (npm `openscad-wasm`), same arguments and same messages as `openscad` for geometry export and `--export-format param`; fonts mounted; several times faster than 2021.01 | `tools/openscad-fast -o stl/part.stl --export-format binstl -D 'part="holder"' part.scad` |
| `export.sh` | Every variant from `variants.txt`: STL in print position, `xN` copies as numbered files, assembled views to `stl/view_only/`, speck cleaning, check_stl (sections auto), render set, coupon with its check and image, the Customizer file regenerated and checked, `stl/EXPORT_LOG.txt`, a table of files; exit 1 on any failure or missing file | `COUPON=test_coupon.scad COUPON_D='preset="rusty"' bash tools/export.sh part.scad 1.0 variants.txt part_context.scad` |
| `check_stl.py` | T4 – T8, T19 on any STL: watertight, winding, bodies, size and size budget, print position, bed contact and slender parts, overhangs (0.05° tolerance, slivers ignored), bridges with their span, sections and wall thickness (exact, located in part coordinates); `--view-only` for assembled views; exit 1 on failure; `--json` | `python3 tools/check_stl.py stl/part.stl --sections auto` then a second pass `--min-area 0.02` |
| `sweep.py` | T1 – T3: reads the Customizer (sliders, menus, checkboxes; [Hidden] excluded), renders the defaults, every slider end and every other menu value; PASS / GUARD / FAIL; refuses unknown names; `--check` cleans specks and runs check_stl; report written line by line; `--resume`, `--merge` | `python3 tools/sweep.py part.scad --check --sections auto --params a,b,c --report tools/sw1.txt` … then `--merge tools/sw1.txt tools/sw2.txt --report tools/sweep_report_<date>.txt` |
| `render_views.py` | T14: front / top / side (orthographic), isometric, `--context` installed (`_context.png`) / exploded / section (camera follows `--section-axis`); headless via xvfb‑run; 2× downsampled; no metadata; captioned sheet; `--views`, `--no-sheet`; fails on a missing module or a timeout | `python3 tools/render_views.py part.scad --out img --name part_holder --context part_context.scad` |
| `section_from_stl.py` | A section drawing from the exported STL, cut faces filled, mm grid, thinnest wall marked; Z cuts are plan views, X / Y cuts side views with the build direction up | `python3 tools/section_from_stl.py stl/part_holder_v1.0.stl --x 0 --out img/part_section_x0.png` |
| `overlay_sketch.py` | T21: section (`--z`) or silhouette (`--view`) of the exported STL drawn over the anonymised photo or sketch; `--calib` gives px/mm from two points | `python3 tools/overlay_sketch.py photo.png --stl stl/part.stl --z 3 --scale 18.4 --origin 700,500 --rot 12 --out img/part_overlay.png` |
| `flatten_scad.py` | T22: the one‑file Customizer version with the exact five‑line header (§7.7); refuses without it; `--verify` compares the geometry | `python3 tools/flatten_scad.py part.scad --out part_customizer.scad --verify` (first time: `--name … --description … --category … --credit … --license MIT`) |
| `lint_customizer.py` | T25: header, help text, sliders, menus, vectors, `part` menu — from OpenSCAD's own parameter export; `--fix` moves help text above | `python3 tools/lint_customizer.py part_customizer.scad` |
| `stl_clean.py` | Removes detached zero‑area specks (< 0.01 mm²) from an STL and says so; export.sh and sweep.py run it | `python3 tools/stl_clean.py stl/*.stl` |
| `compare_meshes.py` | Proves two exports identical (sorted triangles, 1e‑4 mm), so earlier checks carry over | `python3 tools/compare_meshes.py old/stl stl` |
| `test_coupon.scad` (scad/) | Universal tolerance coupon: round / square / rect / slot / D‑shaft openings, a preset menu (tight, sliding, clearance, rusty steel, custom), numbered row + lettered row, debossed or notch labels | `tools/openscad-fast -o stl/part_coupon_v1.0.stl -D 'preset="tight"' -D 'feature="dshaft"' -D nominal=6 -D flat=4 test_coupon.scad` |

### 10.3 Pre‑export checklist
- [ ] Not in §4.1; if restricted, every §4.1b condition met and recorded; criticality and advisor flags set
- [ ] The design review was approved by the user (render sheet, assembled view, load section) before any documentation was written
- [ ] Every load runs along the layers or presses them together; structural review (T24) written with its hand estimates
- [ ] ≤ 200 × 200 × 200 mm, or split with alignment features
- [ ] Modelled in print orientation and exported in print position; large flat face on the plate or brim ears; base edges chamfered or rounded
- [ ] No overhang > 45° from vertical without planned built‑in support; no bridges (or < 10 mm, documented)
- [ ] Walls ≥ 1.6 mm (structural ≥ 1.8 mm); vertical holes ≥ Ø1.5 mm + 0.2; pins ≥ Ø1.8 mm
- [ ] Horizontal holes compensated; clearances match fit type and mating material; each is a parameter
- [ ] Threads only if Ø > 10 mm and pitch > 1.5 mm; otherwise inserts, nut traps or tapping
- [ ] Kit hardware first (M3 / M6, `kit_bolt_for`); anything else listed exactly, with two alternatives and where it can be taken from; sizes are parameters or menus
- [ ] Loads run along the layers; strength holds at 2 perimeters / 15 % infill (§5.5); enough material around bolt holes; flexing features ≥ four perimeters and within the strain limit
- [ ] Acceptable materials listed from what is on the shelf; the geometry does not depend on one material; clinical → light colour
- [ ] Clinical: no text or recesses; cleanable surfaces; no sharp edges; removable parts for cleaning; drainage hole in every closed floor (or the brief says why not)
- [ ] Every cutter clipped to its target; no coincident faces — T4 clean at every sweep case
- [ ] Render set complete (front, top, side, isometric, context, section, sheet); coupon exported alongside the part
- [ ] Failure consequence and test‑before‑use protocol in the README
- [ ] Non‑clinical text: sans‑serif, size per §9.2, 0.6–1 mm deep
- [ ] As simple as possible; modular if complex; print time estimated
- [ ] Customizer: the five‑line header only in the Customizer file; sliders for numbers, menus for fixed choices, help text above; `part` menu with `all` and `assembly` for several components (T22, T25, T26)
- [ ] Header and README complete, including the attribution line, the hardware table, deviations, unverified values and hold limits in numbers; no PLACEHOLDER left
- [ ] Verification table filled in
- [ ] No personal data in any file, file name, render, comment or log (§1.5)

### 10.4 Physical tests (the user prints; you write the protocol)

**Coupons travel with the product.** The coupon is made in the same build pass as the part and shipped in the same package; it prints in 10–40 minutes; the user replies with its code ("B4"); the value is entered as a parameter; then the part is printed. Never make the product wait for the coupon, and never mark a fit confirmed before the coupon or the first article says so.

| Test | When | What the user prints and reports |
|---|---|---|
| Tolerance coupon | Any new fit, new material or new printer | A flat plate printed in the part's orientation with the mating feature at stepped clearances, bottom chamfer and top lead‑in on every hole, steps marked by digits and letters (debossed size ≥ 6.5, 0.6 mm — a non‑clinical test piece) or by notches. Range by fit type: **sliding** −0.1 to +0.8 mm in 0.1 steps; **tight or push‑on onto a machined part** 0.00 to +0.30 mm per side in 0.05 steps; **clearance features** (counterbore over a bushing, nut or head) +0 / +0.2 / +0.4 on the diameter; **push fit on rusty or variable metal** three holes at 0.075 / 0.15 / 0.25 mm per side marked by 1–3 notches (`preset="rusty"`), plus "wire‑brush the tube end" in the assembly steps; **tapered bores** straight rings, one clearance per ring. The reply is the step code |
| Interface coupon | Any copied interface (UMS socket, HomeRacker) | The interface only (`part = "socket_test"`, ≈ 40 min): checks the site's printer, not the geometry |
| Outline check plate | Any outline or slot positions not measured with calipers (§3.6, §3.4 e) | The part outline at full thickness with windows at the openings and the tabs that enter them, ≈ 10 min. Report: drops in without force, gaps under 0.5 mm, windows over the openings |
| Overhang / colour coupon | Overhangs above 45° allowed by the brief; colour bands; a light colour over a dark base | Report drooping and tinting |
| First article | Every new design | Print at the README settings; measure the critical dimensions the README lists; fit it to the real device; photos; feedback questions (§2.2) |
| **Test before use** | Every item — the README carries a protocol proportional to the risk | Function: does what it must, 10 cycles (attach, load, remove; slide, latch). Fit: no rattle, no forcing, the device stays put. Cleaning: wipe with the site agent, look for residue in corners. Edges: nothing sharp on skin or glove. The approver signs the result |
| Load test | Every load‑bearing part (§4.1c) and any holder for more than 2 kg | Static: part on a bathroom scale, load through a steel rod of the mating diameter to 2 × the design load, hold 1 min, 3 times. Rolling or functional: 20 cycles over a 10–15 mm doorstep or the equivalent use. Pass: no cracks, no white stress marks, no deformation, no wobble, hardware in place |
| Drop test | Anything that can fall onto a floor or a person | The loaded part dropped from its mounting height onto concrete, 3 times; no fragments, no sharp break, still holds |
| Test to failure (not always) | Critical items; batches of 10 or more; anywhere the limit matters (owner decision, September 2026) | One sample loaded to failure the way it is loaded in use: increase in steps, note the load at the first crack and at break, the failure mode, and whether it failed safe. Set the stated working limit at ≤ ⅓ of the failure load (default) and record load, mode and a photo in the README. Skip it for low‑load, non‑critical items — say why |
| QC per README | Every production part | Visual · dimensional · fit/tolerance · safety validation by the approver |
| Follow‑up after installation (minimum standard) | Every installed item; more often for critical items | Installation day · + 2 weeks · + 1 month · + 3 months (critical items: + 6 and + 12 months, then every 6 months): cracks, whitened areas, loosening, wear at contact points, hardware tight, latches flexible, surface cleanliness, still in intended use; at 3 months the decision keep / reprint / redesign. Each visit recorded in the README table and validated by the 3D printing advisor (owner, Sept 2026) |

Record confirmed values in a "Confirmed by test print" table in the README and STATUS.md. A value is confirmed only after a physical result: a coupon confirms a clearance, the first article confirms the part.



<!-- ===== references/deliverables.md ===== -->

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
                                         (context, exploded, section: once per set of overrides other than part=)
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

*Reference file of the `msf-3dp-design` skill. Read it when a design resembles a past one, and add a line after every test print, review or user correction.* Section numbers (§) are shared by every file of the skill: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · readiness-levels.md · Appendix A glossary.md · Appendix C sources.md.

## 13. Lessons‑learned register
Add a line whenever a test print, a review or a user teaches something. Each line names the project and the rule it changed or confirmed.

| Project | Lesson → rule |
|---|---|
| Tube and hose connectors | Print standing; all connector ends in one plane; 45° whichever end is on the bed; every grip dimension user‑definable, never auto‑derived; a scripted overhang test became the standard (today `check_stl.py`, §10.1 T7) |
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
| UMS pulse oximeter holder (Masimo Rad‑5) | Research (§3.1) before the questionnaire when a device or system is named — the UMS repository already held the F3 holder; copy a fixed interface from the printed files by cross‑section and verify numerically (drawing 40 / 30.6 vs files 44 / 31 → open question); a validated design's files are an acceptable dimension source; ask where cables exit (top, not the assumed bottom); socket‑only coupon; CGAL boolean hygiene (extend 0.2, overlap 0.05, chamfer 0.01 larger than fillet); swept edge profiles instead of body‑wide minkowski; open‑front corner R ≤ wall_t/2; defaults must pass the guards; second overhang pass at 0.02 mm²; drainage hole requested after seeing the render |
| Handwashing tap‑lever pusher | Ask whether the mating part can turn or loosen (a tap on its thread) — found late, forced a redesign; one label = one dimension; confirm the layout before drawing a measuring guide (the tube was drawn on the wrong side); abrupt ends on the upward‑facing side; self‑centring V + 2 mm clearance + flared mouth; clash test and section check; a cut‑through render caught a crevice every automated check missed; multi‑hole notched coupon for a push fit on rusty tube; asserts with float tolerance; guards only for impossible geometry |
| Concentrator twin caster (DeVilbiss 525DS) | "Make a spare wheel" → find the OEM spare first (501DZ‑603); decide scope per component — a printed stem and fork refused, a twin‑wheel body on the original steel stem with an M6 bolt axle accepted as a critical draft; state failure consequences concretely ("corner drops 50 mm", not "tips over"); ask for the user's concept rather than repeating a refusal; lettered measuring diagram and consistency check; confirm filament on the shelf; bolt shank length and nut type; wire retention for a narrow groove; drain in blind sockets; bathroom‑scale load test; building ahead of the coupon allowed, releasing not |
| OT scavenger exhaust adapter | A one‑line request took four rounds — ask "made before?" first; gas‑path position relative to relief valve and filter decides the scope; fail‑open design, no 15/22 mm ends, system risks in the risk assessment, anaesthesia lead in the approval; 1:40 taper modelled, tapered sleeve bore on straight PVC; state tapers in the hand‑off; nominal value + bracketing coupon when the user will not measure; the checker ignores CGAL slivers < 0.001 mm²; raise IPC observations seen in photos (a dark‑filament clamp in theatre) |
| Glucometer battery cover | Overlay the exported outline on the user's photo and get it confirmed before modelling (two re‑traces avoided); label nested edges and ask which is the boundary; fit primitives and cross‑check; photos give no depth; fit‑trial release with an outline check plate when the device is inaccessible; short snap features on thin covers are stiff clicks, not springs; `-D` for a removed parameter is silently ignored |
| D‑shaft knob (replica, PLA) | Read back every sketch view and dimension — hand sketches are not to scale, written numbers govern; undimensioned flare → estimated parameter + overlay; minimum wall computed along Z under the flare (1.27 modelled / ≈ 1.3–1.4 printed, accepted for a moulded replica); cone roof on blind bores, short documented bridge on the ledge to keep the D‑flat engagement; tight‑fit coupon 0.00–0.30/side — PLA D‑bore on Ø6 steel = 0.15/side (*to confirm*), counterbore +0.2 (the default hole compensation was right); implicit approval for a non‑critical item, stated; deliver a zip; context renders (installed, exploded, section) |
| Owner feedback, Sept 2026 (six test designs) | Foolproof strength — design for 2 perimeters / 15 % infill; a drawing with every request for information; the scope gate warns instead of blocking; materials from the shelf, not from the design; test‑before‑use protocols, with test to failure for critical items or batches; standard render set with context views; coupon alongside the product, never before it; STLs in print position; drainage hole option for closed holders |
| Owner feedback 2, Sept 2026 (skill v1.3) | Renders were slow → OpenSCAD 2025.07 with Manifold via npm `openscad-wasm` (`openscad-fast`), 4–22× faster, measured; ask all questions at the start and build in one pass, clicking wherever possible; no licence or certification text in generated documents; README short and visual, details in DATASHEET.md; readiness only on the Humanitarian Making scale, verbatim; context limits hit → token discipline (§1.6); every part also as a one‑file Customizer version per the MSF customizer standard; follow‑up after installation at 2 weeks, 1 month, 3 months minimum, validated by the 3D printing advisor; brims and supports built in only when the geometry cannot be changed; N identical items → N numbered STL files |
| Pipe cross clamp, fixed angle (v1.0–1.4) | Requester review, not the automated checks, caught the structural faults — structural review (T24: load path against the layers, fastener pattern, thinnest loaded section) before release; never clamp with two diagonal bolts — two per side of each clamped member, never collinear; never put bolt load into a thin wing joining a taller block at an inside corner (layers peel) — solid convex caps, counterbores, captive nuts; check the section over a V apex (wedge spreading: 4 mm ≈ 50 MPa → 10 mm ≈ 9 MPa); corner radii adapt to nearby seats and slots; square‑ended seat blocks + a 45° transition sized from the exact rounded outline; hull only adjacent slabs (one hull over both chamfer flares widened a gauge notch 1.4–1.8 mm); section every height band, including the top face where two chamfers meet; Customizer spec alone after the value, help text on the line above; menus for choices, sliders for numbers, an "all printable parts" plate option; sweep.py misread labelled menus and export/sweep assumed one body per STL (fixed in v1.4: CHECK line); background jobs die at the end of a turn — sweeps in foreground chunks with resume |
| Tube drying holder (v1.0 → 2.0) | Three concepts built to full package before one fitted — confirm the holding principle with a concept card before the sizes; ask what may touch the item and whether anything may enter a lumen; ask how it is done today and, after a rejection, the requester's own idea (the stair won); put numbers on soft parts first (ring bending: ~1 mm per newton on a 12 mm silicone tube; inside grip ~100× stiffer; tube weights 11–75 g per metre); every summary says what the current answers exclude; read free‑text picker answers; record rejected concepts; rotate() bookkeeping and a section in front of each host face (a buried feature passes every check); swept bands need r ≥ band + 0.5; `slices = 1` for scaled extrusions; no 2D booleans inside rotate_extrude; fillet budget 2·r ≤ edge; tangent overlaps leave specks (stl_clean.py); size budget < 60 k triangles / 3 MB; sections away from acute edges; section drawings from the STL (section_from_stl.py); hold limits in numbers |
| Toolchain review, Sept 2026 (skill v1.4) | The fast exporter printed every message with a prefix, so warnings and the coupon table never reached the logs; the wasm build had no fonts, so coupons lost their digits unnoticed (the speed table's coupon row too); section checks never ran (networkx missing) and still said PASS; executable bits were not in git, so a fresh clone fell back to the slow engine; the skill's own example and coupon wrote help text after the Customizer spec, which kills the sliders — every script now fails loudly, and lint_customizer.py reads OpenSCAD's own parameter export; the new automatic sections found a thin top wall and a bed sliver in the example that the fixed heights had missed |
| Owner feedback 3, Sept 2026 (skill v1.4) | Menus for every fixed choice, sliders for numbers, free text only for the user's own text; several components → `part` menu with each part in print position, all parts on one plate, and the assembled view; loads along the layers, never pulling them apart (bolts, weight) — print orientation chosen for it; design review with pictures before any documentation; MSF kit hardware (stainless DIN 912 M3/M6 bolts, DIN 125A washers, DIN 985 and DIN 934 nuts) first, otherwise the exact local part with alternatives and where it can be taken from — medical and non‑medical sources listed, the staff decide; README credits Claude and the skill with its link for verification and accountability; the Customizer file carries exactly the five‑line header (@name, @description, @category, @credit, @license — MIT for new MSF designs), only that file, never a variation |


<!-- ===== references/glossary.md ===== -->

# Plain-language glossary

*Reference file of the `msf-3dp-design` skill. Read it when explaining a term to a user — reuse this wording.* Section numbers (§) are shared by every file of the skill: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · readiness-levels.md · Appendix A glossary.md · Appendix C sources.md.

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
- **Watertight (closed solid)** — the model is a closed solid without holes; slicers need this.
- **PETG, PLA, TPU, PC** — plastics: PETG tough and disinfectable (hospital default); PLA easy but soft in heat (training); TPU flexible; PC heat‑resistant.
- **IPC** — infection prevention and control.
- **Personal data** — anything that identifies a person: names, patient numbers, dates of birth, faces, wristbands, screens with records, and hidden photo data such as GPS. Never needed for a design.
- **Primary packaging** — the sealed container that touches the medicine or food itself: vial, ampoule, blister, bottle, sachet, tube. Printed parts may touch the packaging, never the contents.
- **Outline overlay** — the planned shape drawn as a coloured line on your own photo, so you can check at a glance that it follows the real edge.
- **Coupon** — a small test piece with several sizes of the same hole or slot; you print it in minutes, find the step that fits, and tell us its code.
- **Test to failure** — loading one sample until it breaks, to learn the limit and how it breaks; done for critical parts or big batches, not for every part.
- **Brim ears** — small tabs built into the model at the base for adhesion; you snap them off after printing.
- **Manifold** — the new geometry engine inside recent OpenSCAD builds; same result as the old one, many times faster.
- **Customizer file** — the one‑file version of a part whose sliders and menus you can change in OpenSCAD or in the MSF customizer catalogue without touching code; it starts with five lines that name it, describe it, file it in the catalogue, credit its maker and state its licence.
- **Slider / menu** — how the Customizer shows a setting: a slider for a number, a menu to click for a fixed choice (which part, which bolt size), a text box only for your own text (a label).
- **Print plate** — all the parts of an item laid out together, each in its print position, ready to print in one go.
- **Assembled view** — the parts shown together as they are installed, to see how they fit; for looking, not for printing.
- **Design review** — before any files and documents are made, you see pictures of the design (all views, how it is installed, a cut through it) and say "looks right" or what to change.
- **Layer lines** — a printed part is built from thin layers; it is strong along them and weak between them, like wood along and across the grain. Loads must run along the layers, never pull them apart.
- **Kit hardware** — the stainless bolts, washers and nuts that come with the MSF 3D printing kit: Allen bolts M3 and M6 (DIN 912) in several lengths, washers (DIN 125A), self‑locking nuts (DIN 985, with a plastic ring that stops them loosening) and plain nuts (DIN 934).
- **Counterbore / captive nut** — a pocket that sinks a bolt head below the surface / a hexagonal pocket that holds a nut so it cannot turn.
- **Concept card** — one drawing and a few sentences that say how the part will work (what holds the device, what the device feels, how it could fail), confirmed before any sizes.
- **Follow‑up check** — looking at an installed part again on a schedule (2 weeks, 1 month, 3 months) for cracks, wear and loosening, before deciding to keep, reprint or redesign it.



<!-- ===== references/sources.md ===== -->

# Sources and references

*Reference file of the `msf-3dp-design` skill. Read it when citing a rule or pointing a user to further reading.* Section numbers (§) are shared by every file of the skill: §0–§3 SKILL.md · §4 scope-gate.md · §5 design-rules.md · §6–§7 openscad-environment.md · §8 ipc-and-hospital.md · §9 compatibility-and-markings.md · §10 verification.md · §11–§12 deliverables.md · §13 lessons.md · readiness-levels.md · Appendix A glossary.md · Appendix C sources.md.

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
- openscad-wasm (the npm package behind `openscad-fast`, OpenSCAD 2025.07.18 with Manifold): https://www.npmjs.com/package/openscad-wasm — source https://github.com/openscad/openscad-wasm; OpenSCAD Playground (the same engine in a browser): https://github.com/openscad/openscad-playground
- Kit hardware standards: DIN 912 / ISO 4762 socket head cap screws; DIN 934 / ISO 4032 hexagon nuts; DIN 985 prevailing‑torque (nylon insert) nuts; DIN 125A washers; ISO 273 clearance holes; DIN 974‑1 counterbores.
- This skill, for verification of the designs it produced: https://github.com/MSF3Dprinting/MSF-3DP-DESIGN-SKILL
