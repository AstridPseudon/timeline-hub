# App MAIN574 true refresh

## Source and resolved tree

- Repository: App
- Current integration/base: `9d518546d` (`tl/integration`), including trim-helper deletion `93cd2f7d4`.
- Upstream parent: `17e46de99b7cef52fe494de1703a9865a8d4be24`.
- Incoming upstream tip: `574e97f44a81e0ec1a896fc3fb8626deb2f1edf0` (`origin/main`).
- Incoming commits, in order:
  - `8a8a32186` — mobile Video / Inspector / Extensions tabs.
  - `e4b199066` — extension host and Transcript panel lifecycle.
  - `2fa200ce1` — calm preview row, New timeline picker placement, touch seek Video.
  - `94262ee21` — chat-tab lifecycle and session controls.
  - `574e97f44` — gallery tab opening and readable clip names.
- The five-commit patch was applied to the working tree as `git diff 17e46de99..origin/main`; no Git merge or commit was run.
- Resolved tree is the uncommitted working tree at HEAD `9d518546d` plus the applied patch. Exact final working-tree patch fingerprint: `c0e2a26a2f7f46741ac5bfbaa1af8d103fdff8a5fee8e7dfe7eda27ad9d763bd`.
- Exact incoming patch fingerprint: `3a924ce27a5b3e2543c445731ab3e26807c6ebf07fdd7284426fc5b0dc2dee0b`.
- A Git tree object is intentionally not claimed here: the sandbox Git index/metadata is read-only. The harness must create the commit with `9d518546d` as first parent and `574e97f44a81e0ec1a896fc3fb8626deb2f1edf0` as the second parent.

## Conflict and intent resolution

The ten overlapping paths were:

- `src/tools/video-editor/components/TimelineEditor/TimelineCanvas.tsx`
- `src/tools/video-editor/components/TimelineEditor/TrackLabel.tsx`
- `src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx`
- `src/tools/video-editor/components/TimelineEditor/TrackListRenderer.tsx`
- `src/tools/video-editor/components/TimelineEditorShellCore.test.tsx`
- `src/tools/video-editor/components/TimelineEditorShellCore.tsx`
- `src/tools/video-editor/contexts/VideoEditorProvider.tsx`
- `src/tools/video-editor/lib/timeline-data.test.ts`
- `src/tools/video-editor/lib/timeline-data.ts`
- `src/tools/video-editor/lib/timeline-domain.ts`

The patch had manual rejects only in `TimelineCanvas.tsx`, `TrackLabel.tsx`, and `TrackListRenderer.tsx`. Resolution was minimal:

- Adopt MAIN's removal of the obsolete touch track sheet, `TimelineMobileInspectorDialog`, and `mobile-sheet` helper.
- Preserve current command-backed desktop track-label capture, error retention, and the canvas footer `+ Video` / `+ Audio` controls.
- Stop passing `onAddTrack` through row labels; touch track editing is now the incoming `TrackInspector` surface.
- Keep current integration's command/recovery, raw capture, outbox, hydration, and timeline data changes in the seven automatically overlapping paths while taking MAIN's UI/lifecycle changes.
- Adapted only the pre-refresh touch track-label test matrix: touch rows are now selection-only and their editing is covered by `PropertiesPanel.test.tsx`'s `TrackInspector` cases; desktop command-backed label tests remain intact.

## Incoming deletions and retained paths

Incoming deletions retained:

- `src/tools/video-editor/components/TimelineMobileInspectorDialog.tsx`
- `src/tools/video-editor/lib/mobile-sheet.ts`

No package, Runtime pin, public12 pin, save/outbox/recovery, raw-capture guard, render/download/admission, or legacy-writer path was changed outside the incoming allowlist and the ten overlap resolutions. The existing trim-helper deletion remains present.

## Tests and checks

All runs used the private `/tmp/tl-app-main574-true-refresh-tmp/vitest-preload.cjs`, `NODE_PATH=/tmp/app-coherent-deps12/node_modules`, `--configLoader=runner --no-cache --maxWorkers=1`, and an own `TMPDIR`.

Exact focused commands (the first command below is the complete six-file control lane; the second is the complete 16-file changed-area lane):

```bash
NODE_PATH=/tmp/app-coherent-deps12/node_modules TMPDIR=/tmp/tl-app-main574-true-refresh-tmp node --require /tmp/tl-app-main574-true-refresh-tmp/vitest-preload.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx src/tools/video-editor/components/TimelineEditorShellCore.test.tsx src/tools/video-editor/hooks/useAgentSession.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatSessionSelector.test.tsx

NODE_PATH=/tmp/app-coherent-deps12/node_modules TMPDIR=/tmp/tl-app-main574-true-refresh-tmp node --require /tmp/tl-app-main574-true-refresh-tmp/vitest-preload.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 scripts/astrid-acp-bridge.test.ts src/features/gallery/components/GenerationsPane/GenerationsPane.lightbox.test.tsx src/features/gallery/components/GenerationsPane/components/GenerationsPaneGallery.test.tsx src/features/gallery/components/GenerationsPane/hooks/useGenerationsPaneController.test.ts src/shared/components/ProjectTimelineSelectors.test.tsx src/tools/video-editor/browser/initializeVideoEditorExtensionRuntime.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/VideoEditorRightPanelDock.test.tsx src/tools/video-editor/components/TimelineEditor/ClipAction.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/data/generationAssetResolver.test.ts src/tools/video-editor/lib/assetMetadata.test.ts src/tools/video-editor/lib/clipDisplayNames.test.ts src/tools/video-editor/lib/timeline-asset-plans.test.ts src/tools/video-editor/lib/timeline-data.test.ts src/tools/video-editor/pages/VideoEditorPage.test.tsx src/tools/video-editor/runtime/extensionReleaseControls.test.ts

NODE_PATH=/tmp/app-coherent-deps12/node_modules TMPDIR=/tmp/tl-app-main574-true-refresh-tmp node --require /tmp/tl-app-main574-true-refresh-tmp/vitest-preload.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts
```

Exact static command:

```bash
changed_files=$( { git diff --name-only 17e46de99b7cef52fe494de1703a9865a8d4be24 origin/main; printf '%s\n' src/tools/video-editor/components/PropertiesPanel/TrackInspector.tsx src/tools/video-editor/lib/clipDisplayNames.ts src/tools/video-editor/lib/clipDisplayNames.test.ts; } | sort -u | while IFS= read -r f; do test -f "$f" && case "$f" in *.ts|*.tsx) printf '%s\n' "$f";; esac; done); node node_modules/eslint/bin/eslint.js $changed_files; git diff --check
```

1. Focused shell, Inspector, label, chat, and session controls: **306 passed / 6 files**. This included `TrackListRenderer.test.tsx`, `PropertiesPanel.test.tsx`, `TimelineEditorShellCore.test.tsx`, `useAgentSession.test.tsx`, `AgentChat.test.tsx`, and `AgentChatSessionSelector.test.tsx`.
2. Remaining changed-area tests: **321 passed / 16 files**. This covered gallery, selectors, extension runtime, clip/panel/provider, asset resolver/display names, timeline data/plans, VideoEditorPage, and extension release controls.
3. Root-label command/capture controls: **98 passed / 3 files** (`TrackLabel.command.test.tsx`, `trackLabelCapture.test.ts`, `trackLabelGesture.test.ts`).
4. Targeted ESLint over all existing incoming TypeScript/TSX paths plus new `TrackInspector` and clip-display-name files, then the final conflict files: **exit 0**.
5. `git diff --check`: **exit 0**.

The first combined test launch was stopped after it identified 14 stale touch-sheet expectations in `TrackListRenderer.test.tsx`; a direct command-label run then identified 38 equivalent touch-sheet expectations in `TrackLabel.command.test.tsx`. Both tests were adapted to the MAIN Inspector move, and the exact affected lanes passed. No `it.fails`, skip, or assertion weakening was added.

Total focused evidence: **725 passed** across the three Vitest lanes.

Not run: full suite, browser/e2e, localhost/socket tests, project TypeScript, build, or install. Manager owns the one final full-suite request on the refreshed true two-parent tree.
