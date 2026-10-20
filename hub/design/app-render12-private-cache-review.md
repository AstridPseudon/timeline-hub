# App render12 private-cache review

## Result

Reviewed the render12 candidate at `9b98a7c7539f904d7450ca615d9fbf15a6afb702`.
The only worktree change is deletion of the accidentally committed
`docs/design/app-render-download-public12-cohort.md`. The existing orchestration
report was preserved outside the repository. No product, threshold, negative,
config-semantic, root, package, pin, or endpoint change was made.

The candidate remains HELD. This is source/test qualification only; no current
Runtime/Agent pair or actual browser/render gate is claimed.

## Reviewed allowlist and overlap

The seven reviewed render product/test paths are:

- `src/tools/video-editor/components/TimelineRenderControls.test.tsx`
- `src/tools/video-editor/components/TimelineRenderControls.tsx`
- `src/tools/video-editor/hooks/timelineStore.ts`
- `src/tools/video-editor/hooks/useRenderState.test.tsx`
- `src/tools/video-editor/hooks/useRenderState.ts`
- `src/tools/video-editor/hooks/useTimelineState.ts`
- `src/tools/video-editor/hooks/useTimelineState.types.ts`

The render/download behavior in the reviewed seven remains byte-identical to
`f08c3b976`/`320784f82` except for the already-present public12 helper closure
in `timelineStore.ts`, `useTimelineState.ts`, and `useTimelineState.types.ts`.
That closure forwards the existing track-label capture port and command-session
callbacks; it is unrelated to render behavior and was not introduced here.

The viewing closure remains intact: `playwright.viewing-parity.config.ts`,
`tests/e2e/timeline/player-export-frame-parity.spec.ts`, and all 20 files under
`tests/e2e/timeline/viewing-parity/`. The approved capture fix is preserved as
the complete pair `frames.ts` + `directframes.test.ts`, with four regression
cases. `frames.ts` is byte-identical to `1ba0800af`; `directframes.test.ts` is
byte-identical to `1ba0800af`. No threshold, comparison, negative, or fixture
semantics overlap was found.

## Public 0.0.12 inspection

The read-only dependency target was:
`/tmp/app-coherent-deps12/node_modules` (Composition `0.0.12`). Its artifact is
`vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz`, SHA-256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, with 77
installed regular files. The sorted 77-file content manifest aggregate is
`b4dd7df91c8fcae8552792f350676d726a8ae24e7d4e92486989b2e481037e4b`.

Root/evaluation/theme exports resolved successfully. `DEFAULT_THEME` is the
complete public value: `banodoco-default`, foreground `#FAFAFA`, background
`#050814`, accent `#67E8F9`, Arial/Arial/monospace typography, sizes 32/22/84,
weights 400/600, line height 1.2, fade 450ms, and 1920x1080 at 30fps.

The six App peer manifest hashes were unchanged and recorded as:

```text
react/package.json                 d4e68a5c96babb20cad1daafea8b78822eae45b341552cf5418d06a5304fa64c
react-dom/package.json             d2f29e31bd48b833e48cd7bbf41f192e8ee4ff8da249fdbe10d4ac4114b8b12e
remotion/package.json              1260b76eb109b0ebfff6cfb57f0e2b9b5fc8c6511f18bd43b047bddca068bd01
@remotion/player/package.json     89595cb2ec1e0231f576cf32408e81aa3dab522ebe0c2154dc4adb41746f7abf
@remotion/media/package.json      59e90c2e2d182faf420dd8b9461a74bedd21d6680a627ea6f2fb66c4efb9ee95
@remotion/layout-utils/package.json 244521ec2c97085930463bd476366cdf7f6392793a57d787b6f0576dbdeaafda
```

## Cache-safe evidence

This worktree used the ignored symlink `node_modules ->
/tmp/app-coherent-deps12/node_modules` and ran Vitest with the notes-only
preload `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs`,
`--configLoader=runner`, and `--no-cache`. No shared dependency contents were
modified.

Observed cache mtimes before and after were identical:

```text
/home/user/work/app/node_modules/.vite       2026-10-20 02:56:11.866370272 UTC
/home/user/work/app/node_modules/.vite-temp  2026-10-20 08:36:50.295585193 UTC
/tmp/app-coherent-deps12/node_modules/.vite       2026-10-20 07:51:42.787424251 UTC
/tmp/app-coherent-deps12/node_modules/.vite-temp  2026-10-20 08:32:56.447571292 UTC
/tmp/app-coherent-deps12/node_modules/.cache       missing
```

The default shared `.vite-temp` path therefore has prior activity at
08:36:50 UTC; it must not be described as historically untouched. This run did
not change it or the private12 cache.

## Tests

All commands ran from this worktree; no browser, localhost/live socket, full
suite, build, install, or project `tsc` was run.

- Direct render lane: 95/95 passed, 2 files.
- Render neighbors: 233/233 passed, 5 files.
- Mounted observer/projection neighbors: 357/357 passed, 13 files.
- Node helper lane: 9/9 helper files passed, including all four capture
  regressions in `directframes.test.ts`; zero failed/skipped/todo.
- `node --test config/vite/timelineCompositionPackage.test.mjs`: 1/1 passed.
- Scoped ESLint: passed.
- `check-known-failures`: 3 existing authorized markers, 0 forbidden.
- `check-no-smoke-tests`: passed.
- `git diff --check`: passed.

Exact Vitest invocations used the `snapshot-vitest-runner.cjs` preload,
`--config config/testing/vitest.config.ts --configLoader=runner --no-cache
--maxWorkers=1`; the helper invocation used:

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/components/TimelineRenderControls.test.tsx

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/components/TimelineRenderControls.test.tsx src/tools/video-editor/lib/renderRouter.test.tsx src/tools/video-editor/runtime/renderPlanner.test.ts src/tools/video-editor/runtime/renderability.test.ts

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/hooks/useTimelineRenderRequest.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/components/PreviewPanel/PreviewPanel.test.tsx src/tools/video-editor/components/PreviewPanel/RemotionPreview.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/lib/timeline-view-store.test.ts src/tools/video-editor/lib/timeline-overlay-stores.test.ts src/integrations/runtime/dataProvider.test.ts
```

```sh
node --import tsx --test --test-concurrency=1 \
  tests/e2e/timeline/viewing-parity/{admission,authority,bootstrap,compare,diagnostics,download,harness,media,directframes}.test.ts
```

The actual paired Agent/Runtime qualification, native MP4 render/download,
browser playback, frame parity, audio parity, and planted mismatch remain
unverified and are the recommended next step after the current tuple and
settings-first gate are settled.
