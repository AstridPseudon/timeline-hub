<!-- agent | 2026-10-22T22:16:54Z | dispatcher heartbeat 7s | live 0 (sol 0, luna 0, other 0) | busy30 2 | status age 2m -->
# agent board, 2026-10-22T22:14Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| U2 | upstream merge, rerere, regenerated artifacts | Luna | — | blocked:orchestrator | agt-U2-upstream; agt-U2-review | Author BLOCKED; review queued; unmerged ancestry-only branch MUST NOT LAND | 8a2677cd7 (quarantined branch) |
| U4a | regenerated Runtime client/schema adoption | Luna | U1, U2 | todo | — | — | — |
| R1 | doc.patch semantics and guards | Sol | C0 APPROVED; U2 before merge | blocked:orchestrator | — | — | — |
| R2 | guarded whole/per-step undo, A→B→A | Sol | R1 | todo | — | — | — |
| R3 | dry run and structured errors | Luna | R1 | todo | — | — | — |
| V2 | timing/structure/element/parameter validation | Luna | R1 | todo | — | — | — |
| G2 | open/commit and bounded rerun | Sol | C0 APPROVED; R1, U2 before merge | blocked:orchestrator | — | — | — |
| G3 | document patch emitter and helpers | Luna | G2 | todo | — | — | — |
| G4 | remaining writers through commit | Luna | G2 | todo | — | — | — |
| G5 | delete superseded paths | Luna | G3, G4; H3 go/no-go | todo | — | — | — |
Blockers: orchestrator / agent lead infrastructure — U2 merge-forward denied writing ORIG_HEAD.lock; need approved dispatcher preparation. See escalations/agent-20261022T2214Z-u2-merge-preparation-denied.md. No ancestry-only merge will land.
Blockers: orchestrator — BOARD-HEADER still says C0 NOT YET APPROVED; R1 and G2 dispatch immediately after approval under lane brief's parallel-start permission.
Blockers: runtime — U4a awaits merged U1 and its exact regenerated producer/schema.
Next ready: R1 and G2 on C0 APPROVED; U4a on merged U1 + U2.
