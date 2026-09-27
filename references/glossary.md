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

