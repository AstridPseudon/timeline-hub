# One edit recipe — M0 semantic contract

Status: manager-reviewed M0 design, 2026-10-19; Checkpoint A approval pending.
Owner: Agent editing. PLAN §4.1 wins.
This specifies the forward port; it does not claim main or frozen R4 already
implements every rule. Executable observations and exact remaining source changes are recorded below. Runtime's
`commit-contract.md` owns transport, transaction and durability; this document
owns command meaning. No M1 implementation is included.

## Wire and author API

Retain R4's `EditCommand` vocabulary: `op`, `select`, `args`, `version`,
`resolved`, `expect`, `bindings`, `created`, `authorship`. Add a schema version
separate from the operation implementation version: `schema_version: 1`,
`version: <registry operation version>`. R4's tool-release version alone is not
an adequate semantic version. Unsupported versions fail before execution;
upgrades explicitly migrate a detached command and preserve the original record.

One registry entry supplies an annotated parameter schema and a deterministic
handler over authored state plus request-bound dependencies. Schema annotations
include type/enum/range, units, explicit defaults, nullable/clearable, ownership,
reference kind/picker, and merge policy. A missing argument uses the versioned
default; normalization records that effective default. Null is a value only for
nullable parameters. An operation-specific explicit clear removes presence; it is never null and cannot also assign that field in the same command. The annotated schema emits the existing clear builder (`clip.clear`, or disjoint `values`/`clear` arguments where supported); there is no universal top-level clear field or magic object sentinel. Unknown document and
extension fields round-trip; unknown command arguments fail.

Times use seconds at the API boundary, frame counts declare their unit, frame
rates are numerator/denominator rationals, intervals are half-open. Quantization
and rounding are versioned and run once at the canonical boundary. Pixel values
are authoring canvas pixels, never renderer-normalized coordinates. Reference
pickers return stable scoped identities or immutable anchor identities, never
array positions, display text or a mutable 'latest' media selection.

R4 aliases remain thin builders of canonical operations. The normalized command
explicitly declares applicable intent: ripple/non-ripple and its membership
policy; follow/fixed anchor; shared-shot/occurrence-local; absolute/relative.
There is no silent default from a UI checkbox at replay time. Handler execution
cannot read a clock, random source, filesystem, network or renderer. Allocation
is an injected deterministic service: allocate once, record IDs before dispatch,
persist them with the exact in-flight request, and reuse on replay. A collision
is a conflict. Foundation `id_map` is identity-only (empty or ID→same ID);
nonidentity results refuse. General remapping/forks wait for a concrete supported
command that demonstrates the need. Undo does not recycle reservations.

## What the runner records

The author supplies one registry entry: operation ID/version, annotated JSON
parameter schema, deterministic handler, supported intention/merge policies and
fixtures asserting intent. The handler uses an instrumented authored-state
context: `read(ref,path)`, `select(query,policy)`, `bind(anchor,policy)`,
`write(ref,path,value)`, `clear(ref,path)` and structural create/remove/reorder.
Every explicit write is recorded before comparing values. Structural primitives
record ownership, membership/order and reference edges; validation sees the
complete candidate. Returning a mutated arbitrary dict is not a conforming
extension handler because unobserved reads/writes cannot be inferred afterwards.
The R4 mutable-method adapters initially supply the same records through their
existing direct-path/expectation machinery; the spikes identify where that
machinery needs to become complete. This is a migration seam, not a second
runner or an implemented context API in M0.

Recorder metadata is framework output from those primitives, never an extra
hand-authored extension manifest. Runtime's `records.commands` is the one
accepted representation. Updated §4.1 omits independent `PreparedCommit.commands`;
any local accessor is derived only. Construct `Candidate.commands` by projecting
each record's `command`; check projection/ordinals at acceptance. Do not maintain
parallel mutable commands/direct-writes inventories. Ingress parses legacy
`expect`/`authorship` keys once into canonical `(ref, token path)` addresses;
downstream recording, overlap and inverse use only those addresses. Retain wire
spelling for compatibility, unchanged/direct intent and the structural facts
needed to reconstruct containers, source and order; a diff is insufficient.

The runner executes in order against a detached candidate, resolves selectors on
the base once, records the following, then compiles timing and validates. Failure
publishes nothing. Client records are claims; the provider reconstructs/verifies
them against the immutable base rather than trusting client authority.

* Writes: stable entity ID plus property-token path, before and after state,
  command ordinal and authored owner. Include explicit writes of unchanged
  values. States distinguish absent, present-null and present-value; R4's
  `{state:"absent"}` / `{state:"present",value:null|...}` already expresses this.
* Reads: every authored dependency that influenced execution, including absence
  tests, ownership and reference edges. Record the same tagged values.
* Selections: query version, resolved members **and order**, boundary identities,
  owner and membership policy. Freeze the original membership by default and
  conflict if it changes. A command may explicitly declare a deterministic merge
  policy (for example include concurrent members in a ripple), with fixtures.
* Bindings: resolved anchor ID, source/word identity, immutable source revision,
  follow/fixed policy and relevant time-map revision. Text and ordinal are only
  discovery UI. Fixed anchors store the resolved time and still preserve source
  provenance; follow anchors re-evaluate the same surviving identity.
* Created IDs and dependency edges; structural ownership; pinned media reads and
  authority requirements. Publisher/actor attribution is Runtime-derived. The command `authorship` map classifies handler writes as direct/consequence; the provider reconstructs it, and it never supplies caller authority.

Path overlap is token ancestry within an entity, plus explicit entity ownership
and references. Replacing `params` overlaps `params.x`; it does not overlap
`paramsExtra`. Deleting a track/occurrence overlaps its descendants and checks
all surviving dependents, including references from outside its container.
Opaque extension objects are atomic unless their schema declares structure.

## Replay, inverse and publication history

Only the server rebases. It records against the exact base, reads accepted head,
then replays with the original bindings, selection policy and allocated IDs.
Disjoint authored properties pass. Same-path or ancestor/descendant writes,
changed read dependencies, changed selection membership/order and disappeared
bindings conflict by default. Relative commands declare their read basis;
absolute setters do not accidentally become relative during replay. An operation
may override a merge rule only as a versioned deterministic policy.

Undo is a new guarded command. Generalize R4 `inverse.py`; preserve its structural
restoration, membership, authored-state and dependency safeguards. Coalesce a
group's intermediate writes into first-before/last-after while retaining its
complete read/write/selection history (including no-ops). Reverse in dependency
order; restore exact authored presence and opaque values; compile derived state.
Redo reverses the accepted inverse with fresh guards, not by replaying an old
snapshot. Identity reservations remain monotonic, a documented round-trip
exception outside authored content.

Value comparison is insufficient: Runtime must give the provider the exact
accepted publication ancestry and intervening writes from the target publication
through the current head. A write A→B→A, even A→A, conflicts with inverse at the
same path or structural overlap. Missing/compacted ancestry cannot imply safe
undo. Ancestor proof and complete write summaries must survive compaction, or
the operation refuses with history unavailable. Target publications must belong
to the same timeline and accepted ancestry.

`group_id` and optional short `rationale` are command/batch metadata, preserved in
history and App outbox. Grouping changes the undo unit, not atomicity: each commit
is all-or-nothing. No cross-commit atomic group is implied; a multi-publication
undo is itself one guarded transaction over all selected records.

## Provider, App and compiler seam

The provider receives base/head revision identities and exact immutable authored
images, ordered commands, pinned transcript/media selections, verified project
authority, and accepted ancestry/write records needed for inverse. It returns a
candidate authored image, materialized timing, recorded normalized commands,
direct writes, compiler consequences, structured conflicts/findings and domain
event facts. Runtime atomically accepts snapshot/history/events and returns its
normal `/v1` `CommittedMutation`; there is no parallel acceptance receipt or
client-authored publication identity. Dry-run returns a revision-pinned plan,
never a mutation receipt. Exact DTO names await Runtime's draft.

This narrows main `docs/architecture/semantic-mutations-events-and-agent-ux.md`:
retain its authoritative transaction, registered semantic events, receipt links
and append-only undo. PLAN supersedes its whole-document normal-edit escape
route and strict stale-version policy: normal editing uses commands and server
rebase. One batch emits semantic facts plus one real Runtime receipt, never a
second state-changing snapshot event.

Main App `TimelineCommand`/`TimelinePatch` adapters produce this command wire.
Gesture/group metadata and instant local preview remain; local rows/config/data
effects are preview materializations, never alternate publication payloads.
Preview must carry base revision and provider/compiler versions. It may be
optimistic but the accepted server result replaces it. The outbox retains exact
in-flight bytes, retry key, generated IDs and newer local commands independently;
never regenerate an ambiguous send after restart. Partial compatibility mode and
snapshot-fallback history cannot cross the commit boundary.

### Concrete reconciliation with Runtime's frozen DTOs

Read `commit-contract.md` again after its Runtime-owned §4.1 freeze, plus
`app-contract-review.md`, `agent-review-notes.md` and
`viewing-coordination.md` on 2026-10-19. Adopt Runtime's slim envelope and ABI 1
(main has no prior provider ABI; the exact new generated contract digest excludes
frozen R4, so an invented version increment is unnecessary):
`POST /v1/projects/{project_id}/timelines/{timeline_id}/commit`, required
`Idempotency-Key`, body `api_version:1`, canonical project/timeline IDs,
`base_revision_id`, `base_publication_id`, ordered nonempty `commands`; optional
`dry_run`, `source`, `label`, `rationale`, `group_id`. Use `rationale` consistently
in new DTOs; R4's internal `reason` is a migration adapter only. No R4
`request_id`, session, scope or `change` wrapper survives.
The client persists this exact envelope before sending, with generated IDs; the
Runtime computes its actor-bound request hash before applying defaults.

`provider.commit(context: CommitContext, port: RuntimeCommitPort) -> CommitOutcome`
returns accepted/preview/conflict/refused as in Runtime §4. `CommitContext` is
`{request,invocation,idempotency_key,request_hash,realm_id,publisher}`, supplied by Runtime,
with authenticated identity separate from the untrusted body. A real acceptance
passes a prepared candidate to `port.accept` and returns its stored result;
the provider cannot manufacture acceptance. Required prepared semantics are:
expected head **pair**, candidate compilation/publication with immutable child
pins, normalized executed commands, recorder version, direct writes (including
unchanged), reads/selections/bindings/created IDs, consumed dependency captures,
domain facts, undo/restore linkage. Use Runtime's exact `PreparedCommit` field
set: `{expected_head,canonical_document,document_digest,
records,id_map,semantic_events,provider_version,compiler_version}`.
Runtime derives inserts/reuses from the complete closure, including unchanged
images; no second publication payload or null/no-change variant exists.
Runtime allocates receipt/publication ID,
timestamp and event/project sequence. No evidence envelope is required.

Use Runtime's normal `CommittedMutation` with `receipt.command_kind =
timeline.commit`; `receipt.receipt_id` is accepted publication identity.
`data.canonical_document` and `accepted_revision_id` identify the exact result,
even if head advances before display. `status` is accepted/rebased; preview has
`receipt:null`, evaluated head pair and no accepted identity. The accepted
record's `commands` are authoritative executed records, not a new proposal to
send. Conflicts use Runtime's status/HTTP mapping, stable `kind/ref/path`, tagged
base/theirs/ours and choices; the exact conflict keys are `kind,ref,path` with
`path:string[]` per Runtime §4.1. Clients never parse prose for the kind.

A nonempty intentional same-value edit **must create a publication edge and
receipt**, and may reuse an immutable content revision. Both direct write
inventory and history retain A→A. This supersedes R4 `no_change`; a builder may
emit no command for an idle gesture, but cannot discard an already submitted
write. Frontends may emit no command for an idle interaction. An explicit submitted same-value setter is different: it gets recorded writes and a new accepted edge under a fresh key; an exact retry of the same request/key gets the original edge. When converting main conformance scenarios, retain document idempotence but update the old zero-local-undo-step assumption for explicit accepted writes; test idle omission and exact retry separately. No local CLI no-op policy may erase server history.
Unchanged revision plus changed publication is still a moved head. Adopt
Runtime's three total head-race attempts over one original recorded plan.

Provider reads are only `head`, exact `revision_closure` / `shot_closure`, scoped `history` /
`history_entry`, `selected_media`, `transcript_source` / `config_source` /
`narration_take`.
Runtime's accepted history retains recorder data and complete publication
ancestry; absent baseline history fails closed, and old whole-document writers
conservatively touch their full scope. Exact accepted retry bypasses semantic
execution and mutable media discovery. Retention of accepted retry/history is
Runtime-owned, not another local journal. Local R4 journal/sync code may support
crash recovery/inspection, never become accepted-history authority.

Agent replay, inverse and timing compilation consume Runtime-retained **content**
snapshots of every transcript/config dependency, not just version/digest pins.
Use the exact scoped pin and verified bytes through Runtime §4.1's narrow
content-addressed retention, including after a Document is retranscribed,
replaced or deleted. Never substitute latest content, rerun a producer or rely
on a mutable Document GET. Missing/corrupt retained content fails closed.
Runtime owns retention, lookup and DTOs; this adds no Documents history API.
Consume `transcript_source(DocumentPin)` / `config_source(DocumentPin)`'s exact
`VerifiedDocument` content/header. Include the complete surviving consumed input
closure in `CanonicalDocument.dependency_manifest.documents`; record transcript
pins as `AgentDependency.kind=transcript`, config pins as `kind=source`. Config
inside immutable parent/shot/internal payloads uses that exact closure instead.
Do not inject snapshots: Runtime privately verifies/captures and atomically
retains them with acceptance; first-use live-version races refuse.

Dependent App work follows the orchestrator's PLAN decision: B authored over unacknowledged A remains durable **unsent intent** until A is acknowledged or definitively rejected. Preserve B's original commands, stable references, created-ID dependencies and complete value/identity read and selection guards. After A acceptance at HA, reserve a new B request/key with base HA; provider verifies the original guards against HA and then performs the ordinary server rebase over later head changes. Never refresh guards, rewrite an in-flight request, relabel a snapshot, or reuse A's request identity. Rejection of A leaves dependent B as a visible conflict. Independent work already authored against an accepted base is unaffected.

Absolute B preserves its absolute target; relative B preserves its delta and original relative read basis. A changed guard/selection/identity conflicts. Equal-state ABA/A→A before HA is intentionally allowed for this dependent handoff: the original value+identity predicates still hold. This does not change the separate accepted-inverse rule that rejects intervening publication writes, including ABA. No `base_view`, virtual revision, retained-original-result reconstruction or additional DTO field is introduced. [suffix-basis.md](suffix-basis.md) records the mandated A→5 / B absolute7 or relative+2 / C / exact-retry / reload / created-ID experiment and its limitations. App's real browser/outbox journey remains M1 evidence.

### `clip.move` v1: shared operation and gesture-time capture

This is the capture contract for Python and framework-generated App capture;
authors still supply only schema, handler, intent and fixtures. Generate capture
from the same instrumented primitives, with Python/TS parity fixtures; do not
ask authors to maintain browser-specific read/write metadata. Capture on the
original authoring state **at gesture time, before local materialization** (drag
start freezes reads; drop supplies absolute `args.on`). Each sequential command
captures the preceding local command's result. Persist the resulting original
`resolved/expect/reads/selections/bindings/created` claims with unsent intent.
ACK only binds a new request/base; it never recaptures them. The provider verifies
them before recording at HA, then performs the only semantic rebase.

Source basis: main `authoring_bundle.open_authoring_bundle` verifies the parent
occurrence→shot revision→internal revision closure and gives repeated shots
independent authored owners. App `dataProvider.runtimeGraphToContract` derives
`at_ms` from `placement.start_ms` (fallback `at_ms`), then
`shotCompositionAdapter.prepareContract` and `shotCompositionProjection.projectClip`
produce `at = occurrence.atMs/1000 + child.at`, adding `source_offset/1000`
to source bounds; `sourceTime.ts` maps `t = at + (s-from)/speed`.
Projected IDs `${occurrenceId}:${clipId}`, `child-N` fallbacks, row indices and
asset aliases are not canonical selectors. M1 must retain the raw child ID in
the projection identity lookup; today's `clipIdentities` lacks that field.

The framework captures tagged presence/value reads at these canonical addresses
(paths below are relative to the named stable entity, never array indices):

| Owner / dependency | Required original capture |
| --- | --- |
| `parent/clip:c` or `occurrence:o/clip:c` | Exact resolved singleton, raw clip ID and owner; `at`, `at_ms`, `track`, `asset`/`asset_id`, `clipType`/`clip_type`, `enabled/active/disabled/hidden/deleted`; `from`, `to`, `hold`, `duration`, `duration_ms`, `speed`, including absent alternatives that choose the timing codec/window. Capture referenced track identity/kind/role and selected registry entry's source identity/duration when used for validation. |
| `occurrence:o` and its source closure | Guard normalized occurrence/authoring-owner identity, `placement.start_ms`, fallback `at_ms`, `duration_ms`, `source_offset`, `speed`, `track`, `placement.track`. Capture raw `shot_revision_id`/legacy `revision_id`, parent/shot/internal revision IDs, digests and manifest links as immutable image provenance, not blanket equality reads. Normalize the owner through main's `source_mapping`: read `occurrence:o/shot` path `shot_id` as its actual source_mapping source shot identity. Validate the placement's authoring ID equals that source or main's deterministic isolated ID for this occurrence/source. Guard comparison accepts the identical source or its EXACT deterministic isolated materialization for this occurrence. No prefix/naming heuristic establishes equivalence. The conditional in-memory copy ID never becomes an equality guard. History writes to the physical occurrence `shot_id` still invalidate this semantic owner read, including ABA. Explicit consumed source bindings still guard their semantic source identity/pin. |
| Clip timing relations | Presence/values of both `app.astrid` and flat legacy `app` keys `on`, `fixed_start`, `until`, `until_film_end`, `for`, `cut`, `sequence`, `sequence_index`, `sequence_fit`, `orphan`, `formulas`; relevant container types. If duration/start resolution consumes an anchor, capture its exact binding, source/word ID, transcript DocumentPin and retained content, cut endpoints and their owner/map reads. No text/ordinal substitute. |
| Selection/map basis | `move.target` v1 has owner `parent`/`occurrence:o`, singleton members/order/boundaries `[scoped clip ref]`, policy `guard-membership`; bind clip→owner→track/source edges. Any picker/group/snap/anchor query actually consumed also records its complete original members, order, boundaries and absence predicates. No unrelated all-tracks query is imposed on a direct singleton move. |
| Projection boundary / quantization | `parent` path `config.output.fps` and any consumed child `output.fps`; record the normalized rational rate. Fixed M1 uses the explicit authored window, not projected `outputTimeline`/`timelineContentExtentMs`, and App refuses sibling-start/end and hard-duration-end snaps. Consequently it consumes no output-clip extent/snap query and records no `move.extent`. Any adapter that starts consuming those queries must capture their complete ordered output clip membership and lane role/activity/timing predicates before enabling them. Occurrence M1 does consume `move.blockers`: all active same-lane output occurrences in placement order, their IDs/start/lane/activity and parent lane kind/role/activity, including empty membership and absence of a next blocker. Capture the complete predicates/order, not just the current winner. |

Resolve table entities to `parent_revision.payload.clips/config/occurrences`,
`shot_revisions` keyed by `(shot_id,revision_id)`, then
`internal_timeline_revisions` keyed by the linked internal revision; child paths
address its `payload` TimelineConfig (App unwraps legacy `payload.timeline`).
When both nonempty parent clip spellings exist, payload.clips is authoritative and config.clips is its derived mirror. Record mirror consequences in derived_writes at the command ordinal; regenerate after move, replay and inverse, preserving complete clip objects and unknown fields. Empty payload.clips falls back to config.clips, as main projection does.

Dependency pins retain those actual image IDs/digests; recorder refs stay scoped
entity identities, not array offsets or projection `app.canonicalTiming` caches.

Closure pins authenticate original inputs; they are not a blanket head-digest
equality guard that prevents disjoint rebase. Verify consumed values, identity
edges and selection predicates against the submitted base and replay head.
Fixed M1 guards and clears old anchor relations without evaluating their text or external sources. A surviving Runtime-retained document closure is verified through exact scoped captures and recorded separately as `compile.document:<pin digest>` dependencies (transcript/source DocumentPin); this is compiler input retention, not a claim that words/settings resolved the move. Unused captures outside the retained manifest are not consumed dependencies. Image provenance remains entity. M1 optional semantic_events is empty until scoped Runtime event admission is defined; Runtime still emits the required publication edge.

A's acceptance or a disjoint C can change a containing child revision/digest
without changing B's consumed fields. Those materialization pins must not become
B's `reads`/`expect` equality guards. Bind B by stable occurrence/clip and
normalized authoring-owner identity, then verify its original semantic guards
on HA; verify HA's actual closure provenance independently. This is not guard
refresh or a client rebase. An explicit immutable source selection (media,
transcript/config snapshot, or a consumed source binding) remains an exact
dependency; a true owner/source/window/rate change still conflicts. M1 must
exercise disjoint edits within the same child container and first materialization
of a shared occurrence, not just disjoint parent containers.
Guard comparison is type-aware JSON equality: absent/null differ and booleans
never equal numbers through host-language coercion.
Time-map dependencies are the occurrence placement/offset/rate and clip
start/window/rate above, with their closure pins; main has no universal `time_map`
DTO. Preserve any additional consumed map revision/content pin in existing
dependency records. Unknown explicit mapping semantics refuse rather than being
ignored or given a new basis field.

V1 supports parent identity mapping and occurrence translation with default
occurrence offset (absent/null/0) and rate (absent/null/1); child playback uses
finite positive constant speed and an explicit finite source window or duration.
For an occurrence at O seconds, materialize local start `Q(args.on)-O`, while
retaining the global absolute target on replay; parent local start is `Q(args.on)`.
Source bounds/rate/duration stay fixed. Require the complete half-open moved
interval ending at or before the next same-lane output occurrence, if any;
refuse negative local start or a boundary that would clamp/drop the clip. App's effective extent
is content-derived and capped there (`timelineOccurrenceEffectiveDurationMs`),
not simply stored `duration_ms`. Do not capture a clamped projection as authored length.
Nondefault occurrence offset/rate, rational-object occurrence rates, nonlinear,
piecewise/reverse/zero-rate maps, timing formulas, nested clips, missing/ambiguous
IDs, contradictory timing codecs and sequence/group moves refuse in v1. Main's
authoring capability check and App projection do not establish a common inverse for those cases;
support requires a versioned operation fixture, not silent scalar fallback.

Fixed means explicitly clear both readable spellings of start `on` (record
present→absent, never null); port R4 `relations.write(start, None)`'s
`app.astrid.fixed_start=true` rule so cut membership cannot reattach it. Main's
numeric `Clip.on`/`_place_on` alone is insufficient: it can author a cut offset.
Freeze the resolved authored duration as `app.astrid.for`, clearing both readable
spellings of end-follow `until` /
`until_film_end` when present, without changing source bounds or unrelated app
data; record container presence/restoration too. Clear/write intent remains
recorded even for unchanged geometry. `expect` holds the original tagged state
of every direct write/clear above, including the local `at`/`at_ms` write;
`authorship` classifies them as direct. `resolved` is the exact singleton and
`created=[]` for this move; consumed old-anchor bindings remain provenance,
not an active follow relation. Framework capture emits these claims, not the UI
or extension author. Recompile timing, without ripple or a
second browser patch/rebase engine. Existing App `moveClip` and drag paths only
materialize patches today; they do not yet meet this contract.

M1 acceptance: real App command service **and drag path** capture sequential
moves and B over unacked A; assert exact captured JSON survives lost ACK, exact
retry and browser restart, then verify original guards at HA and later head.
Cover repeated-source occurrence isolation, nonzero occurrence start, trimmed
positive-rate child, source/map/owner/selection changes, boundary refusals,
clear of a followed start, same-value writes, disjoint rebase and inverse/redo.
Keep equal-state dependent ABA success separate from accepted-inverse ABA/A→A
refusal. Also prove one small structural command (track create, then inverse
refusal with a later dependent and exact restoration when empty) through the
same generic framework with only author schema/handler/intent/fixtures. M0's
fixture guard adapter proves neither capture nor generality. This is M1 proof,
not M0 product work or M2 registry expansion; keep the 20–26k product-line budget. The M1 built-in capture contract is not a promise to transpile arbitrary Python handlers into browser code; do not introduce that framework. Real shared-primitive capture/handler parity and the structural proof must pass before claiming automatic metadata across the supported surface.

### Recorder additions to the canonical schema (proposal for generated DTOs)

`schema_version:1` and per-op `version` are required on the wire before outbox reservation;
builders may omit them only when the installed registry supplies the pinned
supported versions before the outbox is reserved. Additional recorder fields
are optional on initial proposals, complete on accepted records:

```json
{
  "reads": [{"ref":"occurrence:o/clip:c","path":["track"],
             "state":{"state":"present","value":"picture"}}],
  "selections": [{"key":"ripple.members","query_version":1,
                  "owner":"parent","members":["occurrence:o/clip:c"],
                  "order":["occurrence:o/clip:c"],
                  "boundaries":["occurrence:o/clip:c"],
                  "policy":"guard-membership"}],
  "intent": {"ripple":"none","anchor":"fixed",
             "ownership":"occurrence","position":"absolute"}
}
```

Only applicable intent keys occur; each operation schema defines its supported
values and versioned defaults. These are semantic fields, not arbitrary client
merge callbacks. Bindings retain R4's text-to-identity map for compatibility;
typed provenance records in `reads` carry source/document/revision/digest and
clock/time-map dependencies. `created` remains an ordered array of scoped IDs.
The sole canonical M0 design artifact is [edit-command.schema.json](edit-command.schema.json), `$id=https://astrid.local/schemas/timeline/edit-command.schema.json`. [command-schema-handoff.md](command-schema-handoff.md) defines its actual Draft 2020-12 command/batch and semantic-leaf schemas, operation signatures and accepted/rejected examples. The recipe worker's branch-local `schemas/change-contract/edit-command.schema.json` is superseded diagnostic evidence, not a second source.

At M1 authority moves to packaged Agent `astrid/core/timeline/schema/edit-command.schema.json` (already covered by `core/**/*.json` package data); Runtime pins a byte-identical `contract/schemas/edit-command.json`, with generated Python/TS exports from that same contract. Preserve `$id`; check with `cmp` and the existing generated Runtime contract digest checks as detailed in the handoff. Retarget M0 scratch/frozen-ref tests to the packaged schema before product-suite integration. Registry-owned argument schemas extend the common envelope; `CommandBatch` already requires nonempty commands and makes restore the sole command.

M1's minimal `clip.move`, operation `version:"1"`, has numeric `args:{on:<nonnegative absolute timeline seconds>}` and a stable parent/occurrence clip selection. It is fixed, non-ripple, absolute positioning. R4's numeric `clip.on` can be cut-relative, so its adapter must explicitly convert rather than alias blindly. Relative/follow/ripple and shared-scope variants need declared supported operation schemas and their own fixtures. Intentional same-value moves still record writes/history.

`expect`/`authorship` retain their R4 target-key wire encoding, normalized once
at ingress by the canonical parser. New recorder leaves address `ref` plus `path:string[]`,
converting R4 property syntax (dot identifiers, numeric or JSON-quoted bracket
atoms) once. Parent/child overlap compares tokens, not raw string prefixes. IDs locate collection members;
numeric property indices inside an opaque atomic value never select an entity. The handoff defines the one legacy-property-to-token conversion, including quoted `::` keys and numeric container-type reads; never split a target key inside a quoted property. Structural inverse order/source/container restoration is reconstructed from exact historical closure, selection and dependency records; the leaf schema is not permission to discard those facts into a plain diff.

R4 `clip.set` can use `{op:"clear"}` as an operation-specific field value and
`clip.clear` takes `keys`; graph/track setters already use disjoint `values` and
`clear`. Keep these documented command-specific builders during migration; the
schema annotation tells generated controls which explicit clear operation to
emit. The accepted recorder's absent tag is uniform regardless of spelling.
An opaque object equal to `{op:"clear"}` is ordinary data when that parameter's
schema declares an object value, never a global magic deletion sentinel.

Inverse wire is `timeline.inverse`, operation `version:"1"`, `select:null`,
`args:{publications:[<receipt>,...]}`: an ordered nonempty unique list, oldest
to newest in accepted ancestry, all in this timeline. A single publication is
a one-item list. Provider reconstructs the full guarded R4 `writes` from
those authenticated history edges; accepted command records contain the
reconstructed writes and guards, which retries never regenerate. The public
inverse command carries targets only; arbitrary client `writes` are rejected.
An internal adapter can still invoke R4's guarded write executor.
`records.undo_of` is that exact explicit target list; `group_id` is
never an implicit history query. Restore is a sole command `timeline.restore`,
operation `version:"1"`, `select:null`,
`args:{revision_id:<id>,content_digest:<sha256>}`. It uses exact pins per Runtime §5 and
requires the expected current head pair; it is an explicit complete-scope write,
not an inverse and not an escape from authority/history checks.

The `Agent*` leaf semantics are fixed here and structurally specified by the
artifact. `AgentWrite` has `ref,path,before,after`; each explicit write (including
A→A) appears at its execution ordinal. `AgentRead` has `ref,path,state`.
`AgentSelection` has `key,query_version,owner,members,order,boundaries,policy`;
members are unique, order is a permutation of members, and boundaries are bound
stable identities with their read predicates. `AgentBinding` has `key,ref,policy,
dependencies`; dependencies are keys of captured dependency records. An exact
word binding includes its source pin, word ID and occurrence/time-map identity,
not just a `word:` string. `AgentCreatedID` has `ref,kind,owner`; owner is null
only at the root. `AgentDependency` has `key,kind,pin,policy`; kind is entity,
media, transcript, source, time-map or authority. Each kind's registry schema
validates the complete pin (media five-field selection; transcript exact
DocumentPin plus word/source data in its immutable content; source exact closure
IDs/digests). No arbitrary foreign-project or mutable latest pin is accepted.
`AgentDerivedWrite` has `ref,path,before,after,cause`, where cause names an
executed ordinal. Runtime's `CommandRecord` containers supply ordinal, so leaves
do not invent another execution numbering scheme.

Conflict kinds are `same-property`, `delete-vs-edit`, `dependent`,
`selection-changed` and `identity-collision`. Infrastructure/history-unavailable,
invalid schema/parameters and authority failures use Runtime refusal reasons,
not a fabricated semantic overlap. Registered domain facts use main's existing
`clip.*`, `track.*` and other domain vocabulary, map to exactly one executed
ordinal, and include schema-validated stable subject/before/after/intention
data; no snapshot-replacement fact is emitted for an ordinary semantic edit.
Per-operation fact payload mappings remain registry work during M1/M2; no claim
that a new event payload catalog is implemented in M0.

The conformance harness extends main's existing fixture/CLI/Python/sheet runner
rather than creating a parallel journal/framework. Each entry contributes
fixtures and intent assertions. Required cases compare complete authored JSON
including opaque/presence states; deterministic replay with same IDs; inverse
then redo; disjoint and overlapping concurrent writes; A→B→A and A→A; changed
selection/order; deleted anchors and new structural dependents; and invalid
media/source authority. Seeded randomized concurrency supplements these fixed
cases. Identity reservations remain monotonic outside authored content. An explicit format migration is a separate recorded edit, not an exception to authored losslessness: record its prior shape and guarded inverse, or refuse an unsafe reversal. The M0 characterization names the existing unrecorded V2-version difference as a port gap; product conformance must not accept or silently strip it.

Port R4 compiler and `_timing_evaluators.py`; preserve main chapters-as-shots,
transcript identities, rational fps, half-open intervals and explicit time maps.
Shared chapter edits intentionally affect all occurrences; occurrence edits use
main's existing isolated authored owner and source mapping, without a general fork/remap service.
Never silently mutate the chapter used by another occurrence. Existing music
sources/arrangements/switches/ripple basis are authored; generated segments and
timing are derived. Inverse restores the former and recompiles the latter.
Compiler-only derived writes are a migration invariant: inventory and relocate
R4 inverse/music projection calls before removing old writers; do not assert it
already holds. Schema/domain/reference/authority validity gates saves; advisory
checks and Composition scene evaluation do not. Renderer unavailable must have
no effect on save, dry-run, retry or inverse.

## Executable evidence and required source changes

Spikes live in isolated `tests/m0_recipe/`, using main APIs and real frozen R4
source `11caf1d9de291d76f491cf69f7942606b7471d7a` in child interpreters. The
test harness extracts the immutable ref with `git archive` into pytest temp
storage, never checks out a ref or patches product functions. Main fixtures are
reused from `test_authoring_bundle.py` and `test_timeline_restructure.py`.
Media/history port data are explicit fixture inputs, not live Runtime authority.
No fabricated renderer answers are supplied. These tests characterize existing
code, not a replacement miniature editing engine.

| PLAN hard case | Executed observation | Required forward-port work |
| --- | --- | --- |
| Ripple/insert and concurrent membership | `RuntimeCommitService._apply` + `rebase` deterministically insert time; a new concurrent clip silently joins the ripple. Ripple-delete inverse restores original entity states except the explicit V2 upgrade below. | `commands._invoke`/recorder must capture ripple membership/order/boundaries, including negative membership reads; `rebase.rebase` must guard them or apply the declared include-concurrent policy. Do not infer membership from changed paths. |
| Transition endpoints and adjacency | Actual `composite_effects._predecessor` accepts exact adjacent endpoint, rejects inserted predecessor, gap and overlap. Actual audio crossfade guards both endpoint curves. Deleting an endpoint prevents replay. Actual `transitions.admit_transition_changes` refuses a new visual transition without renderer admission. | Preserve `_predecessor` domain checks and explicit endpoint binding; replace renderer admission in `transitions.py` and provider scene preflight with schema/declaration/timing/reference validation. The scene evaluator is not a transition-save dependency. |
| Shared shots, occurrence-local edits and chapters | Main `open_authoring_bundle` creates deterministic independent authored owners for a repeated immutable source; compiling a null setting on one preserves its sibling and opaque fields. Main `split`/`flatten`/`Checkout.stored_document` preserve three chapter shots and parent-owned crossing clip/music. | Keep main `authoring_bundle.py` and `timeline_restructure.py` ownership/representation. Shared intent explicitly selects every intended owner using source mapping; occurrence intent selects one scoped owner. Never port R4's chapter adapter over main wholesale. |
| Existing music, authored vs derived | Real `music_beds.collection`, insertion, `compile_timing` and inverse preserve source/ripple basis, deterministic segment IDs and gain restoration. Insertion/deletion inverse leaves only `parent.config.app.astrid.v: absent→2`. | Authored source/arrangements/switches/basis belong in records; outputs/clocks are compiler consequences. Move `music_beds.edit_source` projection and `inverse.apply_inverse` projection to the compiler boundary. Make legacy→V2 conversion an explicit recorded migration before the measured edit (or in its explicit atomic group). Its prior authored shape and guards must be invertible when safe; later dependents may refuse reversal. The ordinary edit must round-trip exactly from its real base. The observed unrecorded version change is a gap, not an approved conformance exception; never blindly downgrade a managed V2 bed. |
| Transcript anchors and source/word identity | Main transcript IDs distinguish source documents even when word IDs match; retiming changes main's generated word ID. Real R4 frozen snapshot parser verifies source/lineage/revision and exact selected word ID; text cannot substitute for ID. Anchored replay follows the same word after timing moves and refuses a shifted legacy ordinal. | Use main `media.transcript/v1` source/document/version/digest with word/occurrence/time-map pins. Adapt `transcript_binding.py` to Runtime `VerifiedDocument`; do not copy R4's other transcript document codec as canonical. Follow re-evaluates the same identity; fixed records resolved time. Source-word continuity across a new producer version requires an explicit mapping, never text/nearest-time matching. |
| Track create/delete with new dependents | Actual track add requires an absent entity guard and full row. Inverse of creation refuses later population; occupied deletion refuses; empty deletion restores complete row. | Retain `track_users`, root restoration and cross-owner dependent checks in generalized inverse. Extend the same structural primitives to new element/reference kinds; do not replace them with equal-value leaf guards. |
| ID collision and replay | Real add and replay preserve IDs; collision refuses. R4's explicit injective mapping succeeds for an identity-only collision, while duplicate layer names still refuse. | Preserve identity reservations; foundation `id_map` is identity-only and collisions refuse. The observed general R4 remapper is not required to port. App persists generated IDs with in-flight request. |
| Absent/null/clear and unchanged writes | Actual setter records absent vs present-null; explicit clear removes presence and inverse restores null. Intentional same-value setter retains direct authorship/expectation in its call but produces empty `Plan.direct_writes`. | Change `commands.finish_recording` to emit **all declared direct writes**, including unchanged, in execution order; provider/Runtime must accept their publication even if content bytes match. Replace global clear-sentinel interpretation with schema-specific explicit clear adapters where object values would be ambiguous. |
| Immutable authorized media add/swap | Actual provider `_capture_media` checks five-field selection and project, rejects stale catalog and forged trusted records. Actual add/swap preserve identity/anchors, replay captured metadata without discovery, and inverse retains a registry entry used by a later clip. | Adapt `_capture_media` from R4's full catalog-shaped record to Runtime `VerifiedMedia`; Runtime privately verifies its catalog digest/realm/authority and rechecks at acceptance. Never hash the new reduced `VerifiedMedia` as though it were the old catalog record or accept caller `media_record`. |
| Publication ABA, parent/child and ancestry | Local inverse accepts A→B→A; actual provider `_inverse_history` rejects it with a later-write conflict. `publication_chain` distinguishes two publications of one revision and fails on missing edge. Ancestor paths overlap, unrelated prefixes do not. Legacy `overlaps` misses equivalent `params.x` vs `params["x"]`. | Preserve publication-edge traversal, expand common history guards to the final replay policy, compare both head pins, canonicalize paths into token arrays and include ownership/dependent edges across entity IDs. Whole-document legacy publications guard whole scope. Never derive safety from final values or revision equality. |

### Forward-overlay execution blocker

After `port-spike-ready.md` appeared, the same nine R4 cases were run read-only
against `/home/user/work/wt/agt-m0-spike`. All nine fail at
`astrid/sdk/timeline/transaction.py:73`: `Edit._check_context()` imports absent
`astrid.core.pack.checks.CheckAdmissionContext`; `_apply` reaches that method at
the transaction validation boundary (`transaction.py:260`). The overlay's
successful import walk and compiler tests do not establish executable command
acceptance. Required source change: replace that R4 Pack V3 admission-context
dependency with main-compatible structural/reference/timing validation context
and keep optional advisory checks outside save; do not port cut Pack V3
infrastructure or disable transaction checking to make the spike green.
No other worker's files were changed. The frozen-source cases remain the
executable semantic observations while this forward-overlay blocker is fixed.

### Verification and limits

Initial system-Python iterations exposed fixture/API mistakes; those were fixed
without changing product code or disabling assertions. The system-Python final
iteration was `12 passed, 2 warnings in 145.97s` (warnings: missing pytest-timeout
plugin in system interpreter). The first required shared-environment run was
`12 passed in 145.41s`; it was repeated after adding the schema checks and
follow-anchor/path-spelling observations (final result below). No dependencies
were installed or modified by this worker.

Commands run from `/home/user/work/wt/agt-m0-recipe`; logs under
`ORCH/workers/agt-m0-recipe/`, outside git:

* `PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/m0_recipe`
  — **14 passed in 157.21s**, no warnings or skips (`final-spikes.log`).
* `PYTHONPATH=$PWD ASTRID_RECIPE_R4_ROOT=/home/user/work/wt/agt-m0-spike /home/user/work/venv-agent/bin/python -m pytest -q tests/m0_recipe/test_recipe_spikes.py`
  — **9 failed in 14.69s**, all at the exact overlay blocker above (`port-spike.log`).
* `/home/user/work/venv-agent/bin/python -m ruff check --isolated --select E4,E7,E9,F,I,BLE tests/m0_recipe`
  — passed. Isolated configuration is explicit because repo lint excludes tests.
* `PYTHONPATH=$PWD make check PY=/home/user/work/venv-agent/bin/python`
  — blocked at preflight, exit 2: this worktree lacks `remotion/node_modules`
  (`make-check.log`). Shared Python dependencies are ready; no Node install was
  attempted. No claim that the full gate passed.

Linux only. Live Runtime atomicity/retry/credential authority, App browser/outbox
journey, renderer-off provider startup/save, actual Composition preview/export
pixels/PCM, native macOS and full repository default/conformance suites were not
run by this worker. They remain their owners' M1+ gates. Saving without scene
evaluation is the specified contract and an identified required deletion, not a
property proven of frozen R4's current `RuntimeCommitService.commit`.

### Remaining contract handoff

Re-read Runtime's frozen §4.1 before handoff: initial ABI 1, fixed factory,
`provider_id="astrid-v1"`, integer version and exact generated schema digest;
complete timestamp-free `CanonicalDocument` closure on the wire (not internal
Checkout bundles), Runtime-derived accepted/rebased status and publication ID,
token-array conflict paths, `rationale`, explicit inverse publication list and
sole-command historical restore are adopted here. The schema artifact above
supplies the requested semantic leaf names and inverse/restore argument shapes.

Implementation seams: apply the settled dependent-suffix original-guard rule without a client rebase; per-operation parameter/UI annotations and
registered fact payload mappings must be filled in during registry port;
main transcript DocumentPin must replace the R4 transcript codec; compiler-only
derived writes need the named migration and legacy format normalization.
These are source/fixture requirements, not permission to weaken PLAN. Runtime's
bootstrap/baseline mapping and receipt retention are Runtime-owned and adopted
fail-closed. Managers still own review/sign-off; this worker does not approve
Checkpoint A or authorize M1.
