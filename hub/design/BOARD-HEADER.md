# BOARD HEADER (orchestrator only), Timeline v2.1
> **PRIMARY GOAL (owner, 22 Oct): keep everything moving forward as fast as possible.** Remove blockers immediately, never leave a ready task waiting, and act on anything slowing the lane. Speed never overrides the hard rules or the tests.


Clock: **H0 = 2026-10-22T21:40Z** (H3 = 00:40Z, H6 = 03:40Z, H9 = 06:40Z). Plan: `$ORCH/PLAN.md` v2.1. Lanes and IDs are in PLAN's "Who does what" table.

## Status
- C0 contract: **C0 APPROVED** (22:15Z). **C0b APPROVED** (22:45Z), covering `steps[].reads` and the provider effect records; see design/astra-c0b-review.md. **C0c APPROVED** (23:55Z, Astra: no blocking issues; see design/astra-c0c-review.md). The contract is complete: merge C0c, then R2 may merge. The principle is adopted now: *every root address resolves to exactly one physical closure image at its evaluation boundary; entity IDs are aliases.* `parent` and the unambiguous addresses are unchanged. `internal:<timeline_id>` and `shot:<shot_id>` are allowed only when they resolve to exactly one root; multiple matches are refused with `ambiguous_ref`, never selected or broadcast. There is an explicit `internal-revision:<revision_id>` form. Resolved bindings are persisted and aliases normalized before overlap checks. Successors are followed only through authenticated provenance, and an alias is never silently retargeted. **R2 may start now** against C0b plus this principle; **R2 merges only after C0c is approved.**
- **Runtime v2 wire PUBLISHED (02:19Z):** R2r merged as runtime 21482a416, integrated PASS 225+24. U4a-v2 and U4p-v2 are now ready, and so is every row that waited on R2r.
- **02:39Z:** U4a-v2 and U4p-v2 are in review; A2 production mount and G2 are in progress. Next on the critical path: A2 mount → P1 re-run → A3/G4 → R5.
- **H6 (03:41Z):** P1–P5: 0 of 5 pass; 10 of 24 plan tasks done; 22 merges in 3 h. ETA 06:00–12:00Z on 24 Oct.
  - **Producer tuple FROZEN at runtime 34eac/ad823 until P1 GO.**
  - The farm is down, so Proof runs P1 and P3 on the test service.
  - R5 is drafted on a branch.
- **H3 go/no-go (P1, 00:40Z): NO-GO (partial).**
  - **PASS:** the R1 real corpus (42 tests on e6f7167d), plus the App provenance and local-save module tests.
  - **NOT proven:** the integrated App chain. Blockers: A2 is not wired into the mounted save path; the v2 DTOs are absent (R0); the rm-f holds (root cause fixed 00:50Z).
  - **Rule:** deletions A4 and G5 stay gated until P1 GO.
  - **Re-run:** the P1 chain runs as soon as App publishes a runnable SHA with the mounted caller.
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

- **D12, no new invalidity (03:23Z):** final validation refuses only declarations the commit creates, modifies or invalidates. Untouched pre-existing unresolvable legacy declarations are preserved and don't block unrelated edits (a diagnostic at most). Contract text: C0d (Runtime).

- **D13, gesture saves declare their reads (03:40Z):** App gestures send the reads they used and merge=fields. Unknown or free transforms stay atomic. Reads never come from byte diffs. Owner: App, row A2-reads.
- **D14, deferred anchor-undo (04:40Z):** the two equal-text anchor-undo positives stay unchanged and visibly failing, listed as deferred (relational timing). There is no C0 change, no skip, and no 54-PASS claim. The owner may fund option (a) later.
- **Merge requests carry only the worker's own commits (04:40Z):** before any request-merge or request-merge-remote, `git log <integration>..tl/<worker>` must show only that worker's commits. A test-only import is a new branch from the target's integration.
- **D15, occurrence.fork (04:58Z):** the per-occurrence fork is a Python semantic command in the Agent provider, owned by Agent (Sol). Prefer the existing carrier, so the 34eac freeze holds. A schema change only if it's unavoidable, then bundled into one tuple. No managed-edge patches and no broadcast.
- **D12a (05:39Z):** D12 covers every new V2 check, including cross-field consistency such as fps parity. A check fires only when the commit writes a field it involves. No epsilon or invented equivalence. Apply it to similar cases yourselves.
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
- **File deletion inside workers (00:15Z):** the automatic review rejects `rm -f`/`rm -rf`-style commands and asks for a safer approach. That approach is:
  - delete named files only inside your own worktree, with the edit tool's delete-file operation (apply_patch "Delete File") or a plain `rm <path>` per file;
  - never `-f` or `-r`, globs or paths outside the worktree;
  - leave temp, cache and build output alone (the harness cleans tmpdir);
  - for npm pack: pack, then `mv` the artifact, with no cache cleanup.

  Held work resumes under this rule. A **repeated** rejection on this approach is a real refusal: stop and escalate.
- **"Done" means wired in (00:15Z):** acceptance always includes the **mounted production caller**, i.e. the real code path a user or agent hits now uses the new code, plus the full v2 DTOs from the contract. A tested but unused module is not done.
- **Peer requests become rows in one pass (01:40Z):** when a PEER MESSAGE in your INBOX asks your lane for a fix, add a board row for it with an owner and a dispatch in your next pass. Don't leave it as INBOX text. The sender checks your board for it.
- **Disk floor by machine (01:40Z):** the floor is 15 GB where it's reachable. On **main** it's 8 GB, because about 30 of main's 40 GB is fixed repos and venvs. Above the floor, disk is not a blocker; spend no worker time on it.
