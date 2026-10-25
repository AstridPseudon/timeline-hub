## D122 report

Completed proof-only continuation.

- Exact candidate: `ef4c40e8e9e57aaac85a8483238027251495a8e5`, tree `86fadb597ec3ba6396296f56fc4c5b14b56f87af`.
- Parsed no-body preflight: PASS.
- Authorized service run: `agt-D122-host14-proof-resume-1212-host14-original-final-1025121324-13117`
- Result: **REG14 — 14 failed, 59 deselected**.
- Root cause for all 14: child `ModuleNotFoundError: No module named 'runtime_protocol'` during `registry_discovery`; custody/census checks were positive.
- Registered row was migrated for the run, then restored byte-for-byte.
- No product or test files changed. Candidate, Runtime, and Composition worktrees remain clean.
- Evidence: `evidence/host14.xml`, `D122-host14-proof.{md,json}`.
- Completion marker and conventional commit message created.