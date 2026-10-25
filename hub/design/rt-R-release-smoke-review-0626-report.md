PASS — no product/source edits or commit delta.

- Source diff is exactly `README.md`, `scripts/check-before-push`, and `tests/test_release_native_smoke.py`; worktree clean.
- Real smoke passed: Agent origin verified at `/home/user/work/agent/.../commit.py`; provider `astrid-v1`; 2 D101 tests passed.
- Fail-closed checks passed for missing and wrong checkout, pytest failure, zero selection, and skips.
- Targeted pytest, `bash -n`, mypy supplemental, Ruff supplemental, and `git diff --check` passed.
- Exact runtime-venv Ruff/mypy commands were unavailable because those modules are not installed; supplemental `/root/.local/bin` tools passed.
- Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-release-smoke-review-0626/evidence/`

Used documented `PYTHON_BIN` because README specifies it; no default/full prepush, browser, install, or unrelated checks were run.