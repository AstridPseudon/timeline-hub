# App exact3a read-only review commands

All commands below used the exact commit archive and the worker-owned private
dependency overlay. No command used `/home/user/work/app/node_modules`.

## Source identity and graph preflight

```sh
git show -s --format='%H%n%P%n%s' 3a4350f9d
git diff --check 3a4350f9d^ 3a4350f9d

git archive 3a4350f9d | tar -xf - -C <worker>/exact3a-private
# <worker>/own-node_modules contains real @scope directories and one leaf
# symlink per package from the clean private12 graph.
realpath <worker>/exact3a-private/node_modules
find <worker>/own-node_modules -type l | wc -l
find -L <clean-private12>/node_modules/@banodoco/timeline-composition -type f | wc -l
```

Observed: exact SHA `3a4350f9d9a578f817568d5fe348c5d750595129`; diff check exit
0; owned node_modules realpath stayed inside the worker; 531 leaf links; the
public12 Composition package had 77 files; no link target referenced the
shared App install.

## Producer and persistence lane

```sh
env -u ASTRID_CHECKOUT node --require <worker>/dirname-preload.cjs \
  <clean-private12>/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/travel-between-images/components/ShotTimelinePreview.test.ts
```

Result: **5 files, 180 tests passed, exit 0**.

## Consumer neighbor lane

```sh
env -u ASTRID_CHECKOUT node --require <worker>/dirname-preload.cjs \
  <clean-private12>/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts \
  src/tools/video-editor/data/shotCompositionProjection.test.ts
```

Result: **5 files, 60 tests passed, exit 0**.

## ES2020 project check

```sh
env -u ASTRID_CHECKOUT node \
  <clean-private12>/node_modules/typescript/bin/tsc \
  -p tsconfig.app.json --noEmit --pretty false
```

Result: **exit 0, no diagnostics**. No output was emitted.

## Read-only source checks

```sh
git show 3a4350f9d:src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.tsx
git show 3a4350f9d:src/tools/video-editor/hooks/useClientRender.ts
git show 3a4350f9d:src/tools/video-editor/lib/canonicalRenderBounds.ts
git status --short --branch
```

These checks show the still and client-render input props omit the shared
compiled vector/fact, and the render-bound helper does not implement the
corrected per-clip invalid-scalar fallback. The App source worktree remained
clean.

Not run: browser, network, install, full suite, live socket, render, or
pixel/audio parity.
