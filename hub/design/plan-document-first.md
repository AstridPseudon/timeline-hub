# Timeline: the document-first plan (proposal v1, 22 Oct)

*Status:*
- *This is a proposal for the owner. Nothing is built, and the project stays paused.*
- *It replaces the editing design and the work packages WP3–WP6 and WP9 in `scope-of-work-90-10.md`. The merge, delivery, farm and process sections there (WP1, WP2, WP10, WP11, §1, §15–§18) still apply unless this page says otherwise.*
- *It **reverses two settled owner decisions** in the original PLAN.md (§2 decisions 3 and 7, and the §4.1 recipe: "a plain before/after diff is not enough"). §8 explains how this design covers what those decisions protected.*

## 0. In one paragraph
The timeline is a document, and anyone may edit it freely: the App, the Agent, a script, a text sheet, a future extension. A save sends the version you started from, the new document (or a patch), a label, and optionally the steps that produced it, with their intent. **Runtime is the only writer.** It computes the exact change itself, validates the whole resulting document, merges it with anything that landed meanwhile, and records it as one commit. Undo and history work on those recorded changes.

The steps are provenance. They give rich history, and they let a step be re-applied when one can be, but they are never required and never a gatekeeper. Nothing is refused except an invalid document or a real clash on the same thing. New kinds of data live in an open metadata area, with no schema change and no new command.

## 1. What it must satisfy

**The original end state (PLAN.md §1):**
- **Read:** one model, many text views.
- **See:** one evaluator, from preview to render.
- **Edit:** one path. Every edit is validated, undoable, attributed, and safe when someone else edited first.

**The seven gates (PLAN.md §6):**
1. lossless semantics;
2. atomic acceptance;
3. renderer-independent save;
4. transport;
5. the adversarial App journey;
6. one writer, one viewer;
7. delivery.

**The owner's goals (22 Oct):**
- as simple and elegant as possible, with nothing built only to be removed;
- the edit logic exists once;
- maximum agent flexibility (e.g. "align every clip to audio activity, add beat metadata, match to image cuts");
- a fast, smooth front end;
- all coding on Codex;
- the cloud version later, as the normal Runtime with normal SQLite, one container per user, on the owner's domain, with minimal cloud-specific code;
- a shippable version in about 12 hours of agent work if possible.

**Future (M5 and beyond), from PLAN.md §4:**
- **Extension types:** commands, views (including editable views), elements, checks, producers.
- **Shared primitives:** references and anchors, markers, signals, rationale, grouping, namespaced data, proposals.
- **Later:** forks and variants; triggers.

## 2. The core design

### 2.1 A commit
```
POST /v1/projects/{p}/timelines/{t}/commit
  base:      revision id I started from
  change:    the full new document, or a patch against base, plus a fingerprint of the expected result
  label:     "Align clips to beats"                           (optional, free text)
  actor:     app | agent | script | extension:<id>             (attributed by Runtime, not trusted from the body)
  steps:     optional list, any length
    - id, kind: command | code | gesture | note
      what:    e.g. split {clip c4, at 12.4}; "script sha256:…"; "dragged c7 to track 2"
      intent:  free text
      tags:    free-form strings
      touches: optional ids
      replay:  optional: a re-applicable command, or a per-step patch
  idempotency-key header
```

### 2.2 What Runtime does, in one transaction
1. **Load the base,** resolve the candidate, and compute the diff: field set, field removed, and list items added, removed or moved by id.
2. **Validate the whole result:**
   - **Strict:** the schema of the core fields (timing, media references, track and clip structure, shots and occurrences), referential integrity, and a timing compile check.
   - **Open:** the `meta` namespaces on project, timeline, shot, occurrence, track and clip, which take any JSON.
3. **If the head has moved since base,** run a three-way merge at field and item level:
   - **Non-overlapping changes** merge automatically.
   - **A real clash** (the same field or item changed on both sides) returns a conflict with the current head. If the commit's steps can be replayed, Runtime may re-apply them on the new head instead.
   - **Bulk-change rule:** a commit that touches more than N items, or declares `atomic`, conflicts if *any* item it touched changed since its base. The client then re-runs its transformation on the new head.
4. **Store the commit:**
   - **content:** the diff, label, steps and actor;
   - **identity:** a new revision and the idempotency record;
   - **pointer:** the head moves through the existing compare-and-set.
5. **Notify subscribers** (push; see §3).

**Reused from today's integration branch:**
- the commit ledger and idempotency (primary-key based);
- the head compare-and-set;
- the history listing;
- revisions;
- the door;
- the renderer-independent save;
- the refusals of the old routes.

**Replaced:**
- the command vocabulary as the *protocol*;
- the App's native capture layer and its TypeScript executor copy;
- the App's generic patch adapter;
- the client-computed `reads`/`expect`.

**New:**
- a document diff with id-keyed lists;
- the full-document validator, consolidating the checks that exist today;
- the field-level merge;
- steps storage;
- push notification.

### 2.3 Undo and redo
- **Undo:** a new commit that applies the inverse of a recorded change, guarded: it is refused if anything it would revert has changed since, including A→B→A. Undo of one step inside a commit works when that step carried `replay`.
- **Redo** works the same way.
- **History** never rewinds; it only adds.

### 2.4 Commands become a helper library, not a protocol
- `split`, `trim`, `move`, `align_to_markers` and the like are ordinary functions, in Python for the Agent and TypeScript for the App. They edit a document and return a step description.
- **They don't have to match each other exactly.** Runtime validates results, not implementations.
- Anyone, including M5 extensions, can add helpers without touching Runtime.

### 2.5 Anchors, markers and signals are data
- **Markers:** beats, downbeats or scene changes are named, versioned marker sets, stored in the document or as artifacts referenced from it.
- **Anchored values:** a clip's start can be anchored to a marker id.
- **Following an anchor:** the timing compiler resolves anchors. When a producer re-publishes a marker set, the anchored clips follow because the compile result changes, not because an edit is replayed.
- **Signals:** named time series, referenced the same way.

### 2.6 Speed and the front end
- The editor holds the document locally. Gestures change it locally every frame, at 60 fps with no network involved.
- On release, the editor updates at once and queues a commit (base, patch, step), with consecutive small edits grouped together.
- The queue is persisted in IndexedDB and sends in order with idempotency keys. The next gesture builds on the local state straight away.
- **Replies:**
  - **accepted:** the revision number moves on;
  - **merged:** the reply includes the other party's change, and the editor applies it;
  - **conflict or invalid:** that step is rolled back on screen with a message.
- **Push from Runtime** (long-poll or SSE) replaces the 30-second head poll, so Agent edits appear in the open App within about a second.

### 2.7 How the Agent edits (detail to come from the UX review)
- **Simple edits:** `timelines edit move c4 --to 12.4`. Internally this is the helper, then a commit.
- **Complex edits:** a script that loads the document, transforms it freely, and commits with a label and optional steps. On a conflict, the script re-runs on the new head.
- **Working copies** (checkout, edit, publish) are just a local document plus base. A copy that has fallen behind is merged by Runtime or re-run; a stale copy is no longer refused by design.
- **Producers** (beats, transcription) write artifacts and marker sets, then commit, or propose a commit for review.

## 3. What this removes compared with the current integration branch

| Removed | Size | Why it goes |
|---|---|---|
| App TypeScript edit executor and capture ports | ~12.8k lines | No client must mirror the server |
| Its golden fixtures | ~45–56k lines | Same |
| App generic patch capture and the three edit vocabularies | | One way to save |
| The command vocabulary as a gate | | Becomes the helper library |
| Hand-run parity regenerators | | Nothing left to keep in step |
| Edit-command schema copies | | Now only internal to the helper library |

Most of the App's 55-conflict merge goes too, because the App returns close to upstream main's editor plus a new save call.

The Python edit core stays as the Agent's helper library. It no longer has to move into Runtime, which saves Opus's estimated 10–16 hours for untangling element and kind admission.

## 4. Execution: the 12–20-hour version (five machines, all coding on Codex, managers on Claude)

| When | Lane | Work |
|---|---|---|
| H0–1 | orchestrator | Restart; the owner decisions in §9; the task board; fetch main |
| H0–6 | **Runtime (Sol, critical path)** | The document-commit mode: diff, validator, field merge, steps storage, idempotency reuse, and the guarded inverse for undo. **Go/no-go at H4** on validator and merge coverage of real App documents. |
| H0–3 | Runtime | Merge upstream, schema v32, push notification |
| H0–5 | App | Start from upstream main's editor. The save funnel and popup writer call `/commit` with base, patch and step. Add a persisted queue, the reply handling and push. Delete the TS executor and capture layer. |
| H0–5 | Agent | Merge upstream. `publish_bundle`, `replace_parent_media`, `create_empty`, the voiceover and text-binding writers, and the render publication all go through `/commit` (document form). The native command path becomes the helper library and commits documents. |
| H2–6 | Runtime | Refuse the old routes, delete their bodies, and run the one-writer test |
| H3–8 | App (Child 3) | Gesture tour on `three-products`: per gesture, the commit sent, zero old-route traffic, only the intended fields changed, then reload and undo; plus the existing gate-5 journey |
| H6–10 | farm | Full suites, the tour, the delivery-build dry run |
| H10–12+ | orchestrator | Final refresh, ZIP, the owner's viewing on a duplicate film |

**Out of the 12-hour scope** (they follow later):
- the physical preview/export parity (gate 6, second half);
- the viewing rows;
- renderer consolidation;
- markers and signals as first-class primitives (they work as `meta` data meanwhile).

## 5. Gates under this design
1. **Lossless semantics.** The exact document round-trip *is* the commit check. Kept: explicit clears (null vs absent), opaque fields, rational fps, half-open intervals, undo/redo. Occurrence isolation becomes a validator rule.
2. **Atomic acceptance.** Unchanged machinery: concurrency, crash points, identical retry, a changed payload under the same key.
3. **Renderer-independent save.** Unchanged.
4. **Transport.** Extended to the document-commit form.
5. **Adversarial App journey.** Same sequence. It asserts the preserved *result*, and the label and steps in history.
6. **One writer:** zero old-route traffic, proved by the tour. **One viewer** (physical parity): scheduled after the 12-hour ship.
7. **Delivery.** Unchanged.

## 6. Risks
1. **Validator coverage and quality.** It is now the main safety net. Unknown until H4.
2. **Merge semantics for id-keyed lists:** order moves, nested shots and occurrences.
3. **Coarser semantic merging** than intent replay. Mitigated by the bulk-change rule, re-runs and optional replayable steps.
4. **Document size.** Patches plus fingerprints keep payloads small.
5. **Upstream drift.** The App starting from main reduces it sharply.
6. **Sunk cost:** about two days of native App gesture work is deleted.

## 7. Future fit
- **M5 extension types:**
  - commands become helpers plus optional replayable steps;
  - views and editable views emit documents or patches, so no command is needed;
  - elements are schema plus evaluator;
  - checks read the document;
  - producers write artifacts and markers, then commit or propose.
- **Proposals** are uncommitted commits held for review.
- **Forks and variants:** a duplicate with ancestry, merged with the same three-way merge.
- **Triggers:** react to the push stream.
- **Cloud:** the normal Runtime and SQLite per container. The plan's rules carry over: plain-SQL migrations, correctness not resting on the in-process lock, media through object routes.

## 8. Reversing PLAN.md decisions 3 and 7: what they protected, and how this covers it

| Protected | How it is covered here |
|---|---|
| **Intent-preserving rebase:** "replays recorded intent, bindings and created ids" | Field and item-level three-way merge by default. Steps can be replayed when they carry `replay`. Bulk edits re-run on conflict. Anchors are data, so they follow through compilation, not replay. |
| **Guarded undo:** refuse if anyone wrote there since, A→B→A, dependents, selection or order changed | A guarded inverse over the recorded diff: refuse if any reverted field or item changed since, or if a created item is now referenced. Selection and order dependence is only partly covered: only if the step recorded `touches` or `replay`. |
| **Generated CLI flags and App controls from command schemas** | Helpers may still declare parameter schemas, but that is optional and not part of the protocol. |
| **"A diff is not enough"** (reads, selections, bindings) | Accepted as a trade-off. Recorded steps restore it where it matters. |

## 9. Owner decisions needed
1. Adopt document-first, reversing PLAN.md decisions 3 and 7.
2. The 12–20-hour scope in §4, with gate 6 parity and the viewing rows after the ship.
3. Delete the App's native gesture layer and TS executor.
4. Open `meta` namespaces with no schema change for new data.
5. The bulk-change conflict rule (threshold N, or explicit `atomic`).

---

## 10. Revision after the two Opus reviews (22 Oct): the hybrid

**Reviews:** `review-20261022/opus-docfirst-requirements.md` and `review-20261022/opus-agent-ux.md`.
- The requirements review judged the pure document-first plan at about 30–45 h, not 12–20 h. The cause is a second commit system built beside one that already does most of the job.
- Verified in code:
  - the store refuses a commit that has no command records (`timeline_commit_store.py:602`);
  - the integration outbox does not care what the payload is (`commitOutbox.ts`);
  - all edit meaning sits in the Agent provider, executed by Runtime.

### The design, revised
1. **Keep the existing Runtime commit engine and `EditCommand` records.** The ledger, idempotency, head CAS, guarded undo, rebase and producer guards all carry over unchanged.
2. **Add one generic op, `doc.patch`.** It carries id-addressed changes (set, remove, list insert/remove/move), and each change carries its *before* value.
   - Any change to the document can be saved, so nothing is refused for lack of a command.
   - The before values make undo and conflict detection exact, including A→B→A, through a scan of later commits.
3. **Semantic edits exist only in Python,** in the Agent provider that Runtime executes: split, ripple, per-occurrence fork, align-to-markers and similar.
   - The App sends either a semantic op (for split, ripple and per-occurrence edits) or a `doc.patch`, and shows a local preview with main's editor logic.
   - The server's result wins. There is no byte-identical TypeScript executor and no golden fixtures.
4. **Close the silent-merge holes:**
   - a commit conflicts if a collection it read changed membership or order (the Python executor already computes reads and selections, `commands.py:228-248`);
   - ripple and per-occurrence edits are sent as ops, never as patches;
   - snaps use anchors;
   - clears and removals are explicit.
5. **Gate 5:** reuse the existing outbox (persisted, payload-agnostic). There is no "keep my changes" overwrite button.
6. **No server-side step replay in v1.** Labels and steps are stored for history; per-step patches are kept for partial undo.
7. **Agent golden path** (from the UX review):
   - CLI verbs: show, find, diff, history, visualize; edit, apply, undo, redo, commit; watch later;
   - Python: `tl = timeline.open()`, then helpers or free edits, then `tl.commit(label | fn, merge="fields"|"atomic", dry_run=, propose=)`;
   - committing a function lets the SDK re-run it on a conflict;
   - Runtime does the dry run;
   - every error carries a code, path, hint and a suggested command.
8. **An explicit merge mode** (`fields` | `atomic`) replaces the "more than N items" rule.
9. **Estimate:** 16–24 h (Opus: "plausible"), with the go/no-go at **H3**. Gate 6 parity is a deferral the owner signs.
10. **After the ship:**
    - anchors as core timing fields, with pinned marker sets;
    - proposals and `watch`;
    - push;
    - gate 6 parity;
    - the viewing rows;
    - the M5 extension model, rebased on "Python semantic ops plus `doc.patch`".
