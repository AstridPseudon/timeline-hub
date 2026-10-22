# BOARD HEADER (orchestrator only), Timeline v2.1
> **PRIMARY GOAL (owner, 22 Oct): keep everything moving forward as fast as possible.** Remove blockers immediately, never leave a ready task waiting, and act on anything slowing the lane. Speed never overrides the hard rules or the tests.


Clock: **H0 = 2026-10-22T21:40Z** (H3 = 00:40Z, H6 = 03:40Z, H9 = 06:40Z). Plan: `$ORCH/PLAN.md` v2.1. Lanes and IDs are in PLAN's "Who does what" table.

## Status
- C0 contract: **C0 APPROVED** (22:15Z). **C0b APPROVED** (22:45Z), covering `steps[].reads` and the provider effect records; see design/astra-c0b-review.md. **C0c is pending:** root addressing (Astra 22:44Z). The principle is adopted now: *every root address resolves to exactly one physical closure image at its evaluation boundary; entity IDs are aliases.* `parent` and the unambiguous addresses are unchanged. `internal:<timeline_id>` and `shot:<shot_id>` are allowed only when they resolve to exactly one root; multiple matches are refused with `ambiguous_ref`, never selected or broadcast. There is an explicit `internal-revision:<revision_id>` form. Resolved bindings are persisted and aliases normalized before overlap checks. Successors are followed only through authenticated provenance, and an alias is never silently retargeted. **R2 may start now** against C0b plus this principle; **R2 merges only after C0c is approved.**
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
- **Upstream fetch (ROOT FIX, 22:55Z):** every lead runs this once per repo: `git -C /home/user/work/<repo> config --add remote.origin.fetch '+refs/heads/main:refs/remotes/origin/main'`. The repos were configured to fetch only an old v1 branch, so origin/main stayed stale. That broke U1, and would also have broken refresh-main and delivery-build. After that, a plain `git fetch origin` works. **Every U-task's acceptance includes** `git merge-base --is-ancestor $(git ls-remote origin refs/heads/main | cut -f1) HEAD`.
- **Use the live `ls-remote` tip at merge time.** Upstream shas quoted by the orchestrator are snapshots; a newer tip that contains them is correct.
- **Leads who cannot write their own manager INBOX** (harness denial): put the request in your lead line and send the orchestrator one line. The orchestrator delivers it through the hub inbox.
