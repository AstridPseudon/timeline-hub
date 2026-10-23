# BOARD HEADER (orchestrator only), Timeline v2.1
> **PRIMARY GOAL (owner, 22 Oct): keep everything moving forward as fast as possible.** Remove blockers immediately, never leave a ready task waiting, and act on anything slowing the lane. Speed never overrides the hard rules or the tests.


Clock: **H0 = 2026-10-22T21:40Z** (H3 = 00:40Z, H6 = 03:40Z, H9 = 06:40Z). Plan: `$ORCH/PLAN.md` v2.1. Lanes and IDs are in PLAN's "Who does what" table.

## Status
- C0 contract: **C0 APPROVED** (22:15Z). **C0b APPROVED** (22:45Z), covering `steps[].reads` and the provider effect records; see design/astra-c0b-review.md. **C0c APPROVED** (23:55Z, Astra: no blocking issues; see design/astra-c0c-review.md). The contract is complete: merge C0c, then R2 may merge. The principle is adopted now: *every root address resolves to exactly one physical closure image at its evaluation boundary; entity IDs are aliases.* `parent` and the unambiguous addresses are unchanged. `internal:<timeline_id>` and `shot:<shot_id>` are allowed only when they resolve to exactly one root; multiple matches are refused with `ambiguous_ref`, never selected or broadcast. There is an explicit `internal-revision:<revision_id>` form. Resolved bindings are persisted and aliases normalized before overlap checks. Successors are followed only through authenticated provenance, and an alias is never silently retargeted. **R2 may start now** against C0b plus this principle; **R2 merges only after C0c is approved.**
- H3 go/no-go (P1): pending.
- H8 scope check: pending.

## Decisions in force
- Owner, 22 Oct:
  - hybrid design (PLAN §1);
  - leads and orchestrator on Claude doing minimal work; managers on Codex Sol; all code, reviews and merges on Codex;
  - Sol only for the tasks marked Sol;
  - gate 6 parity deferred (signed);
  - WC8-style stale working copies refused;
  - upstream freeze before the final merge.
- **Build on our integration branches.** Upstream main is merged into them (U1–U3), never rebased. The App takes upstream's editor files (U3b), but keeps the outbox, the commit transport and the Runtime client.

## Cut list (in order, only if behind)
1. V4
2. push / dashboard extras

**Never cut** writer migrations or tests of promised behaviour.

## Farm schedule
- H0: upstream baselines.
- H6, H9: integrated full suites, the tour and the journey.
- Final.

## Principles from answered escalations (apply them yourself; at most 10 lines)
- **Owner's direct approval:** it has been given in each lead's session for the v2.1 kickoff and for freeing disk to at least 15 GB. Operational instructions from the orchestrator carry the owner's authority. Safety and permission refusals still stop you.
- **v1 leftovers:** v1 pin worktrees (KEEP), dirty v1 worktrees and other v1-only artifacts (private13 graphs, v1 suite scratch dirs, LEASE=READY v1 trees) are abandoned under v2.1. Remove v1 lines from suites.conf too. When disk is needed, release them yourself: check no running process or test uses the path, remove the KEEP marker, then run `bin/recycle`. For a dirty worktree, first keep its diff as `git diff > $ORCH/archive-v1/<name>.patch`. No need to ask.
- **Merges inside a worker** (upstream or tl/integration): workers never run git merge or fetch, because their sandbox cannot write git internals. The sanctioned route:
  1. The lead fetches outside the sandbox: `git fetch origin main` and the hub refs.
  2. The **manager** runs `$ORCH/bin/merge-forward <worker> <base>` on that worker's worktree, with base = `origin/main` or `tl/integration`. This leaves the conflicts in the files.
  3. The worker resolves them in the files only.
  4. The harness commits the merge when the worker exits.

  The alternative is dispatching with `--merge-parent <sha>`. Apply this to U2 and U3a–c without asking.
- **Sandbox limits are not safety refusals.** Worker sandboxes cannot open localhost sockets or write git internals; that is by design, with designed routes:
  - tests needing localhost or browsers: the test service (`bin/request-test`), or dispatch with `--net`;
  - merges: `bin/merge-forward`;
  - fetches: the lead, outside the sandbox.

  Only an auto-mode classifier or safety denial stops you.
- **Upstream fetch (intent plus check; adapt the command to your machine's setup):** before any U-task or baseline, make `git rev-parse origin/main` equal the live `git ls-remote <upstream> refs/heads/main`. Machines differ: some repos fetch with a wildcard refspec (fine), main's fetched only a v1 branch (fixed with `config --add remote.origin.fetch '+refs/heads/main:refs/remotes/origin/main'`), and some have no `origin` at all. Upstream URLs: agent https://github.com/peteromallet/astrid-agent, app https://github.com/banodoco/reigh-app, runtime https://github.com/banodoco/banodoco-workspace-runtime, composition https://github.com/peteromallet/timeline-composition. **Every U-task's acceptance includes** `git merge-base --is-ancestor <live tip> HEAD`.
- **Use the live `ls-remote` tip at merge time.** Upstream shas quoted by the orchestrator are snapshots; a newer tip that contains them is correct.
- **Leads who cannot write their own manager INBOX** (harness denial): put the request in your lead line and send the orchestrator one line. The orchestrator delivers it through the hub inbox.
- **Principle on instructions (22:45Z):** orchestrator instructions state an intent and a check. Leads adapt the exact commands to their machine's real setup and report only if the intent can't be met.
- **Schema single source for this build (23:45Z):** `runtime contract/schemas/timeline-config.schema.json` is the single source. The external `@banodoco/timeline-schema` package is not available on our machines and is not needed. V1 edits that file and regenerates every copy from it with the repo tools. Provenance: record the Runtime commit.
- **Start on the branch, merge later:** a task whose dependency is in review may start on that dependency's branch (`--base tl/<dep-worker>`) and merge forward once the dependency merges. Do not wait idle for a merge.
- **Size tasks for restarts (00:00Z):** containers restart about every 35–45 min, even when the session is active, so assume they will. Brief each worker for **about 30 minutes or less of work**: split larger tasks into steps that commit independently, with `--timeout 45`. A killed worker's WIP is committed by ensure-daemons/stop-worker, so resume it with `--base tl/<worker>` and a brief that says "continue from the WIP commit". Run long suites through the test service or the farm, not inside a worker.
