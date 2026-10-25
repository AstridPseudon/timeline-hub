# R-smoke qualification report

- Runtime HEAD: `c91626f5e905f9336b51aae0486a071d83f0bac7` (clean; home unchanged).
- Agent HEAD: `5554fe792bba5ed17c90e0a1ccf46f4d5df19601` (clean).
- Agent provider origin: `/home/user/work/agent/astrid/sdk/timeline/commit.py`; provider identity `astrid-v1`.
- Exact authored paths verified: `README.md`, `scripts/check-before-push`, `tests/test_release_native_smoke.py`.

Results:

- Native provider smoke: exit 0; exactly 2 selected tests, `2 passed in 2.58s`, no skips/deselections.
- Release smoke test: exit 0; `1 passed`.
- `bash -n scripts/check-before-push`: exit 0.
- Ruff: exit 0.
- Mypy: exit 0.
- In-memory compile and `git diff --check`: both exit 0.
- Worktree unchanged; no source changes made.
- No full/default pre-push suite or package installation run.

Evidence is under 48 KB in [evidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-release-smoke-home-0630/evidence>). `DONE` and commit message were created.