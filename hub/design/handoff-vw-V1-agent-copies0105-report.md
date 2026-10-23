Implemented V1 canonical Runtime copy adoption.

- Source: clean Runtime producer `691a9436ce3dbf2dcbfeaf959c85143c165fe4e2`
- Updated only:
  - `astrid/core/timeline/schema/timeline-config.schema.json`
  - `astrid_runtime_client/contract_metadata.py`
  - `astrid_runtime_client/generated.py`
  - `runtime.lock.json`
- Generator passed:
  `/home/user/work/venv-agent/bin/python scripts/refresh_runtime_client.py --producer /home/user/work/wt/rt-pin-691a9436`
- Lock validation passed; all 15 mapped files `cmp` exactly against producer sources.
- `artifacts.json --check`: passed.
- Targeted tests: `36 passed`.
- Ruff: 52 findings, identical to same-base inherited diagnostics.
- Mypy: 60 findings, identical to same-base inherited diagnostics. Requested `/tmp/astrid-u2-typecheck/bin/python` was unavailable; used `/home/user/work/venv-agent/bin/python`.
- `git diff --check`: passed.
- No full/browser/socket suites run.

Commit message written and `DONE` marker created.