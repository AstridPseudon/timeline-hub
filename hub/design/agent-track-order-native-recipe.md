# Agent source-only contract: native parent media-track order

Status: **SOURCE ONLY — App2 and Runtime ACK required before generated schema,
pin/freeze, or consumer activation.** This worker changed only the Agent
source tree and focused Agent proof. It did not change App, Runtime,
Composition, generated clients, DTOs, endpoints, stores, or frozen artifacts.

## Main positive and boundary

The exact App2 positive is the no-`lanes` branch of
`useTimelineTrackManagement.handleMoveTrack(activeId, overId)`:

```text
useTimelineTrackManagement.ts:927-932
  moveTrackWithinKind(resolvedConfig.tracks, activeId, overId)
  applyEdit({ type: 'config', resolvedConfig: { ...resolvedConfig, tracks: nextTracks } })
```

It permutes the complete raw `config.tracks` array and keeps each track object,
clips, and unrelated config/root fields intact. The existing App positive and
round-trip proof is
`useTimelineTrackManagement.test.ts:149-161` in the App repo.

The `lanes` branch at `useTimelineTrackManagement.ts:918-925` is **not covered**:
it changes both `config.tracks` and
`config.app.timelineDataLanePlacement`. No partial or split native submission is
allowed; that mixed media/data-lane placement remains on its guarded legacy
path until a separate atomic carrier is qualified.

## Current Agent decision

Current main had no native order recipe. `track.set` is a leaf label recipe and
is not widened to carry order. Frozen R4 `timeline.reorder` is useful prior art
(complete permutation, `expected_order`, and synthetic `track_order` direct
write), but it is not in the current pinned registry. Therefore the smallest
new source operation proposed here is:

```json
{
  "schema_version": 1,
  "op": "track.reorder",
  "version": "1",
  "select": "parent",
  "args": {
    "order": ["parent/track:<id>"],
    "expected_order": ["parent/track:<id>"]
  },
  "intent": {}
}
```

Both arrays are complete, unique, parent-owned scoped track identities. The
`expected_order` array is the captured original permutation; `order` is the
desired permutation. Empty arrays are schema-valid, but an absent or non-array
authored track collection is refused by the existing collection primitive.

Capture and execution use the existing `order()` / `arrange()` primitives:

1. Capture selects `collection.tracks` for `parent`, recording the complete
   membership/order and collection shape. The handler rejects stale
   `expected_order`, duplicate/missing/extra identities, and any non-parent
   identity before writing.
2. The only direct authored write is the derived virtual property
   `parent::track_order`. It is read from raw `config.tracks` order and applied
   by `arrange()`; no `track_order` field is stored and no track row is rebuilt.
3. The existing recorder emits the direct write, original order expectation,
   collection selection, and normal command claims. Raw row payloads and
   membership remain untouched.
4. Existing inverse/replay/rebase machinery restores the virtual permutation.
   A same-state forward reorder is recorded and allowed. A changed order,
   membership, or track identity fails closed. A disjoint track leaf edit can
   rebase; an order write, including an A→B→A later intent, blocks guarded undo.

The virtual property has a collection-level logical address solely for overlap
and intervening-write checks. It does not create a persisted field.

## Agent source and executable proof

Changed source:

- `astrid/core/timeline/schema/edit-command.schema.json:494-519,1012-1040` —
  source-only `TrackReorderArgs` and `track.reorder@1` envelope branch.
- `astrid/sdk/timeline/_track_commands.py:11-58` — handler and capture helper.
- `astrid/sdk/timeline/_command_state.py:109-115,295-298,375-382` — virtual
  order address plus `State.get/set` delegation to existing collection order
  primitives.
- `astrid/sdk/timeline/commands.py:35,86` — source registry entry.

Focused executable proof:

- `tests/editing_conformance/test_recipe_track_order.py:33-63` — exact raw
  permutation, opaque/null/false/0 preservation, clips/root preservation,
  serialized reload, replay, inverse/redo, and forward-equal state.
- `tests/editing_conformance/test_recipe_track_order.py:66-102` — disjoint
  label rebase, stale order, changed identity, and later A→B→A guarded undo.
- `tests/editing_conformance/test_recipe_track_order.py:105-118` — cross-owner
  and incomplete permutation refusal with no partial mutation.

Exact targeted results:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_track_order.py \
  tests/editing_conformance/test_recipe_scalar_commands.py
=> 76 passed in 5.73s

git diff --check
=> pass
```

No full suite, browser, localhost, socket, Runtime, generated-contract, or
App journey was run. The App serializer positive is source evidence from the
specified report and live handler inspection; App2 adoption remains unverified.

## Requested peer ACK

Please ACK or reject this exact source contract before any generation or
activation:

- **App2:** confirm that the media-only handler can build `track.reorder@1`
  from the complete current parent raw track identity permutation, preserving
  the existing serializer until consumer proof; confirm the `lanes` branch
  stays legacy/unsupported and is not split.
- **Runtime:** confirm that the existing `/v1` command/provider path can carry
  the source operation with a virtual direct write at `parent::track_order`,
  complete collection selection, guarded inverse/rebase, reload, retry, and
  idempotent acceptance—without a new endpoint, DTO, store, or persisted order
  field. If Runtime requires a different public spelling, state that before
  generation; App2 must not guess one.

ACK scope is source contract only. It does not authorize pinning, freezing,
generated-client changes, App edits, fallback deletion, or mixed-lane support.
