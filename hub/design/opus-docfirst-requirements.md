# Document-first plan: requirements check (Opus, 22 Oct)

*Read-only. No Agent tool was available, so I read the code myself. **Facts** (F1–F10) carry file:line at the integration heads or `origin/main`. The rest is **judgement**.*

## Verdict
The direction is right: clients edit freely, Runtime is the only writer, and the TS executor goes. But the plan builds a second commit system beside one that already does most of the job. Runtime's record, undo, producer and materialization checks are all keyed to command records. The server executor already works out reads and selections itself, so clients never needed to send them. The cheaper design keeps commands as the recorded unit and adds **one generic `doc.patch` command**: id-addressed field and list writes, each carrying its "before" value. Ledger, history, guarded undo, rebase and producer guards then carry over unchanged. As written, 12–20 h is not credible (about 30–45 h). The hybrid makes about 16–24 h plausible.

## Verified facts
- **F1.** Edit meaning lives in the Agent provider: `provider.commit` (`timeline_commit_execution.py:87`), validated by the Agent compiler (`commit.py:14-20`). Runtime's own check is structural (`timeline_commit_store.py:473-589`).
- **F2.** The store refuses a commit with no command records (`timeline_commit_store.py:602`). About 63 places in store, port, materialization and producer code read command records (grep count), e.g. the producer guard (`timeline_commit_port.py:393-400`).
- **F3.** The executor recaptures records itself (`commands.py:228`) and checks client-sent reads or expectations only when they are present (`:229-248`). In the contract they are `NotRequired` (`timeline_commit_types.py:32`). Bare `{op, select, args}` already works.
- **F4.** Rebase is command replay inside a three-attempt CAS loop (`commit.py:1023,1044`). Undo guards use recorded writes (`check_intervening`, `commit.py:985`).
- **F5.** Main already has a three-way merge, but at unit level: a whole clip is one unit, and merged clips are appended at the end, so order is lost (`agent store.py:253`).
- **F6.** Main's App already POSTs the whole parent composition with `expected_head` (`dataProvider.ts:844`, `shot_revisions: []` at `:855`). Its retry record is in memory only (`:819`), and it refuses a newer edit while a save is unacknowledged (`:772`). Upstream had to fix the editor dropping unknown registry fields (313804005, cb98e249b).
- **F7.** Main's gate-5 journey expects a "Keep my changes" conflict dialog (`three-products.spec.ts:405,471-475`).
- **F8.** The integration outbox (551 lines) does not care what the payload is (`commitOutbox.ts:22`) and supports chained edits (`{after: intentId}`, `:16`).
- **F9.** Runtime has no push or streaming (`server.py:9,66`, door).
- **F10.** The stored "document" is a closure, not one JSON: the parent payload, content-addressed shot and internal revisions, and a manifest (`timeline_commit_store.py:478-484`).

## Requirements table
| Requirement | Status | Why | Fix |
|---|---|---|---|
| G1 lossless | **Risk** | Full-document mode makes Runtime accept silent deletes from a lossy client (F6). "Occurrence isolation as a validator rule" can't be defined, because a valid document doesn't show whether a shared change was meant. | App sends patches only. Removal is explicit only. Isolation is proved on the shot-edit helper and op, not the validator. |
| G2 atomic | **Met / risk** | Ledger, idempotency and CAS are generic (`store.py:1103`). The record shape is not (F2). | Keep command records (top change 1). |
| G3 renderer-free | **Met** | Compiler only. | — |
| G4 transport | **Risk** | New contract shapes change the digest and every lock. Push through the door is new (F9). | Push = long-poll on `listEvents`. Keep `CommitRequest` and add one op. |
| G5 App journey | **Not met as written** | Main has no durable queue and blocks chained edits (F6). "Keep my changes" would overwrite the Agent's edit (F7). "Preserved intent" is weakened to "preserved result". | Port `commitOutbox.ts` (F8). Remove the overwrite button. Rebase per patch against the server, not a predicted base. |
| G6 one writer / one viewer | **Risk / not met** | Route refusals carry over. Physical parity is deferred, so M4 is not complete. | Owner signs the deferral explicitly. |
| G7 delivery | **Met** | Unchanged; upstream merges still needed. | — |
| §1 Edit, one path | **Met (redefined)** | It is one route, but reverses "an EditCommand". | The hybrid keeps EditCommand. |
| Edit logic once | **Not met** | §2.4 lets TS and Python helpers differ. Semantic edits then exist twice. | Semantic ops exist only in Python. The App previews and sends ops or patches. |
| Agent flexibility | **Met, better** | Scripts transform freely. | Generalise `document_diff.py` into a `doc.patch` emitter. |
| Fast front end | **Met** | Local edits plus a queue. | — |
| Cloud | **Met** | No storage change. | — |
| Anchors, markers, signals | **Easier** | They are data that the compiler resolves. The PLAN already said so (§4.3). | — |
| Rationale, grouping | **Easier** | Label and steps. | — |
| Namespaced data | **Easier, risk** | Open `meta` has no declared references, so dangling ids after a delete pass validation and the undo dependents check. | `meta.<ns>`, plus optional declared reference paths. |
| Proposals | **Harder** | A stale patch proposal merges coarsely, and its intent is lost. | Proposals carry ops where they exist. |
| Forks / variants | **Easier to build, weaker** | A long-lived fork means bulk-rule conflicts everywhere. | Merge forks op by op where replayable. |
| Triggers | **Easier** | Push stream. | Add an actor-loop guard. |
| Impossible? | **None** | Undoing one step inside a commit, and detecting a changed selection, need `replay`. | — |

## What the reversal loses (real cases)
- **Related clips.** The App trims c4's end; the Agent sets c5 to start at c4's old end. Different fields, so it merges silently into a gap or overlap. Only an anchor saves it.
- **Ripple.** The App ripples c5–c9; the Agent meanwhile adds c10 after them. c10 isn't in the App's diff, so the bulk rule doesn't fire and c10 lands unshifted. Command replay re-ripples it.
- **Shared shot.** The Agent edits shared shot S; the App forks o2 to S′ for "this occurrence only". No field clash, so o2 silently loses the Agent's change.
- **Selection.** "Align all clips to audio activity" plus a concurrent add leaves the new clip out. `touches` lists written items, not membership.
- **A→B→A undo.** Works only if the guard scans later diffs for the same path; comparing values misses A→B→C→B. A *merged* commit must be inverted against the head it landed on. Unchanged-value writes are lost.

The §8 mitigations miss the ripple and selection cases.

**Cheap fix:** record the collections a commit touched; a bulk or `atomic` commit conflicts if their membership or order changed since base. Ripple and per-occurrence edits go as ops.

## Can it be built, and how long?
**Carries over (fact):**
- the idempotency coordinator;
- the ledger and receipts;
- head CAS;
- the history table and listing;
- closure persistence and validation.

**Doesn't carry over:**
- the record-shaped checks (F2);
- the inverse and replay engine (F4);
- the contract.

**The new validator must add** element-parameter admission against pack snapshots for every changed clip. Today that check is per command (`commit.py:483-565`). It still needs Agent code, so the claimed 10–16 h saving is deferred, not removed.

**Is "main's editor plus a save call" realistic?** Partly: the save is already document-shaped (F6), but it needs the outbox, chaining, reply merge, push and conflict UI.

**Estimate (judgement):**
- Runtime lane: 20–30 h, done one after another (diff over the closure, validator, ordered-list merge, records, undo, push, contract).
- With the merges, the App (8–14 h), the Agent writers, the tour and delivery: 30–45 h of wall clock.
- **Critical item:** deciding what a document commit *records*, so that undo, merge, producer guards and materializations still hold. Second: the go/no-go on real App documents (decide by H3, not H4).

**The better hybrid.** `doc.patch` is one more registered op. Its replay is "apply if the before-values still hold", which *is* the field merge. Its writes feed the existing guarded undo.
- The App sends `doc.patch` from main's editor, plus bare ops for split, ripple and per-occurrence edits.
- The Agent sends ops or `doc.patch` from scripts.
- New Runtime work: about 4–6 h for the op, plus 2–4 h for push.

## Top 5 changes
1. **Keep EditCommand as the recorded unit and add `doc.patch`.** A patch is id-addressed, with before-values and list insert, remove and move by id. Full documents are diffed into `doc.patch` on the client. Drop "Runtime may replay steps" from v1, so only one rebase mechanism exists.
2. **Semantic edits exist once, in Python.** The App sends bare ops (F3) with its local preview, and has no TS helpers.
3. **Close the silent-merge holes.** Conflict on changed collection membership or order for bulk and atomic commits. Express ripple and per-occurrence edits as ops. Turn relational snaps into anchors. Use explicit clears and removals. Invert against the head the commit landed on.
4. **Make gate 5 real.** Reuse `commitOutbox.ts`, chain on `{after}`, persist the exact in-flight request, and replace "Keep my changes" with a merge-or-redo choice. Update `three-products.spec.ts:405`.
5. **Re-estimate honestly, and keep the deferrals visible.** Hold the go/no-go at H3 on three real App documents and one Agent script. Treat gate 6 parity as a signed deferral that leaves M4 incomplete.
