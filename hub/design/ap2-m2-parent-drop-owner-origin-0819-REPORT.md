# AP2 M2 original parent ADD owner-origin report

## Result

The original ADD fixture already targets a normal parent-owned element. No
fixture correction is appropriate. The retained DOM resolves both
`f2-app-clip` and `f2-transition-clip` to `data-row-id="V1"`; the helper's
drop point is the center of `f2-app-clip` (`clientX=797`,
`clientY=499.609375`). The spec also requires the resulting row to be `V1`
(`tests/e2e/local/three-products.spec.ts:1440-1600`), while the occurrence is
separately declared on `S1` in the same existing seed.

The minimal App2 source correction is applied in this worktree:

- `src/tools/video-editor/lib/drop-position.ts` now derives planner rows in
  rendered `tracks` order, matching the published geometry's
  `mediaRowIndex`. It retains each row's actions by ID and creates an empty
  row only for a track with no current row.
- `src/tools/video-editor/lib/drop-position.test.ts` adds a regression that
  reverses the mutable rows while retaining rendered `v/a` track geometry and
  proves the hit owner stays `v`.

Patch hash (uncommitted `git diff --binary`):
`8e54d4d5277de6a2c556582c33277a9216431180a43e6301af6375fdc0c4f9ef`.

## Exact owner-origin path

The first refusal was the retained actual31285 result: `row.track='S1'`,
message `track is the lane of an occurrence-owned shot`, and `attempts=0`.
That is the intentional native fence in
`src/tools/video-editor/commands/parentClipAddCapture.ts:379-385`; it ran
before any commit/outbox POST and was not changed.

The upstream App path is:

`useExternalDrop.ts:onTimelineDrop:621-655` →
`external-drop-utils.ts:handleFileDrop:343-356, 512-525` →
`useAssetManagement.ts:303-317` → existing `commands.addClip` →
`parentClipAddCapture.ts:379-385`.

Before this patch, `computeDropPosition` used the rendered geometry's media
row index but passed `dataRef.current.rows` unchanged to
`planClipDrag`. `resolveRequestedTarget` in
`src/tools/video-editor/lib/clip-drag-planner.ts:230-247` preferred
`rows[clampedRowIndex].id`, then found that ID in `tracks`. Thus a stale or
reordered mutable row snapshot could turn a visual hit on rendered `V1` into
`targetTrackId='S1'`. `handleFileDrop` copied that derived ID into the upload
skeleton (`external-drop-utils.ts:453-457`) and the prepared native drop
(`:512-525`); the event itself did not carry authoritative ownership.

The correction keeps the planner's row actions aligned to the same track
order used by `TimelineCanvas`/`buildTimelineRowLayout`, so the row-local
owner is derived from the hit geometry. It does not infer authority from a
label, select a parent in the backend, relax the S1 fence, add a fallback
writer, or alter retry/actual behavior. Existing occurrence-lane refusal
controls remain intact.

The retained trace does not serialize the internal `DropPosition` or planner
inputs, so it cannot prove the exact transient row snapshot for that browser
invocation. It does prove the hit was V1 and the first native refusal was S1.
The new direct regression covers the source mismatch that can produce that
observed owner origin without claiming unverified browser success.

## Transported prerequisite report

The completed parent0812 report was recovered from its harness log after its
accidental worktree no longer existed and transported to:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent31285-no-post-first-cause-0812-REPORT.md`

The source payload and destination are byte-identical: 6,528 bytes, SHA-256
`ce184124b3c8321c51891b1733820a9fcd69e8d633c68333b37b96e9fe77870c`.
No accidental `ORCH/` directory or prior report was copied into App.

## Verification

Passed directly:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs \
  node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/drop-position.test.ts \
  src/tools/video-editor/lib/clip-drag-planner.test.ts
  2 files, 39 tests passed

node_modules/.bin/eslint --no-cache --max-warnings 0 \
  src/tools/video-editor/lib/drop-position.ts \
  src/tools/video-editor/lib/drop-position.test.ts
  passed

git diff --check
  passed
```

No browser, build, daemon, socket, install, actual/retry, full suite, or test
service request was run. The mounted positive/recovery/undo/opaque/legacy
journey remains unverified here by instruction.
