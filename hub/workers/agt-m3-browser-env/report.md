## Done

- Added `ASTRID_REMOTION_BROWSER_EXECUTABLE` to the parent-owned child environment allowlist.
- Added regression coverage for parent precedence and dropping unrelated variables.
- Wrote commit message to the requested `commit-msg.txt`.

## Tests

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/core/test_subprocess_env.py` — **2 passed**
- `git diff --check` — **passed**
- Ruff reports only inherited diagnostics; no unrelated reformatting applied.

No blockers. Recommended next step: harness commit and rerun the viewing CPU export qualification.