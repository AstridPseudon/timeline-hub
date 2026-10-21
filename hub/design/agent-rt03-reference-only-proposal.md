# RT03 unplaced/raw reference-only command proposal

Status: **SOURCE-ONLY PROPOSAL for Agent/Runtime peer review** (2026-10-21).
This handoff does not change the Agent repository, Runtime, a DTO, a store,
an endpoint, a generated client, a schema freeze, a pin, or integration state.
The original strict Runtime positive remains open and must remain a strict
`xfail` until a real current Agent/Runtime pair passes it.

## Decision

The current native registry has no reference-only carrier.

- `occurrence.add-media` and `placement.create` are occurrence-owned births;
  they require a placed occurrence, a clip row, and the existing managed
  `MediaSelection` five-tuple. They cannot represent RT03 without inventing
  placement.
- The existing occurrence `provenance.astrid.timeline_reference` carrier is
  deliberately placed-only: it names an occurrence-local registry asset and
  is projected only from an accepted occurrence closure.
- `shot.pool` is also occurrence-owned and is not an unplaced timeline
  reference.
- The parent registry is an existing read authority, not a reference list.
  Project-catalog references are a different owner and role and are not a
  film-history substitute.

Therefore the smallest executable seam is one closed Agent opcode that writes
one timeline-scoped, namespaced reference record and nothing visible:

```text
timeline.reference v1
select: "parent"
intent: {}
```

This is a proposal for one bounded command, not permission to implement or
freeze it.

## Proposed command shape

The operation's closed args are exactly:

```json
{
  "reference_id": "exact-reference",
  "role": "source",
  "media": {
    "asset": "raw-reference-asset",
    "object_id": "sha256:<accepted-object-digest>"
  }
}
```

Rules:

1. `reference_id` is the exact opaque timeline-reference identity. It is the
   identity that must appear as `timeline_references.id`; it is not a catalog
   name, display label, or lookup key.
2. `role` is a closed literal `source` in v1. Catalog roles such as
   `canonical`, `used_as_input`, `depicts`, or `inspired_by`, and generation
   input roles, are not accepted.
3. `media` is a deliberately smaller raw-object claim, not the current
   managed `MediaSelection`: it has only `asset` and `object_id`. It has no
   `generation_id`, `variant_id`, or `catalog_digest`, and therefore does not
   require managed-generation custody. The `object_id` is a checked claim,
   never caller authority.
4. `asset` must name one already-existing parent registry asset. The command
   does not create or replace a registry entry, import bytes, query the
   project catalog, or resolve a display name.
5. The supplied `object_id` must equal the one canonical immutable object
   identity in that accepted registry entry (`object_id`/`media_id` according
   to the existing normalization; contradictory identities refuse). The
   accepted registry/closure and dependency manifest are authoritative.

The proposed authored carrier is the existing open timeline namespace:

```json
{
  "config": {
    "app": {
      "astrid": {
        "timeline_references": {
          "exact-reference": {
            "version": 1,
            "reference_id": "exact-reference",
            "role": "source",
            "asset": "raw-reference-asset",
            "object_id": "sha256:<accepted-object-digest>"
          }
        }
      }
    }
  }
}
```

The `object_id` is retained to preserve the original raw reference shape, but
the handler must derive/verify it from the accepted registry entry before the
write. Runtime's future projection must repeat that check against the accepted
closure and manifest; it must not trust this duplicated JSON field by itself.
The `asset` link is the source identity needed to prove which existing
registry binding supplied the raw object.

The key is a map key rather than a list position so the command can guard one
reference identity, preserve exact absent/null/present distinctions, and let
the existing recorder inverse one leaf without rewriting unrelated references.
The map is sorted only when Runtime derives the legacy `references_json`
projection; authored order is not semantic.

## Agent execution/capture contract

The future handler should use only existing recorder/state operations:

```text
validate closed args and select == parent
read parent.config.app.astrid.timeline_references (or create its containers)
read destination leaf [reference_id]
refuse if destination is already present (identity_collision)
read parent/registry.assets[asset] through the effective parent registry
require exactly one accepted object identity and object_id equality
record dependency("reference.media", "media", exact raw media pin)
write destination leaf with the five-field-free carrier record
```

The exact recorder dependency pin (an existing Agent dependency-custody
record, not a new public/generated pin) is:

```json
{
  "asset": "raw-reference-asset",
  "object_id": "sha256:<accepted-object-digest>",
  "registry": "parent/registry",
  "role": "source"
}
```

It is an Agent `AgentDependency` of kind `media`, policy `exact`, not a new
Runtime DTO. The handler must record the complete registry binding read (or
the exact canonical subset used by the existing registry resolver) so an
asset/object ABA or a registry replacement refuses on replay and inverse.
The command's `reads`/`expect` must include the destination's `absent` state
and the exact source registry binding. No `occurrence`, `shot`, `clip`,
`track`, placement, or visible-media write is allowed; `created` remains empty
because this is a namespaced property birth, not a visible timeline entity
birth.

The existing `Recording.object`/property-write behavior is sufficient for the
namespace containers. The operation must not use `create_entity`,
`occurrence.add-media`, `placement.create`, or the managed-media `_verified`
path. It should reuse the existing effective parent registry and canonical
media identity normalization rather than add a second registry resolver.

## Runtime boundary (future peer implementation only)

No Runtime implementation is included here. When Runtime reviews/implements
the counterpart at the existing parent-composition acceptance boundary, it
must:

- read only the accepted project/timeline closure;
- validate the namespaced record's `version`, exact `reference_id`, literal
  `role: "source"`, asset alias, and object identity;
- resolve the alias against the accepted parent registry and require the
  normalized object in the accepted dependency manifest/media custody;
- atomically project exactly
  `{reference_id, object_id, role: "source"}` to the existing
  `timeline_references` row and `timeline_revisions.references_json`;
- preserve unrelated legacy references and scope all occupied-ID/state checks
  to the authenticated project and timeline; and
- derive removals only for records proven to be this carrier's prior
  projection, so a clear/restore cannot delete an unrelated legacy reference.

The projection must not use a caller hash as authority, perform a project
catalog lookup, reclassify a project-catalog role, invent a generation
five-tuple, create an occurrence, or add pixels. Direct legacy timeline
reference writers remain a separate refusal control.

## Required focused tests — one behavior per test

These are acceptance requirements for the eventual pair, not claims that this
proposal passes them today.

### 1. Create: unplaced/raw positive

`test_timeline_reference_create_is_unplaced_and_records_exact_raw_source`

- Start with an accepted parent registry asset whose object is in the
  project/closure media authority, but no occurrence/clip uses it.
- Capture and execute `timeline.reference`.
- Assert the authored parent namespace contains exactly the requested
  `reference_id`, raw object identity, and `role: "source"`.
- Assert parent occurrences, shots, internal timelines, clips, tracks, and
  registry binding are unchanged; `created == []`; the command records the
  absent destination guard and exact media dependency.
- Assert the projected film read model has one timeline reference and zero
  new shots/placements/clips/pixels.

### 2. Retry: original idempotency and restart

Keep the original strict test and assertions unchanged:
`tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`.

The eventual current Agent/Runtime pair must submit the same commit with the
same idempotency key, simulate a lost acknowledgement, restart Runtime, and
retry. The second response must be the original accepted result; the durable
row must still contain the exact raw `object_id` and `role == "source"`.
Changing payload under that key must remain 409. A catalog-only or refusal
result is not a pass.

### 3. Inverse: guarded remove/redo

`test_timeline_reference_inverse_removes_only_its_carrier_and_redoes_exactly`

- Accept the reference, inverse its accepted publication, restart, and redo
  through the existing guarded `timeline.inverse` machinery.
- Assert inverse removes only the namespaced reference/projection, retains the
  registry asset and unrelated legacy reference, and never removes a clip,
  occurrence, shot, or media object.
- Change the source registry binding or insert an intervening write, including
  an A→B→A restoration, and assert inverse refuses with the existing guard
  reason and no partial write.

### 4. Occupied identity: no overwrite

`test_timeline_reference_occupied_id_refuses_without_write`

- Seed `reference_id == "exact-reference"` with another source object or
  role, then submit a different idempotency key targeting that identity.
- Assert 409 identity conflict/refusal, unchanged namespace, unchanged
  projection, and unchanged revision history.
- Also cover a foreign-timeline row with the same ID: it must not be treated
  as this timeline's available identity and must not be overwritten.

The original strict positive remains the cross-repository gate. These four
focused tests may be added only when the owners authorize the Agent/Runtime
pair; they must not be weakened, deleted, or converted to a green refusal.

## Existing seam evidence

- `astrid/sdk/timeline/commands.py:28-72` has the closed native operation
  registry; it contains no reference-only or parent-data reference operation.
- `astrid/sdk/timeline/native_occurrence_media_commands.py:60-88` and
  `astrid/core/timeline/schema/edit-command.schema.json:1533-1560` show the
  current five-field managed `MediaSelection` and occurrence-local registry
  binding; this is intentionally not reused for RT03.
- `astrid/sdk/timeline/_recording.py:87-151` records arbitrary property reads,
  writes, bindings, and exact dependencies; this is enough for one guarded
  namespaced leaf without a new recorder family.
- `astrid/sdk/timeline/_command_state.py:340-417` supports recorded parent
  property writes while refusing unrecorded containers; this supplies the
  bounded namespace-container creation and exact inverse boundary.
- `astrid/core/timeline/astrid_ns.py:41-48` treats unknown keys under
  `config.app.astrid` as application-owned namespaced film data.
- `astrid/core/timeline/parent_registry.py:7-22` and
  `astrid/core/timeline/authoring_bundle.py:540-555` provide the existing
  effective parent registry authority.
- `astrid/core/timeline/authoring_bundle.py:778-805` preserves open parent
  authored payload data and derives the dependency manifest from accepted
  canonical payload identities.
- The read-only witness
  `agent-rt03-original-unplaced-reference-witness.md` establishes that the
  original reference is timeline-scoped and unplaced, and that the current
  occurrence carrier and project catalog are not equivalent.

## Evidence from this source tree

Current seam neighbors were run directly after inspection:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/timeline/test_authoring_bundle.py \
  tests/editing_conformance/test_recipe_occurrence_media.py \
  tests/editing_conformance/test_recipe_m2_placement_create_unplace.py
125 passed, 1 deselected in 24.69s
```

This is only evidence for the existing authoring/registry/media carriers. It
does not qualify RT03 and no full suite was run.

## Non-goals and hold points

- No Runtime code, DTO family, SQL table/store, endpoint, generated client,
  schema freeze, public artifact, generation, pin, adoption, or integration
  change is proposed here.
- No visible placement or occurrence birth is permitted.
- No managed-generation five-field requirement is permitted for this raw
  reference.
- No project-catalog role or CRUD operation is a substitute.
- No claim is made that the original strict positive is green; it remains
  open pending the actual pair and all four focused behaviors above.

