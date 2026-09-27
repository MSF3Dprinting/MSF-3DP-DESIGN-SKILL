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

