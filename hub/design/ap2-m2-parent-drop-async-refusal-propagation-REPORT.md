# Async external-drop refusal propagation

## What changed

- Awaited every existing `dropAsset` call in `external-drop-utils.ts`, preserving skeleton removal on native `false` and rejected placement promises.
- Made multi-generation, single-generation, and general asset helpers async and propagated the awaited boolean. Multi-generation drops stop before advancing time/track state when a placement refuses.
- Awaited those helper results in `useExternalDrop.ts` and only seek after an accepted dispatch.
- Added focused refusal/rejection and no-seek coverage while retaining the existing positive multi-drop and file/import assertions.
- Did not edit the shared caller/type seam or any parallel-owned files.

## Checks

- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx` — 21 passed.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/lib/timeline-asset-plans.test.ts` — 4 files, 38 tests passed.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/hooks/useExternalDrop.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/lib/external-drop-utils.ts` — passed.
- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `git diff --check` — passed.

No browser, socket, request-test, or full suite was run, per task scope.
