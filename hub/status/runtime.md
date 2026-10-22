<!-- main | 2026-10-22T22:14:31Z | dispatcher heartbeat 12s | live 2 (sol 1, luna 1, other 0) | busy30 7 | status age 0m -->
# runtime board, 2026-10-22T22:14Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| C0 | commit-v2 contract | Sol author / Luna review | — | merged | rt-C0-contract; rt-C0-review | PASS: 34 targeted tests + JSON/digests/copy equality on c1552f3a tree, identical to integrated 0d4c71a3c; C0 APPROVED | 0d4c71a3c |
| C0b | per-step reads/provider effects amendment | Sol | orchestrator request 22:15Z | doing | rt-C0b-undo-contract | Await author, Luna review and Astra re-review; R2 remains gated | — |
| U1 | merge upstream, schema v32 | Luna | — | review | rt-U1-upstream-merge; rt-U1-review-v2 | Author: 131 passed / 8 deselected, TS build + generator checks pass; independent targeted/static/baseline comparison running | 85b13f3b4 (branch) |
| R2r | store label/steps/patches, attribution | Luna | C0 approved, U1 merged | todo | — | Brief ready; launch immediately after U1 review PASS + merge | — |
| P5 | original gate 2–4 acceptance | Luna | R1, R2 merged for implementation | todo | rt-P5-cases; rt-P5-cases-review-v2 | Collection review PASS; concrete map retained in reviewer report. No implementation/proof credit | — |
| R5 | refuse old save routes | Luna | A3, G4 merged per header | todo | — | — | — |
Blockers: orchestrator — C0b author active for requested contract correctness fixes; notify for Astra re-review when ready. R2 waits for C0b per BOARD-HEADER.
Blockers: runtime — disk 8.3 GB vs required 15 GB. Sweep/compact complete, four unprotected finished v1 worktrees recycled, 73 stale unprotected v1 archives removed (1.20 GB); other remaining worktrees protected or dirty, no refusal bypassed.
Next ready: R2r after U1 PASS/merge (C0 approved); P5 implementation after R1 + R2; R5 after A3 + G4 header confirmation.
