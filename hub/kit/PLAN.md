# Timeline — the plan

**Single source of truth.** Owner: Hannah (AstridPseudon). Orchestrator: Claude. Revised 2026-10-19 after two Astra reviews and a Sol code-verified cut review.
If anything elsewhere disagrees with this page, this page wins. Only the orchestrator edits it; items marked **[owner]** change only with the owner.

## In one paragraph

We are turning a good idea with messy structure into a clean foundation: **one timeline, three ways in — Read it as text, See it as images/video, Edit it through one path — all extensible.** The valuable parts of the frozen R4 project (the edit-command system, server-side rebase, timing compiler, App gesture commands, the Composition evaluator) are ported **forward onto current main** in small units; main's newer infrastructure wins; old duplicate paths are deleted. Work runs as four long-running Codex managers who dispatch Codex workers; the orchestrator trusts but verifies. The owner is involved at one hard stop (foundation complete, before extensions), gets a non-blocking summary at checkpoint A, and decides [owner] items.

---

## 1. End state (non-negotiable)

| Way in | What it means | Builds on (already on main) |
|---|---|---|
| **Read** — as text | One canonical text view for exploring and reviewing a project, for people and agents. Every text view is a projection of the one model, so they always agree. | `astrid timelines show`, `script`, `lines`, `words`, `find`, `shots`, `elements`, `inspect`, `history`, `diff`, `log`, `status` |
| **See** — visually | Frames, filmstrips, App preview and final render, all asking **one evaluator** what is on screen. | `timelines visualize` (kept and strengthened), `render`, `check`, `lint`, App preview |
| **Edit** | Every edit — App gesture, agent, CLI, Python, editable text sheet, JSON — goes through **one path**: an `EditCommand` committed to the Runtime. Every edit is validated, undoable, attributed, and safe when someone else edited first. | `timelines edit`, `apply`, `undo`, `redo`, `history`; R4's command registry |

The foundation comes first and leaves clean seams; the **five extension types** (section 4) plug into Read, See and Edit and are built last.

---

## 2. Settled decisions

1. **Port forward onto current main in small units.** No rebase of R4, no merging main into R4, no waiting until the end. R4 is frozen and used as a parts bin. **[owner]**
2. **main's infrastructure wins:** Runtime door, warm-hold host leases, platform layer, custody ABI, Astrid rename, chapters-as-shots, transcripts. R4 infrastructure is ported only when a test proves the need.
3. **One command format, `EditCommand`, and one recipe for every edit** (section 4.1). App `TimelineCommand` / `TimelinePatch` become thin builders of EditCommands (keeping gesture intent, grouping and instant local preview) or are deleted. **[owner]**
4. **Commit is a normal `/v1` Runtime-door operation** using main's `CommittedMutation` receipt. Command meaning lives in the Agent's provider, loaded by the Runtime at startup. No `/astrid/v1` side route, no gateway.
5. **Saving never needs the renderer.** A commit checks commands, document structure, timing, references and authority. Previews and checks run separately and always say which revision they show.
6. **The Runtime holds the only accepted history.** Each client keeps a small crash-safe **outbox**: unsent edits, the exact in-flight request and its retry identity, and newer local edits. Undo adds a guarded reversing edit; it never rewinds another author's work.
7. **One rebase, on the server.** Clients send *(base revision, commands)*. Newer edits that don't really clash are rebased automatically; only real clashes become conflicts. (main's three-products test, which expects a conflict, is updated.)
8. **One timing compiler** (R4's, with its timing evaluators), adopting main's rules: rational frame rates, half-open intervals, explicit time maps. Making the compiler the *only* writer of derived timing is a migration goal, verified before old paths are removed.
9. **One evaluator** for See: the Composition scene evaluator, as one published package (no vendored copies). It answers "what is on screen"; pixel/audio parity is still proven by a test.
10. **Deletions are deliverables.** Done means the old path is gone, not bypassed.
11. **Output is a ZIP** (git bundles + patch series per repo, applying cleanly to current main). Nothing is pushed to GitHub. **[owner]**
12. **Local Runtime door only** (hosted/paired relay deferred). **Linux** testing; anything macOS-only is flagged, never claimed.
13. **Extensions are the final milestone, behind the one hard stop;** their seams are designed and proven now. **[owner]**

---

## 3. Keep / cut / defer (verified against code)

### Keep
- **Agent:** `astrid/sdk/timeline/` model, commands/registry/runner, commit provider, rebase, compiler + `_timing_evaluators.py`, guarded inverse machinery (`inverse.py` — generalised, not deleted), revisions, sync; recorded writes/expectations/bindings/created IDs.
- **Runtime:** slim commit acceptance — provider compatibility check, exact reads of the media/revisions a command refers to, idempotent retry, accepted-revision identity; history and restore; immutable media-selection read (for add/swap).
- **Publication ancestry and intervening-write checks** (safe undo, detects A→B→A).
- **App:** semantic gesture producers, commit session, outbox/recovery, conflict UI.
- **Read/See tools:** `show` and the text views, `timelines visualize` including its pixel-verification lane.
- **Playback of features existing films use** (music beds, fades, transitions).
- **Local-door security:** origin, credential and project checks.

### Cut
- Scene evaluation inside the save path (~0.5k Runtime + ~1.1k Agent lines).
- R4 host custody / attestation / launch expansion (~6.0k Agent + ~1.5k Runtime added lines).
- R4 extra contract ops: capability-storage preparation, purge plan/execute, receiptless credential ops.
- Paired relay, paired route-policy generation, loopback gateway (~0.9k).
- Draft leases/expiry, retention/purge machinery (~0.5k).
- Evidence/receipt/handback decoration in product code (Runtime's real idempotency receipts stay).
- `astrid/core/timeline/inverses.py` (783, after registry inverses land) and `astrid/core/extensions/` (1.7k).
- Deprecated retime helpers in `timeline_editing.py` (relocate the useful utilities first).
- Private visibility math duplicated inside visualize (not visualize itself, not its pixel lane).
- App fallback writers and whole-document fallback save — each removed once its consumer produces commands (target: zero). Retired providers (`AstridBridgeDataProvider`, `SupabaseDataProvider`) stay dead.
- Vendored Composition copies in Agent and App (~12.6k lines), stale `dist/`, the build's failure masking (`|| true`).
- Unrelated R4 extras: chiptune planner expansion, caption-foundry demo.
- R4 tests for unported machinery and literal-criteria/receipt tests (keep every distinct behaviour; expect ~15–30k of ~135k test lines to survive).

### Defer (re-planned after stop point B from the owner's needs)
- New authoring features: story, motion, ducking, music-bed authoring, copy-sync, lint expansion.
- Hosted security (paired relay); retention/purge; generation duplication.

**Size target:** ~20–26k authored product lines for the whole consolidated core (R4 added ~73k). **Owner ruling 2026-10-20: this is a ROUGH GUIDE, not a hard limit or gate.** Balance pragmatism with solid engineering: land every planned duplicate/legacy deletion; prefer the simpler design; avoid speculative machinery and test or fixture bloat. Do NOT rewrite working main features just to hit a number. Report honest size numbers (main baseline, current, delta per area) at the hard stop.

### Process cut
95-card literal closure, IP0–IP8 gates, review budgets, receipts, ceremonial digests, handover manifests, advisory heartbeats, mandatory second opinions. R4's `docs/projects/timeline-r4/` is archived, not ported; replaced by one architecture page and runnable build/test instructions.

---

## 4. The edit recipe and the extension model

### 4.1 One recipe for every edit (core and extension)

**What the edit author writes:**
1. a **parameter schema** (with units, defaults, how to clear a value, reference pickers);
2. a **deterministic, versioned function** that applies the edit to the authored timeline — no clock, randomness or side effects; IDs it creates are allocated once and recorded;
3. **stable references** (IDs and anchors such as a word, beat, clip, cut, shot), never positions;
4. a few **declared intentions** where they apply: *ripple or not*, *follow the anchor or stay fixed*, *shared shot or this occurrence only*.

**What the framework records for each edit:** what it wrote (including writes of unchanged values), what it read and selected (membership and order), the references it bound, and the IDs it created. A plain before/after diff is not enough.

**What every edit then gets for free:**
- **Validation** — parameters, document structure, timing, references, authority.
- **Undo/redo** — restores the authored state using R4's generalised guarded inverse machinery; refuses cleanly if anyone wrote there since (including A→B→A), if something now depends on what it created, or if a selection/order it relied on changed. Derived timing is recompiled.
- **Rebase** — replays the edit's recorded intent, bindings and created IDs on the new version; conflicts only when what it read, selected or depends on really changed, unless the edit declares a merge policy.
- **Preview / dry run**, **retry safety**, **history and attribution** — from the one commit path.
- **CLI flags, App property controls and help text** generated from the schema. Gestures, keybindings and custom panels are thin adapters that emit commands.
- **A conformance harness** — author supplies fixtures and the intent to assert; the harness checks exact round-trip, deterministic replay, clears, A→B→A, structural dependencies, concurrent edits and stable created IDs, plus randomised cases.

Edits with unusual merge needs may override the defaults.

**Proof before stop point A:** small executable experiments cover ripple/insert, transitions, shared shots/occurrences (chapters-as-shots), music beds, transcript anchors, track creation/deletion, ID collisions, explicit clears, and media add/swap. M1 then proves the recipe end to end with a clip move and restart-safe retry. The **Agent manager owns this contract**, with App and Viewing managers reviewing it.

### 4.2 The five extension types

| Type | Way in | The extension author writes | What they get for free |
|---|---|---|---|
| **Commands** (absorbs macros) | Edit | an edit using the 4.1 recipe | everything in 4.1 |
| **Views** | Read, See (and Edit, if editable) | a projection of the timeline (or a region) to text or frames, pinned to a revision; includes exporters (EDL, subtitles…). Optionally **editable** *(proposal — validated in the M0 extension design: does the existing cut-sheet approach generalise?)*: also supply a parser; the framework diffs the edited text into commands through the one path (the existing cut sheet becomes a built-in editable view) | `show --view`, App panel, agent access, before/after diff of the view across revisions; for editable views, full undo/rebase via commands |
| **Elements** — sub-kinds: components, modifiers, transitions; plus reusable curves | See | a typed contract, schema, deterministic evaluation and declared capabilities | shared preview/render integration with tested parity; animation of parameters declared animatable; unknown internals reported as unknown, never guessed |
| **Checks** | Read, See | findings at references, pinned to a revision | shown in text and as visualize overlays; proposed fixes go through the one path. Advisory: never block a save (core validity rules always do) |
| **Producers** (was "generator"; includes importers) | Edit | slow/AI work (transcription, beats, generation, import) that stores immutable media/data and **proposes** edits | artifacts stored directly; timeline changes go through the commit path, reviewed or explicitly auto-approved |

### 4.3 Shared primitives the core provides early
- **References and anchors** (word, clip, cut, shot, marker) — what makes rebase work.
- **Markers** *(proposal — validated in the M0 extension design against R4's compiler/anchor code; decided at stop point A)* — any extension can publish a named, versioned set of time markers (beats, downbeats, bars, scene changes, lyric lines…) with stable IDs; any edit can anchor to any marker and follows it when the set is re-published. The timing compiler knows one generic kind, *marker*, so anchoring is extensible while the compiler stays closed and simple.
- **One selection/query language** — used by edits, views, checks and `timelines find --where`.
- **Signals** *(proposal, from the persona test)* — named, versioned time series published by producers (loudness, pitch, stem energy, motion, tracked positions). Elements can bind a parameter to a signal; views can plot them. Markers are moments; signals are curves.
- **Rationale** — every command may carry a short human/agent-readable reason; shown in history and diffs.
- **Grouping** — many edits as one undo step (a gesture, a macro, a producer's batch).
- **Namespaced, versioned extension data** at every scope (project, timeline, shot, occurrence, track, clip); unknown data preserved; each field/collection declares its migration, references and merge policy.
- **Proposals** — a reviewable batch of edits (used by producers and agents).

**Golden path — one obvious way per job:**

| I want to… | The one way |
|---|---|
| add a new kind of edit | Command |
| analyse media (beats, faces, speech, stems) | Producer -> artifacts, markers, signals, data |
| suggest edits (AI or otherwise) | Producer emitting a proposal |
| show the timeline differently (text, picture, App panel) | View |
| let people edit through a new representation | Editable View — only emits existing Commands, never defines new edits |
| add something seen or heard in the film | Element |
| make something follow music/speech/motion | anchor to markers (moments) or bind to signals (curves) |
| flag problems and suggest fixes | Check |
| attach your own info to things | namespaced data |

Tie-break rules: fast and deterministic -> Command; slow/analysing/AI -> Producer. A View presents, a Check judges (its findings appear in views automatically). Hand-authored animation -> curves; analysis-driven -> signal binding.

**Policies:** checks never block a human save, but a project may require named checks to pass before a proposal is auto-approved or before export (e.g. licence or flash-hazard checks).

**Persona validation (2026-10-19):** 10 personas x 10 ideas; one sweet-spot pick each (Foley Ghost, Stem Triggers, Corkboard argument view, Cold Open Lab, Replay Diff, Shot Match Lab, sign-language inset, kinetic subtitles, Gaze Veto, plain-text round-trip timeline) all map onto the types above once signals, rationale and policies exist. The M0 extension design must re-walk these ten against the real code.

**Future core feature (after M2, not an extension):** forks/variants of a timeline — a fork is a duplicate with ancestry; merging replays its commands via the existing rebase.

**Author experience target** *(illustrative; the M0 design proposes the actual API)*: one small manifest plus one decorated function per piece (`@command`, `@view`, `@element`, `@check`, `@producer`); `astrid ext new` scaffolds, `astrid ext test` runs the conformance harness against the author's extension. Packaging builds on main's existing pack system, not a new framework.

**Litmus examples** (M5 acceptance includes these working end to end): beat detector (producer -> markers), beat-snap (command anchoring clips to markers; clips follow when beats are re-detected), beat-grid (text view + visualize overlay), off-beat check (findings with beat-snap fix), a script/shot-list text view and an editable text view.

**Later (after M5):** automatic triggers (extensions that react to edits by editing). Checks re-run on new revisions from the start.

---

## 5. Milestones

| # | Milestone | Done when (all proven by tests on Linux unless flagged) |
|---|---|---|
| **M0** | **Groundwork** | Shared environments; main's test baselines recorded; R4 timeline core imports on main and its tests are classified; Composition builds without masking and has evaluator unit tests; App writer inventory; **edit-contract design** and **extension/primitives design**, each backed by the 4.1 hard-case experiments. **Checkpoint A (non-blocking, per owner 2026-10-19):** the orchestrator approves the two designs with a fresh Astra second opinion, records the approval on this page, sends the owner a short summary, and work continues unless the owner objects. |
| **M1** | **Walking skeleton** | A clip move from CLI, Python and App -> `/v1` commit -> survives a lost acknowledgement *and a restart* (persisted in-flight identity) with the same result -> undo works -> visible in `show` and `visualize`; commit works with the renderer off. |
| **M2** | **Widen editing** | Full registry and compiler on main; editing-conformance scenarios across CLI, Python and sheet; every App gesture produces EditCommands; outbox in place; fallback writers deleted to zero; three-products journey extended. |
| **M3** | **Unify viewing** (starts during M0) | One Composition package used by Agent and App; visualize, preview and render use it; duplicate evaluator math retired; frame + audio parity check catches a planted mismatch. |
| **M4** | **Cleanup and delivery** | Deletions complete; one architecture page; all gates green; ZIP verified to apply to fresh main. **⏸ HARD STOP (the only one) — foundation complete. Owner receives the ZIP and the gate results, and watches their almost-ready film (on a duplicate) edited end to end. Nothing in M5 starts until the owner says so.** |
| **M5** | **Extensions** | Acceptance criteria per type written and approved *before* implementation; each type implemented on the seams with at least one real example meeting its criteria; final ZIP. |

---

## 6. The seven gates (the only evidence we produce)

1. **Lossless semantics** — `tests/editing_conformance` across CLI/Python/sheet: opaque fields, explicit clears, occurrence isolation, transcript/source bindings, rational fps, half-open boundaries, deterministic timing, exact undo/redo.
2. **Atomic acceptance** — concurrent commits; stale-head rebase vs real conflict; crash before commit and after commit/before response; identical retry returns the original result; changed payload under the same key refused; no partial writes or duplicate revisions.
3. **Renderer-independent save** — commit, reload and undo with the renderer stopped; preview reports unavailability honestly.
4. **Transport** — Runtime door route/transport/lock/idempotency tests extended for `/v1` commit authorization and project scope; generated-client contract tests.
5. **Adversarial App journey** — `test:e2e:three-products`: App edit -> intervening Agent edit -> lost acknowledgement -> newer local edit -> exact retry -> restart/reload -> undo; asserts preserved intent.
6. **One writer, one viewer** — zero legacy save traffic on representative gestures (incl. popup add/swap); Player/export frame + audio comparison catches a planted mismatch.
7. **Delivery** — repository gates green, real Composition build, ZIP applies to fresh main, owner film viewing.

Every report says exactly what passed and what was not run.

---

## 7. Organisation and oversight

```
Owner (Hannah)            the hard stop before M5; [owner] decisions; notified at checkpoint A
 Orchestrator (Claude)    this page; boundaries; decisions on escalations; trust-but-verify oversight
  Manager: Runtime + delivery   commit contract, durability, generated clients, integration queue, shared envs, cross-product journeys, ZIP
  Manager: Agent editing        edit recipe + registry, compiler, rebase, inverses, CLI/SDK/sheet, Read views, conformance (owns the 4.1 contract)
  Manager: App editing          gestures, outbox, conflicts, history UI, writer deletion
  Manager: Viewing              Composition package, evaluator integration, visualize/preview/render parity, duplicate-evaluator retirement
   Workers (Codex)              one bounded task each, launched via the queue
```

**Managers are long-running** (hours to days). Each owns its area end to end, keeps going until its milestone is done or it is blocked, and:
- dispatches workers through the queue and reviews their results;
- merges good work via the merge queue (it may reject and redo);
- updates its `STATUS.md` at least every ~30 minutes: integrated head, what works now, failing tests, next steps, blockers, resource use;
- checks its `INBOX.md` regularly for orchestrator redirects and acknowledges them in STATUS;
- **escalates only** for cross-manager contract changes, data-loss/security findings, resource exhaustion, or blockers needing another owner — with a recommended decision and evidence — and keeps working meanwhile.

**Managers only see work up to the next gate.** M1+ backlog items wait until the orchestrator records checkpoint A as approved below; nothing past M4 exists in any backlog.

**Path ownership** (avoids collisions): Runtime repo -> Runtime manager. Agent `astrid/sdk/timeline*`, `astrid/packs/timeline/` (except visualize) -> Agent manager. App `src/tools/video-editor/` (except preview/player/render), `src/integrations/runtime/` -> App manager. Composition repo, Agent `astrid/packs/rendering/` + `remotion/`, App preview/player/render/vendor composition -> Viewing manager. Shared files change via their owner.

**Orchestrator oversight — trust but verify:**
- **Hourly (light):** read the one-screen digest — progress (new merges), managers alive, failed/stuck workers, disk, open escalations. If it is moving, do nothing. Restart a dead manager; decide escalations.
- **Every 3 hours (deep):** a fresh audit sub-agent reviews merges since the last audit against this page — direction, minimality/bloat, deletions really happening, tests that really test, drift from the end state. The orchestrator reads its short verdict and redirects through manager inboxes only where needed.
- **About daily:** refresh main into `tl/integration`, re-run gates.
- The owner hears from the orchestrator at stop points, for [owner] decisions, or if something is seriously off.

**Models:** managers Sol 6.1 high; normal workers Luna xhigh; hard coupled workers Sol 6.1 high; Astra only for genuinely contested decisions.

---

## 8. Mechanics (tested)

- **Integration branches** `tl/integration` in `/home/user/work/{agent,runtime,app,composition}` — main snapshot Agent `e51595c6`, Runtime `8c1830d`, App `60aa26b95`; Composition from R4 `c82eb7c`.
- **Workers** each get a git worktree `/home/user/work/wt/<name>` (branch `tl/<name>`). Heavy dependencies are shared: `/home/user/work/venv-{agent,runtime}`, App `node_modules` once in `/home/user/work/app` (symlinked).
- **Tools** (`orch/bin/`): `request` (queue a worker), `request-merge` (queue a merge), `workers` (status table), `digest` (hourly summary); run by the always-on `dispatcher-daemon` outside any sandbox, which enforces free-disk ≥ 5 GB and ≤ 2 concurrent heavy jobs, with per-worker timeouts.
- **Commits:** Codex sandboxes keep `.git` read-only, so workers never commit; they write a commit message file and the harness commits their worktree when they exit. Merges into `tl/integration` happen only through the merge queue (serialized per repo; conflicts abort cleanly and come back to the manager).
- **Delivery:** ZIP of git bundles + patch series per repo, after refreshing onto current main and re-running the gates.
- **Frozen R4 refs:** `origin/codex/handover-timeline-r4-20261019-*`. Research reports: `../luna/reports/`.

## Glossary
- **EditCommand** — one named, typed edit (e.g. move clip, trim, add media) in the single command format.
- **Commit** — sending edits to the Runtime, which checks them against the revision they were made on and records them atomically.
- **Rebase** — re-applying an edit on top of someone else's newer change.
- **Outbox** — a client's crash-safe list of edits not yet confirmed by the Runtime.
- **Evaluator** — the one piece of code that answers "what is on screen at this frame".
- **Stop point** — a pause where the owner reviews before work continues.

---

## Decisions log (orchestrator)
- 2026-10-19: Commit contract: Runtime's reconciliation approved; provider ABI v2 only if main's ABI can't carry it. Agent owns the command schema and inverse/restore args; Runtime owns request/port DTOs.
- 2026-10-19: App manager also owns the popup shotTimelineDataProvider, the shared placementService and the Supabase timeline producers (astridAppendService + callers). All become EditCommand producers on the one commit path; relational placement metadata is out of M2 scope.
- 2026-10-19: Viewing (M3) moves the App's 13 static default components (text-card, animations, transitions, 2rp theme effects) into canonical Composition source, registered via the normal element seam. App deletes its copies and owns its package/lock edits. Tarball 0.0.8, Remotion 4.0.509.
- 2026-10-19: Dependent edits. The client keeps B (authored over unacked A) unsent until A is acked, then submits it at base HA with its ORIGINAL value+identity guards; the server verifies them or reports a conflict. Equal-state ABA is not a conflict. No new DTO field unless an executable user-visible counterexample appears.
- 2026-10-19: Checkpoint A design review (Astra): direction approved with 5 required changes plus cheap wins. See reviews/checkpoint-a-changes.md. Markers/signals before the hard stop = reference/resolver interfaces + fixtures only; missing marker fails closed. Gate 6 includes direct legacy-endpoint rejection.
- 2026-10-19: M2 groups = option A. Canonical shot ownership is the single representation. pinnedShotGroups is migration-only, through a recorded, guarded, lossless migration command (unsupported shapes refused). Retrack updates occurrence-owned child tracks atomically. App gets a read-side legacy group view. (reviews/astra-m2-groups.md)
- 2026-10-19: M1 exit = central e2e-m1-gesture pass + restored App journeys + restore preservation (Runtime/Agent, and App restoreHistory head pair) + all new full-suite failures classified + deep audit without blocking findings + mixed-editing data safety (move then ordinary edit: success or visible refusal with draft kept, never silent loss). M2 priority #1: migrate all remaining App writers to EditCommands. Also M1: atomic refusal when a projection destination is occupied by an unrelated row (proven same-project overwrite), with a permanent regression test.
- 2026-10-19: canonical clip.transition = INCOMING for every producer; the canonical→compiled compiler converts explicitly to the compiled outgoing form; Agent validator fixed; any historical Agent outgoing-meaning data only via a recorded guarded migration.
- 2026-10-19 (OWNER): purge all Supabase canonical timeline writers (ai-timeline-agent, timeline-import, complete_task append + registry upsert, astridAppendService); keep task completion/billing/media prep/relational metadata.
- 2026-10-19 (OWNER intent): everything contradicting the end state is deleted, tracked in design/deletion-ledger.md; each milestone exits only when its ledger rows are DELETED.
- 2026-10-20: render/assembler producers never commit. They return EditCommands as a proposal; the requesting client commits it with its own authority, with task/attempt fencing as commit guards. Historical render uses an explicit immutable revision+receipt selector, additive to the existing admission spec.
- 2026-10-20: word/transcript anchors store their stable word identity in the authored document (with the transcript pin), so the revision alone determines meaning. Restore stays revision-based. Ambiguous text-only anchors refuse.
- 2026-10-20: capture certification reuses the ONE existing Agent projector (project_runtime_parent_composition) through an additive optional pure method on the existing startup-loaded semantic provider; Runtime verifies scope, digests and retained inputs and compares before publishing. Working-copy certification needs the real authoring_preview candidate forwarded as plain task data; without it, preview is cas-only and labelled UNCERTIFIED. No second projector, no new DTO or endpoint.

- 2026-10-20: audio gain envelopes use ONE continuous policy (the public applyAudioEnvelope, gain evaluated per PCM source time) for BOTH App preview and normal Agent export. The old per-frame step-hold (up to ~0.7 dB off mid-fade) is retired as a deliberate improvement with a ledger row; readiness, retry, mute and amplify behaviour are kept.
- 2026-10-20 (owner review at the hard stop): the continuous audio-gain policy audibly changes export audio for existing films with fades, by up to ~0.7 dB mid-fade. Show the owner this in the film-viewing steps.
- 2026-10-20 (REVISED ~04:02Z): element/custom-effect clips GET the clip look (opacity, crop, fades, entrance/exit), with dissolve vs dip per boundary. This follows the owner's own Composition release v0.0.7 (6bd784d, AstridPseudon, 2026-10-10: "clip look ... on element clips; per-boundary transitions (dissolve vs dip ...)"), which main never adopted; main's pinned 0.0.6 mounts effect clips bare. It is an INTENDED, documented difference from main, not lost behaviour: independent fades on overlapping element clips now DIP (the 16-30 golden is approved as intended). The proof must name the difference: MAIN replay from v0.0.6 (git archive reproduces main's locked sha512) against the unified result, showing exactly the intended change and nothing else. Owner review at the hard stop: list the owner's films with overlapping element clips that use fades/opacity/entrance-exit.
- 2026-10-20: fade curve= is HONOURED in the unified path (the public package's fadeInCurve/fadeOutCurve). Main parses curve=NAME (clip_fields.py:358) and then drops it, so main's fades are always linear; the author's request wins, consistent with the owner's composition package. It audibly or visibly changes films that use curve=; Viewing/Agent scan the owner's films and list them for the hard-stop viewing.
- 2026-10-20: route retirement follows consumer migration. A Runtime route that a not-yet-migrated consumer (App, or a fixture) still calls is retired only in the same gated step that lands that consumer's qualified replacement. Retiring it earlier is a sequencing error and gets restored narrowly; safety guards such as the non-empty headless DENY stay.
- 2026-10-20 (FINAL ~06:20Z, supersedes 05:55 and 06:05): implicit default theme. There is ONE authority, the public Composition DEFAULT_THEME, and its VALUE becomes the EXISTING final-export style (Agent builtin banodoco-default: navy #050814 / Arial / cyan, the full object), published in composition 0.0.12 (0.0.11 is already immutable with the trim/rate exports) as part of the planned coordinated pair. Exported films therefore do not change. Agent's core default constant (astrid/core/theme/_schema.py) is derived from or equal to that one object; there are no two definitions under the same ID. The App preview implicit default changes from black/Georgia/white to that style (intended, documented, on the owner-film list). Explicit film themes are always preserved.
- 2026-10-20: delivery format (M4/hard stop). Per repo: (a) a LINEARIZED patch series against the current origin/main, made from `git diff origin/main tl/integration --binary` and split into a few reviewable squashed patches, VERIFIED by applying them to a fresh clone of main and getting a tree byte-equal to tl/integration; (b) a git bundle of tl/integration. format-patch of the merge history is not the deliverable. Composition's integration has an unrelated root: Viewing joins it to origin/main with an `-s ours` merge of 67b8aa3, after proving main's tree is fully represented, so that refresh-main works.
- 2026-10-20: single-occurrence image cap = the STORED value (main reads 4000 ms directly; f105 opacity 0.5). App's derived 5000 ms cap is a bug. (Viewing confirmation 12:40Z.)
- 2026-10-20: giant-file inventory drift from Timeline changes: never loosen the 1200/50 thresholds; the default is a pure extraction of the Timeline-added code into a cohesive helper, back within 50; a truthful entry update (count plus a one-line reason) only when the code belongs there and extraction would split one cohesive function, with main-vs-current diff evidence. The source owner fixes it; inventory green is required at M4.
- 2026-10-20: the size-target boundary (~20-26k authored product lines) counts the TIMELINE CORE only: the authored product code that implements Read/See/Edit for timelines in all four repos (edit commands, commit path, compiler/projector, evaluator, timeline adapters/UI writers, text views). It excludes untouched main infrastructure (Runtime worker/execution, generic astrid_runtime, packs unrelated to timelines), generated contract data and clients, and tests. Each area reports a census with this boundary at M4 (main baseline for those paths, then current, then the delta).
## Gate record (orchestrator updates this)
- Checkpoint A (designs approved): **APPROVED 2026-10-19 ~19:05Z** by the orchestrator, after a fresh Astra review (APPROVE WITH CHANGES; all 5 required changes folded into the design docs; see reviews/checkpoint-a-changes.md). Runtime, App and Viewing M0 complete; Agent designs complete, with its main-baseline count still being recorded (non-blocking). **M1 is open.**
- M1 (one edit path proven; data safety): **RECORDED 2026-10-20 ~03:55Z** by the orchestrator. Integration tuple: Agent 4a75f68f, Runtime 4bb1d0f7, App c8566f12d, Composition c04ada57.
  - Evidence: central e2e-m1-gesture 1019211905-11848 pass; restored App journeys and restoreHistory head pair; Runtime/Agent restore preservation; mixed-editing safety; occupied-destination atomic refusal (Runtime 9f9b25c) with a permanent Agent test; opaque item-reference preservation (Agent a76c6537 + App parity c8566f12d); numeric image reuse (4a75f68f); null speed (4bb1d0f7).
  - Fulls, all classified with 0 new failures: Runtime 1020021911-13639 (3829 pass / 7 baseline); App 1020025341-10022 (18336 pass / 6 baseline); Agent 1020031037-28578 (11732 pass / 79 fail / 30 error, exactly the 109-node supported-env baseline, which was proven identical on f6fbe741 and 4a75 by 1020030741-1883 and 1020030717-18201).
  - Deep audit 20261020T0350Z: CONCERNS, none blocking M1.
  - Open follow-up: Viewing re-verifies any cited pass that ran during its lead's snapshot-deleting check-ins; a cited pass that does not reproduce reopens that item.
  - M2 merges are OPEN, one gated branch at a time.
- Hard stop (foundation complete, M0–M4 done): **NOT YET**
