Implemented AG03 partial compatibility cut in [cli.py](/home/user/work/wt/agt-m2-sheet-cut-preserve-grammar/astrid/packs/timeline/cli.py:3587):

- Connected/default Runtime callers remain bound `NativeSheet`.
- No-client Main callers retain legacy sheet grammar and local save behavior.
- AG03 ledger updated with exact remaining debt and 46 diagnostic failures.

Tests:

- Grammar/self-tests: 176 passed.
- Native focused tests: 104 passed.
- Central HTTP lane blocked by Runtime/Agent schema digest mismatch; no pass claimed.
- No full suite run.

Report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-sheet-cut-preserve-grammar/report.md)