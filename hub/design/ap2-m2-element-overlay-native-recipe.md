# App2 M2 native recipe: parent effect overlay

Date: 2026-10-20  
Base: `hub/timeline/app/tl/app-m3-root-cold-current-source-attribution` (`05b6`)  
Scope: the existing `ElementsLibraryPanel` effect overlay apply/create and whole-overlay remove only.

## Verdict

The positive overlay recipe is executable with existing Agent operations. It is
not `clip.set-element` alone:

```text
existing visual output track:  clip.add
missing visual output track:   track.create, then clip.add
selected project-pack ref:     clip.add, then clip.set-element
selected authored params:      clip.add, clip.set-element, then clip.set-params
whole overlay removal:         clip.delete
```

`clip.add` is the operation that creates the overlay row and carries its
placement, duration, track, element reference, params, and opaque fields.
`clip.set-element` is only the selected-pack authority check and immutable
revision write; for a newly added selected row it is an intentional same-value
write. `clip.delete` removes the complete parent overlay row. The existing
native handlers provide the recorded reads, selections, bindings, created IDs,
expectations, inverse, and replay behavior; no new operation or field is
needed.

This recipe does not qualify transitions, animation-on-existing-clip,
element-ref detachment while retaining a clip, occurrence-owned overlays,
media-backed overlays, or legacy adapter retirement.

## Exact commands

All commands use `schema_version: 1`, `version: "1"`, and `intent: {}`.
Capture each command from the exact staged bundle immediately before that
command. The `id` values below are placeholders for IDs reserved once by App;
they must not be regenerated on retry.

### Optional track creation

Use this only when the chosen destination does not already exist as an active
visual output track. The row is the complete authored track row, including any
opaque sibling fields App is carrying.

```json
{
  "schema_version": 1,
  "op": "track.create",
  "version": "1",
  "select": "parent",
  "args": {
    "row": {
      "id": "reserved-overlay-track",
      "kind": "visual",
      "role": "output"
    }
  },
  "intent": {}
}
```

The native capture guard requires the complete identity
`parent/track:<id>` to be absent. It records an empty `track.create`
selection, creates `parent/track:<id>`, and has no binding. Do not use this to
overwrite an existing track or to turn an audio/non-output track into a visual
one.

### Overlay creation

`clip.add` is parent-owned and appends one complete literal row. For the
current panel's ordinary effect overlay, build the row as follows:

```json
{
  "schema_version": 1,
  "op": "clip.add",
  "version": "1",
  "select": "parent",
  "args": {
    "row": {
      "id": "reserved-overlay-glow-500",
      "clipType": "glow",
      "track": "picture",
      "at": 0.5,
      "hold": 1.25,
      "elementRef": {
        "id": "glow",
        "kind": "effect",
        "revision": "sha256:<64 lowercase hex>"
      },
      "params": {
        "amount": 0.7,
        "clearable": null
      },
      "opaque-clip": {
        "foreign": ["overlay", null]
      }
    }
  },
  "intent": {}
}
```

The actual row must retain every authored field, not just the example fields.
The positive boundary is:

- `select` is `parent` and the destination track is an active visual output
  track;
- `clipType` is the effect element ID, `at` is the panel's authored overlay
  start, and `hold` is its authored overlay duration in seconds;
- `elementRef` is the exact catalog identity, including immutable revision;
- `params` and unknown/opaque JSON are copied literally; `null` is a value,
  not an implicit clear;
- the reserved clip ID is absent before capture and is included in the row;
- no asset/media selector, source window, relation/anchor, nested child list,
  non-unit speed, or creation-time frame rounding is introduced.

Native capture reads the destination track's `id`, `kind`, `role`,
`enabled`, `active`, `disabled`, `hidden`, and `deleted` fields, guards the
parent clip collection and new clip identity, binds
`add.track -> parent/track:<id>`, and records the new clip in `created`.
It appends the complete row without rewriting the existing sibling rows or
their order. `resolved` is empty for the positive `clip.add` capture.

### Selected project-pack authority

`clip.add` deliberately accepts the complete row but does not itself perform
the selected-pack schema admission. If `elementRef.packId` is present, append
this existing operation after the add, captured against the staged bundle:

```json
{
  "schema_version": 1,
  "op": "clip.set-element",
  "version": "1",
  "select": "parent/clip:reserved-overlay-glow-500",
  "args": {
    "elementRef": {
      "id": "glow",
      "kind": "effect",
      "packId": "project-pack-id",
      "revision": "sha256:<64 lowercase hex>"
    },
    "schema_source": {
      "document_id": "document:<id>",
      "version": 3,
      "content_digest": "sha256:<64 lowercase hex>"
    }
  },
  "intent": {}
}
```

This same-value write is required: it proves that the row's selected ID,
kind, owner, and immutable revision are the same as the admitted selection,
and records the native `params.schema`/`params.snapshot` authority. It also
records `scalar.target -> parent/clip:<id>` and `params.element ->
parent/clip:<id>` bindings. It is not a replacement for `clip.add`.

The authority inputs are the existing provider inputs, not caller metadata:

- scoped `realm_id`;
- the exact `schema_source` `DocumentPin` above;
- exactly one verified `schema_inputs` admission for the selected project and
  pin, containing the matching element `id`, `kind`, `packId`, and `revision`;
- the immutable admitted snapshot object bytes/descriptor for that admission.

If the overlay creation supplies authored parameter changes for a selected
element, append `clip.set-params` after `clip.set-element`, with
`select` equal to the new clip and `args` exactly
`{ "values": <literal top-level parameter writes>, "clear": <literal keys>,
"schema_source": <same pin> }`. Capture it against the latest staged bundle
and pass the same `realm_id` and `schema_inputs`. Set/clear overlap is refused;
unmentioned existing params and opaque fields survive. If no authored params
are supplied, omit this operation.

For an unowned/literal ref with no `packId`, use only `clip.add` (plus an
optional `track.create`). Supplying `schema_source` to `clip.set-element`
without a selected pack is refused. A literal ref still carries the exact
`id`, `kind`, and `revision` from the admitted catalog; App must not invent or
rewrite the revision.

### Whole-overlay removal

For the overlay clip created above, capture this against the current bundle:

```json
{
  "schema_version": 1,
  "op": "clip.delete",
  "version": "1",
  "select": "parent/clip:reserved-overlay-glow-500",
  "args": {},
  "intent": {}
}
```

`clip.delete` records the complete target row as its original-state guard,
the parent clip membership/order, all parent/occurrence collection membership,
and declared relation/transition dependency reads. It has no binding or
created IDs. It clears only the selected row, so the base clip, its params,
and unrelated opaque siblings remain unchanged. It refuses atomically if the
target is gone, is a legacy `shot`, contains nested `clips`/`children`, or a
declared semantic dependency cannot be proven safe.

This is whole-overlay removal. The current native registry has no qualified
operation for “clear only `elementRef` but retain this overlay clip”; do not
translate that behavior into `clip.set-element`, because that operation cannot
clear an element reference. If the product means detach rather than delete,
the smallest peer request is for Agent to qualify an authoritative element-ref
clear operation with the same recorded inverse/rebase guards. Until then, the
normal native case is delete-the-overlay-row or visible refusal with the draft
untouched.

## Replay, inverse, and retry contract

The App producer must reserve the track/clip IDs before capture and retain the
exact command batch, captured reads, bindings, expectations, authority inputs,
and created IDs in the existing session/outbox. A retry resends that exact
body and retry identity; it does not recapture against the ACK or allocate a
new suffix. Undo uses the accepted records and the existing guarded inverse.
The private native probe proved:

- existing-track literal `clip.add` preserves placement, duration, track,
  params, element reference, opaque fields, and the sibling row;
- `track.create` + `clip.add` has one exact inverse and deterministic replay;
- literal `clip.set-params`, same-identity `clip.set-element`, and
  `clip.delete` each have exact inverse/replay behavior;
- selected `clip.add` + `clip.set-element` (and selected params when present)
  preserves the complete overlay row and inverse/replay with the admitted
  source and snapshot inputs.

No native operation changes a sibling's opaque data, and no operation is
allowed to refresh the original basis during retry or inverse.

## Exact refusal boundary and App peer request

The current App panel context passes `{id, kind, revision, packId}` but does
not pass the selected `schema_source`, scoped `realm_id`, or verified
`schema_inputs`. A selected overlay producer that omits the scoped realm is
rejected by the existing native capture with the exact error:

```text
selected pack capture requires the scoped realm identity
```

Smallest peer request: expose the already-existing Agent/provider authority
tuple (`realm_id`, exact `schema_source`, verified `schema_inputs` and retained
snapshot objects) through the current command-session/provider seam. Do not
add a panel-side schema cache, pin, registry, or invented command field. Until
that tuple is available, refuse selected-pack overlay apply before changing
the draft; literal no-pack overlays remain eligible for the recipe.

Other normal refusals are native and visible: missing/non-output/inactive
track; parent/occurrence overlay ownership outside `clip.add` v1; media-backed
or source-window clips; non-literal timing/relations; reserved-ID collision;
missing selected admission/snapshot; and unsafe semantic dependencies on
delete. No valid positive case is converted into a denial merely to fit this
boundary.

## Concrete App worker brief

Migrate only the existing effect-overlay branch of
`ElementsLibraryPanel` through the current command-session/outbox and Runtime
`/v1` path. Capture the original selected parent clip and current head, choose
its active visual output track (or explicitly create one), reserve the overlay
ID once, and emit the staged recipe above. Preserve the panel's authored
`at`, duration, exact element revision, params, and opaque row data. Use the
selected authority tuple when `packId` is present; otherwise use the literal
branch. Map whole-overlay remove to `clip.delete`. Keep transitions,
animations on an existing clip, detach-only removal, fallback whole-document
saves, and legacy adapter deletion out of this worker. Add focused producer
coverage for literal and selected branches, missing authority, ID retry,
inverse/replay, and opaque/sibling preservation; do not weaken existing
positive tests or claim writer retirement until the consumer journey is
qualified.

## Evidence

Private native interpreter and source were read-only:

```text
PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary \
/home/user/work/venv-app2-native/bin/python -m pytest -q -c /dev/null -p no:cacheprovider \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary/tests/editing_conformance/test_recipe_m2_clip_add.py \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary/tests/editing_conformance/test_recipe_clip_delete.py \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary/tests/editing_conformance/test_recipe_clip_set_element.py
```

Result: **146 passed in 13.90s**. An additional temporary, non-repository
probe exercised the exact overlay rows and staged batches (literal existing
track; `track.create` + `clip.add`; selected `clip.add` + `clip.set-element`;
selected params; `clip.delete`) and asserted exact row output, opaque/sibling
preservation, inverse, and replay. Results: `overlay-native-probe: PASS`,
`selected-overlay-native-probe: PASS`,
`selected-overlay-params-native-probe: PASS`, and
`selected-delete-native-probe: PASS`.

The probe used the existing native fixture
`tests/editing_conformance/fixtures/recipe_m2_clip_set_element.json` for the
selected admission/snapshot and the existing literal command handlers. It did
not modify product source, the private source archive, the shared venv, a
registry, a pin, generated output, Runtime, browser state, or a ledger. This
experiment is recipe evidence only; it does not claim App consumer
qualification, Runtime durability, Gate 5/6 completion, or legacy-path
retirement.
