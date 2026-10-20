# Agent occurrence duration carrier

Status: **PRIVATE SOURCE PROPOSAL — peer ACK required before freeze, normal
generation, pin, release, Runtime pairing, or consumer activation.** No Runtime
DTO, endpoint, App writer, generation, pin, or release was changed.

## Exact source and hashes

- Base reviewed full-group source: Agent commit `c0644cf1`; base tree
  `0699f877a4c809005536a80f5956b8051a814ef7`.
- Candidate changed-files digest (sorted path + NUL + bytes):
  `ed5a57a1f72e8efb7266f7fe3290a2081341825792065e2356e15809f6992881`.
- Candidate schema:
  `astrid/core/timeline/schema/edit-command.schema.json`, SHA-256
  `79c54f0ba6ddb1028a90f8e5545ece68a34fa156a3642b14fea550a8f02da0c2`.
  It has 59 definitions and 33 operation clauses. Removing this resize
  definition/clause reconstructs the reviewed group schema hash
  `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`.
- Source file
  `astrid/sdk/timeline/native_occurrence_resize.py`, SHA-256
  `4c249adec1913566fa1ac55f4d403cc895ff06e8a70fdf94c7124bb84627c678`.
- Registry wiring `astrid/sdk/timeline/commands.py`, SHA-256
  `d6172dd2511aed829ed95d4702e431a325503acd488a3ec72bedea5862eee10f`.
- Conformance source
  `tests/editing_conformance/test_recipe_occurrence_resize.py`, SHA-256
  `f67bd1711409e3e1adce9bf1da03c931cc512e089087086465af0e679cab18ad`.
- Schema-floor controls
  `tests/sdk/test_timeline_materialization_schema_union.py`, SHA-256
  `13f0a9127934d4bdc303bd79b41f64b1c12dbb7bd86e70c90ad3da654f441131`.

## Command and units

The proposal adds closed `occurrence.resize@1` with:

```json
{
  "schema_version": 1,
  "op": "occurrence.resize",
  "version": "1",
  "select": "occurrence:<stable-occurrence-id>",
  "args": {"duration_ms": 4150},
  "intent": {"ownership": "occurrence"}
}
```

`duration_ms` is a finite positive integer in authored integer milliseconds,
the same raw field Main stores. The handler writes only
`occurrence.duration_ms`. It does not quantize or rewrite placement starts,
parent extent, child timing, shot data, or opaque fields. Rational fps and
half-open compiler behavior are therefore unchanged by this carrier.

## Guards and refusal behavior

- The selector must be one exact `occurrence:<id>` root; no display ID,
  position, child selector, or guessed owner is accepted.
- The row's `occurrence_id`, `shot_id`, and optional `shot_revision_id` are
  read through the existing recorder. The occurrence collection and
  `placement.owners` selection are recorded; shared ownership refuses with the
  existing materialization-carrier boundary.
- Existing `parent.config.pinnedShotGroups` refuses with the existing
  migration-needed guard. No silent legacy migration is performed.
- Existing occurrence timing codecs in `MAP_FIELDS` are guarded and retained;
  none is replaced. A missing/malformed/non-positive existing duration refuses.
- Schema and handler validation both require a positive integer `duration_ms`;
  invalid values refuse before any write and the capture draft remains intact.
- The recorder supplies direct before/after expectations, inverse/redo, replay,
  and intervening-write/ABA guards. The command never replaces the occurrence
  object, aliases `group.move`, or introduces a Runtime field.

## Evidence

The test uses the existing `tests/packs/video_editing/test_draft_voiceover.py`
fixture and `prepare_draft_voiceover(..., timing_policy="ripple")`: its original
occurrence `o1` is 3000 ms and the prepared result is 4150 ms. Native capture
then targets `occurrence:o1` and proves the same identity, exact one-field
write, retained placement/shot/opaque fields, rational-fps-shaped codecs,
inverse/redo, strict ABA refusal, disjoint opaque/sibling rebase, invalid
integer refusal, and missing-identity draft preservation. The schema controls
preserve the previous ordinary and group floors and assert this as one
additional closed operation.

## Remaining gap

The normal compiler does not author a parent `config.duration` consequence for
this occurrence field write. In the original ripple fixture the legacy
prepared candidate separately changes the following occurrence start, parent
hold, and parent `config.duration` from 6 to 7.15 s; this carrier intentionally
does not invent a root writer or claim those consequences. A separate reviewed
command/batch lowering is required for the complete ripple proposal. Runtime
pairing, native HTTP, generation/pin/release, and App adoption remain open
pending peer ACK and the separate audio/provenance work.
