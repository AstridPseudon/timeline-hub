Implemented atomic `queue_many`/`commit_many` and pinned `edit commands-file` through the existing outbox. Regenerated the CLI surface.

- Neighboring tests: **295 passed, 1 skipped**.
- New Runtime proofs: **34 passed, 2 strict xfailed**.
- Outstanding: frozen provider rejects equal-state ABA contrary to PLAN; current Runtime/client contracts differ.

[Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-native-batch-ingress/notes/report.md)

Both commit-message files are written. M2 integration remains held pending PLAN M1 and orchestrator review of the findings.