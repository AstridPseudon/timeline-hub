# F-D108 independent baseline custody review (0830)

Decision: **PASS** for the narrow source-only custody scope.

The Sol0820 repair is independently verified against the retained 0813
FAIL_SECOND findings. The published 0803 full index, author canonical copy,
and review canonical copy are byte-identical at SHA-256
`d6ed7dc547645742c405e9b9288e00617f33e5f8ee378233b46fc621affd226a`.
Exactly 23 rows changed from the retained preimage, XML ordinals 12309–12331,
and only `file`, `line`, and `source_location_method` changed.

All 23 repaired source pairs resolve to actual Git blobs in Agent commit
`92443771676ef2bbb547d0a103d708fa8bec4c63`; the independent check read 762
source files, verified all 12,517 canonical definition mappings, and compiled
both `tools/astrid-rename/tests` source blobs in memory. The canonical source
accounting is 12,515 exact and two explicitly ambiguous AST bases (ordinals
9439 and 9440), distinct from current-selector join ambiguity.

The authentic XML remains SHA-256
`2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f` with
12,517 testcase nodes, 12,396 PASS / 91 FAIL / 14 ERROR / 16 SKIP, 566
subtests, and suite total 13,083. Current joins remain byte-exact at SHA-256
`0fbcdf46e9272a2a3bd1e3f275cfa09f2887e50bef848f41c68c2c71a8ef12c5`: 9,268
rows, 2,956 exact, 6,312 absent, and zero ambiguous. The original summary
(`7af40efb...dbfd7`) and protected historical 0758/0813 review bytes remain
unchanged; dependent JSON/Markdown references were read back with truthful
hashes and no stale 0813 hashes remain in the 0756/0803 successor documents.

Boundary claims are preserved: upstream is FAIL/exit 1; Runtime isolation is
UNCERTAIN; current failure classification and core-open count remain withheld
until D108 terminal. No baseline FAIL or Runtime UNCERTAIN state was promoted.

Checks:

- `python3 .../workers/agt-F-D108-baseline-custody-sol-0820/evidence/validate-custody.py` — **exit 1**, after its custody assertions, because its hard-coded Sol worktree `/home/user/work/wt/agt-F-D108-baseline-custody-sol-0820` no longer exists when it reaches `git diff --check`. This is an environment/path issue, not an evidence assertion failure.
- `python3 .../workers/agt-F-D108-baseline-custody-review-0830/evidence/independent-review.py` — **PASS**.
- `git diff --check` in this composition review checkout — **PASS**.
- Product tests, typecheck, lint, pytest, collection, bodies, services, probes, browsers, installs, and full suites — **N/A/not run** by the read-only custody-review scope.

Independent machine-readable results are in
`workers/agt-F-D108-baseline-custody-review-0830/evidence/independent-review.json`.
No product repository or author output was edited.
