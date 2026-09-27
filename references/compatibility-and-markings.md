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

