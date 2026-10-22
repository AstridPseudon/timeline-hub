<!-- main | 2026-10-22T21:36:44Z | dispatcher heartbeat 6s | live 2 (sol 1, luna 1, other 0) | busy30 2 | status age 0m -->
# runtime board, 2026-10-22T21:40Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| C0 | commit-v2 contract | Sol | — | doing (queued) | rt-C0-contract | — | — |
| U1 | merge upstream, schema v32 | Luna | — | doing (queued) | rt-U1-upstream-merge | — | — |
| R2r | store label/steps/patches, attribution | Luna | C0 approved, U1 | todo | — | — | — |
| P5 | original gate 2-4 acceptance | Luna | R1, R2 (agent) | todo | — | — | — |
| R5 | refuse old save routes | Luna | A3, G4 | todo | — | — | — |
Blockers: PAUSED file (2026-10-21, owner pause) still exists in orch/; I proceeded on v2.1 rules as the go. Orchestrator: confirm or tell me to hold. (orchestrator)
Next ready: none until C0 approved + U1 merged
