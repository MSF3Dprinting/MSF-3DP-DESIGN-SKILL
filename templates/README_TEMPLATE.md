# <Item name>

![overview](img/<item>_sheet.png)

**What it is:** <one sentence>. **Use:** <where and how, one sentence>. **Not for:** <out-of-scope uses — patient support, unpackaged medicine, loads above … kg>.
**Fits:** <exact devices / tubes / rails with sizes>. **Critical item:** yes / no — approval by <role(s)> before use.

## Parts to print
| # | Part | File | Qty | Picture |
|---|---|---|---|---|
| 1 | <part> | `stl/<item>_<variant>_v<x.y>.stl` | 1 | ![](img/<item>_<variant>_iso.png) |
| 2 | <identical items, e.g. rib> | `stl/<item>_rib_1_v<x.y>.stl` … `_10_` | 10 | ![](img/<item>_rib_iso.png) |
| C | Fit coupon — print first, tell us the step that fits | `stl/<item>_coupon_v<x.y>.stl` | 1 | ![](img/<item>_coupon.png) |

All files are in print position: import, slice, print. No supports. <Brim ears are built in / no brim needed.>

## Print
- Material: <acceptable materials in order, e.g. PETG preferred; PLA acceptable indoors> · colour: <light colour for clinical items>
- Settings: works with the printer's default profile (2 perimeters, 15 % infill); recommended 0.2 mm layers, 4 perimeters, 40–60 % infill · print time about <h> on the MK4S
- First print the coupon (≈ <min> min); reply with its code; then print the parts.

## Install / use
![in place](img/<item>_context.png)
1. <step>
2. <step> (![assembly](img/<item>_exploded.png) if there is an assembly)
3. Position away from patients, cots and walkways; the device must stay easily removable.

## Clean
Wipe with Surfanios, bleach 1:10 or IPA. Do not autoclave. Drain hole keeps the floor dry.

## Check
**Before use:** fits without forcing or rattle · holds the load, 10 cycles · no sharp edges · cleaned. **Then, validated by the 3D printing advisor:**
| When | Check | Date | Result | Validated |
|---|---|---|---|---|
| Installation day | fit, function, stability, cleaned | | | |
| + 2 weeks | cracks, whitened areas, loosening, cleanliness | | | |
| + 1 month | same + wear at contact points, hardware tight | | | |
| + 3 months | same + keep / reprint / redesign | | | |
| critical items: + 6 months, + 12 months, then every 6 months | same | | | |
Replace at the first crack or whitened area — reprinting is the normal fix.

## Details
`DATASHEET.md` — full specification, parameters, tests, risk assessment, readiness, version history. `<item>_customizer.scad` — one-file version for the Customizer.

| Role | Name | Date |
|---|---|---|
| Designed by | | |
| Approved by (Biomed / IPC / …) | | |
| Tested by | | |

Version <x.y> — <date> — skill v<version>
