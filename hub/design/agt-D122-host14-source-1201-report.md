## D122 report

- Diagnosed retained stderr: registry discovery child failed with `ModuleNotFoundError: runtime_protocol`.
- Fixed source-mode host projection in `astrid/sdk/host_bootstrap.py` to include the already-imported Runtime checkout. Installed mode remains isolated.
- Added regression in `tests/sdk/test_host_bootstrap_environment.py`.
- Original source-identity test unchanged byte-for-byte; SHA256: `08dfa8dcafeb80c347923630864a29d58dea97e257428e204fc316567795161b`.

Tests/checks:

- Environment regression: `4 passed`
- Direct child import probe: passed
- Ruff: passed
- Mypy `--follow-imports=skip`: passed
- Compileall: passed
- `git diff --check`: passed

Blocked: exact host14-original-final rerun was not submitted because available disk was 4,880,781,312 bytes, below the required 5,000,000,000-byte admission floor.

Commit message and `DONE` marker written.