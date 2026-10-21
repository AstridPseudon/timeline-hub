# AP2-M2 parent file acceptance result repair

## Result

Fixed the remaining file-drop acceptance seam on `tl/ap2-m2-parent-current-repaired-consumer-join`.

`handleFileDrop` now waits for every asynchronously started file placement and returns `true` only when at least one file was actually accepted. Existing skeleton creation, concurrent per-file upload start, `pendingOpsRef` decrement, and refusal/rejection cleanup remain in place. Partial acceptance is explicit: any accepted file permits the outer seek; an all-refused or immediate-refusal drop does not.

Native `false` and rejected placement results remove their skeletons and settle the pending counter before the caller can seek. Unsupported and oversized early refusals create no skeleton/pending operation and return no acceptance. The existing native hook selection, toast, and intent behavior is unchanged.

## Exact remaining-hunk delta

- `src/tools/video-editor/lib/external-drop-utils.ts`: added one local accepted flag and one local `Promise<boolean>` collection; marked the already-awaited direct prepared placement accepted; converted the existing image/video/generic skeleton IIFE to a collected `Promise<boolean>`; returned `acceptedFile || placedFiles.some(Boolean)` after `Promise.all`; returned `false` from failure branches.
- `src/tools/video-editor/hooks/useExternalDrop.test.tsx`: kept the concurrent two-file positive/refusal test alive while awaiting its returned drop promise; asserted partial acceptance seeks; added native-false/rejection file-path no-seek and skeleton-cleanup coverage; asserted the existing unsupported early refusal does not seek.
- No DTO, store, framework, provider, HOME, or shared construction changes.

## Changed exports and live callers

- `handleFileDrop` remains exported from `src/tools/video-editor/lib/external-drop-utils.ts:275`; its only runtime caller (tests excluded by grep) is `dispatchTimelineDrop` in `src/tools/video-editor/hooks/useExternalDrop.ts:115`.
- `useExternalDrop` remains exported from `src/tools/video-editor/hooks/useExternalDrop.ts:482`; its runtime caller is `src/tools/video-editor/hooks/useTimelineState.ts:968`. `useTimelineState.types.ts:75` consumes its return type only.

## Activation and runtime support

The repaired behavior is active in the normal timeline path: `useTimelineState` mounts `useExternalDrop`, whose `onTimelineDrop` awaits `dispatchTimelineDrop`; the seek callback runs only after that dispatch returns accepted. Runtime image/video imports continue through the existing provider capability path (`prepareMediaImport`), while providers without that capability retain the existing generation-upload skeleton path. The fix changes only settlement/acceptance propagation, so it does not claim support for a provider that previously refused the operation.

## Checks

- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx` — 23 tests passed.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/lib/timeline-asset-plans.test.ts` — 4 files, 45 tests passed.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/hooks/useExternalDrop.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/lib/external-drop-utils.ts` — passed.
- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `git diff --check` — passed.

No browser, socket, request-test, or full suite was run, per task scope.
