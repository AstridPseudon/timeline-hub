# Agent film transcript/source-item association recipe

Date: 2026-10-21
Base: current Main014 `6efc81500a0e0688c2bb41e736503f0fc3e04abb`
Scope: Agent source-only design and semantic spike. No schema/registry change,
Runtime/App change, generation, freeze, pin publication, adoption, or endpoint
is made here.

## Result

No existing Main command is a safe carrier for the live App film association.
The smallest bounded next step is one closed, normal-history film command
proposal, named `transcript.associate` below only for this source spike. The
name and schema are **not frozen**. The existing project-document CRUD remains
catalog state, and the existing `project-transcript-host.associate` snapshot
writer remains the App behavior until Agent and Runtime jointly review and
qualify this carrier.

The Agent test spike is
`tests/editing_conformance/test_recipe_film_transcript_association_spike.py`.
It is deliberately test-local: it captures the exact pin, owner and source-item
selection, applies only the association/source collection fields, preserves
opaque and caption data, and exercises pure inverse/rebase/retry/restart and
closed refusal semantics without registering an operation.

## Exact current producer and classification

The live App producer is
`/home/user/work/app/src/tools/video-editor/lib/project-transcript-host.ts`:

| Main/App source | Current behavior | Correct ownership |
| --- | --- | --- |
| `associate(document, assetId, previousItems?)` at lines 600–604 | Verifies selected document media matches the asset; replaces the selected asset's project-transcript source items; appends the selected `{assetId, documentId}` relation; invokes caption/review provenance reconciliation; calls `commitData(next, { save: true, semantic: true })` and waits for the normal save acknowledgement. | One atomic film history edit once a native carrier exists. |
| `projectTranscriptItems()` at `data/typed/projectTranscript.ts:184–208` | Projects each exact document segment into a `SourceFrozenDataItem`: stable segment `id`, source-seconds interval, transcript schema, `sourceArtifactRef.assetId`, adapter provenance, source ID, text, optional speaker/words, document ID and version. | Source-item payload readback, not a text-only binding. |
| `reconcileTranscriptReferences()` at `data/typed/reconcileTranscriptReferences.ts:66–147` | Maps only the existing known legacy/canonical stable IDs; updates generated caption clip IDs/provenance and review keys only when ownership and collision checks prove the mapping. Unrelated text/style/timing/review data remains unchanged. | Same deterministic subroutine inside the atomic association recipe; no new parser or caption authority. |
| `importTranscript`, `write`, `undoSource`, `redoSource`, `promoteSource` | Project transcript document create/update/read/history and draft handling through the repository/document surface. | Catalog/project-document CRUD; not film command history. |
| `replaceTransient()` | Memory-only projection refresh. | Derived state; never accepted history. |

The exact film mutation is therefore the two persisted planes plus the
bounded reconciliation: `transcriptReferences.associations` and
`sourceItemsBySchemaRef[TRANSCRIPT_SCHEMA_REF]`, with the existing config
caption/review references changed only when the existing reconciler proves an
unambiguous stable-ID mapping. It is not equivalent to a clip scalar edit.

## Existing carriers checked

1. `text-binding.set` (`astrid/sdk/timeline/commands.py:61`,
   `native_text_binding.py`) is occurrence-owned immutable text descriptor
   state. Its closed args are `{binding, text|clear}` and its rows live in an
   occurrence shot's `payload.text_bindings`. It cannot select a project
   transcript document, replace `itemsBySchemaRef`, or carry source segment and
   word collection membership/order.

2. `clip.anchor` (`commands.py:63`, `native_word_anchor.py`) is a parent clip
   `on`/`until` relation. Its `WordAnchor` carries one exact transcript
   `DocumentPin`, one source occurrence/clip, and stable `word_ids`; it does not
   associate a transcript with a film asset or replace source items. Its exact
   source pin is useful precedent for this proposal, not a substitute carrier.

3. App `project-data.write` is the existing generic patch carrier in
   `/home/user/work/app/src/tools/video-editor/commands/projectDataMember.ts`.
   It is closed to `select: "parent"` and writes exactly
   `parent.config.app[extension][key]`, with replace/merge validation and
   extension size limits. It is appropriate for extension/catalog data and
   source-map entries; it is not a transcript reference or source-item plane.
   The App patch vocabulary lists it in `src/sdk/video/timeline/patch.ts:17–61`,
   but that does not make it an Agent Main operation or a film association.

The current Main closed EditCommand union is exactly the 29 operations asserted
by `tests/sdk/test_timeline_current_union_schema.py:178–188`:

```text
text-binding.set, clip.swap-media, occurrence.create, clip.add,
clip.add-media, clip.anchor, clip.delete, clip.move, clip.set,
clip.set-element, clip.set-params, clip.split, clip.trim,
occurrence.add-media, occurrence.delete, occurrence.duplicate,
occurrence.swap-media, placement.create, placement.move, placement.unplace,
producer.guard, shot.pool, shot.set, timeline.assembled-target, timeline.init,
timeline.inverse, timeline.restore, track.create, track.set
```

There is no `transcript.associate`, source-item replacement, or
`project-data.write` in this union. `DocumentPin` already exists as the exact
three-field `{document_id, version, content_digest}` definition and should be
reused; it must not be widened with an App-only authority field.

## Proposed closed command/readback map (source-only)

The following is the smallest semantic shape for peer review, not an admitted
command. It uses existing normal EditCommand history, provider hydration and
the existing exact `transcript_source(DocumentPin)` read. It does not add a
store, endpoint, DTO family, parser, or second source authority.

```json
{
  "schema_version": 1,
  "op": "transcript.associate",
  "version": "1",
  "select": "parent/asset:asset-a",
  "args": {
    "asset_id": "asset-a",
    "media_id": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "source_id": "source-1",
    "previous_document": {
      "document_id": "transcript:<exact prior document id>",
      "version": 1,
      "content_digest": "sha256:<digest of exact prior verified content>"
    },
    "document": {
      "document_id": "transcript:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "version": 2,
      "content_digest": "sha256:<digest of exact verified content>"
    },
    "source_schema_ref": "astrid.transcript_segment/v1"
  }
}
```

The exact raw owner identity is the tuple
`(asset_id, media_id, source_id)`. The exact raw source-item identity is the
tuple `(schema_ref, sourceArtifactRef.assetId, payload.sourceId, item.id)`;
`payload.segmentId` must equal the stable segment identity and each
`payload.words[].id` is a stable word identity. No array position, displayed
text, regenerated ID, latest-document lookup, or asset-name heuristic may
resolve any of these identities.

When the selected asset already has an association, `previous_document` is
required and is captured as an exact prior `DocumentPin` plus its verified
content through the same existing normal source-read seam. The association
record stores only a document ID today, so the handler must refuse replacement
if that prior pin/content cannot be supplied; it must not reconstruct a digest
from source items or query mutable latest catalog state. For an unassociated
asset, `previous_document` is absent and the old association is an explicit
absence claim.

The handler reads the exact verified document content behind the pin and
records the following claims before writing:

| Claim | Required exact capture |
| --- | --- |
| owner | `parent/asset:asset-a` exists; registry/media identity is exactly `asset-a` → `media_id`; document content media ID equals it; source ID is the declared exact source ID. |
| document dependency | The new and, when replacing, prior exact `DocumentPin` plus verified transcript content; `document_id`, version, digest, project scope, transcript schema, media ID and source ID all match. Missing, revoked, corrupt or mutable-latest-only content refuses. |
| old association | Complete tagged value of `parent.transcriptReferences`, including absence/null distinction, association membership and order. Duplicate asset ownership is ambiguous and refuses. |
| old source collection | Complete ordered `parent.sourceItemsBySchemaRef["astrid.transcript_segment/v1"]` membership, each item's raw owner/source ID/item ID, envelope, extent, payload, words, provenance and opaque values. Duplicate `(asset, source, item.id)` identity refuses. |
| caption/review basis | The exact generated-caption rows and review records consumed by the existing `reconcileTranscriptReferences()` routine, including provenance, ownership evidence and occupied destination IDs. Ambiguous mappings do not guess or normalize. |

The accepted readback writes only these bounded planes:

```text
parent.transcriptReferences.associations
  = all prior associations except asset-a, then
    { assetId: asset-a, documentId: pin.document_id }

parent.sourceItemsBySchemaRef[TRANSCRIPT_SCHEMA_REF]
  = all prior items except the exact project-transcript rows selected by
    asset-a / source-1, then the exact ordered projection of the verified
    document's segments and words

parent.config
  = unchanged except for the exact generated-caption/review provenance
    changes returned by the existing deterministic reconciler
```

The source collection replacement preserves unrelated items, item order among
retained rows, all incoming document order, opaque payload/envelope fields,
stable segment/word IDs, and caption provenance. It is one atomic command: no
association-only write followed by a source-item write, and no whole-parent
snapshot replacement. Project document create/update remains outside this
command and is never smuggled into its history.

The semantic record must expose the existing framework facts, not a second
receipt format:

```text
reads:       owner/media and exact old association/source/caption state
selections:  old source-item membership and order, plus provenance candidates
bindings:    raw owner tuple and every stable segment/word identity
dependencies: {kind: "transcript", pin: new DocumentPin, policy: "exact"};
             plus prior DocumentPin/content when replacing an association
writes:      tagged before/after association, source collection, and any
             reconciler caption/review writes (including unchanged writes)
created:     []
```

Inverse restores the exact prior association and its prior `DocumentPin`, collection membership/order,
opaque envelopes and caption/review provenance. It retains the old and new
DocumentPins through the accepted dependency closure so undo after a source
document update/removal/restart does not read mutable latest state. The normal
inverse ancestry/intervening-write rule rejects A→B→A, including equal final
values. Redo is a fresh guarded replay of the accepted inverse.

Server rebase replays the original stable owner/item bindings against a newer
head. An unrelated film edit passes and remains in the result; any changed
association, source collection membership/order, owner/media/source identity,
stable segment/word identity, or consumed caption provenance conflicts. Exact
retry reuses the original command bytes, pin and idempotency identity; it does
not reselect a document or regenerate source items after restart.

Refuse atomically before writes for mismatched media/document source, missing
or corrupt exact pin/content, duplicate or ambiguous owner/source-item/segment/
word identity, unsupported envelope shape, changed guards, occupied caption
destination IDs, or any attempted normalization/whole-parent fallback.

## Source spike evidence

The test-only spike uses a real `DocumentPin`-shaped exact source with two
stable segments and three stable words, an unrelated retained source item,
opaque item payloads, generated-caption provenance and review provenance. It
asserts:

- exact owner/pin/source-item membership and order readback;
- no mutation of the input fixture;
- opaque and caption/review values survive unchanged;
- independent opaque rebase, exact inverse and redo;
- exact command/pin retry and pin retention through a simulated restart cache
  loss;
- refusal without mutation for digest, media, duplicate segment, duplicate
  word, and duplicate existing source-item damage; and
- explicit A→B→A inverse refusal.

This is semantic evidence only. It does not prove Runtime hydration,
accepted-history retention, App wiring, restart durability, or generated-schema
compatibility.

## Smallest peer review request

Agent/Runtime should review one question before any schema or generated-client
work:

> Can the existing normal `/v1` EditCommand/provider path admit one bounded
> `transcript.associate` handler selected by `parent/asset:<id>`, reusing
> new and prior `DocumentPin` values and `transcript_source(DocumentPin)`, while recording the
> complete association/source-item selection and applying the existing
> `reconcileTranscriptReferences()` result atomically with exact inverse,
> server rebase, retry and retained-pin behavior?

Runtime review should specifically confirm that its existing accepted closure
can retain/read the exact old and new transcript source content for inverse and
restart, without a new endpoint, store, DTO family, or mutable latest read.
Agent review should confirm the raw owner/item reference spelling and whether
the current state recorder can address the two source planes without a
whole-parent `timeline.restore`. If either answer is no, return the smallest
existing provider/recording seam that is missing; do not broaden the proposal
or alter App assertions in this source task.

## Evidence

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_film_transcript_association_spike.py \
  tests/sdk/test_timeline_current_union_schema.py
=> 42 passed in 146.70s
```

The prior App source report's targeted App tests remain the existing evidence;
this task did not alter App files or rerun App assertions. No full, live,
browser, socket, render, broad-matrix, Runtime, or generated-contract suite
was run. No production command/schema/registry or App/Runtime behavior is
claimed as qualified by this report.
