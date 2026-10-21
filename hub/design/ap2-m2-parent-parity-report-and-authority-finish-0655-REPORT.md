# AP2-M2 parent parity / authority finish

## Result

The unresolved proof is complete. A lossless semantic newborn carrier exists:
the existing `clip.add-media` v1 command can carry the generated video row by
adding `hold = to - from` to the detached newborn row only.

This is not a byte-identical accepted raw row: the original generated row has
no `hold`, and the accepted command necessarily has `hold: 5` because the
published014 parent birth validator requires it. The raw App materialization
is still unchanged: the carrier is added only after the detached clone at
`useTimelineCommandsService.ts:534`, so the generated raw state retains absent
`hold`, `from: 0`, `to: 5`, `speed: 1`, and all opaque fields. Main compiler
output proves both raw and carrier bundles are returned unchanged by the
compiler and have the same exact timing, source window, and speed semantics.

Recovered 0647’s ignored report verbatim from its durable log:
[0647 recovered report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-parent-video-birth-carrier-parity-0647-RECOVERED.md).

No App product source, test, schema, pin, Runtime source, or actual was
changed. The temporary witness was removed; the worktree is clean apart from
the pre-existing ignored shared `node_modules` link.

## Authority and exact comparison

The coherent installed environment was available and used:

```text
venv: /home/user/work/venv-app2-native
PYTHONPATH: /home/user/work/runtime:/home/user/work/wt/agt-pin-6efc8150
Agent: 6efc81500a0e0688c2bb41e736503f0fc3e04abb
Runtime provider source pin: 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
```

The Runtime provider was loaded through its official startup seam, not
bypassed:

```text
PYTHONPATH=/home/user/work/runtime:/home/user/work/wt/agt-pin-6efc8150 \
  /home/user/work/venv-app2-native/bin/python -c \
  'from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider; p=load_timeline_commit_provider("astrid"); print(type(p).__module__+"."+type(p).__name__, p.provider_id, p.interface_version, p.contract_digest)'
=> astrid.sdk.timeline.commit.RuntimeCommitService astrid-v1 1 sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816
```

The temporary App Vitest witness called the official
`captureParentClipAddMedia` and `executeParentClipAddMedia` against the same
minimal parent bundle used by frozen Agent6ef’s
`capture_clip_add_media` and `execute`. Canonical JSON equality was checked
for the complete command, complete record, and complete materialized bundle:

```text
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/__tmp_parent_authority_witness.test.ts
=> 1 file passed, 1 test passed

complete comparison => {"bundle":true,"command":true,"record":true}
```

This comparison included every command record field, not a projection:
`reads`, `selections`, `expect`, `authorship`, `bindings`, `created`,
`resolved`, `dependencies`, `writes`, and `derived_writes`, plus the exact row,
media selection, and materialized parent/config mirrors. The only two-byte
serialized-size difference was object-key order; parsed JSON equality was
true.

Relevant authority paths are App
`src/tools/video-editor/commands/parentClipAddCapture.ts:315-329,461-478`,
Agent6ef
`astrid/sdk/timeline/native_parent_media_commands.py:25-52,87-94`, and
Runtime
`runtime_protocol/timeline_commit_provider.py:55-92`.

## Main timing and acceptance witness

Using the same coherent environment, `compile_timing(TimingInputs(...))` was
run for raw and carrier rows in a valid parent bundle. Both results had:

```text
authored source window: from=0, to=5
speed: 1
duration: 5 seconds
start: 12667/10000 seconds, start_frame=38
end: 62667/10000 seconds, end_frame=188
result.bundle == input: true (raw and carrier)
```

The raw result retained `hold` absent. The carrier result retained only the
new `hold: 5`; `from`, `to`, `speed`, and the rest of the row were unchanged.
This verifies authored-root preservation by the compiler, rather than relying
on visible duration equality alone.

Agent6ef acceptance/capture results for the same rows:

```text
raw (hold absent): CommandError: 'hold' is a required property
carrier (hold=5): accepted; complete command/record/materialized bundle matched App exactly
```

The direct Agent refuser witness preserved the unsafe cases:

```text
hold=null: CommandError: None is not of type 'number'
speed=2 with hold absent: CommandError: 'hold' is a required property
from=Infinity: CommandError: command must be finite JSON
to=from=0: CommandError: 'hold' is a required property
```

The prior 0647 App witness also rejected speed 2, nonfinite `from`, and the
zero-length window; the reused neighbouring App evidence remains 4 files / 104
tests passed. No browser, socket, e2e, full suite, or actual was run.

## Minimal HOME patch and regression recipe (not applied)

Apply only in the prepared-video newborn branch, immediately after the
existing detached clone at
`src/tools/video-editor/hooks/useTimelineCommandsService.ts:534`:

```ts
const row = structuredClone(clip) as unknown as Record<string, JSON>;
if (row.clipType === 'media' && row.hold === undefined && row.speed === 1
  && typeof row.from === 'number' && Number.isFinite(row.from)
  && typeof row.to === 'number' && Number.isFinite(row.to)
  && row.to > row.from) {
  row.hold = row.to - row.from;
}
```

Add one direct service-boundary regression for prepared video
`from:0,to:5,speed:1` with absent `hold` and a valid verified selection:

- before the hunk, `capture`/`finish` refuse and `submit` is not called;
- after the hunk, capture receives a detached row with `hold:5`, while the raw
  source row, `from`, `to`, `speed`, and opaque fields remain unchanged;
- `finish` and `submit` each run once; and
- the durable command has the exact Agent birth records and materializes both
  parent clip mirrors and both registry mirrors.

Keep explicit refusal companions for `hold:null`, speed other than one,
nonfinite endpoints, and zero/negative windows. Do not normalize existing
rows or present `hold` values. Preserve the existing exact-404, retry, order,
opaque, undo, and zero-legacy assertions.

## Sources and prior evidence

- 0641 first-cause report: generated video metadata is `from:0`, `to:duration`,
  `speed:1`, no hold; direct parent capture refuses before outbox submit.
- App generated row: `src/tools/video-editor/lib/timeline-asset-plans.ts:397-405`.
- App source-window materialization:
  `src/tools/video-editor/lib/timeline-data.ts:367-377`.
- App detached capture/await/submit boundary:
  `src/tools/video-editor/hooks/useTimelineCommandsService.ts:474-543`.
- App direct parent validator: `src/tools/video-editor/commands/parentClipAddCapture.ts:319-329`.
- Agent timing precedence: `astrid/sdk/timeline/_timing_evaluators.py:65-83`.
- Agent compiler contract: `astrid/sdk/timeline/compiler.py:114-127`.
- Main duration helpers: `astrid/core/timeline/duration.py`.

Prior targeted evidence reused exactly:

```text
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/parentClipAddCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/media.test.ts \
  src/tools/video-editor/lib/timeline-data.test.ts
=> 4 files passed, 104 tests passed (0647 durable evidence)
```

No product change was authorized or applied in this worker. Recommended next
step: HOME applies the narrow newborn-only carrier hunk and its direct
regression, then obtains the separately authorized actual proof.
