# <Item name>

![overview](img/<item>_<variant>_sheet.png)

**What it is:** <one sentence>. **Use:** <where and how, one sentence>. **Not for:** <out-of-scope uses — patient support, unpackaged medicine, loads above … kg>.
**Fits:** <exact devices / tubes / rails with sizes>. **Holds:** <hold limit in numbers, e.g. "a 1 kg device; tested to 2 kg"> . **Critical item:** yes / no — approval by <role(s)> before use.

## Parts to print
| # | Part | File | Qty | Picture |
|---|---|---|---|---|
| 1 | <part> | `stl/<item>_<part>_v<x.y>.stl` | 1 | ![](img/<item>_<part>_iso.png) |
| 2 | <second part> | `stl/<item>_<part2>_v<x.y>.stl` | 1 | ![](img/<item>_<part2>_iso.png) |
| 1+2 | All parts on one print plate (instead of 1 and 2) | `stl/<item>_plate_v<x.y>.stl` | 1 | ![](img/<item>_plate_iso.png) |
| 3 | <identical items, e.g. rib> | `stl/<item>_rib_1_v<x.y>.stl` … `_10_` | 10 | ![](img/<item>_rib_iso.png) |
| C | Fit coupon — print first, tell us the step that fits | `stl/<item>_coupon_v<x.y>.stl` | 1 | ![](img/<item>_coupon.png) |

All files are in print position: import, slice, print. No supports. <Brim ears are built in / no brim needed.> `stl/view_only/` holds the assembled view — for looking, not for printing.

## Hardware
| Part | Qty | From | If it is not available | Where it can be taken from |
|---|---|---|---|---|
| Bolt M6 × 40, DIN 912, stainless | 2 | MSF 3D printing kit | <alternative 1>; <alternative 2> | <medical and non-medical sources> |
| Washer DIN 125A M6 | 4 | kit | — | — |
| Self-locking nut DIN 985 M6 | 2 | kit | plain nut DIN 934 M6 + thread glue | — |
| <local part: standard, size, length, material> | <n> | local | <two alternatives> | <medical and non-medical sources — the staff decide> |

## Print
- Material: <acceptable materials in order, e.g. PETG preferred; PLA acceptable indoors> · colour: <light colour for clinical items>
- Settings: works with the printer's default profile (2 perimeters, 15 % infill); recommended 0.2 mm layers, 4 perimeters, 40–60 % infill · print time about <h> on the MK4S
- First print the coupon (≈ <min> min); reply with its code; then print the parts.

## Install / use
![in place](img/<item>_<variant>_context.png) ![assembled](img/<item>_assembly_iso.png)
1. <step>
2. <step> (![exploded](img/<item>_<variant>_exploded.png) if there is an assembly)
3. Position away from patients, cots and walkways; the device must stay easily removable.

## Clean
Wipe with Surfanios, bleach 1:10 or IPA. Do not autoclave. <Drain hole keeps the floor dry.>

## Check
**Before use:** fits without forcing or rattle · holds the load, 10 cycles · no sharp edges · cleaned. **Hold limit:** <in numbers>. **Then, validated by the 3D printing advisor:**
| When | Check | Date | Result | Validated |
|---|---|---|---|---|
| Installation day | fit, function, stability, cleaned | | | |
| + 2 weeks | cracks, whitened areas, layers opening, loosening, cleanliness | | | |
| + 1 month | same + wear at contact points, hardware tight | | | |
| + 3 months | same + keep / reprint / redesign | | | |
| critical items: + 6 months, + 12 months, then every 6 months | same | | | |
Replace at the first crack, whitened area or opening layer — reprinting is the normal fix.

## Details
`DATASHEET.md` — full specification, parameters, hardware, structural review, tests, risk assessment, readiness, version history. `<item>_customizer.scad` — one-file version for the OpenSCAD Customizer and the MSF customizer catalogue (sliders and menus, no code to edit).

| Role | Name | Date |
|---|---|---|
| Designed by | Claude (Anthropic), msf-3dp-design skill v<version>, for <requesting role / department> | |
| Approved by (Biomed / IPC / …) | | |
| Tested by | | |

Version <x.y> — <date>. Designed by Claude using the MSF 3D printing design skill v<version> — https://github.com/MSF3Dprinting/MSF-3DP-DESIGN-SKILL — for verification and accountability.
