## Done

- Updated `astrid/sdk/timeline/commit.py` to replay authenticated native fork provenance with source, owner, revision/digest, payload/order, binding, step, and boundary validation.
- Added focused production regression: `tests/timeline/test_fork_reservation_replay.py`.
- Wrote commit message and `DONE` marker.

## Tests

- Focused timeline tests: **32 passed, 1 deselected**
- Fork/duplicate controls: **79 passed, 1 deselected**
- Ruff: passed
- Mypy: passed
- Vendor lock, artifact manifest, and `git diff --check`: passed

Evidence XML is in the assigned evidence directory. Full suite and independent final joined review remain unrun.