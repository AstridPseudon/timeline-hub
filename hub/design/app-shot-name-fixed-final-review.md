# App M2 shot-name fixed final review

## Verdict

**REJECT** source `04810b121ddc36112025e30f9a83630aaff2eece` for the bounded
shot-name fix. The two original stale-basis/draft-retention findings are fixed,
but the required late-callback retirement is incomplete: `useNameEditing`
still updates editor actions after its component unmounts.

## Exact source identity

- App SHA: `04810b121ddc36112025e30f9a83630aaff2eece`
- App tree: `e86392403b3259cbc562aec9b4974fb292830a3b`
- Parent/review target: `a4fb4bbb00e8c0453fdce8d311cf6a63944fc7b9`
- Frozen Agent parity reference: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`
- Agent fixture used for parity: `tests/editing_conformance/fixtures/recipe_m2_shot_set.json`

## Source findings

### Fixed controls

1. `commitSession.ts:367-390` now keeps `before` from the captured basis and
   `after` from the same `finishShotSet` result. It does not combine a stale
   captured result with a newer live `bundle`. Submission compares the captured
   `before` with the current session bundle using `equal`, so a remote
   observation cannot silently publish a mixed graph.

2. The captured command retains the original `expect`, reads, source
   dependency pin, occurrence binding, and writes. The session completion is
   tied to the same outbox intent and is settled from the accepted receipt in
   `pump` (`record.accepted.intentId`), not from `saveStatus`.

3. `useNameEditing.ts:67-103` keeps the native form pending until the returned
   completion resolves, restores the exact untrimmed draft on rejection, and
   leaves the form open. The view callback also gates its canonical-name update
   by mounted state and shot scope (`ShotEditorView.tsx:369-386`). A shot-scope
   change retires the pending hook callback by clearing `pendingSaveRef`.

4. A review-only golden probe against the d874 fixture found App command and
   after-bundle deep equality. The focused session test also exercises the
   accepted completion and native inverse publication. No inverse-generation
   source changed in this fix.

### Concrete remaining rejection

`useNameEditing.ts:82-95` has no unmount guard. `pendingSaveRef` is cleared on
shot-id change, but no effect cleanup retires it on unmount. After an accepted
native completion, the hook continuation still sees the same `pending` and
`syncedShotIdRef` and calls `actions.setEditingName(false)` after unmount. The
view-level `mountedRef` does not prevent this: the hook attaches its own
continuation to the Promise returned by `onUpdateShotName`.

A temporary direct control reproduced this against the reviewed source:
render the hook, start a deferred native save, unmount, resolve the completion;
the safety assertion that neither editor action is called failed because
`setEditingName(false)` was called once. The temporary test was removed and
does not modify the candidate tree.

Required correction: add a hook-owned mounted/lifetime guard (with cleanup)
around both accepted and refused completion callbacks, while preserving the
existing shot-scope guard and exact draft restoration for a still-mounted
scope. Add the direct unmount regression alongside the existing acceptance and
refusal tests.

## Remaining live NAME writers

These remain intentionally outside this bounded review and are not a reason
for the rejection:

- Embedded parent-mounted native path: `ShotEditorView.tsx:357-394`, when
  `shotSetPort` capture succeeds.
- Standalone/canonical fallback name writer:
  `ShotEditorView.tsx:396-418`, via `updateCanonicalShotName` and canonical
  publish.
- Ordinary legacy/Supabase editor writer: `ShotEditorView.tsx:420-424`, via
  `useUpdateShotName().mutate`.
- Gallery/list writer:
  `VideoShotDisplay.tsx:155-163`, via `useUpdateShotName().mutateAsync`.
- Separate canonical settings writer remains in
  `ShotEditorView.tsx:159-210`; it was not migrated here.

## Controls run

All Vitest controls used the private12 Vitest binary, an own runner preload for
the repository's existing `__dirname`, `--configLoader=runner --no-cache`, and
an explicit worker-owned cache directory. No shared `.vite` or `.vite-temp`
path was targeted.

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-shot-name-fixed-final-review/runner-paths.cjs \
  /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run \
  --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-shot-name-fixed-final-review/vitest.private12.config.ts \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/shotSetCapture.test.ts \
  src/tools/video-editor/commands/shotSetSession.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/travel-between-images/pages/ShotEditorView.test.tsx \
  src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts
PASS: 6 files, 119 tests.
```

Review-only controls:

- Agent fixture command/after parity: **PASS**, 1 temporary test; removed after
  execution.
- Unmount retirement control: **FAIL**, 1 temporary test; the reviewed hook
  called `setEditingName(false)` once after unmount; removed after execution.
- ESLint on all eight changed source/test files: **PASS**.
- `git diff --check`: **PASS**.

Not run: full suite, project typecheck, build, browser, localhost/socket
journey, Runtime HTTP acceptance, reload/restart, lost-ACK retry, or the
actual zero-legacy-writer gate. The central runtime/browser gate remains for
after this source rejection is repaired.
