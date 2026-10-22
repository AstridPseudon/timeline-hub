<!-- app | 2026-10-22T23:42:52Z | dispatcher heartbeat 8s | live 2 (sol 0, luna 2, other 0) | busy30 15 | status age 0m -->
# app board, 2026-10-22T23:42:44Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3a | Upstream deletions, docs/config/supabase | Luna high | — | doing | app-U3-live-compose | Sol verified vendor is exact live upstream; composition with U3b must qualify Supabase imports. Other four fixes independently PASS | a66702d9b donor |
| U3b | Upstream editor; retain outbox/transport/client | Luna high | — | review | app-U3b-eof-review | Functional/tsc/lint independently PASS; two EOF blank lines fixed, targeted23/tsc/lint PASS; focused final review active | 369d882ca |
| U3c | QUICK harness plus retained journeys | Luna high | — | merged | app-U3c-quick-adapter-fix | Independent PASS retained; source merged, integrated browser/QUICK proof pending farm (not done) | 1c62edf19 merge / 0ba5378cc source |
| U3 | True live upstream merge and Agent re-vendor | Luna high | U3a/U3b/U3c; merged U2 | doing | app-U3-live-compose | Live GitHub ref verified equal to origin/main; sanctioned merge-forward started, Codex resolves full conflicts and reviewed slice joins | upstream 7c17cc9d9 |
| U4p | Adopt regenerated U1 client/schema | Luna high | U1, U3 | todo | — | Await official U1 tuple and composed U3 | — |
| A2 | Save funnel and dependent local-document chain | Sol high | C0 APPROVED, U3b merged | todo | — | Brief ready; dispatch immediately after reviewed U3b merge | — |
| A3 | Popup/placement/element/registerAsset via A2 | Luna high | A2 | todo | — | — | — |
| A4 | Delete executor/capture ports/adapter/goldens | Luna high | A2, A3, H3 go | todo | — | No deletion before H3 go/no-go | — |
| P1 | Proof lane App chain case collection | Luna high | C0 | merged | ap2-P1-app-chain-cases | Peer PASS: 12 Vitest, tsc/lint; integrated H3 execution awaits farm | 8b979bd21 merge / 898476b0e source |
Upstream: Resolved locally through the connected GitHub read tool. Canonical repository banodoco/astrid-app live refs/heads/main equals local origin/main 7c17cc9d9f9504b578862e2ffd27623fca08a04f. Repeat live check at final merge.
Blockers: Agent/U2 and Runtime/U1: need reviewed merged source and official generated tuple for re-vendor/U4p.
Blockers: Farm: qualify composed U3 baseline and integrated H3/P1 chain with accepted/merged/refused replies; no duplicate local heavy runs.
Next ready: Merge U3b on focused PASS and dispatch A2 immediately. Review complete true-upstream composition; qualify joined types/Supabase and re-vendor when U2 source arrives.
