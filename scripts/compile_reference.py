#!/usr/bin/env python3
"""compile_reference.py — concatenate SKILL.md and every reference into one Markdown file for reading or review.
Usage: python3 scripts/compile_reference.py [skill_dir] [out.md]"""
import os, sys
skill = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(skill, "COMPILED_WORKFLOW.md")
order = ["SKILL.md"] + [os.path.join("references", f) for f in [
    "scope-gate.md", "design-rules.md", "openscad-environment.md", "ipc-and-hospital.md",
    "compatibility-and-markings.md", "verification.md", "deliverables.md", "readiness-levels.md", "lessons.md", "glossary.md", "sources.md"]]
parts = []
for rel in order:
    p = os.path.join(skill, rel)
    if os.path.exists(p):
        text = open(p, encoding="utf-8").read()
        if rel == "SKILL.md" and text.startswith("---"):
            text = text.split("---", 2)[2]  # drop the front matter
        parts.append(f"\n\n<!-- ===== {rel} ===== -->\n\n" + text)
open(out, "w", encoding="utf-8").write("# MSF OpenSCAD design workflow — compiled view\n" + "".join(parts))
print("written", out)
