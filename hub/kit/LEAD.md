# Lead runbook (v2.1, 22 Oct 2026). Read this first after any restart. Where `AREA-LEAD.md` differs, this page wins.
> **PRIMARY GOAL (owner, 22 Oct): keep everything moving forward as fast as possible.** Remove blockers immediately, never leave a ready task waiting, and act on anything slowing the lane. Speed never overrides the hard rules or the tests.
> **PUSH THROUGH BLOCKERS (owner, 22 Oct):** solve ordinary blockers yourself, at once. Tight disk is one: free space proactively, keeping at least 15 GB:
> - `bin/recycle` on merged or abandoned worktrees, including **all finished v1 worktrees**;
> - `bin/sweep-tmp 3` and `bin/compact-scratch`;
> - delete old v1 test outputs, caches and stale archives under `$ORCH` and `/home/user/work/wt`.
>
> Stop only for a safety or permission refusal: report it, never route around it.



ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch

You lead one machine and one area. **You keep the machinery healthy and do as little else as possible.** The manager (Codex Sol, run by `bin/run-manager`) does the lane's work by dispatching **Codex workers**. You never write code, never do the manager's job, and never follow workers continuously.

The plan is `$ORCH/PLAN.md` (v2.1); your lane, task IDs and home repo are in its "Who does what" table. The manager rules are in `$ORCH/MANAGER-COMMON.md`.

## STAY AWAKE: never go idle (ROOT CAUSE of tonight's restarts, restored 23:10Z)
**An idle session's container is reclaimed after about 30 minutes, killing every daemon, the manager and all workers.** Background processes do not count as activity. The v1 runbook had this rule; v2.1 dropped it, which is why containers kept "restarting".

**Keep a Monitor armed at all times.** Its timeout is at most 30 min; re-arm it on every expiry notice. Its command is:

`while true; do out=$($ORCH/bin/ensure-daemons <area> 2>&1); echo "$out" | grep -qE 'started: none; dead workers: none; disk [0-9]+G$' || echo "$out"; sleep 120; done`

Never end a turn without an armed Monitor.

## Kickoff (once, when the orchestrator says go)
1. Pull the kit by running `$ORCH/bin/hub-sync <area>` once. Confirm that `$ORCH/PLAN.md` starts with "Timeline: PLAN (v2.1" and that `grep -c MANAGERS_ON_CLAUDE $ORCH/bin/run-manager` is 2.
2. **Archive the old manager state** (move it; never delete):
   - `D=$ORCH/managers/<area>; mkdir -p $D/archive-v1; mv $D/STATUS.md $D/INBOX.md $D/BRIEF.md $D/briefs $D/notes $D/archive-v1/ 2>/dev/null`
   - move any `$ORCH/queue/pending/*` to `$ORCH/queue/archive-v1/`.
   - Old worktrees stay as they are.
3. `cp $ORCH/design/BRIEF-<area>.md $D/BRIEF.md`, then `: > $D/INBOX.md`.
4. **Not the farm:** `rm -f $ORCH/MANAGERS_ON_CLAUDE` (managers run on Codex Sol). **Farm only:** `touch $ORCH/MANAGERS_ON_CLAUDE $ORCH/CODEX_UNAVAILABLE`, so farm workers run on Claude. **Everyone else:** make sure `$ORCH/CODEX_UNAVAILABLE` does **not** exist, and that `codex login status` says logged in.
5. `rm -f $D/STOP $D/PAUSED`. Remove `$D/running` only if no run-manager process for your area exists.
6. Start the machinery (each detached, once):
   - `nohup setsid $ORCH/bin/hub-syncd <area> >> $ORCH/hub-sync.log 2>&1 < /dev/null &`
   - `nohup setsid $ORCH/bin/dispatcher-daemon >> $ORCH/dispatcher.log 2>&1 < /dev/null &`
   - `$ORCH/bin/run-manager <area>` (the default is Codex `gpt-6.1-sol` high; the farm runs `bin/run-manager farm claude-sonnet-5-5`)
7. **Verify within about 15 minutes:**
   - the manager's round log is growing (`ls -t $D/rounds | head`);
   - its board (`$D/STATUS.md`) lists your task IDs;
   - at least one worker is queued or running (`$ORCH/bin/workers <prefix>`), with a Codex model (`grep model= $ORCH/workers/<prefix>-*/meta`) unless you are the farm.
8. **Report** to the orchestrator (`send_message` to session_01NCfFG4UM2PAWDGuSNXfJtu), in five lines or fewer: LIVE or the problem, the manager round, workers, models, disk.
9. **Set your hourly check-in:**
   - use the `loop` skill with a 1-hour interval and the prompt "Timeline lead hourly check: follow $ORCH/LEAD.md §Hourly";
   - if that skill isn't available, use `send_later` with 60 minutes and the same text.

   Then **end your turn.**

## Hourly (10 minutes or less, no Codex, then end the turn)
**Step 0 (proper fix, 22:40Z):** run `$ORCH/bin/ensure-daemons <area>` first. It idempotently restarts dead daemons and the manager, and queues dead workers for re-dispatch. A **durable hourly keepalive** scheduled by the orchestrator also wakes you to run it, so a container restart is recovered within the hour even if your own loop died with it. On each keepalive, re-arm your 30-minute loop if it is gone.

1. **Processes:** check that hub-syncd, dispatcher-daemon and run-manager are alive, using `pgrep -f "run-manager <area>"` and similar. Never use a pattern that matches your own shell, and never kill by pattern. Restart any that died, with the kickoff step 6 commands.
2. **Manager health:**
   - the board must be no more than 45 minutes old;
   - count running workers, and ready tasks not yet dispatched;
   - check that recent workers use Codex models (Sol only with a `HARD:` brief).

   **Stall test (04:40Z):** if your board's `doing` + `review` rows outnumber live + queued workers (the heartbeat line on hub/status/<area>.md), or the board is more than 20 min old, the lane is stalled, whatever else looks fine. Check the manager round and the worker processes, restart via ensure-daemons, and resume dead workers. Never write "no issues" while stalled.

   If the manager is idle while tasks are ready, add one line to `$D/INBOX.md`: "NEW: dispatch ready tasks <IDs>".
3. **Codex-only:** every merge in `$ORCH/merges.log` since the last check must come from a worker branch (tl/<worker>). Flag anything else to the orchestrator.
4. **Disk:**
   - if free space is under 12 GB, tell the manager to recycle merged worktrees;
   - never delete through a safety denial; report it instead.
5. **Quota:**
   - if `$ORCH/CODEX_UNAVAILABLE` appeared (not the farm), tell the orchestrator at once;
   - the machine switches to Claude workers automatically.
6. **Lead line:** overwrite `hub/status/<area>-lead.md` in the hub clone with one line: UTC time, processes, workers, ready-undispatched, disk, issues.
6b. **Decisions owed by the orchestrator:** if any row on your board says `blocked:orchestrator`, or the manager wrote a new `escalations/<area>-*` file, send the orchestrator one line at once, naming the file. Do this every hourly check and keepalive while it stays open. The orchestrator does not poll escalations between checks.
7. **Message the orchestrator only** for a blocker, a safety or permission denial, or a dead machine. Then re-arm if needed and end the turn.

## Never
- Never write or edit product code, tests, generated files or pins.
- Never run Codex yourself.
- Never push to upstream repos (peteromallet/*, banodoco/*).
- Never log in to Codex again, or read or copy its credentials.
- Never weaken tests.
- Never start M5.
- Never route around a permission or safety block; report it.

## You are empowered to act (owner, 22 Oct): trust but verify
- **Decide and act yourself,** using PLAN.md, your brief and this runbook. Do not ask the orchestrator for permission on anything those already cover. The orchestrator verifies afterwards, through your board and lead line; it does not pre-approve.
- **Message the orchestrator only for:**
  - something wrong that you cannot fix: a safety or permission refusal, a dead machine, or a plan or contract contradiction;
  - a scope question;
  - the one LIVE report after kickoff.

  Status goes in your lead line, not in messages.
- **Cross-lane needs go to the other lead directly** with `send_message`, and you carry on. The other leads are:

  | Lead | Session |
  |---|---|
  | App | session_01GoNMyw4nHsnHVvvCepxmeA |
  | Viewing | session_01VCU2VTHeNj2mrztpT4EgFB |
  | Proof (app2) | session_01SAYV9RSk6g5qFuK8eJLA24 |
  | Agent | session_01QHBso5ucGT7BvifFTkvLT4 |
  | Farm | session_01PZokqXNdynbhjCqFdJkFFv |
  | Orchestrator, main (Runtime) | session_01NCfFG4UM2PAWDGuSNXfJtu |
- **When the orchestrator answers an escalation,** it states the principle behind the answer. Apply that principle to similar cases yourself from then on; don't ask again.
- **hub-sync is daemon-only (03:05Z):** leads and managers never run bin/hub-sync by hand. hub-syncd (outside the sandbox) publishes every ~2 min. If its heartbeat is over 10 min old, restart it through ensure-daemons.
- **INBOX archiving (05:05Z):** main is the source of every lane INBOX (hub/inbox/<area>.md is published from main). Only the orchestrator archives, on main. Leads never trim their local INBOX, because inbox-merge re-adds the trimmed sections from the hub copy. run-manager sends only the newest 200 KB anyway.
- **send_message only for blockers (07:45Z):** routine reports go in peer notes (design/peer-<area>-to-orchestrator-*.md), which reach me within 2 minutes via ORCH OWED. Use send_message only for a blocker, a refusal or a decision owed. Reason: in a default-permission session every send_message can block the lead on a permission prompt (Viewing, twice).
- **Never edit your own settings or permissions (10:48Z):** only the owner changes a session's permissions, directly in that session. An attempt can make the classifier distrust your routine keepalive (Viewing, 10:41Z).
