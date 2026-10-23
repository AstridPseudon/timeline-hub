# Timeline: PLAN (v2.1, restarted 22 Oct 2026)

**This page is the single source of truth.** The previous plan is kept at `PLAN-v1.md`, for the gate details in its §6 and the extension model in its §4; nothing else in it applies. Owner: Hannah (AstridPseudon). Orchestrator: Claude on the main machine.

## Who does what (lanes → machines → areas)
| Lane | Machine / lead session | Area name (prefix) | Home repo it merges | Task IDs |
|---|---|---|---|---|
| Runtime | main (orchestrator) | runtime (rt-) | runtime | C0, R0, U1, R2r, R5, P5 |
| Agent | Timeline Child 4 | agent (agt-) | agent | U2, U4a, R1, R2, R3, V2, G2, G3, G4, G5 |
| App | Timeline Child 1 | app (app-) | app | U3, U4p, A2, A3, A4 |
| Proof | Timeline Child 3 | app2 (ap2-) | none (merge requests to app / agent / runtime) | P1, P2, P3, P4 |
| Schema & viewing | Timeline Child 2 | viewing (vw-) | composition (merge requests for the others) | V1, V3, V4 |
| Farm | Timeline Child 5 | farm (tf-) | none, runs tests only (Claude runner) | F |

- **Managers** run on **Codex Sol (high)**, via `bin/run-manager <area>` with its default model, in bounded 90-minute rounds. **Leads and the orchestrator** (Claude) do as little as possible: they keep the machinery healthy and hand everything else to the managers. The farm alone runs Claude workers.
- **All code, reviews, merges, conflict resolution, generated files and pins** are done by Codex workers: Luna by default, Sol only with a `HARD:` brief line on the tasks marked Sol.
- **Each lane's board** is its manager's `STATUS.md`, published as `hub/status/<area>.md`. The orchestrator's header is `design/BOARD-HEADER.md`.
- **The contract** (task C0) is `design/commit-v2.md`.

*This page plus the hub task board are the whole plan. It supersedes `scope-of-work-90-10.md` and `plan-document-first.md`. v2.1 folds in Astra's review (`review-20261022/astra3-review.md`). The project stays paused until the owner says go.*

## 1. What we are building
- **Runtime is the only writer of film data.** Every edit, from the App, the Agent, scripts, sheets or extensions, is a commit through the existing commit engine, which handles idempotency, head CAS, rebase and guarded undo.
- **A commit carries:**
  - the base;
  - commands, which are either
    - **semantic commands** (split, ripple, per-occurrence fork, plus the existing native move/trim/set), or
    - one generic **`doc.patch`** (id-addressed set, remove and list insert/remove/move, each change carrying its previous value);
  - a label and steps (intent, tags, each step's own patch);
  - a merge mode;
  - declared read dependencies (optional).
- **Semantic edits exist only in Python,** in the Agent provider that Runtime executes. The App previews locally with upstream main's editor, and Runtime's result wins. There is no TypeScript executor and no golden fixtures; the behavioural tests are kept.
- **Agent golden path:**
  - CLI: `show find diff history visualize` / `edit apply undo redo commit`;
  - Python: `tl = timeline.open()` → helpers or free edits → `tl.commit(label | fn, merge=, dry_run=)`. A function re-runs on conflict, with a bounded number of retries.
  - Errors give a code, path, hint and a suggested command.
- **The App:** gestures are local. Saves go through the existing persisted outbox. Merged replies are applied, refusals roll back, and there is no overwrite button.

**Honest scope.** This ships the editing foundation. Deferred, and stated as such in the delivery:
- automatic relational timing (anchors and pinned markers);
- push updates (Agent edits appear on the next poll);
- unified rendering (gate 6 parity, the viewing rows, the renderer consolidation; one Composition artifact is not one evaluator);
- proposals and `watch`;
- the M5 extension model rewrite;
- the repo-structure decision.

Open `meta` stores extensible data, but gives no reference integrity for it.

**Rules kept from before:**
- never push upstream;
- never weaken tests;
- no M5;
- a fresh-main ZIP;
- the owner views on a duplicate;
- all code, **reviews, merges, conflict resolution, generated files and pins on Codex**;
- Claude only dispatches, reads results and keeps the board.

## 2. The contract (H0–H1, written by a Codex Sol worker and approved by the orchestrator)

`contract/commit-v2.md`, with executable examples. It must define:
1. **The request:** base, commands, label, steps (with per-step patch), merge mode `fields | atomic`, declared reads, idempotency.
2. **`doc.patch` semantics:**
   - closure addressing, i.e. which document parts are addressable;
   - absent vs null, and explicit clears;
   - ordered lists and id-less lists, which must be refused or given an index rule;
   - created ids;
   - previous-value checks.
3. **Conflicts:**
   - a written field or item changed since base;
   - membership or order changed in a collection the commit read;
   - for `atomic`, anything it touched changed.

   A patch can't reveal what a script consulted. So free transforms either declare their reads, or are treated conservatively: `atomic`, conflict if the head moved for anything in the touched scope.
4. **Replies:**
   - accepted;
   - merged, with the other party's change;
   - conflict, with the reason and the head;
   - invalid, with code, path and hint.

   Also the dry-run form (extending the existing dry run, Agent `commit.py:1061`).
5. **Undo:**
   - whole-commit and per-step undo, guarded by previous values and a scan of later commits (including A→B→A);
   - a merged commit inverts against the head it landed on.
6. **`meta` namespaces:** where they sit, size and type limits, preserved verbatim.
7. **History:** labels, steps and authoritative attribution are stored and listed.

Changing the contract needs the orchestrator.

## 3. The task graph

**File ownership.** Each task names its files, and there is **one merge queue per repo**, serialised by that repo's lane. Cross-repo tasks name both repos; the repo owner merges each half.

| ID | Repo(s) and files | Task | Model | Needs |
|---|---|---|---|---|
| **C0** | runtime `contract/` | The contract above | **Sol** | — |
| **R0** | runtime `contract/` + generated clients | Publish the v2 commit wire shapes (request, replies, addressing) from commit-v2.md, and regenerate the clients (added 00:40Z; plan gap found by the App lane) | Luna | C0c |
| **U1** | runtime | Merge upstream (rerere); schema v32; regenerate contract and clients | Luna | — |
| **U2** | agent | Merge upstream (13 conflicts, rerere) | Luna | — |
| **U3** | app | Start from upstream main's editor; carry over only the outbox and what A2 needs | Luna | — |
| **U4a / U4p** | agent / app | Adopt the regenerated client and schema from U1 (re-vendor with tools); U4a in agent, U4p in app | Luna | U1, U2 / U3 |
| **R1** | **agent** `sdk/timeline/commands.py` (+ runtime store) | `doc.patch` op: apply, previous-value check, membership/order conflict, declared reads, inverse | **Sol** | C0, U2 |
| **R2** | agent provider | Guarded whole and per-step undo (inverse, scan of later commits, A→B→A); per-step patches | **Sol** | R1 |
| **R2r** | runtime store | Store label, steps and per-step patches; authoritative attribution; history listing shows them | Luna | C0, U1 |
| **R3** | agent `commit.py` | Extend the dry run; structured errors (code, path, hint, suggested command) | Luna | R1 |
| **V1** | one schema source → generated copies | `meta` namespaces; Composition and the renderer ignore unknown `meta` | Luna | C0, U1 |
| **V2** | agent provider | Validator timing and structure rules (reusing the timing compiler); element and parameter checks | Luna | R1 |
| **A2** | app | Save funnel: semantic commands or `doc.patch` through the outbox. Dependent edits chain on the local document. If a predecessor fails, dependents are re-validated against the new head, or rolled back with a message. Reply handling. | **Sol** | C0, U3 (can start before R1 is done) |
| **A3** | app | Popup add/swap, placement, element and registerAsset saves through A2 | Luna | A2 |
| **A4** | app | Delete the TS executor, capture ports, generic patch adapter and goldens; keep the behavioural tests | Luna | A2, A3 |
| **G2** | agent | `timeline.open()` / `tl.commit(label\|fn, merge, dry_run)`; bounded re-run | **Sol** | R1, U2 |
| **G3** | agent | **Document → `doc.patch` emitter** (replaces `document_diff.py` before it is deleted); helpers emit semantic commands or patches plus steps; CLI `edit`/`apply`/sheet call them | Luna | G2 |
| **G4** | agent | Move the remaining writers to commit: `replace_parent_media`, `update-element`, narration, `create_empty`, render publication | Luna | G2 |
| **G5** | agent | Delete native subparsers, `commands-file`, `apply --native`, `undo --publication`, `document_diff.py`, `store.three_way`, `publish_bundle`, separate publish | Luna | G3, G4 |
| **V3** | composition, agent, app | One Composition artifact, adopted by both consumers | Luna | U2, U3 |
| **R5** | runtime | Refuse **and directly reject** every old save route, including headless; delete the bodies; one-writer test | Luna | A3, G4 |
| **P1** | app tests + agent fixtures | **H3 feasibility set:** real documents and edits, *plus* the chain split → trim of the new clip → intervening Agent edit → lost ack → restart, covering accepted, merged and refused replies | Luna | C0 (cases early), R1 and A2 drafts to run |
| **P2** | app tests | Gesture tour: commits sent, zero old-route traffic, only intended fields changed, reload, undo | Luna | A2, A3 |
| **P3** | app tests | Gate-5 journey on the new path | Luna | A2, R2 |
| **P4** | agent tests | CLI, Python and sheet coverage: single edit; 10 notes as one commit with per-step undo; conflict and re-run; read back via show/history | Luna | G2, G3, R2 |
| **P5** | runtime + farm | Carry over the original §6 acceptance: renderer-off save, door authorisation, crash/retry points, a changed payload under the same key | Luna | R1, R2 |
| **V4** | agent, app | Optional quick deletions from the scan | Luna | — (first to cut) |
| **F** | farm | Upstream baseline at H0; full suites, tour and delivery-build dry run at H6 and H9; final run | runner | — |

**The real graph (forked, not one chain):**
1. merged baselines (U1–U3) plus C0 → U4 and V1;
2. then **R1 → R2/R3/V2/G2** on the provider side, **in parallel with A2 → A3** on the App side;
3. then the integrated journey (P1–P3);
4. then **all writer migrations (A3 and G4)** → **R5**;
5. then the final proofs (P2–P5), the farm, and packaging.

**Reserve the last 3–4 h** for final integration, gate re-runs and packaging.

**H3 go/no-go (end to end):** P1 shows that both the real-document `doc.patch` path and the App's mixed-command queue chain work, across accepted, merged and refused replies, a lost acknowledgement and a restart. If either fails, stop and re-plan before any deletions (A4, G5) start.

**H8:** re-forecast from completed integrated behaviour, not from task counts.

**Cut order if behind:** V4 → push and dashboard extras. **Never cut** writer migrations or tests of promised behaviour.

## 4. How the work runs

**The board** (`hub/BOARD.md`) is the single source of truth:
- one row per task: id, repo/files, status, dependencies, worker id, model, blocker and its owner, proof (against the integrated repo head), commit;
- managers edit their own rows only;
- the orchestrator owns the header: clock, go/no-go, decisions, cut list.

**The dashboard** is a **generated view** of the board plus dispatcher data, never hand-written. Its publication needs the owner's one-time OK.

**Manager (Claude Sonnet):**
- **On every worker completion,** with a 20–30-minute watchdog tick:
  1. Dispatch a Codex review worker for each finished task.
  2. If the review passes, dispatch a Codex merge worker into that repo's queue. The merge worker resolves conflicts, regenerates generated files and runs the targeted tests, typecheck and lint.
  3. A failure is sent back once. A second failure goes to Sol, or the task is split.
  4. Dispatch **every independent ready task** (no fixed worker count).
  5. Update the board.
- **Claude never edits product code, tests, generated files or pins.**
- **Enforcement:**
  - the dispatcher only merges through merge workers;
  - every merge records worker provenance;
  - the hourly check flags any commit without it.

**Orchestrator hourly (scripted `tick-facts`):**
- ready-but-undispatched tasks;
- blocked time per lane;
- merges per lane;
- critical-fork position against the clock;
- integrated heads green;
- merge provenance (Codex only; Sol only where flagged);
- disk and quota.

Then unblock and update the board header. Diff spot-checks are dispatched as Codex review workers, not done by Claude.

**Every 3 h (H3, H6, H9, …):**
- re-forecast;
- upstream preview **with refreshed refs**, for all four repos including Composition, where clean textual merges can still change schemas, APIs or pins. Merge consequential upstream changes early, through U-type tasks;
- old-writer grep and schema-digest equality;
- worker failure rates;
- the farm results at H6 and H9;
- two lines to the owner.

**Upstream:**
- merge at H0 (U1–U3);
- preview every 3 h;
- a short freeze before the final merge;
- re-run the gates;
- `delivery-build` squash and fresh-clone verify, then the ZIP;
- **end the freeze after final validation**;
- never rebase, never push upstream.

## 4b. Measuring progress and forecasting the finish

**Three numbers on the dashboard, all generated from the board, the dispatcher and the farm. None are self-reported.**

1. **Proof progress, the real measure.** The acceptance checklist is fixed at H1:
   - the P1–P5 scenarios;
   - the gesture-tour rows;
   - the gate items in §6 of the original plan, carried over.

   Show how many pass **on the integrated heads**, as a burn-up over time. A task that has merged without its proof passing counts as zero.
2. **Projected finish:** now + (remaining critical-fork hours × the slip factor).
   - Each task gets an estimate: S = 1–2 h, M = 2–4 h, L = 4–8 h.
   - The slip factor is actual ÷ estimated, over completed tasks.
   - The projection goes red if it is more than 20% past the target, and is reviewed at every 3-hour check.
3. **Flow:**
   - ready-but-undispatched tasks;
   - blocked hours per lane;
   - live workers;
   - merges per hour.

   This shows *why* the projection is moving.

## 5. Estimate
- **16–24 h of wall-clock is a conditional target, not a commitment.** It depends on the H3 go/no-go and on the reserved integration time.
- **Most likely stall:** A2, i.e. keeping dependent edits, guards and restart recovery working without the executor.
- **Next most likely:** R1/R2 coverage of real documents and partial undo.
