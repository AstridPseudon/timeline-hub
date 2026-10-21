# Agent film transcript association — recorded source report

Date: 2026-10-21  
Worker: `agt-m2-film-transcript-recorded-source`

## Source implementation

Added the unfrozen `transcript.associate` Agent operation. It is selected by
`parent/asset:<asset-id>` and uses the existing normal EditCommand recorder,
provider hydration, inverse, and rebase machinery. Project transcript CRUD
remains catalog state; transient projections remain derived.

The operation:

- hydrates and verifies the exact new `DocumentPin` and, for replacement, the
  exact prior pin through the existing `transcript_source(pin)` seam;
- verifies project scope, canonical transcript identity, media/source ownership,
  ordered stable segment IDs, stable word IDs, and bounded source timing;
- records the raw `(asset, media, source)` owner, source-item membership/order,
  stable segment/word bindings, and exact transcript dependencies;
- writes only the parent `transcriptReferences` and
  `sourceItemsBySchemaRef["astrid.transcript_segment/v1"]` fields, preserving
  unrelated source schemas, ordering, opaque envelopes, and parent data; and
- preserves the source fields through the existing canonical document conversion.

Caption/review reconciliation is deliberately not implemented in this first
unit. If the existing generated-caption or transcript-review provenance would
need an identity change, capture refuses atomically with:
`caption/review reconciliation would change unsupported data; follow up with a
native reconciliation carrier`.

The published S2 compatibility slice remains exact: the unfrozen operation and
its schema definition are excluded from that historical floor only. The current
source schema inventory includes the operation.

## Evidence

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_film_transcript_association.py
=> 4 passed

ruff check astrid/sdk/timeline/native_transcript_association.py \
  tests/editing_conformance/test_recipe_film_transcript_association.py \
  astrid/sdk/timeline/_recording.py astrid/sdk/timeline/commands.py \
  astrid/sdk/timeline/commit.py
=> All checks passed
```

The existing semantic spike passed before this source change. The focused
current Agent schema/floor assertions passed after adding the operation:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/sdk/test_timeline_current_union_schema.py::test_next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions \
  tests/sdk/test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort
=> 2 passed
```

The combined semantic spike, production source tests, and exact schema/floor
assertions passed together:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_film_transcript_association_spike.py \
  tests/editing_conformance/test_recipe_film_transcript_association.py \
  tests/sdk/test_timeline_current_union_schema.py::test_next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions \
  tests/sdk/test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort
=> 14 passed
```

The complete current Agent schema compatibility file also passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/sdk/test_timeline_current_union_schema.py
=> 34 passed in 149.92s
```

No full, live, browser, socket, Runtime, App, or generated-client suite was
run.

## Boundary for Runtime/App2

This is source-only Agent work. Runtime hydration/accepted-closure support and
App2 command production are not claimed. Runtime/App2 ACK should be requested
against this exact source report only after reviewing the new operation,
canonical parent-payload source fields, and the explicit reconciliation refusal.
