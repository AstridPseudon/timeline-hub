# app2 lead: work list (orchestrator, updated 2026-10-20T20:43Z). Read this every hour.
GOAL: your 7 App rows are DELETED: element-routes, ordinary-batch (the critical path), duplicate, parent-media, bootstrap, resolved-edit-serializer, selected-param (last).
STANDING RESPONSIBILITIES: services alive with a Monitor ALWAYS armed; 5-7 live workers; disk >10 GB; merge-forward onto the latest hub integration right before each merge request; lead line hourly in hub/status/app2-lead.md.
WORK LIST NOW:
1. ordinary-batch first: useTimelineOps.ts:298 snapshot ingress is the central remaining App writer. Report its status.
2. Your 4 earlier branches are IN App integration (20ea14c26); don't redo them. Mark their rows' progress.
3. Mark each row DELETED in design/deletion-ledger.app.md (or tell App's manager) the moment its deletion merges.
DONE WHEN: all 7 rows are DELETED with merge shas.
