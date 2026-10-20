# ap2-m2-selected-mounted-production-join

## Result

Completed the App mounted selected-PARAM production join.

- Added the existing `ClipParamsCapturePort` as an optional `selectedParam` field on `ClipPanelProps`.
- Forwarded `useTimelineEditorOps().selectedParam` from `PropertiesPanel` through the real `ClipPanel` boundary into `AstridElementParams`.
- Made `AstridElementParams` prefer the explicit mounted prop, with its existing timeline-store fallback preserved for direct consumers and legacy-safe paths.
- Did not change the AppProvider final join because the current Provider assembly already forwards `editor.selectedParam` into the mounted editor ops.
- Added mounted coverage using the production `useTimelineSave`/command-session path. Retained document/object reads are mocked only on `provider.paramReadClient`; the selected capture port is real.
- Preserved the literal/unqualified PARAM path and the existing legacy `onChange` fallback for non-selected cases.

## Normal production path inspected

`RuntimeDataProvider.paramReadClient` → `useTimelineSave` → `useTimelineCommandSession` (selected authority port plus native `clipParamsPort`) → `useTimelineState` editor ops → `VideoEditorRuntimeContent` Provider join → `TimelineStoreProvider` → `PropertiesPanel` → `ClipPanel` → `AstridElementParams`.

The mounted test proves the final hook/store/inspector portion. The source inspection confirmed the upstream command-session, state, Chrome/Provider, and retained-read forwarding already present on this branch.

## Verification

- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx` — 3 files, 53 tests passed.
- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx` — 2 files, 15 tests passed.
- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx` — 1 file, 2 tests passed after the final assertion update.
- `./node_modules/.bin/eslint src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx --max-warnings 0` — passed.
- `./node_modules/.bin/tsc -p tsconfig.json --noEmit --pretty false` — passed.
- `git diff --check` — passed.

Mounted assertions cover one accepted native `clip.set-params` request, exact original P1/schema source and retained document/object reads, one native intent with no legacy `onChange`, and refusal/draft preservation when the async retained read completes after session teardown.

## Holds / limits

No full suite, browser, localhost, socket, or live-runtime run was requested or performed. The actual browser pending-owner join remains a separate owner’s work; this report makes no claim for it.
