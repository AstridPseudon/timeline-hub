<!-- agent | 2026-10-22T22:13:14Z | dispatcher heartbeat 0s | live 1 (sol 0, luna 1, other 0) | busy30 1 | status age 0m -->
# agent board, 2026-10-22T22:13Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| U2 | upstream merge, rerere, regenerated artifacts | Luna | — | doing | agt-U2-upstream | Targeted tests, lint/typecheck and independent review pending | — |
| U4a | regenerated Runtime client/schema adoption | Luna | U1, U2 | todo | — | — | — |
| R1 | doc.patch semantics and guards | Sol | C0 APPROVED; U2 before merge | blocked:orchestrator | — | — | — |
| R2 | guarded whole/per-step undo, A→B→A | Sol | R1 | todo | — | — | — |
| R3 | dry run and structured errors | Luna | R1 | todo | — | — | — |
| V2 | timing/structure/element/parameter validation | Luna | R1 | todo | — | — | — |
| G2 | open/commit and bounded rerun | Sol | C0 APPROVED; R1, U2 before merge | blocked:orchestrator | — | — | — |
| G3 | document patch emitter and helpers | Luna | G2 | todo | — | — | — |
| G4 | remaining writers through commit | Luna | G2 | todo | — | — | — |
| G5 | delete superseded paths | Luna | G3, G4; H3 go/no-go | todo | — | — | — |
Blockers: orchestrator — BOARD-HEADER still says C0 NOT YET APPROVED; R1 and G2 dispatch immediately after approval under lane brief's parallel-start permission.
Blockers: runtime — U4a awaits merged U1 and its exact regenerated producer/schema.
Next ready: R1 and G2 on C0 APPROVED; U4a on merged U1 + U2.
