# Corrected stored-cap consumer final gate commands

Private review leaf:

```text
/home/user/work/wt/vw-m3-stored-cap-corrected-final-gate/review/app
```

It was reconstructed from the exact App commit
`b1ef4b9b910ba72375c34cf319692f90d22edc25`. The App integration worktree was
not modified. Shared `node_modules` was linked read-only; Vitest used the
worker-owned `review/vite-cache`.

## Patch applicability

```text
git -C review/app apply --check \
  /tmp/.../handoff-vw-m3-stored-cap-consumer-preserve-boundaries-consumer.patch
git -C review/app apply --check \
  /tmp/.../handoff-vw-m3-stored-cap-consumer-preserve-boundaries-tests.patch
```

Result: both patches applied cleanly to the exact clean `b1ef` archive.

For context, applying the patches directly to the newer `/home/user/work/app`
integration tree failed in two preview files because that tree has advanced;
that is not the handoff's stated base and was not used as qualification.

## Focused regression

```text
node /home/user/work/app/node_modules/vitest/vitest.mjs run \
  --config /home/user/work/wt/vw-m3-stored-cap-corrected-final-gate/review/app/candidate.vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 \
  --testNamePattern='uses only the private stored occurrence cap|uses the effective cap for missing and invalid stored metadata|does not clamp malformed stored metadata|delivers the paired vector and bounded extent|bounds only the private stored-cap render copy' \
  src/tools/video-editor/lib/canonicalRenderBounds.test.ts \
  src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx
```

Result: **3 files passed; 9 tests passed, 24 filtered; exit 0** (Vitest
4.1.5, 4.18s).

No full suite, browser, render, network, socket, install, or git mutation was
run.
