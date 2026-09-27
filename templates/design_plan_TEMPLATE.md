# Design plan — <item name>

Confirmed on <date> by <role> (Request Summary and concept card). One item family per conversation; the only user clicks are the design review and the feedback after the print (SKILL.md §2).

| # | Sub-task | Output (file / picture / check result) | Check |
|---|---|---|---|
| 1 | Shared values, helpers, coupon (multi-item sets: always first) | common.scad, helpers.scad, test_coupon.scad with its preset | coupon exports and passes check_stl |
| 2 | Model the working file: <components>, part menu (each part, all, assembly), kit hardware | <item>.scad | lint_customizer.py on the working file |
| 3 | Automated checks | sweep report (chunks merged), check_stl with sections auto | no FAIL; no specks at defaults |
| 4 | Structural review | load table, hand estimates, section drawing | every load along the layers (T24) |
| 5 | Design review — **user click** | render sheet, assembled view, section | "looks right" or changes → back to 2 |
| 6 | Build pass | <item>_customizer.scad (exact header), export.sh release, README, DATASHEET, zip | T1–T26 table filled in |
| 7 | Coupon and first-article feedback (§2.2) — **user click** | confirmed-values table, v<x.y+1> | values confirmed by print |

Rules: building ahead of a physical result is allowed, releasing is not; a change at the design review costs a model edit, never a documentation rewrite; when the turn or the context runs out, deliver what is verified and write STATUS.md.
