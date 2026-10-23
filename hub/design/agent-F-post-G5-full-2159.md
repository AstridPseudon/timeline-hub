## Report

- Added one `agent full-post-g5-2159` harness row, preserving existing rows.
- Added hash-locked launcher and report-all preflight; no product/test/pin changes. Agent worktree remains clean at c36ca8c9/tree50689a4.
- Service ID: `agent-full-post-g5-2159-1023220134-17203`
- Command: `request-test integration:agent full-post-g5-2159`
- Result: `fail`, exit `1`; preflight stopped before the full body.

Preflight: 3 checks passed, xdist probe `6 passed`; 4 harness false negatives:

1. Runtime/profile/schema directory checks incorrectly used file validation.
2. Frozen producer-version literal contained a typo.

No full-suite nodes executed; no regression classification is possible. No retry was submitted per the one-request rule.

Evidence retained under 50 MB: [service-log.txt.gz](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-post-G5-full-2159/service-log.txt.gz>) and manifest. Recommended next step: repair the harness preflight and obtain explicit authorization for a continuation run.