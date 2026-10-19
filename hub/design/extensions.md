# Timeline extensions and primitives — M0 design

Status: M0 design updated for decided Astra changes, 2026-10-19; Checkpoint A pending, no product implementation.
PLAN §4.2–4.3 governs. [edit-recipe.md](edit-recipe.md) owns command meaning,
recording, validation, rebase, inverse, grouping and transport handoff. This page
adds extension-specific inputs to that contract, not a second edit recipe.
M5 requires the owner's explicit release after M4; its section below is acceptance
criteria only. Before the M4 hard stop, markers and signals are limited to bounded
reference/resolver seams and core fixtures; their broader APIs remain M5 proposals.

## Source baseline and conclusions

Source citations use repository-relative paths plus symbols/line numbers. Agent
main is `e51595c68fc23d3d1734a0885c84a6511999697b` (this worktree); App main is
`60aa26b9529dcfa94f8ffdbd5edf42fa6c1babd2`; Composition is
`c82eb7c459d0a41263954bf007071a6a0e8e0a6a` (the supplied R4 base, **not a
claim that Composition is current main**). `R4:` means Agent frozen ref
`origin/codex/handover-timeline-r4-20261019-candidate-sdk`, resolved to
`11caf1d9de291d76f491cf69f7942606b7471d7a`, read with `git show` in
`/home/user/peteromallet/astrid-agent`. Integration worktrees were read only.

Both proposals are supportable, with necessary changes:

* Generic marker anchors fit the existing pure moment/context/compiler boundary.
  R4 does **not** already support marker identity or safe republication. Numeric
  beat ordinals are discovery syntax, not stable references. A future M5 marker
  proposal can add one generic kind with exact set/item identity and source
  mapping; never add one compiler branch per detector.
* Cut-sheet editing does generalise to projection + parser + command builders.
  The framework must compare the edited projection with its exact exported base
  and its declared editable field/membership surface. A JSON document diff is
  insufficient. Current sheet application contains direct mutations and a local
  three-way merge; these cannot become a second accepted write/rebase path.
* Packaging already exists. Main V3 has `actions`, `ui`, `rendering`, `documents`
  and declared resources. Do not rebuild `astrid/core/extensions/` or introduce
  another loader. V3 deliberately has no top-level `extensions` property.
* Existing App consumers are substantial reusable presentation infrastructure,
  but local `baseVersion` and `TimelineOps.flush().version` are not Runtime
  revision identities. Adapt them to the foundation; do not bless the old writers.

## Existing seams; future M5 registration proposal

`astrid/core/pack/definition.py:PackDefinition` already carries the four V3
sections. `canonical.py:CanonicalPackDefinition.declaration_id` (278–286),
`_normalize_declarations` (464–507), `validate_canonical_pack` and resource validation
own admission, identities and contained source paths. `loader.py:scan_packs`
discovers without importing contribution code; invalid optional packs have a
diagnostic quarantine, while normal source admission remains strict.
`registry.py:ElementKindRegistry.register_many` validates collisions before
replacing registry state. `astrid/core/element/registry.py:ElementRegistry` and
`schema.py:ElementDefinition` already own render element discovery/schema.

The future M5 authoring/registration proposal may use those declarations:

```yaml
schema_version: 3
id: beat_tools
name: Beat tools
version: 1.0.0
actions:
  snap:
    description: Anchor selected clips to selected beats
    invocation: {kind: python, path: actions/snap.py, function: apply}
    inputs: schemas/snap.json
    outputs: {type: object}
    metadata:
      timeline: {api: 1, type: command, version: 1}
```

This is a future M5 **interpretation of an existing metadata slot**, not an
already-working timeline registration API. The extension author supplies the
schema, deterministic handler, applicable intent and fixtures; the framework
generates recorder and registration metadata. No decorator, scaffold or
extension-registration API is implied before M5. V3 `actions.*` permits `metadata`,
JSON-schema inputs/outputs, Python invocation and resources
(`schemas/v3/pack.json`, `properties.actions`). It does not permit arbitrary new
action fields or a root `extensions` map. The Agent timeline host would validate
the nested `metadata.timeline` descriptor, admit its parameter schema and bind
its declared function into the one command registry once M5 is authorized. A
command runs as a pure handler under that registry, not as a side-effecting
executor action.

Views/checks/producers use the same action descriptor with a different `type`;
their host interface determines invocation. View metadata may name a parser
resource/function and edit-surface schema; canonical resource containment must
cover those references. UI adapters use `ui.<key>: {type: editor, entry: ...}`;
visual elements stay `rendering.<id>: {type: element, path: ...}` with their
existing element resource, extended with the typed contract. Reusable curves
are typed element resources, not another top-level category. Static payload
schemas may be declared under `documents`; this does not install a Runtime
validator (`docs/packs/data-storage.md`). Runtime remains the schema/storage
authority for product state. Optional decorators may emit this descriptor in
M5; they must not discover code by executing it or create an extra registry.

In the M5 proposal, every piece has a qualified pack/declaration identity, host API version,
implementation version and admitted source/resource identity. Pack semver,
command implementation version, payload schema version, artifact content
identity, set publication version and accepted timeline revision are separate.
History replays the pinned implementation, never whatever is installed as
"latest". Missing/incompatible handlers refuse the affected operation; other
edits can preserve their opaque data. Duplicate IDs fail admission; aliases are
input conveniences and are normalized before recording. App extension IDs such
as `haus.astrid.scene-phase-markers` need an explicit admission mapping to pack
identities; do not silently reinterpret or rename existing stored keys.

| Type | Future M5 host interface, after admission | Existing owner/seam; needed adaptation |
| --- | --- | --- |
| Command | `apply(authored_context, normalized_params)` under the recipe runner; schema and explicit dependencies are registry metadata | Agent's R4 `commands.py:EditCommand`, `Operation`, runner. Deterministic macros expand to the same ordered command batch with recorded allocations. No nested commit. |
| View | `project(read_context, query, options) -> projection`; optionally `parse(text, base_projection) -> typed edits` consumed by a host command builder | Agent `timeline_views.py`, `timeline_sheet.py`, `cli_show.py`; App panel/overlay hosts. Projection carries revision, producer identity, query/options, reference map, MIME type and editable-surface metadata. Exporters are this interface with artifact output. |
| Element | Typed component/modifier/transition contract or pure reusable curve, schema, explicit animatable leaves and capabilities | Agent element registry + Composition contracts below. App inspectors/renderer registration are adapters. The element cannot modify authored timing during evaluation. |
| Check | `find(read_context, query) -> findings` with revision, check version, code, severity, stable refs, message and optional command proposal | Agent `astrid/sdk/timeline/check.py`, lint/visualize reporting; App diagnostics. Common finding projection/overlay needed. Never called as an advisory save veto. |
| Producer | `run(pinned_inputs, artifact_writer) -> artifacts + optional proposal` | Existing pack executor/task/run/media surfaces; `music.beats`, editorial transcription and Foley actions. Add immutable publication/identity reconciliation and command proposals; no accepted timeline writer in the producer context. |

The host interfaces, declaration shape and future data models in this section are
M5 proposals. Before M4 there is no extension registration or host framework;
only the bounded marker/signal reference-resolver seams and their core fixtures
are prepared. The M5 proposal's `read_context` is an immutable accepted revision plus explicitly pinned media/data
and evaluator versions. A local preview is separately labelled by base revision
and draft identity; it must never masquerade as an accepted revision. Rendering
failure leaves a text projection usable and reports unavailable visual output.
A View presents; a Check judges. Panels, shortcuts and gestures bind commands or
views and do not define a sixth extension type. A producer may store artifacts
without proposing timeline edits.

The future M5 extension golden path is deliberately singular:

| Author's job | Use |
| --- | --- |
| Fast deterministic edit or macro | Command, one recorded batch |
| Slow analysis, import or generation | Producer → immutable artifacts/data and optional proposal |
| Read, compare, plot or export | Revision-pinned View |
| Edit through text or another representation | Editable View → existing Commands |
| Draw/play something in the film | Typed Element |
| Follow events or measured values | Marker anchor for moments; signal binding for curves |
| Hand-author an animation shape | Reusable authored curve/keyframes |
| Diagnose and suggest a repair | Check → finding + optional command proposal |
| Attach owned information | Versioned namespaced data at the appropriate scope |

For acceptance/rebase, proposals and editable-view envelopes also retain the
recipe's exact **base revision + base publication** pair. Content-only views can
be keyed by revision; same-value publications still matter to guarded editing.
Use the recipe's canonical DTO names, not new extension-specific commit fields.

## Marker reference/resolver seam and future M5 publication proposal

R4 `astrid/core/timeline/moments.py:Moment` (47–62), `Context` (79–88),
`parse`/`format_moment` (93–213), `resolve` (288–340) are a pure grammar/context
seam. Exact clip anchors use scoped authored IDs; exact `source-word` carries
document, lineage, revision, clip occurrence, snapshot digest and word ID.
`R4:astrid/sdk/timeline/model.py:_MomentContext` maps beats through source in,
clip placement and speed (1492–1509), and recursively resolves clip edges
(1511 onward). `R4:compiler.py:_validate_dependencies.references.visit`
(119–168) handles cut, clip, word and beat edges; beat dependencies explicitly
include the music owner's boundaries. `compile_timing` (385 onward) runs
detached `_timing_evaluators`, with cycle refusal before adoption.

Before M4, the only marker behavior is a bounded resolver seam such as
`resolve_marker(ref, pinned_marker_table, occurrence/time_map) -> moment + dependencies | unavailable`
and deterministic core fixtures for present, missing, ambiguous and out-of-range
references. It consumes pinned immutable content supplied by Runtime; it does not
run a detector, publish or reconcile a set, load a pack, or read a mutable source.
The resolver returns unavailable for a missing referenced marker. Any eventual
republication must fail closed: refuse it atomically, with the prior selected
publication, bindings and authored/materialized state unchanged.
There is no retained materialization or unresolved marker state in the foundation.

The following immutable `MarkerSetPublication` and related data model are a future
M5 proposal, referenced from authored state by an ordinary command:

* Stable set identity: project + publishing namespace + logical set ID + source
  lineage. Display names (`beats`, `downbeats`, `scene changes`) are labels.
* Publication identity/version: exact immutable artifact ref, payload schema,
  producer implementation, pinned input media/document revision and content
  identity. A publication contains items keyed by stable opaque marker IDs and
  deterministic display order. Each item is a **moment**, with rational time
  coordinates and a declared coordinate domain, plus opaque namespaced payload.
* `MarkerRef`: exact set identity + marker ID + placement/occurrence identity
  when source coordinates need projection. A binding records the publication it
  selected, mapping identity and the recipe's follow/fixed policy. A follow ref
  resolves against that set's publication selected by the accepted timeline
  revision; it never reads a mutable producer head during compilation. A fixed
  ref stores its resolved position plus provenance and does not follow updates.

The future M5 compiler integration needs `marker(ref) -> time/dependencies` on the
moment context and one generic `marker` parse/format/resolve/dependency case. The exact text spelling
should serialize the typed ref without ambiguous names, as `source-word` does;
the JSON/schema is canonical. Beat/downbeat aliases remain readable, but a
command selecting a beat binds the exact marker rather than re-running an
ordinal or nearest-time search on replay. Old numeric beat arrays have no stable
IDs: retain their legacy evaluation and all existing films' read/playback
semantics; any later conversion must be explicit, allocate IDs once and record
the conversion. Do not claim identity continuity retroactively.

The future M5 compilation path receives validated, pinned marker tables; it does not load packs,
perform analysis, query Documents, or read files. Timeline-domain markers are
constant inputs. Source-domain markers map through the **exact** occurrence and
explicit time map, retaining source identity even if trimmed out. Source trim,
speed, loop, split and music arrangement dependencies must enter the dependency
graph, including segment/branch identity where a map is not one-to-one. An
ambiguous placement conflicts instead of choosing the first occurrence. An
out-of-range point is unavailable in that occurrence, not clamped to its edge.
Half-open windows prevent double-counting boundaries. The generic implementation
must preserve rational fps rather than copying R4's float-only `Context.fps`.
The recipe/Runtime provider currently exposes exact revision closures and media
selections, not a marker-specific port method. M5 publication data must be part
of that pinned closure or an agreed immutable artifact read; an unsupported
artifact cannot trigger an undeclared filesystem/network read from a handler.

**Stable republication is a future M5 producer responsibility.** Producer event correspondence is not commit `id_map`; the foundation commit map is identity-only until a concrete supported command requires more. A second publication
retains IDs only for reconciled same events in the same source lineage. It
supplies an injective old-to-new identity correspondence where necessary, with
new IDs for inserted events and retained deletion/tombstone knowledge. Never
derive IDs from ordinal, timestamp or detector confidence. Never reuse a deleted
ID for a different beat. Ambiguous re-detection produces an unresolved mapping
or a separately named set for review; nearest-neighbour matching alone is not a
core guarantee. Switching source lineage requires an explicit rebind proposal.

Accepting the new publication pointer and associated authored changes is one
atomic M5 command batch. Following clips then recompile in the same accepted
revision. Undo restores the old selected publication and authored bindings and
recompiles; artifacts remain immutable. A missing referenced ID is a hard
validation failure: refuse the whole republication atomically and leave the prior
selected publication, bindings and authored/materialized state intact. It never
silently retargets or substitutes a previous position. Creating a new binding to a
missing ID is invalid. Structural corruption, cross-project references, or an
introduced dependency cycle refuse the whole batch. This is core validity, not an
advisory-check exemption.

R4 already preserves lost word spans (`_timing_evaluators.py:retime`, 472 onward)
and refuses cycles (`tests/sdk/test_timing_cycles.py`,
`test_beat_source_can_form_a_cycle_with_a_cut`,
`test_cycle_refusal_keeps_inputs_state_and_commands_immutable`). These support
the design direction; the existing source-word behavior is retained for legacy
playback and does not define missing-marker handling. None tests the new marker
kind. The M0 probe demonstrates
the actual ordinal hazard: `[1,2,3]` makes `beat 2 after c1` resolve to `2`;
re-detection `[0.5,1.05,2.05,3.05]` resolves it to `1.05`, not the surviving
second event at `2.05`. This is evidence that an adapter preserving only beat
times cannot meet PLAN's stable-ID requirement.

## Signal reference/resolver seam and future M5 binding proposal

The signal publication, sampling and element-binding model below is a future M5
proposal. Before M4, the only signal work is a bounded `SignalRef`/resolver seam
over pinned immutable content plus core fixtures for pin validation, missing data,
domain mapping and out-of-range behavior. Generalized signal binding, sampling
orchestration and detector publication are M5/later; no pre-stop signal host is
implied.

A marker denotes an event at a moment. A signal denotes a typed value over a
domain: source identity/lineage, immutable publication, coordinate domain,
units/value shape, sample/interpolation rules, valid interval, missing-data and
out-of-range behavior. A reusable authored curve evaluates a declared input to
an output; it is versioned code/data, not a producer result. Detector outputs
such as loudness, stem energy or gaze positions are signals; a threshold producer
can derive trigger markers from a signal. Do not turn every signal sample into
a marker or interpret every number as an animatable property.

The future M5 element-binding proposal is: stable parameter address + pinned signal ref + exact
occurrence/time-map + explicit versioned transform/units + follow/fixed selection
policy. Source mapping is shared with markers; display values must not replace
source values. Missing samples are reported according to declared policy, not
made-up zeroes. When a leaf has authored keyframes and a signal binding, reject
the ambiguous combination unless an explicit deterministic composition mode is
declared. Avoid arbitrary expression evaluation. New signal publications become
visible only when their selection is committed. No automatic edit-trigger loop
is introduced (PLAN defers automatic triggers until after M5).

App `src/sdk/video/families/dataKind.ts` already distinguishes `point`,
`interval`, `series`, coordinate domains, `sourceItemId`, occurrence `id` and
`sourceArtifactRef` (36–65, 127–154, 302 onward). Its lanes can present marker
and signal projections; these are not yet compiler anchors or signal bindings, and
they do not authorize pre-stop signal work.
`dev/scene-phase-markers/extension.ts:ScenePhaseMarker` stores `{id,time}`,
`buildAlignShotsPatch` emits absolute `clip.move`/`clip.update` (682–690), and
`moveExistingShotsToMarkers` uses marker index (797–804). Reuse the ruler/gesture UI,
not that ordinal alignment as following behavior. `TimelineExtensionOverlayHost`
provides marker layers and pointer ownership with integration coverage.

## Editable views: projection plus parser, not replacement documents

General editable-view hosting is a future M5 proposal. M2 still migrates the
built-in sheet through the one command path; that narrow migration does not
install a general editable-view framework.

Main `astrid/sdk/timeline_sheet.py` is concrete precedent:

| Existing path | What it establishes | Required foundation change |
| --- | --- | --- |
| `render_sheet` (63–150), `_layer_row` (227–270) | Projects cuts/lines/sound; supports scoped cuts; elides complex values; preserves formula display | Add accepted revision, grammar/view version, exact query/scope and stable reference-to-row mapping. Current `sheet_version` is a 12-character document hash and local export cache, not an accepted revision. |
| `parse_sheet` (326–397) | Structured rows and line diagnostics; ignores display gutters, carried rows and `scope` banner | Keep parser pure; validate duplicate IDs and scope externally. Store omission/clear/elision intent separately. Parsing must not resolve media handles with I/O; bind them before command execution. |
| `apply_sheet`/`find_version`/`merge_sheet` (596–739) | Detached rollback; exact known base required; local three-way clash diagnostics | Build commands against the exported base, then submit base + batch to the sole server rebase. Local diffs can explain edits; the local merge must not authorize acceptance on a newer head. Missing base refuses, preserving edited text. |
| `_apply_parsed` (742–849), `_update_layer` (948–1011) | Existing semantic operations cover cut/clip additions/removals, gaps, notes, looks and timing | Replace direct `clipType`, parameter pops, `intent.set_*`, music mutation and local resolve with registered command builders. Use recipe clears and stable IDs, not broad object replacement. |
| `astrid/packs/timeline/cli.py:_cmd_apply` (3565–3575) | Current CLI applies to Checkout then `tl.save` | M2 built-in sheet must use the same command commit as CLI/Python/App; preserve one atomic undo group. |

A future M5 editable-view envelope contains accepted base revision (or explicit
draft identity), view/grammar implementation version, options, query + resolved
ordered membership, row-to-scoped-reference map, and an **editable surface**.
The surface declares which fields and collections each row presents completely,
which are partial, and which are read-only/elided. It can travel with the text
or in its bound sidecar; never require hidden process memory for recovery.
The parser returns typed field intents/row membership changes; the host diffs
those against the base projection and emits **existing registered commands**.
That diff is a representation diff, not a before/after timeline diff used to
infer reads or write intent. The command runner remains responsible for the
recipe's authoritative observations. An editable view cannot invent an edit
operation: missing vocabulary is a command registry requirement first.

Deleting a row is a delete only if its containing collection was exported as
complete for that scope. Omission outside scope changes nothing. Omission of a
shown clearable field, explicit null and a placeholder are distinct; `ELIDED`
(`_read_value`, 538 onward) means retain the opaque base value. Unknown fields
and extension objects not represented by the view stay untouched. A concurrent
new member cannot be deleted merely because it was absent from the old text.
Names and row positions are labels; duplicate local names across occurrences
bind through the exported scoped-ID map. Hand-written fragments without a base
may use explicit patch commands but cannot infer omissions/deletions or silently
claim stale-safe round-trip semantics. Malformed input, ambiguous identity,
unsupported grammar or failed migration produces diagnostics and zero commands
committed; text is retained for repair. Script text does not invent replacement
audio/transcripts: media production is a separate producer proposal.

Read-only script and shot-list views reuse `timeline_views.py:render_script`
(289 onward), `render_clips` and `cli_show.py:render_view`. Exporters use the
same pinned projection context; EDL/subtitle loss of unsupported features must be
explicit, never silently flatten unknown elements. A view diff evaluates the
same view version/options at both exact revisions, or reports incompatibility.

## Elements and unknown visual internals

Preserve typed subcontracts inside the one Element category:

* Component: deterministic frame/audio evaluation with declared input clocks,
  parameter schema, assets and supported output/capability facts. Registration
  binds its exact element identity, not a guessed name substring.
* Modifier: instance identity, allowed hosts, parameter validation, wrap/evaluate
  function and bounds/alpha/support policy. Composition
  `typescript/src/modifier-types.ts:ModifierDeclaration` (37–62) already requires
  hosts, bounds, preserved alpha/support and an optional actual validator.
* Transition: two endpoint/adjacency references, boundary ownership, duration,
  parameters and supported transition planner. Composition
  `lib/transition-declarations.ts` (5–46) pins a contributed resource revision;
  its admitted implementations are currently only cross-fade/fade with linear
  opacity. This is not evidence of arbitrary transition/shader support.
* Curve: pure, versioned reusable evaluation and range/units; authored keyframes
  address stable instances. Composition `lib/modifier-keyframes.ts` uses
  `modifiers[<quoted instance ID>].params.<leaf>` and validates schemas/values;
  `lib/motion-curves.generated.ts` and `audio-curves.generated.ts` provide actual
  existing curve vocabularies. Broader animatable annotations need explicit
  admission, not an assumption that all numeric leaves animate.

Composition `scene-capabilities.ts:PreparedComponentCapability` and
`scene-evaluation.ts:querySceneFrame` (77 onward) already distinguish declared
presence, bounds and opaque support. Undeclared component pixels produce
`unknown-component-internals`; undeclared animation/bounds/blends remain unknown.
Agent visualize, App preview and render must consume the same package and
admitted capability contracts. UI overlays are not film elements unless authored
as such. Preview/export support is declared separately; an opaque or unavailable
visual implementation cannot become a successful-looking placeholder export.
Unknown data must survive saving and text edits while preview/checks expose
unknowns. Unknown scene bounds alone do not veto rendering/export when the actual renderer implementation is available; successful output must be established by that real render, not inferred from unknown scene answers. Missing/unsupported rendering reports unavailability rather than placeholder success. Any advisory-check export veto requires the explicit project policy described below. One evaluator does not prove pixel/audio parity; PLAN's planted-mismatch
parity gate remains required. No renderer or scene query is needed to save.

## Shared identity, data, proposals and policies

**Selection/query.** The existing `astrid/sdk/timeline/selection.py`
(`parse_selector`, `Selection`, `FILTER_KEYS`) remains the bounded core seam,
rather than adding a dialect per extension. Its key=value grammar already has AND
across keys and OR lists. Query-language growth is M5/later: main `cli_find.py`
currently has text/asset/line/cut/element/role filters, **no shared `--where`
yet**, and M0–M4 do not add one. A future M5 versioned normalized query may serve
registry commands, views, checks, source/marker/signal pickers and `find --where`.
Any typed namespaces/refs or bounded region/order predicate growth is a future
M5 proposal; M0–M4 use only the existing bounded selector surface and explicit
reference maps.
Reject unsupported predicates; never serialize Python callables as remote query
meaning. Record membership **and order** against the base when edits depend on
them. Read views may query a revision; rebase cannot re-run a live query and
silently enroll new objects. Source items, shot definitions, occurrences, clips,
cuts and projected marker instances remain distinct kinds.

**Namespaced data at every scope.** Core M0–M4 work preserves opaque data using
the existing Runtime-owned `app` carrier
where that scope supports it, with exact admitted namespace + payload schema
version + data. `astrid/core/timeline/astrid_ns.py` already preserves opaque app
siblings and moves Astrid's known intent to `app.astrid` (1–5, `clip_ns`,
`film_ns`, `_keep`). Do not repurpose its compatibility-flattened reader as an
extension write API. Ownership scopes are project, timeline, shared shot,
occurrence, track and clip; nested element/modifier instances also retain their
own unknown fields. For scopes without an admitted `app` slot, a future M5
extension-data proposal may add a declared owner map keyed by typed stable IDs
in the timeline's existing app carrier,
rather than inventing unsupported fields on Runtime rows. The Agent/Runtime
owners must settle the canonical storage projection during M2 schema work;
extension authors see one scoped data accessor regardless of physical layout.

Project pack configuration stays `<pack>.config` (or an independent named
collection) in Runtime Documents, per `docs/packs/data-storage.md` and
`astrid/sdk/documents.py:stable_document_id`. Documents CAS version is not schema
version. Ordinary settings writes use that API; a timeline-affecting input must
be captured as an immutable snapshot/ref in the command and accepted revision.
Reading a mutable project config during replay is forbidden. There is no implied
atomic transaction across several timelines or a settings document and timeline
commit. A project attachment does not grant a pack a separate timeline store.

Accepted edits consume the exact transcript/config content they used through
Runtime's narrow immutable content-addressed snapshots. Runtime owns the retention
mechanism and DTO; Agent owns extension consumers. Consumers use the retained
snapshot/pin and must not depend on a mutable Documents version lookup surviving
retranscription. This is not general Documents history. Authorized source
snapshots/pins remain renderer-free, and no new port or envelope is added without
Agent/Runtime owner coordination.

In the future M5 extension-data model, each namespace schema declares owner scope, reference-bearing typed fields,
field presence/clear semantics, collection semantics and migration version.
Unknown schemas/payload members are opaque and preserved exactly as JSON values
(not a promise of byte-identical whitespace). Generic ID remapping must rewrite
only declared references, never strings in opaque payloads. Prevent deleting a
known referent with surviving dependencies; for unknown reference semantics,
refuse operations that require proving/remapping their internals rather than
guessing. An unrelated edit can still preserve that data. This follows the
recipe's atomic-opaque-object rule.

Collections do not get universal "per-field merge": independent keyed members
may merge by stable ID when declared; ordered lists record order and boundary
dependencies; append-only sets need identity/deduplication rules; coupled fields
(time/value/unit, transition endpoints) are one invariant group; opaque arrays
are atomic. Concurrent delete-vs-edit, reorder and parent replacement conflict
by default. Unknown fields have conservative atomic merge, not last writer wins.
Extension-specific merge overrides are M5/later; foundation work uses the recipe's
declared core policies and fixtures.
Namespace registration grants no authority to write other packs' data.
App `extensionContextFactory.ts:createExtensionTimelineOps` (125–233) already
guards attribution and project-data targets; Runtime/provider must enforce the
corresponding authority, not trust an App-only check.

**Rationale and grouping.** Use the recipe's optional short `rationale` and
`group_id`; the reconciled commit-wire spelling is `rationale` throughout. Show
them in canonical history and projected diffs. Explanatory
`why:` text in the cut sheet is existing **authored cut data**, not a substitute
for command rationale. A gesture, deterministic macro or accepted producer batch
is one undo unit and one atomic acceptance transaction. Producer artifact writes
are independent immutable outputs: failure/rejection leaves unreferenced
artifacts, never partial timeline edits. A shared group ID across requests does
not make those requests atomic. Undo must retain the entire group's observations,
including publication-pointer no-op writes, as the recipe requires.

**Proposals (future M5 proposal).** The proposed envelope is identity + project/timeline + base accepted
revision/publication pair + ordered commands (with captured IDs/bindings) + rationale + source
pack/run/artifact refs and implementation versions. Preview/diff/findings are
pinned derived outputs. Accept sends the original base and commands to Runtime
for the recipe's authoritative rebase, validation and atomic commit. Conflicts
leave the proposal reviewable; reject changes no authored state. Retry uses the
same exact in-flight request; newer proposals do not replace uncertain sends.
App `lib/proposal-runtime.ts` already has review/preview and TimelineOps acceptance
but stores numeric `baseVersion` and patches (`ProposalPersistenceRecord`, 38–52);
its UI/persistence can be adapted, not treated as the accepted history authority.

**Automation/export policies (future M5 policy proposal).** Findings are advisory to human saves. Core
schema/reference/authority/timing validity remains mandatory. Project policies
may require named/versioned checks for a producer proposal's explicit
auto-approval or for export; missing/stale/failed/unavailable required results
mean approval/export is unavailable, with reasons, never implicit pass. Pin the
policy Documents version and check inputs to the actual candidate/accepted
revision; if rebase changes the candidate, rerun required checks before automatic
acceptance, and validate candidate/head identity on commit. Do not run renderer
checks inside the save transaction. A changed head retries planning/checking,
not acceptance with a stale pass. Human review remains possible subject to core
validity and the project's stated export policy. A producer cannot grant itself
auto-approval; preference prose is not authorization. Export gating happens
before producing a successful export, using the exact exported revision.
Checks rerun asynchronously on new accepted revisions from their first release;
old results remain labelled with their revision and cannot act as fresh passes.
This notification/recomputation does not authorize automatic editing triggers.

**Migration failure.** Owning packs provide deterministic migrations over detached
payloads/commands with explicit reference rewrites and before/after schema checks.
Never migrate on inspect, silently downgrade newer data, create defaults on read,
or partially rewrite a document. An explicit migration proposal uses the normal
command path; failure preserves original state, original command/proposal and
artifacts with a repair diagnostic. Uninstall/disable preserves payloads and refs;
missing renderer is reported as unavailable/unknown. App's
`runtime/extensionReferenceReport.ts` already states preservation on uninstall;
`extensionMigration.ts` handles existing package reconciliation but is not a
substitute for payload/command semantic migrations.

## Ten persona walks against real paths — M5/later examples

The names below are PLAN's M5/later sweet-spot examples. They are not M0–M4
implementation work or a pre-stop feature commitment. Existing examples establish
reusable pieces, not readiness of the complete persona workflow.

| Persona / workflow | Available real path | Required work on the five types/primitives |
| --- | --- | --- |
| Foley Ghost — infer and audition sound at visual events | Agent `packs/foley/actions/foley_map/run.py`, `packs/fal/actions/fal_foley/run.py`, `tests/packs/test_foley_review.py`; App `examples/extensions/creative-lab/foley-constellation/index.ts` | Producer pins visual/media inputs, emits immutable audio + event markers and a proposal; audio clips/components play accepted output. View auditions by revision; Command anchors placement; Check flags missing coverage. Current Foley generation is not persistent marker following. |
| Stem Triggers — react to a musical stem | Agent `packs/music/actions/beats/run.py` emits beats.json; App dataKind series lanes; Composition `lib/audio-curves.generated.ts` | Stem separation/energy Producer, typed signal publication, optional threshold markers, explicit signal binding to animatable Element leaf. A deterministic snap is a Command; continuous response is element evaluation, not an automatic edit trigger. Current beat times/curves do not supply stem signals. |
| Corkboard argument view — group claims and rearrange their presentation | Agent `timeline_views.py:render_script`, cut notes; App `runtime/ExtensionPanelHost.tsx`, `sdk/context.ts:CreativeContext.reader` | View projects shot/occurrence refs plus namespaced claim/relation data; editable actions emit existing reorder/move/note commands with rationale. Preserve unshown relations and repeated occurrences. No alternate board-owned timeline or unrestricted graph merge; missing command vocabulary precedes editor UI. |
| Cold Open Lab — propose a different opening | Agent `timeline/edits.py` structural edits; App `lib/proposal-runtime.ts`, `examples/extensions/creative-lab/branching-cut/index.ts` | Producer proposes ordered existing commands on a pinned base, grouped for review/undo, with a comparative View. This can preview a candidate without accepting it. Persistent fork/variant ancestry/merge is PLAN's later core feature; do not implement it as an extension store or claim it exists. |
| Replay Diff — explain what changed and why | Agent `packs/timeline/cli_history.py`, `cli_log.py`; R4 `commands.py` recorded writes and `rebase.py`; App proposal preview/diff | Revision-pinned View compares exact revisions and reads rationale, grouping and normalized commands. Respect authored-vs-derived differences; arbitrary textual diffs cannot recover intent/no-op writes. Accepted shared history and rationale projection need foundation work. |
| Shot Match Lab — compare look/motion and propose matching edits | Agent `packs/rendering/actions/timeline_visualize/`, `cli_visualize.py`; App proposal runtime; Composition scene bounds/unknowns | Producer analyses pinned frames and publishes measurements/signals + proposed existing look commands, optionally modifiers. View compares output; Check can flag mismatch. Numerical look edits exist, but automatic matching/analysis and bindings are new work; unknown component internals cannot certify a visual match. |
| Sign-language inset — add a synchronized interpreter | Agent media/clip authoring and explicit source time maps; App `sdk/video/families/clipTypeContributions.ts`; Composition component capability/bounds | Producer imports/generates immutable interpreter video with transcript/source provenance; Command adds occurrence-local inset; Component handles layout/playback with declared bounds. Word/marker anchors preserve synchronization; no speech-text-to-sign translation guarantee follows from the seam. Live feeds require materialization before reproducible export. |
| Kinetic subtitles — timed expressive word animation | Agent `packs/editorial/actions/transcribe/run.py`, `packs/rendering/actions/timeline_visualize/transcripts.py`; R4 exact `source-word` grammar; Composition modifier keyframe/curve evaluators | Producer supplies immutable transcript/word identity; Commands author captions/bindings; Component/modifier + authored curves or signals evaluate motion; subtitle exporter is a View. Word spelling/index cannot be identity after re-transcription. New typography/animation capabilities need real parity coverage. |
| Gaze Veto — flag visually obstructed or inappropriate gaze regions | App dataKind source/series projection; Composition `scene-evaluation.ts` bounds/coverage; Agent visualize overlays | Producer publishes gaze tracks/confidence as source signals; Check returns revision/ref-pinned findings and optional reframing/move proposal; View overlays. Unknown geometry/low confidence is unknown, not a pass or a fabricated face box. Policy may gate auto-approval/export, never ordinary human save. Gaze detection/check logic is new. |
| Plain-text round-trip timeline | Agent `timeline_sheet.py`, `cli.py:_cmd_apply`, `tests/sdk/test_timeline_sheet.py`, `tests/editing_conformance` | Built-in editable View carries base/scope/ref map; parser + projection diff emits registered commands; server handles stale-head rebase. Existing sheet is the strongest precedent but its local hash/cache, omitted scope metadata and direct setters require replacement. Unknown payload, clears and concurrent members must survive. |

## Ownership and M1–M4 preparation boundary

Agent editing owns semantic schemas/refs/query/projection and command registry;
Runtime owns accepted revisions, media/data custody, Documents, transaction and
generated wire validation; Viewing owns Element/evaluator/capability/clock
contracts; App owns panels, inspectors, gestures, outbox and review UI. Shared
DTO/schema changes are agreed by Agent + Runtime with App/Viewing review, not
four independent copies. Extension-specific payload schemas stay with their pack.

| Milestone | Who prepares/implements the foundation seam | Explicit boundary |
| --- | --- | --- |
| M1 | Agent/Runtime: recipe registry/provider boundary, pinned dependencies and accepted revision IDs; App: durable command outbox/preview identity; Viewing: revision-labelled visualize consumption | Clip move/retry/undo plus one small structural-command proof of framework-generated recording; actual App capture/sequence/dependent-gesture tests are M1 requirements. No marker/signal production, detector, generic extension host, new UI package or signal binding; only design fixtures may exist. |
| M2 | Agent: complete registry/recording/reference and scoped opaque-data preservation, compiler and cut-sheet command adapter; bounded marker/signal reference-resolver seams consume pinned inputs and core fixtures; Runtime: admitted storage/wire projections and exact dependencies; App: all writers including existing extension patches become command adapters or lose mutation access | No detector publication, ID reconciliation, marker/signal registration, generalized signal binding, policy orchestration or general editable-view host. Built-in sheet migration remains M2. Preserve every existing film's beat/word read and playback semantics. |
| M3 | Viewing: one published Composition evaluator and typed element/capability/parameter contracts; App/Agent: consume it for preview/render/visualize, including unknowns | No marker/signal behavior beyond the bounded resolver seams and fixtures. Current components/modifiers/transitions/curves and parity are foundation work; third-party element registration, generalized signal binding and examples remain M5. No scene evaluator in commit. |
| M4 | Agent removes old extension engine after all consumers are inventoried/migrated or explicitly retired; all managers finish deletions, document schemas/APIs and verify unknown-data/renderer-independent behavior; Runtime/delivery owns ZIP | Do not require an M5 framework to delete `core/extensions`. Inventory/remove old direct mutation dispatch and retain established built-in behaviors as commands/views. Foundation seams are concrete function/data boundaries and tests, not installed extensions. Hard stop remains. |

M5 ownership after authorization: Agent implements the thin pack-to-five-types
projection and author-facing marker/query/proposal adapters; Runtime supplies existing
artifact/commit operations with agreed schema additions; Viewing implements
admitted element/signal evaluation; App adapts presentation/review. This is an
ownership statement for future API/data-model proposals, not an implementation
backlog or permission to start it.

## Recipe integration and counterexamples needing its attention

The recipe draft read during this work was headed "early review draft" and
already required recorded selection/order, pinned anchors, opaque namespaces,
explicit clears, historical R4 injective-map probes and grouped guards. Those probes do not authorize a general foundation remapper: current commit `id_map` is identity-only. Its subsequent
"Concrete reconciliation with Runtime's first draft" and "Recorder additions"
sections were also read: use base head pairs, wire `rationale`, typed provenance
in reads, and command-specific clear builders as specified there. Its executable evidence
was still marked in progress. The extension design relies on that contract and
does not claim its hard-case probes have passed. Cross-links for all PLAN cases:

| Recipe hard case | Extension-specific application |
| --- | --- |
| Ripple/insert | Beat-snap or board selection captures membership/order; a concurrently inserted beat/clip cannot silently enter the batch. |
| Transitions | Contributed transitions bind both endpoints/adjacency, not just a named style; deleted/reordered endpoint conflicts. |
| Shared shots/occurrences | A marker/signal source may have two placements; occurrence-local subtitle/inset edits must not mutate a shared shot. |
| Music beds | Source beat markers traverse arrangements/trim/speed; undo restores authored publication/source arrangement and recompiles. |
| Transcript anchors | Kinetic subtitle/source-word refs survive spelling changes only through explicit source identity; removed words remain unresolved, not rebound by text. |
| Track lifecycle | A producer adding a track cannot undo-delete it after another author adds dependents; namespace data and marker bindings count as dependencies. |
| ID collisions | Imported/re-detected sets reserve stable IDs and use declared typed remaps; never rewrite a coincidentally matching string in opaque data. |
| Explicit clears | Editable-view omission/null/elision/clear are separate, including namespace fields and complete collections. |
| Media add/swap | Producers pin immutable authorised media; source replacement cannot silently carry a marker/signal lineage to different content. |

Three extension counterexamples should be included in the recipe hard-case
fixtures/conformance after the relevant M5 seam is authorized; they are not a
pre-stop implementation requirement:

1. **Moving dependency without changed clip declaration.** Clip A follows marker
   m2; re-detection inserts m0 and moves m2, then another client edits/reasserts
   the selected publication A→B→A. A clip-only write footprint misses the change.
   Record the selected set publication, exact item identity, follow policy and
   time-map dependencies; undo/rebase must inspect publication writes/ancestry.
   Follow deliberately permits a newer position for the same surviving identity
   according to an explicit versioned policy. A missing or deleted identity fails
   closed: republication is refused atomically and the prior selected publication,
   bindings and state remain intact. Do not default publication changes to silent
   rebinding.
2. **Lossy projection plus concurrent membership.** A partial text view elides
   unknown namespace data and exports c1's members; another author adds a member
   and changes a hidden field. An edited text omits one old visible row. Only
   that base-scoped row is a removal; hidden data and the new member survive or
   selection policy returns a clear conflict. Main `parse_sheet` ignores the
   printed `scope` line: the envelope must carry completeness/membership, not
   trust display text. The stdlib probe verifies this parser fact.
3. **Unknown reference-bearing payload during structural remap.** An imported
   unknown schema contains a clip-ID-shaped string. Preserve it exactly on
   unrelated edits, but refuse a clone/remap requiring proof of its references
   until a schema/migration is available. Do not assume every string is a ref,
   or that unknown implies reference-free. Group atomicity includes the migration
   and all known ref rewrites. Existing R4
   `test_id_map_rewrites_only_recorded_scoped_ids_and_not_opaque_values`
   (`tests/sdk/test_timeline_rebase.py`) covers the opaque-string half only.

These are contract integration requirements, not permission to enlarge the M0
implementation. The first is an M5 marker-republication case; pre-stop work is
limited to bounded marker fixtures. The second can already exercise
sheet/projection semantics; the third tests the
recipe's general opaque data and structural dependency rule.

## M5 acceptance criteria only — approval required before implementation

Common M5 acceptance: each example is pack-admitted using existing source/resource
validation; exact code/schema versions are recorded; unload/reload preserves
unknown data; text/CLI/Python/App adapters agree on accepted revisions; all edits
use the recipe and real Runtime acceptance. No proposed example is implemented
or claimed working by this document.

| Type | Observable acceptance criteria |
| --- | --- |
| Commands | Beat-snap selects stable clip and marker identities, declares follow/fixed and ripple/scope intent, previews without renderer, accepts atomically, retries after restart without duplicate IDs/revision, and undo/redo restores exact authored presence/data. Re-detecting beats with an inserted earlier event moves followed clips with the same surviving marker IDs, keeps fixed clips fixed, and never ordinal-rebinds deleted IDs. A missing referenced marker fails closed: republication is refused atomically and the prior selected publication, bindings and state remain intact. Rebase permits declared same-ID following and disjoint edits; conflicts name changed identity/membership or source mapping. Grouped no-op writes and A→B→A remain guarded. |
| Views, including exporters and editable | Beat-grid text and visualize overlay show the same marker IDs/times at an explicit accepted revision. Script and shot-list projections agree on transcript, shots/occurrences and time windows with canonical show. A plain-text editable view exports/imports unchanged as no-op, emits commands for edits, supports scoped additions/removals/explicit clears and opaque elision, and gives one undo step. Stale base gets server rebase or an actionable conflict, never replacement; unavailable base/grammar fails without writes and retains text. Old/new revision view diff uses pinned options/version. One exporter (e.g. subtitles) pins revision and reports unsupported features; required export-policy failures prevent success without blocking save. |
| Elements (all sub-kinds and curves) | At least one admitted component, modifier, transition and reusable curve exercises its actual typed contract and explicit animatable leaves. Preview, visualize and export agree on frame/audio behavior under rational fps and boundary/time-map cases; a planted mismatch is caught. A signal-bound leaf follows the selected immutable series with declared interpolation/units, while authored-curve evaluation stays deterministic. Invalid host/params, conflicting animation modes and missing materialization report precise errors. Unknown bounds/support/pixels are UNKNOWN, preserved in save, and never converted into proven coverage or assumed export success; real rendering may still establish a valid export when the implementation is available. Renderer-off save remains green. |
| Checks | Off-beat check returns stable clip/marker references, check version and revision-pinned findings in text and visualize overlay; a beat-snap fix is a proposal of existing commands. Accepting the fix removes the finding at the resulting revision; stale fixes rebase or conflict. Check failure/crash/unavailability never blocks human save. An explicit project policy blocks auto-approval/export on missing/stale/failing required results and reruns on a changed candidate; check execution never writes the timeline directly. |
| Producers | A beat detector publishes an immutable artifact and named marker set with source/input/version identity, then proposes the selection/publication commands. A second run retains reconciled IDs, records inserted/deleted/ambiguous events explicitly, and demonstrates beat-snap following, beat-grid visualization and off-beat fix together. Reject/cancel/failure changes no timeline; artifacts remain inspectable. Acceptance is grouped, authorised and retry-safe; missing media/source-lineage change is diagnosed. A producer of a typed signal demonstrates source-to-occurrence mapping, and an importer proposes ordinary commands preserving unknown data rather than replacing a document. |

The full litmus chain must be one tested journey: detector → immutable markers →
snap → re-detect with retained IDs → followed placement → beat-grid/visualize →
off-beat finding → proposed fix → accepted fix. Script/shot-list and editable
text view are additional required journeys, not screenshots substituted for
round-trip behavior. Structural identity/merge counterexamples above and
the recipe hard cases must be represented in main suites before acceptance.

## Verification and limitations

This M0 work does not establish extension integration or Linux render parity.
The standalone observations execute existing R4 pure moment code and AST-selected
main pure parser functions; they do not execute a proposed marker implementation
or a mocked substitute for the compiler. They are design probes, not gate proof.

Commands actually run in `/home/user/work/wt/agt-m0-ext`:

* `python3 -B tests/m0_extensions/probe_extensions.py -v`: first run, 3 passed,
  1 error (`Any` absent from the extracted parser namespace); the probe namespace
  was corrected. Second run: **4 passed**, 0.063 s. No third-party dependencies,
  pack execution, files written by the probe, or network access.
  After formatting only, the same command passed **4 tests in 0.102 s**.
* `PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_show_views.py tests/editing_conformance`:
  **219 passed, 4 skipped, 2 warnings in 31.87 s** (exit 0). The four existing
  skips are `test_platform_safety_net.py:test_preview_matches_render_frame`
  parametrizations; their pre-existing reason requires App preview/render frame
  capture. No skip was added or weakened. Warnings report unknown pytest config
  options `timeout` and `timeout_method` (system Python lacks pytest-timeout).
  The dependency-only shared env `/home/user/work/venv-agent` was absent, so this
  command used the available system Python environment; it is not an env-baseline
  or full-gate result.
* `git diff --check`: exit 0, no whitespace errors.
* `python3 -m ruff --version`: exit 1, `No module named ruff`; no lint result is
  claimed. The probe is outside the current configured Ruff include paths.

Relevant main entry points (run only where included in the exact command above):
`tests/sdk/test_timeline_sheet.py::{test_applying_the_printed_sheet_changes_nothing,
test_a_fragment_touches_only_its_cuts_and_a_new_line_adds_a_layer,
test_detail_prints_long_values_as_editable_json_and_round_trips,
test_trim_syntax_on_a_visual_layer_is_refused_atomically}`;
`tests/sdk/test_timeline_show_views.py`; `tests/sdk/test_timeline_selection.py`;
`tests/packs/test_canonical_pack_v3.py`; `tests/packs/test_pack_quarantine.py`.
`tests/editing_conformance/README.md` documents the CLI/Python/sheet scenario
runner, exact undo/redo, no-op and refusal comparisons.

Frozen R4 migration tests inspected, **not run here**:
`tests/sdk/test_timing_cycles.py`, `test_timing_compiler.py`,
`test_timeline_rebase.py`, `test_timeline_sheet_journal.py` (including
`test_sheet_property_mapping_preserves_authored_values_and_atomic_refusal`).
These require the real port environment/fixtures; do not count source inspection
as a test pass. The recipe worker owns hard-case execution/classification.

Relevant App suites, **not run here**: `src/tools/video-editor/lib/proposal-runtime.test.ts`,
`runtime/extensionMigration.test.ts`,
`components/TimelineEditor/TimelineExtensionOverlayHost.integration.test.tsx`
("drives one validated manifest through the real provider assembly, lifecycle,
hook, host, and marker"). Exact targeted command for the App owner:
`npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/lib/proposal-runtime.test.ts src/tools/video-editor/runtime/extensionMigration.test.ts src/tools/video-editor/components/TimelineEditor/TimelineExtensionOverlayHost.integration.test.tsx`.
Broader existing gates are App `npm test` and `npm run test:e2e:three-products`;
Agent `make check` and `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance`;
Runtime `python -m pytest -q -n 2`. None of those broad gates is claimed here.
Composition `package.json` currently masks build failures with `|| true`; a
successful old build command would not prove parity. Viewing owns removing it
and adding unit tests; this worker did not change or build Composition.

Linux only: no macOS/native custody, windowed App, actual detector/media inference,
browser render/audio parity, export or cross-product journey was exercised here.
No shared environment was installed or changed, no integration worktree written,
and no git mutation/push performed.
