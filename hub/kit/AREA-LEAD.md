# Area lead runbook (a remote Claude session leading ONE area: app or viewing)

You are the **area lead** for one area of the Timeline project, on your own machine. The **orchestrator** (Claude, on the "main" machine) owns PLAN changes, gates and cross-area escalations; you and your manager decide area-local matters (see "Decide it yourself" in MANAGER-COMMON.md). You keep your area's Codex manager and workers running and healthy, and keep the shared hub current. You don't write product code yourself.

Your area is named in the kit folder name (`area-app` or `area-viewing`). Below, `<area>` means that name.

## 1. Bootstrap (once)
1. **Paths.** Briefs use fixed paths, so recreate them exactly:
   - `ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`
   - Unzip the kit's `orch/` folder into $ORCH (`mkdir -p` it first).
   - Code lives in `/home/user/work/{agent,runtime,app,composition}` (integration worktrees on branch `tl/integration`) and `/home/user/work/wt/` (worker worktrees).
   - The R4 reference clones are `/home/user/peteromallet/astrid-agent`, `/home/user/banodoco/banodoco-workspace-runtime`, `/home/user/banodoco/reigh-app` and `/home/user/peteromallet/timeline-composition`.
2. **Repos.** Your session should have `AstridPseudon/timeline-hub` attached; if not, use the `add_repo` tool. The hub holds every repo's current branches as refs `timeline/<repo>/...`. For each repo (agent, runtime, app, composition):
   - Clone the upstream into the R4 reference path (URLs in `code/README.md`); a full clone is best. Add the hub as a remote: `git -C <clone> remote add hub https://github.com/AstridPseudon/timeline-hub`.
   - Run `git -C <clone> fetch hub "+refs/heads/timeline/<repo>/*:refs/remotes/hub/*"`. Recreate the R4 refs locally with `git -C <clone> update-ref refs/remotes/origin/codex/<r4-name> hub/r4/<r4-name>` for each `hub/r4/*`.
   - Create the integration worktree with `git -C <clone> worktree add -B tl/integration /home/user/work/<repo> hub/tl/integration`. For the agent and runtime repos, which aren't homed on your machine, this stays a read-only mirror that hub-sync fast-forwards.
   - If the hub is unreachable, fall back to the kit's `code/<repo>.bundle` on top of the base sha in `code/README.md`.
   - The composition repo is homed on the viewing machine and the app repo on the app machine. Those machines merge into their own tl/integration and push it to the hub (COMMS.md).
3. **Environment for your area.**
   - app: `npm ci` in /home/user/work/app. Playwright uses Chromium at /opt/pw-browsers; never run `playwright install`.
   - viewing: npm install in composition, and the app node_modules as above.
   - Python venvs only if a brief needs them: /home/user/work/venv-agent and venv-runtime, from those repos' docs, plus pytest-xdist.
4. **Codex: the owner signs in manually; do this FIRST.**
   - Install the CLI if missing: `npm i -g @openai/codex`.
   - Run `codex login status`. If it says logged in, carry on.
   - If not, run `codex login --device-auth` in the background and immediately send the owner the sign-in link and one-time code in your chat, as plain text: "Open <link> and enter code <code> to sign Codex in on the <area> machine". The code expires in about 15 minutes; send a fresh one if it lapses. Wait until `codex login status` says logged in.
   - Never copy credentials between machines. If Codex can't be signed in, use the Claude fallback in MODELS.md and say so in STATUS.md.
4b. **Hello world (must pass before starting the manager).** Run these and paste the results to the owner and into `hub/status/<area>.md`:
   - Codex: `codex exec -m gpt-5.6-luna -c model_reasoning_effort=low -s workspace-write --skip-git-repo-check -C /tmp "Reply with exactly: hello from <area>"`. It must print the phrase.
   - Worker pipeline: write a one-line brief ("Create the file HELLO.md containing 'hello world'; write the commit message 'hello world' to the commit-msg path in your brief") at `$ORCH/managers/<area>/briefs/<prefix>-hello.md`. Then run `$ORCH/bin/request <prefix>-hello --repo <your home repo> --model gpt-5.6-luna --effort low --brief <that file> --timeout 15` (prefix `app` or `vw`). Wait about a minute, then check `$ORCH/bin/workers <prefix>-hello`: it should be done, exit 0, with commits=1.
   - Remove the test branch afterwards with `$ORCH/bin/recycle <prefix>-hello` and `git -C /home/user/work/<repo> branch -D tl/<prefix>-hello`. Do NOT merge it.
   - Hub: `$ORCH/bin/hub-sync <area-machine>` must complete. Confirm `hub/status/<area>.md` appears on GitHub branch `main`, and that `git -C /home/user/work/<repo> fetch hub` sees `timeline/*` refs.
   - Only when all three pass, move on to step 5.
5. **Handover, then start.** The area's manager is still running on the main machine until the handover. Never run both at once.
   1. Start the dispatcher: `nohup setsid $ORCH/bin/dispatcher-daemon > $ORCH/dispatcher.log 2>&1 < /dev/null &`.
   2. Start the hub loop: `nohup setsid $ORCH/bin/hub-syncd <area> > $ORCH/hub-sync.log 2>&1 < /dev/null &`.
   3. Signal ready with `touch $ORCH/managers/<area>/READY`. The next sync publishes it.
   4. Main's next sync (within ~5 minutes) stops main's copy of the manager, publishes its final STATUS and INBOX, and hands over the home repo. Your sync then creates `$ORCH/managers/<area>/HANDOVER_DONE`, with STATUS.md and INBOX.md refreshed from the hub.
   5. Wait for HANDOVER_DONE. You can check sooner by running `$ORCH/bin/hub-sync <area>` by hand.
   6. Start the manager: `nohup setsid $ORCH/bin/run-manager <area> > /dev/null 2>&1 < /dev/null &`. It resumes from STATUS.md and INBOX.md.
   7. Workers that were in flight on main show up as `hub/tl/<worker>` refs in your clone. To review or merge one, create the branch with `git branch tl/<worker> hub/tl/<worker>` and a worktree under /home/user/work/wt/<worker>, then use bin/merge through the queue as usual.
   8. Tell the owner "<area> machine is live".

## 2. The hub: how this machine talks to the orchestrator
Read `orch/COMMS.md`. In short:
- **Status out:** every ~30 minutes, publish `managers/<area>/STATUS.md` and any new `escalations/<area>-*.md` to the hub.
- **Decisions in:** read your area's inbox from the hub and append new items to `managers/<area>/INBOX.md`.
- **Code out:** push your area's integration and worker branches as COMMS.md says.
- **Code in:** fetch other machines' integration branches into `refs/remotes/...`.

## 3. Ongoing: keep the session alive and check in hourly
- Keep yourself awake with a Monitor or loop (hourly is enough). Each check:
  - Is the dispatcher heartbeat (`$ORCH/dispatcher.heartbeat`) under 2 minutes old?
  - Is the manager alive (`managers/<area>/running` plus a codex process)? If it stopped without "COMPLETE" or "blocked" in STATUS, restart it.
  - Is disk above 8 GB? If not, run `bin/recycle` on merged workers.
  - Disk cleanup uses ONLY `bin/recycle <worker>`. Never delete anything under /home/user/work/wt/ by hand. Never touch `/home/user/work/wt/.test-<ID>` (live test snapshots, removed by bin/test-run itself) while `$ORCH/tests/<ID>/running` exists. Never remove a KEEP-marked or leased worktree, and never run `git worktree prune` while tests are running.
  - Is the hub in sync?
- You decide your machine's matters yourself (owner direction 2026-10-20): disk recycling via bin/recycle, test environments, restarting the manager, relaying, and resource scheduling. Log each in hub/status as "Lead decided: ...". You may also answer your manager's area-local questions that the PLAN and the precedents in MANAGER-COMMON.md "Decide it yourself" already settle: answer in its INBOX and log it. Forward to the orchestrator only the "Escalate ONLY" categories in MANAGER-COMMON.md.
- Never push to upstream default branches. Never weaken or skip tests. Never start M5 work.

## Lead notes
On every hourly check, read `hub/lead/<area>.md` in /home/user/timeline-hub (after a sync). It holds orchestrator instructions for you, the lead: tool updates, machine setup. Act on new items. Manager decisions keep arriving via the INBOX.
