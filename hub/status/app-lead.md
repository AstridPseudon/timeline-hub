# app lead - 2026-10-20T02:16Z (hourly check-in)

## Health
- Dispatcher heartbeat 12s (pid 311, running with PLAYWRIGHT_BROWSERS_PATH env). hub-syncd alive (pid 310); last "hub-sync app" commit on origin/main 02:09:37Z (~6 min old, within cadence); no rebase-merge in the hub clone. Codex: "Logged in using ChatGPT".
- Disk: 7.8 GB free on /home/user (81% used; below the 8 GB floor). Another lead subagent is recycling worktrees; I recycled nothing. /home/user/work/wt is 18 GB (66 worktrees). Mem 14.9 GB available, load ~2.
- Lead watcher (scratchpad/lead-watch.sh): NOT running (count 0). It is a one-shot ~55 min monitor owned by the lead session; the container restart and its 01:49Z exit explain it. Its auto-recycle (<10 GB) and manager auto-restart therefore are not active until the lead session re-arms it. I did not start it detached because its output would go nowhere.

## Manager
- Model gpt-6.1-sol/high, no fallback, no Codex rate-limit/auth errors. Alive (codex exec pid 4123, 26 min old, round 20261020T0148Z log still growing, 958 KB) and ACTIVE: it was writing briefs at 02:14Z (scalar-ingress-map, parent-delete-real-spec). No restart done by me this hour (last restart 01:49Z, see lead-manager-restarts.log).
- Workers running: 3 (app-m1-opaque-move-parity 02:09Z, app-m2-params-null-session 02:11Z, app-m2-scalar-owner-binding 02:11Z). Below the 5-7 target; two new briefs were just written and dispatch should follow, and free disk (7.8 GB) is a plausible limit. Watch at the next check: if still <5 for 30 min (from ~02:18Z) without a stated blocker, restart.
- No failed (nonzero exit) workers; none stuck. queue/pending and held are empty. queue/refused holds 3 old items (app-m1-bounded-log-classify, recovery-core-local, recovery-ui-local) plus one old test request; unchanged and known.
- Integration sha of /home/user/work/app: ea3461e0c6945e50e4e80539ead92ed2fbc7efe7 (in sync with hub/tl/integration).

## Milestone (STATUS.md, 02:12Z)
M1 App parity port LANDED (opaque-remap port merged at ea3461e0c, 02:06:47Z, the only new merge since 00:33Z); M0 COMPLETE. Global M1 remains unrecorded in PLAN.md (gate record has only Checkpoint A and "Hard stop: NOT YET"); waiting on the Runtime null-speed fix (Agent a610 fix already merged). All M2/M3 integration merges HELD. Not COMPLETE, not blocked on infrastructure.

## Lead instructions / inbox items seen and acted on
- Container restart recovery ~01:18Z: dispatcher (with PLAYWRIGHT_BROWSERS_PATH), hub-syncd, manager and watcher were restored; manager restarted 01:18Z.
- Final M1 fulls 12729 and 2755 both showed exactly the 6 baseline failures (18301 PASS / 6 baseline FAIL / 3 expected, 1458 files executed). Orchestrator accepted App's final full at 01:58Z and approved parity.
- Manager restart 01:49Z (round 20261020T0148Z) for "full speed on M2 branch work, only merges wait".
- hub/lead/app.md items since last-seen (00:10Z OOM check on full 24066, 00:15Z bundle1 read-only worktrees, 00:55Z quiet window, 00:50Z release held jobs): all done earlier (full retried and finished, bundle1 leases exist and are protected, held queue is empty). No new lead instruction after 00:55Z.
- New hub/inbox/app.md items through 02:07Z (opaque-remap-parity, native group delete gap, opaque-native-expectations APPROVED, label-initial-release-batch APPROVED) are all present in managers/app/INBOX.md and reflected in STATUS.md (opaque native expectations merged 02:06Z, opaque-move-parity worker active, release compose done). The 02:07Z label-initial-release item is acknowledged only implicitly in STATUS (combined release composer); manager will see it as INBOX.md already holds it.
- Escalations: app-20261020T0202Z-opaque-native-expectations, T0203Z-label-initial-release-batch, T0205Z-popup-media-read-gap are on origin/main hub/escalations (the first two answered at 02:07Z). Open for the orchestrator/Runtime: T0205Z popup-media-read-gap (Runtime/Agent decision on production read for popup ADD/SWAP).
- Merge requests from Viewing (vw-m3-app-pure-opacity df6ba7120, vw-m3-flat-compiled-source b23108926): PENDING owner review, HOLD until M1 record; no action.
- Disk cleanup in progress by another lead subagent (recycle log last entries: render-requester-map, opaque-native-expectations, opaque-remap-parity).

## Infra changes this check
None (no restarts, no recycling, no config changes).

## Open blockers and attempted fixes
- Disk 7.8 GB < 8 GB floor: recycling is being handled by another subagent; lead watcher auto-recycle is currently off. Not touched by me.
- Lead watcher not running: needs re-arming by the lead session (not restarted here).
- Worker count 3 < 5: manager active and queuing; re-check next hour.

## Questions for the orchestrator
- None new. Pending on your side: Runtime null-speed fix then PLAN M1 record; popup-media-read-gap decision (Runtime/Agent).

## Lead 02:25Z: disk pressure on the app machine (for the orchestrator / App manager)
- Free disk fell to 7.6 GB at 02:12Z. Recycling finished worktrees already contained in integration or in another live branch brought it back to 13 GB.
- About 45 finished App M2 worktrees (~300 MB each) cannot be recycled safely: their branches are unmerged (M2 merges are held until the M1 record) and contained nowhere else. With 5–7 new workers running, disk will shrink again.
- Ask: please have the App manager name in STATUS.md (or a "Recyclable:" line) the finished workers it no longer needs a worktree for (superseded, or composed into another branch). Branches are always kept; only worktrees are removed. The lead watcher will then recycle them automatically.

## Lead 02:36Z: second container restart (~02:32Z), recovered
- All processes were lost again. By 02:35Z the dispatcher (Playwright shim env), hub-syncd, the App manager (Codex gpt-6.1-sol, round 20261020T0234Z) and the lead watcher were back. Disk, repos and Codex login are intact.
- Six M2 workers were killed mid-run and marked exit=137 INTERRUPTED (no commit; any partial changes stay uncommitted in their worktrees) for the manager to re-dispatch: app-m2-ordinary-session-compose, outbox-upgrade-proof, placement-native-parity, scalar-controls, trim-ingress-map, writer-contract-refresh.
- Full app-full-m1-opaque-integration-1020022402-17106 was killed mid-suite (no final summary; log kept) and marked error INTERRUPTED. Requeued once as app-full-m1-opaque-integration-1020023434-26543 on the same target and suite.
- Recovery is now scripted, so a future restart is restored the same way.
