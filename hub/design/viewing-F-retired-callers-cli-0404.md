## PASS — F-retired-callers CLI

- The assigned file already contains the required public-caller migration from `1794f0a2e`; no duplicate diff was needed.
- Retained scenarios use sheet `show` → edit → connected `apply`/`commitTimeline`, preserving golden semantics, preview/lost-ACK idempotency, parent-scoped refusal, and public help.
- Current target: `11 passed`.

Tests/checks:

- With required environment: `11 passed in 1.63s`
- Ruff: passed
- Mypy: passed
- Vendor lock, artifact manifest, `git diff --check`: passed
- Bare acceptance pytest lacked `PYTHONPATH` and failed import of `runtime_protocol`; resolved using `PYTHONPATH="$PWD:/home/user/work/runtime"`.

Actual origins confirmed:

- Agent CLI/SDK: this worktree’s `astrid/packs/timeline/{cli.py,cli_native.py}` and `astrid/sdk/timeline_{sheet,sync}.py`
- Runtime: `/home/user/work/runtime/runtime_protocol/timeline_commit_{store,execution}.py`

Historical evidence reused: `1794f0a2e`, prior qualified `19646f...`, and `agent-F-five-integrated-2340`; these were not treated as current-head proof.

No product files changed. `DONE` and commit message were written.