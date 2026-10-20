Fixed generic M2 ingress matching using the existing JSON equality helper. Boolean/number changes now fail before send and preserve the flight; numeric equivalence and default-intent retries remain supported. M1 implementation/tests are unchanged.

- Before fix: **6 regression failures**.
- After fix: **134 + 153 local tests passed**, **4 central ingress tests passed**.
- Ruff, mypy and whitespace checks passed.
- No implementation blockers. M2 remains held pending the orchestrator’s M1 gate.

[Report with exact commands, counterexample and corrected counts](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-ingress-json-identity/notes/report.md). Both commit-message files are written. Recommended next step: review the bounded diff; no merge attempted.