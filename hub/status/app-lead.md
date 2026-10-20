# app lead - 2026-10-20T00:33Z (hourly check-in)

## Health
- Dispatcher heartbeat 1s. hub-syncd alive (pid 4743); last "hub-sync app" commit on origin/main 00:14:16Z (sync runs every ~5 min); no rebase-merge in the hub clone. Lead watcher (lead-watch.sh) alive. Codex: "Logged in using ChatGPT". Disk: 15G free on /home/user (63% used; floor 8G). Mem 15G total, ~11-14G available; cgroup OOM kills of worker tsc (node ~1.7G RSS) seen 23:57-00:04Z.
- Manager: alive and ACTIVE (codex exec pid 13287, round 20261019T2229Z log still growing, writing briefs at 00:22Z), model gpt-6.1-sol/high, no fallback, no real CLI rate-limit/auth errors. No restarts this hour (no lead-manager-restarts.log entries).
- Workers running at 00:29Z: 1 (app-m1-full-extra-classify, started 00:18Z). Target is 5-7. Seven workers were active at 00:10Z; most finished at 00:15-00:27Z (clip-params-parity, history-retirement-map, label-client-pin, recorder-primitives all exit 0). Manager has just written 3 more briefs (label-browser-qualify, bundle1-agent-source, bundle1-runtime-source) not yet dispatched. Not idle (no restart); the watcher restarts it if <5 for 30 min (~00:45Z) with no external blocker. Failed 0, stuck 0. Queue refused: only the two old app-m1-recovery-*-local items.
- Integration sha (/home/user/work/app tl/integration): 2bfde69ea (tree dd1fe6a725cf20015f7b8cb4a966bdf507319653), clean. No new merges since 23:42:37Z (app-m1-draft-opaque-roots). M2 merges held.
- Milestone (STATUS.md 00:18Z): M1 App preservation fixes COMPLETE on integration; M1 awaits orchestrator record; M0 COMPLETE; M2 on branches (bundle #1 label qualification, clip delete/params/parent add/swap capture, edge PURGE composed). PLAN.md gate record: still no M1/M2/M4 entry; hard stop NOT reached.

## Final full run
- app-full-source-integration-1019234330-24066: FAIL exit=1 in 2097s on tree dd1fe6a7 (started 23:56Z, ended ~00:29Z). Test Files 6 failed|1451 passed (1457); Tests 9 failed|18280 passed|3 expected fail (18292).
- Classification: 6 original baseline nodes (examples-governance x2, HoverScrubVideo.gateway x2, AuthContext.gated x1, useAgentSession.proposal-vertical x1) = same as app-full-1019224105-27715. New vs baseline: 3 nodes: PublicAstridSite.lifecycle x2 and EmptyWorkspaceGuidance x1. All three ran under heavy load (54.9s file); lead isolated rerun on the exact tree (--maxWorkers=1): both files PASS, 16/16, 11s. So: baseline 6 + 3 load-flaky nodes that pass in isolation; no product failure shown. Manager classifier worker app-m1-full-extra-classify is running. Orchestrator judgment needed (escalation app-20261020T0032Z-lead-m1-final-full-classification).
- app-m1-draft-opaque-roots-full-source-integration-1019233523-9530: status=error "could not compute tree of wt/app-m1-draft-opaque-roots" (worktree recycled while it waited); same tree and cache key as 24066, so 24066 is the evidence. Not requeued. The classification is also appended to App STATUS.md (Lead 00:31Z line).
- Old app-full-1019230552-26792: cancelled 23:55Z by the lead at the orchestrator's request (process group killed, status=cancelled, markers and snapshot removed).

## Lead instructions and inbox
- hub/lead/app.md new since last check: 23:30Z MAX SPEED (keep 5-7 workers, heavy cap 2, nudge/restart if idle). Acted: the watcher + this check; manager has acked MAX SPEED in STATUS. Nothing else.
- hub/inbox/app.md (92729 bytes) == managers/app/INBOX.md (92732, hub-sync copies when larger): reached the manager. New items since 23:20Z: 23:15 close M1, 23:18 data-loss guard FYI, 23:30 MAX SPEED, Runtime 23:42, 23:55 BUNDLE #1, Runtime 23:49/00:00, 23:53 M1 safety accepted, 23:58 deletion ledger, 00:05 popup-native-contract DECISION (bundle #2). STATUS (00:18Z) acks through the 23:58 ledger and the 23:55 bundle; the 00:05 decision is reflected (docs-only popup audit, bundle 2 sources) but its explicit ACK is not yet in the Inbox line.
- hub/kit/PLAN.md changed (M1 destination-occupancy exit item; owner deletion-ledger intent): auto-copied by hub-sync. design/ updates mirrored by hub-sync.
- Escalations: popup-native-contract answered by the 00:05 inbox decision (already in hub closed). Lead handled two infra escalations (moved to $ORCH/escalations/closed with responses): (1) tsc-memory-pressure: inspected host, full 24066 was healthy and not killed; manager's flock/4 GB cap mitigation endorsed. (2) bundle1-checkouts: created detached read-only-use worktrees /home/user/work/wt/app-bundle1-runtime = Runtime 6be970633cc82ab412428151e6bf42f3e7fc3081 and /home/user/work/wt/app-bundle1-agent = Agent tl/agt-m2-bundle1-pin 3bf9e5368a956ef562c77e1beb0a745addf23daf (tree b6e56b9f == prepared tested tree). Please move both from hub/escalations/ to closed once synced.

## Infra changes made
- Two worktrees above (mirrors' integration branches untouched: runtime 9f9b25c, agent fc324e83). Isolated read-only vitest run of 2 test files in /home/user/work/app (no file edits). STATUS.md note appended. .lead-last-seen updated. No bin/ patches, no test cancelled/requeued.

## Open blockers and attempted fixes
- None infrastructural. Memory pressure from concurrent tsc is the one risk: worker typechecks serialized by manager (flock + 4 GB). Worker count dipped below 5 as batch workers finished while briefs were being written; watching.
- Dependencies (not lead-owned): Agent bundle1 pin worker commit landed (3bf9e53); App label browser qualification brief written; popup bundle #2 contracts pending on Agent.

## Questions for the orchestrator
- M1 record: is "6 baseline + 3 load-flaky nodes, isolated PASS" acceptable as 0 new for M1, or rerun at low load? (escalation app-20261020T0032Z-lead-m1-final-full-classification)
- Carried forward (low priority): commit a root .gitattributes line 'hub/design/*.md merge=union' on origin/main (kit hub-sync's fallback 'merge -X theirs' can drop another machine's appended section; this clone has the rule only in .git/info/attributes). Not acknowledged yet.

## Lead 00:36Z: final full addendum
- Independent isolated rerun by the lead: app-targeted-1020003017-9364 on the same tree dd1fe6a7 (integration:app), PublicAstridSite.lifecycle + EmptyWorkspaceGuidance: PASS 16/16 in 11s (--maxWorkers=2). This matches the check-in's 16/16 at --maxWorkers=1. Neither file changed since 60aa26b95.
- 9530 status=error was caused by the lead's disk cleanup at ~00:22Z, which recycled its worker worktree while the run was queued. The worktree is restored, and auto-recycle now skips any worker with a queued or running test. 9530's cache key equals 24066's, so 24066 is the result for that tree.

## Lead 01:20Z: app machine container restart (~01:15Z), recovered
- A container restart killed all processes mid-run, including the quiet-window M1 retry app-full-m1-bounded-integration-1020003328-12729 (started 00:33Z). That run is marked status=error, summary INTERRUPTED (not a test result); its log is kept.
- Recovered by 01:18Z: dispatcher, hub-syncd, App manager (Codex gpt-6.1-sol high, round 20261020T0118Z) and lead watcher restarted. Disk, repos, venvs and Codex login were all intact.
- The ONE bounded retry was requeued on the same final tree dd1fe6a7 (integration 2bfde69ea): app-full-m1-bounded-integration-1020011705-2755 (running since 01:17Z, maxWorkers=2). The quiet window is enforced again (other heavy jobs paused or held, no installs). Peak load and memory will be written to STATUS and here when it ends.
