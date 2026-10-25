## Report

Implemented the F-D86 repair in [test_cli_document_commit.py](/home/user/work/wt/agt-D86-main-CLI-return-2358/tests/packs/timeline/test_cli_document_commit.py).

- Deleted `_runtime_idempotency`; retries/refusals now use genuine Runtime store/provider behavior.
- Corrected the oracle to `error.details["reason"] == "idempotency_mismatch"`, matching Runtime’s store and public error mapping.
- Preserved all 12 bodies, assertions, parameters, decorators, and 8 assigned selectors.
- Only the assigned test file changed.

Checks:

- `py_compile`: pass
- Ruff: pass
- mypy: pass
- `git diff --check`: pass
- AST conservation: pass
- Baseline Ruff: 11 pre-existing `F811` diagnostics; no candidate diagnostics
- Pytest/service/full qualification: not run per source-only instructions.

Commit message and evidence are recorded; `DONE` created. Branch is ready for protected review and merge.