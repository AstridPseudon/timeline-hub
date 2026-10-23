<!-- app | 2026-10-23T00:02:45Z | dispatcher heartbeat 4s | live 1 (sol 0, luna 1, other 0) | busy30 9 | status age 1m -->
# app board, 2026-10-23T00:01:49Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U3a | Upstream deletions, docs/config/supabase | Luna high | — | doing | app-U3-live-compose | Sol verified vendor is exact live upstream; composition with U3b must qualify Supabase imports. Other four fixes independently PASS | a66702d9b donor |
| U3b | Upstream editor; retain outbox/transport/client | Luna high | — | merged | app-U3b-eof-fix | Independent PASS: target23, tsc/lint/diff-check. Integrated overall proof pending composition/farm | f9d5d0cdd merge / 369d882ca source |
| U3c | QUICK harness plus retained journeys | Luna high | — | merged | app-U3c-quick-adapter-fix | Independent PASS retained; source merged, integrated browser/QUICK proof pending farm (not done) | 1c62edf19 merge / 0ba5378cc source |
| U3 | True live upstream merge and Agent re-vendor | Luna high | U3a/U3b/U3c; merged U2 | doing | app-U3-live-compose | Live GitHub ref verified equal to origin/main; sanctioned merge-forward started, Codex resolves full conflicts and reviewed slice joins | upstream 7c17cc9d9 |
| U4p | Adopt regenerated U1 client/schema | Luna high | U1, U3 | todo | — | U1 merged27f0306b9; exact producer checkout requested. Await composed U3 | — |
| A2 | Save funnel and dependent local-document chain | Sol high | C0 APPROVED, U3b merged | merging | app-A2-save-funnel | Independent scoped PASS: inactive session279 tests/tsc/lint. Production funnel/emitter/replies still blocked on official v2 join; not A2 done | e739d880e |
| A3 | Popup/placement/element/registerAsset via A2 | Luna high | A2 | todo | — | — | — |
| A4 | Delete executor/capture ports/adapter/goldens | Luna high | A2, A3, H3 go | todo | — | No deletion before H3 go/no-go | — |
| P1 | Proof lane App chain case collection | Luna high | C0 | merged | ap2-P1-app-chain-cases | Peer PASS: 12 Vitest, tsc/lint; integrated H3 execution awaits farm | 8b979bd21 merge / 898476b0e source |
Upstream: Resolved locally through the connected GitHub read tool. Canonical repository banodoco/astrid-app live refs/heads/main equals local origin/main 7c17cc9d9f9504b578862e2ffd27623fca08a04f. Repeat live check at final merge.
Sources: U2 merged3f1ceaed1, clean exact Agent checkout ready at /home/user/work/wt/agt-pin-3f1ceaed for re-vendor. U1 merged27f0306b9, clean exact producer ready at /home/user/work/wt/rt-pin-27f0306b. U4p/re-vendor follow composed U3 source.
Blockers: Runtime/generated v2 join: A2 current DTOs omit steps/merge/reads/doc.patch and merged/invalid. Official generation/adoption needed; A2 local-chain work continues. Runtime board reports R2r safety HOLD, no restart or workaround requested. Escalation app-20261022T2350-a2-generated-v2-join.md.
Blockers: Viewing/V3: qualified one-artifact packaging/adoption is safety-held after automatic cleanup-command rejection on that lane. Do not repack or adopt an alternate artifact to resolve the U3 Composition-source mismatch.
Blockers: Farm: qualify composed U3 baseline and integrated H3/P1 chain with accepted/merged/refused replies; no duplicate local heavy runs.
Next ready: Review first A2 funnel slice on completion; dispatch A3 as soon as A2 merges. Review true-upstream composition, then U4p/re-vendor when official U1/U2 handoffs arrive. A4 stays behind real H3 GO.
Disk: 17GB free. Resumed overlapping manager ended after independent cleanup: 14 finished v1 source/pin trees recycled with branches/reports retained, current worktrees/shared dependencies untouched. Manager also recycled the two finished v1 App trees; sweep/compact found no eligible scratch.
Blockers: Lead: repeated duplicate manager rounds are yielding harmlessly but consume Sol capacity; suppress duplicate starts while original23:09 round is active. Escalation app-20261022T2358-duplicate-manager-watchdog.md.
