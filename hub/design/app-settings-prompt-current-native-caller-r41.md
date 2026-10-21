# App M2 prompt native-caller migration (r41)

## Result

Migrated the exact `useVideoTravelSettingsHandlers.ts:149-151` prompt callback. For the canonical placed-shot path, the callback now sends `{ prompt }` to the existing settings-intent/capture path before updating the visible draft. Successful native capture uses the existing `shot.set` session/outbox flow; capture refusal or missing native authority keeps the draft visible and surfaces the refusal instead of falling back to a snapshot.

The production change is limited to the handler, the necessary provider callback plumbing, and the existing `ShotEditorView` native settings branch. Gallery/name fields, Provider/session core, graph creation, and unrelated prompt writers were not changed.

## Schema and capture verification

The published Runtime 0.2.14 schema at source commit `95bd3c5f` admits `settings.prompt` as `string | null`; `settings.prompt` is also a valid clear path. Clear removes property presence, while unmentioned settings survive. The App `shot.set` capture already validates and records this scalar with raw presence/value semantics, preserving raw siblings and opaque fields. Direct capture tests now cover prompt string, explicit null, and clear/presence behavior.

## Live callers and cut scope

- Migrated caller: the BatchSettingsForm prompt callback routed through `usePromptSettings.setPrompt` and the canonical ShotEditorView settings-intent path.
- Still outside this one-family cut: LoRA trigger-word prompt edits in `VideoTravelSettingsProvider`, travel-between-images modal prompt edits, and compound pair prompts. These remain existing direct writers and were not broadened into this migration.
- The native prompt branch is activated only after prompt capture succeeds or an explicit native refusal is recorded. This preserves existing uncaptured legacy test/setup behavior and avoids an accidental broader settings rewrite.

## Tests

Passed:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/travel-between-images/hooks/settings/useVideoTravelSettingsHandlers.test.ts src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/video-editor/commands/shotSetCapture.test.ts src/tools/video-editor/commands/shotSetSession.test.ts src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx
5 files, 46 tests passed

./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/travel-between-images/hooks/settings/useVideoTravelSettingsHandlers.ts src/tools/travel-between-images/hooks/settings/useVideoTravelSettingsHandlers.test.ts src/tools/travel-between-images/providers/VideoTravelSettingsProvider.tsx src/tools/travel-between-images/pages/ShotEditorView.tsx src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/video-editor/commands/shotSetCapture.test.ts
passed

git diff --check
passed
```

No full suite, browser/live-socket suite, build, install, or typecheck was run per task scope. Accepted/reload durability is not claimed; the independent data-safety review remains pending.
