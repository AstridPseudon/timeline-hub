<!-- app | 2026-10-22T23:37:57Z | dispatcher heartbeat 2s | live 2 (sol 1, luna 1, other 0) | busy30 12 | status age 0m -->
# app board, 2026-10-22T23:37:18Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3a | Upstream deletions, docs/config/supabase | Luna high | — | doing | app-U3a-vendor-closure | Second review FAIL only dependency closure; Sol HARD split fixes incomplete package. Other four fixes PASS | a66702d9b source |
| U3b | Upstream editor; retain outbox/transport/client | Luna high | — | review | app-U3b-repair-review-r1 | Repair author: tsc/lint PASS, required122 + provider173 + canary59 PASS; one inherited host assertion under independent attribution | 69099d6db |
| U3c | QUICK harness plus retained journeys | Luna high | — | merged | app-U3c-quick-adapter-fix | Independent PASS retained; source merged, integrated browser/QUICK proof pending farm (not done) | 1c62edf19 merge / 0ba5378cc source |
| U3 | True live upstream merge and Agent re-vendor | Luna high | U3a/U3b/U3c; merged U2 | todo | — | GitHub live ref verified equal to local origin/main 7c17cc9d9; repeat before final composition | — |
| U4p | Adopt regenerated U1 client/schema | Luna high | U1, U3 | todo | — | Await official U1 tuple and composed U3 | — |
| A2 | Save funnel and dependent local-document chain | Sol high | C0 APPROVED, U3b merged | todo | — | Brief ready; dispatch immediately after reviewed U3b merge | — |
| A3 | Popup/placement/element/registerAsset via A2 | Luna high | A2 | todo | — | — | — |
| A4 | Delete executor/capture ports/adapter/goldens | Luna high | A2, A3, H3 go | todo | — | No deletion before H3 go/no-go | — |
| P1 | Proof lane App chain case collection | Luna high | C0 | merged | ap2-P1-app-chain-cases | Peer PASS: 12 Vitest, tsc/lint; integrated H3 execution awaits farm | 8b979bd21 merge / 898476b0e source |
Upstream: Resolved locally through the connected GitHub read tool. Canonical repository banodoco/astrid-app live refs/heads/main equals local origin/main 7c17cc9d9f9504b578862e2ffd27623fca08a04f. Repeat live check at final merge.
Blockers: Agent/U2 and Runtime/U1: need reviewed merged source and official generated tuple for re-vendor/U4p.
Blockers: Farm: qualify composed U3 baseline and integrated H3/P1 chain with accepted/merged/refused replies; no duplicate local heavy runs.
Next ready: Review U3b on completion; merge reviewed slices; dispatch A2 immediately after U3b merge. Review U3c repair, then compose true upstream merge after freshness check.
