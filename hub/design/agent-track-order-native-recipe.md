# Agent source-only contract: native parent media-track order

Status: **SOURCE ONLY — App2 and Runtime ACK required before generated schema,
pin/freeze, or consumer activation.** This change qualifies the Agent source
recipe and its focused proof only. It does not change App, Runtime,
Composition, generated clients, DTOs, endpoints, stores, or frozen artifacts.

## Scope and boundary

The source contract covers the App2 media-only reorder branch: a complete
permutation of the parent authored `config.tracks` collection. The `lanes`
branch is explicitly unsupported because it also changes
`config.app.timelineDataLanePlacement`; no partial or split native submission is
allowed until an atomic carrier for both authored collections is qualified.

The current source operation is `track.reorder`, version `1`:

```json
{
  "schema_version": 1,
  "op": "track.reorder",
  "version": "1",
  "select": "parent",
  "args": {
    "order": [
      "parent/track:overlay",
      "parent/track:picture",
      "parent/track:music"
    ],
    "expected_order": [
      "parent/track:picture",
      "parent/track:overlay",
      "parent/track:music"
    ]
  },
  "intent": {}
}
```

Both arrays are required, unique, complete, and contain only
`parent/track:<id>` references. `expected_order` is the captured original
order; `order` is the desired final order. The command refuses missing, extra,
duplicate, cross-owner, malformed, or stale identities before writing. An
absent or non-array authored collection is refused by the existing collection
primitive; no new empty-collection behavior is introduced.

## Exact semantics

Capture selects `collection.tracks` for `parent`. The recorder therefore keeps
the collection shape read, complete member identity list, exact original order,
membership boundaries, and the direct virtual write expectation. The virtual
`parent::track_order` address exists only for recorder overlap and inverse
guards; it is not a stored field and does not add a schema or persistence leaf.

Execution applies `arrange()` to the existing raw track rows. It changes only
array order. Track objects are not rebuilt or normalized, so labels, null,
false, zero, opaque fields, clips, root/config siblings, and data-lane fields
are preserved byte-for-byte in the authored bundle. A disjoint track-label edit
can rebase across the reorder. A changed collection order, membership, or
identity fails closed. An equal-final-state forward replay is allowed, while
inverse checks the complete intervening recorder history and rejects an actual
A→B→A sequence.

The operation is source-only and uses the existing command registry, recorder,
rebase, inverse, and serialized bundle paths. It introduces no generation,
freeze, pin, Runtime DTO, public operation, or guessed published contract.

## Executable floor

`tests/editing_conformance/test_recipe_track_order.py` proves:

- exact raw-row permutation and preservation of null/false/zero/opaque fields,
  clips, root/config siblings, and `timelineDataLanePlacement`;
- collection shape read plus complete member/order/boundary recorder claims;
- serialized bundle and record reload, deterministic replay, inverse and redo;
- equal-final-state forward replay;
- disjoint label rebase, stale order refusal, changed-identity refusal, and
  complete unique same-owner membership refusal;
- strict inverse rejection for both a direct intervening order write and a
  real recorded A→B→A sequence; and
- explicit refusal of an unsupported `lanes` argument.

## Requested peer ACK

Please ACK or reject this exact source contract before any generation or
activation:

- **App2:** confirm that the media-only handler can capture the complete
  current parent raw track identity permutation for `track.reorder@1`, retain
  the existing serializer until consumer proof, and keep the `lanes` branch
  guarded/unsupported without splitting its two authored collections.
- **Runtime:** confirm that the existing `/v1` command/provider path can carry
  this source operation with its virtual direct write at
  `parent::track_order`, complete collection selection, guarded inverse/rebase,
  serialized reload/redo, retry, and idempotent acceptance—without a new
  endpoint, DTO, store, or persisted order field. If Runtime needs a different
  published spelling, state that before generation; App2 must not guess one.

ACK scope is the source contract only. It does not authorize pinning, freezing,
generated-client changes, App edits, fallback deletion, mixed-lane support, or
publication/activation.
