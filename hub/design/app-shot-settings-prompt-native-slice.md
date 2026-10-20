# App D01 shot settings prompt native slice

## Scope

This slice migrates only the placed-shot `settings.prompt` writer in the embedded
Shot Editor. The existing shot name path and all other settings writers remain
unchanged.

The UI ingress is:

`BatchSettingsForm` → `handleBatchVideoPromptChangeWithClear` →
`usePromptSettings().setPrompt` → `handleBatchVideoPromptChange` →
`updateField('prompt', value)`.

## Implementation

- Prompt intent is captured before the settings draft changes.
- The existing occurrence-owned `ShotSetCapturePort` captures the original raw
  prompt value and explicit `occurrence:{id}/shot` owner.
- Prompt-only saves finish and submit the existing `shot.set` command with
  `{ values: { settings: { prompt } }, clear: [] }` through the existing command
  session and durable outbox.
- The captured carrier is cleared after accepted completion. Submission errors,
  conflicts, and stale-session refusals leave the carrier and the settings draft
  intact for the existing recovery/error UI.
- An explicit empty-string intent is submitted even when normalization makes the
  displayed form look unchanged over an absent or null raw settings root.
- Prompt plus another settings change is refused with the existing kept-draft
  error path. Other unsupported/complex settings continue on their existing
  path.
- No new operation, DTO, store, public API, UI control, normalization serializer,
  default materialization, or owner inference was added.

## Evidence

Targeted command:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/shotSetCapture.test.ts \
  src/tools/video-editor/commands/shotSetSession.test.ts \
  src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx \
  src/tools/travel-between-images/pages/ShotEditorView.test.tsx \
  src/tools/travel-between-images/components/ShotEditor/controllers/useGenerationController.test.tsx
```

Result: 5 files, 44 tests passed.

```sh
git diff --check
./node_modules/.bin/eslint \
  src/tools/video-editor/commands/shotSetGesture.ts \
  src/tools/video-editor/commands/shotSetSession.test.ts \
  src/tools/video-editor/commands/commitSession.ts \
  src/tools/travel-between-images/hooks/settings/useVideoTravelSettingsHandlers.ts \
  src/tools/travel-between-images/providers/VideoTravelSettingsProvider.tsx \
  src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx \
  src/tools/travel-between-images/pages/ShotEditorView.tsx \
  src/tools/travel-between-images/pages/ShotEditorView.test.tsx
```

Both passed with no output.

## Limits and next step

No full suite, browser/localhost gate, build, project TypeScript check, install,
or shared-cache write was run. The existing native full-record shot-set tests
and local command-session/outbox tests pass; actual Runtime-door/browser
acceptance remains the next integration gate after this source is committed.
