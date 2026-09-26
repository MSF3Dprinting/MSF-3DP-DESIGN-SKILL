# Package contents — msf-3dp-design v1.3.1 (26 September 2026)

This one archive is the complete package and installs directly as a skill (SKILL.md is in the top-level folder).

| Item | What it is | Use it for |
|---|---|---|
| `SKILL.md`, `references/`, `scripts/`, `scad/`, `templates/`, `evals/` | The skill itself | upload the archive in claude.ai (Settings → Capabilities → Skills), or copy the folder to `.claude/skills/msf-3dp-design/` in a repository for Claude Code |
| `docs/PROJECT_INSTRUCTIONS.md` | The always-on text for the Project's instructions field (priorities, hard rules, "use the skill"). An upload cannot install this — paste it into the Project | claude.ai Projects; or as a short CLAUDE.md in a repo |
| `docs/COMPILED_WORKFLOW.md` | SKILL.md and every reference stitched into one document for reading and review; regenerate with `scripts/compile_reference.py` | reviewing the rules as a whole |
| `docs/workflow-history/CLAUDE_v1.2.md`, `CLAUDE_v1.1.md` | The monolithic workflow files the skill was cut from (v1.2 = owner feedback 1 + six test designs); v1.3 changes live in the skill only — see `docs/CHANGELOG.md` | record only; the skill supersedes them |

Quick start: install, paste `docs/PROJECT_INSTRUCTIONS.md` into the Project instructions, then send "I need something to hold the oximeter next to the bed" and check that the questions come as clickable options in consecutive rounds, followed by one confirmation and a single build pass.
