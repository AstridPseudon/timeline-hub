# Selected-server lifecycle correction

Fixed on App base `b9c03ef5ba705312dc36f37f4b7b5fa7fd0a784c` in `/home/user/work/wt/app-m2-selected-server-lifecycle-fix`. No blocker or decision disagreement. D01 and qualification remain OPEN.

## Changes and decisions

Only `src/tools/video-editor/commands/commitSession.ts` and its existing `commitSession.selectedParams.test.ts` changed.

- Recognize native selected and inverse command acceptance as requiring the actual server closure, including while retaining newer suffixes. Accepted inverse seed 4 replaces the formerly displayed seed 8.
- Reconstruct the working bundle from accepted state plus remaining ordinary move/label preview writes. Existing ordinary executors run against each payload's ORIGINAL capture to obtain those writes; neither stored commands nor their guards/basis/pins change. Container creation preserves existing opaque fields; clip mirror synchronization uses the resulting accepted-plus-ordinary clips, never an old full PARAM after-state. Selected and inverse results are never locally executed.
- Recovery projects the saved accepted closure for a selected/inverse acceptance and retains the exact ordinary suffix. Ordinary-only recovery still projects the original display basis, preserving the existing original-B recovery control.
- Explicit cancellation rebuilds from acceptance instead of restoring the canceled draft's stale `before`. A fresh capture after cancellation has accepted seed 4 and `acceptedBasisAvailable: true`; the original pending capture remains false and immutable.
- Remaining selected intent publishes `pending` with its reason, including after canceling an ordinary tail. Known unsent pending work exposes cancellation through the existing `canUndo` field when no request is pending; provider-acceptance pending does not enable it.

Promoted all four external counterexamples into the existing selected session suite with their original expected outcomes unchanged. Added one neighboring regression: inverse ACK with selected + two ordinary suffixes, successive tail cancellations, exact retained-intent equality, immutable original false flag, preserved opaque parameters, working move position, and a new selected submission on actual accepted P2.

The 08:36 decision is preserved: one SERVER validator, native original exact schema pin, no selected local after-state before ACK. No wire/schema/provider/browser export, queue/store, pin, UI activation or hook change. The helper reconstructs ordinary local preview state only; it does not authorize submission or refresh any original B guards. Provider semantics did not change, so the native-provider oracle was not rerun; its prior reported PASS is not new evidence here.

## Exact validation

All commands ran from `/home/user/work/wt/app-m2-selected-server-lifecycle-fix`. Private config mirrors the repository configuration with absolute imports, runner-compatible dirname, private cacheDir, cache disabled, maxWorkers=1 and no file parallelism. Composition 0.0.12 was privately extracted from this worktree's existing tarball; shared dependencies were read-only. To reproduce, first run:

```bash
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-lifecycle-fix/notes/prepare-test-env.py
```

Before the product fix, after promoting the original four tests:

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-lifecycle-fix/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts
```

Exit 1: **4 failed / 10 passed**, exactly the four review counterexamples. `notes/red.log`, 4.16 s. No tests were skipped, weakened or marked expected-to-fail.

Intermediate session check:

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-lifecycle-fix/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

Exit 0: **2 files / 83 tests PASS**, 8.65 s; `notes/session.log`.

Final requested targeted cohort, after all changes:

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-server-lifecycle-fix/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.selectedParams.test.ts --max-warnings 0
git diff --check
```

All exit 0: **8 files / 237 tests PASS** (old 232 + original four + one suffix regression), 24.49 s on the final source; **ESLint zero warnings**, whitespace clean. Logs: `notes/targeted-final.log`, `notes/lint.log`. The same cohort also passed before the final canUndo restriction (24.93 s; `notes/targeted.log`).

The original 4→8/16 refusal, false unacknowledged basis, after-only-ACK, exact original request/key retry, suffix/opaque and mounted projection controls passed without changes to their expectations. Fixtures are synthetic normal-port transport/session tests; the mounted projection control is not a browser or live-provider journey.

## Limits and handoff

No full suite requested or rerun; FULL21209 remains the orchestrator's existing complete result, not a result produced by this worker. No build, project tsc, install, browser, localhost/live socket, shared dependency/cache mutation, git commit/merge/rebase/checkout, push, ref deletion or integration-worktree modification. Private Composition extraction/cache removed after tests; configs, reproduction script and logs retained under this worker's notes. No KEEP marker or queued test.

Next: orchestrator reviews/integrates this bounded correction, then owns the separate paired qualification. Pair/public property UI, actual V1 after V2/removal and Runtime process restart, durable lost-ACK exact retry, inverse/reload and zero-legacy journey all remain OPEN. The current tests do not prove those runtime/browser/custody properties.
