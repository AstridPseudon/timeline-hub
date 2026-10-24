## Report

Completed F/D54a terminal upstream comparison.

- Verified terminal service: exit `1`, 12,396 passed, 91 failed, 14 errors, 16 skipped, 566 subtests, 3,563.50s.
- Validated durable XML, source/runtime tuple, environment guards, and completeness.
- Compared all exact 276 selectors:
  - 75 matched: 66 failed, 9 passed
  - 201 missing/renamed/uncollected: UNKNOWN, never PASS
- Current rollup preserved: 162 PASS, 112 OPEN, 2 deferred.
- Identified all five current core-open worker-ready selectors; no current regression proven.
- Preserved deferred checkpoint contrast without relabeling it as regression.
- Evidence written under `.../workers/agt-F-D60-baseline-terminal-1452/evidence/` (~1.1 MB).

Validation:

- Prepared comparator: exit `2` as expected because 201 selectors remain UNKNOWN.
- JSON/XML/TSV integrity assertions: PASS.
- `git diff --check`: PASS.
- Worktree clean; no product/test/source edits or reruns.

Commit message and empty `DONE` marker created.