# Fcore rehearsal report

- Refreshed exact scope: 9,263 nodes / 408 files, including all 3 original P4 nodes, D13 environment node, and both D23 deferred nodes.
- Central service: corrected ID `agent-OWN-REHEARSAL-SUITE-1024224113-23499`
- Result: `8,713 passed, 308 failed, 242 errors, 86 warnings, 173 subtests`; exit 1 after 1,256.11s.
- Known P4 ten-note failure: 1. D13 environment: 1. D23 deferred: 1. Remaining bad nodes: 547 uncertain; no regression/pre-existing/dead-scope claims fabricated.
- Initial service attempt was zero-body launcher failure (`cp` manifest onto itself). Corrected by moving the service manifest outside evidence; no test body was repeated.

Checks:

- Collection: passed.
- `bash -n`, Python AST/compile, `git diff --check`: passed.
- Positive stub: exactly once, exit 17.
- Poisoned SHA: rejected, zero stub calls.
- Ruff and mypy: existing helper diagnostics remain (I001 and tuple typing error).
- Evidence: [evidence directory](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-core-rehearsal-2234/evidence) — 43 MB.
- Only rehearsal candidate/helper files changed; no product or test bodies changed.
- No D59 gate credit earned; final gate run remains owed.

Commit message and `DONE` marker were created.