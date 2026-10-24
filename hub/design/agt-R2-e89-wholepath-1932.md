## Report

- Read-only investigation complete; no source/test edits and no body rerun.
- Retained original invocation finished unchanged: `2 failed, 2 passed in 178.47s`.
  - `False-None`: timeout 45.007s
  - `False-public-element`: timeout 45.007s
  - Both `True` cases passed: 42.886s, 42.950s
- Trace reaches Runtime recursive verification:
  `history_entry → _verify_accepted → _inverse_stage_history → history_entry → historical sequential validation → jsonschema`.
- Authentic PASS controls:
  - R2 whole-restore: `1 passed in 6.87s`, max recursion depth 6, 258 `history_entry` calls.
  - P4 conflict-rerun: PASS in `12.386s`.
  - Strict PARAM controls: `99 passed in 49.74s`.
- Cause: Runtime-owned recursive accepted-history revalidation, not proven to be PARAM authority. Finite-JSON optimization alone cannot be assumed sufficient.
- Exact seam: Runtime `timeline_commit_store.py:202-269`, `442-468`, `864-873`; validation capture at `timeline_commit_auth.py:2243-2267`, `2370-2387`, `2469-2535`.
- Unproven: exact per-original phase counts and schema-vs-digest cost split. Historical profile source predates current Runtime `e89eb8c7…`, so it is control evidence only.
- Recommended next bounded measurement: disabled local counters/timers around `_verify_accepted`, `_inverse_stage_history`, `_historical_sequential`, capture functions, and `validate_commit_value`, keyed by publication, original/landing, command ordinal, and validation definition. Preserve ABI, guards, full validation, publication identity, and ABA/security semantics.

Evidence: [r2-wholepath-investigation.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-e89-wholepath-1932/evidence/r2-wholepath-investigation.md>)

Worktree clean. Commit message and `DONE` marker created.