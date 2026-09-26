# <Item name> — technical specification datasheet

*Full technical record for the 3D printing advisor and the approvers. The short, visual README.md is what users read; this file holds the details. Internal document — no licence statements or certification marks.*

## General Information
| Field | Value |
|---|---|
| Internal Ref. | N/A or MSF code |
| Name | |
| Product stage | Concept / Product in development / Validated / In use |

## FORM
### Product picture
![<item> render or photo](img/<file>.png)
### Version / Category / Subcategory / Critical item / Dangerous goods / Short description
- Version: x.y
- Category: Medical / Logistics / Laboratory / Training / Office
- Subcategory: Biomed / IPC / Pharmacy / WASH / ...
- Critical item: Yes / No   (section 4.2 of the design rules)
- Dangerous goods: No
- Short description: two or three sentences
### Dimensions / Use / Solution type
- Overall dimensions: X x Y x Z mm at default parameters (range if parametric)
- Single/Multiple use: 
- Permanent/Temporary solution: 
### Intended use and out-of-scope uses  (UMS)
- Intended situations of use: 
- Explicitly not intended for: patient contact / patient support / drug delivery / diagnosis / therapy / contact with unpackaged food, drink or medicine / loads above ... / devices other than those listed
### Readiness (Humanitarian Making scale — https://humanitarianmaking.org/resource/readiness-levels)
- Field readiness: <level, exactly as defined in references/readiness-levels.md> — <one-line reason>
- Maker readiness: 
- User readiness: 
- Technology readiness: 
- Risk level: 
- Use the level definitions verbatim from references/readiness-levels.md and apply its MSF interpretation (critical items: risk 3/2/1; single printed part: maker 5/4; with bolts or local materials: 4/3; special materials or technologies: 3/2). Mark every level "proposed" until the 3D printing advisor confirms it.
### Justification of using 3D printed item
- The field problem and why local printing solves it
### Approval required by
- e.g. Biomed advisor, IPC advisor

## FIT
### Compatibility
#### Primary compatibility: exact devices and interfaces, with diameters and other dimensions, per variant
#### Compatible accessories: bolts, screws, zip ties, inserts with sizes
### Tolerance to misalignment (when the mating part can move or vary)
| Case | Lean / shift / angle / tilt | Result (clear / touching / clash) |
|---|---|---|
| | | |
### Parameters (Customizer)
| Parameter | Default | Range | What it changes | Confirmed by test print |
|---|---|---|---|---|
| | | | | |
### Manufacturing Instructions
#### 3D printing optimization
- What is pre-engineered (chamfered bottom edges, compensated horizontal holes, in-built supports, orientation): print as provided, no added supports, do not re-orient
#### Material and color
- Acceptable materials from what is on site, in order of preference, with the difference each makes (e.g. "PETG preferred; PLA acceptable indoors below 40 °C"); clinical items in white, natural or a light colour so soiling and surface imperfections are visible
#### List of other materials
- hardware, zip ties, inserts; N/A if none
#### 3D Printer
- Any FDM 3D printer; reference: Original Prusa MK4S, 0.4 mm nozzle
#### Slicer settings
- Works with the printer's default profile (2 perimeters, 15 % infill); recommended for a longer life: 0.2 mm layer height, 4 perimeters, 40-60 % infill; no supports; brim ears are built in where needed; print sheet for the material, no glue; reference print time and filament use on the MK4S; colour-change heights for banded parts; every STL is in its print position - do not rotate
#### Post processing instructions
- Remove the brim; clean stringing and imperfections; deburr sharp edges
#### Assembly instructions
- Numbered steps; installation position advice (falling-equipment hazard); clean before use
#### QC procedures
- Visual inspection: 
- Dimensional validation: which dimensions, measured with what, accepted range
- Tolerance inspection: how the fit must feel (slides easily, holds firmly, no rattle)
- Safety validation: validated by whom before use
- Test before use: the protocol from the design (function, fit, cleaning, edges; load test, drop test or test to failure where they apply), who performs it and what "pass" is
- Follow-up after installation (minimum; more often for critical items), each visit validated by the 3D printing advisor:
| When | What to check | Result | Checked by | Validated by (3D printing advisor) |
|---|---|---|---|---|
| Installation day | fit, function, stability, no sharp edges, cleaned | | | |
| + 2 weeks | cracks, whitened areas, loosening, cleanliness, still in intended use | | | |
| + 1 month | same + wear at contact points, hardware tight, latches still flexible | | | |
| + 3 months | same + decision: keep / reprint / redesign | | | |
| critical items: + 6 months, + 12 months, then every 6 months | same | | | |

## FUNCTION
### Detailed description of the component/product/workflow and its use
### Additional notes
- Unverified values; tapers and clearance directions; deviations from the MSF design rules and why; hand estimate of stress for load-bearing parts; known limits (e.g. no load rating published)
### Cleaning and disinfection / sterilization procedures
- Agents: Surfanios, bleach 1:10, IPA (or the agents an existing document lists); follow IPC guidelines
- Do not use autoclave
### Packaging and storing instructions
- Sealable zip-lock bags; room temperature; no direct sunlight or humidity
### Related links, standards, safety considerations
- No text or embossed symbols on parts that are cleaned
- Warnings: not a patient-support device / do not autoclave / mount only the listed devices / replace cracked or stiff parts / falling-equipment hazard
- Repository or Printables links; ISO 10993 note where skin or mucosal contact applies
- Items placed in the mouth: the guideline entry or written approval relied on, biocompatibility justification, single-use or reprocessing statement (design rules 4.1b)
### Spaulding Classification (IPC)
- Non-critical / semi-critical / critical, or "no patient contact - to be confirmed by the IPC advisor"
### Risk assessment  (UMS - critical items)
| # | Hazard / failure point | Foreseeable harm | Likelihood | Severity | Mitigation (designed-in / procedural) |
|---|---|---|---|---|---|
| R1 | | | | | |
- Always consider: the mating part moves, loosens or wears; the item falls; any guideline warning category and the advisor's decision

## VERIFICATION (from the build)
| Test | Result | Evidence |
|---|---|---|
| Render at defaults + sweep (T1-T3) | | tools/sweep_report_<date>.txt |
| Watertight, bodies, size, print position (T4-T6) | | tools/check output |
| Overhangs / bridges (T7-T8, two passes) | worst <x>°; bridges: none / documented | |
| Sections and walls (T19) | | |
| One-file Customizer version identical (T22) | | flatten_scad.py --verify |
| Not verified | physical print, load test, ... | |

## ATTACHMENTS
- Files in the package: <item>.scad, <item>_customizer.scad, STLs (one per identical item, with parameter sets and colour-change heights), coupon, renders, tools, brief - none of them containing personal data
- Made with the msf-3dp-design skill v<version>; exporter OpenSCAD <version> (Manifold) — recorded in stl/EXPORT_LOG.txt

| Role | Name | Date |
|---|---|---|
| Designed by | | |
| Product approved by | | |
| Product tested by | | |

## VERSION HISTORY
| Version | Date modified | Modified by | Changes |
|---|---|---|---|
| 1.0 | | | Initial documentation |
