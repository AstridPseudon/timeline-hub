## Report

- Ran the exact authorized 15 D52 nodes with the documented `venv-agent`, Runtime `becfe6db88`, Node `v20.19.4`, and profile `agent-remotion-v3-819acf-1110`.
- Result: **15 failed**, exit code **1**, in **133.04s**.
- All failures stopped before the test bodies at `registry_discovery`:
  - `original_wait_exit_code=1`
  - `census_complete=true`
  - `custody_admitted=true`
  - child stderr: `ModuleNotFoundError: No module named 'runtime_protocol'`
- Classified as the existing local installed-profile/registry-probe environment gap; bootstrap identity assertions were not reached.

Evidence:

- [local15.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D52-bootstrap-local-1156/evidence/local15.xml)
- XML SHA-256: `3c6dd12b277c553ece06acb8cf6ad0bc5697279f6e920fe6396cd7ba3db9f110`
- 15 natural child-stderr files were retained; each had the same missing-`runtime_protocol` traceback.

Preflight passed:

- Corrected profile archive: `819acf…40234`
- Old `255b` archive: `21fde…893e6e`
- Runtime path and source imports matched the documented current row.
- Test AST matched full9758 exactly.
- Worktree, source, fixtures, and registry remained unchanged.
- `git diff --check` passed.
- No full suite, child environment request, install, source acquisition, or rerun was performed.

The production caller and bootstrap identity behavior remain unverified because the probe failed before reaching them. DONE marker and commit message were prepared.