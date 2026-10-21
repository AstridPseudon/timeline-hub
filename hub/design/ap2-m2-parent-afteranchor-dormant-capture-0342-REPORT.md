# App2 parent after-anchor dormant capture report

## Result

Prepared a dormant, row-local parent after-anchor capture helper in:

- `src/tools/video-editor/commands/parentAfterAnchorCapture.ts`
- `src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts`

The helper uses the existing `clip.add-media@1` carrier with
`select: parent/clip:<raw-id>` and closed `{row, media}` args. It does not add
an `afterClipId` wire field or change the existing prepared-media refusal.

The capture resolves one exact raw parent anchor, derives the cloned row and
rate-aware ripple from that raw row, preserves opaque/source-window fields,
retains the original five-field media selection and verified response, and
records anchor/asset/rate/peer reads, full collection and after-boundary
selections, peer writes, bindings, and created asset/clip IDs. Other-track
rows are not shifted. JSON reload and exact retry retain the reserved IDs.

No live callers changed. No UI, hook, service, session, Provider, generated
DTO, schema, Runtime, pin, activation, or deletion work was performed. The
current `afterClipId` refusal remains byte-identical.

## Evidence

Passed:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts \
  src/tools/video-editor/commands/parentClipAddCapture.test.ts
Test Files 2 passed; Tests 8 passed

./node_modules/.bin/eslint \
  src/tools/video-editor/commands/parentAfterAnchorCapture.ts \
  src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts --max-warnings 0
passed

git diff --check
passed
```

The focused parity witness uses an opaque video anchor with `from=2`, `to=6`,
`hold=4`, `speed=2`, rational `24/1` output FPS, a later same-track peer, and
an untouched other-track peer. It asserts Agent-equivalent clone timing
(`at=3.003`, `at_ms=3003`), same-track ripple (`6 -> 8`), raw selection,
source asset read, peer reads/writes, bindings, and created IDs. It also
rejects occurrence selectors, missing anchors, ambiguous identities, and a
changed media tuple.

The repository TypeScript check was run:

```text
./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

It exits 2 on existing unrelated repository errors (Composition exports,
timeline config types, older command typing, and preview/composition files).
The final output contains no diagnostics for either new file. No full,
browser, HTTP, localhost, live-socket, pin, or adoption suite was run.

## Decisions and next steps

The published App command type is safe for this dormant command: its existing
generic `select` and JSON `args` fields carry the already-published
`clip.add-media@1` shape without a schema bypass. The helper therefore stops at
the source-only seam as directed.

The next step is a separately qualified private Agent/Runtime consumer pair,
followed by one real App producer qualification with reload, lost-ack retry,
undo/redo, and zero-legacy-traffic evidence. This dormant helper has no live
consumer and is not activation evidence.
