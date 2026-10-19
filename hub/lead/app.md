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
