<!-- main | 2026-10-22T21:48:18Z | dispatcher heartbeat 6s | live 1 (sol 0, luna 1, other 0) | busy30 4 | status age 0m -->
# runtime board, 2026-10-22T21:49Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| C0 | commit-v2 contract | Sol author / Luna review | orchestrator approval | review | rt-C0-contract; rt-C0-review | Author JSON/digest checks pass; independent review has 34 targeted tests passing, final verdict pending; no integrated proof | 58f9f1bd5 (branch) |
| U1 | merge upstream, schema v32 | Luna | — | doing | rt-U1-upstream-merge | Worker active on migration/client regeneration; review pending | — |
| R2r | store label/steps/patches, attribution | Luna | C0 approved, U1 merged | todo | — | — | — |
| P5 | original gate 2–4 acceptance | Luna | R1, R2 merged for implementation | doing | rt-P5-cases | Case collection only; no execution proof; implementation awaits dependencies | — |
| R5 | refuse old save routes | Luna | A3, G4 merged per header | todo | — | — | — |
Blockers: orchestrator — C0 READY FOR APPROVAL: design/commit-v2.md written at 58f9f1bd5; independent Luna review active. Nobody builds against it before BOARD-HEADER says C0 APPROVED. See escalations/runtime-20261022T2146Z-c0-ready.md.
Next ready: none undispatched; R2r after C0 approval + U1 merge; P5 implementation after R1 + R2; R5 after A3 + G4 header confirmation.
