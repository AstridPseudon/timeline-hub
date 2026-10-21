# Agent -> Runtime/App2: raw OLD swap full-floor source packet

Status: **PRIVATE SOURCE-ONLY SUCCESSOR READY**. This packet is for the
Runtime/App2 hub and ORCH/design. It does not request Runtime artifact
generation, client regeneration, pin movement, merge, freeze, adoption, or
activation.

## Exact source identity

- Settled source patch: `9b9baa01ab43bce144f3f1e6d6d73722df99a8e7`
  (`feat(timeline): add raw old swap successor`), tree
  `f924720e382d442f391d45cdc6e24064be9a6a5e`, parent
  `5672d2b7deee2bfe2ab375fd6db5fc35a192591d` (`floor5672`).
- This worker's composed base is `a905fa29b1bb47739df438f4203ed987be588e46`,
  tree `5871915b4ed820e1a9c17a44f20ffd683f05df8c`; the eight raw-OLD paths
  are unchanged from its `floor5672` parent and were applied byte-for-byte
  from the approved successor patch.
- The harness-assigned final commit/tree is intentionally not available until
  worker exit; no direct git commit or ref mutation was performed.

## Contract and changed paths

The source adds only the closed raw-OLD alternatives:

- `clip.swap-media@2` with `old_media` exactly
  `{"media_id", "content_digest"}` and NEW exactly the existing five-field
  `selected_media` envelope.
- `occurrence.swap-media@3` with the same OLD/NEW shape.
- Existing `occurrence.swap-media@2` and ordinary parent
  `clip.swap-media@1` remain immutable selected-media lanes.

The implementation preserves the existing request-scoped `raw_media_info`
read for OLD and `selected_media` read for NEW, original-base clip/alias/raw-pin
guards, source-window and sibling scope, exact create-or-require NEW alias
behavior, and existing recording/rebase/inverse/retry machinery. It adds no
caller duration, adoption, latest lookup, or metadata authority. No live
callers were changed (`live callers changed: NONE`), and no Runtime artifact,
generated client, public pin, or App/Runtime source was touched.

Changed Agent paths:

```text
astrid/core/timeline/schema/edit-command.schema.json
astrid/sdk/timeline/commands.py
astrid/sdk/timeline/commit.py
astrid/sdk/timeline/native_occurrence_media_commands.py
tests/editing_conformance/test_raw_old_swap_successor.py
tests/sdk/test_timeline_composed_schema.py
tests/sdk/test_timeline_current_union_schema.py
tests/sdk/test_timeline_materialization_schema_union.py
```

## Schema and floor evidence

- Raw schema SHA-256: `9e4b4421ebbba94f13f8f286c7ea1df5eb9ca128142ed904c92a993985954cfd`.
- Canonical `json.dumps(indent=2) + newline` SHA-256:
  `d3274d7ed2d4bd80691472dd94daf8f4b8041fc184f39f1dd562d5de5d6a15c2`.
- Inventory: 64 definitions, 36 closed operation clauses.
- Targeted floor reconstruction passes byte-exact ordinary `6ba7` and the
  existing reviewed floors; the raw-OLD definitions/branches are removed only
  when reconstructing the earlier floors.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_raw_old_swap_successor.py \
  tests/sdk/test_timeline_composed_schema.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_materialization_schema_union.py
69 passed in 183.00s (0:03:02)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B -m ruff check --no-cache \
  astrid/sdk/timeline/native_occurrence_media_commands.py \
  astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py \
  tests/editing_conformance/test_raw_old_swap_successor.py \
  tests/sdk/test_timeline_composed_schema.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_materialization_schema_union.py --output-format=concise
All checks passed!

git diff --check
passed
```

Not run by scope: Runtime/client/schema generation, full, browser, socket,
renderer, and native end-to-end raw qualification. The existing approved
158-test source review remains the independent broader evidence; this worker
ran only the requested bounded raw-OLD handler/schema lane.
