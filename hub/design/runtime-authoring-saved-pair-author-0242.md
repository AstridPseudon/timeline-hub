## Report

Changed only `tests/timeline/test_authoring_bundle.py`.

- Preserved `previous_revision_id` and asserted saved-pair actions bind `parent-1 → saved-revision`.
- Retained strict coverage for both `current_head` actions and all original mapping/request/reply predicates.
- No product files or other tests changed.

Checks:

- Isolated `5b5eab591a` source qualification: **6 passed, 63 deselected**.
- Ruff on both fixture files: **passed**.
- Parent/final mypy comparison: **0 diagnostics, 0 new identities**.
- `git diff --check`: **passed**.

The direct b782 base still fails two selected tests at the known Agent no-op commit-builder gap; this fixture change does not weaken or mask that behavior. Commit message and `DONE` marker were created.