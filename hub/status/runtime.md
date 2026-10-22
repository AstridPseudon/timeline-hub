<!-- main | 2026-10-22T21:46:57Z | dispatcher heartbeat 1s | live 3 (sol 0, luna 3, other 0) | busy30 4 | status age 0m -->
# runtime board, 2026-10-22T21:46Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| C0 | commit-v2 contract | Sol author / Luna review | orchestrator approval | review | rt-C0-contract; rt-C0-review requested | Worker: 17 JSON blocks/copy parse, digest/fixture checks and diff check pass; review pending; no integrated proof | 58f9f1bd5 (branch) |
| U1 | merge upstream, schema v32 | Luna | — | doing | rt-U1-upstream-merge | — | — |
| R2r | store label/steps/patches, attribution | Luna | C0 approved, U1 merged | todo | — | — | — |
| P5 | original gate 2–4 acceptance | Luna | R1, R2 merged for implementation | doing | rt-P5-cases requested (case collection only) | No execution proof; implementation awaits dependencies | — |
| R5 | refuse old save routes | Luna | A3, G4 merged per header | todo | — | — | — |
Blockers: orchestrator — C0 READY FOR APPROVAL: design/commit-v2.md written at 58f9f1bd5; independent Luna review requested. Nobody builds against it before BOARD-HEADER says C0 APPROVED.
Next ready: none undispatched; R2r after C0 approval + U1 merge; P5 implementation after R1 + R2; R5 after A3 + G4 header confirmation.
