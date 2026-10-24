## PASS — F-D52-shot-set

- Repaired only `tests/editing_conformance/test_recipe_shot_set.py`.
- Root cause: current inverse path requires authenticated `_runtime_document`; legacy detached fixtures lacked it, causing `history_unavailable`.
- Added faithful canonical Runtime closure setup from existing `_closure` records. Portable fixtures are migrated in `$TMPDIR`; checked-in fixture and all original test bodies/assertions remain unchanged.
- Production caller/source inspected: Agent `commit.py` → `execute(commit_request)` → compiler/materialization; Runtime route uses `timeline_commit_execution.py`.

Tests:

- Assigned selectors: **17 passed**
- Full shot-set file: **61 passed**
- Ruff: passed
- Scoped mypy, parent/current diagnostics: both passed with zero new diagnostics
- `git diff --check`: passed

No production, schema, client, generated-file, or Runtime changes. No HTTP/live custody or full-suite proof was run per task limits. Evidence is under the worker `evidence/` directory.