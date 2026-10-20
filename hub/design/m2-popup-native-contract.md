# M2 popup native contract — staged Agent source, official Runtime generation required

Worker: `agt-m2-popup-media-recover`, worktree
`/home/user/work/wt/agt-m2-popup-media-recover`, base
`2f77310e6e4a6920f993a1c9c0093cd71b133543`.
M2 integration remains HELD until PLAN records M1. Frozen Bundle1 refs are unchanged.
These are executable Agent captures and goldens, **not an official paired release
or a qualified App handoff**. Real Runtime9f9b25c rejects the new asset guard key
at its normal PreparedCommit schema boundary. Runtime owns normal artifact/root
schema generation; no provider validator bypass or local schema override is used.

## Exact operations and args

Both use `schema_version:1`, `version:"1"`, and exactly
`intent:{"ownership":"occurrence"}`. No shared, placement or registry-upsert op.

* `occurrence.add-media`: `select:"occurrence:<raw occurrence ID>"`,
  `args:{"row":<raw child clip>,"media":<MediaSelection>}`.
  Row requires `id`, `clipType`, `track`, `at`, `hold`; `asset` must equal
  `media.asset`. `row.id` is reserved once by the caller before capture. The
  immutable selection's `asset` is the registry alias, fixed before capture,
  never regenerated or silently renamed on retry/collision.
* `occurrence.swap-media`:
  `select:"occurrence:<raw occurrence ID>/clip:<raw child ID>"`,
  `args:{"old_media":<MediaSelection>,"media":<MediaSelection>}`.
  The existing child supplies its raw track, local timing and old registry alias.
  Only its asset property changes; all authored opaque/null fields stay intact.
  `${occurrenceId}:${clipId}` is a projected display ID, not the raw child ID.

`MediaSelection` is the existing closed, immutable five-field value:
`{asset,generation_id,variant_id,object_id,catalog_digest}`. Both digests use
`sha256:<64 lowercase hex>`; IDs are nonempty strings. No caller intrinsic
metadata, acquisition or new media port is accepted.

For example a video ADD row can be:

```json
{"id":"reserved-child","clipType":"video","asset":"reserved-new","track":"picture","at":0.125,"hold":4,"from":2,"to":6,"speed":2,"params":null,"opaque":[null,false,{}]}
```

Timing is unprojected child-relative seconds. `hold` is SOURCE seconds;
`[from,to)` must equal that source hold. Playback duration is `hold/speed`.
Positive finite noninteger speeds work; negative, zero and boolean speeds refuse.
An occurrence starting globally at 8 seconds keeps this child at 0.125, not 8.125.
The raw child interval must fit `[0, occurrence.duration_ms/1000)`; an equal end
is allowed. Video window end may equal verified intrinsic duration. Parent and
child fps must match, including exact rational fps; no authoring-time rounding.
Images require positive hold, no from/to and default speed.

## Capture exports, schema and portable golden

```python
from astrid.sdk.timeline.native_occurrence_media_commands import (
    capture_occurrence_add_media,
    capture_occurrence_swap_media,
)

add = capture_occurrence_add_media(bundle, owner, row, media,
                                   verified_media=verified_media)
swap = capture_occurrence_swap_media(bundle, raw_child_ref, old_media, media,
                                     verified_media=verified_media)
```

Both run the actual deterministic handler/recorder and return one complete
EditCommand with original reads, selections, bindings, created, expect,
authorship and resolved claims. Replay verifies those exact claims.
`verified_media` contains detached existing `VerifiedMedia` responses, not a
second authority mechanism: production `RuntimeCommitService` validates the
command args then calls the existing ABI1 `port.selected_media(pin)` outside
pure execution, passing exact responses into execution/server replay. The
existing 9ebd87af `_verified` helper is reused as `_media_inputs.py`.

Canonical schema:
`/home/user/work/wt/agt-m2-popup-media-recover/astrid/core/timeline/schema/edit-command.schema.json`.
Raw file SHA256:
`8b48748f9220e4b79dce4ad1ccb8b9e9f28b314fc96f71f34d6fec7de4ab480f`.
Exports: `OccurrenceAddMediaArgs`, `OccurrenceSwapMediaArgs`, `MediaSelection`.
The ordinary leaf source extends ScopedId/EntityRef/TargetKey/AnchorIdentity
with scoped `asset` references; existing AgentCreatedID fields remain unchanged.
Managers must compose this source with foundation before normal Runtime root
export/generation; this hash is this worker's source, not the foundation bundle hash.

Exact golden:
`/home/user/work/wt/agt-m2-popup-media-recover/tests/editing_conformance/fixtures/recipe_m2_occurrence_media.json`.
It has `add` and `swap` cases, each containing exact `input`, `verified_media`,
`commands`, `records`, and `output`. Both use rational 30000/1001 fps, nonzero
occurrence start, nonzero raw child start and video from/to/speed, shared source
occurrences, opaque/null values and a NEW object absent from the original manifest.
Goldens assert byte-for-byte JSON structure after normal decoding and exact
recorder equality. They do not pretend portable fixture media is real authority.

## Registry birth, guards, inverse and identity retirement

Missing new alias creates exactly:
`{media_id:media.object_id,type:<image|video>,generationId:media.generation_id,variantId:media.variant_id}`.
An existing new alias must equal that complete binding or refuse, including
extra/null keys. Existing old aliases are read and checked against verified
old identity/type/generation/variant while preserving opaque legacy fields;
unsupported identity/source-locator codecs refuse.

`Recording.create_asset` records an ordinary whole-entity write and
`{ref:"occurrence:ID/asset:ALIAS",kind:"asset",owner:"occurrence:ID"}` birth.
It does not append caller invented facts or add a DTO/history table/ABI.
Reads cover raw occurrence/shot ownership, placement map, duration, fps, source
window, raw child track and registry bindings; selections cover occurrence,
track and child membership/order as consumed. ADD records the created child too.

The generalized inverse checks alias dependents after reversing its consumers.
Local asset/asset_id and explicit scoped asset_ref/owner_ref edges prevent
removal, including references from another occurrence or shot payload. Overlap
normalizes asset references to their owner/source registry leaf, so an intervening
same-value registry write still blocks undo. Reservation scans include implicit
registry identities and accepted births: a fresh request cannot reuse a retired
alias; authenticated redo of its own history can restore it. No standalone upsert.

The inherited 2f77310e provider-only `document_from_bundle(...,
inverse_records=AcceptedRecords(...))` manifest hook remains unchanged. Only
introduced pins proven by authenticated boundaries are removed. Original
unselected pins and later disjoint media stay; surviving media/document
references refuse. Detached captures alone cannot authorize pin removal.

## Explicit refusal scope and qualification

Only active image/video raw children on active visual output child tracks;
only existing, explicit occurrence owners with translation-only placement maps
(source_offset absent/0, occurrence speed absent/1). Nondefault/rational-object
occurrence maps, internal source_window, anchors/relations, transitions, alternate
timing codecs, mismatched/missing inputs, registry collisions, parent/display
selectors, shared intent and out-of-occurrence intervals refuse. Existing opaque
params and app data are preserved. This slice does not implement placement,
relational timeline_frame/end_frame, registry-container creation or implicit shared
writes. Pack custody and producer guard changes remain on their agreed separate
owners/seams; nothing here changes them.

The native detached suite proves exact capture, compile/reload inverse/redo,
shared-occurrence isolation, deterministic replay, disjoint rebase, source-unit
hold with noninteger speed, half-open bounds, scoped asset dependencies and
retired-ID refusal. Real managed generations/public media-selection reads and
the production provider reach normal Runtime acceptance; positive preview is
currently refused at PreparedCommit's old TargetKey asset pattern. Strict xfails
retain acceptance/reload/restart/exact retry/changed-key/undo/redo and lifecycle
race expectations. Only that exact old schema error qualifies for xfail;
credential revocation already passes normally. No Runtime source/pin was edited.
Final exact commands/counts and central result ID are in the new worker report.

Next: manager composes source -> Runtime performs normal official generation ->
paired artifacts/pin -> rerun the unchanged strict tests and qualify actual App
capture/browser consumption. No positive real popup acceptance is claimed yet.

Manager correction00:58: Runtime MediaReads.selection for the actual App immutable association/object/version read sets asset=variant.id (timeline_commit_port.py449), which is a stable unique variant identity, NOT the output port label. My initial main/video selector assumption above was incorrect. Do NOT add an alias field or widen this contract on that premise. Legacy asset/generation/variant read accepts caller alias but that is distinct from the proven App path; mismatched existing alias refusal is exactly create-or-require policy. Current normal App tuple-derived identity is acceptable pending real repeated-output selection proof. Collection-membership breadth remains review only, not a new contract blocker.
