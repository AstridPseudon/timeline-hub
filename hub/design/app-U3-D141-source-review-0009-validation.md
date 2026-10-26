# U3/D141 validation

## Static/source checks

- `git diff --check`: PASS, exit 0.
- `git merge-base --is-ancestor 5696769dfca056676cde1ab46d8bc94354b3a44a HEAD`: PASS, exit 0.
- `git merge-base --is-ancestor 7ca61bb3280beca21d98a854af266a382f7ce5df HEAD`: PASS, exit 0.
- Conflict-marker scan over all six author conflict paths: PASS, zero markers.
- JSON parse of `public/install-manifest.json` and `vendor/astrid-browser/provenance.json`: PASS.
- Worktree remained clean; reviewer made no product/test/generated/config changes.

## Targeted tests

The prescribed direct command was attempted with Node `v20.19.4`:

```sh
npm run test:app -- --no-cache --configLoader=runner --maxWorkers=1 src/shared/components/PaneControlTab.test.tsx src/shared/components/RuntimeConnection/RuntimeConnectionPanel.test.tsx src/shared/state/editorTourStore.test.ts src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/TourChatPanel.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.playback.test.tsx src/tools/video-editor/components/PreviewPanel/previewPlaybackPreferences.test.ts src/tools/video-editor/components/TimelineEditorShellCore.test.tsx src/tools/video-editor/hooks/useKeyboardShortcuts.test.tsx src/tools/video-editor/runtime/commandRegistry.test.ts src/tools/video-editor/tour/runner/cardPlacement.test.ts src/tools/video-editor/tour/runner/editorTourTargets.test.ts src/tools/video-editor/components/PreviewPanel/RemotionPreview.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.mailbox.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.audioFailure.test.tsx
```

Direct result: NOTRUN/exit 1 before collection. The configured Vitest runner loader evaluated `config/testing/vitest.config.ts` with `__dirname` undefined. Repository preflight checks passed before this startup error.

The allowed central targeted service then ran the same exact 15 file paths on candidate tree `736026fcdd9ba9fa377a4d06d7fca166c6e3fea8` (service invocation used its configured `npx vitest ... --maxWorkers=2` command):

- 15 files; 14 passed, 1 failed.
- 497 tests collected; 484 passed, 13 failed.
- All 13 failures are in `src/tools/video-editor/components/AgentChat/TourChatPanel.test.tsx`.
- The other 14 files passed, including `AgentChat.test.tsx` (76 tests) and `TimelineEditorShellCore.test.tsx` (128 tests).
- No full suite, browser journey, build, ZIP, or child run was requested.

The 13 failures are the source-regression evidence: session hooks were called during the tour, the scripted composer remained absent/empty, and the tour anchors did not render. They are not generated-artifact failures.

## Lint/type/installer checks

All commands used the supplied Node `v20.19.4`; TypeScript commands used the existing shared flock.

- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/components/AgentChat/TourChatPanel.tsx src/tools/video-editor/components/AgentChat/TourChatPanel.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx --report-unused-disable-directives --max-warnings 0`: PASS, exit 0.
- `flock -w 600 /home/user/work/.app-tsc.lock node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json --pretty false`: PASS, exit 0.
- `flock -w 600 /home/user/work/.app-tsc.lock node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json --pretty false`: PASS, exit 0.
- `node --import tsx --test --test-concurrency=1 --test-reporter=spec --test-reporter-destination=stdout --test-reporter=./scripts/quality/node-skip-guard-reporter.mjs --test-reporter-destination=stdout scripts/installer/manifest.test.mjs scripts/installer/update-manifest.test.mjs`: PASS, 4/4 tests.

## Author checks retained as deferred

The author’s manifest plan remains blocked by Runtime lock/source mismatch; vendor verification remains blocked by the two mismatches recorded in `source-manifest.json`. Those are not treated as source behavior evidence and no hashes or pins were changed.
