<!-- app | 2026-10-22T22:44:41Z | dispatcher heartbeat 8s | live 1 (sol 0, luna 1, other 0) | busy30 5 | status age 0m -->
# app board, 2026-10-22T22:44:29Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3a | Upstream deletions, docs/config/supabase | Luna high | — | blocked:orchestrator | app-U3a-upstream-deletions; app-U3a-review-r1 | No review PASS; stop requested after automatic command safety rejection | — |
| U3b | Upstream editor; retain outbox/transport/client | Luna high | — | doing | app-U3b-recover-r1 | Recovering original interrupted source; targeted/static checks underway | — |
| U3c | QUICK harness plus retained command journeys | Luna high | — | review | app-U3c-upstream-quick-harness; app-U3c-review-r1 | Discovery 5 and lint passed; independent final verdict pending | — |
| U3 | True current upstream merge and Agent re-vendor | Luna high | U3a/U3b/U3c; merged Agent U2 | todo | — | Integration c85da542; verified live upstream 7c17cc9d9 per orchestrator | — |
| U4p | Adopt U1 regenerated client/schema | Luna high | U1, U3 | todo | — | Await U1 tuple | — |
| A2 | Save funnel and dependent local-document chain | Sol high | C0 APPROVED, U3b merged | todo | — | Brief prepared; do not dispatch before U3b merge | — |
| A3 | Popup/placement/element/registerAsset via A2 | Luna high | A2 | todo | — | — | — |
| A4 | Delete executor/capture ports/adapter/goldens | Luna high | A2, A3, H3 go | todo | — | No deletion before H3 go/no-go | — |
Blockers: Orchestrator/safety: automatic command review rejected the U3a review scratch-export/cleanup command as "rm -f style commands are not permitted". Stop requested; this round stops under the owner rule, with no retry or workaround. Escalation app-20261022T2244-review-safety-refusal.md.
Blockers: U3b: original worker died in restart with uncommitted edits; merge-forward stopped because those changes would be overwritten. app-U3b-recover-r1 preserves them in its own worktree before a true upstream merge.
Blockers: Agent/U2: re-vendor needs reviewed merged Agent source. Runtime/U1: U4p needs official regenerated tuple.
Blockers: Farm: qualify composed U3 baseline and integrated H3/P1 chain, then scheduled heavy tour/gate-5/full runs; no local duplicates.
Next ready: Await existing U3b recovery and U3c review results. U3a review stopped for safety disposition. After reviewed U3b merges, dispatch Sol A2 immediately using briefs/A2-save-funnel.md. Then A3; U4p once U1/U3 merged.
