Confirmed the bug: newly captured seed 16 passes capture, compilation, and native provider acceptance against the unchanged max-10 admitted revision. Seed 8 passes commit/reload/undo/redo with opaque data preserved.

- Tests-only change; product code and existing guard tests untouched.
- Targeted tests: **392 passed, 7 xfailed**.
- New probe with `--runxfail`: **1 passed, 3 expected failures**, all `DID NOT RAISE`.
- Ruff and diff checks passed. No full suite or live Runtime tested.

[Report with exact commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-selected-schema-proof/notes/report.md) · [Source findings and recommended minimal follow-up](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-selected-schema-proof.md)

Both commit messages written. No blockers; product fix remains for orchestrator scoping. Candidate 1 unaffected.