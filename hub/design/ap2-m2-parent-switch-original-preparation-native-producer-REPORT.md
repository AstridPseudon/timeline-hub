# ap2-m2-parent-switch-original-preparation-native-producer

## Result

Implemented the qualified `useSwitchToFinalVideo.updateToLatestVideo` parent replacement path in the App worktree.

- Captures and shallow-freezes the UI-selected final-video identity, raw target fingerprint, replacement clip ID, and native session preparation before producer awaits.
- Uses the existing Runtime `prepareMediaImport` boundary, requires its original five-field `mediaSelection`, then passes that selection through the existing `prepareGenerationAsset` facade.
- Sends exactly one `commands.addClip({ preparedAsset, replaceClipId })` call into the existing native facade. The qualified path does not call legacy registry registration or `applyEdit`; the existing facade performs Runtime verification and parent `clip.swap-media` capture/submit.
- Added session preparation/epoch assertions to the existing parent swap port and its command-session wrapper. A stale target/session refuses before command submission.
- Preserves the native carrier’s raw parent clip semantics because no replacement timing or metadata mutation is constructed by the producer callback.
- Added callback tests for exact selection forwarding, no legacy edit, and pending native preparation refusal.

## Files changed

- `src/tools/video-editor/hooks/useSwitchToFinalVideo.ts`
- `src/tools/video-editor/components/AstridTimelineEditor.tsx`
- `src/tools/video-editor/commands/commitSession.ts`
- `src/tools/video-editor/hooks/useTimelineCommandSession.ts`
- `src/tools/video-editor/hooks/useClipEditing.test.ts`

## Verification

All commands ran in the private worker worktree with shared dependency installs left untouched.

- `./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useSwitchToFinalVideo.ts src/tools/video-editor/components/AstridTimelineEditor.tsx src/tools/video-editor/hooks/useClipEditing.test.ts` — passed.
- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/parentClipSwapCapture.test.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx` — 6 files, 214 tests passed.
- `git diff --check` — passed.

An initial attempt with `--configLoader runner` stopped at config startup because this repo's Vitest config uses CommonJS `__dirname`; the successful command above uses the normal loader and does not write the shared Vite cache.

No full, browser, localhost, socket, or AppProvider-final-join suite was run, per task instructions. No blocker remains in this worker scope.
