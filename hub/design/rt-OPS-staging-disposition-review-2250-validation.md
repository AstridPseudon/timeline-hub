# Validation — rt-OPS-staging-disposition-review-2250

## Static custody checks

Reviewed first:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`
- original owner brief `rt-OPS-staging-tool-2209`
- `rt-OPS-staging-return-2223`
- independent `rt-OPS-staging-final-review-2235`
- residual Sol `rt-OPS-staging-residual-sol-2239`

Working tree: `/home/user/work/wt/rt-OPS-staging-disposition-review-2250`.

Observed:

- `git status --porcelain=v1` — PASS, clean.
- `git rev-parse HEAD` — `25f311f8567fdb65408f1ae8a8f662649c1e0f57`.
- `git rev-parse HEAD^` — `9524356e2ca603f444eda451a502438ef9110d3b`.
- `git diff --name-only 9524356..HEAD -- ops-drop-staging` —
  `ops-drop-staging/README.md` only.
- `git diff --check 9524356..HEAD -- ops-drop-staging` — PASS.
- `git diff --quiet 9524356..HEAD -- ops-drop-staging/drop_staging.py
  ops-drop-staging/test_drop_staging.py ops-drop-staging/drop-staging` — PASS
  (exit 0; no functional diff).
- `PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY' ... ast.parse(...) ... PY` —
  PASS for `drop_staging.py` and `test_drop_staging.py`.

The exact current/base hashes and modes are in `source-manifest.json`.

## Reused execution evidence

Per task instruction, unchanged tests were not rerun. The residual Sol evidence
records these exact commands and results:

- `PYTHONDONTWRITEBYTECODE=1 python3 ops-drop-staging/test_drop_staging.py` —
  PASS, 14 tests, exit 0.
- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-0ba2342d2c/review2235-reproductions.py`
  — completed the five residual defect observations, exit 0.
- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-0ba2342d2c/residual_cli_controls.py /home/user/work/wt/rt-OPS-staging-residual-sol-2239/ops-drop-staging`
  — 5 tests, 5 failures, exit 1; RED is expected and retained.
- `/home/user/work/venv-agent/bin/ruff check ops-drop-staging/drop_staging.py ops-drop-staging/test_drop_staging.py`
  — PASS in the residual run.
- `/home/user/work/venv-agent/bin/ruff format --check ops-drop-staging/drop_staging.py ops-drop-staging/test_drop_staging.py`
  — PASS in the residual run.
- private `py_compile` of the three candidate files — PASS in the residual run.
- `git diff --check` — PASS in the residual run.

The recorded binaries were Python 3.13.16 (`/usr/bin/python3.13`, SHA-256
`a35753ccb97941cce1467786cce892e608141f09d717188a3235d4f51a754446`) and Ruff
0.12.0 (`/home/user/work/venv-agent/bin/ruff`, SHA-256
`bc4a4145ff8a2caee4ef71e7f50e27b3d48bca60c1aceee8ad0ad6d434b97195`).

No live cleanup, install, acquisition, full suite, provider/body, browser,
child, Store, or D130 action was performed. Synthetic fixtures are not real
worker acceptance.
