# ap2-m2-parent-manual-drop-native-producer

## Result

The actual manual prepared-video file-drop producer now uses the existing qualified `addClip` command door when the prepared asset carries the original Runtime `MediaSelection`. The native call receives a normal add (`time` and optional `trackId`, with no `afterClipId` or replacement/removal fields), and its result is returned to the file-drop carrier so the existing skeleton is removed only after native refusal or a successful native preview. No prepared-media `applyEdit` fallback runs for this native-eligible video path. Images and prepared assets without Runtime selection retain their existing local behavior.

The existing command facade is created with the same `createTimelineCommands` mechanism already used by the editor and passed through the existing row-local asset-management hook. This is needed because `useTimelineState` builds the hook before `TimelineStoreProvider` is rendered; it does not add a public API, store field, DTO, provider method, commit-session method, Runtime door, or shared dependency. The file-drop path now awaits the existing `handleAssetDrop` result so native refusal is observable before skeleton cleanup.

## Changed source

- `src/tools/video-editor/hooks/useAssetManagement.ts`
  - accepts the existing `addClip` facade as an internal hook carrier;
  - routes video + `mediaSelection` through `addClip` and refuses silently only as a returned `false`, without fallback snapshot application;
  - keeps non-video and non-qualified prepared-media behavior unchanged.
- `src/tools/video-editor/hooks/useTimelineState.ts`
  - constructs the existing command facade with Runtime verified-media access and supplies it to the row-local asset hook.
- `src/tools/video-editor/lib/external-drop-utils.ts`
  - awaits prepared file-drop placement so the skeleton/refusal semantics remain correct.
- `src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx`
  - adds native manual-video producer success and native-refusal regressions, including original selection identity, normal ADD shape, no fallback `applyEdit`, and skeleton-preserving refusal.

No shared dependency or shared-repo patch is required.

## Verification

- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx`
  - PASS: 3 files, 27 tests.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/lib/external-drop-utils.ts`
  - PASS.
- `npx tsc --noEmit --pretty false --incremental false`
  - PASS.
- `git diff --check`
  - PASS.
- Central targeted harness:
  - `ap2-m2-parent-manual-drop-native-producer-targeted-1020202451-27876`
  - PASS, 2 files / 16 tests, exit 0, App tree `d5bd62cffcf558c6d5ffc1ebf3e9d368b09e47d0`.

No full suite, browser, localhost, live socket, schema, public-pin, or dependency run was performed.

## Next actual UI gate

The next gate is the real browser three-products/manual-file-drop journey against the candidate, covering Runtime verified selection, wrong-selection/stale-epoch refusal with draft preservation, lost acknowledgement/newer local intent, restart/retry/reload, undo, opaque preservation, no double placement, and legacy-writer absence. Run the central App browser suite only after that journey is present; do not treat this focused producer qualification as browser qualification.
