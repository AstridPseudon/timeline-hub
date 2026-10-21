# Local upload skeleton/native handoff repair

## What changed

- Added one existing-lifecycle predicate in `lib/external-drop-utils.ts` that recognizes a local upload placeholder only when its `uploading-*` ID, `uploading:` asset marker, live row, and absence from authored config/order all agree.
- `useAssetManagement.ts` now strips `removeClipId` only for that proven transient placeholder before calling native prepared-video `addClip`.
- External-drop cleanup now runs after either accepted or refused placement, but only deletes the still-proven transient placeholder. Upload failure/cancel cleanup remains intact; a changed, missing, or authored row is left alone.
- Added a positive native handoff regression and a negative authored-row replacement regression. The latter still forwards `removeClipId`, preserves the row, and surfaces the native refusal.

## Live callers changed

- `src/tools/video-editor/lib/external-drop-utils.ts:handleFileDrop` — image/video/generic prepared file-drop cleanup seam; video calls carry the skeleton ID through the existing `dropAsset` argument.
- `src/tools/video-editor/hooks/useAssetManagement.ts:placePreparedAsset` — shared prepared-video native `commands.addClip` caller.

Other prepared-asset callers (`useSwitchToFinalVideo.ts`, `useAddVariantAsGeneration.ts`, and `AstridTimelineEditor.tsx`) were not changed: they use genuine `afterClipId`/replacement semantics and must retain native refusal behavior.

## Data-safety implication

The normal external upload path no longer presents a non-persisted placeholder as an accepted replacement to native ADD. On successful native ADD, the local placeholder is removed only if its transient marker is still present. On upload/native failure, the existing cleanup removes only that same placeholder. A genuine authored replacement ID, including one that resembles an upload ID but has authored metadata/config/order, is still sent as `removeClipId`; native refusal remains visible and no authored row is silently deleted.

The native service, provider/session, selection/epoch fences, retry behavior, wrong-selection404 path, and persistence/DTO surfaces were not edited.

## Tests

Passed:

```text
TMPDIR="$PWD/.tmp-ap2-m2-parent-local-skeleton" node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx
Test Files  3 passed (3)
Tests       44 passed (44)

node_modules/.bin/eslint src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/lib/external-drop-utils.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useExternalDrop.test.tsx --max-warnings 0
passed

node_modules/.bin/tsc --noEmit --pretty false --project tsconfig.json
passed

git diff --check
passed
```

Not run by instruction: browser, localhost/live-socket, central actual/full, or pin/bootstrap qualification. Independent review and the newly authorized original mounted ADD journey remain next steps.

## Decisions/blockers

No blocking issue. The top-level orchestrator `STATUS.md`/`INBOX.md` paths named in the brief were absent; the current App status and the supplied ADD diagnosis report were read instead. No decision was changed from PLAN.
