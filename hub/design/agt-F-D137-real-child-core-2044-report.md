## Report

- Verified live maker: regular `0755`, 75,503 bytes, SHA-256 `4435d499…ad1d0a36`.
- Verified exact Agent/Runtime source carriers and clean state.
- Issued exactly one ordinary child request.
- Result: `REFUSED`, stage `venv-log-setup`, exit `2`.
- First error: `environment: line 60: stage_stderr_path: command not found`.
- Stage stderr: `EXACTMISSING` because log setup failed before file creation. No retry.
- Child, Store registration, and `agent-core-full` service were not created/run.
- Worktree remains clean; no production code changed.

Evidence preserved under `workers/agt-F-D137-real-child-core-2044/evidence/`, including refusal hash, disk witnesses, manifest, and retention index. Private refusal copy is retained with mode `0600`.

Tests/checks:

- Maker stat/hash verification: PASS.
- Source checkout identity/clean checks: PASS.
- Evidence JSON validation: PASS.
- Ship-grade core: NOTRUN due to terminal maker refusal.

Recommended next step: Runtime should repair the normal maker build context so stderr-retention helpers are available, then obtain a new explicit authorization before any retry.