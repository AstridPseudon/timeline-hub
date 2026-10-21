# Agent peer packet: mixed track/data-lane reorder source review

Date: 2026-10-21T04:43:31Z

## Verdict

**SOURCE HOLD — no cross-area ACK for the unregistered
`track.reorder@2` candidate yet.** The candidate has the right existing
authored carriers and an atomic two-write recorder path, but its placement
acceptance semantics do not match Main in two concrete cases: absent/null
placement and unknown `beforeTrackId` anchors. This is a source-contract
boundary only. No implementation expansion, registration, schema generation,
client change, pin, freeze, activation, native claim, or writer deletion is
authorized by this packet.

## Exact source identities

- Agent candidate harness: commit `dd1b1a9152b4742734c4dba8f3e7cf3daaa4774b`,
  tree `b1d9500d7d3c385bfc9301544c4cc4a126d3448e`.
- Candidate source blobs: `_track_commands.py`
  `65e8afb09a2fbdc17063cd81355fdbd14e415715`,
  `test_recipe_track_order.py`
  `ec189f47727d38202b76093242712ca60b8eae8d`.
- Agent schema SHA-256:
  `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`.
  The candidate commit changes only `_track_commands.py` and its focused
  test; the schema and registry are byte/diff unchanged. The public schema
  still requires `track.reorder` version `"1"` with only `order` and
  `expected_order` (`edit-command.schema.json:530-555,1044-1069`), and the
  registry still exposes only the v1 handler
  (`astrid/sdk/timeline/commands.py:94-102`).
- Main/App source inspected: commit `e1e153091b23aeafd09a15c500616384fba4330a`,
  tree `aa20a99731b91c2fa5e36b258c131147f3d7d651`.
- Previously published Runtime v1 boundary remains the only Runtime track
  order ACK in hand: Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`,
  tree `d3a290b407fa61e6ab2d476f50c068073f70df00`, public schema digest
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
  That prior ACK does not accept or pin this v2 source.

## Main representation and order

Main’s authored placement type is exactly:

```ts
{ version: 1, lanes: Array<{ laneId: string; beforeTrackId: string | null }> }
```

This is `src/tools/video-editor/lib/timeline-row-layout.ts:6-9`. The lane
array is row order. `beforeTrackId` is the following media-track anchor;
`null` places the lane after the media rows. `reorderTimelineRows` constructs
the next media permutation and emits each lane in visual row order with the
next following track ID, or `null` at the end
(`timeline-row-layout.ts:80-98`). The App handler sends both changed
collections in one existing `config` edit
(`useTimelineTrackManagement.ts:944-964`), with the authored leaf at
`resolvedConfig.app.timelineDataLanePlacement`
(`TimelineCanvas.tsx:557-561`).

The stable lane binding is not the display sortable ID. Registered lanes use
`kind.kindId` (`data/typed/assembleDataLanes.ts:241-255`); unknown schema
lanes use `opaque:${schemaRef}` (`assembleDataLanes.ts:262-275`); the display
ID is only `data-lane-${laneId}` (`timeline-row-layout.ts:63-67`).

Main’s normalizer returns `{version: 1, lanes: []}` for absent, `null`,
wrong-shaped, or otherwise malformed placement and filters malformed entries
from a present array (`timeline-row-layout.ts:28-39`). It also maps an anchor
that is not a current media track to `null` for layout
(`timeline-row-layout.ts:49-59`). Therefore a mixed reorder with visible
lanes can materialize a valid placement from an absent/null source; the
handler conditionally writes the resulting placement
(`useTimelineTrackManagement.ts:950-957`).

## Candidate guard/write review

The candidate does preserve the intended atomic carrier boundary:

- `_validated_track_order` selects the complete parent track collection,
  requires the captured order to match, then requires a complete unique
  same-owner permutation before any write (`_track_commands.py:75-89`).
- Placement validation requires a v1 object with exactly `version` and
  `lanes`, unique non-empty lane IDs, and `beforeTrackId` as string or null
  (`_track_commands.py:14-31`). It compares desired and expected lane-ID
  membership (`_track_commands.py:49-54`) and guards the exact current whole
  leaf (`_track_commands.py:56-64`).
- All validation completes before either carrier is recorded. The recorder
  then writes the virtual order address and the real
  `config.app.timelineDataLanePlacement` leaf (`_track_commands.py:66-72`).
  The virtual order address maps to the raw `config.tracks` collection and is
  not a persisted `track_order` sibling (`_command_state.py:109-115`).
- The five-test source proof confirms exact two-write order, raw track
  membership/object/opaque preservation, App sibling preservation, and
  disjoint label rebase (`test_recipe_track_order.py:224-261`). Existing v1
  source tests cover complete-order stale/membership/identity guards and
  strict inverse A→B→A refusal (`test_recipe_track_order.py:74-183`); the
  existing recorder/inverse path is reused by the candidate.

The mismatch is precise: `_track_commands.py:56-60` refuses an absent or
null authored placement, whereas Main treats it as empty and can write a
new placement for a visible mixed-lane reorder. Also, `_track_commands.py:23-27`
accepts any string anchor, whereas Main’s layout maps an anchor not present in
the current track IDs to `null` (`timeline-row-layout.ts:54-56`). The current
five-test candidate proof has no absent/null or unknown-anchor vector.

## Smallest follow-up

Before any v2 peer ACK, settle one narrow source policy and add only its
focused vectors:

1. Either explicitly bound native v2 capture to an existing, valid placement
   whose anchors are `null` or current parent track IDs, returning a visible
   unsupported-dependency refusal for absent/null/unknown-anchor inputs while
   App2 keeps the current serializer; or
2. If parity with Main’s materialization is required, make the unregistered
   candidate’s expected/desired placement state-aware for absent/null and
   define the exact null-to-empty write, plus the current-track anchor rule.

Until that choice is recorded and proved, the correct disposition is **HOLD**;
do not infer a new data-lane authority or silently normalize authored data.

## Evidence

Run directly on the candidate harness above:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_recipe_track_order.py
```

Result: **5 passed in 0.84s**.

The completed source-worker evidence, intentionally not repeated under this
task’s “no repeat64suite/registry audit” boundary, is the exact command over
`tests/sdk/test_timeline_composed_schema.py`,
`tests/sdk/test_timeline_current_union_schema.py`, and
`tests/sdk/test_timeline_materialization_schema_union.py`: **64 passed in
180.22s**. This packet does not relabel that prior run as a new execution.

No full, browser, socket, Runtime live/provider, generated-client, registry
audit, pin, freeze, or activation test was run here.
