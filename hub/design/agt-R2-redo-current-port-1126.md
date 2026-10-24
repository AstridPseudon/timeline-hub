## Report

- Ported only the authorized helper blobs onto `b4c1ec83fb`:
  - `test_captured_nested_redo.py` → `afd57690…`
  - `test_recipe_m2_auto_placement.py` → `770aa109…`
- No production, schema, pin, fixture, or test-body changes. No caller-binding splice remains.

Validation:

- Exact six targeted pytest cases: **6 passed**
- Scoped Ruff: **passed**
- Qualified mypy: **passed**
- Test AST parity: **passed** (9 + 19 tests; also matches `c2b1f7e5a3`)
- `git diff --check`: **passed**
- Durable JUnit, origins, and AST evidence saved under the worker evidence directory.
- No full suite or captured codec-positive test run.

Commit message written and `DONE` marker created.