<!-- main | 2026-10-22T22:31:55Z | dispatcher heartbeat 1s | live 2 (sol 0, luna 2, other 0) | busy30 5 | status age 7m -->
# runtime board, 2026-10-22T22:20Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| C0 | commit-v2 contract | Sol author / Luna review | — | merged | rt-C0-contract; rt-C0-review | PASS: 34 targeted tests + JSON/digests/copy equality on tree identical to integrated 0d4c71a3c; C0 APPROVED | 0d4c71a3c |
| C0b | per-step reads/provider effects amendment | Sol author / Luna review | orchestrator request 22:15Z | review | rt-C0b-undo-contract; rt-C0b-review | Author: 34 tests PASS, 19 JSON examples/digests/schema/transitions/copy equality PASS; independent review queued; not approved, R2 gated | 756eeb3d2 (branch) |
| U1 | merge upstream, schema v32 | Luna | resolve permission refusal + review findings | blocked:orchestrator | rt-U1-upstream-merge; rt-U1-review-v2 STOPPED | FAIL recovered on review branch: actual upstream-v31 provenance, merge/rerere evidence, +1 typecheck delta; 206 pass/5 socket permission failures/7 deselected; no merge | 85b13f3b4 (branch) |
| R2r | store label/steps/patches, attribution | Luna | C0 approved, U1 merged | todo | — | Brief ready; U1 unmerged after review refusal | — |
| P5 | original gate 2–4 acceptance | Luna | R1, R2 merged for implementation | todo | rt-P5-cases; rt-P5-cases-review-v2 | Collection review PASS; concrete map in reviewer report. No implementation/proof credit | — |
| R5 | refuse old save routes | Luna | A3, G4 merged per header | todo | — | — | — |
Blockers: orchestrator — U1 review permission refusal (localhost socket creation, Errno 1); stopped, no alternate route or rerun. See escalations/runtime-20261022T2216Z-u1-permission-refusal.md, updated with recovered FAIL and stale upstream schema-30 ref evidence. U1/R2r held.
Blockers: orchestrator — C0b READY FOR ASTRA REVIEW on 756eeb3d2; independent Luna review queued. See escalations/runtime-20261022T2224Z-c0b-ready.md, including author internal:<timeline_id> ambiguity question. R2 waits for C0b approval.
Blockers: runtime — disk 9.9 GB vs 15 GB target; 30 additional clean unused abandoned v1 pin worktrees recycled after authorized KEEP release; sweep zero, compact zero; no cleanup denial. Luna rt-U1-v1-cleanup active on eligible v1 scratch/archives and explicitly authorized obsolete suite definitions.
Next ready: C0b merge after review PASS, Astra/orchestrator approval still required; R2r after U1 reviewed PASS/merge and refusal resolved; P5 after R1/R2; R5 after A3/G4 header confirmation.
