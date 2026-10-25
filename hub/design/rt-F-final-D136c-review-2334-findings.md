# D136c private preservation review — FAIL

## F1 — blocking: target inventory is dead metadata

The candidate advertises 101 Python targets plus the preserved TypeScript target in
`core-inventory.json`, but the existing `run-final-services.py` core runner has a
hard-coded 98-file `CORE_TEST_FILES` selector and does not read `core-inventory.json`.
The exact set difference is:

- `tests/test_timeline_commit_ancestry_reads.py`
- `tests/test_timeline_commit_closure_growth.py`
- `tests/test_timeline_missing_observation_diagnostics.py`

This violates the task requirement that the new provenance/helper be consumed by the
future existing runner and that the target list not be dead metadata. The private
inventory and matrix preservation checks pass, but they do not qualify execution of
the omitted targets.

No other finding was identified in this bounded review.

Required next step: update the owner-approved final runner/selector so it consumes the
authoritative inventory or includes the exact 101-target set, then rerun the same
private checks and obtain a fresh review. This review did not modify the candidate.
