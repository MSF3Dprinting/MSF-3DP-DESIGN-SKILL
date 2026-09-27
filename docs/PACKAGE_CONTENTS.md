# Package contents — msf-3dp-design v1.4.0 (27 September 2026)

This one archive is the complete package and installs directly as a skill (SKILL.md is in the top-level folder).

| Item | What it is | Use it for |
|---|---|---|
| `SKILL.md`, `references/`, `scripts/`, `scad/`, `templates/`, `evals/` | The skill itself | upload the archive in claude.ai (Settings → Capabilities → Skills), or copy the folder to `.claude/skills/msf-3dp-design/` in a repository for Claude Code |
| `docs/PROJECT_INSTRUCTIONS.md` | The always-on text (priorities, hard rules, "use the skill"). An upload cannot install this — paste it into the Project's instructions (claude.ai) or into the repository's CLAUDE.md (Claude Code) | claude.ai Projects; Claude Code repositories |
| `docs/COMPILED_WORKFLOW.md` | SKILL.md and every reference stitched into one document for reading and review; regenerate with `scripts/compile_reference.py` | reviewing the rules as a whole |
| `docs/CHANGELOG.md` | What changed in each version | release notes |
| `docs/workflow-history/CLAUDE_v1.2.md`, `CLAUDE_v1.1.md` | The monolithic workflow files the skill was cut from; later changes live in the skill only | record only; the skill supersedes them |

Quick start: install, paste `docs/PROJECT_INSTRUCTIONS.md` into the Project instructions (or CLAUDE.md), then send "I need something to hold the oximeter next to the bed". Check that the questions come as clickable options in consecutive rounds, followed by one confirmation with a concept card, pictures of the design for your approval, and only then the files.
