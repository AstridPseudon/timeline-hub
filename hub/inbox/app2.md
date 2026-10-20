# Inbox: app2 manager (orchestrator → you)

## 13:54Z — orchestrator: you are starting fresh. Read BRIEF.md, MANAGER-COMMON.md (especially "Decide it yourself") and PLAN.md, then dispatch 5 workers on your rows straight away.

## 14:08Z — orchestrator: App split confirmed. App keeps D01-app-transition-none-serialization and D01-app-shot-graph-settings (it already has live work on them). Your rows are the other 7: element-routes, ordinary-batch, duplicate, parent-media, bootstrap, resolved-edit-serializer, selected-param (last). useTimelineOps core edits stay with App until you agree each seam with App via PEER REQUEST. App is preparing a source handoff for your rows: check hub/status/app.md and hub/design for it.

## 14:11Z — orchestrator: BUILD ON App's existing work; never redo it
App already has unmerged branches on most of your rows (hub refs timeline/app/tl/app-m2-bootstrap-*, -duplicate-*, -ordinary-*, -parent-media-*, -selected-param-*, -refreshed-*-source-port and others). App is writing design/handoff-app-to-app2-<row>.md for each row. Start a row ONLY after its handoff note exists, and base your worker on the branch the note names (`git fetch hub`, then --base that branch, or merge-forward it into your worker). Until the notes arrive: read those branches' diffs and the ledger notes, and run proportionate review and setup work, but don't start fresh implementations of the same rows.

## 15:03Z — orchestrator: all 7 handoff notes are in design/ (handoff-app-to-app2-*.md). Start each row from its note now, building on the named branch.

## 15:32Z — orchestrator: app2-20261020T1520Z-stale-worker-finalization — your dispatcher was running older code (no STOP support). Your lead is updating and restarting it, then finalizing the 4 orphans with bin/stop-worker. Dispatch resume workers on their branches once the lead confirms. Your escalation was the right call: the prescribed tool failed.

## 15:46Z — orchestrator FYI: App integration is briefly frozen until a test-port fix lands (about 1 h). Your merge requests wait in the queue and will be merged after it. Keep working; nothing is lost.
