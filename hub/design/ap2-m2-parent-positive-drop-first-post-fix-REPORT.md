# AP2 M2 parent positive manual-drop first-post fix

## Result

Fixed the first proven positive manual-drop failure in the App producer. The
Runtime import and configured verified-selection read both completed, but the
native parent-media capture stopped before session submission because the
detached video row carried `from`/`to` without the required `hold` span. The
native `clip.add-media` validator requires `hold === to - from`, so this
produced zero native commit POSTs.

The fix adds `hold` only to the detached row sent through the native
`ParentClipAddMediaCapturePort`; the local preview/document row is unchanged.
The original five-field selection, verified read, session/epoch fences,
skeleton cleanup, and refusal-without-fallback behavior remain unchanged. A
regression covers the generated native row and verifies submission is reached.

## Tree/source verification

Base tree: `tl/ap2-m2-parent-valid-selection-refusal-fixture`.

The immutable tree included both the migrated producer (`ec663e205`,
`fix(timeline): route manual video drops through native addClip`) and the
corrected valid-mismatch fixture (`4a67447bb`,
`test(timeline): use valid mismatching media digest`). The prior central run
was therefore diagnostic evidence for the positive path, not a qualification
pass: its negative branch passed, then the positive branch reached the
verified-selection checks and timed out with `wire.posts.length === 0`.

## Validation

- `npx vitest run --config config/testing/vitest.config.ts --no-cache --configLoader=bundle --maxWorkers=2 --no-file-parallelism src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/commands/parentClipAddCapture.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/mediaImport.test.ts` — 5 files, 158 tests passed.
- `npx vitest run --config config/testing/vitest.config.ts --no-cache --configLoader=bundle --maxWorkers=2 --no-file-parallelism src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx` — 3 files, 39 tests passed.
- `npx eslint src/tools/video-editor/hooks/useTimelineCommandsService.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx --max-warnings 0` — passed.
- `npx tsc --noEmit --pretty false --incremental false` — passed.
- `git diff --check` — passed.

No local browser/socket/localhost/full suite was run, and no central test was
requested while the source was dirty.

## Next central command

After the harness commits this clean candidate, run exactly:

```sh
sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-drop-real-central-qualification/run-parent-manual-drop-central.sh run "$PWD"
```

This is the existing mounted manual-drop wrapper and should be the first
central qualification of the repaired positive path. Its result is not yet
verified here.
