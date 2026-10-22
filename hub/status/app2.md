<!-- app2 | 2026-10-22T22:40:26Z | dispatcher heartbeat 14s | live 1 (sol 0, luna 1, other 0) | busy30 5 | status age 0m -->
# app2 board, 2026-10-22T22:40:24Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| P1 | H3 real corpus + split/trim/Agent/lost-ack/restart chain | Luna high | C0 APPROVED; R1 + A2 drafts to execute | doing | ap2-P1-agent-cases-fix; App remote merge queued | App independent PASS: 12 tests + tsc/lint. Agent review FAIL: one incorrect trim provenance citation; 13 tests + ruff/mypy PASS, first repair dispatched. Collection only; no integrated H3 proof | Agent c241aecaae (repair pending); App 898476b0e3 (merge requested) |
| P2 | three-products gesture tour | Luna high | A2, A3 merged | blocked:app | — | Not run; heavy tour belongs to farm | — |
| P3 | gate-5 new-path journey | Luna high | A2, R2 merged | blocked:app+agent | — | Not run; heavy journey belongs to farm | — |
| P4 | CLI/Python/sheet, 10-note commit + per-step undo | Luna high | G2, G3, R2 merged for execution | doing | ap2-P4-case-collection | Early real fixture collection dispatched; execution pending G2/G3/R2, no P4 proof | — |
Blockers: app + agent — publish R1/A2 draft hub refs and exact provider/outbox execution seams for immediate P1 integration. C0 APPROVED at 22:15Z; latest App board still claims unapproved and needs correction. Existing cross-lane request: escalations/app2-20261022T2215Z-p1-prerequisites.md.
Blockers: orchestrator — C0b step reads/provider effects still pending; R2-dependent P3/P4 execution awaits C0b/R2, no undo shape assumed.
Blockers: farm — H3 2026-10-23T00:40Z P1 App+Runtime+Agent accepted/merged/refused/lost-ack/restart chain requested; exact command follows reviewed case handoffs and R1/A2 drafts. P1 RESULT: PENDING; no GO evidence yet, A4/G5 remain gated by P1.
Next ready: Agent P1 repair review then merge on PASS; App P1 merge acknowledgement; execute P1 against R1/A2 drafts immediately when available; P2 after A2/A3; P3 after A2/R2; P4 after G2/G3/R2.
