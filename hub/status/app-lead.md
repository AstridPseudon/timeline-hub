# app lead - 2026-10-20T03:17Z (hourly check-in)

## Health
- Dispatcher heartbeat 11s (pid 310, up ~40 min, started with PLAYWRIGHT_BROWSERS_PATH). hub-syncd alive (pid 311). Last "hub-sync app" commit on origin/main 03:12:27Z (~5 min old); no rebase-merge in the hub clone. (Push-negotiation warnings in hub-sync.log are harmless; pushes land.)
- Codex: "Logged in using ChatGPT". Lead watcher (lead-watch.sh, pid 4705) running again since the 02:34Z recovery.
- Disk: 20 GB free on /home/user (51% used). Mem 14 GB available, load ~1. No recycling by me this hour.
- Leased worktrees present, clean, KEEP-marked: app-m1-full-agent-source at 4a75f68f, app-m1-full-runtime-source at 4bb1d0f7.

## Manager
- Model gpt-6.1-sol/high, no fallback, no rate-limit/auth errors. Alive (timeout 7d codex exec pid 352, round 20261020T0234Z, started 02:34Z, running marker present). ACTIVE, not idle: STATUS refreshed 03:12Z and two new workers were dispatched at 03:13Z.
- Workers running: 2 (app-m2-ordinary-core-qualify, app-m2-parent-track-create-capture; both started 03:13Z). Below the 5-7 target: six workers finished between 03:07 and 03:12Z and the manager is mid-dispatch; briefs for app-m2-empty-bootstrap-seam, controls-source-compose and others are written. No test running; queue pending/held empty. If still <5 at ~03:45Z without a stated blocker, the watcher/I will restart the manager.
- Six interrupted M2 workers (exit=137): four were re-dispatched as -r1 and finished (placement-native-parity-r1, scalar-controls-r1, trim-ingress-map-r1, writer-contract-refresh-r1; plus scalar-control-owner-fix and ordinary core results are in STATUS). ordinary-session-compose and outbox-upgrade-proof have no -r1; STATUS lists their results (ordinary f5e438652, outbox upgrade 9 cases) as completed UNRUN, and ordinary-core-qualify is now running. No failed or stuck workers. queue/refused: the 3 old items plus 1 old test, unchanged.
- Corrected-environment App full: requested and COMPLETE (app-full-m1-opaque-integration-1020025341-10022): 18336 PASS / 6 exact-baseline FAIL / 3 expected, all 1459 files executed, 991 s, failing set equal to the accepted baseline, ZERO new. Used the restored lease sources. 26543 stays recorded as INVALID ENVIRONMENT.
- Integration sha of /home/user/work/app: c8566f12d114c538db8136b8c580a1e663af1ad1 (merged 02:17:58Z, app-m1-opaque-move-parity; only new merge since 02:16Z).

## Milestone (STATUS.md, 03:12Z)
M0 COMPLETE; APP M1 EXIT COMPLETE (parity full 10022 zero new); global M1 NOT RECORDED in PLAN.md (gate record still only Checkpoint A + "Hard stop: NOT YET"). All M2/M3 integration merges HELD. Not COMPLETE, no infrastructure blocker. Quiet window ended; targeted core tests allowed.

## Lead instructions / inbox items seen and acted on
- hub/lead/app.md: no new items after 00:55Z (file unchanged). Earlier items all done.
- 02:32Z container restart: recovered by lead-recover.sh (dispatcher, hub-syncd, manager, watcher); six M2 workers marked exit=137 INTERRUPTED; full 17106 marked interrupted.
- 02:49Z orchestrator decision (leased sources recycled): 26543 cancelled INVALID ENVIRONMENT; 02:58Z leased-worktree fix done: both worktrees recreated (Agent 4a75f68f, Runtime 4bb1d0f7), lease notes updated, workers/<w>/KEEP set. One corrected-environment full authorized and completed (10022, above). The kit bin/recycle (refuses KEEP / *.lease / *ACTIVE* names) is in hub/kit and $ORCH/bin/recycle is byte-identical to it. The lead's own recycler follows the RECYCLE RULE (recyclable-finished-clean.txt or merged App workers, under flock).
- New hub/inbox/app.md items through Runtime 02:59 (popup decision 02:12, Runtime 02:16 and 02:33 notes, Agent 02:39 Bundle2 FROZEN, orchestrator 02:49 and 02:54, Runtime 02:59 M1 final) are all in managers/app/INBOX.md; manager STATUS ACKs the 02:49 full authorization/recycler fix, Agent 02:39, Runtime 02:33/02:12/02:07.
- Closed escalations since last check: popup-media-read-gap, leased-full-sources-recycled, remaining-writer-contracts (all answered). New hub/kit changes (AREA-LEAD recycling rule, COMMON "full only if brief asks", PLAN capture-certification line, recycle) applied automatically by sync.
- Merge request vw-m3-initial-projection-mounted (910773b31, from Viewing): PENDING owner review, HOLD until M1 record; no action.
- Open manager escalations on the hub/outbound: app-20261020T031215Z-m1-parity-complete (on origin/main); app-20261020T031359Z-empty-bootstrap-preservation (written 03:13Z in $ORCH/escalations, publishes with the next sync; Agent/Runtime-owned decision, judgment, not mine).
- Viewing's 03:02Z "snapshot-postflight" escalation asks for a lead action on the Viewing machine (.test snapshot lifetime); not this machine's.

## Infra changes this check
None (no restarts, no recycling, no config changes).

## Open blockers and attempted fixes
- Worker count 2 < 5: manager active and dispatching after a burst of completions. Re-check next hour; restart rule at 30 min.
- No infrastructure blockers.

## Questions for the orchestrator
- Please record global M1 in PLAN.md (App 10022 ZERO NEW, Runtime 3829/7-baseline zero new, Agent 4a75f68f). M2/M3 merges and the held public10 install wait on it; the workers are limited to source/static work meanwhile.
- Pending your decision: app-20261020T031359Z-empty-bootstrap-preservation (two preservation seams for createDefaultTimeline) and Agent/Runtime ownership of the transition-SET and parent media/import insertion contracts.

## Lead 03:20Z: re orchestrator 03:17Z (Codex usage limit on main)
- App machine Codex WORKS: at 03:19Z `codex exec -m gpt-5.6-luna ... "Reply with exactly: ok"` returned ok, and `codex login status` says logged in (ChatGPT). No "hit your usage limit" appears in any App manager round log or worker log. So no CODEX_UNAVAILABLE flag here, and the manager stays on gpt-6.1-sol.
- Prepared: if the limit appears here, the lead will create $ORCH/CODEX_UNAVAILABLE, use the kit's bin/run-manager and bin/dispatch (Sol->Sonnet, Luna->Haiku mapping), restart the manager with claude-sonnet-5-5, mark interrupted workers, and cap at 5 workers. The lead watcher now alerts on that error string.
- App M1 acceptance (full 10022) noted.
