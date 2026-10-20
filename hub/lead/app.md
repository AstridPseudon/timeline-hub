# Orchestrator → app AREA LEAD (read on every hourly check; newest item last)

## 2026-10-19T20:11Z — one-time tool update (do once)
Main now publishes the shared tools and rules in hub/kit/. Run:
`cp /home/user/timeline-hub/hub/kit/bin/* $ORCH/bin/ && chmod +x $ORCH/bin/*`
then restart hub-syncd: `kill $(cat $ORCH/hub-syncd.pid)`, then `nohup setsid $ORCH/bin/hub-syncd app > $ORCH/hub-sync.log 2>&1 < /dev/null &`.
After that, tool and PLAN updates apply automatically each sync. Confirm by adding a line "tool update done <UTC>" to the top of your status (it publishes on the next sync).

## Also for the App lead
The hub has not seen this machine yet: no hub/status/app.READY and no "hub-sync app" commits. Finish the AREA-LEAD steps (hello world, then the READY handshake). Until then the App manager keeps running on main, which is fine.

## 2026-10-19 20:25Z — please apply the tool update now (important)
A main-side App manager kept running after your handover, and both machines merged app-m1-wiring-fix. The contents are identical (tree afb021cf5), so nothing was lost. Main's copy is stopped and aligned to your 430546e42.
Your current hub-sync still force-pushes worker branches you only imported. It overwrote main's app-m1-recovery-basis (dc519fb7f) and app-m1-recovery-compose (436410bcd) with 0f16295c1. The new hub-sync in hub/kit/bin publishes a worker branch only from the machine that ran it. Apply the one-time tool update above, then restart hub-syncd.

## 2026-10-19 20:30Z — ACTION for the App lead: restart hub-syncd now
Your manager copied the new tools at 20:20 but can't restart the daemon from its sandbox. Do it yourself, outside the sandbox: `kill $(cat $ORCH/hub-syncd.pid); nohup setsid $ORCH/bin/hub-syncd app > $ORCH/hub-sync.log 2>&1 < /dev/null &`. Then put "tool update done <UTC>" at the top of your status. Until then, your machine still force-pushes adopted worker branches.

## 2026-10-19 23:30Z — lead: MAX SPEED
The owner wants max throughput. Every 30 minutes, check that your manager keeps 5–7 workers running (heavy cap stays 2). If it's idle without a stated blocker, nudge it, or restart it if it has exited. Use Haiku or Sonnet for chores.

## 2026-10-20 00:10Z — ACTION (lead): check that the final M1 full is healthy
Your manager reports memory pressure (concurrent tsc killed with exit 137). Check the host processes and OOM logs (`dmesg | grep -i -E 'killed process|oom'`) for full run app-m1-draft-opaque-roots-full-source-integration 24066 (running since 23:54; no output since 23:57). If it's alive and progressing, leave it. If it was OOM-killed or is hung, keep its log, mark it failed, and start ONE retry of the same final tree with no other heavy job running alongside. This is the LAST M1 item.

## 2026-10-20 00:15Z — ACTION (lead): bundle #1 candidate checkouts (read-only)
Create isolated READ-ONLY git worktrees on your machine from hub refs, for branch qualification:
- Runtime: `git -C /home/user/work/runtime fetch hub "+refs/heads/timeline/runtime/*:refs/remotes/hub/*" && git -C /home/user/work/runtime worktree add --detach /home/user/work/wt/app-bundle1-runtime 6be970633cc82ab412428151e6bf42f3e7fc3081`
- Agent: once Agent publishes its bundle #1 pin branch (named in design/m2-writer-bundle-1.md), do the same at /home/user/work/wt/app-bundle1-agent, detached at that exact sha.
Make no installs, pushes or integration changes. Use the existing venvs. Tell your manager the paths, through its INBOX.

## 2026-10-20 00:55Z — lead: QUIET WINDOW for the final M1 full retry
Your manager will run ONE bounded full (maxWorkers=2) on the final tree. While it runs (~35 minutes), keep the machine quiet: no other heavy jobs, tsc serialised or paused, no installs. Watch load, and record peak load and memory in STATUS. This is the last M1 gate.
