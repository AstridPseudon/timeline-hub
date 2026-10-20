# Runtime current S3 native birth reservation proof

Status: PRIVATE qualification complete; no Runtime source change required. The requested exact same-immutable-image boundary was explicitly disproved for normal native allocation, and the existing occupied-destination guard remained intact for reachable occupied cases.

## Exact qualification tuple

- Agent source: `537c2ecd28f92b391c79e383e0e045fd71b3258f`, whole source exported privately.
- Agent schema: SHA256 `8a55a9fd84d6fc188e48f63976dacc1c27ea25c7747ea88e7eba7589974dd85a`, 54 definitions / 28 operations.
- Runtime source: `b748ae723b51c6d578ba7a393209ce37d6e2b0c3` (private archive).
- Private Runtime generation used normal `generators/generate.py`, `--check`, `scripts/artifact_manifest.py`, and `--check`, with the exact Agent schema as private generator input only.
- Generated Runtime bundle `runtime_protocol/schemas/timeline-commit-bundle.json`: SHA256 `a694f3caf7efcc7c39fa4083742c845761eba9d254f9d2f85e4bb9f5f83a0013`.
- Generated `contract/artifacts.json`: SHA256 `420af466ea8a628cce76adb57857b092b34a9318bcb77f04d2960b4bd8c4bc88`.
- Generated `runtime_protocol/contract_metadata.py`: SHA256 `ee7ec48d160dea71fee89cedc5403f78869b5ae6a9c56ae5d82ee8a31dd230d1`.
- Public Runtime S2 source/schema in the assigned worktree was not modified.

## Native evidence

The original native first-birth helper ran against the private generated pair for both paths:

```text
_prove_birth(..., grouped=False): exit 0
_prove_birth(..., grouped=True): exit 0
```

This is the normal bootstrap → native `occurrence.create` path, including invalid-timing refusal, typed created facts, same-project other-timeline occupancy refusal, trusted inverse/redo, dependent-inverse refusal, restart, and exact retry.

The original S3 reviewed cohort test also passed:

```text
tests/editing_conformance/test_s3_reviewed_cohort_runtime.py::test_init_occurrence_media_parent_swap_word_grouped_inverse_reload_restart
1 passed in 8.27s
```

## Exact-image boundary

The authority probe used normal Runtime fixture APIs, `create_timeline`, native parent-track acceptance, native `occurrence.create` dry-run, and native acceptance. It did not insert SQL rows or fabricate history.

For a dry-run candidate and an unrelated same-project occupant on another timeline, the generated immutable images were different:

```text
candidate shot revision: authoring-shot-revision-f17e4ea6580b2a65770af3dbef27ec4769b9606b80042330ec17196b48f48e17
candidate digest:        sha256:ff7ea24b5766840819590ca6e3c9c8f9733aa7f2d7bdad3f98c9da3c481e22b7
candidate internal:      authoring-timeline-revision-f8b3f6e797c2c17363cd886f5c45eaae42ba592b5ccaff2bbe213692a6ad32d7

occupant shot revision:  authoring-shot-revision-9552490beeb34e98ce6eef9ef95a73f31ded44b603fcfeee1d27b1a3ec651170
occupant digest:         sha256:45e0acdc4ef83d5e732736bb7218a84e0a9226e7065e095a9eea505f91eb8473
occupant internal:       authoring-timeline-revision-c3e20c4e03d29d7ee109a608d63a70b9a90507f76b36f5a9ea5931aa8d3054ed
```

The same normal setup against a foreign project likewise produced different immutable identities. The original target command with the occupied shot identity was refused with HTTP 409 `destination_occupied`.

This is an allocator/API impossibility, not a missing Runtime branch: Agent’s normal compiler derives the new internal revision from `(project_id, timeline_id, allocated shot identity, internal payload)`, and the shot revision payload embeds that internal revision. Changing the unrelated timeline or shot identity necessarily changes the immutable image. The native source is explicit at `astrid/core/timeline/authoring_bundle.py` in the `authoring-timeline-revision` and `authoring-shot-revision` identity construction. The exploratory different-shot target submission also encountered an unrelated idempotency mismatch before authority; it is not counted as acceptance evidence. No native command was forged to manufacture an equal image.

## Runtime guard and historical controls

The private Runtime continued to preflight actual project-wide shot occupancy before persistence. The original native helper refused the same shot on another timeline before and after trusted inverse. The existing C4 historical-reuse controls were retained and passed, including reuse without rewriting `project_shots` and preservation of a newer global shot head.

Central bounded integration, exact requested files:

```text
request-test rt-m2-current-s3-birth-reservation-proof targeted --files \
  "tests/test_timeline_projection_occupancy.py tests/test_timeline_legacy_occupancy.py tests/test_timeline_commit_acceptance.py"
91 passed, 2 deselected in 35.50s
```

No Runtime branch fix was warranted: adding a blanket image-based rejection would alter allowed C4 historical reuse, while the requested new semantic birth with an exactly reused immutable image is not reachable through the normal allocator/API.

## Limits

This is private qualification only. No public freeze, merge, pin, publication, full suite, browser, socket, or live-service qualification was performed. The private pair was generated in an ORCH worker directory and did not alter shared dependencies or the assigned worktree.

