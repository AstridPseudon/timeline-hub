# app2 lead: work list (orchestrator, updated 2026-10-20T23:32Z). Read this every hour.
NOTE: report progress in your hourly lead line, not by message; message only for blockers, escalation categories, tool bugs or direct questions (LEAD.md "Communication").
GOAL: your 7 App rows are DELETED: element-routes, ordinary-batch (the critical path), duplicate, parent-media, bootstrap, resolved-edit-serializer, selected-param (last).
STANDING RESPONSIBILITIES: services alive with a Monitor ALWAYS armed; 5-7 live workers; disk >10 GB; merge-forward onto the latest hub integration right before each merge request; lead line hourly in hub/status/app2-lead.md.
WORK LIST NOW:
1. ordinary-batch first: useTimelineOps.ts:298 snapshot ingress is the central remaining App writer. Report its status.
2. Your 4 earlier branches are IN App integration (20ea14c26); don't redo them. Mark their rows' progress.
3. Mark each row DELETED in design/deletion-ledger.app.md (or tell App's manager) the moment its deletion merges.
4. (22:03Z, deep audit) Duplicate is DELETED, good. Next: ordinary-batch now that 7d42fcd3a landed, coordinated with App item 10 (the mounted journey).
9. (23:32Z) READY QUEUE (new tool): capacity dipped below 4 in 3 areas this hour as short workers ended together. Make the manager keep 3+ briefed items in managers/app2/ready via bin/request-ready (MANAGER-COMMON 'READY queue'); the dispatcher auto-starts them under 5 live. Report the READY count in your lead line. Also: the theme-api.fallback build blocker: check design/ for the App/Viewing answer before asking again.
10. (00:36Z) MANAGER RESTART ONCE NOW: managers only read kit rule changes at round start. bin/run-manager now uses 90-min rounds (was 3 h). After your hub-sync installs the new bin/run-manager (grep '90m' $ORCH/bin/run-manager), restart the manager once, with a LEAD NOTE: 'top up managers/<area>/ready to 3 via bin/request-ready, then dispatch to 5 live'. Report the READY count and live count in your lead line.
11. (01:47Z) Canary deletion follow-up (INBOX 01:47Z): one Luna worker adds the foreign-owned/user-clip skip tests for transcript-lane and scene-phase-markers remove/update, and drops the 2 stale references. Report the merge sha in your lead line.
DONE WHEN: all 7 rows are DELETED with merge shas.
