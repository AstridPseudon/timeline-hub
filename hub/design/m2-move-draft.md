# M2 design — migrate legacy groups, then move canonical occurrences

2026-10-19, `agt-m2-canonical-design`; Agent base `4ffbb8b081a57eb5f6d8962c30d02b30660491ae`.
**This task is design only; M1 remains open.** PLAN's decisions log and Agent
INBOX **DECISION on M2 group representation** settle option A. The earlier
soft-tag recommendation in [m2-group-ownership.md](m2-group-ownership.md) is
superseded by [Astra's review](../reviews/astra-m2-groups.md). No implementation,
merge or M1 closure is authorized by this task. The newer 22:35 INBOX permits
separate M2 implementation branches; merging still waits for recorded M1 closure.
`clip.move` v1 remains unchanged.

Canonical shots and occurrences own groups. `config.pinnedShotGroups` is only
an explicit migration input; clearing it consumes that input, never edits a
second group store. No load-time conversion. Implementation dependency sequence
(branch work per 22:35 INBOX; integration only after M1 is recorded):

1. Approved order/staged-inverse groundwork; recorded lossless migration of the
   existing two-clip group; occurrence move to an existing lane; derived App view.
2. Compose existing `track.create` with occurrence move, one acceptance/undo unit.
3. Separately add free multi-clip moves of explicit scoped clips.

All three original App success assertions survive exactly. Local rows/config/
`pinnedShotGroupsOverride` observations describe the compatibility preview/view,
not persistence. No whole-parent/group-array ordinary move, display-ID ownership,
new Runtime endpoint/DTO/ABI, history fields, soft-tag editor or M5 framework.

## Actual source limits and the required seams

Agent paths below are relative to this worktree; App/Runtime integration sources
are read-only. These are inspected limits, not passing M2 behavior:

| Source | Observed limit / bounded required change |
| --- | --- |
| `astrid/sdk/timeline/{commands,capture,_recording}.py` | Registry has clip.move and track.create; inverse/restore are special dispatches. Add the two closed M2 commands below, read-first capture, versioned queries and deterministic recapture. `Recording.create` assumes config collections and the `track.create` query, even for another kind; it is not a shot/occurrence creation API. |
| `astrid/sdk/timeline/_command_state.py:State` | Existing occurrence roots can be read/property-written; missing occurrence lookup raises even with optional=True; root writes split owner/kind and cannot create occurrences/shots. `config(owner)` assumes parent or an existing occurrence. Add explicit root absence/create/remove and shot aggregate resolution, preserving main's occurrence materialization. Do not pretend schema-allowed shot-scoped clips already work. |
| `astrid/sdk/timeline/commit.py:_check_reservations` | Assumes non-null owner and `owner/kind:id`; occurrence root `occurrence:o` does not fit. Generalize by registered semantic identity kinds, with old track records unchanged; see reservation section. |
| `astrid/core/timeline/shot_composition_migration.py` | Reuse contiguous/order/ambiguity checks, not its publisher, activation/receipt machinery, rounded duration, reconstructed parent or recursive `_canonical_provenance` sanitizer. Those lose opaque data. |
| `astrid/core/timeline/authoring_bundle.py`, `astrid/sdk/timeline_editing.py:add_authoring_shot` | Compiler needs complete shot/source mapping. The existing new-shot helper seeds synthetic source IDs/digests; it is not a recorded creation path. Add an explicit new-shot materialization branch backed by accepted creates; never claim an invented source revision was read. Keep exact existing-source reuse/isolation. |
| `astrid/core/timeline/shot_composition.py:_walk_for_legacy` | Recursively rejects even opaque nested `pinnedShotGroups`/clipType=shot. A scope-aware check of actual retired structural fields is required for lossless provenance; do not sanitize unknown nested keys to satisfy it. Test the canonical graph as well as raw codec. |
| Agent `shot_composition_projection.py:_project_clip`; App `src/tools/video-editor/data/shotCompositionProjection.ts` | Both retain raw child track; App line 377 prefers it to occurrence lane. Placement change alone does NOT retrack children. App projection currently omits groups and qualifies display IDs; add the explicitly bound read-side view below. |

## Proposed exact command contracts (not installed)

Both use existing `schema_version:1`, `version:"1"`, optional `group_id`/rationale;
unknown args/intents refuse. IDs are nonempty address-safe strings (no `/` or
`::`), distinct within their semantic scope. Existing `timeline.inverse` and
`track.create` v1 contracts remain. No caller-supplied arbitrary payload patch.

| Operation | Exact closed args, selection and intent |
| --- | --- |
| `timeline.migrate-groups` | `select:"parent"`; `args:{groups:[{legacy_shot_id,shot_id,occurrence_id},...]}`. Nonempty ordered list; all three fields required strings, no other keys. Exactly one entry per original group in original group-array order. `legacy_shot_id` is the original unique `shotId`, not a new group ID. `shot_id` and `occurrence_id` are allocated once before sealing capture/outbox; no defaults/randomness on replay. Effective `intent:{}`; `resolved:[]`. |
| `occurrence.move` | `select:"occurrence:o"`, `resolved:["occurrence:o"]`; `args:{on:number,track?:"parent/track:t"}`. `on` required finite global seconds >=0; optional track must be an exact parent output-lane ref; omitted means retain lane, null refuses. Effective intent `{ripple:"none",anchor:"fixed",position:"absolute",ownership:"occurrence"}`. No shared intent, by/ripple/follow/partial group in v1. |

One explicit guarded migration consumes **all** legacy groups on this parent
before ordinary occurrence editing. This is a one-time broad read/structural
operation, not a broad guard repeated on each drag. Prefer a separate accepted
migration followed by new pointerdown capture on its accepted canonical bundle.
If a UI initiates migration during a drag, hold the dependent move until migration
ACK and retain its original staged claims/IDs; never refresh claims after ACK.
Migration is an explicit action/proposal, not an automatic read-side write.

### Migration admission, preservation and recorded effects

Require an authored array, unique group `shotId`s, ordered unique `clipIds`,
unique parent clip IDs, disjoint groups, existing members contiguous in **authored
array order**, and exact matching `clipIds` order. Duplicate shotId-derived
identities, interleaving, reordered/missing/overlapping membership, legacy nested
shot clips or ambiguous aliases refuse unchanged. No repair/sort/deduplication.
No existing canonical shot is overwritten merely because its ID matches a legacy
shotId; a newly allocated destination must be absent/unreserved. Resolve any
legacy shot metadata from the exact captured immutable input, not latest storage.

First slice accepts one-lane groups, fixed explicit clip timing, translation-only
maps, positive child rate and source windows admitted by M1, matching rational
fps, and representable canonical geometry. Group start is min authored start;
end is max authored end; child starts become start-relative with unchanged raw
IDs/order/windows/speed/hold/opaque fields. No trimming, clamping or quantization
during migration. Canonical `duration_ms` is integer in the existing Runtime
schema: if exact span cannot be represented, refuse unchanged rather than round.
Unsupported timing/source maps remain explicit refusals pending their later slice.

| Recorder part | Exact proposed observation/effect |
| --- | --- |
| Reads | Tagged state of `parent.config.pinnedShotGroups`, config/container presence, every consumed full member row, parent clip mirror/layout presence and equality, every copied full track row plus track order, full copied output context/fps, consumed registry keys and any shot metadata actually consumed. Original parent fields stay in place. Read the full original legacy field once; it is migration input, not a future editable array. |
| Selections | New v1 `migration.groups` (owner parent, ordered proposed occurrence refs from args, boundaries the same; complete legacy rows guarded by the read above), `collection.clips` and `collection.occurrences` (entire original membership/order), and `collection.shots` (existing shot identities). Query results, including empty, use existing members/order/boundaries/policy:guard-membership. Uniqueness and all exclusion predicates are verified before writes. |
| Bindings/dependencies | Fixed `migration.group:<i>` → new occurrence ref, `migration.shot:<i>` → new shot ref, and `migration.member:<i>:<j>` → exact source parent clip ref with its destination occurrence/clip ref recorded as a separate binding. Capture immutable media, transcript DocumentPins, authority and source/map pins through existing dependency kinds. Source/destination mapping is explicit, never inferred from display IDs. |
| Creates | One `shot:S` aggregate per group (full authored shot payload plus internal timeline), then one `occurrence:O` root pointing to it. No new stable clip IDs, internal timeline document IDs, group IDs or shot-item IDs are needed: raw child IDs remain. First slice requires empty canonical item collections; later item-copy support needs explicit preallocated destination IDs/mapping because physical item IDs are global, never silent reuse. Internal revisions use the existing parent timeline_id. New content-addressed revision IDs/digests are compiler outputs, not random allocations. Unsupported legacy items lacking canonical identity refuse; no index IDs. |
| Writes | Full new shot/occurrence root writes (before absent), root removals of consumed parent clips with full before rows, and clear `parent` path `["config","pinnedShotGroups"]` (before full original array, after absent). Preserve ungrouped clips/order and all unrelated parent keys. Mirror updates are derived once. No whole-parent replacement. Record all writes, including unchanged assignments/clears. |

Construct the new internal timeline from the complete selected raw clips, copied
full parent track definitions (authored order) and consumed output/registry
context; leave other parent config/audio/effects/opaque fields on their original
owner. Do not duplicate parent playback content into every child. A supplied
legacy shot's complete raw metadata/items/unknown fields must remain lossless in
its canonical payload or immutable migration provenance, including collisions
with required envelope fields. Do not rebuild through a known-field whitelist.

Proposed occurrence `provenance.group_migration` is an open authored provenance
object: `{legacy_group:<complete original row>,members:[{legacy_clip_id,clip_id},...]}`.
Members have the exact original order and identity mapping. This immutable source
provenance supplies mode/opaque group metadata and legacy aliases to the view;
current timing/lane/membership come from canonical owners. It is not editable
membership or a second authoritative group array. All new provenance keys must
be guarded against collision; preserve existing nested null/absent/order values.
No full parent snapshot is embedded. Original parent rows/legacy field bytes
remain in accepted write-before states for inverse, including original field
absence where a recorded container was created. No recursive sanitizer anywhere.

For the fixture: child c1 at0, c2 at2, hold2/track V1; occurrence O at0ms,
duration4000ms, track/placement.track V1, source_offset0, speed1; shot S is its
new canonical owner. Full original group row/mode images stays in provenance.
Canonical source_mapping is constructed by the new-create materializer; current
helper's fabricated source-shot/revision IDs cannot be presented as accepted pins.
All parent/child/shot images, pins and records accept together or none do.

### Exact migration inverse and redo

`timeline.inverse` names the accepted migration publication. Authenticate its
records/ancestry and guard postimages, original reads, membership/order and
created-identity dependencies. On detached scratch, remove the created occurrence
and shot only after reversing their own consumers; preserve any sibling still
referencing a shared shot. Any later reference blocks deleting that shot. Restore
full parent clip before rows at their original positions and the original tagged
legacy field, without reconstructing it. Restore any created container's original
absence/null exactly. Existing unrelated parent/shot fields survive; this is not
a historical parent/root rewind. The legacy bytes are restored **only** as inverse
of their consumed migration, never as a soft-tag edit operation.

If a move followed migration, undo that move first (or stage both explicit target
publications newest-first), then inverse migration. A later overlapping edit/ABA
or surviving dependent refuses atomically. Redo inverses the accepted inverse,
restores the same created IDs and canonical geometry, and clears the same legacy
field. Never replay a fresh migration with newly allocated IDs on redo.

## Ordinary whole-occurrence move and atomic child retrack

Capture all queries/reads/bindings from one immutable pre-command canonical
bundle. Pointerdown basis must survive structuredClone/JSON/outbox/remount;
finish resolves targets on that basis, plus only an explicit captured track
create. No WeakMap token, live UI selection, preview-mutated read basis or ACK
recapture. Share Python/TS capture/goldens, not gesture-specific metadata tables.

Absolute start is `Q(on)=floor(on*F+0.5)/F` using pinned rational fps, then
milliseconds for placement. Move occurrence start only; retain duration, child
relative starts/order, source bounds/rates and every opaque field. Literal zero
works. Refuse nontranslation occurrence maps, unsupported follows/formulas or
ambiguous start aliases; never infer maps from extent or projection. No `clip.move`
loop: compute complete candidate geometry, validate, then write atomically.

| Capture/effect | Minimal ordinary move scope |
| --- | --- |
| Owner | Read occurrence_id, exact source-shot identity via existing `occurrence:O/shot`, map/source_offset/speed, activity, duration and all placement/start/lane aliases. Authenticate closure pins as provenance, not whole-revision equality guards. Bind `move.owner` and source-shot identity; allow only main's exact occurrence materialization mapping. |
| Members | New `occurrence.members` v1 selects complete occurrence-owned child refs in authored order. Read every inclusion/extent predicate, CLIP_FIELDS/source window and consumed registry/source pins, track identity and any timing relation actually evaluated. Guard membership/order, not arbitrary siblings' bytes. Bind every child ref explicitly; repeated raw IDs in other occurrences are legal. |
| Lane | Read source and destination parent lane id/kind/role/activity; require active compatible editable output lanes. Role absent means output; explicit source/unknown/null refuses; audio is not excluded just by being audio. Guard complete parent lane membership/order only if consumed (e.g. bottom-track creation), not every track value on a same-lane move. |
| Blockers | New `occurrence.move.blockers` v1 selects active applicable destination-lane parent clips/occurrences, excluding O, with complete lane-local membership/order. Lane/activity exclusion predicates are part of this query, not raw value reads of every excluded row. Read selected geometry/source inputs needed for collision/extent; other lanes' starts are not global reads. Query inputs are the recorded command target/args (including omitted-track original binding); replay/inverse use that authenticated context, not new claims. |
| Writes | Write `occurrence:O` `["placement","start_ms"]`; maintain present supported start aliases, and `["placement","track"]` plus `["track"]` on retrack. Record needed container creation/tagged presence. At occurrence app/app.astrid scopes clear supported on/until/until_film_end; write fixed_start=true and resolved for-duration. Never clear/change shared-shot or child temporal anchors merely to move the parent. Unsupported relation semantics refuse. |
| Atomic retrack | Write **every affected occurrence-owned child** `["track"]` to the target lane, including raw tracks which projection would otherwise prefer. First slice requires a complete single-lane group, not remapping arbitrary layered shots. If the destination child track definition is absent, explicitly create its exact full parent destination row with the same captured lane ID, record its absence/order/created ref, and reserve it; occupied incompatible definition refuses. No new ID allocation during handler/replay. |

Validate complete output extent and same-lane blockers using half-open intervals;
exact contact is allowed, equal-start overlapping output is refused (no zero
hard-window exception). Do not clamp projection overhang or shorten windows to
fit. Internal preexisting overlap may persist under whole-group translation;
new selected/unselected overlap refuses. Source windows/hold/speed remain exact.
The new query is not M1 `move.blockers`, whose scope/implementation is narrower.

Occurrence-local retrack materializes only O's child via main's exact mapping;
unchanged sibling occurrences keep the original shared shot/revision and source
pins. Placement-only moves reuse unchanged shot images. Any future shared-shot
content operation requires explicit ownership:shared and separate semantics;
this occurrence command rejects it. No displayID, `(shotId,trackId)` or prefix
heuristic establishes ownership. Undo restores each authored placement/child-track
value and presence from records, then compiles; a cloned child-track created by
this command is deleted only after its own child references are reversed.

After migration, MOVE(A) and MOVE(B) on independent groups/lanes rebase over each
other: scoped property writes, owner/member guards and lane-local predicates
stay disjoint. Same-lane collision/read dependencies can legitimately conflict.
The shared query/rebase layer must compare relevant predicate membership/order
at intervening boundaries, including membership ABA; a change on an unrelated
lane that leaves the exclusion predicate false is not a global row-value guard.
This query-aware footprint is required work, not present M1 selection support.
The one-time migration's broad legacy-array/order guards do not contaminate a
later move. Concurrent identical migrations are not independent; one conflicts
or exact retry returns the original acceptance. Root restore remains global.

## Approved groundwork — original order and common overlap

Retain the prior approved primitive design; these are prerequisites, not a new
collection API/order store. New v1 queries `collection.tracks`, `collection.clips`,
`collection.occurrences`, `collection.shots` select stable owner-scoped identities
in authored order with existing AgentSelection fields and guard-membership.
Empty is a real result; duplicate/missing/foreign IDs refuse. Record exact tagged
container shape; structural create still requires an authored list unless explicit
recorded container creation supplies one. Never normalize absent/null to empty.

Structural writes retain complete raw member roots; property writes remain token
paths, no array-index selectors. A shared restoration helper restores membership,
then arranges **current full objects by identity** into the verified original
ordered-ref vector. Exact member-set checks precede installation. `[A,B,C]` →
`[A,C]` inverse restores the complete B at index1; unrelated newer C fields stay.
No reconstruction, time sort, append fallback or new persisted clipOrder.
First-slice retrack retains authored clip-array order; no promise to append in
selection order. Standalone arbitrary reorder is a later explicit operation.

Use original selections plus authenticated target pre/post closure order and
inverse args.publications/undo_of linkage to reconstruct position for inverse
and inverse-of-inverse. Historical closure is identity/order/container proof,
never replacement row values or a snapshot rewind. Missing proof refuses as
history_unavailable. No new record field absent an actual counterexample.

One shared logical overlap relation must cover coalescing, claim verification,
rebase, intervening writes and inverse; current equal-ref token ancestry is not
enough. Normalize dot/bracket paths once; numeric opaque-array tokens remain
property tokens, not entity identities. Preserve first-before/last-after plus
actual write occurrences, including unchanged writes and clears.

| Address pair | Required relation |
| --- | --- |
| parent.clips / parent.config.clips / parent/clip:c | Same admitted collection/member. Reject divergent mirrors. Whole-array replacement overlaps membership/order and all member descendants; compiler mirror writes are derived. |
| parent.config.tracks / parent/track:t | Collection replacement overlaps row roots/properties/order; another row's opaque property alone does not alter membership/order. |
| occurrence:O/source arrays / occurrence:O/clip:c or track:t | Same rules with exact occurrence owner materialization; shared source occurrences remain distinct. |
| occurrence:O root / its scoped children | Structural owner replacement/removal invalidates all descendant ownership/bindings. Ordinary placement property edits retain precise paths. |
| shot:S aggregate / explicitly bound occurrence descendants | Shared shot changes invalidate dependent owners; occurrence materialization targets only that occurrence. Resolve actual shared-reference edges, not string prefixes. |
| timeline root restore | Existing `overlaps(("timeline",()), anything)` remains global in both directions, including new refs. No exception for equal JSON. |

Whole-array reads guard all bytes; collection selections guard membership/order
and explicit predicates only. Fold nested/alias writes in execution order when
coalescing, so stale whole arrays cannot overwrite later leaves. No semantic
legacy-group-row address is enabled; schema's old shot-group spelling is not an
editable store. Migration field clears retain their real broad conflict scope.

## Approved groundwork — guarded staged inverse and M1 compatibility

The current inverse checks created-track dependents before reversing its own
moves; it refuses create C + move to C. Replace this with authenticated preflight
and detached staged reversal, preserving later-dependent/ABA refusals:

1. Authenticate targets in accepted ancestry, complete records, required boundary
   closures and **all non-target** intervening edges. For noncontiguous targets,
   compare edges relative to each target, not just after the newest one. Check
   normalized writes/reads/selections/bindings before staging; later writes cannot
   be masked by another target's reversal.
2. Verify original final postimages and projected final membership/order/identity
   against immutable head H. Copy H to scratch, preserving disjoint newer fields.
3. Reverse records newest-first and writes in reverse execution order, checking
   each after-state at its corresponding stage. Reverse own consumers before
   creator removal; restore original order after membership changes. Validate
   each target's original reads/selections at its reconstructed input stage.
   Create C selection excludes C at S0; move's includes C at S1. Neither is
   reinterpreted as a single head-time fact or refreshed to H.
4. Just before deleting a created entity, scan staged declared reference edges
   across clips, placements, audio/effects, shot bindings and owners. Later
   dependents survive scratch and block deletion; don't detach/delete them.
   Unknown declared resolver means safe removal is unproven. Never delete a
   still-shared shot. Full reference validation is also required at the end.
5. Install through the same recorder/executor, compile mirrors/timing and validate
   once, then atomically accept. Any bad stage/order/reference discards all work.

New command reads/selections/expect describe its immutable **input**, while each
AgentWrite.before describes that event's actual stage. Inverse's historical
S0/S1 checks stay internal, derived from authenticated targets; do not flatten
them into new public head reads. Capture touched head collection orders before
scratch writes. `finish` must not emit transient scratch values as head guards.

**M1 records remain valid.** Old track.create selection plus full root write
proves append order. Old accepted move/create/inverse/redo commands, claims,
ordinals and digests remain untouched. Reconstruct known v1 intra-command reads
(intent-container creation and inverse writes) from their trusted trace/targets
and exact boundaries, and compare stored values unchanged at matching stages.
Do not reinterpret all old reads as pre-command, drop overlapping reads or demand
new enriched recorder fields retroactively. Select compatibility from trusted
vocabulary/history, never a caller override. Unknown unrecoverable stages/order
fail closed; fixtures must prove supported M1 histories including multiple creates.

M1 `timeline.restore` is already a sole, exact-head-pair, recorded root-pin
operation at this base, not an ordering/migration tool. Preserve its global guard,
verified historical closure, semantic inverse and later-write refusal. No root
restore/snapshot shortcut may implement migration undo or ordinary move undo.

## Schema, semantic kinds, reservations and retry

| Addition | Exact schema/artifact impact versus unchanged carriers |
| --- | --- |
| New shot aggregate `shot:S` | Add this spelling to ScopedId, EntityRef, TargetKey and AnchorIdentity (for command bindings). Define State root value as complete authored `{payload,internal_timeline}`; base/source_mapping bookkeeping is compiler provenance, not caller-editable fields. Root replace is migration/inverse only, no shared ordinary group edit. |
| Occurrence roots and scoped child tracks/clips | `occurrence:O`, `occurrence:O/shot`, `occurrence:O/clip:c`, `occurrence:O/track:t` already fit ScopedId/EntityRef/TargetKey/AnchorIdentity. Add semantic absence/create/remove/resolution, not another spelling. Existing `shot:S/clip:c` syntax is not license for shared edits; remain unsupported outside registered operations. |
| Closed operations | Add MigrateGroupsArgs and OccurrenceMoveArgs, v1 select/intent conditions and admission/registration. Later ClipMoveSetArgs is a separate schema change. TrackCreateParameters is currently closed only in commands.py; publish the existing v1 closed row envelope in the shared artifact without changing its meaning. |
| Semantic created kinds | New `{ref:"shot:S",kind:"shot",owner:null}` and `{ref:"occurrence:O",kind:"occurrence",owner:"parent"}`; child lane creation remains `{ref:"occurrence:O/track:t",kind:"track",owner:"occurrence:O"}`. AgentCreatedID already has open kind/ref and nullable owner: no envelope expansion. Register validators/resolvers/reservation scopes explicitly. |
| Queries/records | New keys named above in open AgentSelection.key/owner/members; new fixed binding keys in open AgentBinding; existing read/write ref strings and TokenPath/AgentState already carry them. No new query/record DTO, stage index, order ref, dependency kind, semantic event or history field. No per-group soft-tag ref. |

Agent owns `astrid/core/timeline/schema/edit-command.schema.json` and native
meaning. Runtime owner refreshes its byte-identical packaged command artifact,
`runtime_protocol/schemas/timeline-commit-bundle.json` projections, generated
Python/TS exports, digest/manifest; Agent refreshes official runtime-client pins;
App refreshes parity types/fixtures. This is an expected command-schema addition,
not a new Runtime endpoint, port DTO/ABI shape, table or compiled-config schema.
Keep schema_version1 and old operation/query semantics; new versions are explicit.

IDs are allocated/captured once before outbox sealing; migration destinations and
new bottom lane ID are in original args/created claims. Extend reservation checks
to typed scopes: shots project-wide, occurrences timeline-wide, tracks owner-wide; validate
materialized item identity occupancy against Runtime's existing item-ID scope too.
Check current occupancy AND all trusted accepted creations across inverse/redo
lineage; no slash-prefix assumption or treating bootstrap as allocation proof.
Undo never frees reservations. Ordinary reuse of retired ID refuses; only trusted
inverse/redo restores the same identity. Preserve original command.created/record
created consistency, duplicate-in-batch refusal and unavailable-history failure.
No random replay IDs, prefix guessing or broadening id_map: it remains identity
pairs only (empty is valid), never legacy→canonical remapping. The explicit
migration provenance/bindings carry that different mapping.

Repeated-shot retrack needs an additional explicit creation case: main's
`_authoring_shot_id` / `_copy_shot_for_placement` already compute exact independent
shot/item identities while opening the bundle. These working slots are not proof
that the IDs were accepted/reserved. Before sealing capture, record those exact
identities if they become persistent creations: shot:S via kind shot above and
`shot:S/item:I` via kind item, owner shot:S. Add this item spelling to ScopedId,
EntityRef/TargetKey/AnchorIdentity and its State resolver/shot-root overlap; existing
item IDs otherwise remain unchanged. No arbitrary new allocation or provider
id_map rewrite. This is required semantic/schema work, not current M1 support.

Creation occupancy must compare the authenticated input CanonicalDocument plus
staged accepted-kind creates, distinct from virtual authoring-slot existence.
Record full newly materialized shot aggregate absent→present before its owned
child writes; item creation facts are contained effects of that aggregate with
exact IDs, not a second items-array writer. Bind the original source and exact
main mapping. Extend common alias/overlap/staged inverse accordingly. Preserve
older M1 records through their verified closure/mapping compatibility path, not
retroactively invented created claims. Repeated-shot accepted reload/reservation
proof blocks that case until this distinction is implemented; singleton migrated
groups do not require these isolation/item creates.

Exact retry after lost ACK/restart returns the same accepted publication/result;
changed same-key payload refuses. Dependent unsent B waits for A ACK, then submits
at HA with original value/identity claims. Equal-state suffix ABA remains allowed
per PLAN. Accepted undo and stale replay retain intervening same-value/A→B→A
protection on overlapping semantic addresses. No predecessor pin is added here.

## Derived App group view and the three unchanged successes

App derives groups from accepted canonical occurrence/child state plus immutable
migration provenance; the view is pinned to actual accepted revision identity.
Each view row carries explicit ownerRef=`occurrence:O`, occurrenceRef and ordered
member clipRefs, with exact source/shot pins. Sidecar maps bind every legacy
clip/display alias to those refs. Display/group IDs and original shotId are
labels only. Readback uses `commands/authoringBundle.ts` plus canonical projection,
never a raw config-only fallback. Reload must reproduce the same view.

Clone the complete legacy group metadata losslessly, then derive current trackId
from canonical placement/child lanes, clipIds from canonical member order through
the explicit alias map, and mode from preserved metadata (images in fixtures).
Do not reuse App's known-field group clone, which drops unknown fields. Canonical
projection currently emits occurrence-qualified IDs; **required App change**:
provide the original unique aliases c1/c2 at the compatibility observation seam,
with bound canonical refs kept separately. Ambiguous alias reuse never chooses
an owner; normal canonical views can retain qualified display IDs. No group-array
serialization/write-back and no ownership inference from an alias or tuple.

Keep original assertions and test names in
`src/tools/video-editor/hooks/useClipDrag.test.tsx` exactly; all three remain
`it.fails` until their implementing slice passes. The `applyEdit` spy observes a
thin local preview notification from the command result, not a legacy publisher.
Its asserted rows/config/override shape is compatibility output only. No tests
are rewritten to expect refusal, and no new accepted-history stack is introduced.

| Original exact test name | Canonical accepted geometry / order / mode; exact inverse/readback |
| --- | --- |
| `updates pinnedShotGroupsOverride when a pinned group is dragged across tracks` | Migrate c1[0,2),c2[2,4) V1 to S/O above; `occurrence.move(select:O,args:{on:1,track:"parent/track:V2"})`. O start1000ms/duration4000ms; both owned children V2, local at0/2, hold2. View V1 empty, V2 c1[1,3),c2[3,5) ordered c1,c2, group shot-1/V2/mode images; exact original rows/metaUpdates/clipOrderOverride/group-array/transaction/selection assertions. Accepted reload matches. Inverse move returns O start0/V1 and both children V1, retaining canonical ownership. Inverse migration then returns exact original parent rows/group representation. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged onto a new track` | After migration, `[track.create(parent,{row:{id:"V3",kind:"visual",...}}),occurrence.move(O,{on:3,track:"parent/track:V3"})]`. O start3000ms; child local0/2, V3, projected [3,5),[5,7), order c1,c2, mode images, parent lanes V1,V2,V3. Keep original type=config and group shot-1/V3 assertions; additionally prove full geometry/reload. Inverse reverses child/placement consumers, removes only its newly created child lane and parent V3, restores O/V1 geometry; redo same IDs. Inverse migration restores original legacy bytes after move undo. |
| `commits a config edit when a free multi-clip drag drops onto a new bottom track` | **Later independent free-set slice**, no legacy group/migration. Parent c1 at0/V1 and c2 at2/V2, hold2; create V3 once, then explicit members [parent/clip:c2,parent/clip:c1], anchor c2,on3,track V3. Lane delta+1 and time delta+1 gives c1 at1/V2,c2 at3/V3, hold2; lanes V1,V2,V3, selection [c2,c1], ghosts and one transaction, no group override. Accepted reload matches original resolvedConfig assertions. Inverse restores c1 at0/V1,c2 at2/V2, full source/opaque rows/order and removes V3; redo reuses V3. |

Track-create capture is S0; following move capture is S1 containing only that
explicit create, original IDs/claims retained. Both share one group_id/publication
and undo unit; failure of either leaves no created lane or partial placement.
Parent V3's ID is allocated once before sealing; a needed occurrence child V3
uses that exact captured lane identity as its scoped created track, not a second
random allocation. This must pass staged own-consumer inverse before dispatch.

## Later free multi-clip slice (separate operation, no group editing)

Proposed `clip.move-set` version1, schema_version1: select exact scoped anchor;
closed args `{members:[ScopedClipRef,...],on?:number,by?:number,track?:ScopedTrackRef}`.
Nonempty distinct ordered members, one parent or occurrence owner; anchor included.
Exactly one of finite on>=0 or signed finite by; if neither normalize by0; null
refuses. track optional, same owner. Intent none/fixed, absolute for on or relative
for by, ownership:occurrence for occurrence owner. resolved equals members.
Quantize one delta (`Q(on)-anchorStart` or `Q(by)`), preserve all relative offsets,
source windows/duration and original authored array order; by0 preserves off-grid
starts. Retrack applies captured editable-lane index delta to each member's source
lane. Missing/out-of-range/incompatible targets, negative starts, cross-owner
relocation and blocked placement refuse the **whole** set; no trim/routing/ripple.

Read/query all members once, original lane membership/order and every inclusion
predicate when row offsets are used, and lane-local collision/extent/source/map
inputs including empty/excluded candidates. Exclude the whole moved set from
blockers; stage final intervals and validate selected-selected plus unselected
collisions before writing any member. Occurrence tail/next hard boundary must be
computed from full candidate output extent without clamping. Shared ownership
refuses. No per-member recapture, group expansion, occurrence-placement edit or
legacy array update hidden in this op. Exact future query names/portable goldens
are frozen in that later slice; it cannot delay migrate+existing-lane delivery.

## Planned behavior evidence — existing suites only; all UNRUN here

Extend `tests/editing_conformance/test_recipe_m1_commands.py`, existing
`test_conformance.py`/`runner.py` and `tests/editing_scenarios/`; no fake receipt
or detached recorder-shape tests as substitutes for authored results:

| Proposed cases | Required result |
| --- | --- |
| Legacy→canonical→inverse→redo | Compare complete authored parent/shot/clip objects, metadata/source windows, original membership/order and alias mapping; unknown nested sanitizer keys clipType/pinnedShotGroups (including null), arrays/order, absent/null/empty containers, opaque shot metadata and exact source/transcript pins. Graph validation plus actual accepted reload, not just JSON encode/decode. Inverse returns original representation/absence/bytes; redo same IDs. |
| Refused shapes | Interleaved/reordered/duplicate shotId, duplicate/missing members, overlap, alias/mirror divergence, unsupported timing/maps/items or nonrepresentable duration: no bundle/input mutation, no partial candidate/publication. No successful behavior test replaced by refusal. |
| Existing-lane group move | Parent placement AND raw child tracks change atomically; source bounds/hold/speed/order/mode fixed. Pure placement probe alone cannot claim retrack. Include exact contact, equal-start blocker, clipped overhang, trimmed speed2 clips, rational fps and clear-presence roundtrip. |
| Repeated shots/concurrency | Two occurrences share a shot/raw clip IDs; edit O only, sibling pins/bytes unchanged. Independent migrated groups on different lanes rebase with original claims. Same-lane blocker change, member/order/owner deletion/recreation, source pin or exclusion predicate change conflicts. One-time migration broad guards tested separately. |
| Ordered restoration/staging | Remove first/middle/last row → inverse exact order → redo; disjoint later row property preserved. Create+move, create+move+create with own consumers, mixed root/leaf writes, noncontiguous targets and inverse-of-inverse. Bad late stage discards all work. Missing historical order refuses honestly. |
| Reservations/dependencies/ABA | Same IDs through retry/reload/undo/redo; retired-ID ordinary create, occupied ID, duplicate batch ID, unavailable history, later clip/placement/effect/audio/shot references block removal. A→A/A→B→A and raw-array/semantic-leaf overlap refuse undo; root restore overlaps every old/new scope. Dependent suffix equal-state ABA retains PLAN's distinct allowed result. |
| M1 compatibility | Fixed accepted move/create/inverse/redo traces (incl. multiple creates and intent-container reads), original claims/digests unchanged, exact effects. Existing restore semantic inverse/global guard unchanged. No retroactive required field. |

Provider coverage belongs beside
`tests/sdk/test_timeline_commit_provider_document.py` and
`tests/editing_conformance/test_commit_runtime_m1.py`: actual canonical provider,
accepted closure/reload, renderer-off, grouped inverse/redo, lost ACK/restart/exact
retry and later dependent/ABA refusal. No synthetic provider receipt proof.
CLI EditCommand batch ingress, Python queue/flush (currently queue_move only) and
sheet start/track adapters must reach this same acceptance; existing local Checkout
runner/save is not evidence of that. Extend existing conformance runner, no new
harness. Add Python/TS golden capture/preview/accepted-bundle equality including
JSON/structuredClone recovery, not independently handwritten guard fixtures.

App owns existing hook/capture/planner/provider suites and central browser
journeys: retain all three original assertion blocks, observe compatibility output,
assert canonical accepted reload/undo/redo and zero legacy save traffic. Enable
existing-lane group first, new-track next, free multi last. Runtime owns existing
commit/door tests for new-command schema pin, real provider atomicity and collision
admission. Socket/browser/full runs use the central service only after final edits;
no service/full/socket test is authorized by this design task.

## Ready implementation split and blockers

| Order / owner | Files and exit boundary (branch work allowed; merges wait M1) |
| --- | --- |
| 1 Agent shared primitives | `astrid/sdk/timeline/{_command_state,_recording,inverse,rebase}.py`, adjacent conformance/provider tests: shared overlap/order and staged reversal with M1 record compatibility, no new fields. |
| 2 Agent schema + migration | `astrid/core/timeline/schema/edit-command.schema.json`; `astrid/sdk/timeline/{commands,capture,commit}.py`; bounded `astrid/core/timeline/{shot_composition_migration,shot_composition,authoring_bundle}.py` adapters. Register shot/occurrence identity/ref semantics and reservations; replace sanitized conversion/new-shot fabricated-source assumption with exact recorded creation. Exit: legacy→canonical→accepted reload→exact inverse. Core shared-file edits coordinated by Agent manager. |
| 3 Agent occurrence move / App view | Same recorder/capture/commands and Agent projection; App `src/tools/video-editor/commands/{semanticGestures,clipMoveCapture,clipMovePrimitives,authoringBundle}.ts`, `data/{shotComposition,shotCompositionProjection}.ts`, `lib/{pinned-group-projection,timeline-domain,clip-drag-planner}.ts`, `hooks/{useClipDrag,useClipDrag.helpers}.ts` and adjacent tests. Exit: first existing-lane success plus explicit owner-bound view and independent-group rebase. Reuse current commitSession/outbox. |
| 4 Agent/Runtime artifact owners | Runtime `runtime_protocol/schemas/` + generated clients/artifact manifest; official Agent/App pin/parity refresh. Existing DTO/ABI stays. Runtime privately validates new-shot creation collisions before `_persist_closure`; no endpoint/second writer/table. Gate step2/3 acceptance on matching artifacts. |
| 5 Agent/App new-track composition | Reuse track.create, record child-lane creates and own-consumer staged inverse. Parent/child V3 removal/redo/reservations + second group success, central accepted journey. |
| 6 Agent/App free set + frontends | Separate clip.move-set schema/handler/capture and existing planner/CLI/Python/sheet adapters; third original success and cross-frontend conformance. No editing of group provenance/store. |

Concrete blockers: M1 remains open for integration; root shot/occurrence recorder support,
lossless scoped legacy validation, new-shot materialization and accepted projection
are unimplemented. `_check_reservations` sees one timeline's history; that cannot
prove project-wide shot absence/reservation by itself. Runtime currently rejects
foreign-project shot scope but upserts a same-project project_shots row; shot_items
also has persisted identity constraints, not an assumed owner-local namespace. **Required
bounded Runtime change**: atomically refuse a claimed new shot ID already used or
retired anywhere relevant (using existing rows/history), while trusted inverse
restoration/materialized existing sources stay valid. Agent's timeline-local
reservation scan alone is insufficient; agree the private admission implementation
before claiming safe creation, without enlarging the provider ABI. If existing
history cannot prove it, refuse/report the exact gap; never assume a random ID
makes the check unnecessary. Existing valid shot-item IDs/media requirements also
need real Runtime persistence proof; do not advertise unsupported legacy images.

## Evidence of this revision

Read-only source inspections used the Agent base above, current App/Runtime
integration files, PLAN, latest Agent INBOX, Astra review and group audit.
`workers/agt-m2-canonical-design/notes/probe.py` ran via shared venv with
PYTHONDONTWRITEBYTECODE=1 and this worktree's PYTHONPATH: exit0. It observes current
schema acceptance but State refusal of missing occurrence/shot roots, unsupported
shot-group resolution, recursive sanitizer loss, contiguous/order refusal, missing
collection/member overlap and existing global timeline-root overlap. See probe.log.
The separate stdlib `notes/check_assertions.py` source comparison exited0: all
three assertion blocks equal App main `60aa26b95` exactly (ignoring terminal blank
space), still it.fails; see source-check.log. Hooks were not executed.
Those are observations of missing support, not implemented M2 tests. No pytest,
make check, vitest, browser, full suite, service, network or install was run.
No product/test/schema/generated files changed; no git merge/commit was run.
