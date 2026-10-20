# AP2-M2 bootstrap listed-timeline review gate

## Result

**NOT QUALIFIED — the one authorized central bootstrap-only run failed at the
new exact outbox-scope timing guard.** No source edit was made and no retry was
submitted.

## Review

- Candidate target: `9308c1277` (`tl/ap2-m2-bootstrap-created-timeline-scope-source`).
- `timelineFromList` selects only an exact `timeline_id`; seeded callers still
  use their explicit seeded project/timeline scope.
- The bootstrap test observes the created project from the URL and the exact
  UI-selected timeline from the URL, then requires the matching realm/project/
  timeline outbox scope before polling that created project’s normal Runtime
  list. No arbitrary timeline, widened scope, forced-ready path, timeout
  inflation, or wrapper typecheck was added.
- The existing native create/init ordering, history, outbox, retry, reload /
  restart, guarded undo, opaque-data, and zero-legacy assertions remain
  present after the new gate. Composition 0.0.13 and the proven graph guard
  were retained.

## Checks

- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — PASS.
- `./node_modules/.bin/eslint tests/e2e/local/support/timeline-scope.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/three-products.spec.ts --ext ts --report-unused-disable-directives --max-warnings 0` — PASS.
- `./node_modules/.bin/tsc -p tsconfig.node.json --noEmit --pretty false` — PASS.
- Targeted scope types with `tsc --noEmit --allowImportingTsExtensions ...` — PASS.
  The first probe omitted `--allowImportingTsExtensions` and failed only on
  TS5097; the corrected probe passed.
- `git diff --check` and final `git status` — PASS; worktree clean.

Central request (exactly one):

```text
ap2-m2-bootstrap-listed-timeline-review-gate-ap2-m2-bootstrap-scoped-audit-central-gate-1020222120-1691
```

The absolute narrowed driver selected exactly one bootstrap test before build;
hosted build, source tuple, private graph, and graph guards passed. It retained
Agent `3c4f6de4`, Runtime `202074110717146fc7f08af2306a8dd7f695b0b1`, producer
`a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, artifact `f021…`, schema `6ba…`,
and Composition 0.0.13. The test failed after 90 seconds at
`tests/e2e/local/three-products.spec.ts:1170-1172`: no outbox owner matching
the created project and selected timeline appeared. The Runtime list poll and
all later assertions were therefore not reached.

The first-failure stack and source tuple are retained in the central result
log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-bootstrap-listed-timeline-review-gate-ap2-m2-bootstrap-scoped-audit-central-gate-1020222120-1691/log.txt`

The browser trace was emitted under the central driver’s disposable temp
directory and removed during service cleanup; no other run’s trace is claimed.

## Next step

Inspect why the production initializer’s selected created timeline does not
produce the matching outbox scope in this frozen tuple. Qualify a new candidate
only after an approved fixture/source correction; do not rerun this unchanged
tree.
