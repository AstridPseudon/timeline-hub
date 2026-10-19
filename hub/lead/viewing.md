# Orchestrator → viewing AREA LEAD (read on every hourly check; newest item last)

## 2026-10-19T20:11Z — one-time tool update (do once)
Main now publishes the shared tools and rules in hub/kit/. Run:
`cp /home/user/timeline-hub/hub/kit/bin/* $ORCH/bin/ && chmod +x $ORCH/bin/*`
then restart hub-syncd: `kill $(cat $ORCH/hub-syncd.pid)`, then `nohup setsid $ORCH/bin/hub-syncd viewing > $ORCH/hub-sync.log 2>&1 < /dev/null &`.
After that, tool and PLAN updates apply automatically each sync. Confirm by adding a line "tool update done <UTC>" to the top of your status (it publishes on the next sync).

## 2026-10-19 — adopting a worker that finished on main
For vw-m3-agent-package, and any worker that finished on main: when the transferred meta already exists but there's no worktree, recreate one with `git -C <agent clone> worktree add /home/user/work/wt/<w> hub/tl/<w>`, create branch tl/<w> from it, and keep the transferred report. Don't re-run the worker.

## 2026-10-19 20:30Z — optional: an H.264-capable browser for export checks
If you can, install Google Chrome stable (it ships proprietary H.264/AAC codecs) at a separate path, without replacing /opt/pw-browsers. Tell your manager the executable path. If it can't be installed, say so in your status. Not urgent; the main parity route doesn't need it.

## 2026-10-19 22:40Z — infrastructure fix (also sent directly)
Restart the dispatcher from your own shell, outside the sandbox; pid 4 / read-only .git means it's running inside one. Restore the running markers of the 3 live workers that lead-recover wrongly marked 137. Make lead-recover require "no process AND log idle for 10+ minutes" before it marks a worker interrupted.
