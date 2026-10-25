# D136a source intake validation

## Exact custody

- Base preimages matched donor parent `c99214a227154df5fbaf681c2e0fc52c54500025` byte-for-byte for both authorized paths.
- Final working-tree Git blobs match donor `20dbfdef45f71fa28a63f5382c154f5cca50b83a` exactly for both paths.
- Donor commit changed exactly the two authorized paths; worktree scope audit reports exactly those two paths.
- `_timing_evaluators.py` remains byte-identical to the actual base.
- Donor binary diff SHA-256: `1f3f7af792722507c9d61ad7f4c6f13468424fb75b7a5fe60daa3b44e9cdde91`.

## Static checks

- `PYTHONPYCACHEPREFIX=/tmp/w-d36965b2a0/d136a-static/pyc311 /usr/bin/python3.11 -m py_compile astrid/sdk/timeline/validation.py tests/sdk/test_d136_fps_upstream_compat.py` — PASS.
- `/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/validation.py tests/sdk/test_d136_fps_upstream_compat.py` — PASS (`All checks passed!`).
- `MYPY_CACHE_DIR=/tmp/w-d36965b2a0/d136a-static/mypy /home/user/work/venv-agent/bin/mypy astrid/sdk/timeline/validation.py tests/sdk/test_d136_fps_upstream_compat.py` — PASS (`Success: no issues found in 2 source files`).
- Known repository mypy baseline remains 1902 findings for the full `astrid`/`scripts/reshape` scope, as recorded in `scripts/reshape/baselines/mypy_astrid.json`; this scoped check did not rewrite the baseline.
- `git diff --check HEAD` — PASS.

## Behavior boundary

Behavior suites, production matrix, and App original9/current9 proof were not run here. The independent donor review reports are retained as DONOR evidence only; this source-only intake claims no behavior/core/ship credit.
