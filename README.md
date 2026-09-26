# msf-3dp-design — skill for the MSF OpenSCAD design workflow

A Claude skill (SKILL.md + references, scripts, scad library, templates) that turns a request from an MSF field user into a safe, cleanable, printable, parametric 3D-printed part with a short visual README and a full datasheet. v1.3 adds: questions front-loaded and click-first, one build pass; OpenSCAD 2025.07 with Manifold as the exporter (`openscad-fast`, 4–22× faster); one-file Customizer version of every part; numbered STL copies; follow-up schedule; no licence text in generated documents. See docs/CHANGELOG.md.

**Version:** 1.3.1 (owner feedback 2 + readiness scale, 26 Sep 2026) · **Owner:** MSF 3D Printing Advisor · internal MSF material.

## Install
- **claude.ai:** Settings → Capabilities → Skills → upload the archive as it is (SKILL.md sits in its top-level folder). Team / Enterprise owners can share it with the organisation from Organization settings → Plugins & skills. Then paste `docs/PROJECT_INSTRUCTIONS.md` into the Project's instructions so the priorities and hard rules are always on — an upload cannot do that step.
- **Claude Code:** copy the folder to `.claude/skills/msf-3dp-design/` in the design repository (shared with everyone who clones it) or to `~/.claude/skills/` for yourself; or distribute it as a plugin.
- **Any sandbox:** `bash scripts/install_openscad.sh` sets up native OpenSCAD 2021.01 (PNG views), `openscad-fast` (2025.07 + Manifold, geometry export) and the Python tooling.

## Layout
```
SKILL.md                 workflow core: behaviour, gates, intake (always loaded when the skill triggers)
references/              rules read on demand — scope gate (§4), design rules (§5), OpenSCAD (§6–7), IPC (§8),
                         compatibility and markings (§9), verification (§10), deliverables (§11–12), lessons (§13), glossary, sources
scripts/                 universal tools: openscad-fast + openscad_manifold.mjs (Manifold exporter), check_stl.py, sweep.py,
                         render_views.py, overlay_sketch.py, flatten_scad.py, export.sh, install_openscad.sh, compile_reference.py
scad/                    common.scad (defaults), helpers.scad (modules), test_coupon.scad (universal coupon),
                         context_scene.scad (context renders), example_part.scad (worked example)
templates/               README (short, visual), DATASHEET (full), design brief, design plan, STATUS, lessons learned, request summary, variants
evals/                   test prompts used to check that the skill triggers and behaves
docs/                    for humans: PROJECT_INSTRUCTIONS.md to paste, COMPILED_WORKFLOW.md for review, workflow-history/
```
`python3 scripts/compile_reference.py` writes `COMPILED_WORKFLOW.md`, the whole workflow as one file for reading or review.

## Updating
Lessons from a design go into `references/lessons.md` (one line per project) by pull request; rule changes into the reference that owns the section; bump the version here and in SKILL.md's description only when behaviour changes. Every README produced by the skill records the skill version it was made with.
