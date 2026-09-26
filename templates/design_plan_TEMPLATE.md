# Design plan — <item name>

Brief version <x.y> approved on <date> by <role>. One stage per conversation where possible; each stage ends at its gate.

| # | Sub-task | Output (file / render / check result) | Load | Gate — what the user does |
|---|---|---|---|---|
| 1 | Shared values, helpers, coupon, checker (multi-item sets: always first) | common.scad, test_coupon.scad + STL, tools/ | Low | — |
| 2 | Model: <main body> | <item>.scad, preview render | Medium | accepts the preview |
| 3 | Model: <interfaces / attachment options> | updated .scad, ghost previews | Medium | confirms fit types |
| 4 | Verification (§10) and render set (T14) | sweep report, check results, img/ | Low | — |
| 5 | Delivery package (§11) | zip, README, EXPORT_LOG | Low | prints coupon, then part |
| 6 | Coupon and first-article feedback (§2.5), revision | confirmed-values table, v<x.y+1> | Low | reports fit, photos |

Rules: never add work to a High stage; stages 3–6 may run in one pass for a single Low-load part when the user says "proceed"; building ahead of a physical result is allowed, releasing is not.
