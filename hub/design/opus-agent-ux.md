# The agent's editing experience under document-first (Opus, 22 Oct)

## Verdict
Document-first suits an AI agent well. Agents are best at "read a structure, change it, save it", and that is the whole protocol here. It also restores the loop upstream main teaches (checkout, edit, publish), whose rich surface (addresses, moments, sheet, re-flow) the integration branch parked as "legacy"; that surface becomes the helper library, with one way to save. Three things decide whether it is elegant or merely loose:
- **The SDK commits a function, not a document.** Then a conflict means "run it again on the new head", with no replay machinery.
- **Each step carries its own patch,** so partial undo always works.
- **Anchors are core timing fields resolved by one compiler, and marker sets are pinned by version.** "Clips follow the beats" then stays reproducible.

Without these, bulk agent edits will conflict often or drift silently.

## Today, verified (agent repo)
On the integration branch (`hub/timeline/agent/tl/integration`):
- **Two write paths sit behind one verb.** `edit move | track-label | commands-file` are native (`cli_native.py:330-339`). Plain `edit --trim-in/--on` is routed to native by a heuristic and otherwise falls back to the detached draft (`cli_native.py:23-70`). Everything else (`--split`, `--swap-asset`, `--set`, `--retime`…, `cli.py:3691+`) edits a draft.
- **The docs call the broad surface held:** Checkout "is not a general writer" (`rendering/docs/references/editing.md:80-99`).
- **There are two Python writers:**
  - `TimelineSession` has `commit`, `commit_many`, `move`, `trim`, `undo(publications)`, `restore`, `queue_proposal` and `flush` (`sdk/timeline/sync.py:137-420`).
  - `Checkout` has `edit(label)` as a transaction with `dry_run` and a `Plan` (calls, changes, diff, lint_delta, blocking) (`checkout.py:255`, `transaction.py:18`), plus `step()` (`checkout.py:377`) and `publish()` (`publish.py:30`).
- **Two undo meanings share one verb:** draft steps and publications (`checkout.py:263-290`).
- **The document bridge refuses the edits agents want most.** `document_diff_to_commands` turns a JSON document back into commands and refuses clip membership and order, track order, placements, shot create and delete, and registry edits as "held" (`document_diff.py:128-379`). `timeline_document.py:238-294` uses it.
- **The client-side merge is three-way and unit by unit** (`store.py:217`). `publish_bundle` reads the head, merges and publishes (`store.py:305`).
- **Moments live in clip `app.astrid` metadata** (`sdk/timeline_intent.py`) and are resolved by Python re-flow (`reflow.py:149,349`).
- **The query language exists:** `parse_selector` and `Selection.where` (`selection.py:40,94`), with errors that list the choices (`selection.py:120`). `CheckReport.brief()` reports blocking problems and new lint (`check.py:679-693`).
- **A proposal is a guarded command batch** (`producer.py:47`).

On `origin/main`, `checkout/edit/apply/undo/redo/publish` all act on one working copy (`packs/timeline/cli.py:3851-3860`). The editing guide's loop is checkout → edit or apply sheet → publish.

Everything below is a **proposal**.

## The golden path
**CLI: eleven verbs.**

| Read | Write | Watch |
|---|---|---|
| `show` (text, `--as sheet`, `--as json`) | `edit <helper> …` | `watch` |
| `find --where` | `apply FILE` (`.sheet`, `.json` document, patch, or `.py` transform) | |
| `diff` | `undo [COMMIT[/STEP]]` | |
| `history` | `redo` | |
| `visualize` (and `check --at`) | `commit DRAFT` | |

Every write takes `--dry-run`, `--propose`, `--draft NAME`, `-m LABEL`. `edit` subcommands (move, trim, split, delete, swap, rename, set, add, transition…) come from the helper registry.

**Python: one object, one write call.**
```python
tl = timeline.open("P", "TL")              # document at head + its base; read model + helpers
tl.clips().where("track=plate cut=c06..c09")
tl.clip("c30.cover").move(on='after "Astrid"')   # helpers edit locally and record a step
r = tl.commit("Cover after Astrid")         # or tl.commit(fn, label=…) for transforms
tl.undo(r.commit) ; tl.undo(r.step("snap")) ; tl.watch(since=r.revision)
```

**One result shape for every write** (undo and proposals too): `status` (accepted, merged, conflict, invalid, preview), `revision`, `summary` (lines by address), `steps`, `merged_from`, `conflicts`, `problems`, `lint_new`, `look` (moments to check).

## 1. Simple edits
```
$ timelines edit move TL --clip c30.cover --on 'after "Astrid"'
accepted r419 · moved c30.cover 91.50→92.34 (on: after "Astrid")
look: timelines check TL --at 92.34
$ timelines edit trim TL --clip c41.mink --out 3.0
$ timelines edit split TL --cut c33 --on '"tool" in v20a'
$ timelines edit transition TL --cut c18 --kind crossfade --for 12f
$ timelines edit swap TL --clip c22.plate --asset ROCKET-B
```
- Each is one commit with one `kind: command` step (`replay` = the helper call).
- **Verify** with `diff TL r418..r419`, `show TL c30.cover`, or `check --at` / `visualize`. `--dry-run` previews; `undo` reverses, guarded.

## 2. Complex edits
**Producers run first,** because they are slow and write artifacts, not the timeline:
```
$ astrid run audio.activity --media vo-main      → signal  activity:vo-main@v1
$ astrid run beats.detect   --media music-01     → markers beats:music-01@v1
$ astrid run scene.cuts     --media broll-3      → markers cuts:broll-3@v1
```
**The transform is a pure function of the document.**
```python
def align(doc):
    beats = doc.markers("beats:music-01@v1")
    with doc.step("snap", intent="cuts start on the nearest downbeat", tags=["beats"]):
        for cut in doc.cuts():
            cut.anchor(beats.nearest(cut.start, kind="downbeat"))
    with doc.step("beat-meta", intent="record beat index"):
        for c in doc.clips().where("track=plate"):
            c.meta["beats"] = {"index": beats.index_at(c.start)}
    with doc.step("match-cuts", intent="b-roll cuts land on image cuts"):
        ...

r = tl.commit(align, label="Align to audio, beats and image cuts", dry_run=True)
print("\n".join(r.summary)); r.look()      # Runtime dry run: exact merge + validation
r = tl.commit(align, label="Align to audio, beats and image cuts")
tl.undo(r.step("beat-meta"))                # part
tl.undo(r.commit)                           # all
```
- **Steps and patches:** the SDK snapshots the document at each step boundary, so every step is sent with its own patch, and undoing part of a commit is a guarded inverse of that one patch.
- **Re-cutting to a script** is one helper inside a transform: `doc.apply_script(spec, takes=DIR)` (today `reflow.py:284`).
- **Retiming a range:** `doc.retime("c10..c20", speed=1.1)` does a bulk retime.
- **B-roll:** generate first (producer media), then place each clip `on '"rocket" in n21'` so it survives re-takes; propose if creative.
- **CLI equivalent:** `timelines apply TL align.py -m "…"`. A `.py` file defines `transform(doc)`.

## 3. Concurrency
**An automatic merge** (the human dragged c07 meanwhile):
```
merged r421 onto r420 (Hannah · app · "nudge c07"): kept their 1 change
```
`r.merged_from` lists the other commits by actor, label and summary.

**A conflict on a single helper edit:**
```
conflict: Hannah (app) set c30.cover.start 91.50→92.00 in r420 after your base r418; you set 93.00
next: rerun on r420, or --theirs / --ours c30.cover.start
```
- **Transforms rerun.** Function-form commits default to `merge="atomic"`. If anything they touched changed, the SDK reruns `fn` on the new head, with up to three attempts and a fresh idempotency key each time (hash of base, change and label).
- **Learning what changed:** `timelines watch TL --since r418` streams commits as JSON lines; `tl.changes_since(rev)` in Python.

## 4. Analysis-driven edits
- **Anchors:** `clip.start = {anchor: "beats:music-01@v1#b17", offset: "+2f"}` is a core timing field, resolved by one compiler everywhere. Helpers write anchors, never resolved seconds.
- **Re-detection:**
  1. The producer publishes `@v2` with id continuity, mapping each old beat to its nearest new one.
  2. Following it is a one-field commit, `markers.bump beats:music-01 v1→v2`, which can be proposed and undone.
  3. Every anchored clip moves because the compile changes.
- **Why pinned:** "latest" would change what a past revision renders, with no commit.

## 5. Reviewable proposals
- **Making one:** `tl.commit(fn, label=…, propose=True)` (or `--propose`) stores base, patch, steps and rationale without moving the head.
- **Review in the App:** the App shows it as an overlay diff, grouped by step. The human accepts all, accepts some steps (each has its own patch), or rejects.
- **Acceptance** is an ordinary three-way commit on the current head. A clash comes back as a conflict on the proposal, and the agent reruns.
- **The agent follows** through `watch`. Project policy may auto-approve (e.g. a beats bump when the off-beat check passes).

## 6. Reading and orientation
- **As text:** `show TL` gives the human text, `show TL c41.mink` one full record, `show --as sheet --range c30..c31` an editable view, and `--as json` the raw document.
- **Finding things:** `find TL --where 'track=sprite text="Astrid"'` uses the same selector language as `.where()` and as `edit --where` for bulk helper edits.
- **History and sight:** `history` lists commits with actors, steps and intents; `diff --commit C/STEP`; `visualize`/`check --at` accept a revision, draft or proposal.
- **Editable views become trivial:** parse the sheet into a document and commit it. No translation into commands is needed, so every "held" refusal in `document_diff.py` disappears.

## 7. Errors
Every problem carries a `code`, a document path, an address, a message, the bad value, a hint and a command to try. Nothing is committed when any problem is present.
```
invalid (nothing committed): 2 problems
  E_OVERLAP   c30.cover overlaps c30.tool on track sprite 91.50–92.10
              fix: timelines edit move TL --clip c30.tool --on 92.10, or use another track
  E_MEDIA_REF parent/clip:b7 asset "ROCKET2" is not registered; known: ROCKET, ROCKET-B
```
Anchor errors name the nearest valid ids; `meta` gets warnings from optional namespace schemas; `--json` returns the same fields.

## Gaps

| Gap | What closes it |
|---|---|
| Undoing part of a commit needs `replay` | The SDK sends a patch per step automatically |
| A stale read: the agent aligned to audio the human then moved, and the merge was clean | Anchor to it, or declare `depends: [ids]`; also atomic merge |
| Unpinned marker re-publication changes past revisions | Pin sets by version; following is a bump commit; producers keep ids continuous |
| Anchor resolution is client-side Python today (`reflow.py`) | Anchors become core fields, compiled once (Runtime and evaluator) |
| "N items" bulk threshold is arbitrary | Explicit `merge: fields \| atomic`, with a default per form |
| A local dry run differs from the real merge | `/commit` with `dry_run` returns the exact merged result |
| Separate writers (`replace-parent-media`, `update-element`, `restructure`, narration's second revision `publish.py:54-58`), "make one timeline equal another" | Helpers through one commit; `apply --from TL@rev` |
| Order merges in id-keyed lists (tracks, clips, placements) | Define move semantics in the merge; test with App documents at H4 |
| Proposals and `watch` are outside the 12-hour scope | Ship their storage and push first; App UI after |
| `meta` is never validated | Optional per-namespace schemas, as warnings (the "checks" type) |

## Recommended design changes
1. **SDK:** `commit(fn | label)`. Reruns are the client's strategy for clashes, which drops the reliance on `replay: command`.
2. **Per-step patches** come from step boundaries and are recorded by Runtime. Partial undo and partial approval then work everywhere.
3. **Replace the N threshold** with `merge: fields | atomic`. The default is atomic for transforms and fields for helper edits.
4. **Anchors are core timing fields** and marker sets are pinned; following is a commit. Promote today's `app.astrid` moments into this field.
5. **Server dry run** and one result shape for every write.
6. **An error contract:** code, path, address, hint, command.
7. **`watch`, `changes_since` and `propose`** are in the first ship; they are small.
8. **Idempotency keys are derived by the SDK.** Hide the `--idempotency-key` flags.
9. **Delete:**
   - the native subparsers and routing heuristics (`cli_native.py`), `commands-file`, `apply --native`, `undo --publication`;
   - `TimelineSession`'s command outbox protocol (keep a retry queue of commits);
   - `document_diff.py`, `store.three_way`, `publish_bundle`, the `timeline_document.py` bridge;
   - `checkout`/`publish` as concepts (a draft is a file plus `commit DRAFT`) and draft-step undo.

   **Keep:** addresses, moments, the selector, the Checkout read model and edit methods (as helpers), re-flow, the sheet, `CheckReport.brief`, `Plan`, `visualize`.
