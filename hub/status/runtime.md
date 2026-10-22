<!-- main | 2026-10-22T22:09:16Z | dispatcher heartbeat 1s | live 0 (sol 0, luna 0, other 0) | busy30 4 | status age 20m -->
# runtime board, 2026-10-22T21:51Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| C0 | commit-v2 contract | Sol author / Luna review | orchestrator approval | review | rt-C0-contract; rt-C0-review | Author JSON/digest checks pass; independent review has 34 targeted tests passing, final verdict pending; no integrated proof | 58f9f1bd5 (branch) |
| U1 | merge upstream, schema v32 | Luna | — | review | rt-U1-upstream-merge; rt-U1-review queued | Author: 131 passed / 8 deselected, TS build and generator checks pass; broad lint/typecheck baseline non-clean; independent review pending | 85b13f3b4 (branch) |
| R2r | store label/steps/patches, attribution | Luna | C0 approved, U1 merged | todo | — | — | — |
| P5 | original gate 2–4 acceptance | Luna | R1, R2 merged for implementation | review | rt-P5-cases; rt-P5-cases-review queued | Case collection complete; review recovering detailed map from log; implementation awaits R1/R2 | — |
| R5 | refuse old save routes | Luna | A3, G4 merged per header | todo | — | — | — |
Blockers: orchestrator — C0 READY FOR APPROVAL: design/commit-v2.md written at 58f9f1bd5; independent Luna review active. Nobody builds against it before BOARD-HEADER says C0 APPROVED. See escalations/runtime-20261022T2146Z-c0-ready.md.
Next ready: none undispatched; R2r after C0 approval + U1 merge; P5 implementation after R1 + R2; R5 after A3 + G4 header confirmation.
