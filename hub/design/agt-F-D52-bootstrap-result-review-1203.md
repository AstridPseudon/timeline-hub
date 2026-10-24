## D52 bootstrap result review: PASS

Qualified the recorded actual15 failed-result package.

- Exact 15 JSON selectors match JUnit XML after normalizing dotted classnames; 15 failures, 0 errors/skips, no extras/omissions.
- XML SHA-256: `3c6dd12b…db9f110`.
- All 15 natural stderr files were retained: distinct paths, 738 bytes each, identical hash `ddc33f…e9e8`; first import was `runtime_protocol`, failing with `ModuleNotFoundError`.
- Environment matched venv-agent, Runtime `becfe6db88`, Node `v20.19.4`, and profile archive `819acf…40234`; stale profile was `21fde…893e6e`.
- Current test AST matches full9758 exactly. Full9758 historical results and the original 267-record count remain preserved.
- Failures occurred during `registry_discovery` before identity assertions. This does not claim all test-body setup was unrun.
- Live production callers are confirmed through `autobootstrap.py:496–502` and `services.py:81–90 → host_bootstrap.py:1815–1818`.
- No additional overlay, install, acquisition, child environment, credentials, source mutation, or causal repair was inferred. The source-import-whole-path task remains separate.

Recorded run: exact pytest qualification command, exit 1, 15 failed in 133.04s. No repeat test or full suite was run. Worktree is clean; `git diff --check` passes.

Evidence: [local15.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D52-bootstrap-local-1156/evidence/local15.xml).