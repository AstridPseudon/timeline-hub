# App2 M2 live producer ownership negatives

## Result

Added focused ownership-safety coverage for the active transcript-lane and
Scene Phase Markers producers. Transcript regeneration now removes and updates
only clips whose existing `managed`/`managedBy` metadata identifies the active
extension. Scene Phase Markers alignment now updates only clips owned by that
extension; generated Scene clips also retain the existing `app.managedBy`
metadata on creation so later alignment can recognize them. Foreign-owned and
user-authored clips receive no remove, move, or update operation.

Removed only the approved stale compiler-canary entries from
`eslint.strict-debt.js` and `docs/cutover-inventory.md`; no other debt entries
or thresholds changed.

## RED / GREEN

The new negatives were run against the pre-fix producer code before restoring
the ownership guards. RED: 2 tests failed as expected:

- transcript regeneration emitted `clip.update` for a non-owned deterministic
  caption ID;
- Scene Phase alignment emitted move/update pairs for both a foreign-owned and
  user-authored clip.

After the fix, the same producer lanes were GREEN.

## Tests

Passed, 8 files / 492 tests. Exact command:

    TMPDIR="$PWD/.tmp-test" node --require /tmp/ap2-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/dev/transcript-lane/__tests__/fixtureProvider.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/lib/timeline-reader.test.ts src/tools/video-editor/lib/managed-object-guard.test.ts

Targeted ESLint passed. Exact command:

    node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 src/tools/video-editor/dev/transcript-lane/extension.ts src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/dev/transcript-lane/__tests__/fixtureProvider.test.ts src/tools/video-editor/dev/scene-phase-markers/extension.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx eslint.strict-debt.js

`git diff --check` passed.

No full, browser, socket, or localhost suite was run locally.

## Changed exports and live callers

No new export or public shape was added. Existing exported builders changed:

- `buildTranscriptCaptionPatch` is called by `renderTranscriptAsCaptions` in
  `transcript-lane/extension.ts:769`, the live transcript action path.
- `buildCreateShotsPatch` and `buildCreateEmptyShotsPatch` are called by
  `createShotsFromMarkers` in `scene-phase-markers/extension.ts:799-800`.
- `buildAlignShotsPatch` is called by `moveExistingShotsToMarkers` at
  `extension.ts:854`.
- `moveExistingShotsToMarkers` is called by the panel at
  `ScenePhaseMarkersPanel.tsx:155` and by the unified action at
  `extension.ts:888`.

## Normal path and route proof

The normal accepted Scene generated-clip path now adds only the existing
`app.managedBy` ownership metadata; no new DTO, store, writer, or public shape
was introduced. Owned clip timing/update behavior is otherwise unchanged.
Foreign-owned and user-authored clips produce no accepted mutation.

Before merging this data-loss fix, run the normal `/tools/video-editor` route
with a real transcript regenerate and Scene Phase alignment request containing
one foreign-owned and one user-authored clip. Capture the generic
command/session request, confirm the committed command contains no operation
targeting either protected clip, then reload/read the raw accepted timeline and
assert both clips' complete authored values are unchanged. Repeat through the
normal retry/reload path; no legacy writer or direct test-only provider may be
substituted. This browser/Runtime proof was not run in this worker.
