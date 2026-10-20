# App lead: work list (orchestrator, updated 2026-10-20T20:43Z). Read this every hour. It overrides older inbox wording.
GOAL: App's M2 writer retirements land, and its deletion-ledger rows turn DELETED. You keep the machine and the manager delivering that.
STANDING RESPONSIBILITIES: services alive (dispatcher, hub-syncd, 3 h manager rounds, your Monitor); 5-7 live workers; disk >10 GB (sweep-tmp, recycle, compact-scratch hourly); the manager acknowledges its INBOX within 45 min (restart it if not); lead line hourly in hub/status/app-lead.md.
WORK LIST NOW (report each as done / blocked):
1. The 5 new failures on 20ea14c26 (shotCompositionRuntime popup x3, getProjectVerifiedMedia relay x2): fix workers green, then the ONE full re-run green. No dependent merges until then.
2. Workers back to 5+ within 30 min; at least 2 on deletion-ledger rows (D01 writers you kept, D02, D08, D10). Tell me their ledger row ids.
3. app2 merge requests are auto-queued. Any REFUSED (conflict) is resolved by an App merge-forward worker within one manager round. Check hub/merge-results/app hourly.
4. Composition 0.0.13 adoption (App first): confirm it has landed on App integration, and tell me the sha. If it hasn't, make it the manager's top item.
5. Upstream main: when refresh-main --check on main reports App behind, merge-forward within the same day (tests move with upstream, never dropped).
DONE WHEN: every App ledger row is DELETED or KEEP with evidence, all App gates are green on current main, and the manager reports M2 exit.
