# App2 M2 element overlay capture

## Source result

The App worker added one bounded pure commandbuilder in
`src/tools/video-editor/commands/elementOverlayCapture.ts` and one focused
test file beside it. It emits the verified native literal recipe:

- existing active visual output track: one `clip.add` command;
- explicitly supplied absent destination track: `track.create` followed by
  `clip.add` in one staged batch;
- whole overlay removal: one guarded parent `clip.delete` command.

The builder snapshots the original bundle, reserves no IDs itself, preserves
the complete literal row and opaque fields, records native collection/order,
track, identity, created-ID, mirror, and delete dependency guards, and returns
immutable capture bases. It does not wire a consumer, writer, UI, store, DTO,
pin, generated file, or dependency.

Selected project-pack refs remain visibly gated with
`selected project pack capture requires authoritative Agent schema capture`;
no authority is synthesized from caller metadata or retained JSON.

## Evidence

On the worker tree:

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  src/tools/video-editor/commands/elementCapture.test.ts \
  src/tools/video-editor/commands/clipMoveCapture.test.ts \
  src/tools/video-editor/commands/trackLabelCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/runner.test.ts
```

Result: **6 files, 245 tests passed**.

```text
./node_modules/.bin/eslint src/tools/video-editor/commands/elementOverlayCapture.ts \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  --report-unused-disable-directives --max-warnings 0
```

Result: **passed**.

```text
./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

Result: **passed**.

Actual current-TS command probes were sent to frozen Agent `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3` using the private read-only source archive and venv. Existing-track create + delete and optional-new-track create each had `validate=accepted`, `execute=accepted`, exact command/record/bundle parity. Agent inverse and replay both matched exactly, including a create/delete round trip. No browser, localhost, live socket, or full suite was run locally.

## Remaining family gap

This is source qualification only. The Elements panel/session consumer is still
unwired and the overlay row remains HOLD. Selected-pack create/params still
needs the existing authenticated authority tuple; transitions, animation on an
existing clip, detach-only removal, media-backed overlays, occurrence-owned
overlays, and legacy writer retirement remain outside this worker.
