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

