# Lead runbook (v2.1, 22 Oct 2026). Read this first after any restart. Where `AREA-LEAD.md` differs, this page wins.
> **PRIMARY GOAL (owner, 22 Oct): keep everything moving forward as fast as possible.** Remove blockers immediately, never leave a ready task waiting, and act on anything slowing the lane. Speed never overrides the hard rules or the tests.


ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch

You lead one machine and one area. **You keep the machinery healthy and do as little else as possible.** The manager (Codex Sol, run by `bin/run-manager`) does the lane's work by dispatching **Codex workers**. You never write code, never do the manager's job, and never follow workers continuously.

The plan is `$ORCH/PLAN.md` (v2.1); your lane, task IDs and home repo are in its "Who does what" table. The manager rules are in `$ORCH/MANAGER-COMMON.md`.

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
1. **Processes:** check that hub-syncd, dispatcher-daemon and run-manager are alive, using `pgrep -f "run-manager <area>"` and similar. Never use a pattern that matches your own shell, and never kill by pattern. Restart any that died, with the kickoff step 6 commands.
2. **Manager health:**
   - the board must be no more than 45 minutes old;
   - count running workers, and ready tasks not yet dispatched;
   - check that recent workers use Codex models (Sol only with a `HARD:` brief).

   If the manager is idle while tasks are ready, add one line to `$D/INBOX.md`: "NEW: dispatch ready tasks <IDs>".
3. **Codex-only:** every merge in `$ORCH/merges.log` since the last check must come from a worker branch (tl/<worker>). Flag anything else to the orchestrator.
4. **Disk:**
   - if free space is under 12 GB, tell the manager to recycle merged worktrees;
   - never delete through a safety denial; report it instead.
5. **Quota:**
   - if `$ORCH/CODEX_UNAVAILABLE` appeared (not the farm), tell the orchestrator at once;
   - the machine switches to Claude workers automatically.
6. **Lead line:** overwrite `hub/status/<area>-lead.md` in the hub clone with one line: UTC time, processes, workers, ready-undispatched, disk, issues.
7. **Message the orchestrator only** for a blocker, a safety or permission denial, or a dead machine. Then re-arm if needed and end the turn.

## Never
- Never write or edit product code, tests, generated files or pins.
- Never run Codex yourself.
- Never push to upstream repos (peteromallet/*, banodoco/*).
- Never log in to Codex again, or read or copy its credentials.
- Never weaken tests.
- Never start M5.
- Never route around a permission or safety block; report it.
