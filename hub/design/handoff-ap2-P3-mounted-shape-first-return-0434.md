# Handoff: P3 mounted shape-first return

## Change

Starting from `bd4a89bb31484e6b973f8657b39514c0ecb3d244`, changed only `tests/e2e/local/three-products.spec.ts`.

Gate 5 now has mounted-document-only setup/owner helpers. They inspect the real persisted `local-save.documentIntent` chain, including B's `{ after: A }` basis, local canonical `before` at 5, local canonical `after` at 7, and the exact guarded patch:

```text
set parent/clips/id:<appClipId>/at
before: present(5)
value: 7
```

The post-restart B request is asserted as the exact `doc.patch` command and step patch derived from the persisted B intent. Existing native journeys keep `ownerWithTwoMoves` and `prepareAfterAckLossMoves` unchanged. Gate 5's original retry key/body/receipt, merged status, canonical closure, Agent C, undo, preview, opaque-data, and zero-legacy expectations remain unchanged.

## Evidence

- Gate 5 list command: PASS, exactly 1 test.
- `npm exec tsc -- --noEmit`: PASS.
- `npx eslint tests/e2e/local/three-products.spec.ts --max-warnings 0`: PASS.
- `git diff --check`: PASS.
- No browser/socket/service/body/full run.

## Qualification boundary

The fixture is source-faithful but the Gate 5 body is still pending D13. The production handoff currently calls `appendDocument` without known gesture reads (`src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:188-190`); the outbox consequently emits an omitted `reads` field and atomic fallback (`src/tools/video-editor/commands/localSaveSession.ts:162-169`). The real provider makes that whole-parent scope and rejects an overlapping Agent publication as `atomic_scope_changed` (`_commit_patch.py:246-247,448-459,783-787`). Because Gate 5's C edit is deliberately in the same parent and the plan requires `merged`, no test-only workaround was introduced. D13 must add faithful production caller reads before body qualification.
