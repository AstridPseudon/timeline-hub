# App AP2 M2 ordinary artifact boundary

## Result

The earlier ordinary-family row that called the whole live transcript
association “project-catalog / producer-artifact state” is too coarse. The
current `associate()` path is a mixed transaction and must be split at the
existing storage boundaries:

1. The transcript document is producer/catalog state. Create and correction
   use the existing project-document operations. They do not enter film
   history.
2. The timeline's selected transcript association is an authored source pin.
   It is part of the timeline revision and must travel with the film edit
   path. It cannot be hidden inside a catalog operation.
3. Caption/source-pin reconciliation is also film-path work whenever it
   changes authored clip identity/provenance or materialized caption clips.
   It must be grouped with the association edit so no accepted revision has a
   dangling source pin.
4. A generic persisted data-kind replacement is producer/catalog source state
   only while its current reader remains duration/render/pin neutral. Its
   transient counterpart is local derived state and must never save.

This is a classification and migration recipe only. It does not add an
operation, DTO, store, endpoint, schema, or App implementation.

## Exact current carriers and readers

### Project-owned transcript document: catalog/producer carrier

`ProjectDocumentSurface` already supplies `list`, `get`, `create`, and
versioned `update` (`src/sdk/context.ts:102-110`). Runtime maps these to the
existing `/v1/projects/{project}/documents` list/get/create/PATCH operations
(`src/integrations/runtime/generated.ts:138-141`,
`src/integrations/runtime/client.ts:589-592`). The transcript repository is a
policy wrapper over that surface, preserving the existing kind, deterministic
document ID, project/media/source identity, strict content, and expected
version (`src/tools/video-editor/data/typed/projectTranscript.ts:7-19,
82-119,125-158`).

Use these existing operations for:

- `importTranscript`'s new document (`project-transcript-host.ts:756-825`,
  especially `:808`);
- source corrections, undo, redo, and explicit draft reapply
  (`project-transcript-host.ts:499-599,909-994`), which call repository
  `update`, not timeline save;
- listing/selecting an existing project source and promotion of a local source
  into a project document (`project-transcript-host.ts:710-857`).

The project document is versioned catalog state. Its create/update receipt,
CAS, retry, and conflict handling remain exactly those existing project
operations. Do not request a film-history operation for the document merely
because the old App import flow followed it with a timeline snapshot.

### Timeline association/pin: authored film carrier

The timeline data model carries `transcriptReferences` beside the authored
config and source plane (`src/tools/video-editor/lib/timeline-data.ts:91-125`).
The bundle envelope persists `transcriptReferences` and
`itemsBySchemaRef`, with strict source-item envelopes and loose unknown
top-level fields (`src/tools/video-editor/data/typed/timelineBundle.ts:25-29,
77-106`). Runtime currently embeds the bundle in the parent composition during
the existing head-guarded timeline save (`src/integrations/runtime/dataProvider.ts:891-905,
907-975`).

`associate()` currently:

- replaces the selected asset's `{assetId, documentId}` association;
- calls `reconcileTranscriptReferences()`;
- prepares the source plane while excluding canonical project-transcript
  projections from durable bundle items; and
- calls `commitData(next, {save: true, semantic: true})`
  (`src/tools/video-editor/lib/project-transcript-host.ts:600-652`).

The first bullet is an authored source pin. It selects which immutable
project document the timeline means for that media asset after reload, so it
belongs to the film revision/edit path. It is not catalog CRUD. The migration
must preserve association order and exact IDs; replacing an association must
not silently select by filename, source text, or array position.

### Caption reconciliation: authored film carrier, not catalog-only

`reconcileTranscriptReferences()` is deliberately narrow but writes authored
timeline state. For an unambiguous legacy-to-canonical identity mapping it
renames a generated caption clip and rewrites its generated provenance
`sourceItemId`; it also renames the extension-owned review key
(`src/tools/video-editor/data/typed/reconcileTranscriptReferences.ts:58-146`).
The function explicitly retains caption text, style, timing, review status,
and unrelated extension data (`:61-64`). The identity test proves the clip
identity/provenance and review-key writes while preserving the existing clip
value (`src/tools/video-editor/data/typed/importTranscriptIdentity.test.tsx:210-241`).

Therefore:

- association + any resulting caption source-pin/provenance rewrite is one
  guarded film edit, not a catalog-only write;
- ambiguous/shared identities must retain the current fail-closed behavior;
  do not guess ownership or rewrite by position;
- review-record key movement is extension project-data state, but it must be
  included in the same semantic migration boundary when it is caused by the
  caption source-pin rewrite. It must not be used to claim that the clip
  rewrite was non-film.

The existing dev caption producer is an independent, explicit film edit:
`buildTranscriptCaptionPatch()` computes frame-rounded caption timing and
emits track/clip operations (`src/tools/video-editor/dev/transcript-lane/extension.ts:78-93,
288-476`); `renderTranscriptAsCaptions()` validates and submits it through the
existing `ctx.creative.timeline.apply()` path (`:754-775`). Preserve this
seam. A source-data replacement must not auto-regenerate or silently alter
caption clips; preserve mode remains a no-op for an existing edited caption.
Regenerate/add/remove caption clips are EditCommands through the existing
timeline adapter.

### Timing and read projection: derived, unless authored output is written

Project source items are reconstructed from the immutable document by
`projectTranscriptItems()` (`projectTranscript.ts:184-207`). The panel and
lane read the transient project projection before any duplicate persisted
copy (`transcript-panel-adapter.ts:56-112`). Occurrences are derived by
intersecting source-second extents with each clip's `from`/source duration and
mapping through the existing source-to-timeline time map
(`transcriptProjection.ts:20-81`). Word timing is marked `word`, `outside`,
or `unusable`; it is not authored back into the source or clip.

Text correction is a useful positive: `editTranscriptText()` says it does not
touch timing or occurrence geometry, and segment replacement clears stale word
alignment (`data/typed/editTranscript.ts:23-99`). The host then updates the
project document and reprojects transiently. Existing tests prove two
timelines converge on the correction while the timeline config, head, stable
signature, save, and history remain unchanged (`project-transcript-host.test.ts:325-371`).

Do not promote these derived projections to film edits. Conversely, if a
future reader starts writing rendered caption clips, source pins, clip timing,
or other authored output as part of replacement, that writer crosses the
boundary and must emit a guarded EditCommand batch.

## Persisted data-kind replacement

The current SDK has two explicit channels:

- `DataKindItemsHost.replaceTransient()` validates and replaces an in-memory
  map only; it notifies subscribers and never calls `commitData`
  (`src/tools/video-editor/data-kinds/dataKindItems.ts:34-69`). The transcript
  host uses this for project-document projections and clears it on dispose
  (`project-transcript-host.ts:339-353,675-702`). This is derived/transient,
  not a film edit.
- `replacePersisted()` validates source envelopes, replaces one schema-ref
  collection through `preparePersistedDataKindItems()`, and currently calls
  `commitData(..., {save: true, semantic: true})`
  (`data-kinds/dataKindItems.ts:21-31,43-58`). This is the legacy snapshot
  writer to migrate.

For a generic data kind whose registered reader only paints a duration-neutral
lane, the persisted source collection is immutable producer/catalog artifact
state, not film history. The SDK's own TimelineData contract says data lanes
are evidence/visualization state and are never inputs to duration computation,
`configToRows`, or export scanning (`src/tools/video-editor/lib/timeline-data.ts:109-124`).
The source envelope is opaque to the host except for its declared schema,
shape, domain, source artifact reference, provenance, and order; the bundle
schema must keep unknown envelope fields/opaque payloads and array order
exactly as today (`timelineBundle.ts:77-106`).

Do not route this through the Agent project-data command. The already-assigned
project-data classification targets extension-owned
`parent.config.app[target][key]` entries and their exact key/value inverse;
it is not a carrier for `sourceItemsBySchemaRef` envelopes or
`transcriptReferences` (see the existing handoff
`handoff-ap2-m2-ordinary-projectdata-native-contract.md`). Do not duplicate
that contract here.

Actionable migration:

1. Keep the current `replacePersisted()` positive reachable until the
   artifact/source-plane peer carrier is qualified. Preserve the complete
   collection replacement, schema ownership, opaque payloads, item order,
   explicit empty replacement, and current validation.
2. When Agent/Runtime provide the already-approved artifact/source-plane
   carrier, make App's adapter submit one existing `commands[]`/outbox intent
   for the whole replacement and use the existing local projection. The
   carrier must guard the prior collection and preserve unrelated schema refs;
   this note intentionally does not invent its operation name or wire shape.
3. If a data kind's current reader is changed so replacement itself alters
   rendered captions, authored source pins, clip membership, or timing, split
   that authored output into the existing timeline command path and keep only
   the immutable source replacement in the artifact channel.
4. `replaceTransient()` remains local and must stay off both artifact and film
   history paths.

This is the minimal peer prerequisite for the generic persisted lane: an
existing qualified artifact/source-plane carrier. A new App-only
`project-data.write` mapping, second bundle/store, or guessed DTO would either
lose the current envelope contract or misclassify source data as film history.

## Transcript-specific migration recipe

Apply the following order without changing current positives:

1. Keep `documents.create/update` as the sole producer/catalog owner for
   project transcript content and its version/CAS. Keep local drafts, source
   undo/redo, and conflict retention there.
2. Build one timeline edit for the selected transcript pin, the exact
   timeline-owned association state, and any unambiguous generated-caption
   source-pin/provenance reconciliation. It must preserve all unrelated
   config/app data, caption text/style/timing, review values, source-item
   envelope order, and explicit clears; refuse ambiguous identity mappings.
3. Do not persist canonical project-transcript projections as a second source
   owner. Reconstruct them from the selected document and expose them through
   the existing transient data-kind channel. The existing save helper already
   strips `astrid.projectTranscript` projections from the durable item plane
   (`src/tools/video-editor/data/typed/projectTranscript.ts:209-220`,
   `src/tools/video-editor/hooks/useTimelinePersistence.ts:959-969`).
4. Keep explicit caption materialization/regeneration as the existing timeline
   command producer. It is film-visible and must never be folded into a
   catalog/document operation.
5. Use the Agent project-data operation only for extension-owned review or
   other project-data records that do not themselves mutate captions, pins, or
   timing. If a project-data record is consumed to perform such a mutation,
   the consuming mutation is a separate film command and remains guarded.

This keeps the film-vs-catalog precedent intact: catalog revisions/documents
may advance without accepted film history, while placement, selection, source
pins, captions, and authored timing stay on the EditCommand path.

## Evidence

Bounded existing probe:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/data/typed/importTranscriptIdentity.test.tsx
=> Test Files 1 passed; Tests 6 passed
```

The probe covers canonical association/import, legacy caption/review
reconciliation, repeated preserve-mode import, and ambiguous shared-source
refusal. No product or test files were changed. No full, browser, localhost,
socket, dependency, pin, schema, or Git operation was run.

## Open prerequisite / handoff

The App side is blocked only on the peer-owned artifact/source-plane carrier
for generic `replacePersisted()`; no additional App contract is requested. The
Agent project-data operation already assigned elsewhere must remain separate.
Runtime/Agent should qualify that carrier against exact collection replacement,
opaque/order preservation, explicit clear, guarded inverse/rebase, and atomic
retry before App retires the legacy snapshot writer. The transcript document
CRUD path and the explicit caption EditCommand path already have existing
carriers and need no new endpoint.
