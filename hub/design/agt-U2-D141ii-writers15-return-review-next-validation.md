# D141ii writers15 return validation

## Targeted execution

The author/current exact return selector set was independently run with the required environment and private basetemp/cache:

`ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-U2-D141ii-writers15-return-review-next:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -n 3 --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-D141ii-writers15-return-review-next/evidence/targeted.xml --basetemp=/tmp/agt-U2-D141ii-review.wmXC6T/basetemp -o cache_dir=/tmp/agt-U2-D141ii-review.wmXC6T/pytest-cache [22 exact selectors]`

Result: **22 passed in 11.94s**, 0 failed/errors/skips.

The prior review's seven distinct neighboring controls were read from its XML. The union was run as 29 exact Python-list selectors (the 22 return selectors plus those seven controls; the missing accepted-head neighbor was separately confirmed once before the final union). Result: **29 passed in 11.53s**, 0 failed/errors/skips. `targeted.xml` is the final 29-node union report.

## Static validation

- `/home/user/work/venv-agent/bin/ruff check` on all eight changed Python paths: **PASS** (`All checks passed!`).
- Private-output compilation of all eight changed Python paths with `/home/user/work/venv-agent/bin/python` and `py_compile.compile(..., cfile=private path, doraise=True)`: **PASS**, 8 files.
- `git diff --check`: **PASS**.
- Outside-allowed blob check against original base: **PASS**, no outside path.
- Exact required mypy: **FAIL_ENVIRONMENT**. `/home/user/work/venv-agent/bin/mypy --follow-imports=silent --ignore-missing-imports astrid/packs/timeline/cli_native.py` stops at NumPy `__init__.pyi:737` because the configured Python 3.11 target rejects the Python 3.12 `type` statement. Interpreter is Python 3.13.16; mypy is 1.17.0.
- Narrow valid target-only baseline: **PASS** with the same command plus `--python-version 3.12`, `Success: no issues found in 1 source file`. This does not replace the exact-command result and no shared dependency/config was changed.

## Scope/non-claims

No full/core/browser/install/render/child-body suite was run. No source, test, generated file, branch, hub, or Git-internal repair was made. The return tree is clean after validation except for the harness-managed evidence outside the worktree.
