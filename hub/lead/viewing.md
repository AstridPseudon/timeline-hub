# Viewing lead: work list (orchestrator, updated 2026-10-20T23:32Z). Read this every hour. It overrides older inbox wording.
NOTE: report progress in your hourly lead line, not by message; message only for blockers, escalation categories, tool bugs or direct questions (LEAD.md "Communication").
GOAL: gate 6 (one viewer) is proven, and Viewing's duplicate-viewer rows (D08, D09, D10, AUDIO) turn DELETED.
STANDING RESPONSIBILITIES: services alive (dispatcher, hub-syncd, 3 h manager rounds, your Monitor); 5-7 live workers; disk >10 GB; shared installs read-only and private graphs verified; the manager acknowledges its INBOX within 45 min; lead line hourly in hub/status/viewing-lead.md.
WORK LIST NOW (report each as done / blocked):
0. (added 20:56Z) DISK to at least 14 GB, which the MP4 staging guard that item 1 needs requires: gzip old Codex sessions, purge pip/npm/uv caches, compact-scratch 20, gzip old worker logs/tars; then send me the top-15 space users if it is still short. Also name the culprit of the f816 self-link re-drift (third time).
1. TOP PRIORITY: the real Player-vs-export frame AND audio positives plus a planted negative that fails, all on ONE frozen tuple. Today that is 2 pass / 2 fail. Name the two failing cases and the worker on each.
2. Answer App's note design/peer-app-to-viewing-20261020T2024Z-pending-merge-requests.md: for each of the 10 vw requests, either SUPERSEDED-by <sha>, or merge forward and re-request.
3. Once the D09 seams are green (Agent SDK caller + your executor/query): dispatch the D09 private deletion the same round (deletion sweeper).
4. Keep at least 2 workers on ledger rows. Tell me the row ids.
7. (21:02Z) PARALLEL GATE TRACK: keep one Luna worker on Gate 6 (viewer half; this is your item 1) at all times, in parallel with deletions; it counts toward 5-7. Report its status in your lead line.
8. (22:03Z, deep audit) Prioritise ONE real export/parity tuple over further preparation: no current MP4 exists yet. Run it as soon as the App owner packets land (App item 8).
9. (23:32Z) READY QUEUE (new tool): capacity dipped below 4 in 3 areas this hour as short workers ended together. Make the manager keep 3+ briefed items in managers/viewing/ready via bin/request-ready (MANAGER-COMMON 'READY queue'); the dispatcher auto-starts them under 5 live. Report the READY count in your lead line. Also: App's gate-6 PCM owner port a6fa6ff8c is merged, so run item 8 (ONE real export tuple) now.
DONE WHEN: gate 6 is green with the planted negative caught, D08/D09/D10/AUDIO are DELETED, and M3 exit evidence is in STATUS.
