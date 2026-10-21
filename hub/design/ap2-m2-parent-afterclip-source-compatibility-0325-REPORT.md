# App2 parent after-clip source compatibility

## Verdict

**Bounded SOURCE ACK for Agent commit `3b3208c43903b770010de0649691cfa566447822`.**

This ACK covers only the Agent parent-owned after-clip insertion source. It
does not qualify an App caller, Runtime/provider acceptance, generation,
pinning, freeze, publication, activation, or writer retirement. The current
App consumer remains visibly refused until a containing release supplies the
private compatible Agent/Runtime pair. Published014/6ba is not evidence for
this source.

## Exact source identity and wire contract

- Commit: `3b3208c43903b770010de0649691cfa566447822`
- Parent: `a19192ea789a209260da46bfbdd5b616fc7cc4ac`
- Commit tree: `84120e176540fbc2281dcff4b7186ec8ae413274`
- Changed paths: `astrid/sdk/timeline/_recording.py`,
  `astrid/sdk/timeline/commands.py`,
  `astrid/sdk/timeline/native_parent_media_commands.py`, and its focused
  parent-media tests. No schema file changed.
- `astrid/core/timeline/schema/edit-command.schema.json` SHA-256:
  `f44b00983b2d5e8c3f137985baabb8b226fe00e821fed74e66444fa3fbdd3a69`
  (60 definitions; the reviewed union reports 34 operation clauses and 12
  explicit v2 clauses).

The closed operation is the existing `clip.add-media` version `1`:

```json
{
  "schema_version": 1,
  "op": "clip.add-media",
  "version": "1",
  "select": "parent" | "parent/clip:<raw-id>",
  "args": { "row": { "id", "clipType", "track", "at", "hold", "..." },
            "media": { "asset", "generation_id", "variant_id", "object_id", "catalog_digest" } }
}
```

`args` is closed to exactly `row` and `media`. The row requires the five
listed fields and preserves additional JSON fields. The media selection is
closed to the exact five immutable fields. The operation's intention object is
closed and empty. There is **no `afterClipId` wire field and no new argument**:
the after-anchor is carried only by `select: "parent/clip:<raw-id>"`. The
source requires that selector to be a raw parent clip; it does not infer a
display ID, occurrence, lane end, or mutable catalog selection.

## Semantic comparison with Main's prepared duplicate intent

The Agent source matches the intended parent-only behavior, subject to the
consumer mapping below:

- Anchor identity: Agent resolves and records the exact raw
  `parent/clip:<id>` row. Main's current local duplicate helper accepts a
  displayed `clipId` and works from `TimelineData.meta`/rows; that is not a
  sufficient wire identity. A future caller must resolve an exact raw parent
  counterpart and refuse if it cannot.
- Order and insertion: Agent records the complete parent clip membership and
  order, then creates immediately after the captured anchor. Main's
  `buildDuplicateClipEdit` inserts after the action index in the displayed
  row. The outcomes agree for a clean parent projection, but Agent's raw
  collection/order guard is the authoritative behavior.
- Ripple: Agent uses the source row's canonical timeline span
  `max(0.05, clip_timeline_duration(source))` and shifts every later raw clip
  on the same track, including both authored start codecs when present. Other
  tracks are not shifted. This matches Main's current `max(0.05,
  action.end - action.start)` same-row ripple for ordinary duplication.
  App must not precompute the insertion time or peer shifts for the native
  command.
- Source clone and preservation: Agent clones the complete raw anchor row and
  changes only the reserved destination clip ID, selected asset, optional
  effect identity, and derived start codecs. It preserves opaque/unknown row
  data, source-window fields, speed, and other authored values. Main's local
  `cloneClipMeta`/`rowsToConfig` path carries the known projected metadata but
  is not a proof of arbitrary raw/opaque preservation for a new clip. It must
  not be used as the native after-anchor implementation.
- Media authority: The qualified Main duplicate-generation caller retains the
  original five-field `MediaSelection` from preparation and asks Runtime for
  matching verified media. Agent records and guards that exact selection and
  the new raw asset binding. No catalog refresh or inferred selection is
  acceptable. The current `useAddVariantAsGeneration` path does not carry a
  `mediaSelection` and therefore remains the legacy path, not this ACK.
- Ownership: Agent refuses an occurrence-owned lane and requires the source
  and destination to stay on the same raw parent track. Cross-track rows are
  left unchanged. This ACK does not cover free-multi, groups, occurrences, or
  new-track drag behavior; those remain HOME scope.

## Recorded safety behavior

The source records and guards the raw anchor row, its parent track, complete
clip collection membership/order, source asset binding, parent output FPS,
the exact verified destination media selection, and reserved asset/clip IDs.
It records peer reads and writes for later same-track rows, including timing
codecs. The existing guarded replay/inverse machinery therefore refuses a
missing or changed anchor, changed membership/order, changed same-track peer
timing/extent, changed source/media/rate, or occupied created identity. Exact
retry reuses the same command and reserved IDs. Inverse and JSON reload are
covered by the existing source controls; no App-side ABA or inverse logic is
needed beyond retaining the exact command in the durable outbox.

The preceding `timeline.assembled-target` sequence remains the explicit
non-ripple replacement exception and is outside this after-anchor ACK.

## Current App callers and refusal state

Live caller inventory:

- `src/tools/video-editor/hooks/useTimelineCommandsService.ts:474-544`:
  prepared assets with an original `mediaSelection` enter the native parent
  media branch. It currently refuses non-video assets at lines 478-480,
  refuses any local `afterClipId` at lines 481-484, and requires a caller
  target time/track plan at lines 485-507. Those are all deliberate current
  refusal boundaries: Agent after-anchor birth supports verified image or
  video media and derives the destination track/time from the raw anchor; no
  command is emitted today.
- `src/tools/video-editor/components/AstridTimelineEditor.tsx:596-613`:
  duplicate-generation insertion is the qualified intent: it preserves the
  prepared Runtime selection and calls `addClip({ preparedAsset,
  afterClipId })`. It currently reaches the refusal above.
- `src/tools/video-editor/hooks/useAddVariantAsGeneration.ts:87-97`:
  prepared variant insertion calls `addClip({ preparedAsset, afterClipId })`
  without a five-field media selection, so it uses the old local prepared
  duplicate path and is not source-qualified.
- `src/tools/video-editor/hooks/useTimelineCommandsService.ts:547-596`:
  the unqualified prepared branch still calls `applyPreparedMediaCommand`,
  whose `buildDuplicateClipEdit` path is the legacy projected writer. It is
  not a substitute for raw parent capture.
- The ordinary registered-asset path at
  `src/tools/video-editor/hooks/useTimelineCommandsService.ts:612-640` also
  uses the local row mutation and is outside this media-selection source ACK.

## Smallest future App mapping

When the containing private Agent/Runtime source is available, keep the
current refusal until one bounded App change is ready:

1. In the qualified `mediaSelection + afterClipId` branch, resolve the input
   to one exact raw parent anchor `parent/clip:<raw-id>` from the authoring
   bundle. Refuse display-only, occurrence, group, missing, or ambiguous
   mappings. Do not put `afterClipId` into `args`.
2. For this after-anchor branch, allow the Agent-supported verified image or
   video kind and do not require `input.time`, `trackId`, or a target-time
   plan. Reserve one destination clip ID before the producer/verification await and
   retain it in the existing parent-media preparation/outbox basis. Pass a
   minimal requested row carrying that ID, the raw source track, the prepared
   asset alias, and the required row fields. Do not copy projected timing or
   hand-build the ripple.
3. Extend the existing parent-media capture seam by one optional raw-anchor
   value (or an equivalent narrowly named after-anchor capture method), so it
   calls the Agent capture with `after="parent/clip:<raw-id>"`. The Agent
   capture must clone the raw source row, derive the start, insert/ripple, and
   record the guards. The App must retain the original five-field selection
   and call the existing verified-media read once.
4. Build the local preview from the returned Agent result/recorded command,
   submit that exact command through the existing session/outbox, and keep
   the existing preparation-current, lost-ack, retry, reload, inverse, and ABA
   refusals. Do not route this case through `buildDuplicateClipEdit`,
   `applyPreparedMediaCommand`, or a fallback writer.

This is the smallest mapping because it reuses the existing parent-media
session, verified-media read, and outbox; only the raw-anchor capture seam and
the qualified branch need to learn the existing Agent selector carrier.

## Evidence

Agent source controls, run against the committed source with the read-only
shared Python environment:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent:/home/user/work/runtime \
/home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider \
/home/user/work/agent/tests/editing_conformance/test_recipe_m2_parent_media.py -k 'after_'
4 passed, 81 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent:/home/user/work/runtime \
/home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider \
/home/user/work/agent/tests/editing_conformance/test_recipe_m2_parent_media.py
85 passed
```

The first run emitted only two existing unknown-config warnings for `timeout`
and `timeout_method`; neither test run failed. The documented
`/home/user/work/venv-agent/bin/python` was not present on this machine, so
the available read-only environment was used instead.

Current App caller-neighbor controls:

```text
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache \
  src/tools/video-editor/commands/parentClipAddCapture.test.ts \
  src/tools/video-editor/commands/media.test.ts \
  src/tools/video-editor/hooks/useAddVariantAsGeneration.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx
Test Files 5 passed; Tests 47 passed; Duration 8.81s
```

`git diff --check` passed and the App worktree remains clean. No full,
browser, localhost, live-socket, Runtime acceptance, or public release suite
was run.

## Blockers and next steps

No source blocker or Agent mismatch was found. The open item is deliberately
consumer-side: the exact private Agent/Runtime successor must be available,
then App can implement the four-step mapping above and qualify one native
duplicate-generation positive plus reload/lost-ack/retry/undo/ABA and
opaque/cross-track refusal controls. Until then, leave the current
`mediaSelection + afterClipId` branch refused and do not broaden the ACK.
