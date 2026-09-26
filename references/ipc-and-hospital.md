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

