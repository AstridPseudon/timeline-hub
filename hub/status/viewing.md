<!-- viewing | 2026-10-22T23:11:19Z | dispatcher heartbeat 6s | live 0 (sol 0, luna 0, other 0) | busy30 2 | status age 3m -->
# viewing board, 2026-10-22T23:08:11Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V1-prep | schema source and drift inventory (read-only) | Luna high | H0 | review | vw-V1-schema-inventory-review2 | Corrected author exit0/report present; independent second review queued on tl/vw-V1-schema-inventory-fix. First FAIL received one bounded correction. Four-copy SHA/cmp + Runtime generator/manifest checks pass; no implementation proof | No repo changes |
| V1 | bounded open meta and consumer ignore behavior | Luna high | C0 APPROVED, U1 merged | blocked:runtime | — | Awaiting U1 reviewed merged source and regeneration seam; contract section6 includes registry records and separate parent/config meta locations | — |
| V3 | commit-named Composition artifact and both consumer pins | Luna high | U2, U3 merged | blocked:agent+app | — | Awaiting reviewed baseline merges; no artifact/pin work dispatched | — |
| V4 | optional stale dirs/copy/block deletions | Luna high | U2, U3 merged per lane brief | blocked:agent+app | — | Not started; first to cut | — |

Blockers: orchestrator/lead — bin/recycle app-pin-d00a6613 app-pin-0d432391 returned Permission denied at22:32Z; cleanup remains stopped, no retry or alternative deletion. Existing escalation viewing-20261022T2232Z-recycle-permission-refusal.md. Current disk ~16GB available, above15GB target.
Blockers: Runtime — V1 needs reviewed merged U1 plus its canonical materializer source handoff. Latest synced Runtime22:42 board still has rt-U1-real-upstream doing; C0/C0b APPROVED, C0c pending root amendment does not change section6.
Blockers: Agent/App — V3/V4 need U2/U3 merged. Latest synced Agent22:18 has U2 quarantined/retry blocked; App22:44 has U3a safety stop, U3b recovery and U3c review. Upstream completion unverified, so implementation stays gated.
Next ready: V1-prep review disposition; V1 immediately after reviewed U1 merge; V3/V4 immediately after U2+U3 merged.

Restart audit: corrected V1-prep author finished22:44Z, exit0/report; original restart-killed worker superseded by resume+fix. Queued independent Luna high review2 at23:08Z using existing bounded review brief. No v1 task/review/ledger resumed. No fixed worker target under v2.1. No ready authorized implementation left waiting. Manager writes only briefs/status/escalations; all code/tests/generated/pins remain workers' work.

Inventory: design/viewing-v1-schema-inventory.md, authored by worker. Runtime contract copy is canonical integration artifact; upstream package/materializer source provenance must stay truthful. Four actual duplicates include App node_modules alias, not four independent authored sources. Explicit gaps: Agent registry meta allowlist, Composition asset type, bounded raw meta validation; unknown meta must never become media references.
