## Report

**Overall: FAIL — packaging metadata only.**

- **Census:** PASS — 201 closed / 66 open of 267.
- **Qualified delta:** PASS — +29 exact originals: 7 H3 + 22 inverse.
- **0550 correction:** PASS — historical 172/95 preserved; 179/88 clearly historical; prior 37-row mapping unchanged.
- **0600 delta:** PASS — exact 22 inverse rows, 16 corruption + 6 retained-scope; 59-row mapping totals 30+7+22.
- **Baseline preservation:** PASS — all prior 172 node records unchanged.
- **Evidence SHA:** PASS — `705c6df3a22200510c335143826c9a57df5de8ea05abe1697e4ca21058586771`.
- **AST/source checks:** PASS — H3 current/installed source hashes match; inverse source-mode proof records unchanged target functions and authoritative helper use.
- **Exclusions:** PASS — no aggregate credit; source-copy, D40, track-label, ABA, IMAGE, renderer, and Farm remain non-credit/open.
- **Full result:** Original full run remains `FAIL 17159 passed,262 failed,5 errors,4 skipped`; no new full-suite claim.

Blocking defect: `reconciliation.active_family_counts["Rendering missing result file"]` is stale at `6`, although those six nodes are `proven_passed`. Metadata sums to 72 active nodes while actual active membership is 66. Correct this field to `0`, then recompute the external SHA, limits reference, and mapping base hash.

Checks:

- JSON/count/hash/ID/mapping/source audits: PASS except the family-count coherence check.
- `git diff --check 2007cf7aaf5d304964e68a33e967502a16de1d24..1f929a4acb`: PASS.
- No tests, product changes, or full suite were run.

Completion marker and commit message were written.