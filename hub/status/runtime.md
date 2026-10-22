<!-- main | 2026-10-22T22:18:36Z | dispatcher heartbeat 1s | live 1 (sol 1, luna 0, other 0) | busy30 4 | status age 2m -->
# runtime board, 2026-10-22T22:16Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| C0 | commit-v2 contract | Sol author / Luna review | — | merged | rt-C0-contract; rt-C0-review | PASS: 34 targeted tests + JSON/digests/copy equality on c1552f3a tree, identical to integrated 0d4c71a3c; C0 APPROVED | 0d4c71a3c |
| C0b | per-step reads/provider effects amendment | Sol | orchestrator request 22:15Z | doing | rt-C0b-undo-contract | Await author, Luna review and Astra re-review; R2 remains gated | — |
| U1 | merge upstream, schema v32 | Luna | resolve permission refusal + review findings | blocked:orchestrator | rt-U1-upstream-merge; rt-U1-review-v2 stop requested | Review: 206 pass, 5 PermissionError failures, 7 deselected; baseline same; actual upstream-v31 fixture gap and rerere evidence unresolved. No PASS, no merge | 85b13f3b4 (branch) |
| R2r | store label/steps/patches, attribution | Luna | C0 approved, U1 merged | todo | — | Brief ready; U1 unmerged after review refusal | — |
| P5 | original gate 2–4 acceptance | Luna | R1, R2 merged for implementation | todo | rt-P5-cases; rt-P5-cases-review-v2 | Collection review PASS; concrete map in reviewer report. No implementation/proof credit | — |
| R5 | refuse old save routes | Luna | A3, G4 merged per header | todo | — | — | — |
Blockers: orchestrator — U1 review permission refusal (localhost socket creation, Errno 1); affected review stop requested, no alternative route used. See escalations/runtime-20261022T2216Z-u1-permission-refusal.md. Review also found actual upstream-v31 fixture and rerere evidence gaps. U1/R2r held.
Blockers: orchestrator — C0b author active for requested contract fixes; request Astra re-review when ready. R2 waits for C0b per header.
Blockers: runtime — disk 8.3 GB vs required 15 GB; sweep/compact complete, four unprotected finished v1 worktrees recycled, 73 stale unprotected archives removed (1.20 GB); remaining worktrees protected or dirty.
Next ready: no ungated implementation; R2r after U1 reviewed PASS/merge and refusal resolved; P5 after R1/R2; R5 after A3/G4 header confirmation.
