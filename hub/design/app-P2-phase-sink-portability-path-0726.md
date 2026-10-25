# P2 phase-sink portability path — FAIL

No source changes were made. The frozen worktree remains clean at `f09c357e…`.

Finding: D105 is not portable. The committed Node suite depends on pre-squash Git history:

- `scripts/testing/d66-plain-stack.test.mjs:225` uses fixed `git show f0fcdce…`.
- Lines 14–15 and 264–266 use fixed `git ls-tree`/`git cat-file` for `f7201e02…` and blob `9fccbff…`.

Focused evidence:

- Current tree: D105 passed (`1 passed, 26 skipped`) with those historical objects present.
- Fresh source snapshot with no historical objects: D105 failed before production-caller execution with `fatal: not a tree object` at line 264.
- Existing reviewer27 evidence remains the behavioral boundary: seed ordinal 1 preserved; two ordinal-2 starts succeeded with separate `launch-*` directories and `0600` logs; old source collided; full P2 inventory is 3 files/8 cases with worker-scoped and placement fixtures sharing `runtime-private`.

Whole-path map:

1. D66 configures seed logging at `runtime-private`, ordinal 1.
2. `DirectHarness.start()` prepares the sink, starts Runtime, and seeds.
3. `enableTimelineAuthoring()` starts the captured authoring Runtime.
4. P2 launches stage-2 fixtures with ordinal 2.
5. Each start allocates a private child directory; shutdown writes `runtime.stdout/stderr` with `wx`, mode `0600`.
6. The eight P2 gesture bodies, reload, and undo remain unverified here, as already recorded by the prior review.

Checks:

- Node20 syntax checks: PASS.
- `git diff --check`: PASS.
- Existing reviewer27 D66 evidence: `27 passed, 0 failed`.
- No live Runtime, browser, full suite, build, install, or shared dependency changes.

Decision: blocker confirmed. The normal committed suite must stop requiring fixed historical Git objects; old-red historical proof may remain external evidence but must not gate ordinary execution.

`DONE` and commit message were written. No `report.md` or design sidecar was written; this final response is the report.