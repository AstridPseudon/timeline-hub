# RT03 original unplaced film-reference witness

Status: read-only reconciliation, 2026-10-21. This document makes no product,
schema, Runtime, or generated-client change.

## Result

The original RT03 positive and the closed Agent carrier are different shapes.
The original positive is an **unplaced/raw film reference**: it creates a
durable `timeline_references` record with the exact `reference_id`, raw
`object_id`, and `role: "source"`, but it does not place an occurrence or add a
clip. Its effect is visible in the timeline read model, not as pixels in the
film. The current closed carrier is occurrence-owned: it requires an existing
placed occurrence and an existing local media selection, and therefore cannot
represent the original case without inventing placement or imposing managed
generation custody.

The original strict positive remains open. Do not count
`occurrence.add-media`, a project-catalog reference, or a refusal as its
success.

## Exact original effect

`tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`
uses the legacy timeline writers with:

```json
{
  "reference_id": "exact-reference",
  "object_id": "object-digest",
  "role": "source"
}
```

The accepted result is a timeline-scoped reference row and its
`timeline_revisions.references_json` snapshot. The test also creates a shot,
but its `reference_ids` is empty; the reference is not a shot item, occurrence,
or visible clip. After restart, the original key must replay exactly; a changed
payload under that key and a different key targeting the occupied identity must
both return 409; the durable row must still say `role == "source"`.

The original test is still a strict `xfail` on current Runtime because the
direct timeline writers are retired. That preserves the positive assertions;
it is not evidence of a successful refusal.

## Executable witnesses already run

### Existing Agent carrier

The completed Agent probe ran:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_film_reference_closed_carrier.py
4 passed in 0.98s
```

The relevant witness is
`test_unplaced_reference_cannot_be_reclassified_as_an_occurrence_birth`:

1. An occurrence birth carrying `timeline_reference` is rejected by the
   existing command shape.
2. Removing that field makes the same birth executable, but it creates
   `occurrence:unplaced-occurrence` and a placement entry.

Thus the existing birth path cannot carry an unplaced reference. The other
three passing cases prove only the placed `occurrence.add-media` carrier's
local media binding, inverse, and guards. They do not close RT03.

### Existing Runtime project-catalog probe

The completed Runtime visibility probe ingested the raw bytes
`retained raw object` and created a project-catalog reference. Its recorded
result was:

```json
{
  "before": {"head_publication_id": null, "head_revision_id": null, "references": [], "shots": []},
  "after": {"head_publication_id": null, "head_revision_id": null, "references": [], "shots": []},
  "catalog_reference": {
    "reference_id": "rt03-reference",
    "media_id": "sha256:bda56aca1a65e67361c3aed9ed7d8e9e74b42302baa09c7fc427bc33afadeca3",
    "role": "canonical"
  },
  "same_key_replay": true,
  "changed_payload_status": 409,
  "occupied_identity_status": 409,
  "object_id_status": 422
}
```

This is an executable no-placement witness, but it is not the RT03 positive:
the catalog operation leaves the film timeline unchanged and rejects the
film-shaped `object_id` input. The original positive requires a successful
timeline reference with `role: "source"`.

## Catalog relation: same behavior?

No. There is one narrow similarity: both paths can be durable and idempotent
without producing on-screen pixels. Their authorities and effects differ:

| Path | Durable relation | Identity/role | Film-history effect |
| --- | --- | --- | --- |
| Original RT03 positive | `timeline_references` and `timeline_revisions.references_json` | raw `object_id`, `role: "source"` | Adds a timeline read-model reference; no placement or clip |
| Project catalog | `project_references` and `media_references` | project-owned `media_id`, catalog role `canonical` | No timeline reference, occurrence, head, or shot change |
| Closed Agent carrier | occurrence provenance plus accepted closure | `reference_id`, `role: "source"`, occurrence-local `asset` | Requires a placed occurrence; Runtime may project its verified media to the timeline reference row |

This is the settled film-versus-catalog boundary: catalog metadata may advance
without accepted film history, while placement, selection, source pins, and
authored timing belong to the film edit/commit path. Catalog CRUD therefore
cannot be used as a positive substitute for RT03.

## Smallest peer decision/proposal

Peer decision needed: acknowledge the existing closed carrier as **placed-only**
and keep the original unplaced positive open, or explicitly authorize a
separate minimal reference-only acceptance seam at the existing Runtime
commit/provider boundary.

If the latter is authorized, the smallest proposal is a source-only design
review—not implementation in this handoff—with these invariants:

- preserve the exact original `reference_id` and `role: "source"`;
- derive the raw object from existing accepted project media/dependency
  custody, without a caller lookup or second media authority;
- create no occurrence, placement, clip, catalog reclassification, or
  managed-generation five-tuple requirement;
- retain restart retry, changed-payload refusal, occupied-identity refusal,
  and durable success assertions from the original test; and
- keep direct legacy writer refusal and project-catalog CRUD as separate
  controls.

Until that peer decision and a real Agent/Runtime pair exist, the accurate
status is: **placed occurrence carrier qualified; unplaced/raw RT03 positive
not represented**. `occurrence.add-media` does not solve an unplaced reference.

## Source anchors

- Frozen/current strict positive: `tests/test_runtime_exact_idempotency.py:81-124`.
- Current Runtime 95bd project catalog writer:
  `runtime_protocol/service.py:3474-3507`; it writes
  `project_references` and `media_references` only.
- Current Runtime 95bd timeline read projection:
  `runtime_protocol/timeline_catalog.py:12-25`; it reads
  `timeline_references` separately from project-catalog rows and canonical
  parent heads.
- Current Runtime 95bd storage shape:
  `runtime_protocol/canonical_schema.py:135-176`.
- Closed Agent carrier contract: the orchestrator evidence document
  `scratchpad/orch/design/agent-rt03-film-reference-role-carrier-contract.md`
  (the occurrence-local `provenance.astrid.timeline_reference` v1
  vocabulary).
- Completed prior evidence: Runtime's original visibility witness and Agent's
  closed-authoring report in the orchestrator scratchpad.

