# PROPOSED M2 — first multi/group move and retrack contract

Reconciled design only, 2026-10-19, worker `agt-m2-primitives-design`, Agent
base `7a7acc0eea47b372e15bb7921563b281ada00fb4`. Agent manager owns semantics;
App review and orchestrator approval of group ownership remain required.
This is preparation under PLAN §4.1 and the approved `drag-milestone-contract`, **not M1 evidence or
permission to implement/merge before the orchestrator records M1 complete**.
M1 takes priority.
The final `clip.move` v1 section of [edit-recipe.md](edit-recipe.md) and
[command-schema-handoff.md](command-schema-handoff.md) remain unchanged.

## Current decision boundary

The latest Agent INBOX **M1 CLOSURE HOLD** supersedes earlier closure claims.
The original mounted-path proof remains evidence for its exact tuple; it does
not release M2 implementation. Restored App journeys, failure classification
and the deep audit still gate the orchestrator's M1 record. The interim
`m2-group-contract` approves two groundwork behaviours after that record:
exact original ordered-collection restoration and staged guarded reversal of
composed commands, preserving later-dependent refusals and ID reservations.
Neither approval selects group ownership. This document specifies those shared
primitives first; the move-set operation below remains proposed.

Read [the group ownership audit](m2-group-ownership.md): the three App fixtures
contain authored **parent** clips and `config.pinnedShotGroups` rows shaped as
`{shotId,trackId,clipIds,mode,...}`. That is not a canonical occurrence group.
Its display key `(shotId,trackId)` changes on retrack and is not a persisted
stable group ID. Agent's separate canonical shot graph rejects this migration
key; App's canonical shot projection omits it. The raw CanonicalDocument codec
can preserve it. Preservation alone supplies neither editable ownership nor
accepted readback through the canonical App projection.

The actual alternatives, pending orchestrator/Astra, are:

* Retain explicitly authored parent soft tags and define their command/read-side
  compatibility contract. Independent-row concurrency would require a reviewed
  semantic row address and shared overlap rules. Whole-array recording already
  works but conservatively conflicts across all rows; this is an alternative,
  not approval to bypass the manager's per-row requirement if soft tags win.
* Use canonical pinned shots and occurrence ownership, with a read-side
  compatibility projection for the same App success effects. Existing migration
  copies members into an internal timeline and removes the parent groups/clips;
  dragging the resulting group is an occurrence-placement operation, outside
  the proposed child-clip set operation. Its codec, command and inverse mapping
  must be specified, not disguised as parent retrack.

Both need the missing canonical read/projection seam: command-produced accepted
raw state → canonical App group/row view, preserving identity, membership/order,
mode and opaque data. The legacy publisher is rejected after command history;
it cannot fill that seam. No first-slice persisted occurrence-member fields or
group entity support are assumed. The schema's existing `parent/shot-group:...`
spelling does not mean `State.entity` supports it. Parent groups naming child
occurrence clips have no approved scoped provenance contract; repeated raw IDs
must fail ambiguous resolution. Free occurrence-local selections retain scoped
clip refs and main's existing materializer.

## Approved groundwork: smallest ordered-collection mechanism

Extend the existing `Recording`, `State`, overlap helpers and `inverse.py`;
keep one candidate and one accepted recorder. The scope is structural
create/remove/restoration of the existing owner-scoped track/clip arrays.
It is not a new general collection API, group implementation or ordering store.

1. A structural primitive records a complete **pre-command** collection selection
   using `AgentSelection.{key,query_version,owner,members,order,boundaries,policy}`.
   Proposed built-in keys `collection.tracks` / `collection.clips`, version 1,
   mean all stable scoped member refs in authored order, including empty arrays;
   policy is `guard-membership`. These are new query implementations, not
   existing callable queries. Keep existing `track.create` v1 semantics unchanged.
   Queries guard existence/owner and container shape; reads retain the exact
   tagged state of any container they create/clear. Duplicate member IDs refuse.
   Existing structural create requires an authored list; absent/null/scalar
   collection containers stay unsupported unless a separately recorded container
   creation explicitly supplies one. Never normalize absent/null to empty.
2. Keep root `AgentWrite.{ref,path:[],before,after}` for the **full raw member**,
   including all unknown fields. Property writes retain token paths. Root remove
   changes membership; append-create is deterministic as today. No array indices
   are selectors and no copy of `clipOrder` or row position is authored.
3. A shared State restoration helper takes a verified original ordered-ref
   vector from the trusted target selection/historical boundary. After restoring
   membership, arrange **current full objects by identity** into that order.
   Check the member set exactly before installing it. Never reconstruct rows
   from known fields, sort by time, or append a restored middle row. For
   `[A,B,C]→[A,C]`, undo restores the original B object at index 1; inverse of that
   accepted inverse removes B and returns `[A,C]`. Unaffected objects retain
   newer disjoint fields. Missing, duplicate, foreign-owner or extra members
   refuse; unchanged numeric indices are not evidence of unchanged identity.
4. The recorder retains order as structural selection evidence and records the
   membership-changing full-row writes. The deterministic inverse command's
   existing `args.publications` links to the exact target records/boundaries
   that prescribe restoration position. An accepted inverse is therefore not
   reconstructed from its root writes alone: use its authenticated historical
   pre/post collection orders and target linkage when it becomes a redo target.
   Compare those orders with the recorded selections and write effects. Read
   historical closure **only for identity/order/container provenance**, never
   use it as a replacement undo snapshot or copy its unrelated row values.
   Missing boundary/order proof refuses as history unavailable.

This deliberately avoids a new order-valued virtual entity or unrecorded order
side effect: position is a specified structural effect of the authenticated
inverse, reproducible from its accepted inputs, guarded at both boundaries.
A future standalone arbitrary reorder needs an explicit operation/effect
contract. Existing raw collection `AgentWrite` can express it losslessly but
conservatively; it is not required for these fixtures. In particular **remove
the earlier general promise to append incoming clips in selection order**.
Keep the authored clip array order for first-slice retrack and derive per-lane
order. The three actual fixtures already project to the required order.

Backwards compatibility is part of the primitive, not a migration of history.
Already accepted M1 `track.create` records have the complete `track.create`
selection before their append and a full root write; derive post-order by that
known v1 effect. Accepted M1 move/inverse/redo records retain their original
commands, guards, ordinals and digests. For inverse records whose structural
position is not recoverable from a single pre-selection, use the exact accepted
pre/post closure plus original inverse target linkage described above. Do not
require a new selection retroactively, rewrite accepted records or fabricate a
missing collection. Unsupported/legacy-unknown histories fail closed where
proof is missing; supported M1 move/create/inverse/redo round-trips must remain.

## One address/overlap relation

Token ancestry on equal refs is necessary but insufficient. Normalize logical
addresses in the common State/overlap layer, using the authenticated owner and
layout, and use that same relation for coalescing, claim verification, rebase,
intervening-write guards and inverse. Do not add a gesture-local overlap table.

| Address pair | Required relationship |
| --- | --- |
| `parent.clips`, `parent.config.clips`, `parent/clip:c` | Same logical collection/member in the admitted main layout. Map a physical whole-array replacement to every member/descendant and membership/order; keep clip property writes precise. Divergent mirrors refuse at ingress. Compiler mirror writes remain derived consequences, not independent authored writes. |
| `parent.config.tracks`, `parent/track:t` | Whole collection replacement overlaps the member root/properties and original membership/order facts. Structural add/remove/reorder affects collection queries; a different row's opaque property alone does not change membership/order. |
| `occurrence:o/source` clip/track arrays, `occurrence:o/clip:c` / `track:t` | Same rules in that occurrence's authored owner. Two occurrences of one immutable source stay distinct; use main's exact materialization mapping, never prefix/display-ID guesses. |
| Owner/document root replacement and scoped descendants | Replacement overlaps all descendants and collection facts, even if the final JSON equals the old content. Deleting an owner also invalidates bindings/references. |
| Raw group array versus any future semantic group row | If soft tags win and row addresses are approved, they must join this relation. No group address is enabled in this first slice. |

A read of a whole raw array really does guard its row content; a collection
selection guards only recorded membership/order plus its explicit predicates.
Do not implement precise selections by recording whole-array value reads.
Normalize legacy dot/quoted-bracket paths once. Numeric tokens inside opaque
arrays remain property tokens, never member identity. An opaque atomic object
is guarded as declared by its schema. Cross-address same-value writes count;
canonicalizing equivalent addresses must not drop write occurrences or A→A.
Coalescing retains first-before/last-after **logical effects** and full write
history; when a collection/root effect contains member effects, fold their raw
objects in execution order rather than applying stale arrays after newer leaves.
For structural order, derive initial/final vectors from selections plus the
trusted effect trace, including implicit root membership changes.

## Approved groundwork: guarded staging, not early dependent rejection

Let `S0 --create C--> S1 --move to C--> S2` be one publication, with accepted
records R0/R1. R0's lane selection excludes C; R1's lane selection includes C.
Those are both original facts. Neither is replaced with a head-time selection.
The current inverse checks `_dependents(S2,C)` too early and refuses its own
move. The replacement is a preflight followed by staged reversal on a detached
candidate; failure at any step publishes nothing.

1. Authenticate explicit target publications in accepted ancestry and obtain
   complete original records, their immutable boundary closures where needed,
   and all non-target intervening writes. Build the normalized effect/owner/
   reference footprint. Check it against intervening history **before** staging,
   including writes to all original guarded reads/predicates/collection facts.
   For noncontiguous target publications, classify non-target edges relative to
   each target's position, not only after the newest target. A later write to a
   selected address refuses even if another selected command would mask it.
2. Against immutable current head H, validate the group's final authored
   postimages, exact current membership/order and surviving identity/dependency
   bindings. These are original final expectations projected through the
   group's own recorded effects, not values recaptured from H. Preserve newer
   disjoint fields and references in the scratch copy. A missing/recreated
   target, incomplete history or changed original dependency refuses here.
3. Traverse target records newest-to-oldest, writes in reverse execution order.
   Verify each write's recorded `after` at its corresponding stage before
   restoring its `before`; full-root/container and alias effects must use the
   common normalization. Maintain the actual write trace for execution, rather
   than executing a flat coalesced diff. Reverse R1 on scratch S2 first; C is
   still present. Restore that record's verified original collection order
   after its membership changes, then validate R1's original input
   reads/selections on S1, including its lane order **with C**. Reverse R0 next,
   removing C only once all of its own consumers have reversed. Restore R0's
   verified input collection order, then validate R0's original input
   reads/selections at S0, including C's absence and order **without C**.
4. Immediately before removing a created entity, scan the staged current model
   for surviving declared dependents across all owners: clips, occurrence
   placements, audio/effects, shot bindings, and registered reference edges.
   A later clip/reference is retained on scratch and still blocks deletion;
   it is never detached, moved or deleted on the inverse's behalf. A dependent
   restored by an earlier reverse step also counts. Use declared reference
   edges, not string matching inside opaque data. A declared reference kind
   whose resolver is unavailable cannot prove safe deletion. Complete candidate
   reference validation is the final backstop, not a substitute for those scans.
5. Install the verified candidate through the same recorder/executor, compile
   mirrors/timing once at the normal boundary, validate and atomically accept.
   The accepted reversing writes include A→A, clears and full restored rows.
   No second journal, undo stack, store, snapshot writer or alternate path.

**Stage assignment is part of the design.** New ordinary M2 commands gather
all semantic reads/selections/bindings on an immutable pre-command view before
writes. Create+move has two such views, not one batch-wide read basis. During
capture the set's original basis is advanced by only the explicit captured
create; replay advances by that same command and reserved ID. Check create's
absence/order claims on S0 and move's original claims on S1 on the base, and
on the corresponding staged states over a rebased head. Never verify both
against H/S0, substitute new head values, refresh a predicate or drop a guard
because it overlaps a target write.

Within the inverse, historical target read/selection checks are **internal
stage checks**, retained in their original trusted records. The new inverse
command's own `reads`, `selections` and `expect` must describe its immutable
**input head**. Capture each touched collection's original head order before
any scratch writes, so the accepted inverse supplies its own guarded basis.
Do not copy historical S1/S0 facts into that flat head-read list.
Keep the pre-command input view in Recording: public `expect` is the input
state of each written address; `AgentWrite.before` is the actual state at that
write event. They can differ after an earlier write in the same command.
Stage checks derive from authenticated targets, while new head guards describe
the external basis. `finish` must not accidentally emit transient values as
head expectations. Deterministic recapture verifies supplied claims exactly;
it never refreshes the original authoring claims to make them pass.

M1 compatibility needs an explicit v1 adapter, since today's recorder can read
while creating intent containers and while executing an inverse. Reconstruct
those known read sites against the original v1 write/target trace and exact
historical boundary, compare the stored values unchanged, then check the same
sites at the matching scratch stage. Do not reinterpret every old flat read
as a pre-command read, or discard all reads overlapping writes. If an unknown
operation needs arbitrary intra-command read stages which cannot be recovered,
refuse rather than guess; a future event-index contract would need explicit
approval. It is unnecessary for the proposed read-first move-set and known M1
operations. Use the known v1 capture rules for old records, not equality against
newly enriched recorder output; select that compatibility path from their trusted
operation/query vocabulary and boundary facts, never a caller override.
Add compatibility fixtures for existing accepted inverse records, including
multiple creates, before claiming this adapter works.

## Wire, reservation and retry decision

No new wire field, schema version, provider ABI, endpoint or persistence table
is required for the approved two primitives. Exact existing carriers are
`CommandRecord.ordinal`, ordered `writes`, tagged `AgentState`, the selection
fields above, `reads`, `bindings`, `dependencies`, `created`, and inverse
`args.publications` / accepted `undo_of` linkage plus immutable history pins.
The new collection query keys are a deliberate versioned **semantic** addition
in the existing open `AgentSelection.key` field; register/validate them in
Agent and mirror capture parity in App. They are not already implemented.
No synthetic path such as `tracks.$order`, new ref kind or hidden index field.
If implementation cannot reconstruct exact stage/order from these authenticated
inputs, stop and report the counterexample; do not silently add record fields.

Move-set still requires a new registered operation/version/closed argument
schema and its generated contract pin refresh. That is a separate expected
contract addition, not a claim that this operation exists. Group-specific
schema/address changes remain pending the ownership decision. A future pure
order address would also change `EntityRef`/`TargetKey` and State semantics;
the current schema does not grant it merely because `AgentWrite.ref` is a string.

Created-ID reservation stays in authoritative accepted `commands[].created`
history, scoped by owner, including inverse/redo lineage. Never unreserve on
undo, reinterpret a bootstrap prefix as allocation proof or allocate during
replay. Ordinary new create of a retired ID refuses; only trusted inverse/redo
may restore that exact identity. App allocates a bottom-track ID once before
sealing its batch/outbox and uses it in both commands. Exact-key retry returns
the original accepted result through Runtime's ledger, including after restart;
changed payload under the key refuses. No extra scan for moves with no creates.
Redo targets the accepted inverse, verifies its current head/stage/order guards
and uses the same IDs. Occupied identity or a new dependent refuses atomically.

Same-value writes and A→B→A are not filtered from accepted history. For accepted
inverse and stale-head replay they conflict at normalized overlapping writes,
reads and structural predicates, even when final values/order match. The
settled dependent unsent B rule is distinct: hold until A ACK, send at HA with
B's **original value/identity guards**; equal-state suffix ABA is allowed. Do
not add a predecessor field or turn that decision into blanket inverse safety.

## Smallest operation surface

Propose one new reusable registry entry, `clip.move-set` version `"1"`, for a
singleton retrack or free multi-selection, and conditionally a complete group
only if approved ownership maps it to such a clip set. These are builders of
the same operation, not three gesture handlers. Reuse `track.create`
v1 for a new bottom lane. No new transport DTO, recorder, inverse or undo stack.
`clip.move` v1 remains absolute, fixed and non-ripple with its original capture.

| Field | Exact proposed meaning |
| --- | --- |
| Envelope | `schema_version:1`, `op:"clip.move-set"`, `version:"1"`; existing optional `group_id` and `rationale`. Unknown args/intents refuse. |
| `select` | Exact scoped anchor clip, `parent/clip:c` or `occurrence:o/clip:c`; must occur in `args.members`. It need not be the first/earliest member. |
| `args.members` | Required nonempty ordered array of distinct scoped clip refs, all one authored owner. This is explicit original membership, never a live UI selection. Defaults: none. `resolved` is this same ordered array. |
| `args.on` / `args.by` | Mutually exclusive finite numbers in **global timeline seconds**. `on>=0` sets the anchor's absolute start; signed `by` translates the original set. If both omitted, normalize to `by:0` (pure retrack). Null is invalid. |
| `args.track` | Optional exact scoped destination track for the anchor, in the same owner. Omission retains the anchor's source track. Never a row number, name, inferred owner or null. Other members retain their original row offsets as below. |
| Intent | `ripple:"none"`, `anchor:"fixed"`, `position:"absolute"` for `on`, otherwise `position:"relative"`; add `ownership:"occurrence"` for occurrence-local members. Normalize effective defaults; supplied intent must agree. No follow/shared/ripple policy in this version. |

Let original global starts be `s[i]`, anchor start `a`, and rational fps `F`.
Use M1's boundary rounding, `Q(t)=floor(t*F+0.5)/F`, with Python/TS parity.
Absolute mode uses `delta=Q(on)-a`; relative mode uses `delta=Q(by)` (including
negative deltas). Write `s[i]+delta`, preserving every original relative offset
and duration. Quantize the one translation, not each member/end independently;
`by:0` must preserve an originally off-grid start. Preserve off-grid relative
offsets rather than silently stretching a group. Refuse any resulting negative
owner-local start. Do not clamp individual members or change source windows.
For group-label drags the UI's target is the group bounding start: convert to
anchor `on = droppedBoundingStart + (a - originalBoundingStart)` using the frozen
basis. Thus clicking a later group member does not collapse its earlier siblings.

For retrack, take the ordered editable output lanes in this owner, compute the
anchor's destination-index minus source-index, and apply that integer offset to
every member's original lane index. Missing/out-of-range/incompatible targets
refuse the whole command. Compatibility requires the same authored track kind,
an active editable output lane, and supported role. Use main's output/source
role classifier (`role` absent means output; `"output"`/`"source"` are the only
explicit values; null/unknown refuses); audio output is not excluded merely
because it is audio. Active means enabled/active are not false and
disabled/hidden/deleted are not true; muted content still has temporal extent.
No nearest-lane search or server choice of a different destination occurs.
Complete groups must land on one lane; mixed source lanes in a soft group refuse.
Cross-owner/parent-to-child/cross-occurrence relocation, shared-shot editing,
source/data lanes, and moving occurrence placements themselves are unsupported.
Two independent commands may target separate owners in one commit, without
implying one cross-owner relative transform.

## Original capture and the queries that actually matter

Use the existing capture/execute/record/replay path and instrumented
`read/select/bind/write/clear/create` primitives. Extend their reusable authored
collection queries; do not add metadata assembled by individual gesture handlers.
Selections use existing `AgentSelection` fields, `query_version:1`, stable refs,
`guard-membership`, exact original members/order/boundaries, including empty
results. Query inputs come from operation args and bound owner/track identities;
keys below are versioned built-in query names, not a new query DTO.

| Query / original dependencies | Required capture and use |
| --- | --- |
| `move-set.members` | Every requested member, in input order; require exactly one match per scoped ref. For **each** member reuse the complete M1 clip/source/window/rate/relation/container/owner/map/fps capture table, including absent alternate codecs and registry source fields. All starts and lengths come from raw authored state, never clamped projection rows. |
| Group membership/provenance | **Pending ownership decision.** The actual parent fixtures resolve `shotId`, `trackId`, ordered `clipIds` and full raw group objects. If soft tags win, guard intersecting membership and exclusion predicates, require complete groups, preserve every field and original row position, and resolve destination-key collisions. If canonical occurrences win, specify a placement command and compatibility projection instead. No callable `move-set.groups` query or semantic group-ref support is asserted here. |
| `move-set.lanes` (only when `track` supplied) | Complete authored track membership/order, plus each track's `id`, `kind`, `role`, `enabled/active/disabled/hidden/deleted`, including excluded lanes and absence predicates. Derive the editable output order from these facts before computing row offsets. Preserve bindings for every source and resolved destination. Concurrent lane creation/deletion/reorder/role or activity change conflicts. No global lane query for a same-track explicit translation. |
| `move-set.lane-members:<track-ref>` | Complete source/destination clip membership in authored order, and each candidate's track identity (including excluded candidates). Guard lane membership/order used by the plan and query destination nonmembers for collision checks. Record active/type predicates, start/window/rate and consumed owner/map/source facts for those blockers; inactive/gap/spacer clips do not become blockers silently. Empty destination is still a query. |
| `move-set.blockers` (occurrence owner) | Complete ordered parent occurrence membership and lane/activity predicates, plus parent lane kind/role/activity, before filtering same-lane output occurrences; read both placement/fallback start spellings. Bind the complete applicable blocker result and absence of a next blocker, not only the nearest winner. These facts bound the candidate against the next output occurrence. |
| `move-set.extent` (occurrence owner) | Complete original ordered child clip membership; raw starts, windows/durations/rates, activity/type and referenced track role/activity for every inclusion predicate. Compute original and complete candidate output content extents from this set, excluding source lanes and inactive/gap/spacer content. Guard all consumed extent inputs, not the cached/stored duration or just the old furthest clip. Tail duration may grow/shrink with content, capped by the hard blocker; never use the current soft tail as an immovable wall. |

The original bundle authenticates parent→occurrence→shot→internal closure pins.
Pins are provenance, not equality guards on the entire containing revision.
Repeated shared shots use main's deterministic occurrence authoring materializer;
only the selected occurrence changes. Duplicate raw IDs in different occurrences
are legal scoped identities; duplicate IDs inside an owner or duplicate input
refs refuse before writing. Never first-match, silently drop missing members,
deduplicate user parameters, or infer occurrence ownership from a projected ID.
The actual three group fixtures name parent clips only. Do not extend them to
occurrence children by inventing persisted member provenance; that contract is
missing and remains pending. Ambiguous repeated-shot raw IDs refuse.

Capture an immutable JSON basis at pointerdown from the same raw optimistic
authoring bundle used by M1, before preview. Finish/drop may choose `on/by/track`
and allocate a new track once; it runs the same built-in materializer on that
frozen bundle. Target-dependent queries read **that bundle** (plus only the
explicit captured create for a new lane), never current head or a preview
where earlier members have already moved. Preserve original query
claims with the finalized commands. The local basis can contain the existing
bundle and command seed; it is local data, not a new wire field. It must work
after `structuredClone`, JSON stringify/parse, outbox recovery and host remount;
no WeakMap/object-identity-only token. Python and TS consume identical golden
inputs and compare claims, authored result and preview. ACK never recaptures.

## One simultaneous plan, one atomic result

Within a set command, compute **all** queries, transforms, bindings and guards
against one immutable pre-command read view. Exclude the entire moved set from
destination blocker queries. Stage every final interval, validate the union,
then write in `members` order. No per-member call to `execute(clip.move)` and no
recapture after the first write. Intermediate writes cannot feed later queries.
Half-open endpoints may touch. Existing internal overlap within a set is preserved
under translation on the same lane; refuse newly introduced selected-selected
overlap on a destination lane and any selected-unselected active overlap there.
This first version refuses blocked placement; it does not shift a source window,
ripple nonmembers, route to another lane or choose a nearest gap. Snaps to
siblings/hard walls and automatic collision routing stay unsupported until their
versioned query-driven policy has parity fixtures. Literal `on:0` is supported.

For occurrences require the complete candidate output extent before the next
same-lane hard boundary, with exact contact allowed; no projection clamping or
dropped overhang. Main's timing helper treats another occurrence at the same
start as a zero hard duration; test that case explicitly before freeze.
Keep M1's translation-only occurrence map, positive constant child speed, finite
explicit window/duration and matching rational fps restrictions. Nondefault
occurrence offset/rate, nonlinear/reverse maps, formulas, nested clips and
sequence retiming remain unsupported. Fixed move clears both readable start
`on` and end `until/until_film_end` spellings, writes `fixed_start=true` and the
original resolved duration `for`, exactly as M1; source bounds/rate/opaque fields
survive. Explicit clears and unchanged writes remain recorded, never null.

Retrack writes each `track` and preserves authored clip array order; derive
App per-lane order from those complete existing rows. Selection order remains
intent/selection order, not a hidden reorder request. The exact three fixtures
need no clip-array reorder. Do not serialize through the old lossy config or
group clone builder. Group result mapping remains conditional: retained soft
tags would update the full original group's `trackId` in its original array
position with unchanged ordered `clipIds`, mode and opaque fields; canonical
ownership needs its different placement/projection mapping. Neither permits
key collision, implicit merging or a second publisher. Semantic group-row
addressing is a pending contract, not existing first-slice support.

New bottom track: reserve `row.id` once, then submit
`[track.create v1 {row}, clip.move-set v1 {...,track:<new-ref>}]` in one existing
commit. Set capture is over original basis plus **only that explicit create**;
the resulting lane-order/absence facts reference the recorded created ID.
Both commands share `group_id`/rationale, one publication and one undo unit.
Provider execution follows ordinals, validates the complete candidate and
publishes nothing if either fails. Created reservations remain monotonic, retries
reuse IDs, and redo uses the guarded accepted inverse. Top/middle insertion needs
an explicit supported track-order operation; do not hide it in set-move v1.

Ordinary rebase uses the common overlap and staged original-guard rules above.
Disjoint properties can pass; changed consumed membership/order, blocker/extent,
source/owner or destination identity conflicts. The two groundwork primitives
must pass their own acceptance nodes before create+move is enabled. A group
operation additionally waits for ownership and canonical projection approval.

## Three preserved App behaviours and the acceptance handoff

Read-only current App `dd376d5e03892276a6335a055b40fa16447d6f9b`, file
`src/tools/video-editor/hooks/useClipDrag.test.tsx:827,1173,1283`, already has
exactly the three original success cases as `it.fails`. Their expectations stay
exact; this task changes no App tests. Group fixtures originate in
`makePinnedGroupData` at line 191, with parent `config.clips` and parent soft-tag
rows, not occurrence children. The group mappings below describe required
observable effects; they do not settle their future persisted representation.

| Original test name | Concrete M2 command/result (parent refs abbreviated below) |
| --- | --- |
| `commits a config edit when a free multi-clip drag drops onto a new bottom track` | Original c1 at0/V1, c2 at2/V2, hold2 each. `track.create(parent,{id:"V3",kind:"visual",...})`, then set `select:c2,members:[c2,c1],on:3,track:V3`. Row delta +1 produces c1 at1/V2 and c2 at3/V3; lanes V1,V2,V3, no group override, selection `[c2,c1]`, secondary ghosts, one transaction. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged across tracks` | Original c1[0,2), c2[2,4) on V1; group shot-1/V1 with those members, mode images. Set `select:c1,members:[c1,c2],on:1,track:V2` gives [1,3),[3,5) on V2, empty V1, order c1,c2 and group trackId V2, other fields unchanged, one transaction/selection. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged onto a new track` | Same group. Create V3, then set `select:c1,members:[c1,c2],on:3,track:V3`; group trackId V3 and clips [3,5),[5,7) there, mode/membership retained, one transaction. The original test only asserts config/group track; additionally assert geometry and accepted readback. |

These parameters are shorthand for the envelope above, **not existing callable
APIs**. The following is a proposed parent clip-set translation only: its group
ownership/update effect cannot freeze until the pending decision supplies it.

```json
{"schema_version":1,"op":"clip.move-set","version":"1","select":"parent/clip:clip-1","args":{"members":["parent/clip:clip-1","parent/clip:clip-2"],"on":1,"track":"parent/track:V2"},"group_id":"drag-5","rationale":"Move the complete pinned group"}
```

App keeps every original assertion (including config/rows previews, override
shapes, transaction count, selection and ghosts) exact. Adapt the test boundary
to observe the single command service's equivalent local preview notification;
that notification must not reinstate `applyEdit` as publication authority.
Flip exactly those `it.fails` to `it` only once capture, preview,
real commit/readback and grouped inverse pass. Preserve all neighbouring stale
selection/group-label tests. Add simultaneous self-blocking/collision cases,
destination/group deletion or membership reorder, same-value write, ABA inverse,
trimmed speed2 source-window preservation, repeated-shot isolation, duplicate
IDs, clone/reload and dependent B cases. Do not replace successes with refusals.

Agent owns schema args/version registration, shared query/structural primitives,
handler/capture/replay/inverse and `tests/editing_conformance` fixtures, starting
from `astrid/sdk/timeline/{commands,capture,_recording,_command_state,inverse}.py`.
Reuse the current scenario runner with YAML cases under
`tests/editing_scenarios/` for the three examples, relative/pure retrack, explicit
clears and occurrence isolation. Each runs CLI **EditCommand batch ingress**, Python
session queue/flush, and sheet edits to both starts and tracks as one batch,
comparing authored JSON, undo/redo, IDs and records. Existing CLI `apply`/session
builders must be wired to these same ops; current `timelines apply TL FILE` is
sheet-only, not JSON command ingress, and current Python session exposes only
`queue_move(select,on)`. Generic batch ingress and sheet adaptation are required
handoff work; do not claim today's local writers already commit through Runtime.
No speculative convenience flags.
Runtime only refreshes the byte-identical packaged schema/generated exports via
the existing handoff; no endpoint/ABI changes. App owns
`commands/{semanticGestures,clipMoveCapture,clipMovePrimitives}.ts`,
`lib/{clip-drag-planner,multi-drag-utils}.ts`,
`hooks/{useClipDrag,useClipDrag.helpers}.ts` and their tests. Reuse
`commands/authoringBundle.ts` and existing outbox/session/preview materializer.

## Future acceptance nodes in the existing suites — all UNRUN

Add these precise proposed nodes to
`tests/editing_conformance/test_recipe_m1_commands.py` (extend the existing
suite, not a new recipe harness). Names are acceptance targets, not present or
passing tests. Keep all current M1 expectations, including
`test_structural_group_uses_generic_creation_and_restores_order`, which presently
covers appended creates rather than middle deletion.

| Proposed test node | Required assertions |
| --- | --- |
| `test_middle_member_delete_inverse_restores_original_order` | Tracks A,B,C with opaque/null fields: delete B → A,C → inverse A,B,C → redo A,C. Parameterize first/middle/last, parent/occurrence tracks and supported clip removal; compare complete authored JSON and full objects, not sets. Preserve unrelated later C fields. |
| `test_structural_inverse_guards_original_membership_and_order` | Added/removed/reordered/duplicate members, owner replacement and equal-looking delete/recreate refuse. Empty collection is a real selection. Changed container shape/presence refuses; no append fallback. |
| `test_mixed_commands_keep_every_original_stage_guard` | Create D, delete B, move an existing clip, then another move to the same clip; one atomic batch, first-before/last-after result and exact staged inverse/redo. Original reads/selections retain their values at each command input. A bad late guard or reversed write failure leaves input untouched and no publication. Use only registered commands once ported. |
| `test_create_track_and_move_inverse_reverses_own_dependents_first` | Create C plus singleton retrack and multi-set retrack to C; undo reverses all own moves before deleting C; redo restores the identical row/ID/order. Assert create's lanes exclude C and move's lanes include C, including clone/JSON recovery and replay. |
| `test_inverse_of_create_move_create_preserves_dependency_order` | Two creates and two moves consuming them, including a move away from the first created track; inverse reverses the actual trace. Test inverse of accepted inverse as one ordinal and a target list spanning publications with non-target edges. |
| `test_staged_inverse_refuses_surviving_later_references` | Parameterize later same-owner clip, cross-owner `track_ref`/`owner_ref`, occurrence placement, effects/audio and shot binding; every later reference survives scratch and blocks deletion. Removing that dependent through a separate accepted edit permits undo only if all other original guards still hold. |
| `test_collection_alias_overlap_catches_same_value_and_aba` | Physical whole arrays vs semantic row leaf in both directions, top/config clip aliases, owner roots and token aliases. A→A and A→B→A publications refuse undo/rebase despite equal final JSON/order. Disjoint row properties pass with precise membership selections; test changed exclusion predicates too. |
| `test_structural_inverse_preserves_unknown_and_absent_states` | Full unknown row/nested object/array data, missing/null/empty containers, explicit clears, mirror layouts and off-grid values survive forward/undo/redo exactly. Unsupported structural container shapes refuse without normalization. A later disjoint opaque edit survives all directions. |
| `test_m1_accepted_record_compatibility_after_structural_upgrade` | Fixed pre-upgrade M1 move/create/inverse/redo recorder fixtures; original commands/guards/digests unchanged, no new required fields, exact results. Include multiple appended creates and intent-container reads. Missing history/order evidence refuses honestly; supported old records still pass. |
| `test_created_ids_retry_redo_and_retired_collision` | Same bottom-track ID in create, move and accepted records; reload/exact retry uses the same publication/ID, undo retains reservation, ordinary retired-ID create refuses, trusted redo restores it. Occupied ID, duplicate batch IDs, changed same-key payload and unavailable reservation history refuse. No new ledger. |
| `test_composed_capture_expectations_describe_input_not_transient_state` | Inverse structural restore and mixed root/leaf writes: `expect` and public reads describe that inverse's input; individual write `before` can describe a later scratch stage. Supplied claims round-trip exactly; changing either external or original historical stage claim fails. |

Extend `tests/editing_conformance/test_commit_runtime_m1.py` beside
`test_cli_python_outbox_restart_and_guarded_inverse` with proposed
`test_composed_create_move_restart_retry_inverse_redo`: actual provider/Runtime
acceptance and history, complete accepted before/after readback, lost ACK,
restart, exact retry, one publication and IDs, grouped inverse/redo, and later
reference/ABA refusals without partial state. Run socket/live parts centrally.
A local primitive probe cannot stand in for that test.

Use the existing `test_conformance.py` / `runner.py` and YAML scenarios with
valid existing `structure.*.*` IDs, e.g.
`structure.remove.middle-track`, `structure.move.multi-bottom`,
`structure.move.group-cross-track`, `structure.move.group-bottom-track`.
These proposed scenarios require CLI EditCommand batch ingress, Python batch
queue/flush and sheet start/track edits to reach the same Runtime path. Today's
runner uses local Checkout/save and is not yet that evidence. Registry removal
and frontend adapters must land before those scenarios can claim acceptance.
Do not invent a callable track-delete op in this design merely to run a probe.

App retains exactly the three `it.fails` success expectations above, with all
neighbouring stale-selection/group-label behaviour. Flip to `it` only after
capture/preview/real accepted readback/grouped inverse, including preservation
of unknown group fields, succeeds on the chosen representation. Add Python/TS
portable parity for create S0 vs set S1, lane/order exclusions, trimmed speed-2
windows, occurrence isolation, equal-start hard blockers (zero hard window),
exact contact, and off-grid translation. An unchanged pre-existing
selected/unselected overlap is refused by this proposed fixed non-collision
slice; by:0 on an otherwise admissible selection preserves exact starts and
source windows. No collision trim/routing fallback is approved.

Planned commands after implementation (not run here):

```bash
PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_conformance.py
# Socket/provider integration through the central service, after final edits:
R=$("$ORCH/bin/request-test" "$AGENT_WORKER" commit-integration) && "$ORCH/bin/wait-test" "$R"
# App targeted hook/capture/parity files in the implementing App worktree:
npx vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/hooks/useClipDrag.softtag.test.tsx src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/lib/clip-drag-planner.test.ts src/tools/video-editor/lib/multi-drag-utils.test.ts
```

App browser coverage must exercise all three drags, zero legacy save traffic,
accepted projection, lost ACK/restart and inverse; reuse the central named
journey lane with added cases, not M1's single-clip counts. Future implementing
workers request full suites only once after final changes per the central rule.
This design task requests neither merge nor full tests.

## Evidence, limits and dispatch after M1 is recorded

Read-only sources: PLAN and Agent INBOX latest closure HOLD/interim decision;
[edit-recipe.md](edit-recipe.md); [group audit](m2-group-ownership.md) and its
external `workers/agt-m2-group-audit/probe.py` / `probe-python.log`; Agent base
7a7acc0e `sdk/timeline/{_command_state,_recording,commands,capture,inverse,rebase,commit}.py`,
packaged `core/timeline/schema/edit-command.schema.json`, and the three existing
conformance test/runner files above (Agent paths under `astrid/`). App
`dd376d5e` fixture/expectations were inspected directly, as were the audit's
source/projection findings. No App files were edited or suites run. A read-only source check compared all
three positive assertion blocks to App main snapshot `60aa26b95`: identical
assertion text (ignoring a terminal blank line); all three remain `it.fails`.
The check is `workers/agt-m2-primitives-design/check_sources.py`, exit 0, output
`source-check.log`. This is source comparison, not hook execution.

Offline observation only, exit **0**:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-m2-primitives-design /home/user/work/venv-agent/bin/python "$ORCH/workers/agt-m2-primitives-design/probe.py"
```

Output is `workers/agt-m2-primitives-design/probe.log`: current middle deletion
restores A,C,B; full row remains intact; raw collection vs member overlap is
currently false; create's selection excludes C while the following stage's
selection includes it; composed inverse currently refuses its own dependent.
The existing selection/write leaves used by the probe validate against the
packaged schema. The move is constructed with existing recording primitives,
not a registered retrack operation. **No proposed algorithm is executed or
proven by this probe; it is not repository conformance.** It corroborates the
audit's two gaps and the stage distinction. Repo tests, actual M2 publication,
projection/readback, browser/restart/redo and full gates are **UNRUN by design**.

Size tradeoff: add one structural-selection/restoration helper and shared
address normalization, then refactor guarded inverse into preflight and reverse
execution in the existing modules. Retaining exact ordered-ref vectors and
using existing immutable history avoids array snapshots in every leaf record,
new stage fields, virtual order refs and another store. Historical boundary
reads cost more for legacy inverse/order reconstruction; cache only within one
request, and fail closed when unavailable. No product line estimate is claimed
before implementation; prefer this bounded change over a general event journal
or arbitrary reorder feature. If a concrete parity case proves a missing stage
cannot be reconstructed, report it as a contract blocker before adding fields.

Ready-to-dispatch split **after the orchestrator's M1 record**:

1. Agent primitives worker: shared owner/layout/address overlap plus structural
   selection/position restoration; M1 historical compatibility and first/middle/
   last deletion nodes. No group handler or product schema expansion.
2. Agent inverse worker, after that seam: preflight, stage-aware original-guard
   validation, reverse trace and deferred created-entity dependent scans;
   multiple creates, inverse-record expectations, later dependents, ABA,
   reservation/retry/redo nodes. Keep publication ancestry checks and exact
   original guards. One module owner at a time where files overlap.
3. Agent move-set/capture worker after primitive proofs: register the reviewed
   operation, fixed transform/collision queries and create→set stage parity;
   CLI/Python/sheet adapters in a bounded follow-up. Runtime consumes only the
   official schema artifact refresh for the registered op, with no new DTO/ABI.
4. Agent/App group/projection work waits for the orchestrator/Astra choice and
   a concrete projection contract. Then App consumes shared capture, preserves
   the exact three success assertions, and adds real grouped readback/inverse
   coverage on the sole commit path. Canonical occurrence ownership may require
   replacing the proposed group use of move-set with a placement operation.

Blocking only group dispatch: ownership, lossless canonical projection and (if
soft tags are retained) reviewed row concurrency/addressing. Before freezing
move-set, settle equal-start boundary parity with shared fixtures and confirm
frontend batch ingress mapping. These do not block drafting the two approved
primitives; M1 closure still blocks all M2 implementation/landing. No new
orchestrator decision is claimed by this revision.
