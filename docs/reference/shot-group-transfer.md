# Cross-track pinned-group transfer

`shot-group.set` admits `intent: "transfer"` on the existing recorded transaction
path. The group must already exist. A caller sends its captured base revision
with this command (and any existing guarded track-add / movement commands) in
one commit:

```json
{
  "op": "shot-group.set",
  "select": null,
  "args": {
    "group": {"shotId": "s", "trackId": "picture"},
    "intent": "transfer",
    "target": "parent/track:destination",
    "members": ["parent/clip:i2", "parent/clip:i1"]
  }
}
```

`target` is the exact canonical visual track ScopedId in the members' parent or
occurrence scope. `members` is a complete, distinct permutation of the existing
scoped group members, in the requested resulting group order. It does not select
replacement members. For occurrence-owned members, use `occurrence:<id>/clip:<id>`
and `occurrence:<id>/track:<id>`; the ordinary source/placement guards bind their
revision pins. Bare local or projected IDs do not grant ownership. Existing
admitted occurrence-local authoring is required; transfer does not create a new
occurrence, change its placement track, or invent an inherited child track.

The producer captures tagged expectations for the complete source row, complete
group collection order (`<source-group-id>::group_order`), absent target group,
source/target canonical track rows, exact current member rows and their relative
storage order, occurrence placement/source pins, media registry entries, and any
retained snapshot identities. The saved recorded command retains those original
expectations for guarded replay/rebase. A caller may also supply captured tagged
expectations in `expect`; these are checked, never overwritten with newer values.
The group semantic ID is the existing `shot_groups.identity({shotId, trackId})`
encoding; no new persisted identity is allocated.

Only the key's `trackId`, requested `clipIds` / existing `memberSelectors` order,
active member `track` fields, and existing retained snapshot `track` /
`authoring.clip.track` fields change. Mode, video asset, names, occurrence owner,
all other snapshot content/order, opaque siblings, group collection position and
active clip storage order remain intact. Video snapshots require the existing
lossless authored provenance schema. Existing image groups with absent `mode` or
`memberSelectors` retain that representation, including scoped legacy `clipIds`.
Transfer refuses a stale group key that
disagrees with its active ownership, a target collision, mixed/ambiguous ownership,
an invalid target or conflicting snapshot reservation.

For a new lane, prepend the existing `timeline.add` with an exact scoped reserved
track ID, complete track row and `<track-id>::` tagged absent expectation. Add
existing movement commands for the planned positions in the same batch. Transfer
does not change clip timing, media edges or authored relations. Relation choices
remain the responsibility of those existing movement producers and their callers.
A failure anywhere rolls back the whole batch, including track creation.

The actual `Plan.direct_writes` / accepted `change.direct_writes` contain the old
and destination group roots and each member's `track` field, with tagged before
and after states. Aggregate document arrays and compiled clocks remain
consequences. `shot_groups` returns the resulting key and ordered `reused`
members, no created/restored clip identities. `id_map` maps the old group semantic
ID to the destination and reuses the exact scoped clip identities. Existing
accepted-publication inverse/history owns Undo and replay; transfer adds no
history writer. A later change to an owned field or either group key is guarded
and attributed by that history path; unrelated later member fields can survive.

This SDK source contract does not adopt an App caller, remove its existing
cross-track fallback, or qualify mounted Runtime/Host publication, portfolio
cards, release gates or live data.
