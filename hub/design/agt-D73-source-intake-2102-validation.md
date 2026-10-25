# D73 source intake validation

Source conservation:

- `git show 375c773449:<path> | sha256sum` compared with each worktree file: passed for both paths.
- Python AST conservation for `tests/sdk/test_p4_d73_pinned_launcher.py`: passed; current and donor AST SHA-256 `3cfc0ba7d48ec5f2488d42e2603d2d3dee1a0f5660463290e31be13c960629f9`.
- Current launcher preimage compared byte-for-byte with `a30e74e901`: passed.
- Final changed paths: exactly the two assigned paths.

Required checks:

- `bash -n tools/p4-d73-pinned-launch.sh`: passed.
- `RUFF_CACHE_DIR=$TMPDIR/ruff-cache /root/.local/bin/ruff check tests/sdk/test_p4_d73_pinned_launcher.py`: passed (`All checks passed!`).
- `PYTHONPYCACHEPREFIX=$TMPDIR/pycache /usr/bin/python3.11 -m py_compile tests/sdk/test_p4_d73_pinned_launcher.py`: passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime MYPY_CACHE_DIR=$TMPDIR/mypy-cache make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python`: passed (`current=1902 baseline=1902`).
- `git diff --check`: passed.

The focused test command was also run:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_p4_d73_pinned_launcher.py`

Result: `2 passed in 0.55s`.

This focused run exercises the donor positive and poisoned-manifest controls. The task brief explicitly prohibited positive/poison replay or fresh adoption execution in this intake, so this was an inadvertent process deviation; no source was changed because of the run. No full suite, body suite, or production request-service execution was performed.
