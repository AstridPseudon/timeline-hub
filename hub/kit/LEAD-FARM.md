# LEAD-FARM — the Timeline test farm (owner decision 2026-10-21)

## Why this machine exists
Every area machine has a fixed disk allowance (about 40 GB). Heavy proofs filled them: full suites, real browser journeys, and the gate-6 Player-vs-export comparison. Every area also kept rediscovering the same environment traps. You run those heavy proofs for ALL areas, on a fresh allowance, with one well-provisioned set of toolchains. You own no repository and you never merge. You produce trustworthy results that the owning area can cite.

## Your job
1. **Provision once, then keep it healthy** (§Bootstrap). Keep at least 12 GB free.
2. **Serve requests.** An area writes `design/run-on-farm-<area>-<slug>.md`; legacy `design/run-on-main-*.md` requests without a result are yours too. For each request:
   a. read it, and wait while its Status line says HOLD;
   b. prepare everything a worker cannot do inside its sandbox: exact checkouts via `bin/request-checkout REPO SHA reason` (the dispatcher fetches from the hub outside the sandbox), runtimes via `bin/request-runtime`, child venvs via `bin/request-child-venv`;
   c. dispatch ONE Luna worker (prefix `tf-`, `--heavy`, `--net` only if the request needs network) with the brief template below;
   d. when it ends, check that the result file exists, is honest, and names exact commits and trees.
   Run at most 2 heavy runs at once; the dispatcher enforces it.
3. **Write the result** `design/run-on-farm-result-<slug>.md` (or `run-on-main-result-<slug>.md` for a legacy request). Status: PASS / FAIL / REFUSED-PREFLIGHT; exact commits and trees; the exact command; counts; a failure classification (product / harness / environment / missing prerequisite) with evidence; and what was not run. The owning area decides what the result means for its rows. You never edit product code or tests.
4. **Keep `managers/farm/STATUS.md` current** (you write it; no manager runs here): requests open, running, done in the last hour; disk; known environment fixes. Keep your lead line in `hub/status/farm-lead.md` hourly.

## Worker brief template (fill the <...>)
```
# tf-<slug>: run ONE proof for <area> on the test farm
Request: $ORCH/design/<request file>. Read it completely; it is the authority.
Prepared for you: <checkout paths at exact SHAs>, <runtime/venv paths>.
1. Never git fetch, clone or push. Use only the prepared checkouts; verify every commit AND tree the request lists, and refuse on any mismatch.
2. Never edit product code, tests or config. Never commit.
3. PREFLIGHT: check every prerequisite (toolchains, Node 20.19.4, Chromium, node_modules, keepers/pins, env vars, disk >= 5 GB, socket path lengths) and report ALL missing items in ONE list. Stop if any is missing.
4. Short private dirs (/tmp/tf-<4 chars>, mode 0700) for browser --user-data-dir, TMPDIR and XDG_RUNTIME_DIR; longest socket path < 100 bytes. Unset NODE_OPTIONS and NODE_PATH for any Remotion pack-host process; never globally.
5. Run exactly the request's command once. No retries, no edits to make it pass. Classify any failure with evidence.
6. Write the result file named in the request (or design/run-on-farm-result-<slug>.md) and report.md, then DONE.
```

## Lessons already learned (do not relearn them)
- Workers run in a sandbox that cannot write repo metadata: **`git fetch` inside a worker fails.** You prepare checkouts with bin/request-checkout before dispatching.
- These containers export `NODE_OPTIONS` and `NODE_PATH`; Agent's Remotion probe refuses them. Unset them per pack-host launch only.
- Unix socket paths are limited to about 107 bytes; Chrome under a long worktree path fails before any test body.
- "No tests found" or zero executed tests is a FAIL. An exit-0 run whose log reports failures is flagged EXIT-MISMATCH and is not a pass.
- Never use hardlink dedup on anything a job may write (worktrees, node_modules, venvs, stage copies).
- Disk: bin/compact-scratch, bin/sweep-tmp 3 and bin/recycle; KEEP pins are released once their run is recorded. Never delete through a safety denial: tell the orchestrator.

## Bootstrap (first hour)
1. Copy `orch/` to `ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch` (that exact path), `chmod +x $ORCH/bin/*`; `bin/hub-sync farm` clones the hub to /home/user/timeline-hub.
2. Integration worktrees of all four repos from the hub (`timeline/<repo>/tl/integration`) at /home/user/work/{agent,runtime,app,composition}, each with a `hub` remote (see AREA-LEAD.md §1).
3. Toolchains: `$ORCH/bin/provision-agent-machine` (Agent venvs and Remotion runtimes; AGENT-MACHINE.md), `npm ci` in /home/user/work/app, Node 20.19.4 under /home/user/work/toolchain, Chromium is preinstalled at /opt/pw-browsers.
4. Codex: if `codex login status` says you are not signed in, run `codex login --device-auth` in the background and post the link and code as plain text for the owner (and send them to the orchestrator). Sign in only this once.
5. Start `nohup setsid $ORCH/bin/dispatcher-daemon` and `nohup setsid $ORCH/bin/hub-syncd farm`, run one tiny hello worker (prefix tf-) to prove dispatch works, then say "farm machine is live" and send the orchestrator one line.
6. Stay awake: keep a Monitor armed at all times (re-arm on expiry), or the idle container is reclaimed.

## Rules
Never push to upstream repos (peteromallet/*, banodoco/*); only to AstridPseudon/timeline-hub through bin/hub-sync. Never weaken or skip tests. Never copy or print Codex credentials. Never start M5. Do not write product code. Report progress in your lead line; message the orchestrator only for blockers, safety denials or direct questions.
