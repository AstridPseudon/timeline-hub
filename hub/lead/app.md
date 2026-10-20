# App lead: work list (orchestrator, updated 2026-10-20T20:43Z). Read this every hour. It overrides older inbox wording.
GOAL: App's M2 writer retirements land, and its deletion-ledger rows turn DELETED. You keep the machine and the manager delivering that.
STANDING RESPONSIBILITIES: services alive (dispatcher, hub-syncd, 3 h manager rounds, your Monitor); 5-7 live workers; disk >10 GB (sweep-tmp, recycle, compact-scratch hourly); the manager acknowledges its INBOX within 45 min (restart it if not); lead line hourly in hub/status/app-lead.md.
WORK LIST NOW (report each as done / blocked):
1. The 5 new failures on 20ea14c26 (shotCompositionRuntime popup x3, getProjectVerifiedMedia relay x2): fix workers green, then the ONE full re-run green. No dependent merges until then.
2. Workers back to 5+ within 30 min; at least 2 on deletion-ledger rows (D01 writers you kept, D02, D08, D10). Tell me their ledger row ids.
3. app2 merge requests are auto-queued. Any REFUSED (conflict) is resolved by an App merge-forward worker within one manager round. Check hub/merge-results/app hourly.
4. Composition 0.0.13 adoption (App first): confirm it has landed on App integration, and tell me the sha. If it hasn't, make it the manager's top item.
5. Upstream main: when refresh-main --check on main reports App behind, merge-forward within the same day (tests move with upstream, never dropped).
6. CRITICAL PATH (added 20:51Z): app2 handed App a shared-file patch for ordinary-batch (useTimelineOps stale retained adapter; peerfix 97fb1c46…, in its flat handoff note in design/). App owns that file, so land it as the manager's TOP item this round: review lightly, run the targeted tests, merge, and tell app2 the sha. Ordinary-batch is the central remaining App writer.
7. (21:02Z) PARALLEL GATE TRACK: keep one Luna worker on Gates 5, 6 (writer half) and 3 (App half) at all times, in parallel with deletions; it counts toward 5-7. Report its status in your lead line.
8. (21:24Z) Viewing's gate-6 worker (vw-m3-gate6-current-suite-owner) is HELD on App: the "owner-five / controller-two" merge and a clean Root. Tell me which App merge that is and its ETA, and make it the next merge after the current full turns green.
9. (21:27Z) MAIN DRIFT: upstream app main is 72 commits ahead. The manager dispatches ONE merge-forward worker today (--merge-parent the upstream tip; regenerate generated files with the repo tooling; tests move with upstream, never dropped), merges it, then reruns the affected gates. Report the merge sha. If a published contract or pin changes, tell me.
DONE WHEN: every App ledger row is DELETED or KEEP with evidence, all App gates are green on current main, and the manager reports M2 exit.
