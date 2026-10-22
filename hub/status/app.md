<!-- app | 2026-10-22T23:17:36Z | dispatcher heartbeat 14s | live 3 (sol 0, luna 3, other 0) | busy30 3 | status age 5m -->
# app board, 2026-10-22T23:14:00Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3a | Upstream deletions, docs/config/supabase | Luna high | — | review | app-U3a-review-r2 | Fresh authorized review queued; prior denied scratch command remains prohibited | 7192c0127 source |
| U3b | Upstream editor; retain outbox/transport/client | Luna high | — | doing | app-U3b-recover-r2 | Recovery queued; both interrupted dirty donor trees retained read-only | — |
| U3c | QUICK harness plus retained journeys | Luna high | — | doing | app-U3c-repair-r1 | First review FAIL: missing QUICK, six dropped journeys, eight zero-discovery configs; first Luna return queued | 1a036a917 source |
| U3 | True live upstream merge and Agent re-vendor | Luna high | U3a/U3b/U3c; merged U2 | todo | — | Local origin/main 7c17cc9d9; live verification awaits normal Git access | — |
| U4p | Adopt regenerated U1 client/schema | Luna high | U1, U3 | todo | — | Await official U1 tuple and composed U3 | — |
| A2 | Save funnel and dependent local-document chain | Sol high | C0 APPROVED, U3b merged | todo | — | Brief ready; dispatch immediately after reviewed U3b merge | — |
| A3 | Popup/placement/element/registerAsset via A2 | Luna high | A2 | todo | — | — | — |
| A4 | Delete executor/capture ports/adapter/goldens | Luna high | A2, A3, H3 go | todo | — | No deletion before H3 go/no-go | — |
| P1 | Proof lane App chain case collection | Luna high | C0 | merged | ap2-P1-app-chain-cases | Peer PASS: 12 Vitest, tsc/lint; integrated H3 execution awaits farm | 8b979bd21 merge / 898476b0e source |
Blockers: Lead/upstream: Git ls-remote cannot reach configured 127.0.0.1:39063 proxy. Restore normal access, fetch explicit main refspec and verify live tip before U3 composition. Local origin/main is 7c17cc9d9.
Blockers: Agent/U2 and Runtime/U1: need reviewed merged source and official generated tuple for re-vendor/U4p.
Blockers: Farm: qualify composed U3 baseline and integrated H3/P1 chain with accepted/merged/refused replies; no duplicate local heavy runs.
Next ready: Review U3b on completion; merge reviewed slices; dispatch A2 immediately after U3b merge. Review U3c repair, then compose true upstream merge after freshness check.
