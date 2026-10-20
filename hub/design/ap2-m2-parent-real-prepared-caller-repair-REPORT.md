# ap2-m2-parent-real-prepared-caller-repair

## Result

Fixed the three owned command-facade callers that synchronously read
`commands.addClip(...).ok`:

- `useSwitchToFinalVideo.ts` now awaits the existing sync-or-Promise result
  before interpreting it, and both final-video placement paths await the
  helper.
- `useAddVariantAsGeneration.ts` now awaits its manual prepared-video
  insertion result.
- `AstridTimelineEditor.tsx` now awaits the duplicate-generation insertion
  result.

No command API, DTO, carrier, provider, or native branch changed. The
inherited `legacyClean` fencing of parent-media capture/finish/submit remains
untouched.

## Caller and ingress audit

| Caller | Prepared asset source | Qualified `mediaSelection` possible on this path? | Result |
| --- | --- | --- | --- |
| `useSwitchToFinalVideo.ts` | Locally planned final-video asset, `source: 'registered'` | No; replacement/group fields also stay on the existing guarded path | Awaited result; fallback `applyEdit` behavior unchanged |
| `useAddVariantAsGeneration.ts` | Promoted variant registration plan, `source: 'registered'` | No; `afterClipId` duplicate remains unqualified | Awaited result |
| `AstridTimelineEditor.tsx` | Duplicate-generation registration plan, `source: 'registered'` | No; `afterClipId` duplicate remains unqualified | Awaited result |
| `useAddToVideoEditor.ts` | Popup/lightbox registration plan, `source: 'registered'` | No; left unchanged as the existing popup path | Existing synchronous behavior preserved |

`prepareMediaImport` is async for normal image/video file import and returns a
descriptor carrying `mediaSelection`. `useAssetManagement.prepareGenerationAsset`
forwards that selection, making a qualified prepared asset. The current normal
external-drop path consumes that prepared asset through `dropAsset`/
`handleAssetDrop` and its existing prepared-media `applyEdit` route; it does
not reach the three named command-facade callers. Audio and image imports,
automatic/recovery producers, popup adds, and replacement/group paths were not
migrated into the native qualified branch.

The existing facade contract is intentionally sync-or-Promise: unqualified
`AddClipCommandInput` returns a synchronous `TimelineCommandResult`, while an
asset with `mediaSelection` enters the async verified-media branch. Awaiting
the result handles both contracts without changing the API. The qualified
branch still refuses unsupported inputs before capture and does not fall
through after verification failure.

## Tests

Passed:

```text
VITEST_CACHE_DIR="$PWD/.vitest-cache" node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useAddVariantAsGeneration.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/components/AstridTimelineEditor.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx
  4 files, 102 tests passed

VITEST_CACHE_DIR="$PWD/.vitest-cache" node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useAddVariantAsGeneration.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts
  5 files, 174 tests passed

./node_modules/.bin/tsc --noEmit --pretty false
  passed

./node_modules/.bin/eslint src/tools/video-editor/hooks/useSwitchToFinalVideo.ts src/tools/video-editor/hooks/useAddVariantAsGeneration.ts src/tools/video-editor/hooks/useAddVariantAsGeneration.test.tsx src/tools/video-editor/components/AstridTimelineEditor.tsx --max-warnings 0
  passed

git diff --check
  passed
```

The added regression exercises the real `useAddVariantAsGeneration` manual
ingress with a prepared video and a Promise-returning `addClip` result; the old
synchronous `.ok` read would have reported a failure/toast.

No full suite, browser, localhost, live socket, or central e2e suite was run.

## Decisions, blockers, next steps

- Kept the patch to the three explicitly owned production callers. The popup
  lightbox and external-drop/import producer paths remain on their existing
  unqualified/legacy behavior as required.
- No blockers for this bounded repair.
- The separate Runtime/provider qualification prerequisite noted by the prior
  worker is still outside this task and remains unverified here.
