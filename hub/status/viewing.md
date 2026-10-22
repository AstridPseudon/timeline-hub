<!-- viewing | 2026-10-22T22:40:03Z | dispatcher heartbeat 15s | live 1 (sol 0, luna 1, other 0) | busy30 3 | status age 2m -->
# viewing board, 2026-10-22T22:37:41Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V1-prep | schema source and drift inventory (read-only) | Luna high | H0 | review | vw-V1-schema-inventory-resume → vw-V1-schema-inventory-review | Author exit0/report present22:37Z; four schema paths SHA256 f52b8202…97b1 (one symlink); Runtime generator/manifest checks PASS; lock checks held on pre-U1 pin. Independent review queued | No repo changes |
| V1 | open meta namespaces and ignore behavior | Luna high | C0 APPROVED, U1 merged | blocked:runtime | — | No integrated proof; awaiting U1 reviewed merge and regenerated source | — |
| V3 | one commit-named Composition artifact and consumer pins | Luna high | U2, U3 merged | blocked:agent+app | — | No integrated proof; upstream baseline integrations unmerged | — |
| V4 | optional stale dirs/copy/block deletions | Luna high | U2, U3 merged (lane brief) | blocked:agent+app | — | Not started; first to cut | — |

Blockers: orchestrator/lead — unresolved cleanup permission refusal: bin/recycle app-pin-d00a6613 app-pin-0d432391 exit255/Permission denied at22:32Z. Cleanup stopped; no retry, alternate deletion or bypass. See escalations/viewing-20261022T2232Z-recycle-permission-refusal.md. Current disk reports16G available, above15GB decimal target; refusal still needs owner resolution.
Blockers: Runtime — V1 needs merged U1; current hub board22:20Z holds85b13f3b4 after review FAIL/permission refusal. C0 APPROVED22:15Z; C0b gates undo only. Inventory may continue read-only.
Blockers: Agent/App — V3/V4 need merged U2/U3; current hub Agent22:18Z quarantines8a2677cd7 after failed upstream merge preparation; App U3a/b/c underway. No dependent implementation dispatched.
Next ready: consume independent V1-prep review; V1 after reviewed merged U1; V3/V4 after merged U2+U3.

Read through INBOX restart NEW item; no newer item. BOARD-HEADER v2.1 and contract section6 read. All preceding v1 work/rules remain VOID; no parity, old rendering or ledger work resumed. One read-only Luna review queued; author completed without repo changes; no fixed worker quota in v2.1. Manager writes only briefs/status/escalations, no product/test/generated/pin changes. No ready implementation left waiting.

V1-prep source map published by worker: design/viewing-v1-schema-inventory.md. No prep result counted as V1 implementation or integrated meta proof. Review checks distinction between Runtime-owned materialization and pinned package authored source, plus actual raw payload/meta boundaries.
