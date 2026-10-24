# A4 review: PASS

Reviewed candidate `b2a546f535dc9e0fb98d81cc1d5dd5883794a67d` against base `fb27e554a9ba47e58ae4ae617581ec99e8fb6876`.

Candidate tree: `2c79d014780f3e3d67ebbf90f2d04f9f68ed80ba`

Scope was exactly three changed files:

- `useTimelineHistory.ts`
- `useTimelineHistory.test.ts`
- `types/history.ts`

No product edits were made.

## Findings

The TS `historyCommandRunner`, command descriptors, inverse transaction metadata, and runner helpers were removed. Local history now uses the existing snapshot reconstruction path.

The mounted Runtime caller remains guarded:

- `useTimelineState` passes `save.localDocumentSave` as `remoteHistory`.
- `useTimelineHistory` checks `remoteHistoryAvailable`, `canUndo/canRedo`, pending operations, interaction state, and editability.
- It delegates to `remoteHistory.undo()/redo()` and does not fall back to applying a local snapshot when Runtime history is unavailable.
- Runtime handoff still emits guarded `timeline.inverse` operations against publication targets; ancestry, head mismatch, pagination, missing records, undo barriers, and CAS/previous-value validation remain enforced.

Therefore the candidate does not introduce a whole-snapshot overwrite over a moved mounted remote head.

The unchanged remote-boundary tests retain coverage for remote poll boundaries, conflict reload, redo invalidation, upload preservation, and signature-identical echoes. D31 remains unchanged at exactly 397 lines and 40 assertions.

## Assertion migration

- The old runner-backed media swap test constructed and applied a semantic inverse transaction, then asserted successful application and restored media.
- The replacement supplies the existing reconstructed snapshot directly and preserves the restored-media assertion plus history commit behavior.
- The old snapshot-fallback test no longer configures a runner failure; it directly exercises snapshot restoration.
- `commands/media.test.ts` was not changed despite the author summary wording; its semantic media-command coverage remains in place.
- No remote-boundary assertions were changed.

The replacement tests are narrower about semantic command execution, but this is consistent with retiring the TS executor: command semantics remain covered by media command tests, while history behavior tests the supported snapshot path.

## Verification

Exact six-file lane, Node 20, private `TMPDIR`, runner preload, no shared-cache writes:

```text
6 test files passed
95 tests passed
```

Required TypeScript checks:

```text
tsc -p tsconfig.json --noEmit --incremental false
tsc -p tsconfig.app.json --noEmit --incremental false
tsc -p tsconfig.node.json --noEmit --incremental false
```

All passed.

Scoped ESLint with `--max-warnings 0` passed.

`git diff --check` passed.

No full, browser, HTTP, backend, dispatcher, graph, schema, or service suite was run.

## Risks and limits

The local fallback path still reconstructs a whole snapshot when no mounted Runtime history authority exists. That could be stale after external changes in an older/non-Runtime route; this is not introduced by the candidate and is not the mounted production path reviewed here.

`commandHistory` plumbing still exists in `useTimelineState`/`useTimelineCommit`, but it is no longer consumed by `useTimelineHistory`; removing that broader A2-owned plumbing was outside this review scope.

No blockers.