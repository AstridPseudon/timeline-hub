# P3 read-only investigation report

## Result

Source verdict: **FAIL — P3 setup oracle does not match the mounted parent producer.**

Live/browser verdict: **UNKNOWN.** The retained P39310 evidence is only the `page.waitForRequest` timeout at `three-products.spec.ts:1540`, before setup/reset/tail. It does not prove zero POST or a historical product-root cause.

## Confirmed producer path

Mounted drag path:

`dragTimelineClip` → `useClipDrag` pointer-up → `commitDraggingSession` → `applyResolvedClipMove`/`applyEdit` with `moveReadBasis` → `scheduleSave` → `localDocumentSave.capture` → `timelineLocalSaveHandoff` → `documentPatchIntent` → durable outbox → `provider.commitTimeline`.

The resulting mounted request is a single guarded `doc.patch`, not semantic `clip.move`:

- `commands[0].op`: `doc.patch`
- `select`: `null`
- `args.changes`: guarded `set` of `parent/clips/id:<clip>/at`, e.g. `0 → 5`
- `label`: `Edit timeline`
- step intent: `Move <clip> on <track>`
- `merge`: `fields`
- request and step `reads`: captured move dependencies
- `source`: `{ via: 'app' }`
- `dry_run`: `false`
- `Idempotency-Key`: durable outbox key
- `created`: current serializer supplies `[]` for this no-allocation patch

Runtime supports both native semantic commands and `doc.patch`; the separate App `ClipMoveCapturePort` is not the selected mounted local-document path.

## Demonstrated defect

P3 setup currently requires `clip.move` in both places:

- [three-products.spec.ts](/home/user/work/wt/ap2-P3-predecessor-whole-path-0705/tests/e2e/local/three-products.spec.ts:1540)
- [gate5-reset-precondition.ts](/home/user/work/wt/ap2-P3-predecessor-whole-path-0705/tests/e2e/local/support/gate5-reset-precondition.ts:52)

The offline control passes only because it manually fabricates a `clip.move` request; it does not validate the installed mounted producer.

The bounded source witness in `useTimelinePersistence.test.tsx` confirms the real producer shape: `doc.patch`, guarded `at` change, move reads, and move step metadata.

There is also a separate static inconsistency worth verifying later: the unchanged downstream P3 assertion at `three-products.spec.ts:1640` omits `created`, while the current full-v2 serializer includes `created: []`. I did not alter that protected tail.

## Tests and checks

- `npm exec vitest -- --run --no-cache --config config/testing/vitest.config.ts ...documentPatchIntent.test.ts ...localSaveSession.v2.test.ts`  
  **2 files passed, 27 tests passed.**
- `npm exec vitest -- --run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelinePersistence.test.tsx -t "genuine causal move|move"`  
  **1 file passed, 5 tests passed, 96 skipped.**
- `node --import tsx --test tests/e2e/local/support/gate5-reset-precondition.test.mjs`  
  **1 subtest passed.**
- `git diff --check`  
  **Passed.**
- Worktree remained clean at `66354161950d1e747965c095ea97b881d2592708`.

No browser, backend, socket, HTTP, full suite, or live request was run.

## Recommendation

Route to the App shape owner: update only the P3 setup observer/helper to require the authentic single `doc.patch` move shape and its exact guards/reads/receipt/head/readback/outbox checks. Do not accept either operation generically, weaken the gate, or change the protected reset/tail.