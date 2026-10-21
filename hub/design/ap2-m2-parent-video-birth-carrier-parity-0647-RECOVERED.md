# AP2-M2 parent video birth carrier parity

## Decision

**Equivalent for the requested normal newborn row.** Published014 already has
the required carrier: `clip.add-media` v1 preserves a complete row and its
schema requires `id`, `clipType`, `track`, `at`, and positive `hold`, while
allowing the source-window fields as additional row data. Agent's parent
handler then requires a positive hold and requires `to - from === hold` for a
video row.

No product edit or actual was made. The smallest shared-service proposal for
HOME is below; it must be applied only in the prepared-video newborn branch,
after the detached clone at
`src/tools/video-editor/hooks/useTimelineCommandsService.ts:534` and before
`port.capture`:

```ts
const row = structuredClone(clip) as unknown as Record<string, JSON>;
if (row.clipType === 'media' && row.hold === undefined && row.speed === 1
  && typeof row.from === 'number' && Number.isFinite(row.from)
  && typeof row.to === 'number' && Number.isFinite(row.to)
  && row.to > row.from) {
  row.hold = row.to - row.from;
}
```

This is newborn construction, not existing-row repair. It adds a number only
when the generated row has an absent hold, finite source endpoints, positive
window, and the normal generated speed of one. A present `null` hold remains
`null`; speed other than one, nonfinite values, and zero/negative windows are
not normalized. Unknown authored fields remain in the clone. The proposed
field is exactly the source-window length, so Main's `hold` precedence produces
the same duration while `from`/`to` remain unchanged.

## Compact executable witness

I created a temporary Vitest witness, ran it, and removed it afterwards. It
used `buildTimelineData` plus `applyPreparedMediaCommand`, then called the
official App `captureParentClipAddMedia` with the generated row and with the
minimal carrier. The generated row on App tree `acb582c2c3b08481d43853b8526894ac60d074bc`
was:

```json
{"id":"clip-0","asset":"asset-new","at":1.2667,"clipType":"media","from":0,"speed":1,"to":5,"track":"V1","opacity":1,"volume":1}
```

It has no own `hold` property. The carrier was the same object plus
`"hold":5`. Results:

| row | Main start | Main duration | authored hold | source window |
|---|---:|---:|---:|---|
| generated | frame 38 | 5.0 s | absent | 0..5 |
| carrier | frame 38 | 5.0 s | 5 | 0..5 |

The raw row is refused at App capture because the direct parent path does not
use the after-anchor raw-window exception. The carrier captures successfully.
The witness also rejected the proposed carrier for speed 2, nonfinite `from`,
and a zero-length window; the direct capture rejected those unsafe variants as
well.

The exact App command for the carrier was:

```json
{
  "schema_version":1,
  "op":"clip.add-media",
  "version":"1",
  "select":"parent",
  "intent":{},
  "args":{"row":{"id":"clip-0","asset":"asset-new","at":1.2667,
    "clipType":"media","from":0,"hold":5,"opacity":1,"speed":1,
    "to":5,"track":"V1","volume":1},"media":"<exact detached selection>"}
}
```

Its captured records were the authoritative direct birth records: binding
`media.track -> parent/track:V1`; created
`parent/asset:asset-new` and `parent/clip:clip-0`; absent expectations for
both; direct authorship for both; and `resolved: []`.

The frozen Agent6ef implementation produced the same command envelope, row,
binding, created IDs, absent expectations, authorship, and empty resolved set
when run against the equivalent minimal parent bundle. Its relevant sources
are `astrid/sdk/timeline/native_parent_media_commands.py:87-94`,
`astrid/sdk/timeline/native_parent_media_commands.py:25-32`,
`astrid/sdk/timeline/native_occurrence_media_commands.py:166-184`, and
`astrid/core/timeline/schema/edit-command.schema.json:790-800,2377-2391`.

## Why Main accepts the carrier

Main's timing path is the current Agent tree
`345085a511d05bc136672de1ff7236f2284bfb84`, also present at Agent6ef:

- `astrid/core/timeline/duration.py:113-142` computes source duration as
  numeric `hold`, otherwise `to - from`, then divides by positive `speed`.
- The upstream reference `docs/reference/timeline-composition-v0.0.6/lib/duration.ts:20-28`
  has the same precedence.
- `astrid/sdk/timeline/_timing_evaluators.py:65-83` applies the same source
  window/hold precedence and speed division.

For the witness, the direct Main duration helpers returned
`[{"start_frame":38,"timeline_duration":5.0,"hold":null,"source":{"from":0,"to":5}},
{"start_frame":38,"timeline_duration":5.0,"hold":5,"source":{"from":0,"to":5}}]`.
The only semantic difference is the authored carrier field itself; it is
acceptable because its value is exactly the preserved source-window length,
and it is added only to a newborn row that otherwise cannot enter published014.

## First-cause path and unchanged callers

The prior report's first cause is confirmed:

1. `timeline-asset-plans.ts:397-405` constructs generated video metadata with
   `from: 0`, `to: duration`, `speed: 1`, and no hold.
2. `timeline-data.ts:367-377` preserves that source-window representation.
3. `useTimelineCommandsService.ts:534-542` clones, captures, verifies, and
   catches the refusal before submit.
4. `commitSession.ts:405-411` calls the direct parent capture, whose
   `parentClipAddCapture.ts:319-321` requires the missing hold.

The live caller chain is unchanged:
`onTimelineDrop -> useExternalDrop.ts -> external-drop-utils.ts ->
useAssetManagement.placePreparedAsset -> createTimelineCommands.addClip ->
useTimelineCommandsService.addClip -> commitSession parentClipAddMediaPort ->
existing outbox`.

The proposed hunk does not alter `useAssetManagement.ts:300-309`,
`commitSession.ts`, the schema/pin/API, Runtime, or any existing-row repair
path. No `useTimelineCommandsService` or `commitSession` change was applied in
this worker.

## HOME regression recipe

Add one direct service-boundary regression for a prepared video with
`from:0`, `to:5`, `speed:1`, no `hold`, and a valid verified selection. Before
the hunk, assert the current failure (`result.ok === false`, `finish` is not
completed, and `submit` has zero calls). After the hunk, assert:

- `capture` receives the detached row with `hold:5`, while `from`, `to`,
  `speed`, and all opaque fields are unchanged;
- `finish` and `submit` each run once;
- the durable command has the exact row and ordinary Agent birth records; and
- existing exact-404, retry, order, opaque, undo, and zero-legacy assertions
  remain unchanged.

Keep companion cases for `hold:null`, speed 2, nonfinite endpoints, and
`to === from`; they must remain visibly refused, not silently repaired.

## Exact sources, trees, and validation

App sources read: `useTimelineCommandsService.ts:532-542`,
`timeline-asset-plans.ts:397-405`, `timeline-data.ts:367-377`,
`commitSession.ts:405-411`, `parentClipAddCapture.ts:315-376`, and
`useAssetManagement.ts:298-313`.

Agent sources read: Agent6ef `capture.py`, native parent/media capture and
schema above, Main compiler timing evaluator, Main duration implementation,
and the upstream v0.0.6 duration reference. Agent6ef is
`6efc81500a0e0688c2bb41e736503f0fc3e04abb`.

Commands and results:

```text
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/__parent_carrier_witness.test.ts
1 file passed, 1 test passed

node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/parentClipAddCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/media.test.ts \
  src/tools/video-editor/lib/timeline-data.test.ts
4 files passed, 104 tests passed

PYTHONPATH=/home/user/work/agent /home/user/work/venv-app2-native/bin/python \
  -c '<direct Main duration witness>'
raw and carrier both returned start_frame=38 and timeline_duration=5.0
```

An attempted full `compile_timing` invocation was not usable in this sandbox:
the Agent import requires unavailable `runtime_protocol`. No install was
performed. No browser, socket, e2e, full suite, or actual was run.
