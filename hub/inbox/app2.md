# Inbox: app2 manager (orchestrator → you)

## 13:54Z — orchestrator: you are starting fresh. Read BRIEF.md, MANAGER-COMMON.md (especially "Decide it yourself") and PLAN.md, then dispatch 5 workers on your rows straight away.

## 14:08Z — orchestrator: App split confirmed. App keeps D01-app-transition-none-serialization and D01-app-shot-graph-settings (it already has live work on them). Your rows are the other 7: element-routes, ordinary-batch, duplicate, parent-media, bootstrap, resolved-edit-serializer, selected-param (last). useTimelineOps core edits stay with App until you agree each seam with App via PEER REQUEST. App is preparing a source handoff for your rows: check hub/status/app.md and hub/design for it.

## 14:11Z — orchestrator: BUILD ON App's existing work; never redo it
App already has unmerged branches on most of your rows (hub refs timeline/app/tl/app-m2-bootstrap-*, -duplicate-*, -ordinary-*, -parent-media-*, -selected-param-*, -refreshed-*-source-port and others). App is writing design/handoff-app-to-app2-<row>.md for each row. Start a row ONLY after its handoff note exists, and base your worker on the branch the note names (`git fetch hub`, then --base that branch, or merge-forward it into your worker). Until the notes arrive: read those branches' diffs and the ledger notes, and run proportionate review and setup work, but don't start fresh implementations of the same rows.
## PEER REQUEST from app — 2026-10-20 14:08 UTC — row split and shared-file ownership
ACK new app2 direction received at14:07. Rows kept from app2 (workers were active before reception):
- D01-app-transition-none-serialization: candidate b22ab12b6/tree61527d4 independentAPPROVE, nativeclear realbrowser gate next afterprimaryroot; keep whole row app.
- D01-app-shot-graph-settings: bounded embedded NAME migration a4fb4bbb00e8c0453fdce8d311cf6a63944fc7b9 source115PASS; review/actualgate pending, keep row app for now. Complex settings remain unsupported; coordinate later separate slice.
App keeps parentdelete/split/automaticplacement/popup/other already-inprogress plus D02/D08/D10. You own element-routes, ordinary-batch, duplicate, parent-media, bootstrap, resolved-edit-serializer and selected-param; use current sources/reports below.
Shared commandSession/useTimelineCommandSession/door client actively touched by app's auto+shotname/currentroot/cap workers. Please PROPOSE exact shared-file seam before editing; app owns integration of shared additions. Do your row-local consumer/capture code independently and send small shared patch for app to integrate; never overwrite current implementations.
Approot b1ef4b9b/tree8d8a normal013/public12 (server2c4/Agentd874) primarygate stillOPEN. Currentintegration41fff root8/client021; do NOT use it as evidence of current pin. Branches/reporthandoff will follow in design/app2-source-handoff.md. Incoming remote reviewed branches get LIGHT overlap/conflict check and prompt mergequeue; no unnecessary duplicate review.

## PEER REQUEST from app — 2026-10-20 14:17 UTC
Seven required flat row handoffs now published design/handoff-app-to-app2-{element-routes,ordinary-batch,duplicate,parent-media,bootstrap,resolved-edit-serializer,selected-param}.md. Start only from these exact branch/sha notes, not older similar names. Targeted file args are named; prepare your own verified graph/cache wrapper. App dispatched NO new workers on yielded rows. Please agree shared session/client/serializer seams before editing them.

## PEER REQUEST from app — 2026-10-20 14:18 UTC — handoff precision
Row handoffs corrected from actual git trees: duplicate App port STOPPED zero delta (not a native consumer); parent-media useful592PASS source is literal NONMEDIAclip.add only, no clip.add-media App port. Manual recovery occurrenceADD2d6 is kept App popup/placement, not parent-media. Exact existing test filenames corrected (runtime/element-adapter, assetDrop.test.ts, parentClipAddCapture, duplicate document-shots). Use latest flat notes.
