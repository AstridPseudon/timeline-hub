# App M2 post-merge shot-name cut ledger

## Verdict

**BOUNDED EMBEDDED NAME QUALIFIED; D01 REMAINS OPEN.** The merged App source
has a real embedded `shot.set` ingress, but the legacy callback and fallback
writers are still present. This is evidence for the bounded embedded name
completion only. It is not a whole settings, standalone, gallery, or
zero-writer deletion.

## Source and merge applicability

- Assigned merged commit: `ddd9e7824c7c0c08b1293132484f5ac52d1de3c3`
- Assigned merged tree: `83cf9199f2f858147d8ebbfc6648f01962bbe333`
- Shot-name parent commit: `9d9eb4b18c5526d9599131ac8e4fcf6be95707da`
- Shot-name parent tree: `2d5d7dba66e91f6306aa72a006abcdf4ea4bdd0b`
- `git diff --stat 9d9eb4b18..ddd9e7824` is seven disjoint visual-seam
  paths; no shot-name source or test path changed. The merge is therefore
  applicable to the current App2 seam without changing the exact browser
  evidence identity.

The existing central proof remains exactly the proof recorded for
`9d9eb4b18/tree2d5d7dba`: 1 browser test, 9 Composition resolver tests, and
the recorded 83 focused controls passed. It is not relabeled as evidence from
`ddd9e7824`.

## What the merged source proves

The embedded route is connected as follows:

`AstridTimelineEditor` selects the session's `shotSet` port and passes it to
`LocalTimelineShotBrowser`, which passes it to `ShotEditorView`.
`ShotEditorView` captures before opening the name editor, using the verified
project, parent-document, head, and occurrence identity. On save it finishes
the captured basis as `shot.set` with `{ values: { name }, clear: [] }` and
submits through the same durable command session. The command-session seam
rejects a changed generation or observed bundle instead of merging live bytes
into the original captured guards.

The current type/seam remains optional through
`TimelineEditorOpsContextValue.shotSet`, `useTimelineState`, and
`useTimelineCommandSession`. That is the native requirement: an embedded name
edit is native only when a verified `shotSetPort` is present and its
project/timeline/head matches the displayed composition. If that authority is
missing or stale, capture must refuse and the name draft must remain; it must
not fall through to a legacy writer.

## Remaining legacy writers

The legacy callback was not removed. `ShotEditorView` still supplies
`onUpdateShotName` through the ShotEditor controller/header chain. The callback
currently has these remaining callers/branches:

- `ShotEditorView.tsx:396-418`: canonical `updateCanonicalShotName` followed
  by `canonicalShotComposition.publish` when no captured native basis is
  available;
- `ShotEditorView.tsx:420-425`: `useUpdateShotName().mutate` fallback;
- `VideoShotDisplay.tsx:139-167`: direct gallery
  `useUpdateShotName().mutateAsync` writer;
- `ShotEditorView.tsx:137-212`: the separate canonical shot-settings
  persistence writer remains.

The native branch takes precedence for a successfully captured embedded edit,
but the source still contains callable fallback paths. No exact writer is
retired by this merge, so no `DELETED` subrow is added. The parent
`D01-app-shot-graph-settings` row stays `in-progress`; its evidence was
updated to record this bounded name qualification and the open settings,
standalone, and gallery scope.

## Tests run on the assigned merged source

Command:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/shotSetCapture.test.ts \
  src/tools/video-editor/commands/shotSetSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts \
  src/tools/travel-between-images/pages/ShotEditorView.test.tsx \
  src/tools/travel-between-images/pages/LocalTimelineShotBrowser.test.tsx
```

Result: **6 test files passed; 65 tests passed; exit 0.** This includes the
native capture/session controls, mounted command-session seam controls, name
completion/refusal controls, and existing canonical/local shot-editor seam
controls.

An initial `--configLoader runner` invocation was not usable because the
repository's config uses `__dirname`; it failed during config loading before
tests ran. The command above uses the repository's supported bundled config
loader and is the qualifying result.

Not run: full suite, browser, TypeScript, build, install, localhost/live
sockets, or shared-cache writes. No product files were changed.
