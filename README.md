# msf-3dp-design — skill for the MSF OpenSCAD design workflow

A Claude skill (SKILL.md + references, scripts, scad library, templates) that turns a request from an MSF field user into a safe, cleanable, printable, parametric 3D-printed part with a short visual README and a full datasheet. v1.4 adds: a design review with pictures before any file or document; menus and sliders in the Customizer, never typing a fixed choice; an exact five-line header in every Customizer file; all parts on one print plate and an assembled view; loads along the layers with a structural review; MSF kit hardware first, with local alternatives and sources; a README that credits Claude and links this repository; and a toolchain that fails loudly. See docs/CHANGELOG.md.

**Version:** 1.4.0 (owner feedback 3, lessons from the tube holder and pipe clamp, toolchain review — 27 Sep 2026) · **Owner:** MSF 3D Printing Advisor · internal MSF material. Designs made with the skill credit it and link here for verification and accountability.

## Install
- **claude.ai:** Settings → Capabilities → Skills → upload the archive as it is (SKILL.md sits in its top-level folder). Team / Enterprise owners can share it with the organisation from Organization settings → Plugins & skills. Then paste `docs/PROJECT_INSTRUCTIONS.md` into the Project's instructions so the priorities and hard rules are always on — an upload cannot do that step.
- **Claude Code:** copy the folder to `.claude/skills/msf-3dp-design/` in the design repository (shared with everyone who clones it) or to `~/.claude/skills/msf-3dp-design/` for yourself — the folder name must stay `msf-3dp-design`; or distribute it as a plugin. Put the text of `docs/PROJECT_INSTRUCTIONS.md` into the repository's `CLAUDE.md` so the hard rules are always on.
- **Any sandbox:** `bash scripts/install_openscad.sh` sets up native OpenSCAD 2021.01 (PNG views only), `openscad-fast` (OpenSCAD 2025.07 with the Manifold engine — every geometry export, 4–28× faster) with fonts, and the Python tooling; it ends with a readiness test.

## Layout
```
SKILL.md                 workflow core: behaviour, questionnaire, design review, build pass (always loaded when the skill triggers)
references/              rules read on demand — scope gate (§4), design rules (§5: loads along the layers, kit hardware, soft parts),
                         OpenSCAD and Customizer (§6–7), IPC (§8), compatibility and markings (§9), verification (§10),
                         deliverables and order of work (§11–12), readiness levels, lessons (§13), glossary, sources
scripts/                 universal tools: install_openscad.sh; openscad-fast + openscad_manifold.mjs (Manifold exporter); export.sh;
                         check_stl.py, sweep.py, stl_clean.py, compare_meshes.py; render_views.py, section_from_stl.py, overlay_sketch.py;
                         flatten_scad.py (Customizer file with its header), lint_customizer.py; compile_reference.py
scad/                    common.scad (defaults, MSF kit hardware), helpers.scad (modules, print_plate, kit cutters),
                         test_coupon.scad (universal coupon with presets), context_scene.scad (context renders),
                         example_part.scad (worked example: two parts, kit bolts, part menu with all parts and the assembled view)
templates/               README (short, visual), DATASHEET (full), design brief, design plan, STATUS, lessons learned, request summary, variants
evals/                   test prompts with checkable expectations (skill-creator format); files/ holds a synthetic test photo
docs/                    for humans: PROJECT_INSTRUCTIONS.md to paste, COMPILED_WORKFLOW.md for review, CHANGELOG.md, PACKAGE_CONTENTS.md, workflow-history/
```
`python3 scripts/compile_reference.py` writes `docs/COMPILED_WORKFLOW.md`, the whole workflow as one file for reading or review.

## Updating
Lessons from a design go into `references/lessons.md` (one line per project) by pull request; rule changes into the reference that owns the section. Every rule change bumps the version in SKILL.md's title, this README, docs/CHANGELOG.md and docs/PACKAGE_CONTENTS.md together, and updates docs/PROJECT_INSTRUCTIONS.md when a hard rule changes; regenerate docs/COMPILED_WORKFLOW.md. Every README produced by the skill records the skill version it was made with.
