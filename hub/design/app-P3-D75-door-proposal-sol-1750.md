**HOLD — v3 is not ready to apply.** Added only [proposed-v3.patch](/home/user/work/wt/app-P3-D75-door-proposal-sol-1750/proposed-v3.patch), retained controls, and [evidence with hashes and predicate map](/home/user/work/wt/app-P3-D75-door-proposal-sol-1750/proposal-evidence-v3.txt). Protected source remains unchanged.

Source confirms 1731’s old-URL premise was wrong: commits use the stable Runtime door. V2’s equality with the dynamic daemon URL was also wrong.

A further lifecycle conflict remains: the intermediate `page.reload()` can automatically retry A before restart, violating the original forwarded-count guard. Holding that retry instead produces four observed attempts before release, violating D75’s exact three.

Validation:

- `/opt/node20/bin/node --import tsx --test tests/e2e/local/support/gate5-fault-order.test.mjs proposal-controls-v3.mjs` — **20/20 passed**, including two controls requiring the candidate lifecycle to fail.
- `proposal-controls-v3.mjs --lint` — zero diagnostics.
- `proposal-controls-v3.mjs --types` — 23 baseline / 23 virtual, zero new diagnostics.
- `git apply --whitespace=error --check proposed-v3.patch` and artifact whitespace checks — passed.
- No browser, service, original journey, or full suite run.

Applied source delta: **0 bytes**. Unapproved candidate: **+37/-2 lines, net +1,839 bytes**.

**ORCH scope question:** may the intermediate mounted reload/persistence block be consolidated into the post-restart fresh mount, retaining its exact persistence predicates and wait ceilings?

Wrote the conventional commit message and `BLOCKED` marker. Recommend resolving that question before independent review or application.