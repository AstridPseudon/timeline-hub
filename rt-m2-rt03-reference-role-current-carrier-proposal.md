# RT-M2-RT03: smallest existing-carrier proposal

Status: proposal only. No Runtime code, schema, endpoint, DTO, or generated artifact was changed.

## What the user currently sees

The project reference catalog is a real, durable read model: `project_references` identifies the
reference and `media_references` retains its project-owned `media_id` and catalog role
(`runtime_protocol/canonical_schema.py:233-258`). `create_project_reference` verifies project
ownership and records that immutable media association (`runtime_protocol/service.py:3271-3304`);
`_project_reference_resource` returns it (`service.py:3739-3749`). This is the KEEP path. Its roles
(`canonical`, `used_as_input`, `depicts`, `inspired_by`) are catalog relations, not a film
placement/selection role.

The film read model is different. `timeline_resource` reads legacy `timeline_shots` and
`timeline_references` (`runtime_protocol/timeline_catalog.py:12-25`). The canonical film read is
the accepted parent revision and its `occurrences`/dependency manifest
(`runtime_protocol/service.py:2307-2319`). `verify_catalog_tail` expressly requires the legacy
snapshot to remain unchanged by canonical commits (`timeline_catalog.py:89-95`). Therefore a
catalog row or catalog association can be visible and correct while the film still has no
reference placement or role; that is not equivalent to the original positive assertion.

## Existing carriers

* Placement already has an authoritative carrier: the canonical parent occurrence. Runtime
  retains the complete authored occurrence in `parent_composition_revisions.payload_json` and
  projects its canonical placement fields to `composition_revision_occurrences`.
  The table already stores `placement_json`, `source_offset_json`, duration, speed, track,
  transform, gain, mute, and `provenance_json`
  (`runtime_protocol/canonical_schema.py:360-400`). `_normalize_occurrence` deliberately starts
  from a deep copy and preserves opaque fields (`runtime_protocol/service.py:2628-2693`).

* Exact film media selection already has a guarded carrier. Agent's
  `capture_placement_create` records the exact five-field Runtime media selection
  (`/home/user/work/agent/astrid/sdk/timeline/native_placement_commands.py:132-142`), and
  `capture_occurrence_add_media`/`capture_occurrence_swap_media` do the same for occurrence-owned
  media (`native_occurrence_media_commands.py:168-184`). Runtime commits the media dependency
  manifest alongside the immutable parent revision (`runtime_protocol/service.py:3101-3107`).
  This is the film source authority; do not infer it from a mutable catalog association.

* Agent already has role-bearing immutable entities: `ShotRevisionRecord.assets[*].role` and
  `generation_inputs[*].role` are validated (`/home/user/work/agent/astrid/core/timeline/shot_composition.py:78-123,558-580`).
  Those roles describe shot/source inputs, however, and do not by themselves identify a
  timeline-level reference or an occurrence placement. The existing occurrence `provenance`
  carrier is the smallest place to bind the missing film reference identity plus role to the
  occurrence without widening a public DTO. The exact namespaced key and role vocabulary require
  Agent semantic agreement; do not silently reuse catalog roles or the renderer's `source` track
  meaning.

## Bounded Runtime projection proposal

After Agent's sole EditCommand recorder emits an occurrence containing the agreed stable
reference identity, role, and link to the already-selected media, Runtime should, in the same
canonical acceptance transaction, project the accepted value into the existing
`timeline_references(id, timeline_id, object_id, role)` read model and its existing
`timeline_revisions.references_json` snapshot. `timeline_resource` already exposes that shape, so
this needs no new table, endpoint, or public DTO. The projection must derive `object_id` from the
verified canonical media/dependency, not from a caller-supplied catalog lookup.

The existing `verify_catalog_tail` invariant must be extended narrowly to recognize this
canonical-derived projection (and its revision snapshot) while continuing to reject any raw flat-
film legacy write; the current comment at `runtime_protocol/timeline_catalog.py:89-95` is the
guard that needs this distinction, not removal.

The projection must retain current identity rules: same accepted command/retry replays the exact
row; changed role under the same idempotency key is a 409; a different key cannot overwrite an
occupied reference identity with different media or role; project ownership and immutable media
verification remain mandatory. No direct legacy writer should be restored. The original
`tests/test_runtime_exact_idempotency.py:81-122` positive assertion stays OPEN until an executable
current command plus this projection proves creation, restart retry, changed-payload refusal,
different-key refusal, and durable `role == "source"`. The separate catalog assertion in the same
file (`:48-79`) does not close it.

## Evidence and decision

Inspected exact source/tests: `tests/test_runtime_exact_idempotency.py:48-122`,
`tests/test_timeline_reference_authority.py:277-395`,
`tests/test_project_reference_catalog.py:1-35`, and the Runtime/Agent files cited above. The
authority tests explicitly keep catalog CRUD while checking the film snapshot is unchanged, and
the original timeline-reference test is strict `xfail`, not a refusal-equivalent success.

Tests were not executed: this is a read-only source/design task and no implementation was made.
