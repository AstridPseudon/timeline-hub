# App label reconciliation private13 control verification

Date: 2026-10-20 UTC  
Worker: `app-m3-label-reconciliation-private13-controls`

## Scope and source identity

Verification only. No App source or test files were changed.

- App HEAD: `8a79a7bb9416302f36b6a8c104444ff609dff5e0`
- App tree: `19b61ebd8ec15de7ba3b656059412df5de97e913`
- `package.json` SHA-256: `a2ac9c9d946bd2d0ee1b2283154d94adad926f6282fff4417aeaf7520f138437`
- `package-lock.json` SHA-256: `7f1bfcea48cef38d4c6f1163aa34190b8d5e71c9f08c7378e01a962d6696fc14`
- `runtime.lock.json` SHA-256: `550de9dc3269380c79f44a6db4c87a5d5459058d550ae49e635a6dda809e76a2`
- Worktree status before/after: clean

## Approved private13 graph

Toolchain root used for the run:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules`

Verified package identities from that root:

- `@banodoco/timeline-composition@0.0.13`; approved archive is 58,477 bytes,
  77 regular members, SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- `react@18.3.1`, `react-dom@18.3.1`
- `remotion@4.0.509`, `@remotion/media@4.0.509`,
  `@remotion/player@4.0.509`, `@remotion/layout-utils@4.0.509`
- `vitest@4.1.5`, `vite@5.4.21`
- With the worktree-local root symlink pointed at this graph, the direct
  `@banodoco/timeline-composition/evaluation` probe found
  `computeMediaTrim`.

The normal worktree `node_modules` symlink was temporarily redirected only to
the approved private root for each run and restored afterward. No bundled
renderer fallback, install, extraction, or shared dependency repair was used.

## Exact commands

For each lane, the worktree-local `node_modules` symlink was redirected to the
private13 root above, with a trap restoring the original symlink. The exact
Vitest invocation was:

```sh
TMPDIR="$RUN_TMP" NODE_OPTIONS="--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs" \
node /home/user/work/wt/app-m3-label-reconciliation-private13-controls/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  <files>
```

Exact two-file lane:

```text
src/tools/video-editor/lib/timeline-save-utils.test.ts
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx
```

Its complete command was:

```sh
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-label-reconciliation-private13-controls/runs/private13-verify/tmp-exact \
NODE_OPTIONS="--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs" \
node /home/user/work/wt/app-m3-label-reconciliation-private13-controls/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/timeline-save-utils.test.ts \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx
```

Former 31-failure and MAIN label/timeline/projection lane:

```text
src/tools/video-editor/lib/clipDisplayNames.test.ts
src/tools/video-editor/lib/timeline-data.test.ts
src/tools/video-editor/lib/config-utils.test.ts
src/tools/video-editor/data/timelineOutputProjection.test.ts
src/tools/video-editor/data/shotCompositionProjection.test.ts
src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx
```

Its complete command was:

```sh
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-label-reconciliation-private13-controls/runs/private13-verify/tmp-broad \
NODE_OPTIONS="--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs" \
node /home/user/work/wt/app-m3-label-reconciliation-private13-controls/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/clipDisplayNames.test.ts \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/lib/config-utils.test.ts \
  src/tools/video-editor/data/timelineOutputProjection.test.ts \
  src/tools/video-editor/data/shotCompositionProjection.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx
```

The private13 graph probe, run after the overlay was active, was:

```sh
node --input-type=module -e "import('@banodoco/timeline-composition/evaluation').then(m => { if (typeof m.computeMediaTrim !== 'function') throw new Error('private13 computeMediaTrim missing'); console.log('private13 composition evaluation export: computeMediaTrim'); })"
```

## Results

- Exact two-file lane: **2 files, 39 tests passed, 0 failed**.
- Former 31-failure plus MAIN lane: **8 files, 146 tests passed, 0 failed**.
- Distinct union: **10 files, 185 tests passed, 0 failed**.
- The prior `getSanitizedMediaTrimProps is not a function` failures did not
  reproduce with private13. They were an environment-only mismatch from the
  shared Composition 0.0.10 package, not unresolved product failures on this
  graph.
- Shared node_modules before/after full-file fingerprint:
  `3f3063f8ce79536d7e60ad32932488bd0e064a33d6d227713f17eb2a1480dc02`.
  Key shared package hashes were also identical; the worktree symlink was
  restored to `/home/user/work/app/node_modules`.
- No worktree build/cache directories were created.

## Limits

No full suite, TypeScript check, browser/live-socket run, build, install, or
new tests were run. This is not a claim that the latest full suite is green.
Semantic independent review is separate and is not claimed by this control
verification.
