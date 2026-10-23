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
- **H9 (06:43Z):** P5 DONE and P4 partial (1 of 5 proofs). 105 of 142 rows merged. ETA 10:00–16:00Z on 24 Oct, so per the cut order **V4 is CUT**. **G4 DONE, and the R5 gate is A3 only.** App's machine is reclaimed hourly (keep-awake denied, owner to-do #1); the Proof lane may author App-repo rows as failover.
MERGE-ONLY lanes: app   (07:20Z: App's container is reclaimed within ~30 min of each wake. App merges only; app2 authors App product rows as failover. Remove when the owner allows App's keep-awake.)
- **Upstream drift (09:40Z):** Runtime upstream is now a98fbc2f9 (macOS CI fixes plus a skip registry; 3 conflicts) → U1b dispatched. Agent upstream is now 74f3f7edb (the same no-invisible-skips policy, 93 files) → U2b dispatched (10:03Z). App and Composition are unchanged. **12:46Z:** App upstream is now 6e3445ee9 and Runtime 6162e0e33, both tests/CI only, so per the upstream rule they're DEFERRED. **15:13Z (farm ZIP rehearsal):** App live efe83c77e has 7 conflicts against integration; Runtime live f23d1e43f overlaps in 5 files; Composition applies cleanly. The freeze-time U-tasks will need Sol.
- **GATE CRITERIA (09:44Z; machine-checkable, so act the moment a criterion is true, without waiting for a header line):**
  - **A3 DONE** = App integration contains the A3-shared and A3-child-placement merges (including the JSON fix 0b6b), and the joint A2/A3 integrated qualification passes. → **R5 merges at once.**
  - **P1 GO** = the ORIGINAL mounted P1 chain (split → trim new ID → intervening Agent edit → lost ack → restart, covering accepted, merged and refused) passes on the integrated App + Agent + Runtime heads, with the independent no-weakening review PASS. → **A4 and G5 (except the D17 duplicate writer) merge at once.**
  - **P2/P3** run as soon as A2-undo and A2-move-reads are merged in App integration.
- **10:40Z: R5 DONE**: old save routes are rejected, with an integrated proof (original 20 + legacy 80). U1b (Runtime upstream) is merged. P2 and P3 are running. The farm is live: App full suite run, 50 real failures sent to App.
- **11:41Z: P4 DONE** (single, ten-notes, restart, show/history, conflict, rerun): 2 of 5 proofs pass. 25 merges in the last hour. App has held 78 min with the keep-awake.
- **H18 (15:44Z):** P4 and P5 DONE. P1 runs end to end (2 known fails, D24). P2 and P3 wait on the Runtime atomic-birth guard fix (Sol). App full suite PASS 18,819. ETA about 19:00Z on 24 Oct. Upstream: App efe83c77e (7 conflicts; U3b-draft on a branch); Runtime aa6c5b0cb (deferred).
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
- **D16, earlier refusal (06:22Z):** when v2 refuses earlier than v1 for the same protected property, adapt the test to the earlier refusal and keep all its assertions. Get an independent no-weakening review, and list it as a behaviour change. Defer like D14 only when v2 can't provide the behaviour at all.
- **Conflict-free merge-forward (06:43Z):** when a merge-forward has no conflicts and the worker's own diff is unchanged, the targeted integrated re-run is enough; no new independent review is needed. This ends port/join/review churn.
- **Failover authoring (06:43Z):** when a lane's machine is unavailable, a healthy lane that already merges into that repo may author its rows from that repo's current integration. The repo owner merges. Whoever dispatches first owns the row.
- **D17, cross-timeline duplicate (08:39Z):** in scope, as a writer migration. One Agent semantic command (Sol), with Runtime verifying source authority, on the existing carrier. G5 deletes the old duplicate writer only after the two original duplicate tests pass on the new command.
- **Stacked reviewed merges (09:44Z):** a merge request may carry several stacked commits, but only if EACH commit has its own independent PASS and none comes from unreviewed ancestry. List each commit with its review ID. This lets a lane with short wake windows (App) clear its whole queue in one wake.
- **Row discipline (09:44Z):** add new rows only for critical-path or gate items, or real regressions found by full suites. Anything else goes to a 'later' list on your board, not a row. Rows grew faster than they closed (142 → 204).
- **Host scripts are lead-only (09:44Z):** workers never run ensure-daemons, run-manager, hub-sync or dispatcher tools. ensure-daemons now refuses inside a worker sandbox.
- **D18, product guard vs harness (10:40Z):** a product validation error that refuses our test harness's setup is a harness defect. Fix the harness invocation and never the guard. 'Hard safety refusal' means the tool harness or the auto-mode classifier refused an action.
- **Fresh clones and delivery builds (11:41Z):** a fresh clone for a dry run or delivery build lives in the worker's tmpdir (harness-cleaned), never in evidence/ or notes/; keep only reports, logs and patches. **The final delivery build runs on the farm** (21 GB free), not main (8–10 GB). A 1.4 GB dry-run clone had pushed main to its floor.
- **D21, harness vs proof (12:46Z):** benches are provisioned by the dispatcher (request-child-venv, request-runtime, request-checkout). Every gate run starts with a report-all preflight. Harness-only changes with a hash-locked identical test body need no independent review.
- **Upstream rule (12:46Z):** defer by default. Merge early only for gate paths, a failure we're hitting, or a security fix; never while an exact-pin proof on that repo is pending. Everything else goes in one U-task per repo at the freeze.
- **D19/D22, full suites live with their lane (13:33Z):** a lane's own full suites run on that lane's test service, with its own checkout and venv requests. The farm runs only what its workers' permissions allow (Composition, P2/P3 heavy on request, the final delivery build). Farm permission denials are never worked around.
- **Kit changes ($ORCH/bin, distributed to every machine) (13:39Z):** Codex-authored, independently reviewed and smoke-tested. Installed atomically (.new then mv), never while that script is running. Keep the predecessor as <script>.<UTC>.bak for rollback. Add one line to the Runtime board's Blockers ('KIT CHANGE: <script> <sha> <why>') so the orchestrator sees it. Never weaken a guard in ensure-daemons, run-manager or hub-sync without an orchestrator OK.
- **D23, child-word anchors (14:08Z):** deferred as relational timing (PLAN §1), the D14 pattern. The test stays unchanged and visibly failing, and is listed as deferred. G5 may retire the SDK publisher at P1 GO. Owner question bundled with D14.
- **D24, P1 ownership (15:44Z):** line 824 is a test expectation (the stronger toEqual fix goes ahead under review). App stops its contradicting clear-fix 1534. App owns the missing-POST diagnosis (Sol). Then one P1 rerun.
- **D21a, bench lifecycle (16:49Z):** REUSE the bench for the same tuple across reruns; build a new one only when the tuple changes. When a tuple is superseded, retire its bench venvs with `bin/request-retire-venv NAME` (installed 16:49Z; the dispatcher refuses anything referenced, live or under an hour old). Never chmod or delete benches by hand.
- **D21b, bench keys and disk routing (17:51Z):** each bench component is keyed by what it depends on (Remotion runtime = Agent remotion/ tree hash; child venv = Agent SHA plus Runtime client), and reused when unchanged. A lane at its disk stop line hands gate RUNS to a machine with disk (currently the farm). The owning lane keeps authoring and the GO verdict.
- **D21c (18:41Z):** the child bench is keyed by Agent SHA + backend SHA + client tuple; the Remotion runtime by the remotion/ tree hash only.
- **Scratch location (18:41Z):** all scratch, fixtures and fixture venvs go in $TMPDIR (harness-cleaned). Worker folders hold under 50 MB (COMMON.md).
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
- **Disk floor by machine (01:40Z):** the floor is 15 GB where it's reachable. On **main** it's 8 GB, because about 30 of main's 40 GB is fixed repos and venvs. Above the floor, disk is not a blocker; spend no worker time on it. **CLARIFIED 15:08Z: floors are cleanup TARGETS, never stop lines.** Below the target, keep working and clean up opportunistically. Stop starting new heavy runs only below **8 GB** free on any machine. Never stop a proof gate for a target.
