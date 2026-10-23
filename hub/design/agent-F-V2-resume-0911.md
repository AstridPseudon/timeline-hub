# Agent F V2 resume review — 0911

Result: **PASS for the exact fixture-only source review.**

Reviewed exact source: `6e27aff9c02bbfa0f9f667206193b65ad1de0fe6`, branch
`tl/agt-F-V2-resume-0911`, parent `fad05679a`. The commit contains only the
two intended fixture test files. The resumed worktree remains clean; this
review made no product or test edits.

Evidence:

- Original named scalar and graph nodes: **2 passed in 2.58s**.
- Focused invalid timing/schema controls: **14 passed in 3.78s**.
- Single bounded exact-tree type comparator: **exit 0**, current `1912`,
  baseline `1912`, completed within the `180s` limit.
- Ruff: **2149 current / 2149 baseline**.
- Vendor lock, artifact manifest, and both diff checks: **pass**.

No-weakening result: **pass**. Scalar authentic retained schema custody is in
place at element creation and replacement, with the original stale-basis
refusal and no-state-change assertions retained. Graph setup changes only the
new occurrence duration `2000ms -> 3000ms` so C0's half-open timing rule admits
the original child `hold=3`; original IDs and reload/inverse/redo assertions
remain. No positive-to-refusal conversion, skip, xfail, deletion, production
validator/provider/runtime change, generated-file change, or baseline change
was found.

Limits: this remains detached Agent fixture evidence, not Runtime authority,
integration acceptance, upstream status, or full-suite evidence. No daemon or
dispatcher recovery was invoked. Next owner is Agent integration/review, which
should rerun the two named nodes on the preserved integration head.
