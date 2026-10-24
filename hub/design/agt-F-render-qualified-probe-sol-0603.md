Added [the diagnostic harness](/home/user/work/wt/agt-F-render-qualified-probe-sol-0603/tools/run-render-qualified-probe-0603.py). **One qualified probe completed; original failure causality remains unproved.**

Preflight passed against installed `3b5c` Agent `ba8f` / Runtime `f320`, the existing fixture, and profile `819acf`. Caller `HOST_EXECUTION_PROFILE` remained intentionally dropped.

The single source-derived transition call returned in **15.839s**:

- Registry loading: **11.497s**, including two discovery scans.
- Transport: **4.334s**.
- Child PID `16`: exit `0`, empty stdout/stderr, 563-byte result containing only the expected transition rejection.

[Evidence and interpretation](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-render-qualified-probe-sol-0603/evidence/analysis.json) include argv, cwd, declared environment, process state, result contents, identities and timings. Harness SHA before execution: `7bc25e863edf6adbf39643de8672b8de3b3a4bb47695bbf6cc5260bb8a3c6302`.

Checks passed:

- `python3 tools/run-render-qualified-probe-0603.py` — exactly one probe, exit `0`.
- `/home/user/work/venv-agent/bin/ruff check --no-cache tools/run-render-qualified-probe-0603.py`
- `/home/user/work/venv-agent/bin/ruff format --check --no-cache tools/run-render-qualified-probe-0603.py`
- In-memory Python syntax compilation.
- `git diff --no-index --check /dev/null tools/run-render-qualified-probe-0603.py`
- `git diff --check`

This call consumed **35.2%** of the original ten-probe global 45s budget. Tracing overhead is uncalibrated; child internal Python stages remain unobserved. The transport’s `600s` allowance is separate from that global watchdog.

Original 0509 failure and wrong-environment 0530 evidence remain unchanged. No product/test changes, Node/browser/render execution, or additional probe occurred. Recommend causal review before any fix. Commit message and `DONE` written.