Implemented the R-smoke release guard.

- Updated [README.md](/home/user/work/wt/rt-R-release-smoke-0622/README.md) with the exact invocation.
- Updated [scripts/check-before-push](/home/user/work/wt/rt-R-release-smoke-0622/scripts/check-before-push) with fail-closed checkout/provider-origin, selection, skip, timeout, and result checks.
- Added focused CLI controls in [tests/test_release_native_smoke.py](/home/user/work/wt/rt-R-release-smoke-0622/tests/test_release_native_smoke.py).

Validation:

- Genuine Agent-provider D101 smoke: **2 passed**
- CLI guard test: **1 passed**
- `bash -n`: pass
- Ruff and mypy: pass
- In-memory compile and `git diff --check`: pass
- Full/default prepush suite: not run, per task instruction

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-release-smoke-0622/evidence`

Commit message and `DONE` marker created. Independent review remains the next step.