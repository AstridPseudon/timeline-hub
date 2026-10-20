# Commands and results

All commands ran against a private b1ef App snapshot with a private Composition 0.0.13 package overlay. Shared App `node_modules`, shared runtimes, and shared caches were not modified.

## Targeted mounted tests

```sh
node /home/user/work/app/node_modules/vitest/vitest.mjs run \
  --config "$PWD/candidate.vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 \
  src/tools/video-editor/lib/canonicalRenderBounds.test.ts \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/RemotionPreview.mailbox.test.tsx \
  src/tools/video-editor/hooks/useRenderState.test.tsx
```

Result: exit 0; 5 test files passed; 100 tests passed; 9.95s.

The mounted test covers stored caps of 4000ms and 4500ms, hold/fade/end-frame behavior, private config identity, compiled transition delivery, Player duration/extent, local→saving→accepted labels, late acknowledgement of A while B remains displayed, and unchanged editor/source behavior.

## Unapplied patch validation

```sh
git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-stored-cap-preview-consumer-proposal-consumer.patch
git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-stored-cap-preview-consumer-proposal-tests.patch
```

Result: both checks passed against the clean b1ef App snapshot.

No full suite, browser/e2e, localhost/socket, codec, render, network, or install command was run.
