Published the [authority rule](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/selected-param-original-pin-rule.md), portable equal-JSON fixture, and executable replay. Added native record-shape probes without changing existing tests or product code.

Validation: **164 passed, 2 strict xfailed** across five targeted files. Fixture export passed; standalone replay reproduced six record envelopes and both equal canonical documents. Ruff and whitespace checks passed.

The two xfails expose pending provider enforcement: conflicting PARAM pins and missing legacy authority. The rule specifies the minimal internal seam using existing Runtime ports; wiring awaits Runtime review. Live Runtime retry/restart and browser draft preservation remain unverified.

[Detailed report with exact commands, results, decisions, and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-selected-param-original-pin/notes/report.md). Commit message and `DONE` written; no full suite requested.