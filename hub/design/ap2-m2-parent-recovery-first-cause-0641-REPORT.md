# AP2-M2 parent recovery first-cause report

## Result

No App source correction was made. The first real failure is a shared native
parent-ADD seam, outside the permitted `useAssetManagement` /
`external-drop-utils` ownership for this task.

The exact 0629 actual was:

- Test: `ap2-m2-parent-final-body-approved-one-case-0629-ap2-m2-parent-pin-final-acb-explicit-0617-actual-1021062952-11497`
- App source: `acb582c2c3b08481d43853b8526894ac60d074bc`
- App tree: `141724b56736be40a269f60aa8bfc060914ebd29`
- First failure: `tests/e2e/local/three-products.spec.ts:1557`, recovery `attempts: 0` instead of `1` after 90 seconds.
- The exact wrong-selection 404 body, normal import 201, selection 200, and verified selection 200 all passed. No ADD request or commit request was emitted.

## First missing effect

The first missing effect is `port.finish`, before `port.submit` and before the
outbox can create/send an attempt:

1. `useTimelineCommandsService.ts:474-537` reaches the native prepared-video
   branch and awaits `getProjectVerifiedMedia` at line 537. The retained
   network trace proves this valid verified read returned 200.
2. `applyPreparedMediaCommand` materializes the video row through
   `timeline-asset-plans.ts:397-405`: it has `from: 0`, `to: duration`, and
   `speed: 1`, but no `hold`.
3. `rowsToConfig` preserves that source-window shape at
   `timeline-data.ts:367-377`; it does not add `hold`.
4. `commitSession.ts:411` calls `captureParentClipAddMedia`. Its direct parent
   path invokes `executeParentClipAddMedia` without the after-anchor/raw-window
   mode. The shared validator at
   `commands/parentClipAddCapture.ts:319-320` therefore requires a positive
   `row.hold`; the generated video row has none and `finish()` throws.
5. The exception is caught and converted to a refused result at
   `useTimelineCommandsService.ts:541-542`. Consequently `port.submit()` at
   line 539 is never reached, so no outbox owner/attempt or commit POST exists.

This also explains why the browser observer sees `attempts: 0`: it is an
observer of the later outbox effect, not the cause. The trace contains no
console error because the App command path catches the exception.

## Ruled-out causes

- Refusal preservation is not the first cause: the wrong selection returned
  the required exact 404 body and the timeline remained unchanged.
- The current draft/epoch and Runtime port are available: the valid path got
  through import, selection, and verified-media transport. The mounted
  assembly at `useTimelineState.ts:940-968` binds the verified Runtime method
  and passes `parentMediaCommands` into asset management.
- The prior forwarding fix is present; this is not a missing `forwarding968`
  diagnosis. The valid verified request could not occur without that mounted
  runtime/port path.
- The upload-skeleton handoff is also not the observed first failure. The
  current row-local guard at `useAssetManagement.ts:300-309` removes
  `removeClipId` only for a proven transient placeholder and preserves an
  authored replacement refusal. If the skeleton ID were still forwarded, the
  native service would refuse at `useTimelineCommandsService.ts:481-483`,
  before the verified read; the retained 200 verified read proves that is not
  the 0629 stop.

## Exact HOME shared-seam request

Please apply and test the smallest shared correction at
`src/tools/video-editor/hooks/useTimelineCommandsService.ts:534`, immediately
after cloning the generated row and before `port.capture`:

```ts
const row = structuredClone(clip) as unknown as Record<string, JSON>;
if (row.clipType === 'media' && row.hold === undefined
  && typeof row.from === 'number' && typeof row.to === 'number') {
  row.hold = row.to - row.from;
}
```

This supplies the existing Agent birth-schema carrier required by
`parentClipAddCapture.ts` while retaining the existing `from`/`to`/`speed`
values and adding no store, DTO, authority, or new writer. The direct native
ADD regression should assert that the generated video row reaches `finish`
and the durable outbox with `hold === to - from`; all existing positive ADD,
order, opaque, reload, ACK/retry, undo, zero-legacy, and exact-404 assertions
must remain unchanged.

No source/test files were changed in this App worker because the owning hunk
is a shared command seam and the task explicitly forbids editing that seam.

## Validation

Targeted direct command:

```sh
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/parentClipAddCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx \
  src/tools/video-editor/hooks/useExternalDrop.test.tsx
```

Result: **5 files passed, 136 tests passed**. The first attempted equivalent
with `--configLoader=runner` failed during config startup because this repo's
config uses `__dirname`; it did not execute tests. No browser, central actual,
second executor, install, full suite, timeout change, or actual rerun was
performed.

The App worktree remains clean at source/tree
`acb582c2c3b08481d43853b8526894ac60d074bc` /
`141724b56736be40a269f60aa8bfc060914ebd29`; the harness should therefore
record the same source/tree after its no-op commit handling.

## Live callers

The relevant live chain is unchanged:

`onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts ->
useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip ->
commitSession parentClipAddMediaPort -> existing outbox`.

Recommended next step: HOME applies the shared row-carrier hunk, adds the
direct regression at the shared command boundary, runs its direct neighboring
tests, and obtains a new qualified actual before any recovery/ADD claims.
