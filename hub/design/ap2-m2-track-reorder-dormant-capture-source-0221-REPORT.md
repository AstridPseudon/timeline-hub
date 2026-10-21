# Dormant parent track reorder capture

## Result

Added only the dormant row-local capture module and focused test:

- `src/tools/video-editor/commands/trackReorderCapture.ts`
- `src/tools/video-editor/commands/trackReorderCapture.test.ts`

The builder captures the complete raw parent track permutation as
`expected_order`, accepts a complete desired `order`, and emits the existing
`EditCommand` carrier with the Agent `track.reorder@1` shape. It records the
existing read, selection, virtual `parent::track_order` expectation, direct
authorship, and write diagnostics. Preview execution reorders existing raw row
objects without reconstructing them, so opaque values, null/false/zero values,
clips, config siblings, and `config.app.timelineDataLanePlacement` remain
unchanged.

The builder refuses lane-bearing input, malformed/missing/duplicate/foreign
identities, stale order, and changed identities before changing the local
preview. The basis is JSON-round-trippable and keeps the original capture
claims. The generated timeline DTO/types were not changed, and no unsafe cast
was added to production code to bypass them.

## Live callers changed

None. The module is intentionally dormant and is not exported, wired into a
handler, session, Provider, serializer, store, API, pin, generated artifact,
or activation path. Existing `handleMoveTrack` behavior remains unchanged,
including its mixed media/data-lane path.

## Evidence

Passed:

```text
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/trackReorderCapture.test.ts src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts
2 files, 36 tests passed

node_modules/.bin/eslint src/tools/video-editor/commands/trackReorderCapture.ts src/tools/video-editor/commands/trackReorderCapture.test.ts --report-unused-disable-directives --max-warnings 0
exit 0

git diff --check
exit 0
```

The focused test includes one peer-source shape witness against Agent source
`c1ae9e93` / tree `a54be6e2` and existing track-management controls. No matrix,
full, browser, localhost, socket, Runtime, pin, or activation suite was run.

The requested App project type check was run:

```text
node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

It exits 2 because the current integration baseline has unrelated errors in
generated health types, Composition exports, and existing App files. The
output contains no diagnostics for either new track-reorder file after the
fix.

## Decisions and limits

- Used the Agent-ACKed operation spelling and diagnostic carriers exactly; no
  new DTO, command port, API, store field, or generated validator was added.
- Treated a lane-bearing argument as unsupported while preserving any existing
  authored lane-placement data as opaque. This follows the compatibility
  review’s atomic media-only boundary.
- Kept the existing legacy producer live because this task explicitly forbids
  activation, serializer cuts, and fallback deletion.

## Next step

Only after the matching Agent/Runtime generated and provider cohort is
qualified should an App owner add the row-local session/outbox adapter and
its real retry/reload/undo proof. This packet does not claim that activation.
