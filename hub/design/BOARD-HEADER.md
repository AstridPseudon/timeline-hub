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
MERGE-ONLY lanes: none   (lifted 10:47Z 23 Oct after the keep-awake was allowed. Machine-read by ensure-daemons: list lane names here only when a lane is merge-only.)
- **Upstream drift (09:40Z):** Runtime upstream is now a98fbc2f9 (macOS CI fixes plus a skip registry; 3 conflicts) → U1b dispatched. Agent upstream is now 74f3f7edb (the same no-invisible-skips policy, 93 files) → U2b dispatched (10:03Z). App and Composition are unchanged. **12:46Z:** App upstream is now 6e3445ee9 and Runtime 6162e0e33, both tests/CI only, so per the upstream rule they're DEFERRED. **15:13Z (farm ZIP rehearsal):** App live efe83c77e has 7 conflicts against integration; Runtime live f23d1e43f overlaps in 5 files; Composition applies cleanly. The freeze-time U-tasks will need Sol.
- **GATE CRITERIA (09:44Z; machine-checkable, so act the moment a criterion is true, without waiting for a header line):**
  - **A3 DONE** = App integration contains the A3-shared and A3-child-placement merges (including the JSON fix 0b6b), and the joint A2/A3 integrated qualification passes. → **R5 merges at once.**
  - **P1 GO** = the ORIGINAL mounted P1 chain (split → trim new ID → intervening Agent edit → lost ack → restart, covering accepted, merged and refused) passes on the integrated App + Agent + Runtime heads, with the independent no-weakening review PASS. → **A4 and G5 (except the D17 duplicate writer) merge at once.**
  - **P2/P3** run as soon as A2-undo and A2-move-reads are merged in App integration.
- **10:40Z: R5 DONE**: old save routes are rejected, with an integrated proof (original 20 + legacy 80). U1b (Runtime upstream) is merged. P2 and P3 are running. The farm is live: App full suite run, 50 real failures sent to App.
- **11:41Z: P4 DONE** (single, ten-notes, restart, show/history, conflict, rerun): 2 of 5 proofs pass. 25 merges in the last hour. App has held 78 min with the keep-awake.
- **H18 (15:44Z):** P4 and P5 DONE. P1 runs end to end (2 known fails, D24). P2 and P3 wait on the Runtime atomic-birth guard fix (Sol). App full suite PASS 18,819. ETA about 19:00Z on 24 Oct. Upstream: App efe83c77e (7 conflicts; U3b-draft on a branch); Runtime aa6c5b0cb (deferred).
- **H21 (18:46Z):** ETA ~20:00Z 24 Oct (14:00Z 24 Oct to 08:00Z 25 Oct). P1 still diagnostic, so D25. P3 is on the farm, with P2 in parallel. Bench lifecycle goes to OPS-bench-store.
- **H24 (21:50Z):** ETA ~04:00Z 25 Oct. P1 case 1 PASS, case 2 FAIL. P2/P3 move to App's service; G5 re-gated on P1 case 1 + P4; A4 split (D31).
- **00:16Z, readiness decision:** P2 and P3 stall at the same point (native 21 + history green, then the owner/read-only readiness baseline after bootstrap is UNKNOWN). One shared row **readiness-after-bootstrap**: App owns the fix, Proof gives the verdict. No more P2/P3 runs until the cause is named, except one run when a fix lands. The door-port EADDRINUSE is a harness fix (per-run port allocation, D21).
- **H27 (00:40Z):** P1 original two-case run 18792 reported **PASS** (exit 0, 141 s); Proof verdict 0036 pending, so A4 is still held. P2/P3 are blocked on readiness. Upstream candidate cause: Agent f38e164cca (bootstrap readiness marker + Linux census race); U2c-readiness-draft is a branch only. 31 merges in 3 h (21 in the last hour). **ETA ~10:00Z 25 Oct (02:00Z to 24:00Z 25 Oct).** **Time box: if readiness has no named cause by 03:00Z, the App lead tells the orchestrator at once.**
- **00:43Z: P1 GO.** Original run 18792: both cases PASS (exit 0, 141 s) on the pinned tuple App f8b15af0 / Agent 78738040 / Runtime 2a9e347f, with the spec blob unchanged; independent verdict 0036 + custody 0040 PASS. **A4 (per D31) and G5 may merge now.** Readiness-after-bootstrap has a named cause, a cancelled-bootstrap restart deadlock (App Sol 0029, RED to GREEN); independent review 0041 is active. U2c-readiness-draft is deprioritised: start it only if the App fix fails to clear readiness on the one authorised run.
- **H30 (03:50Z):**
  - P2 run 12221 on the 37eb pin PASSED readiness for the first time: 3 FAIL (App-side: element head guard, popup target, parent move to outbox) and 5 NOT RUN. P3 3362 still fails readiness on margin, so D42 applies.
  - Agent D32: an estimated ~80 of 267 still open, and Agent is now co-long-pole with P2.
  - 46 merges in 3 h.
  - **ETA ~14:00Z 25 Oct (06:00Z 25 Oct to 06:00Z 26 Oct).**
- **05:13Z: READINESS SOLVED for P2 and P3** (D45 pair on App c0fe889944 + Agent 079 + Runtime 37eb, no memo). P3 4065 passes readiness in 16.7 s; the original Gate-5 ran and then FAILED (its reset expects a 5-second state the fresh fixture lacks; Proof owns the setup correction, no weakening). P2 13583: element, popup ADD and parent move still FAIL, 5 NOT RUN (Sol 0459 + independent).
- **H33 (06:55Z):** Agent D32 is 65 of 267 open; Runtime full 0 of 36. P3 needs a setup precondition; P2 has 3 App gesture fixes plus 5 never-run gestures. D48 freeze plan and D49 venues set. 32 merges in 3 h. **ETA ~16:00Z 25 Oct (06:00Z 25 Oct to 10:00Z 26 Oct).**
- **H36 (10:00Z):** Agent D32 at 263 of 267 closed / 4 open; Runtime full 0 of 36. FREEZE: U1c + D39 merged in Runtime; Agent U2 and App U3b reviewed; Composition clean. P2/P3: 1 informative cycle since 05:13Z, with P2 popup root cause in Agent rebase_patch (D41 pin backport in parallel) and element Apply to be instrumented. **ETA ~16:00Z 25 Oct (08:00Z 25 Oct to 12:00Z 26 Oct).**
- **H39 (13:00Z):** the speed-up (D54–D57) is in effect, and the freeze merges are in for all repos. Runtime has core 0 / regressions 0. Agent's full run has 276 failing, being sorted. P2 needs all 8 (D55b); D58 and D59 set. **ETA ~04:00Z 25 Oct (22:00Z 24 Oct to 16:00Z 25 Oct).**
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
- **D25, P1 convergence (18:46Z):** an independent triage rules defect vs test expectation for the 'no recovery POST' before any fix. Diagnostics go to artifact files, not capped logs. A GO on a pinned tuple counts, and the freeze re-runs all gates on the final heads.
- **D26, no mutual blocks (19:39Z):** two rows may never be blocked on each other. The orchestrator names one owner and the next action in the same pass. P1 case 2 and P3 owner-ready are App's; Proof merges the diagnostics collector now (harness-only, D21).
- **D27, own-made permissions (19:39Z):** EACCES on files our own run made read-only inside our own $TMPDIR is a defect in our code: fix the order. Restoring u+w on your own TMPDIR fixtures is allowed. Policy and classifier refusals still stop.
- **D28, environment first (19:44Z):** when gate runs fail on one runner but not another with the same code, diff the environments before any product fix. The D21 preflight asserts the editor is 'connected' and the owner is ready before gestures.
- **D30, reports (20:39Z):** a worker's final message IS its report (the harness's -o report.md). Workers never write report.md or design/ themselves; managers copy handoffs into design/.
- **D31, A4 legacy subset (21:39Z):** if a production caller reaches the legacy transcript capture paths, restore them on v2 (Agent semantics). If they're dormant, keep that subset and its tests in the delivery, listed, and delete the rest of A4 at P1 GO.
- **D32, the final full-suite gate (00:50Z):** a full suite passes the final gate when every failure on the integrated head is either (a) fixed, or (b) proven pre-existing: it fails identically on the matching upstream main, with no project change touching it, and it is listed as a known gap in the delivery notes. Never skip, deselect or xfail to get green. This applies to Agent full 25691 (262 FAIL + 5 ERROR, census 2346): the Agent manager tags each census entry `ours` or `pre-existing`, and only `ours` gets rows. Viewing and Runtime may failover-author `ours` rows, picked from the Agent board's `failover-ok` list. The Agent manager assigns them, so no row is duplicated.
- **D33, plain-words communication (00:50Z):** board cells are 200 characters or fewer, in plain words with spaces. Long evidence goes in a linked file. Every peer note starts with one line, `Ask: … / Owner: … / By: <UTC>`. Blockers lines say who is blocked on what and nothing else, and are cleared the pass the blocker clears. Reason: dense shorthand hid stale state ("P1 NO-GO" stayed on three boards after it passed) and unowned asks (the door-port fix).
- **D34, disk work above the floor (00:50Z):** this re-affirms "above the stop line, disk is not a blocker". Runtime pauses OPS-bench-store and v1-archive retirement (0040/0042) while main is over 8 GB. Disk work resumes only below 8.5 GB, or after the delivery.
- **D35, how a gate opens (01:05Z):** a gate is open once BOARD-HEADER records it; leads and managers act on the header line, not on a peer's word. Proof's GO note goes to `peer-app2-to-orchestrator-*`, and the orchestrator records it in the header within 15 minutes, or at the next check if that's sooner. A lead who sees a GO note that isn't in the header asks the orchestrator once, and doesn't act until it's recorded.
- **KIT CHANGE (01:45Z), D36 ephemeral Codex:** every `codex exec` in the kit now runs with `--ephemeral`, so it persists no session or thread history. That history was the steady disk drain on every machine (LOOPS #38). Nothing resumes Codex sessions. Leads: no action needed; it arrives with the hub kit. Backups are `*.1024T01*.bak` next to each script.
- **D37, dormant A4 subsets (02:15Z):** D31's rule applies to every A4 subset with no production caller (proven by the census call graph, e.g. census 0042). That includes trackReorderCapture's same-order track_order record and parentAfterAnchorCapture's raw null-hold and incoming-transition birth positives. Keep each implementation and its tests **unchanged** in the delivery, list them in design/deletion-ledger.md as `dormant: no production caller; follow-up deletion for owner review`, and build no provider migration or new operation for them. Production reaches zero fallback writers, which is the end-state test. A4 is done when every reachable path is cut and every dormant subset is listed.
- **D38, script invocation (02:15Z):** a `Permission denied` from running a 0644 repo script directly (`scripts/x.py`) is a sandbox file-mode limit, not a safety refusal. Use the repo's documented interpreter form (`python scripts/x.py …`, from the lane venv) with the identical arguments. Never chmod repo files.
- **D39, truthful retired-route contract (02:15Z):** APPROVED, the corrected scope in design/runtime-R5-conformance-review-0119.md:
  - retired_route in common.json, plus a reusable RetiredRoute 410;
  - the stale success/409 declarations fixed on the five unconditional retired operations;
  - a conditional 410 on the gating document, recover and placed-shot operations (not promoteProjectShotCandidate);
  - the canonical commitTimeline 409 kept, plus a genuine commit_conflict_409;
  - recorder, fixtures, conformance tests and manifest updated.

  It merges to Runtime integration after review. **Client regeneration and Agent/App tuple adoption happen once, at the freeze.**
- **D40, external pack source authority (02:15Z):** APPROVED, the bounded **private** Runtime source admission at the host-preparation boundary:
  - it takes an exact repo/revision/subpath/manifest/tree plus the definition and capability, a symlink-free byte inventory, and an immutable snapshot leased through launch on the existing one-use launch custody;
  - the authoritative input is an owner-only Runtime configuration allowlist in Runtime private state (tests write it through the owner fixture);
  - profile, caller and source_identity claims never authorize, and there is no public schema, client or tuple change.

  HARD Sol plus an independent security review; 12 guards and 6 attacks unchanged. It gates the final full-suite gate only.
- **D41, pin-preserving gate fixes (02:45Z):** a producer fix that a pending gate run needs is first backported onto that gate's pinned producer SHA, with client and OpenAPI bytes identical by hash, its own integrated proof and an independent review. The gate run uses the backport, and the tip and the consumer tuple are adopted once, at the freeze. Reason: Runtime 45c3 changed client bytes, so P2/P3 needed a two-lane re-qualification for a one-function fix.
- **D42, readiness root cause (03:25Z):** P2/P3 readiness fails because Runtime re-verifies the immutable accepted seed commit on every history GET while holding the global store mutex (2–6 s per GET for the 21-command seed), and P2 issues the GET twice. **Approved fix:** a per-process, in-memory verification memo keyed by the SHA-256 of the exact record bytes plus the validator version, with full re-verification on any miss or difference and a negative test; verification moves outside the mutex where provably safe; backported onto the 37eb pin (D41). App coalesces the in-flight basis read on same-head effect restarts. The 5000 ms wait, test bodies and guards are unchanged. Details: design/peer-orchestrator-to-runtime-app-app2-20261024T0325-readiness-root-cause-D42.md.
- **D43, off-lane checkpoint full runs (03:50Z):** when a lane's own machine can't afford a full suite (disk), the farm runs it as a non-gate checkpoint on the lane's integration head, so exact nodes get credited and regressions show. Gate runs still follow D22, D32 and the freeze. Each lane board shows `N of M full-suite failures open`.
- **D44, untouched shared-alias siblings keep their identity (04:05Z):**
- **D45, the next P2/P3 run doesn't wait for the D42 memo (04:45Z):** the memo's security review keeps finding bypasses (sealed-validation Sol 0423). The run doesn't need it: 37eb's 3x cost cut plus App's merged coalescing (one history GET, not two) should fit the 5 s poll.
- **D46, U2c closed; relay and remote-provider custody stay out of scope (04:55Z):**
- **D47, D42 memo deferred (05:08Z):** the D42 verification memo or validation capsule is DEFERRED until after delivery, as Runtime recommended. No stable sealed validator boundary exists, and nine state attacks are open. Its held source stays unmerged on its branch, listed as a follow-up. No capsule scope is opened now. Runtime priority: the farm checkpoint follow-through, the 10 open headless nodes and the occupancy rows.
- **D48, the freeze is an owned, dated sequence (06:50Z). Coordinator: Runtime manager** (main machine, with hub access). One row `FREEZE` on the Runtime board, listing each step with its owner and state:
  1. **Draft now, on branches, in parallel:**
     - Runtime U1c (ready);
     - **Agent U2-freeze**: upstream 25359ed68 into Agent tl/integration (includes f38e164cca and D46). Agent manager, Luna + Sol review;
     - **App U3b-refresh**: upstream 2a288e629 (App manager);
     - Composition: check upstream; no merge if it is unchanged (67b8aa3d0).
  2. **Merge into integration as soon as reviewed:** Runtime U1c, then D39 client generation; Agent U2-freeze, then D39 tuple adoption in Agent. This is now allowed: the P2/P3 runs use exact pins (App 9b810 / Agent 079 / Runtime 37eb), not integration heads, and the freeze re-runs every gate anyway. That supersedes 'no merge while an exact-pin proof is pending' for this freeze. **App U3b merges right after P2/P3 GO** (so App's in-flight P2 fixes don't rebase onto it), then D39 adoption in App.
  3. **Integrated qualification** of the final tuple (all three integration heads), then **re-run P1–P5** on it (Proof), then the **final full suites** (D49), then **farm F-final + ZIP**.
- **D49, final full-suite venues (06:50Z), each proven by one checkpoint run before the freeze ends:**
  - Runtime full: main's test service (proven: 0 of 36 open).
  - Agent full: **the farm**, once OPS-farm-agent-full v2 fixes its environment and a checkpoint shows zero setup errors. The fallback is Agent's own service, after the child-venv dependency-reuse fix.
  - App full: App's test service, on the current head (last full run was 12ef).
  - Composition: Viewing's service.
  - P1–P5: App's service, with Proof verdicts.
  - Each lane board shows its venue and the checkpoint result.
  - U2c (the early port of upstream f38e164cca) is CLOSED: the readiness root cause was Runtime-side (D42 and D45). The commit arrives with the single Agent U-merge at the freeze, and candidate a181136220 stays unmerged.
  - **No new authority backend** for Linux relay peers, and **no provider-child custody** for RunPod. The paired relay and remote providers are owner-deferred scope (default: local Runtime door only), and the guards stay fail-closed.
  - At the freeze, any upstream test that fails only because our custody rejects unauthenticated relay peers or unproven provider children is reported to the owner as a known gap of deferred scope, unchanged and visibly failing, unless upstream's own lane registry already marks it manual or opt-in. Never weaken a guard to pass it.
  - The next single P2/P3 run uses 37eb + Agent 079 + App with coalescing, element-writer and diagnostics, as soon as App's popup-target and parent-move fixes are merged. Phase diagnostics will show if readiness still misses.
  - The memo continues as hardening. It merges only on a clean independent security review, and never as a gate dependency. Principle: under time pressure, prefer the fix that adds no new trust surface.
  - When authoring publication edits one occurrence of a shared alias, the untouched sibling keeps its exact physical identity (shot-shared / its revision). Only the edited occurrence forks. This follows the approved C0 principle that an alias is never silently retargeted, and it matches the minimal-change and undo guarantees.
  - The one predicate in the existing test_candidate_compiler_integrates_with_runtime_atomic_publication that requires every alias to materialize as shot-placement-* is replaced by the exact identity assertion this implies: the edited occurrence equals its fork placement ID, and the untouched sibling equals its exact source ID. The other 10 predicates are unchanged.
  - Independent review required. It's recorded as a deliberate behaviour change in design/deletion-ledger.md (section `behaviour changes`) and reported to the owner. No marker-based policy.
- **D50, protected expectations follow the approved wire shape exactly (07:40Z):** when a protected original expectation omits a field that the approved C0 v2 shape requires, and production sends it (e.g. `created: []` on a no-allocation doc.patch), the expectation is updated to the **exact** contract shape: the field is added, the equality stays strict, and nothing is optionalized, unioned or dropped. Each case needs an independent no-weakening review and actual before/after body hashes, and is recorded in design/deletion-ledger.md under `behaviour changes`. Approved now for three-products.spec.ts:1640 (P3 requestB doc.patch `created: []`). It isn't a blanket licence: every other protected byte stays.
- **D51, the owner is merging to upstream main over the coming hours (11:15Z, owner message):** don't chase each upstream move.
  - The freeze (D48) continues against the current snapshot tips.
  - **At delivery**, F-final rebuilds the squashed patches against the live upstream mains, as the deliverable requires, with ONE final U-refresh per repo.
  - U-drafts are kept small and mechanical so that final refresh is cheap.
  - The hourly upstream fetch (LOOPS #39) keeps everyone's view current. Lanes report a conflict with an owner merge to the orchestrator; they never revert or work around the owner's commits.
- **D52, owner latitude to deprecate (11:15Z, owner message: 'be big-brained about what we skip or deprecate'):** prefer **removing dead scope** over porting or repairing it:
  - (a) code this project retired (old save routes, fallback writers, deleted helpers), together with tests that exercise ONLY that code;
  - (b) dormant code with no production caller (census-proven), together with its tests. This **supersedes D37**: those subsets are now deleted, not kept;
  - (c) owner-deferred scope (paired relay, remote providers, extensions): stays out, listed as a known gap.

  Each removal is a deletion-ledger entry with its caller proof and an independent review. **Never** skip, xfail or weaken a test of LIVE behaviour; the strict gates (P1–P5 and live-path suites) are unchanged. For full-suite triage (D32), every failing node gets a category: ours-live (fix), dead-scope (remove with its code, D52), deferred (gap), env (fix setup) or pre-existing (gap).
- **D53, P3 exact-retry accounting (11:20Z):** APPROVED, the proposal in design/handoff-ap2-P3-fault-order-review-1100.md. In prepareAfterAckLossMountedDocuments' before-B-drop guard (three-products.spec.ts:1365), the single `wire.attempts===1` is replaced by STRICT complete accounting:
  - the browser sequence is exactly [A, A], same key and body;
  - exactly one forwarded Runtime request [A];
  - zero distinct B;
  - one held A retry established deterministically by the network-fault helper, with any extra or mismatching request failing.

  Production automatic retries stay on. The Gate-5 body, reset and downstream tail are byte-identical. It needs the independent no-weakening review, actual before/after hashes and a behaviour-change ledger line (same principle as D50). It's stricter than the original, not weaker.
- **D54, SHIP RULE, owner-approved 12:20Z:** we deliver when **P1–P5 and the CORE timeline suites are green on the final tuple.**
  - CORE is the end-state model: EditCommand, the commit door, undo/redo, history, split/trim/move/placement/occurrence, read/see projections (show/sheet/visualize), the App save path, and the Agent editing runner, rebase and inverse.
  - Full-suite failures OUTSIDE core (rendering and Remotion environment, legacy CLI surfaces, extensions, external packs, relay and providers, viewing-parity extras) are listed in the delivery as **known gaps**, with the tests unchanged and visibly failing. Never skip, xfail or edit them.
  - Every lane classifies its failing nodes as core / non-core (plus D52 dead-scope removals). Only core failures block. Each lane puts `core open: N` on its board.
- **D55, P2 RULE, owner-approved 12:20Z:** P2 is done when its **core editing gestures** pass. App classifies each of the 8 original gestures as core or non-core against D54 and sends me the list within the hour, for me to decide. Non-core gestures still failing are known gaps, with their tests unchanged and visibly failing.
- **D55b, P2 classification decided (12:40Z):** **all 8 original P2 gestures are CORE.** Each is an App editing gesture with a live production caller, and PLAN's P2 promise (one edit path, zero old-route traffic, intended fields only, reload, undo) is the end state's 'every edit through ONE path'. P2 GO requires all 8. Evidence: design/app-P2-core-classification-1222.md (App worker 1222).
- **D54a/D55a, REGRESSION GUARD (12:25Z, owner asked 'will we lose functionality?'):** a failing node or gesture may be a known gap ONLY if it is (i) environment/setup, (ii) failing identically on upstream main (pre-existing), (iii) a D52 deliberate deprecation, or (iv) owner-deferred scope. **If it PASSES on upstream main and FAILS on ours, it is a regression we caused. We fix it, or revert the change that caused it, core or not.** Result: no functionality loss compared with upstream, except deliberate deprecations. Every known-gap entry in the delivery notes names its category and evidence.
- **D57, OPERATING PRINCIPLES, owner re-affirmed 12:30Z. Every manager applies them every pass:**
  1. **Codex does the work.** Every task over about 5 minutes (code, tests, analysis, reviews, triage) goes to a Codex worker. Managers plan, dispatch and merge; leads do host-only actions and relay. Neither authors code or runs long analyses itself.
  2. **The weakest model that can do it.** Luna is the default for authoring, reviews, triage, tests and env work. Sol only with a `HARD:` first line naming why: a security or custody design, a multi-file root cause after a Luna attempt failed, or cross-repo contract work. Target ≥85% Luna per lane (main is at 89%). The board header shows the sol/luna live split; if Sol is over 30% of live workers, the manager justifies each Sol in its board row.
  3. **Maximum safe parallelism.** Every pass, dispatch EVERY independent ready row up to the machine cap: 6 live above 9 GB free, 4 between 8 and 9 GB, 2 below 8 GB. Split large rows into independent sub-rows (e.g. the D54 classification by package or directory, one Luna each). Never let ready work wait on an unrelated review. Board line: `live N / cap M; ready-undispatched K`. K above 0 with N below M is a defect to fix that pass.
  4. **Efficiency:** no duplicate workers on one question, no report-only passes repeated without new instrumentation (LOOPS #60), the smallest brief that fully specifies acceptance, and --timeout ≥45 for test-heavy work.
- **D58, P2 receipt oracle (12:50Z):** APPROVED, subject to the contract check below. The P2 test's `receipt_id === post.key` (helper at three-products.spec.ts:299, used by :690) conflates the client idempotency key with the server-assigned receipt.
  - Correction: `post.key` is asserted ONLY for idempotency (an exact retry reuses it), and history, head and undo joins use the authoritative `receipt_id` from the reply, with strict equality throughout.
  - The independent no-weakening review must cite the approved C0 CommittedMutation receipt envelope showing receipt_id ≠ idempotency key. If the contract says they are equal, this approval is void and the product is fixed instead.
  - Same safeguards as D50/D53: actual hashes and a ledger line.
- **D59, FINAL-TUPLE CUT and rerun venues (12:50Z):**
  - **Candidate now:** P2 and P3 run on the CURRENT integrated heads at every cycle (no waiting for Agent's unrelated repairs), so the never-run gestures surface early.
  - **The cut:** the final tuple is the set of integration heads at the moment every active lane reports `core open 0; regressions 0` and P2/P3 pass on those heads. After the cut, only core or regression fixes merge.
  - **Rerun matrix:** a product-source change in repo X reruns P1–P5 plus X's core suite. A test-only or harness change reruns only the affected gate.
  - **Venues:** P1/P2/P3 on App's service (App verdicts); P4 on Agent's service; P5 and the Composition suite on main's service. All of these are on existing qualified benches, with no farm or schema child.
  - **Boards' D57 line must copy the dispatcher-generated live count** from the board header, not a self-count.
- **D60, FINAL UPSTREAM REFRESH NOW (13:25Z; the owner reports upstream pushes are DONE).** Each repo merge-forwards ONCE to these exact upstream tips, now, before the final-tuple cut, so every gate proves once on code that includes upstream:
  - **App** 09c844033
  - **Runtime** d4f496ec4
  - **Agent** 924437716 (retargeted 13:38Z from 0d5d16af6: 2 commits, ancestor-compatible)
  - **Composition** 67b8aa3d0 (unchanged)

  Rules:
  - **Conflicts are resolved by Codex workers:** Luna by default, Sol (HARD:) for semantic conflicts in core paths. A true merge commit (merge-parent = the upstream tip). Never rebase. Never revert or rewrite the owner's upstream commits.
  - **Judgment calls go to the lane manager, then to the orchestrator if they're cross-lane or contract-level.** The default when upstream and our change collide: keep upstream's behaviour and adapt ours to it, unless that breaks a core end-state guarantee. In that case, escalate with both versions.
  - **Review:** an independent review only for conflict hunks in core product source, security code or protected tests (D56.2). Otherwise the author's tests plus the lane's core suite.
  - **Order:** Runtime first (producer), then D39 client regeneration if the contract changed, then Agent and App in parallel. P2/P3 and the core suites then run on the refreshed heads.
  - At delivery, F-final applies the squashed patches to these same tips. A new upstream move after this point triggers another refresh only if the owner asks.
  - **Test-file conflicts (13:40Z): keep BOTH.** Upstream's new and changed tests are taken as they are, and every one of our live test cases is re-applied on top: adapted to upstream's structure, never dropped. Taking 'incoming' and discarding our cases is weakening, so it's refused. The independent review maps every pre-merge live predicate to its post-merge location. Product-code conflicts follow the default: upstream behaviour, with ours adapted.
- **D84a, the request-scoped verification memo is AUTHORIZED, and it is the FIRST move (21:58Z).** Runtime's cost measurement (runtime-D83-request-cost-2126) shows the multiplier. ONE request with 2 prior entries and 3 commands did 21 accepted verifications, 16 historical sequential traversals, 144 capture-document checks and 212 schema checks, and re-verified ancestor 2 FIFTEEN times. That is quadratic re-work inside a single request, not slow verification.
  - **Fix:** within ONE request evaluation, verify each accepted entry (by its authenticated ordinal and digest) at most once, and traverse each historical sequential boundary at most once. Every later use inside that same request reuses the result.
  - **This is NOT the D45/D47 cross-request memo:**
    - nothing outlives the request;
    - nothing is shared between requests or persisted;
    - the head is still CAS-checked at accept;
    - every fresh-read and freshness predicate still runs once per request.
    - The trust surface is unchanged: the same checks, done once instead of 15 times.
  - The schema-setup churn (Sol 2141, immutable schema objects) is the same class: build once per process from immutable inputs, which is allowed.
  - **Owner:** the D84 HARD Sol (or 2141, if it is already in that code). Prove it in the local loop by counting verifications per request: each must be ≤ 1 per entry. Then one security review that checks nothing crosses a request boundary. Then P4 ten-note and the App isolated element run.
  - D84's "verify outside the lock" stays as step 2 if timing still needs it.
- **D84, a STRUCTURAL history-verification fix, not more micro-gains (21:50Z; H48 Opus).** So far +5.7%, +4.3% and +8%, and none has closed a gate. Accepted history is fully re-verified on every request, serialized, O(N). Runtime: ONE HARD Sol now (only one Sol is live on main), in the local seconds loop, then ONE security review. In this order:
  1. **Never verify while holding the request/execution lock.**
     - Verify outside it.
     - Re-check only the head pair under the lock (CAS).
     - No cache, so no new trust surface. Try this first.
  2. **Only if (1) is not enough:** an in-process verified-PREFIX memo.
     - Keyed by the authenticated chain position and digest (ordinal plus entry digest of the last verified entry).
     - It verifies only the new suffix, and any mismatch invalidates it and falls back to full verification.
     - It is never persisted.
     - This is exactly the D45/D47 memo class that failed security review before: the reviewer must specifically attack its invalidation (rewind, fork, ABA, restart, tamper).
  - **Gate:** the local loop shows per-request verification time flat in N, then P4 ten-note under 45 s and the App element/popup/parent isolated runs.
- **App:** App-side P2 defects do NOT wait for Runtime. Source-only authors fix registerAsset ownership (12674) and the placement locator (28255) now, under the D74a source-only floor.
- **D83, the speed-up (20:20Z; owner asked to speed up significantly; Opus second opinion, verified against the boards):** **most of the remaining red is ONE Runtime bug.**
  - **The evidence:**
    - All 5 D80 single-gesture runs AND the D78 live run died at the same native-seed `transport_timeout`, before any gesture.
    - Inside that seed, provider ordinal 1 took 1.7 s, but ordinal 2 only entered the store at 35 s and authorization at 45 s: that is waiting, not compute.
    - The P4 ten-note step, Agent's PARAM and restart-timeout cases fail at the same ~45 s mark.
    - Treat them all as one accepted-history-cost or lock-wait defect until proven otherwise.
  1. **Runtime, TOP priority above everything (two HARD Sol, disjoint questions):**
     - (a) Read the live stack from run 14383 (4206 B, hash eb2e), then build a SECONDS-LONG LOCAL repro loop: a local daemon, N history entries, the seed commit sequence, timing accept/store/auth, and a `py-spy dump` each iteration. Find what ordinal 2 waits ~33 s on.
     - (b) The accepted-history read/verify cost path, from P4 profile 14690.
     - No more 5–8 min service runs to diagnose this. One security review of the fix (it touches history authorization). Then ONE batched gate run.
  2. **P3: list ALL remaining failures in one run.** A throwaway DIAGNOSTIC copy of the spec (never the gate file) using `expect.soft`, continuing on failure, on a local stack, prints every remaining mismatch in about 8 min. Then ONE batched correction, ONE review, ONE gate run. No more one-assertion-per-cycle.
  3. **Collapse the review chain:**
     - The reviewer that PASSes a correction applies it and submits the gate run in the same worker.
     - Hash checks become a script, not prose.
     - NO-GO runs get a brief automatic summary, with no independent verdict and no whole-path challenge; GO verdicts keep one independent verdict.
     - D82's standing rule widens: ANY expectation correction that keeps every assertion or makes it stricter is decided in the lane with one independent diff review and a log entry. Escalate to me only when an assertion would be dropped or loosened.
  4. **Free slots now:** the E-plan rows (E1/E2/E3) and D79 are PAUSED until the ZIP. Running E/D79 workers stop at their next checkpoint via stop-worker (their work is kept), and their slots go to item 1. They resume after the ZIP.
  5. **P2 order:** single-gesture runs until all 8 pass, then exactly ONE full serial tour for the gate.
  - **Not cut:** the D54a regression guard; no dropped or loosened assertions (D69 check); the 45 s budget; security review on the history fix; one final full P2 tour; P1–P5 plus core on one pinned final tuple.
- **D82, P3 recorded-command expectation (20:08Z), deciding escalation app-20261024T1954Z-P3-recorded-command-envelope:** APPROVED, conditional on independent review 1954 PASS.
  - **Why:** the test compared the raw SUBMITTED command to the provider's authoritative RECORDED command. The provider adds seven authenticated recorder fields, by design (C0 §§1,4,7).
  - **The correction asserts BOTH, exactly:** six submitted keys, and thirteen recorded keys with deep equality of the complete command, including derived authorship, expect/reads, and the empty bindings, intent, resolved and selections. That is stricter than before.
  - Every raw request field, identity check, outer record guard, wait, recovery count and downstream assertion stays unchanged.
  - **Then:** one clean worker applies the exact reviewed patch with real hashes, merges it normally, and runs ONE pinned, preflighted P3 (D74a). Log it with D70/D75.
  - **The same rule from now on, without escalating:** an expectation that compares a raw submission to an authoritative recorded or normalized record may be corrected to assert both exactly, with no fields dropped, when an independent review passes. Log each one. Escalate only if a field would be dropped or loosened.
- **D81, E-plan (owner-approved 19:55Z): elegance work runs in parallel as design-only now, implementation after the ZIP.** See design/E-PLAN.md (rows E1–E5).
  - NON-gating. It never takes a slot from a critical row (D80) and never merges into tl/integration or changes the final tuple before the ZIP.
  - Owners: E1 and E3 Runtime; E2 Agent. TRIMMED 20:02Z: E1 is one shared Python module (no DSL or codegen); E4 is dropped (a product feature, for the owner later); E5 folds into the P4 fix. Every row must reduce total LOC.
  - Dispatch each when a slot is free behind the critical rows.
- **D80, H45 actions after the Opus second opinion (18:50Z):**
  1. **App: surface the 5 never-run P2 gestures NOW, in parallel, on App's 4 free slots.** These are registerAsset save, automatic child placement, popup SWAP, transition single clear and transition bulk clear.
     - Run each ALONE, from its own pinned and preflighted start, with Playwright `--grep` on the unchanged original spec. Use one request per gesture.
     - Test bodies are unchanged. This is a harness selection, not an edit.
     - If a case depends on state from an earlier serial case, record that as a finding (setup-dependent) and move on; don't edit the spec.
     - These are DIAGNOSTIC runs: they surface the remaining defects now, instead of one per 7-minute serial tour. The gate verdict still comes from the full original P2 run.
  2. **Runtime: critical rows first.** The non-gating D79 rows yield. Stop dispatching them while any critical row is ready, and let the running D79 kit worker finish but don't replace it. The freed slot goes to the ready critical row, then to Agent's 2 blocked:runtime rows (home-proof failover, D76 duplicate).
  3. **D78 has a 1-hour time box (to 19:50Z).** If the out-of-browser replay does not reproduce the hang, reproduce it LIVE: run the element gesture alone (item 1) with the D79 auto stack dump, or `py-spy dump` / `gdb py-bt` on the daemon and provider while the browser waits.
  4. **Popup 422 owner mismatch: ONE cross-repo HARD Sol (Runtime-owned) settles a single shot-owner definition for Agent's provider and Runtime's auth together,** citing the C0 contract, with one security review. This is the third popup refusal in a row, and each came from the two sides disagreeing.
- **D79, three cheap robustness rows, in parallel and NON-gating (18:30Z, owner asked for robustness without bureaucracy or slowdown).** Luna only, one row each, author tests only (no review gate), never on the critical path, and never preempting a critical-path slot. Promote one to a gate only if it is green and I decide so.
  1. **App: live-edit smoke (1 Playwright case on the D66 plain stack, pinned + preflighted).** Open the editor, have the Agent CLI commit an edit to the same timeline, and assert:
     - (a) the open timeline shows the Agent's edit, after the turn completes, within 10 s;
     - (b) a drag held during the remote arrival is not clobbered (usePollSync's in-flight hold), and the remote edit lands afterwards;
     - (c) undo after the remote arrival does not resurrect pre-remote state (the remoteCommit history drop).

     A failure is a real product finding: report it, and it goes through D54a like anything else.
     - **Added 19:50Z:** (d) an Agent edit and a user edit on DISJOINT targets both land (`merged`); (e) on the SAME field the Agent gets 409 value_conflict, re-reads and reruns (at most 3), and never silently overwrites; a stale front-end save keeps its draft.
  2. **Runtime: conformance replay corpus.** Take the REAL accepted commit records already retained from today's passing P1/P4/Agent home runs (no new runs), and add one test per side that replays them:
     - Agent: the recorder/reservation checks accept every record;
     - Runtime: auth/validate accepts every record and re-derives the same recorder_abi;
     - plus ONE mutated copy of each that both sides must refuse.

     It targets the bug class behind most of today's defects (Agent and Runtime strictness drifting apart). Fixture and test only, with no product change.
  3. **Kit: automatic stack dump on a hung test request.** The test service and the D66 harness, when a request has had no response for 20 s, run `py-spy dump` (if installed) or `gdb -batch -ex py-bt` on the Runtime daemon and provider PIDs into the run's evidence dir. It's harness only and no product code changes, so every future hang arrives with its blocked frame.
- **D78, element-apply hang: reproduce OUTSIDE the browser, with stack dumps (18:20Z).** It has recurred since H36, through 2 P2 runs today, and the in-run phase instrumentation came back UNAVAILABLE. Stop diagnosing it only through 7-minute browser runs.
  - **Runtime, HARD Sol, dispatched with `--net`:**
    1. Start the stack at P2 22847's pinned tuple (App 587316e / Agent f4d6c72 / Runtime 327da20 / Composition 635f4de).
    2. Replay the EXACT retained element `doc.patch` request (method, headers, body, idempotency key, from App's retained network evidence) with curl or a minimal client.
    3. If it hangs past 10 s, dump every Python thread stack of the Runtime daemon and the Agent provider process (`faulthandler` via `faulthandler.register(SIGUSR1)` if the processes allow it, else `py-spy` if installed, else `gdb -batch -ex "py-bt"`), and record which lock, wait or call each request thread is blocked on.
    4. If it does NOT hang with replay, the difference is in what the browser sends or how it waits: diff the two requests byte for byte.
  - Report the blocked frame with file and line. The fix follows from that, with a security review only if auth code changes.
  - **D78 switched to the LIVE route now (19:00Z):** the exact replay lacks the original realm, base and history state, and we will not invent it. So, as soon as the D79 auto stack-dump route is installed on the App test service (Runtime installer 1847): App runs the element-apply gesture ALONE (D80 per-gesture, --grep, pinned and preflighted), and the dump fires at 20 s with no response, capturing the Runtime daemon and provider stacks. If the installer is not live within 20 min, App runs the same single gesture and the Runtime owner takes `py-spy dump`/`gdb py-bt` on the service host while it waits. The Runtime replay owner reads the blocked frame.
  - **Popup 422** ("provider created shot owner differs from its authenticated occurrence") stays with the Runtime popup owner. First check whether b318's fork-created shot-root projection compares the owner against the wrong occurrence. **The parent "Committed ..." label** is App's.
- **D75b, P3 recovery counts (18:15Z, scope question 1805):** **retain BOTH automatic-recovery mounts, with strictly revised COMPLETE exact counts.** Do NOT consolidate.
  - **Why:** consolidating the intermediate reload into the post-restart mount drops an observation point, and that is a weakening. Counting every attempt the product really makes, including the intermediate reload's extra attempt A, observes more of production.
  - **Rules:**
    - every attempt is asserted with exact identity (request, key, body, origin);
    - exact equalities only: no "at least" or range counts;
    - the sequence order is asserted;
    - every original wait and timeout is unchanged.
  - Independent 1806 must confirm the revised totals come from the real retained controls, not inferred. Then apply it and rerun P3 on a pinned, preflighted tuple.
- **D77a, proceed with the consumer migration (18:00Z), deciding escalation runtime-20261024T1753Z-D77-upstream-proof-limit:**
  - The source evidence is enough. Upstream's wiring supplies the schema Python payload end to end: Composition 0.0.6 lock → schema 0.0.1 archive → Backend.stage → host bootstrap → strict reader. Ours (Composition 0.0.14) lacks it while the reader is unchanged.
  - Under the regression guard, when the evidence points to a regression, we treat it as one and fix it. We do NOT wait for a live upstream render proof that would need denied acquisition. So it is a presumed regression and cut-blocking.
  - **Authorized:** the HARD Sol consumer migration (host_bootstrap plus the remotion_runtime strict schema input/probe reading the canonical local JSON), keeping equivalent origin, ownership, digest, closure and refusal validation. Then one independent review. Prove it with the current staged-host controls plus the final-cut render gate.
  - The upstream runtime outcome is recorded as UNKNOWN, not as a failure.
- **D77, installer local schema: accept the integrity migration, decide the render path by the regression guard (17:55Z), deciding escalation runtime-20261024T1745Z-D72-installed-schema-scope:**
  1. **ACCEPT** the installer integrity migration b4f79d12e0 under D72: checked-in canonical JSON verified against the runtime.lock digest, the obsolete external install removed, recursive guards kept. Merge it on its author and independent PASS.
  2. **The installed host render path is NOT a D67 env gap by default.** D67 covered one preflight test needing a real installed tuple. Staged rendering on an installed host is user-visible, upstream-supported functionality.
     - Settle it with ONE Luna row, read-only, on upstream 924 with the upstream installer and Composition 67b8aa3d0: does upstream's staged host path obtain `banodoco_timeline_schema` models and get through host_bootstrap/render validation?
     - **Upstream works → a REGRESSION we caused (D54a), cut-blocking.** Fix it with a consumer migration: host_bootstrap/render validation reads the canonical local JSON schema, the same contract and the same strict refusals. HARD Sol plus one independent review. No fake models and no JSON-for-model substitution without equivalent validation.
     - **Upstream also fails or lacks it → PRE-EXISTING.** It becomes a visible known gap, with the evidence cited.
  3. All refused or denied acquisition routes stay stopped.
- **D76, duplicate-chapter original is a D72(2) setup migration, not a product fix (17:50Z), deciding escalation agent-20261024T1738Z-duplicate-canonical-fixture:** APPROVED.
  - **Why:** the upstream body mocks `check()` and feeds a non-canonical registry (`{"media_id":"m-r"}`). Upstream's own test never proved that un-mocked admission accepts such input. Our renderer-free `_check_core()` correctly refuses a missing canonical selected-media identity. Four strict duplicate controls pass: per-chapter identity, all-or-nothing, renderer-off and collapse refusal.
  - **Do:** a faithful SETUP-ONLY migration to a genuinely canonically admitted media fixture, keeping EVERY chapter, copy and publication assertion. Run the D69 mechanical check, then one independent review, then a D72 log entry. If it then fails, fix the product.
  - Do not honour mocks, accept `m-r`, or fabricate identity.
- **D75, P3 recovery step observes production auto-recovery (17:45Z), deciding escalation app-20261024T1733Z-P3-automatic-recovery-observation:** APPROVED for the CORRECTED proposal (Luna 1736, after 1722 FAILED review 1731), conditional on its own independent PASS against the conditions below.
  - **Why it's sound:**
    - The "Recover saved edits" click is OURS: it was added 19–20 Oct (8c942a46f and successors) and is absent upstream.
    - It targets a button that exists only in fixtureControls.
    - Production `useTimelineSave` recovers automatically, per C0 §§1,4,5,7 and D13. That is the same product source P1 26312 passes on.
    - Observing the genuine automatic retry, held across the Runtime restart and then released, tests MORE of the real product than a fixture click did.
  - **The conditions 1731 must confirm:**
    - every original wait and timeout is unchanged;
    - request, key and body, plus the downstream B/history/undo/canonical assertions, are preserved;
    - the new observed 3-before/4-after, exact-identity and forwarded-1 guards are present;
    - no manual recovery, ignored attempt or alias;
    - real before and after hashes, with nothing inferred.
  - Log it with D44/D50/D53/D70. After PASS: apply it and rerun P3 at once on a D73-pinned tuple.
- **D74a, critical-path runs get a lower floor (19:40Z):** the P1–P5 gate runs and the D78 live element run may be SUBMITTED down to **6.0 GB** free, one at a time. It applies on every lane (21:38Z), including heavy critical batches such as Agent P4 and timeout originals; the 8.5 GB heavy gate applies only to non-critical heavy work. **App 22:14Z:** App gate and source-only critical work may start down to 5.2 GB, one at a time; App stop line 4.5 GB. **Extended 21:28Z:** small SOURCE-ONLY authors on critical-path rows (~0.2 GB checkout, no service build) may also dispatch down to 6.0 GB. Everything else keeps D74: no new dispatch below 7.5 GB for non-critical work, and none at all below 6.5 GB except those runs.
  - **Release stale trees by the principles route.** KEEP pins whose SHA is not a current lane head, a running or queued request, or an in-flight P-run's D73 tuple: confirm nothing uses them, remove KEEP, then bin/recycle.
  - Dirty old U3b trees: first save `git diff > $ORCH/archive-v1/<name>.patch`, then recycle.
  - If the classifier or a guard refuses, stop and report.
- **D74, disk caps lowered by 0.5 GB, and the classifier refusal goes to the owner (17:16Z):**
  - **New D57 caps:** 6 workers above 8.5 GB, 4 at 7.5–8.5 GB, 2 below 7.5 GB, and no new dispatch below 6.5 GB.
    - A worker tree is ~0.1–0.5 GB, so two more slots cost ≤1 GB.
    - Disk-falling alerts stay; the run-output retention fix (post-verdict, guarded tools) is the root fix for growth.
  - **Agent's release of 38 stale pin checkouts was DENIED by the auto-mode classifier** ("Irreversible Local Destruction").
    - Per the rules, nobody routes around it. That includes me running it from main: that would be laundering the refusal.
    - It goes to the owner, who may add a permission rule or say no.
    - Until then, Agent stays at the new caps.
  - App and the rest: if a guarded release is refused by the classifier, stop and report it, same as above.
- **D73, gate runs pin their tuple at submit (17:08Z; root cause of P3 31887 dying in 3 s: Agent home moved ef036→a60f8b3 between the head check and the run, so the "current" checkout did not exist):**
  - **Rule:** every P1–P5 request names EXACT SHAs for all four repos, captured once at submit. The service runs THOSE SHAs. It never re-resolves "current home" at run time.
  - The submitter requests the pinned checkouts (`request-checkout`) BEFORE submitting and submits only on their receipt. That turns the race into one deterministic step.
  - A newer head arriving mid-run does not invalidate the run. For the cut (D59), the latest passing pinned tuple is the candidate, and the matrix decides what reruns.
  - App fixes this once in `d66-plain-stack`/its submit step (harness, D56: author tests only). Agent's P4 and main's P5/Composition follow the same rule.
  - **Addendum (18:02Z):** the submit step runs the source/preflight stage ALONE on the pinned tuple first (seconds) and submits only on exit 0. One command, so it cannot be skipped. This follows three pre-case launch deaths (12541, 31887, 20321).
- **D72, restored upstream tests that hit retired interfaces (17:05Z), deciding escalation agent-20261024T1654Z-D69-restores-vs-retired-contracts:** D69 amended. **The regression guard protects BEHAVIOUR, not internal interfaces.** For each family:
  1. **Retired by the approved plan (G5/R5: separate publish and its CLI subcommand, `publish_bundle`, `store.three_way`, merger, native subparsers, old writer routes, `WorkspaceClient.publish_parent_composition`'s retired route):** these go to the **deletion ledger**, citing the G5/R5 row and D52.
     - Each entry MUST name the CURRENT test that covers the replacement behaviour: publish → commit through Runtime; three_way conflict diagnostics → Runtime conflict reply; idempotency/CAS/clean-copy/output → the commit equivalents.
     - Where no current test covers a user-visible capability the old test proved (idempotency, CAS/conflict, clean-copy, terminal output), add ONE targeted test on the current API (Luna). No resurrected writers, no aliases.
     - The retired user-facing CLI commands go into the ZIP README migration notes and the owner update.
  2. **Live behaviour whose body calls a removed INTERNAL helper** (7 element cases monkeypatching `resolve_admitted_element`/direct publisher, 2 approval cases using the old promotion writer, 2 create-empty cases via `publish_parent_composition`, the generic-host `_publish_assembled_timeline` case): **faithful migration.**
     - Rewire ONLY setup/caller to the current API (TimelineSession/Runtime bootstrap, the commit path).
     - Keep every behavioural assertion: same inputs, same observable outputs.
     - Run the D69 mechanical check (no assertion removed or loosened), then one independent review, then a "migrated upstream test" log entry.
     - A migrated test that then fails is a regression: fix the product.
  3. **Rendering/input (4):** the 2 sliced-clock/null-window cases migrate to the approved native FrameWindow contract with equivalent frame-coverage assertions, citing that decision. The generic-host case follows (2). The installer schema case migrates to the approved local Composition/Runtime schema (D65 principle).
  4. **The possible live duplicate (chapter admission, owner 1653) and the 2 CLI output regressions (candidate 81a261):** product fixes, already moving.
  - **Batching:** run this as parallel Luna rows (CLI / SDK / core / render), each with one independent review. Report per family: ledgered+covered / migrated / fixed. This must finish before the cut.
- **D71, P4 private-cache leak (17:00Z), deciding escalation agent-20261024T1650Z-P4-inspection-capture-contract:** **option B: fix the product, keep the P4 predicate.**
  - **Why:** P4 passed before d05fcc0766c. Its assertion (`_runtime_document` must not appear in `original["source_mapping"]` of the bundle an ordinary read hands back) encodes a real product property: private Runtime authority does not leak into caller-visible data. d05fcc, our change, broke it, so under D54a this is a regression we caused. Fix the source, never relax the gate.
  - **Shape:** the authenticated exact-pair cache stays, but lives on a PRIVATE channel (a side-table or attribute keyed by revision/publication, or stripped in the caller-visible projection that `TimelineSession._bundle` returns). Private authenticated execution and every wrong-pair, wrong-publication no-write and accepted-result guard stay exactly as strict. No cache authority is removed.
  - **The hydration unit test** (`test_clean_bundle_hydration_authenticates_exact_pair_without_pending_commands`) is ours. If it asserts the cache's LOCATION inside source_mapping, re-point it to the private channel with the same strength (exact pair present; wrong pair refused). That counts as an expectation change, so it needs independent review and a behaviour-change log entry. Its behaviour must not get weaker.
  - **Owner:** Agent's HARD Sol (1639 continuation), then one independent security review (custody), then an unchanged P4 rerun.
  - **The 2 repeated-source-copy redo failures** (test_commit_runtime_source_copy.py:335) are a separate Luna classification, as Agent assigned. If they started failing because of a change of ours, D54a applies.
- **D70, P3 setup intent expectation (16:55Z), deciding escalation app-20261024T1643Z-P3-exact-move-intent:** APPROVED, conditional on independent review 1643 PASS.
  - The change is one line at `tests/e2e/local/three-products.spec.ts:1347`: `intent: "Save local editor changes"` becomes ``intent: `Move ${seed.appClipId} on V1` ``. Label, tags and the original Gate5 body, reset and tail stay byte-identical.
  - **Why it's sound:** that expectation is OURS. It was added 23 Oct (cc64db3a8 "adapt Gate 5 to mounted document intents") and is absent upstream. Our production `timelineLocalSaveHandoff.ts` intentionally emits the semantic gesture intent for gesture saves, per contract C0 §§1,4,7 and D13. The new expectation is MORE specific than the old one: an exact string, not a weakening.
  - It goes in the behaviour-change log next to D44/D50/D53. D66's "originals unchanged" governs the HARNESS. It does not forbid an approved, reviewed expectation correction.
  - After 1643 PASS: apply it, then rerun P3 on the current head.
- **D69, reverse-diff follow-through (16:05Z; Agent found 362 upstream-924 selectors not matching ours: 137 in the D52 ledger, 47 restore-needed, 178 present-but-changed, 0 renamed):**
  - **47 restore-needed:** restore each upstream test body UNCHANGED. If it then fails, it goes through the D54a regression guard (fix or revert the product change), never a test edit. The three Luna rows proceed.
  - **178 present-but-changed upstream tests: a weakening audit, mechanical first.** One Luna pass diffs each test body ours-vs-924 and flags any REMOVED or loosened assertion: an `assert`/`expect`/`raises` line removed, a comparison relaxed (== to in/>=, exact to approx), a parametrize case dropped, or a skip/xfail added. Unflagged changes (pure renames/adaptations, assertions intact) are cleared. Each flagged one must cite a logged decision (D44/D50/D53/D58-type entry in the behaviour-change log) or be restored to upstream's assertion. Report counts: cleared / cited / restored.
  - **Same audit for App and Runtime:** each runs the reverse diff (upstream tip tests missing or changed in ours) as one Luna row. Composition is unchanged, so it is exempt.
  - None of this blocks P2/P3. The results must be in before the cut.
- **D68, upstream App moved after D60 (15:45Z):** upstream reigh-app main is now 3881e9440 (4 commits, 14:05–14:19Z: onboarding/connection/tour; 41 files, +1718/−506). Its only file overlap with our App diff is `src/shared/components/SettingsModal/sections/ConnectionSection.tsx`.
  - **Merge it forward NOW, once**, in App (`bin/merge-forward` with a true merge commit, Luna resolving; default to keep upstream and adapt ours; test conflicts keep BOTH). It is cheap now because P2/P3 have not run on the current heads yet, so no gate proof is lost.
  - Do it in parallel with the D66 harness boot, NOT blocking it. P2/P3 submit on whichever App head is integrated when the boot passes, and the cut needs the merged head.
  - **From now on, upstream is frozen for gating:** any later upstream move is NOT merged into the gating tuple. F-final applies our patches to fresh upstream main (D51), and a conflict there goes to Luna, with Composition/App full suites re-run on F-final only if files overlap. I tell the owner.
  - Upstream Runtime d4f496ec4, Agent 924437716 and Composition 67b8aa3d0 are unchanged.
- **D67, Agent D13 UNKNOWN is an env known gap (15:30Z):** `tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight` is NEW-OURS (added 21 Oct; absent at upstream 924). It checks a real INSTALLED deployment tuple: a source profile, a 7-key expected-bindings JSON, and the Node/Remotion/browser/ffmpeg/ffprobe paths and hashes. Nothing in the lanes' test environments supplies that, and nothing may be fabricated.
  - Under D54 it is an **environment known gap**: kept, unchanged, visibly failing. It is NOT core-blocking.
  - The ZIP README lists it as a post-install check, with the exact env vars to set.
  - Agent's core-open target is therefore 6 (4 fork + 2 forward), all on D62 / forward-created auth.
  - This is not a permission-refusal case, so no owner action is needed.
- **H48 (21:55Z):** ETA ~12:00Z 25 Oct (07Z 25 Oct to 04Z 26 Oct). P1 and P3 GO; P2 0/8 (Runtime history verification stall plus App registerAsset setup); P4 ten-note 45.4 s. Critical path: the D84 structural verification fix.
- **GATE P3 GO (20:44Z):** original Gate5 request 15493 passed: exit 0 in 248 s; readiness 1/1 and original 1/1 PASS (recovery mounts with exact 5/3 counts, merged B, history, restart, canonical, guarded undo). App c184bd0bec, protected spec 93c2bf4c72 (D70/D75/D75b/D82 corrections). Independent verdict GO: app-P3-15493-GO-verdict-2024. The cut matrix (D59) decides any rerun on the final tuple. P2 waits on the Runtime native-wait fix (D83): the SDK times out at 30 s on seed request 2.
- **H46 (19:42Z):** popup shot-owner fix merged (87bc); P3 26908 NO-GO (recovery count 3 vs 4); P4 ten-note still >45 s (profile ordered); element capture 13100 reached accept. Agent core 5.
- **H45 (18:55Z):** ETA ~12:00Z 25 Oct (06Z 25 Oct to 04Z 26 Oct). Gates: P1 GO current (26312/1616); P2 22847 0/3/5; P3 NO-GO (D75b applied); P4 ten-note 45 s FAIL. Critical path: D80 per-gesture diagnostics plus the D78 element hang, then a full P2 rerun.
- **H43 (16:45Z) gates:** P2 25943 NO-GO (0 pass / 3 fail / 5 notrun: element doc.patch hang -> Runtime Sol; popup 422 physical observation -> Runtime whole-path, D54a check vs 8b32/bc227; parent reads present -> App 1625). P3 10033 NO-GO on the history oracle missing recorder_abi (App fix done). P1 current control 13564 fails its initial split (App Sol1600). Agent core open 3 (inverse proof pending on bc227; P4 single edit; P4 ten-note timeout). Reverse diff done: 47 restored, 178 audited (167/9/2).
- **H42 (15:40Z):** ETA ~08:00Z 25 Oct (03-22Z). Critical path: App plain-launch boot (D66) -> P2/P3 parallel; Runtime D62 bundle -> one regen -> Agent 4 fork + 2 forward proofs -> manifest pin -> cut.
- **D66, H42 cuts after the Opus second opinion (15:35Z):**
  1. **App: STOP the caller-custody stack.** No more work on F-caller, F-service-binding, F-caller-join, F-launch (custody review 1505) or P1-current-caller as custody machinery; the "worker-only install" is no longer a prerequisite. Stop in-flight workers on those rows at their next checkpoint and keep their diffs. The proof harness only has to:
     - (a) start the App service stack from the current integrated heads with the normal test/dev commands;
     - (b) run the ORIGINAL P1/P2/P3 test files UNCHANGED;
     - (c) record a plain run manifest: every repo's HEAD SHA, sha256 of each original test file, the running service's reported versions read back at start, and the JUnit XML.

     That manifest IS the identity proof (it replaces the stale-setup check). Use ONE Sol worker (Luna whole-path 1514 gives the facts) to make P1, P2 and P3 boot this way on the current heads. Gate: P1 runs green through it (it passed historically, so it is the control). Submit P2 and P3 in parallel immediately after, without waiting for P1's verdict review. This replaces D64's "reuse P1's route", because P1's current caller is also failing.
  2. **D65 amended:** pin the manifest ONCE, after D62's regeneration lands, because the new HistoryEntry field changes the schema digest. Until then the skew test stays visibly failing as "pending D62 regen".
  3. **D63 extended:** one Luna row diffs the OTHER way: upstream-924 test selectors missing from ours. Each one must be either renamed (mapped), D52-deleted (in the deletion ledger), or restored. This is the real lost-functionality check.
  4. **Runtime provider-completion incident:** one historical failure with no reproduction, whose bounded source review found no defect. It is not held open now. The cut rerun decides it: its originating test passes on the final tuple → closed; fails → core-open and root-caused then.
  5. **Agent D13 UNKNOWN:** Agent posts ONE line (exact test id; the exact missing input and where it would come from). If it comes from the D62 recorder or current App D13 reads, re-run after D62. If it needs a source behind a permission refusal, it becomes an env/owner known gap and I put it to the owner. The ship rule must not wait on a refused permission.
  6. **Runtime: no separate "integrated proof" stage for D62.** Its author tests + security review + Agent's four-fork/two-forward actual-home proof suffice; the final cut rerun covers the rest. Merge the D62/forward/wire bundle and regenerate ONCE.
- **D65, install-manifest pins are release-coupled (15:24Z), deciding escalation app-20261024T1514Z-installer-runtime-release:**
  - **The facts:** `public/install-manifest.json` pins Runtime and Agent by COMMIT SHA plus `schema_digest`, with no release tag. Upstream App pins upstream Runtime 0dd3/3605 and Agent e2cac. Our App vendors Runtime e68/4118, so the strict skew guard fails. It is caused by our cross-repo change, so it is fixed, never waived.
  - **During gating:** App's manifest points at the Runtime and Agent commits of the tuple being proven: the current integrated heads now, the F-final commits at the cut. `schema_digest` is the generated 4118 (or whatever the final generation produces). Use App's existing manifest tooling. The guard stays strict and must PASS. One Luna row now; it's a harness/pin update and merges on the author's tests (D56).
  - **Delivery (Runtime F-final/ZIP):** the real upstream SHAs exist only after the owner merges our patches. So the ZIP's README gives the order: merge Runtime, then Agent, then run ONE included command in App that rewrites the manifest SHAs to the new upstream commits and verifies the schema digest equals the generated one (content-addressed, so the guard still proves it), then merge App. This is an owner release step, listed in the owner update. Nothing is published or pushed by us.
  - Any test that FETCHES the pinned SHAs from GitHub during gating is env (the commit isn't upstream yet). Classify it so, with the exact test id, and run it after the owner's merge.
- **D64, P2/P3 launch: reuse P1's proven route; harness provenance is not "custody code" (15:16Z, App pair 12541/1689 exit 2 in 1 s):**
  - **Smallest fix:** P1 passes on the SAME App test service. The P2/P3 caller must launch the same way P1 does (same service entry and recipe shape), with its four TIMELINE inputs supplied by the request/recipe the way P1 supplies its own. Sol1437 takes Luna whole-path1437's P1 diff as the spec. No new launch-custody machinery, no new authentication layer for the test caller.
  - **Review scope (D56 clarified):** "security or custody code" means PRODUCT authorization/custody (Runtime auth, receipts, bindings). Test-run provenance guards (CUSTODY_PREFIX, caller environment guards, recipe identity checks) are HARNESS. They merge on the author's tests plus the dry launch below. No separate independent review cycle.
  - **Gate before ANY next original submission:** one dry launch of the EXACT request through the real service: no inherited TIMELINE inputs, it reaches the first original case, and it exits cleanly at a no-op/abort point. One poison control (an input missing → refused). Then submit P2 and P3 at once, in parallel.
  - **Installer schema failure 1507:** fix only if it blocks that dry launch; otherwise run it in parallel and keep it off the critical path.
  - **Target:** P2/P3 resubmitted by ~16:00Z. If Sol1437 has not returned by 15:45Z, start a parallel Luna copying P1's launch for P2/P3 directly; first one to pass the dry launch wins.
- **D63, classifying the upstream-baseline diff (15:03Z, Agent's 276 vs upstream-924 full 1621):**
  - **Selectors missing upstream (201) are NOT "UNKNOWN" for the regression guard.** A test that does not exist upstream cannot show upstream behaviour we broke (D54a). After ONE cheap rename check (same test function name, or same body text, under another path upstream → map it and compare those as normal), every remaining one is **NEW-OURS**: it tests our own code, so it goes by the D54/D55 core rule: core → core-open; non-core → known gap, visibly failing; D52-dead scope → deletion ledger. Do this as one Luna row over the existing XML and tracebacks (no reruns).
  - **Fails on both (66) = pre-existing.** The Luna A/B traceback check (1458) finishes as planned. Same failing test plus a matching exception type and location = pre-existing. Only a DIFFERENT failure on ours goes to a per-test look. Don't block on deeper cause identity.
  - **Pass upstream, fail ours (9): 8 already pass now and 1 is the deferred D23 timing case.** Proven regressions: 0, once the 8 are confirmed on the cut run.
  - The e68/becfe recipe mismatch check (1459) continues. The full-run classification stands unless it finds that the run did not use the integrated Runtime.
  - **The forward ABI1 ACK (request 1440) was given at 14:57Z** in the agent INBOX: Runtime's R-forward-created-authority, HARD Sol 1450, owns both cases.
- **D62, D61 clarified: NO native-execution custody seam (14:55Z), deciding escalation runtime-20261024T1443Z-D61-private-native-custody:**
  - **Declined:** the proposed cross-repo private native-executor custody/digest seam. It is a new trust surface (D45/D47 principle: under time pressure prefer the fix adding none). It defends only against a lying AUTHENTICATED producer at submit time, which is producer-trust scope deferred with D46. Upstream has none of this code (the timeline commit SDK and its fork guards are ours), so the regression guard (D54a) is not engaged.
  - **What "derived from its own validation" (D61) means:** `recorder_abi` is a pure function of the record Runtime ACCEPTS (2 if it was accepted by the v2/sequential-execution validation, i.e. physically enriched bindings; else 1). It is computed once at accept, persisted in the immutable accepted-commit record under the existing event+metadata authentication, and returned as the proposed optional top-level `HistoryEntry.recorder_abi` (enum 1|2; absent = 1; D39 regeneration). Runtime keeps validating what it already validates; it does not try to prove native coverage is complete.
  - **Why that is sound for the gate:** the 4 fork originals (and the 1350 attack, and D61's FULL REWRITE variant) damage history AFTER acceptance. Persisting the classification freezes it, so a stripped/rewritten v2 entry still says abi 2 and Agent's `_check_reservations` fails closed. A submission that is ABI1-shaped through and through IS a genuine ABI1 commit (indistinguishable = equivalent authoring), and a v2 submission with omitted native bindings is recorded abi 2 and fails closed at use (missing authenticated binding). Neither needs submit-time custody.
  - **Known gap, recorded in the behaviour-change log:** "Runtime does not prove a v2 producer's native coverage is complete at submit (Sol1422's 8 omission packets); such commits fail closed at fork/inverse use." Post-delivery hardening, not a regression.
  - **Runtime: implement now** (HARD Sol may resume 1422 with this scope; Luna1443's challenge is re-scoped to: does the persisted, accept-time abi pass the 4 fork originals + genuine legacy positive + v2 strict negatives). One independent security review (D56: custody code). If any of the 4 originals requires SUBMIT-time detection, escalate back citing the exact test id and assertion. Do not try to reach that by inference.
  - **Agent:** the consumer (Sol1417/port1433) adopts the field when it is published. No other change.
- **D61, authenticated recorder ABI mode for fork reservations (14:10Z), deciding escalation agent-20261024T1400Z-ABI-mode-authority:**
  - **The authority must be Runtime-derived, never caller-supplied.** Runtime validates every accepted commit against its schema, so it alone knows authoritatively whether a commit's bindings were written by the v2 recorder (complete binding coverage) or are legacy ABI1.
  - **Approved minimal boundary extension:** at accept time Runtime persists `recorder_abi` (1 or 2), derived from its own validation, in the immutable accepted-commit record, and returns it in the history entry Agent already authenticates via load_boundary.
    - Prefer an EXISTING authenticated extensible slot in that entry (no schema change). If none exists, add it as an additive field, which triggers a D39-style client regeneration for Agent and App.
    - Commits accepted before this change lack the field and count as legacy (ABI1).
    - `_check_reservations` (agent/astrid/sdk/timeline/commit.py:681) consumes it. A capture whose authenticated commit says abi 2 but which presents ABI1-shaped bindings is REJECTED.
  - **Both originals must pass:** the genuine legacy positive and the v2 strict negative. The FULL REWRITE variant must be refused.
  - **Owners:** Runtime producer (HARD Sol + independent security review, as D40) and the Agent consumer (Sol 1354 continues). No caller flag, no inference from public fields, and no weakening of the guard.
- **D56, PROCESS SIMPLIFICATION, owner-approved 12:20Z:**
  1. **Prove once, on the final tuple.** The freeze merges go into integration NOW (App U3b, then D39 adoption; Agent U2, then D39; Runtime already done). No more pinned-tuple runs or D41 backports. Every further P2/P3 run and every gating full suite runs on the final integrated tuple. D41 is retired for this delivery.
  2. **Review only where it pays.** An independent review is required only for: security or custody code; protected test bodies and expectations (D50, D53 type); product source changes on core paths. Harness or test-setup fixes, D52 dead-scope removals, kit/env fixes and anything a green gating full-suite run covers merge on the author's tests alone.
  3. **F-final and the ZIP are built on main by the Runtime manager**, from fresh upstream clones (D51), using the existing delivery-build tooling (DB dry runs passed). The farm stands down: no more farm venue work, and the banodoco/astrid-agent access request is dropped. D49 venues are each lane's own service; Composition's full suite runs on main.
  4. **Proof folds into App.** App owns the P2/P3 runs AND their verdicts, with one independent reviewer worker per verdict. Proof (app2) finishes its in-flight items, hands its open rows to App, then stands down. **Viewing stands down** (all its rows are done).
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
