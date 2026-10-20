# App embedded shot-name legacy fallback cut

## Result

Deleted the one replaced embedded placed-shot NAME writer in
`src/tools/travel-between-images/pages/ShotEditorView.tsx`: the
`updateCanonicalShotName` → `canonicalShotComposition.publish` fallback branch.
The unused `updateCanonicalShotName` import was removed with it.

Canonical name edits now require the existing occurrence-owned `shotSetPort`
capture/session. A canonical timeline/occurrence with no mounted authority
reports `Mounted shot.set name authority is unavailable; draft kept.` and
throws through the existing `useNameEditing` path, which restores and keeps
the exact dirty draft. It does not call the canonical composition publisher,
the project/Supabase mutation, or a whole-config snapshot.

The existing `useUpdateShotName` project method remains unchanged for edits
without explicit canonical timeline/occurrence ownership, preserving
standalone and unplaced project-catalog behavior without inferring an owner.
Canonical shot settings persistence remains open and was not changed.

## Ledger classification

`qualifyboundedDELETED`: the embedded placed-shot NAME fallback writer is
actually gone. This is a bounded deletion only; the parent
`D01-app-shot-graph-settings` / whole shot-settings row remains open.
Standalone, gallery, and canonical shot-settings writers were not removed.

## Tests

Command run:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/shotSetCapture.test.ts src/tools/video-editor/commands/shotSetSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/travel-between-images/pages/LocalTimelineShotBrowser.test.tsx
```

Result: 5 files passed; 62 tests passed; 1 file failed with 3 tests. The
three failures are the existing `ShotEditorView` assertions that directly
invoke the removed canonical fallback and still expect it to publish. Test
hunks were not changed because the composer owns the one-to-one refusal and
equivalent native-success remap. No full suite, browser, TypeScript, build,
install, or shared dependency writes were run.

