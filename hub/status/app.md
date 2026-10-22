<!-- app | 2026-10-22T23:52:48Z | dispatcher heartbeat 10s | live 2 (sol 1, luna 1, other 0) | busy30 13 | status age 4m -->
# app board, 2026-10-22T23:48:16Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3a | Upstream deletions, docs/config/supabase | Luna high | — | doing | app-U3-live-compose | Sol verified vendor is exact live upstream; composition with U3b must qualify Supabase imports. Other four fixes independently PASS | a66702d9b donor |
| U3b | Upstream editor; retain outbox/transport/client | Luna high | — | merged | app-U3b-eof-fix | Independent PASS: target23, tsc/lint/diff-check. Integrated overall proof pending composition/farm | f9d5d0cdd merge / 369d882ca source |
| U3c | QUICK harness plus retained journeys | Luna high | — | merged | app-U3c-quick-adapter-fix | Independent PASS retained; source merged, integrated browser/QUICK proof pending farm (not done) | 1c62edf19 merge / 0ba5378cc source |
| U3 | True live upstream merge and Agent re-vendor | Luna high | U3a/U3b/U3c; merged U2 | doing | app-U3-live-compose | Live GitHub ref verified equal to origin/main; sanctioned merge-forward started, Codex resolves full conflicts and reviewed slice joins | upstream 7c17cc9d9 |
| U4p | Adopt regenerated U1 client/schema | Luna high | U1, U3 | todo | — | U1 merged27f0306b9; exact producer checkout requested. Await composed U3 | — |
| A2 | Save funnel and dependent local-document chain | Sol high | C0 APPROVED, U3b merged | doing | app-A2-save-funnel | Sol high HARD dispatched immediately on merged U3b base f9d5d0cdd; no executor/fallback/overwrite | — |
| A3 | Popup/placement/element/registerAsset via A2 | Luna high | A2 | todo | — | — | — |
| A4 | Delete executor/capture ports/adapter/goldens | Luna high | A2, A3, H3 go | todo | — | No deletion before H3 go/no-go | — |
| P1 | Proof lane App chain case collection | Luna high | C0 | merged | ap2-P1-app-chain-cases | Peer PASS: 12 Vitest, tsc/lint; integrated H3 execution awaits farm | 8b979bd21 merge / 898476b0e source |
Upstream: Resolved locally through the connected GitHub read tool. Canonical repository banodoco/astrid-app live refs/heads/main equals local origin/main 7c17cc9d9f9504b578862e2ffd27623fca08a04f. Repeat live check at final merge.
Sources: U2 merged3f1ceaed1, exact Agent checkout queued for re-vendor. U1 merged27f0306b9, clean exact producer ready at /home/user/work/wt/rt-pin-27f0306b. U4p/re-vendor follow composed U3 source.
Blockers: Runtime/generated v2 join: A2 current pinned DTOs omit steps/merge/reads/doc.patch and merged/invalid. Official generation/adoption is required; A2 continues local durable-chain implementation. Escalation app-20261022T2350-a2-generated-v2-join.md.
Blockers: Farm: qualify composed U3 baseline and integrated H3/P1 chain with accepted/merged/refused replies; no duplicate local heavy runs.
Next ready: Review first A2 funnel slice on completion; dispatch A3 as soon as A2 merges. Review true-upstream composition, then U4p/re-vendor when official U1/U2 handoffs arrive. A4 stays behind real H3 GO.
Disk: 17GB free. Resumed overlapping manager ended after independent cleanup: 14 finished v1 source/pin trees recycled with branches/reports retained, current worktrees/shared dependencies untouched. Manager also recycled the two finished v1 App trees; sweep/compact found no eligible scratch.
