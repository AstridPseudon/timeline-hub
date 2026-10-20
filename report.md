# RT03 original film-reference visibility witness

## Result

Main's writable project-reference API is catalog metadata, not film authoring.
Creating a catalog reference does not create or move a visible occurrence or
clip, and it does not populate the timeline-reference read model. The original
film-reference positive therefore remains open; catalog CRUD is not evidence
that it has been restored.

The smallest current boundary is executable: Main accepts a project-owned raw
object through `media_id`, while the existing Agent occurrence-media/placement
recorder accepts a verified media selection and writes a visible clip. A new
carrier must not turn the reference into a clip birth or require a managed
generation five-tuple merely because those are the only current native media
recipes. If the agreed occurrence-local binding cannot carry the original raw
object case, Agent and Runtime need to discuss that boundary before designing
an extension.

## Original strict positive

`tests/test_runtime_exact_idempotency.py:81-124` is the preserved positive.
It creates a timeline shot, then a film reference with the exact shape
`{"reference_id": "exact-reference", "object_id": "object-digest", "role": "source"}`.
After restart it requires the same-key retry to return the original result,
changed payload under that key to return 409, a different key to refuse an
occupied identity, and durable `role == "source"`. It is strict `xfail`, not a
success-equivalent refusal.

The separate direct film-reference writer remains retired: the authority
controls in `tests/test_timeline_reference_authority.py` require 410 without
lookup, replay, or mutation. This witness does not weaken either assertion.

## Main before/after witness

Using an own `TemporaryDirectory`, `RealmStore`, and `RuntimeService` from this
checkout, the probe created a project and empty `main` timeline, ingested the
raw bytes `retained raw object` as `application/octet-stream`, and called
`create_project_reference` with that object's `media_id`. The exact output was:

```json
{
  "before": {"head_publication_id": null, "head_revision_id": null, "references": [], "shots": []},
  "after": {"head_publication_id": null, "head_revision_id": null, "references": [], "shots": []},
  "catalog_reference": {"reference_id": "rt03-reference", "media_id": "sha256:bda56aca1a65e67361c3aed9ed7d8e9e74b42302baa09c7fc427bc33afadeca3", "role": "canonical"},
  "same_key_replay": true,
  "changed_payload_status": 409,
  "occupied_identity_status": 409,
  "object_id_status": 422
}
```

This is a normal Main API witness, not an owner-film fixture or fabricated
accepted history. The source explains the result:

- `runtime_protocol/service.py:3449-3481` rejects `object_id`, requires
  project-owned `media_id`, performs `_command_replay` before the occupied-ID
  check, and writes only `project_references` plus `media_references`.
- `runtime_protocol/timeline_catalog.py:12-24` reads film `shots` and
  `timeline_references` separately from canonical parent heads.
- `runtime_protocol/service.py:4767-4770` allows the ordinary raw-object ingest
  path used by the probe; no generation/variant identity is required.

## Agent boundary and handoff

The immutable Main Agent source at
`/home/user/work/agent/astrid/sdk/timeline/commands.py:29-72` exposes 20 native
operations and no reference/provenance operation. The closest existing paths
are:

- `native_occurrence_media_commands.py:60-88,132-165`: the registry binding
  is derived from a verified selection containing `object_id`,
  `generation_id`, and `variant_id`, and `occurrence.add-media` creates a
  visible clip or `occurrence.swap-media` changes one;
- `native_placement_commands.py:81-104`: `placement.create` is an image clip
  birth, not a reference-only write.

Agent obligations:

1. A reference carrier must not add a visible occurrence/clip solely to encode
   the reference.
2. It must preserve the original exact `reference_id` and `role: "source"`,
   derive source identity from the accepted occurrence-local media/dependency
   custody, and never guess from a mutable catalog association.
3. It must not impose a managed-generation five-tuple on the original raw
   object case that Main accepts as a retained project object.
4. It must retain the original positive's same-key retry, changed-payload
   refusal, occupied-identity refusal, restart durability, and success
   assertions.

The already agreed occurrence-local carrier remains the only bounded seam. If
that carrier cannot represent this raw-object positive without either a visible
clip birth or the managed-generation selection tuple, this is the concrete
peer-discussion boundary. No new operation, DTO, endpoint, table, or fabricated
accepted history is proposed here.

## Evidence

- Pass — ephemeral Main API probe described above; output is recorded verbatim.
- Pass — Agent registry probe:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python - <<'PY' ... operations() ... PY`
  Output: 20 operations; `occurrence provenance candidates: []`.
- Pass — local Runtime service regression:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/tests:$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_runtime_domains.py::test_project_reference_mutations_roll_back_before_idempotency_replay`
  Result: `1 passed in 0.29s`.
- Pass — isolated central original-positive file:
  `request-test rt-m2-reference-original-visibility-equivalence targeted --files "tests/test_runtime_exact_idempotency.py"`
  Result: `2 passed, 1 xfailed in 3.54s`; the xfail is
  `test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`.
- Central targeted request:
  `... request-test rt-m2-reference-original-visibility-equivalence targeted --files "tests/test_runtime_exact_idempotency.py tests/test_project_reference_catalog.py tests/test_timeline_reference_authority.py"`
  Result: `3 passed, 1 xfailed, 179 errors in 6.40s`. The errors are fixture setup
  failures because the central runner lacked `ASTRID_CHECKOUT` (`/home/user/work/wt/astrid`);
  the strict original remains xfailed and was not treated as passing.
- No product/schema/test assertion changes, full suite, renderer, browser,
  owner film, public pin, generation, or new authoring operation.
