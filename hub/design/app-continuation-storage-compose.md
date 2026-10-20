# Inactive App continuation storage composition

Completed 2026-10-20 in `/home/user/work/wt/app-m2-continuation-storage-compose`, branch `tl/app-m2-continuation-storage-compose`, base `6b22b03c3` (fixed-type public12 source). KEEP retained. No plan decision changed. This is a bounded source composition, not current-pair qualification or a whole-tree merge.

## Changes and decisions

Composed only the requested parts: D13 `c195d1ee1`, placement storage `f89cc8d`, requester consumer `07f64b46f`, native bootstrap `f0112b846` with completion correction `3a1d9c852`, and post-ACK-loss scheduling fix `5fe884946`. Existing base history/label safety remains. The bootstrap capture/adapter and placement requester are inactive exports with no production ingress added. No package/lock, generated client, Runtime wire, root pin, UI writer, server or other feature cohort changed.

All ACK operations share the existing strict `astrid.command-outbox` / `owners` transaction, browser lock and generation fence. Acceptance retains creation-phase defaults/request as before; original init intent/request/result/head; every requested render acceptance and its admission/locator; linked placement acceptance; and dependent `readyBase`. It then prunes only the accepted prefix. Rejection propagation, exact in-flight replay, owner discovery and existing cancellation fences remain.

Initialization tags route adapter data only. Completion still validates the exact saved request and scoped receipt/result, finds the original publication through normal paginated commit history, reads its immutable parent closure, and separately loads today's display basis. Later edits, equal-byte inverse/restore publications and rolling `accepted` cannot replace that original proof. Missing older checkpoints remain visible and refuse completion. The original history/immutable mismatch counterexamples are unchanged.

Two small composition decisions close interactions between these existing features:

- Ordinary command-session discovery/claim checks local editor payload shape and canonical pending commit route. Creation/init, task-only, render-only and accepted-only owners remain in authenticated storage discovery for their explicit requester; they are not sent to the ordinary commit callback. Older ordinary editor records need no new discriminator. These checks select a recovery consumer and confer no acceptance authority.
- Explicit disposition of a rejected placement chain cancels its old linkage atomically, preserving it without recapture. Otherwise the inherited resolution method would remove the intent while leaving its requester permanently queued. A single cancellation helper serves leaf cancellation and rejected-chain disposition, including rollback.

Exact copied definitions and shared test bodies were included once. `newIntent`, finite-JSON copying, request identity comparison, scope discovery and storage transactions remain single implementations. No additional store, journal, coordinator, timer or workflow abstraction was added.

## Evidence

Final focused command, from the assigned worktree:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/runner-paths.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/createDefaultTimeline.test.ts --maxWorkers=1 --no-file-parallelism
```

**PASS: 7 files / 339 tests, exit 0, 15.86s.** [Final log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/final-targeted.log). Physical dependency target: `/tmp/app-coherent-deps12/node_modules`, installed Composition `0.0.12`. The cache-free runner needs the notes-only preload because the repository config uses `__dirname`; both affected config modules resolve the same `../../` project root. The original config and dependency packages were not edited to enable it.

All **331 inherited tests** passed before the eight new cases. New coverage: one combined create/init/render/placement-A/lost-ACK/B/C/inverse/reopen case; five owner-routing classifications; a saved task-route control with an older editor payload; and rejected-placement disposition with abort rollback/no rearming. Cross-feature tests use real outbox transactions and the existing synthetic authority fixtures. Ordinary native capture/replay controls use the existing HTTP fixture; placement command payloads and later A/B/C/inverse acceptances are opaque storage fixtures. No real semantic acceptance is implied.

```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/commitOutbox.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts src/tools/video-editor/commands/placementRequester.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/commands/bootstrapCapture.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/integrations/runtime/bootstrapInitialization.ts src/integrations/runtime/bootstrapInitialization.test.ts
node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/audit.cjs
git diff --check
```

**All PASS, exit 0.** [Lint log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/lint.log), [audit output](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/audit.log), [audit data](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/audit.json). Parsing original test statements verifies all original bodies in the **67 / 79 / 129 / 181 / core118** cohorts remain byte-identical substrings: 14 source-file comparisons, 315 statements across overlapping cohorts. Thirteen whole-file checks preserve bootstrap golden/capture fixtures, clip capture tests, requester tests/source, corrected bootstrap adapter, original create-default implementation/tests and package/lock. The session environment receives only the original ACK-loss fixture delta, retaining newer base label/transport behavior. No tests were skipped, marked failing, deleted or weakened.

Earlier runs of the same seven-file command with the default loader and without `--no-cache` passed **331/331** (21.70s, inherited composition) and **339/339** (15.66s, completed cases). Logs: [originals](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/composed-originals.log), [completed default-loader run](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/targeted.log). One subsequent runner invocation without the preload failed config loading with `ReferenceError: __dirname is not defined`; zero tests ran. The final invocation above resolved that configuration issue. An initial audit invocation hit a sandbox `spawnSync` wrapper error despite child exit 0; the audit now reads the successful child status/output and passes.

## Size and lifecycle debt

| Product path | Base lines | Composed lines | Net |
| --- | ---: | ---: | ---: |
| `commands/commitOutbox.ts` | 327 | 580 | +253 |
| `commands/commitSession.ts` | 504 | 521 | +17 |
| `runtime/bootstrapInitialization.ts` | 0 | 196 | +196 |
| `commands/bootstrapCapture.ts` | 0 | 52 | +52 |
| `commands/placementRequester.ts` | 0 | 267 | +267 |
| **Product total** | **831** | **1,616** | **+785** |

Task delta: **13 files, +2,985/-22** including eight test/helper/golden files (net +2,178 non-product lines). [Exact source patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/source.patch) includes new files; [audit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/audit.json) records hashes and byte sizes. Counts are physical authored source lines in these changed product paths, excluding tests/helpers/fixtures and untouched main infrastructure; this is not a whole-project census.

Lifecycle debt remains explicit: owners, historical init links and render/placement continuation arrays have no bounded retirement policy; failed/cancelled/accepted links are retained indefinitely. Original creation-phase data rolls with `accepted` until init, as on its source branch; no second historical creation journal was invented. Schema remains version 1 with additive optional data; old owners cannot have missing authoritative init inputs guessed. Recovery needs explicit authenticated requester calls; there is no production reconnect wakeup or concrete automatic semantic capture here. Large existing session/outbox modules remain; this composition introduces no new lifecycle manager to hide that debt.

## Shared dependency write incident

The first two default Vitest invocations used Vite's default cache paths. They updated `/tmp/app-coherent-deps12/node_modules/.vite/vitest/da39a3ee5e6b4b0d3255bfef95601890afd80709/results.json` and created/deleted transient config modules under `.vite-temp`. **This violated the read-only shared-dependency rule.** No installed package/symlink was deliberately changed, and no shared files were removed or repaired afterward. The final cache-free runner left both observed paths' metadata unchanged (results file: `2026-10-20 08:24:12.787540165 UTC`; `.vite-temp`: `08:23:56.939539222 UTC`). This is a limited cache-path check, not a complete before/after dependency-tree attestation. The orchestrator should account for this incident when judging overlapping qualification; no claim of a wholly untouched dependency directory is made.

## Limits and next steps

No install, full suite, app build, tsc, browser, socket/server, native Python parity rerun, live Door admission or current Runtime/Agent pair proof was run/requested. Native browser IndexedDB/locks, real process restart/fsync, normal render authorization, automatic placement semantics/attempt fencing, zero legacy production traffic and current-pair qualification remain unverified. No git commit/merge/rebase/checkout/push or ref mutation was performed. No build/temp output remains in the worktree; the ignored dependency link selects the required physical directory.

No source blocker. Review/land this bounded composition through the harness, review the cache-write incident, then separately qualify the official supported tuple and production requester ingress before activating or deleting any writer. Lifecycle retirement requires its own bounded design; it was not added here.

Artifacts: [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes/report.md), [notes directory](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/notes), [commit message](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/commit-msg), [DONE](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/DONE), [KEEP](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-continuation-storage-compose/KEEP).
