## Report

- Updated only `scripts/reshape/baselines/ruff_astrid.json`: Ruff `2145 → 2143`.
- No mypy baseline change; no source/test/config changes.
- Parent/current normalized Ruff comparison: `0 removed`, `0 added`; baseline metadata was stale.
- Protected `astrid/` and `tests/` remain identical to `4f6c85ddc6`.

Checks:

- `make ruff PY=/home/user/work/venv-agent/bin/python` — PASS, 2143/2143.
- Qualified mypy command — PASS, 1902/1902.
- Ruff generator idempotence — PASS.
- JSON validation — PASS.
- `git diff --check` — PASS.

Commit message written: `chore(timeline): tighten R1 Ruff baseline`. No targeted/full/browser tests run per brief.