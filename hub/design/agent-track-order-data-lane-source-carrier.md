# Agent mixed track/data-lane reorder source spike

## Result

The Main producer has a stable authored carrier for the mixed row reorder, so
this is not a missing-source refusal.  The carrier is the existing optional
leaf `parent.config.app.timelineDataLanePlacement`; no new entity, store, or
data-lane authority is needed.

The Agent worktree contains an unregistered `track.reorder` version `2`
source candidate in `astrid/sdk/timeline/_track_commands.py`.  The existing
registered `track.reorder@1`, its schema, capture format, and media-only
behavior are unchanged.  The candidate is deliberately not in `operations()`
and is not accepted by the public validator until App2 and Runtime ACK this
shape.

## Main source contract

Main's `useTimelineTrackManagement.handleMoveTrack` calls
`reorderTimelineRows` for the `lanes` branch and submits one `config` edit:

```ts
{
  tracks: nextTracks,
  app: { ...resolvedConfig.app, timelineDataLanePlacement: next.placement },
}
```

The exact authored leaf is:

```ts
timelineDataLanePlacement?: {
  version: 1,
  lanes: Array<{ laneId: string, beforeTrackId: string | null }>,
}
```

`laneId` is the stable binding.  Registered lanes get `kind.kindId` from the
`DataKindSnapshotRecord`; opaque lanes use the deterministic
`opaque:${schemaRef}` form in `assembleDataLanes`.  `data-lane-${laneId}` is
only a sortable/display ID and is not part of this contract.  The placement
array order is authored row order.  `beforeTrackId: null` means the lane is
after the media rows; otherwise it is the raw track ID anchor.  There are no
time, frame, or pixel units.  Main's normalizer defaults absent, null, or
malformed input to an empty in-memory placement, but the source candidate
only accepts an existing present authored object and never invents that
default or turns an absent/null leaf into a write.

## Candidate shape

```json
{
  "schema_version": 1,
  "op": "track.reorder",
  "version": "2",
  "select": "parent",
  "args": {
    "order": [
      "parent/track:overlay",
      "parent/track:picture",
      "parent/track:audio"
    ],
    "expected_order": [
      "parent/track:picture",
      "parent/track:audio",
      "parent/track:overlay"
    ],
    "data_lane_placement": {
      "version": 1,
      "lanes": [
        {"laneId": "opaque:custom/v1", "beforeTrackId": "picture"},
        {"laneId": "astrid.transcript", "beforeTrackId": "audio"}
      ]
    },
    "expected_data_lane_placement": {
      "version": 1,
      "lanes": [
        {"laneId": "astrid.transcript", "beforeTrackId": "overlay"},
        {"laneId": "opaque:custom/v1", "beforeTrackId": null}
      ]
    }
  },
  "intent": {}
}
```

The candidate validates both complete unique same-owner track permutations,
both closed placement objects, and exact lane-ID membership before writing.
It records exactly two direct authored writes atomically:

```text
parent::track_order
parent::config.app.timelineDataLanePlacement
```

The first remains the existing virtual recorder property and raw
`config.tracks` carrier.  The second replaces only the known placement leaf,
so `app` siblings, track row objects, opaque track fields, clips, null/false/0
values, and unrelated config data survive.  The expected placement is a
whole-leaf guard, so lane order, anchors, membership, and identity changes
conflict; no data-lane registry is consulted or guessed.  Both guards are
checked before either write.  Existing recorder/inverse logic therefore has
the two writes for rebase, strict inverse/A→B→A refusal, reload, and retry
identity handling.

The focused source proof is in
`tests/editing_conformance/test_recipe_track_order.py` and uses a compact
Main-shaped vector with `astrid.transcript` and `opaque:custom/v1` lanes.  It
also proves the existing media-only tests remain unchanged.

## Boundary

This is a source spike only.  No App writer, Runtime DTO/endpoint, schema
artifact, public registry entry, pin, activation, generation, or fallback
deletion was changed.  App2 should keep the mixed serializer writer live
until a paired consumer ACK and outbox/recovery proof exist.  Runtime should
review this two-write `track.reorder@2` candidate before it is registered;
the frozen `track.reorder@1` contract remains the only public operation.
