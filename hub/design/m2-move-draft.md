# PROPOSED M2 — first multi/group move and retrack contract

Draft only, 2026-10-19, worker `agt-m2-move-design`. Agent manager owns semantics;
App review and manager approval are required before freezing. This is preparation
under PLAN §4.1 and the approved `drag-milestone-contract`, **not M1 evidence or
permission to implement/merge before the real M1 gate is green**. M1 takes priority.
The final `clip.move` v1 section of [edit-recipe.md](edit-recipe.md) and
[command-schema-handoff.md](command-schema-handoff.md) remain unchanged.

## Smallest operation surface

Propose one new reusable registry entry, `clip.move-set` version `"1"`, for a
singleton retrack, free multi-selection, or complete soft-tag group. These are
builders of the same operation, not three gesture handlers. Reuse `track.create`
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
| `move-set.groups` | Complete ordered parent `config.pinnedShotGroups` rows intersecting the selected members, including an empty result. Guard the member-resolving predicates (`shotId`, `trackId`, `clipIds`, optional `memberSelectors`/`ownerOccurrenceId`) for candidate rows, so an excluded row becoming relevant is detected. Require every touched group's complete ordered membership in the set; no partial group. Bind semantic group refs using frozen R4 `shot_groups.identity`'s base64url JSON `[shotId,trackId]` key. Read the complete touched row to preserve mode/snapshots/opaque data and original group order. |
| `move-set.lanes` (only when `track` supplied) | Complete authored track membership/order, plus each track's `id`, `kind`, `role`, `enabled/active/disabled/hidden/deleted`, including excluded lanes and absence predicates. Derive the editable output order from these facts before computing row offsets. Preserve bindings for every source and resolved destination. Concurrent lane creation/deletion/reorder/role or activity change conflicts. No global lane query for a same-track explicit translation. |
| `move-set.lane-members:<track-ref>` | Complete source/destination clip membership in authored order, and each candidate's track identity (including excluded candidates). Required for retrack ordering; also query destination nonmembers for collision checks. Record active/type predicates, start/window/rate and consumed owner/map/source facts for those blockers; inactive/gap/spacer clips do not become blockers silently. Empty destination is still a query. |
| `move-set.blockers` (occurrence owner) | Complete ordered parent occurrence membership and lane/activity predicates, plus parent lane kind/role/activity, before filtering same-lane output occurrences; read both placement/fallback start spellings. Bind the complete applicable blocker result and absence of a next blocker, not only the nearest winner. These facts bound the candidate against the next output occurrence. |
| `move-set.extent` (occurrence owner) | Complete original ordered child clip membership; raw starts, windows/durations/rates, activity/type and referenced track role/activity for every inclusion predicate. Compute original and complete candidate output content extents from this set, excluding source lanes and inactive/gap/spacer content. Guard all consumed extent inputs, not the cached/stored duration or just the old furthest clip. Tail duration may grow/shrink with content, capped by the hard blocker; never use the current soft tail as an immovable wall. |

The original bundle authenticates parent→occurrence→shot→internal closure pins.
Pins are provenance, not equality guards on the entire containing revision.
Repeated shared shots use main's deterministic occurrence authoring materializer;
only the selected occurrence changes. Duplicate raw IDs in different occurrences
are legal scoped identities; duplicate IDs inside an owner or duplicate input
refs refuse before writing. Never first-match, silently drop missing members,
deduplicate user parameters, or infer occurrence ownership from a projected ID.
For a parent soft-tag row naming occurrence children, require unambiguous scoped
provenance (`memberSelectors`/`ownerOccurrenceId`, or a uniquely proven mapping);
ambiguous repeated-shot `clipIds` refuse. No new group store or persistent ID.

Capture an immutable JSON basis at pointerdown from the same raw optimistic
authoring bundle used by M1, before preview. Finish/drop may choose `on/by/track`
and allocate a new track once; it runs the same built-in materializer on that
frozen bundle. Target-dependent queries read **that bundle**, never current head
or a preview where earlier members have already moved. Preserve original query
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
start as a zero hard duration; test that case explicitly (see review points).
Keep M1's translation-only occurrence map, positive constant child speed, finite
explicit window/duration and matching rational fps restrictions. Nondefault
occurrence offset/rate, nonlinear/reverse maps, formulas, nested clips and
sequence retiming remain unsupported. Fixed move clears both readable start
`on` and end `until/until_film_end` spellings, writes `fixed_start=true` and the
original resolved duration `for`, exactly as M1; source bounds/rate/opaque fields
survive. Explicit clears and unchanged writes remain recorded, never null.

Retrack writes each `track` and preserves unaffected per-lane order; append
incoming members in `members` order. Use structural member/order records to
materialize authored clip collection order and App `clipOrder` consistently,
preserving complete objects; do not serialize rows back through the old lossy
config builder. Update every touched soft-tag's `trackId` and preserve its ordered
`clipIds`, shot identity, mode and opaque content. A changed composite group key
is a guarded relocation of that semantic row: old present→absent, new
absent→present, original container position preserved. Destination-key collision
refuses; never overwrite/merge groups. Group refs stay reads/writes/selections,
not new entries in `resolved` or newly allocated IDs. Extend existing structural
primitives deliberately for this semantic row; do not copy frozen R4 wholesale.

New bottom track: reserve `row.id` once, then submit
`[track.create v1 {row}, clip.move-set v1 {...,track:<new-ref>}]` in one existing
commit. Set capture is over original basis plus **only that explicit create**;
the resulting lane-order/absence facts reference the recorded created ID.
Both commands share `group_id`/rationale, one publication and one undo unit.
Provider execution follows ordinals, validates the complete candidate and
publishes nothing if either fails. Created reservations remain monotonic, retries
reuse IDs, and redo uses the guarded accepted inverse. Top/middle insertion needs
an explicit supported track-order operation; do not hide it in set-move v1.

Ordinary rebase verifies original value/identity/query guards on the new head,
using token ancestry overlap and structural ownership/reference dependencies.
Disjoint opaque properties can pass; changed membership/order, blocker/extent
inputs, destination track deletion, owner/source change or group-key occupation
conflict. Never silently retarget/replan. Existing server history rules apply,
including intervening overlapping A→A/ABA writes; dependent unsent B still waits
for A and uses original value/identity guards at HA, with equal-state suffix ABA
allowed under the settled decision. No suffix/wire redesign here.
Inverse coalesces first-before/last-after for the explicit batch, restores exact
presence, full group objects/container order and source fields, recompiles
mirrors/timing, then removes a created track only after its own moves reverse.
A later dependent clip/reference on that track, target deletion or overlapping
publication write makes the entire inverse refuse; retain accepted ancestry.

## Three preserved App behaviours and the acceptance handoff

Source baseline: App main snapshot `60aa26b95`, file
`src/tools/video-editor/hooks/useClipDrag.test.tsx`. Integration observed at
`0dfb3896545e555c221c5be7a6e1680965b6d004` still contains refusal replacements;
App owns restoring the original success assertions as exactly three `it.fails`
under the orchestrator instruction. This draft changes no tests.

| Original test name | Concrete M2 command/result (parent refs abbreviated below) |
| --- | --- |
| `commits a config edit when a free multi-clip drag drops onto a new bottom track` | Original c1 at0/V1, c2 at2/V2, hold2 each. `track.create(parent,{id:"V3",kind:"visual",...})`, then set `select:c2,members:[c2,c1],on:3,track:V3`. Row delta +1 produces c1 at1/V2 and c2 at3/V3; lanes V1,V2,V3, no group override, selection `[c2,c1]`, secondary ghosts, one transaction. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged across tracks` | Original c1[0,2), c2[2,4) on V1; group shot-1/V1 with those members, mode images. Set `select:c1,members:[c1,c2],on:1,track:V2` gives [1,3),[3,5) on V2, empty V1, order c1,c2 and group trackId V2, other fields unchanged, one transaction/selection. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged onto a new track` | Same group. Create V3, then set `select:c1,members:[c1,c2],on:3,track:V3`; group trackId V3 and clips [3,5),[5,7) there, mode/membership retained, one transaction. The original test only asserts config/group track; additionally assert geometry and accepted readback. |

These parameters are shorthand for the envelope above, **not existing callable
APIs**. Example exact new command for the middle row:

```json
{"schema_version":1,"op":"clip.move-set","version":"1","select":"parent/clip:clip-1","args":{"members":["parent/clip:clip-1","parent/clip:clip-2"],"on":1,"track":"parent/track:V2"},"group_id":"drag-5","rationale":"Move the complete pinned group"}
```

App keeps original expected success effects and points their observation at the
single command service's preview materialization; `applyEdit` is not reinstated
as a publisher. Flip exactly those `it.fails` to `it` only once capture, preview,
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

Planned verification commands (not executed by this design worker):

```bash
# App targeted, from its future implementing worktree:
npx vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/hooks/useClipDrag.test.tsx src/tools/video-editor/hooks/useClipDrag.softtag.test.tsx src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/lib/clip-drag-planner.test.ts src/tools/video-editor/lib/multi-drag-utils.test.ts
# Agent targeted, including newly contributed cases through the existing harness:
PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_conformance.py
# Central browser/socket verification, requested by each implementing worker:
"$ORCH/bin/request-test" "$APP_WORKER" full-e2e-three-products
"$ORCH/bin/request-test" "$AGENT_WORKER" commit-integration
# Wait each returned result directory with "$ORCH/bin/wait-test" "$R".
```

The new tests must be included in these existing suites; browser cases must
actually exercise all three drags, no legacy save traffic and lost-ACK/restart/
inverse, rather than borrowing M1's single-clip pass. Full suites use the central
service once after final implementation edits, per the orchestrator rule.

## Precise review points before freeze

1. Approve the single set operation, one-owner limit, bottom-create composition
   and explicit blocked-placement refusal for the first M2 item. Main's
   `multi-drag-utils.applyMultiDragMoves` can shift a group's position **and source
   window** during collision resolution; this draft deliberately preserves the
   recipe's fixed window instead. Automatic route/snap/gap policy is additional
   M2 work, not evidence from these three non-collision tests.
2. Verify extent/role parity against main
   `data/{shotCompositionTiming,shotCompositionProjection}.ts`: gap/spacer and
   Source filtering, content-tail growth and equal-start hard blockers. Existing
   M1 `capture.py` uses `start>origin`; main's hard-duration helper uses `>=` for
   other occurrences. This is evidence for manager review, not a change to M1 or
   a claim of current parity. The draft proposes fail-closed equal-start bounds.
3. Confirm authored clip order materialization and parent group semantic-row
   relocation coverage in existing structural inverse primitives. Current M1
   only proves track create; frozen R4 group code is reference, not implemented
   support. First M2 acceptance needs exact inverse/order/unknown-field fixtures.
4. Confirm CLI JSON apply, Python queue and sheet mapping ownership before
   implementing conformance cases. The existing conformance README describes
   local Checkout/save, so a passing old scenario alone is not Runtime evidence.

No executable/product test result is asserted by this draft.

## App manager review — 2026-10-19 20:01 UTC (draft only)
The three mappings match the restored original success assertions: free bottom-lane creation preserves row offsets/selection order, cross-lane complete group preserves its semantic row/order/mode, and new-bottom group preserves the full group with additionally asserted geometry. One authored owner plus explicit bottom track.create is a useful initial boundary; no nearest-lane or collision trim fallback is approved. Fixed source windows, original immutable capture, one batch/publication/undo and explicit blocked-placement refusal match App needs. The original tests observe local preview effects; applyEdit must not regain publication authority. Exact3it.fails and their gate exceptions are removed only with real capture/preview/accepted readback/group inverse coverage, not mock submissions alone.
Before freezing: close the documented equal-start occurrence blocker discrepancy with shared executable boundary fixtures (exact contact and zero hard window), and state whether an unchanged pre-existing selected/unselected overlap is refused or preserved; do not accidentally make by:0 change source fields or silently clamp/drop output. Keep parent-group refs to occurrence children scoped and fail ambiguous repeated raw IDs. This is review of the proposed M2 first task, not implementation permission or M1 evidence. M1 mounted real journey remains priority.

## Agent manager review — still proposed, 2026-10-19

The single reusable set operation and explicit track-create composition are a useful minimum; this is not frozen yet. App must prove which raw group rows own the three fixtures before implementation: projected chapter/group caches must not become a duplicate canonical group store. Verify source mapping, stable group identity and exact row/order restoration against main rather than adopt an R4 key by convenience. The common recorder needs an executable collection-order/group-row inverse proof before adding handlers. Capture extent/lanes only where the declared operation actually consumes those queries; preserve disjoint same-child concurrency and test exclusion/negative-membership cases. App review plus exact three original tests, collision/window and equal-start semantics remain prerequisites. No product merge before the real M1 browser gate is green.
