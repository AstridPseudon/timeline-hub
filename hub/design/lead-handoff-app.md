# App lead handoff (written 2026-10-20 20:35Z). Read $ORCH/LEAD.md first (it is in hub/kit/LEAD.md until it syncs).
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch . I am the App lead; the orchestrator is session_01NCfFG4UM2PAWDGuSNXfJtu (send_message).
The hub is AstridPseudon/timeline-hub (clone /home/user/timeline-hub). Never push to banodoco/* or peteromallet/*. App home repo: /home/user/work/app (upstream fetch is read-only).

## How this machine's daemons run (exact commands; all from /home/user)
- Dispatcher: nohup env PLAYWRIGHT_BROWSERS_PATH=/home/user/work/pw-browsers setsid $ORCH/bin/dispatcher-daemon >> $ORCH/dispatcher.log 2>&1 < /dev/null &
  (the env var points Playwright 1.60 at a symlink shim over the image's chromium 1194; without it browser tests fail). Pid in $ORCH/dispatcher.pid. Now pid 20932 (restarted 01:14Z so it runs the kit READY-refill code).
- hub-syncd: nohup setsid $ORCH/bin/hub-syncd app > $ORCH/hub-sync.log 2>&1 < /dev/null &   (pid 311; every ~5 min; never run bin/hub-sync by hand)
- Manager: rm -f $ORCH/managers/app/running only if no manager process remains, then nohup setsid $ORCH/bin/run-manager app > /dev/null 2>&1 < /dev/null &
  It is a loop with 3 h codex rounds (gpt-6.1-sol high). Restart a stuck round by killing ONLY the `timeout 3h codex exec` pid; the loop starts a fresh round.
  Round pid 9155 since 19:56Z. NEVER count processes with a pattern that also matches your own command line (I skipped a start once that way).
- Container-restart recovery: bash /tmp/claude-0/-home-user-repo/544d0084-45e8-5a60-a8da-0655935c4bb0/scratchpad/lead-recover.sh (marks interrupted workers/tests, restarts all three).
- Watcher: bash .../544d0084-45e8-5a60-a8da-0655935c4bb0/scratchpad/lead-watch.sh (run in the background, timeout 4200000; ends each ~55 min with "TIMEOUT no events"; auto-restarts an idle or <5-worker manager, aborts a stuck hub rebase, alerts on gates). Re-run it when it exits.
- Plus arm a Monitor (max 30 min) printing when a heartbeat is stale, the manager is down, workers <4 or disk <9 GB.
- Hourly check-in: scheduled task trig_01Tgek99pWsLa2AwUoddbQGu at :13, a Sonnet subagent does the checks and overwrites hub/status/app-lead.md. LEAD.md wants the top line `LEAD <UTC> | workers N | disk G | ledger rows DELETED x, in progress y | merges pending z | lead decisions: ...`.

## Rules I learned
- Kit files (bin/, PLAN, rules) are overwritten from hub/kit every sync; never patch them. The permission policy blocks lead edits to shared files under $ORCH (bin/dispatch etc.): ask main to change the kit.
- Never rm under /home/user/work/wt by hand; use bin/recycle under `flock -n /home/user/work/.lead-recycle.lock`; skip KEEP, leased (managers/*/notes/*.lease, *ACTIVE*), queued/running-test worktrees.
- Relay anything the manager has not seen by appending a "## <time> — App lead ..." section to $ORCH/managers/app/INBOX.md (inbox-merge keeps local lead notes).
- Upstream App refresh: lead fetches origin/main read-only; manager merges forward with --merge-parent <sha>; verify ancestry (merge-base --is-ancestor) and compare removed test lines PER FILE (tests move with upstream UI moves, never deleted; I once missed an identity-gating test).

## Watching now (20:35Z)
- App integration a11dd7a91 (20:27Z). Last green full c57dcc261 (1488 files / 19103 pass / 0 actual fail / 3 expected drag). Full on 20ea14c26 (run 1020195758-21398): 19240 pass / FIVE new failures (shotCompositionRuntime popup x3, getProjectVerifiedMedia relay x2); separate fix workers running (app-m2-full20ea-popup-regression-fix); later merges not covered by that full. NOT accepted green.
- Workers: 4 running + 3 dispatch requests pending (target 5-7).
- Milestones: M1 recorded 03:55Z. M2 (writer removal) and M3 open; no M2/M4 record; hard stop NOT YET. Never start M5.
- app2 (ap2-*) merge requests are auto-queued by hub-sync; four stale ones were content-joined in 20ea14c26 and marked SUPERSEDED/MERGED.
- Viewing: 10 PENDING merge requests listed in design/peer-app-to-viewing-20261020T2024Z-pending-merge-requests.md; waiting for Viewing to say SUPERSEDED or still wanted, then I close the superseded ones (move queue/refused -> queue/done with a SUPERSEDED line).
- Agent D10 source deletion merged (f711cbd2); manager should mark the FIRST-OWNER D10 row DELETED (peer note delivered 20:28Z).

## Recent "Lead decided" items (also in hub/status/app-lead.md and lead-manager-restarts.log)
13:52 manager restart (stale STATUS); 15:25 freed disk (idle /tmp copies, finished-worker private copies); 15:33 dispatcher restart for kit STOP/CHECKOUT; 17:18 manager restart; 19:28 queued 4 ap2 merges (refused on conflict); 19:56 manager restart for the 3 h round kit; 20:03 closed the 4 stale ap2 results; 20:24 superseded ap2 carrier request.

## Only I know
- Disk is tight (9.7-11 GB with full suites running); the watcher sweeps below 10 GB. Big consumers: /tmp/app-coherent-deps12 (linked by tests), worker record dirs under $ORCH/workers/*/notes.
- Codex login works on this machine (ChatGPT); no fallback is in use. If it ever needs sign-in, send the owner the device link and code.
- Disk lever found 03:30Z: /root/.codex/sessions holds ~1.6 GB of finished-run transcripts; `find /root/.codex/sessions -name '*.jsonl' -mmin +180 -print0 | nice xargs -0 -n20 gzip -q` frees ~1 GB losslessly (Codex rounds are fresh execs, never resumed; do not touch auth.json or the sqlite files). Also never run bin/sweep-tmp with H<1 (removed live workers' /tmp/tl-* dirs once); the kit tool now enforces 1 h.
