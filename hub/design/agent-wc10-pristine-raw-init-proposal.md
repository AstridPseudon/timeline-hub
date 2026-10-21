# WC10 pristine raw-config initialization proposal

Status: **unregistered source spike; no activation requested** (2026-10-21).

This is one concrete Agent-side proposal for the unresolved custom-config
positive in `agent-wc10-custom-output-existing-recipe-plan.md`. It keeps the
current `timeline.init` operation family and version 1 unchanged, and uses the
existing recorder/inverse/reload machinery. It does not register a command,
change a public caller, update a pin, or replace an initialized timeline root.

## Proposed literal closed envelope

Use the existing operation with a new version boundary, `timeline.init@2`:

```json
{
  "schema_version": 1,
  "op": "timeline.init",
  "version": "2",
  "select": "parent",
  "args": {
    "name": "Custom",
    "slug": "custom",
    "config": {
      "tracks": [],
      "theme_overrides": {
        "visual": {
          "canvas": {
            "width": 1920,
            "height": 1080,
            "fps": 30,
            "background": null
          },
          "opaque_visual": {"enabled": false}
        },
        "opaque_theme": [null, false]
      },
      "opaque_sibling": {"literal": "preserve-me"}
    }
  }
}
```

The outer command and `args` object are closed: no `output`, root replacement,
intent override, arbitrary target, or extra argument is admitted. `args.config`
is the one intentionally open semantic-JSON subtree. Its authored keys and
values stay at their original paths, so `theme_overrides.visual.canvas` is not
projected to `output`; `null` remains a value; omitted fields remain absent;
opaque sibling keys/values remain present; and array order is retained. The
example omits `background_scale` intentionally to make absence distinct from
the explicit `background: null`. Runtime canonical JSON may sort textual object
keys; this proposal promises semantic JSON and array order, not object-member
byte order.

## Recipe boundary

The future handler should use the same exact pristine guard as current v1:

1. `ctx.record["ordinal"] == 0`.
2. The authenticated input parent equals exactly the empty bootstrap parent
   (`config.clips == []`, `config.tracks == []`, `registry == {}`, `clips ==
   []`).
3. `placements` and `shots` are empty.
4. The current parent `config`, `name`, and `slug` are read from the input;
   `name` and `slug` must still be absent. The proposed `args.config` is then
   checked by the empty-structural boundary below. No caller-supplied
   equal-bytes head, prior publication, or post-edit head satisfies this guard.

The open `args.config` has one additional empty-structural boundary. The known
authored structure slots (`tracks`, `clips`, `occurrences`, `placements`,
`shots`, `groups`, `pinnedShotGroups`, `media`, `references`, `reference`,
`assets`, and `registry.assets`) must be absent or their empty collection
(`[]`/`{}`). A nonempty value is an unrecorded birth and is
refused: this initializer has no `created` fact or structural input fact that
could justify it. This check is at the known structural paths only; it does
not recursively reinterpret arbitrary namespaced/opaque metadata, including
`theme_overrides` arrays. A future nonempty structural initializer would need
ordinary recorded creation commands and their input/media/reference facts,
not a wider whole-config write.

The only authored writes are these three scoped addresses, in this order:

```text
parent::config  <- args.config
parent::name    <- args.name
parent::slug    <- args.slug
```

There is no `parent` whole-root write, no `registry.assets` injection, no
`config.output` projection, and no write to clips, tracks, placements, shots,
or registry siblings. The config container is the bounded carrier; this is not
a generic initialized-root replacement writer. A later edit overlaps the
scoped `parent::config` container and must make inverse refuse rather than
silently restore over it.

The existing `Recording.write` can represent the bounded container write while
retaining exact nested JSON. `Recording.finish(capture=True)` supplies the
normal `before`/`after`, exact absence/value reads, authored guards, and the
same record shape consumed by `inverse.py`; the empty-structural check ensures
that this write does not masquerade as a collection/media/reference birth. No
snapshot, frozen schema copy, or special inverse path is needed.

## Executable controls in this spike

`tests/editing_conformance/test_pristine_raw_initialize_proposal.py` is
test-only and deliberately bypasses `operations()`/schema registration. It
contains the literal envelope above and a small pure capture helper. The two
controls prove:

- exact raw config roundtrip through `document_from_bundle` /
  `bundle_from_document`, including the canvas path, explicit null, absent
  field, opaque siblings, and array order; then the existing guarded inverse
  restores the pristine authored payload after reload;
- a changed bootstrap parent refuses with `not_pristine`, a second init after
  the first init refuses with `not_pristine`, and a later `track.create` makes
  inverse refuse with `intervening_write`;
- a compact counterexample shows an unconstrained open config accepting
  nonempty track/clip/group/media/reference/asset structure with no recorder
  creation or entity input facts, while the empty-structural boundary refuses
  each case as `unrecorded_birth`.

This is recorder/inverse capability evidence only. It is not Runtime custody,
CAS, HTTP, installed-pair, App, or public-positive evidence.

## Exact source and schema implications for activation

No source or schema implication below is applied by this spike.

| Surface | Required future change | Must remain unchanged now |
| --- | --- | --- |
| Agent `native_initialize.py` | Add a v2 handler/capture builder with the guard and exactly the three writes above. Keep v1's fixed App `output` recipe separate. | No v1 behavior or current operation registry change. |
| Agent command schema | Add one `timeline.init` conditional for `version: "2"` and a small `TimelineInitRawArgs` definition: required `name`, `slug`, `config`; `config` is an object whose values use the existing recursive `JSON` definition. Keep `additionalProperties: false` on the args object. | Do not copy/freeze a second full schema; do not alter `TimelineInitArgs` v1, schema version, generated/public command surface, or existing pins. |
| Agent validator/registry | Permit only this exact op/version pair once the schema is intentionally adopted; the current `version == "1"` and `operations()` behavior is the activation seam. | The current validator must continue refusing this unregistered v2 spike. |
| Runtime provider | Reuse the existing `timeline.init` provider route, authenticated bootstrap publication, receipt/idempotency, exact base pair, inverse, and CAS retry boundary. Its init detection is already operation-family based; paired qualification must prove it forwards the config subtree unchanged and rejects any non-bootstrap/later head. | No new endpoint, DTO, generic root writer, publication bypass, or Runtime schema/client behavior in this task. The reviewed `b3bc0f75…` fixture conversion proves only the native ULID/default positive, not this custom raw positive. |
| App | On a future agreed activation, `bootstrapCapture` would persist this exact v2 command and source `config` from the caller raw config. It must not pass `DEFAULT_OUTPUT`/`withDefaultTimelineOutput` or synthesize `output`; null/absence/opaque siblings stay in `config`. | No App caller migration or public behavior change now. |

The provider boundary is not the local `ordinal == 0` check. The existing
provider must continue to require the authenticated bootstrap intent,
`previous == None`, and the exact base head, and must recheck that exact head
on CAS retry. In particular, a first init after undo is refused even when the
document bytes are empty again; the existing
`tests/sdk/test_timeline_pristine_initialize_provider.py` positive/refusal lane
remains the authority for that fact.

The eventual paired positive must retain the original `tests/v10` custom
canvas expectation at `theme_overrides.visual.canvas`; it must not convert that
expectation to `config.output` or turn it into a refusal merely to make the
native fixture green. Until the v2 schema/registry and Runtime/App pair are
explicitly approved, the original custom-canvas positive remains open.

## Existing seam / counterexample

The existing recorder is sufficient for the bounded `parent.config` carrier;
the refined spike reproduces the real admission risk if the open config is not
structurally bounded, and then shows the smallest empty-only constraint. It
found no recorder counterexample for nested null, absence, opaque sibling
values, array order, serialization/reload, or guarded inverse. The exact
unresolved seam is still admission, not recording: current Agent
`edit-command.schema.json`, `commands.validate_command`, and `operations()`
admit only `timeline.init` version 1, whose fixed `output` args cannot spell
this raw config. The current Runtime/App paths consequently cannot claim the
original custom positive. The proposal must remain unregistered until that
explicit v2 agreement and a paired Runtime acceptance proof exist.

## Original `create_empty` caller inventory

The original positives in `tests/v10/test_timelines_create.py` cover the
default and custom canvas configs; both have empty structural collections and
preserve the raw `theme_overrides.visual.canvas`. The current CLI caller at
`astrid/packs/timeline/cli.py:175-192` and the stage1 empty-timeline caller
likewise pass empty structure. They are not evidence for a nonempty raw-init
carrier.

There is one genuine nonempty caller: `astrid/sdk/timeline_duplicate.py:194-200`
passes a deep copy of the source parent config to `create_empty`. A duplicate
of an existing populated timeline can therefore carry nonempty tracks, clips,
and registry/media data. That is an existing duplicate workflow, not pristine
`timeline.init`; this proposal does not cut, normalize, or migrate it, and any
future replacement must retain its own source-copy positive separately.
