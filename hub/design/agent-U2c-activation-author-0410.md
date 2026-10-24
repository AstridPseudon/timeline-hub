Implemented the U2c abort fix; **acceptance remains BLOCKED and the branch remains HELD**.

- `abort()` verifies parked identity before cleanup or signaling, preserves the primary exception, and accepts the child-exit race only with an integer `wait()` result.
- Removed exactly two obsolete fixture keywords. All existing assertions and activation predicates remain unchanged.
- Added focused tests for missing/invalid wait proof and native identity-observation failure. The upstream port remains otherwise unchanged.

Validation:

| Check | Result |
|---|---|
| Four original abort controls | **OLD: 4 failed → CURRENT: 4 passed** |
| Abort controls plus new focused tests | **14 passed, 11 deselected** |
| Prescribed activation/source-identity command | **10 failed, 77 passed** |
| Scoped Ruff versus exact parent | 3 → 3 diagnostics; **zero new** |
| Private-cache mypy versus exact parent | 0 → 0 diagnostics |
| Vendor lock, artifact manifest, `git diff --check` | Passed |

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2c-activation-sol-0410/evidence/commands.txt) · [Ruff/mypy commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2c-activation-sol-0410/evidence/quality-commands.log)

The acceptance failures require orchestrator triage: eight activations encounter Runtime’s required `child` proof absent from the existing inspector projection; one identity test receives a different refusal message; local control raises `BrokenPipeError` on a path requiring Darwin audit-token custody on Linux. I left provider code and predicates unchanged.

Wrote the U2c commit message and `BLOCKED` marker. Recommend resolving those acceptance blockers before independent review and freeze. No home merge or readiness-causality claim.