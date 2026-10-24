# D40 Stage A Harness Review — PASS

- Runner SHA: `3cfefd6a72bec379897b80745c91ecdcfa5358c42d7f59afd826adbc3e5e1630`
- Genuine child: Python 3.13.16, isolated `-I`
- Six synthetic checks passed.
- `original_body_runs: 0`
- Production modules imported: none
- 2,053 product/test Python files unchanged; worktree clean.
- No original test, host launch, subprocess, browser, or full-suite execution.

Evidence: [preflight.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D40-observer-review-0607/evidence/preflight.json)

Commands/results:

```text
ruff check tools/run_d40_installed_observed.py     PASS
compile check                                      PASS
git diff --check / scoped diff                     PASS
Stage A preflight                                  PASS
```

Expected observer failures were visible for durable-write and origin failures while synthetic return values, exceptions, arguments, and object identities remained unchanged. Existing profile hooks were preserved; iterators were not consumed.

Stage B remains unverified by design. The static audit confirms the exact single-test pytest scope and installed isolated-child command, but no production caller/body or host subprocess was run. Manager may use Stage B only after this PASS and independent authorization.

The local `design/commit-v2.md` was absent; I used the specified Runtime fallback at `runtime/contract/commit-v2.md`. No v2 production API acceptance is claimed.

Required commit message and `DONE` marker were written.