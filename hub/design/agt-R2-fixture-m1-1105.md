## Report

Updated [`test_recipe_m1_commands.py`](/home/user/work/wt/agt-R2-fixture-m1-1105/tests/editing_conformance/test_recipe_m1_commands.py:37) to use production `bundle_from_document()` with the complete `_runtime_document` closure.

Tests:

- Baseline: 101 passed, 25 failed.
- Final targeted run: 116 passed, 10 failed.
- Remaining failures are shared-occurrence redo cases requiring authenticated `commit.materialization` bindings absent from the recorder-only helper.
- Ruff: passed.
- Typecheck-v2 mypy: passed.
- `git diff --check`: passed.
- JUnit: `evidence/m1.xml`.

Blocked on a faithful accepted-boundary builder for `track.remove`/`clip.remove`; no authority was fabricated. BLOCKED marker and commit message were written.