# Track reorder capture parity repair

## Result

Repaired the two exact dormant capture-contract defects from the prior review:

- `parent/collection:track` now records the Agent collection read shape:
  `present({config: present({}), members: present([])})`.
- The non-singleton `track.reorder@1` capture now records `resolved: []`.

The focused App test now compares the complete captured command with the real
frozen Agent SDK capture for the same three-track media fixture. The complete
record matches for args, `resolved`, reads, selections, expectation,
authorship, bindings, and created IDs. Existing row/order/identity/raw-value,
same-order write, stale-order, and refusal assertions were preserved.

## Exact references and parity evidence

- Frozen Agent commit: `c1ae9e93d31c1c091b93c952ae803059a890bf61`
- Frozen Agent tree: `a54be6e2269e191c032496b3b73cfcf761d7402e`
- App reviewed base commit: `1611384358c846ac42b98c38c7f9a6e447d17b77`
- App reviewed base tree: `798534e22841e4ba3ea64948a394b6bb9782df3e`

I executed the frozen Agent SDK capture from the exact commit using its
committed `media_track_bundle` fixture shape. Its record was:

- `args.expected_order`: `picture, audio, overlay`
- `args.order`: `overlay, picture, audio`
- `resolved`: `[]`
- collection read: `parent/collection:track`, path `[]`, state present with
  `config` present `{}` and `members` present `[]`
- selection: complete ordered parent track membership with
  `guard-membership`
- expectation: present original `parent::track_order`
- direct authorship for `parent::track_order`
- `bindings: {}`, `created: []`

The App complete-record assertion passes against those exact values.

## Live callers

None. A repository search found no callers outside the dormant helper and its
focused test for `captureTrackReorder`, `finishTrackReorder`,
`executeTrackReorder`, or `track.reorder`. No session, Provider, serializer,
DTO, generated type, pin, API, or activation path changed.

## Tests and checks

Passed:

```text
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/trackReorderCapture.test.ts \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts
2 files passed; 36 tests passed

node_modules/.bin/eslint \
  src/tools/video-editor/commands/trackReorderCapture.ts \
  src/tools/video-editor/commands/trackReorderCapture.test.ts \
  --report-unused-disable-directives --max-warnings 0
passed

git diff --check
passed
```

Typecheck was run:

```text
node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

It exited 2 on existing integration errors in generated health types,
Composition exports, and unrelated App files. It reported no diagnostics for
either touched track-reorder file.

No full suite, browser, localhost/socket test, install, generated artifact,
Runtime acceptance, or live consumer gate was run. A separate direct `tsx`
probe was not usable because the sandbox denied `tsx`'s temporary IPC pipe
before code execution; the frozen Agent capture and the passing complete-record
App assertion provide the parity evidence instead.

## Changes and decisions

Only these files changed:

- `src/tools/video-editor/commands/trackReorderCapture.ts`
- `src/tools/video-editor/commands/trackReorderCapture.test.ts`

I followed the prior review exactly and did not infer or alter any other
recorded claim. The separate HOME status file was not present in the provided
orchestration tree; the available App2 `STATUS.md` and `INBOX.md` were read.

## Next step

Re-review this repaired dormant source against the frozen Agent record before
any future generation, pinning, activation, or live consumer work.
