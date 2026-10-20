# Whole-occurrence move and retrack — App review handoff

Source: `/home/user/work/wt/agt-m2-retrack-recover`, base `e4338c48`.
This is a branch implementation and portable capture handoff, **not an official
artifact freeze or M2 integration approval**. PLAN still records M1 open. Frozen
Bundle1 and R4 refs are unchanged. Legacy admission/migration is a separate slice.

## Exact command and capture

`schema_version:1`, `op:"occurrence.move"`, `version:"1"`.
Select the stable root `occurrence:<raw occurrence_id>`; `resolved` is exactly
`[select]`. Closed args are `{on:number, track?:"parent/track:<raw lane ID>"}`.
`on` is required finite nonnegative **GLOBAL seconds**, including literal zero.
Omitting `track` retains the original lane; null refuses. Effective intent is
`{ripple:"none",anchor:"fixed",position:"absolute",ownership:"occurrence"}`.
No shared ownership, relative move, ripple, child subset, implicit migration or
arbitrary layer remapping is admitted. Existing raw-child `placement.move` keeps
its own meaning; it is not a group operation.

Python exports:
- `astrid.sdk.timeline.occurrence_commands.capture_occurrence_move(bundle, select, on, *, track=None, ownership='occurrence') -> captured EditCommand`
- `astrid.sdk.timeline.occurrence_commands.OCCURRENCE_MOVE_INTENT`
- Existing `astrid.sdk.timeline.capture.capture_track_create(bundle, owner, row)`
- Existing `astrid.sdk.timeline.commands.execute(bundle, commands)`

Capture on the immutable pointerdown bundle, retained through JSON/outbox/remount.
For a new bottom lane, allocate V3 once and capture track.create on S0; execute
only that create to get S1; capture occurrence.move on S1 with the exact V3 parent
ref. Add the same `group_id` to both commands, submit the ordered batch once, and
undo its one accepted publication. No claim recapture on ACK. Failure of either
command leaves S0 untouched. Both parent V3 and scoped child V3 reuse the same
captured raw lane ID. An existing target is required at move execution.

## Capture meaning and effects

`occurrence.members` v1 records all occurrence-owned raw child refs in authored
order; members/order/boundaries are those exact refs. Bindings are
`move.member:<index>`, `move.owner` and `move.track`. Existing `placement.owners`
records canonical authoring ownership with source-shot boundary. Source image
pins use the existing `move.images` dependency and `move.source:<index>` exact
member media/registry dependencies. Existing `move.quantization` records rational
fps and half-toward-positive-infinity rounding. Main's exact occurrence mapping
isolates shared source authoring; no display-ID or shot/track tuple inference.

`occurrence.move.blockers` v1 uses owner=the moved occurrence and
boundaries=`[exact parent target track ref]`. Members/order select active parent
clips followed by active other occurrences on that lane, in authored order.
The moved occurrence is excluded. Empty results and activity/lane exclusion
predicates are guarded. Replay/inverse compare membership at intervening atomic
record boundaries, so lane/activity ABA conflicts while unrelated lanes remain
independent. Selected geometry, source windows, relation predicates and parent/
child fps are captured; unrelated sibling row values are not global guards.

The handler quantizes the global start with the existing move primitive, retains
occurrence duration and local child positions/windows/speed/order/opaque data,
and checks full output extent against half-open blockers. Exact contact is legal;
equal-start overlap and child overhang refuse. Translation-only maps and complete
single-lane groups are required. Active output visual/audio lanes must match
kind; source/unknown/null roles refuse. Unsupported temporal aliases are recorded
as absent guards, so their ABA cannot disappear from accepted history.

Writes: occurrence placement.start_ms; present at_ms alias; on retrack, both
placement.track and track **plus every owned raw child track**. If absent, the
child destination lane is explicitly created as the exact full captured parent
definition, including opaque fields; an incompatible occupied definition refuses.
Existing compatible child lanes are reused. Occurrence app/app.astrid on/until/
until_film_end clear explicitly; fixed_start=true and for=duration are authored.
Child temporal anchors and immutable migration provenance are preserved. Inverse
uses authored writes and staged own-consumer reversal, never parent restoration.
Unknown legacy pinnedShotGroups refuse pending recorded migration.

## Portable golden and App observations

Portable artifact:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-occurrence-move-golden.json`

Canonical test source:
`/home/user/work/wt/agt-m2-retrack-recover/tests/editing_conformance/fixtures/recipe_m2_occurrence_move.json`

SHA256: `b25c21a11abc27ac33a608c658f70078ae3952cd495cbb13fde1f5d88ea9f160`.
Each case contains original CanonicalDocument input, capture request, exact
commands/recorder exports and compiled output CanonicalDocument. First case is
V2 at global1: clip-1 [1,3), clip-2 [3,5). Second is parent track.create V3 plus
move at global3: clip-1 [3,5), clip-2 [5,7). Raw local starts remain0/2, hold2,
order and mode=images remain in provenance, sibling images/pins remain unchanged.
Both cases carry group_id=group-drag. The original App it.fails assertion blocks
were read unchanged; this worker changes no App tests or product code.

App must derive its compatibility group/clip aliases from canonical ownership
and preserved explicit migration provenance. No pinnedShotGroups writeback.

## Qualification and integration holds

Actual RuntimeService at Runtime `9f9b25c` accepts both gestures using real API-
registered media, shot and text binding input, with renderer calls forbidden.
The permanent targeted test closes/reopens Runtime, reloads the accepted closure,
retries the exact request without executing semantics, undoes the whole gesture,
refuses ordinary reuse of the retired created child lane, and redoes the same IDs.
This is service/SQLite/CAS acceptance evidence, not HTTP/browser evidence.

Repeated-source **geometry/isolation** works through main's mapping, but the
preexisting materializer still fails to emit exact persistent shot/item creation
facts. A strict xfail names that canonical-A reservation requirement. Do not call
shared-source identity reservations complete from the successful geometry and
Runtime roundtrip tests. Manager must compose the shared root/item creation and
reservation slice before qualifying repeated-source integration. This worker
adds no alternate allocator, endpoint, Runtime implementation or pin bypass.

Canonical command schema (byte-identical to the recovered pre-fix schema):
`/home/user/work/wt/agt-m2-retrack-recover/astrid/core/timeline/schema/edit-command.schema.json`
SHA256: `28f91af8d1134725de3695838b238ac00bc30b911ac88ae4d46eb48f7579f46e`.
Native registered operations: clip.move, occurrence.move, placement.move,
track.create, clip.add, track.set, clip.set-params; framework timeline.inverse and
timeline.restore. The recovered schema has explicit conditions for all of these
except the existing native track.create parameter contract in commands.py.
Manager owns composition with other held M2 schema changes and normal Runtime
root/artifact generation; this is not the final composed foundation hash.
