# Commands and results

All commands used the private b1ef App extract and private Composition build
under this worker's scratch directory. Shared `node_modules` was read-only;
Vite used the worker-owned cache.

## Targeted mounted regressions

```text
node /home/user/work/app/node_modules/vitest/vitest.mjs run \
  --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-stored-cap-consumer-preserve-boundaries/scratch-app/candidate.vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/lib/canonicalRenderBounds.test.ts \
  src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/RemotionPreview.mailbox.test.tsx \
  src/tools/video-editor/hooks/useRenderState.test.tsx
```

Result: 6 files passed, 115 tests passed, exit 0.

## Scoped lint and types

```text
./node_modules/.bin/eslint \
  src/tools/video-editor/lib/canonicalRenderBounds.ts \
  src/tools/video-editor/lib/canonicalRenderBounds.test.ts \
  src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.tsx \
  src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx \
  src/tools/video-editor/components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx \
  src/tools/video-editor/hooks/useRenderState.ts \
  --report-unused-disable-directives --max-warnings 0
```

Result: exit 0.

```text
./node_modules/.bin/tsc -p tsconfig.worker.json --noEmit --pretty false
```

Result: exit 0. The worker config points at the private Composition build;
the initial borrowed stale overlay was not used as final evidence.

## Patch validation

```text
git -C /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-stored-cap-consumer-preserve-boundaries/base-app apply --check \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-stored-cap-consumer-preserve-boundaries-consumer.patch
git -C /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-stored-cap-consumer-preserve-boundaries/base-app apply --check \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-stored-cap-consumer-preserve-boundaries-tests.patch
```

Result: both unapplied patches apply cleanly to the clean b1ef extract.

