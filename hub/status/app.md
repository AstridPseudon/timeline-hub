<!-- app | 2026-10-22T22:39:14Z | dispatcher heartbeat 2s | live 3 (sol 0, luna 3, other 0) | busy30 5 | status age 0m -->
# app board, 2026-10-22T22:39:00Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3a | Upstream deletions, docs/config/supabase | Luna high | — | review | app-U3a-upstream-deletions; app-U3a-review-r1 | 29 targeted passed; 10 collection failures; fresh independent review running | — |
| U3b | Upstream editor; retain outbox/transport/client | Luna high | — | doing | app-U3b-recover-r1 | Interrupted source recovered in a new worker; lint passed historically, no final typecheck/report | — |
| U3c | QUICK harness plus retained command journeys | Luna high | — | review | app-U3c-upstream-quick-harness; app-U3c-review-r1 | Discovery 5/lint/diff passed; fresh behaviour-retention review running | — |
| U3 | True current upstream merge and Agent re-vendor | Luna high | U3a/U3b/U3c; merged Agent U2 | todo | — | Integration c85da542; upstream freshness must be checked before composition | — |
| U4p | Adopt U1 regenerated client/schema | Luna high | U1, U3 | todo | — | Await U1 tuple | — |
| A2 | Save funnel and dependent local-document chain | Sol high | C0 APPROVED, U3b merged | todo | — | C0 approved; pending C0b step reads/effects must remain compatible | — |
| A3 | Popup/placement/element/registerAsset via A2 | Luna high | A2 | todo | — | — | — |
| A4 | Delete executor/capture ports/adapter/goldens | Luna high | A2, A3, H3 go | todo | — | No deletion before H3 go/no-go | — |
Blockers: App lead: verify refreshed origin/main with explicit main refspec and ls-remote. Current local origin/main is 7c17cc9d9, different from both the old 2dca750a slice base and the 22:37 expected 3f4619da4. Do not certify stale upstream composition.
Blockers: App U3b: manager merge-forward on the interrupted dirty source stopped because local/untracked changes would be overwritten; no merge started. Recovery worker preserves that source before the sanctioned merge route resumes.
Blockers: Agent/U2: U3 vendor regeneration needs the reviewed merged Agent source. Runtime/U1: U4p needs the regenerated official tuple.
Blockers: Farm: qualify composed U3 baseline, then run P1 chain/H3, gesture tour and gate-5 on integrated heads; no local duplicate heavy runs.
Next ready: Three U3 recovery/review workers are running. Review recovered U3b immediately; merge current upstream through workers, then start Sol A2 as soon as U3b is merged. U4p follows official U1 tuple.
