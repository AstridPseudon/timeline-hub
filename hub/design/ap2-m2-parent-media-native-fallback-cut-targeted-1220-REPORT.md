# Parent prepared-media fallback cut

## Result

Cut the remaining simple prepared-video parent ADD fallback at the mounted
`createTimelineCommands().addClip()` boundary. An unqualified prepared video
now returns a visible `mutation_failed` refusal naming the missing original
Runtime media selection before `applyEdit`; the existing draft object remains
unchanged. A native-qualified prepared video still uses the existing
row-local preview, exact five-field selection, verified-media await, session
fences, and parent `clip.add-media` submit path.

## Exact physical scope and family boundary

- Changed live caller: `src/tools/video-editor/hooks/useTimelineCommandsService.ts`
  (`addClip`, immediately after the native-selection branch at lines 555-571).
  The simple prepared-video shape with no `mediaSelection`, no duplicate
  anchor, generated clip ID, replacement/removal list, or pinned-group
  override is no longer admitted to the local `place-prepared-media` writer.
- Added direct regression coverage in
  `src/tools/video-editor/contexts/VideoEditorProvider.test.tsx`: the refusal
  is structured, `applyEdit` is not called, and the selected timeline draft
  remains the same object.
- No `useTimelineState`, shared session/state/provider, popup occurrence/SWAP,
  movement, scalar gesture, route, pin, DTO, or public API files changed.
- The broad `place-prepared-media` descriptor and its row helpers were not
  deleted: image prepared placement and the real Main-only duplicate-after-clip
  and final-video replacement callers still use them without the native media
  carrier/op. Their positives are preserved deliberately. `useAssetManagement`
  already routes qualified video drops natively and refuses missing selection;
  no extra hunk was needed there or in `useExternalDrop`.

Independent source review basis: the reviewed parent native capture repair
(`app2-parent-media-native-repair`) approved the native row/registry mirror,
opaque-data, detached-selection, and retry behavior. This worker reviewed the
two-file diff and the remaining prepared-video callers against that boundary.

## Verification

All commands ran in this worktree with Vitest cache disabled and one worker:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useAddVariantAsGeneration.test.tsx
PASS — 4 files, 90 tests

node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/hooks/useTimelineCommandsService.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx
PASS

flock /home/user/work/.app-tsc.lock node_modules/.bin/tsc --noEmit --pretty false --incremental false
PASS — exit 0

git diff --check
PASS
```

Not run: browser/full/localhost/live-socket suites, as prohibited by the
interim rule and reserved checkpoint ownership. No dependency install or
shared-install mutation was performed.

## Commit handoff

The harness should commit the worktree with the message in the worker
`commit-msg` path. No blocker remains.
