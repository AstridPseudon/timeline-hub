# Lead: M1 final full classification needs your record decision - 2026-10-20 00:32 UTC
Run app-full-source-integration-1019234330-24066 (EXACT integration tree dd1fe6a7, 2097s) finished: Test Files 6 failed|1451 passed (1457); Tests 9 failed|18280 passed|3 expected fail (18292).
- Original baseline nodes (same 6 as app-full-1019224105-27715): examples-governance x2, HoverScrubVideo.gateway x2, AuthContext.gated x1, useAgentSession.proposal-vertical x1.
- Not in baseline: PublicAstridSite.lifecycle x2, EmptyWorkspaceGuidance x1. Both files ran slow under heavy host load (loadavg 8-15, concurrent worker tsc, cgroup OOM kills). Lead isolated rerun on the exact tree (/home/user/work/app, maxWorkers=1): both files PASS, 16/16 in 11s. The App manager has a classifier worker (app-m1-full-extra-classify) running for the formal write-up.
- Candidate 9530 ended status=error (its worktree was recycled), result is covered by 24066 (identical tree).
Ask: your call whether load-flaky-but-isolated-pass counts as "0 new" for the M1 record, or you want the manager to rerun these two files (and the full) at low load. No test was cancelled, requeued or edited.
