Implemented the `media.admit` provider-only census fix in:

- [test_timeline_composed_schema.py](/home/user/work/wt/agt-F-schema-census-fix-0605/tests/sdk/test_timeline_composed_schema.py:28)
- [test_timeline_current_union_schema.py](/home/user/work/wt/agt-F-schema-census-fix-0605/tests/sdk/test_timeline_current_union_schema.py:243)

Tests:

- Baseline: 2 expected failures.
- Former failures: `2 passed`.
- Full two-module cohort: `41 passed`.
- Ruff: passed.
- Artifact manifest: current.
- Runtime vendor lock: passed against pinned producer.
- Diff/schema checks: passed; 30 unique wire branches preserved.

Blocked diagnostics:

- Parent mypy blocked by missing `types-PyYAML` and Python 3.13/NumPy stub incompatibility.
- Hermetic doctor could not import the uninstalled worktree; direct doctor reported typed `runtime_unavailable`.
- Hygiene check reports pre-existing tracked `test-support/` entries.

Commit message written to the requested path; `DONE` marker created.