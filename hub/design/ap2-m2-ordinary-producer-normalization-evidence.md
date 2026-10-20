# AP2 M2 ordinary producer normalization evidence

## Boundary and shape

The production Scene Phase Markers alignment producer previously emitted:

```text
clip.move   payload { track: trackId, at: time }
clip.update payload { hold, mode: "merge" }
```

For a known clip whose current track is the requested track, it now emits the
documented ordinary-member equivalents:

```text
clip.move   payload { at: time }
clip.update payload { values: { hold }, clear: [] }
```

The move target, time unit (seconds), operation order, source, metadata, and
positive hold value are unchanged. Cross-track and unresolved targets retain
the legacy `{ track, at }` move shape and therefore remain on the existing
guarded path. Shot creation (`clip.add` plus labelled updates) is unchanged.

Duplicate target alignments, negative/non-finite times, and non-positive or
non-finite holds refuse before `timeline.apply`; the panel catches the error,
reports diagnostics, and shows an error toast.

## Checks

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx \
  src/tools/video-editor/lib/timeline-patch.test.ts
```

Pass: 4 files, 350 tests.

```text
node_modules/.bin/eslint \
  src/tools/video-editor/dev/scene-phase-markers/extension.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  --max-warnings 0
```

Pass.

```text
node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

Exit 2 on existing diagnostics in `elementCapture.ts`, `elementGesture.ts`,
`genericPatchCapture.ts`, `occurrenceDuplicateCapture.ts`, Preview/Composition
integration files, and `config-utils.ts`. No diagnostic names either changed
Scene Phase Markers file.

`git diff --check` passed. No browser, localhost, socket, full, or central
actual-journey suite was run. The remaining gate is the central locked
`e2e-m2-ordinary-three-products` execution after this candidate is registered
with the qualified ordinary member tuple.
