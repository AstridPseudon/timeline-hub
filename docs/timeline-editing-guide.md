# Timeline editing guide

For cross-product ownership and the canonical path, see [Timeline architecture](architecture/timeline.md).
The agent-facing summary is the [timeline editing skill](../astrid/packs/rendering/docs/SKILL.md);
this guide is the longer version with worked examples. The two must agree.

## The model in one paragraph

A timeline is tracks of clips placed in seconds. The connected Runtime keeps
every revision. An edit is submitted as one commit; Runtime accepts or
refuses it as a whole; an accepted commit gets one receipt and one undo.
Nothing ripples unless you call a ripple helper. Media files are imported
into the project catalog by content and stay there after undo.

## One path per task

| Task | Path |
|---|---|
| One small, named change | `timelines edit` (media add, literal move, source trim) |
| Rows of a table | `timelines show --as sheet --native`, edit, `timelines apply` |
| Logic, loops, ripple, mixed changes | `tl.commit(fn)` |
| Reviewed exact changes | `tl.commit(list)` from a preview |

A function is intent: on a clash it is evaluated again on the newer
timeline. A list is a decision: it is applied exactly or refused.

## Opening and reading

```python
from astrid.sdk.timeline.api import CommitConflict, Timeline, TimelineEditError

tl = Timeline.open(project, timeline)          # configured runtime connection
tl.clips(track="V1")                           # a filterable list
tl.clip("intro")                               # one clip, or a refusal listing candidates
tl.words(between=(10, 20))                     # spoken words with times
tl.word("Meanwhile", n=1)
tl.duration
```

Pass a `client=` to `Timeline.open` only when you already hold an
authenticated SDK client; never recover credentials from Runtime storage.
Shot occurrence ids for `arrange` are
`[p["occurrence_id"] for p in tl.bundle["placements"]]`, in their current
order. `timelines history <timeline> --json` lists past commits and their
receipt ids.

## The four owner cases

These are the acceptance cases for this editing surface. Each makes one
authored commit, and one undo restores the prior content and order.

```python
# 1. Twenty media items in time order.
def place_twenty(t):
    assert len(items) == 20
    for n, (path, at, hold) in enumerate(sorted(items, key=lambda x: x[1]), 1):
        t.add(path, at=at, hold=hold, track="V1", id=f"shot-{n:02d}")
r = tl.commit(place_twenty, label="Place twenty files", idempotency_key="place-20")
tl.undo(publications=[r["receipt"]["receipt_id"]])

# 2. Arrange twenty real shot occurrences, back to back.
assert len(order) == len(set(order)) == 20
r = tl.commit(lambda t: t.arrange(order, at=0, gap=0), label="Arrange shots")

# 3. New picture and audio tracks with content.
def picture_and_voice(t):
    t.track("V2", above="V1")
    t.add("picture.mp4", at=0, track="V2", id="pic").trim(0, 4)
    t.add("voice.wav", at=0, track="A2", id="vo")
r = tl.commit(picture_and_voice, label="Picture and voice")

# 4. Several kinds of change together, previewed first.
def recut(t):
    f = t.clip("footage").trim(1, 5).on(2)
    t.clip("cutaway").split(8, id="cutaway-right")
    t.clip("title").hold_for(2).on(f.end + 0.25)
    t.track("titles").rename("Opening")
    t.arrange(order, at=12, gap=0.5)
    t.clip("old-intro").remove()
    t.add_text("Chapter one", at=12, hold=3, track="titles", id="ch1")
preview = tl.commit(recut, label="Recut", dry_run=True)
r = tl.commit(preview["data"]["commands"], label="Recut")
```

Case 1 imports up to twenty files and case 3 imports two; the imports are
listed in the result and survive undo. `t.add` creates a missing track once,
deriving its kind from the verified file; an existing track of the wrong
kind refuses.

## Helpers

- **`t.add(path, at=, hold=, track=, id=)`**: image, video or audio. A video
  without `hold` uses its verified duration; `.trim(in, out)` then sets the
  source window.
- **`t.add_text(text, at=, hold=, track="titles", id=)`**: plain text.
- **`t.track(id, above=)`**, **`.rename(label)`**: create, order and label
  tracks.
- **`clip.on(t)`, `clip.trim(in, out)`, `clip.hold_for(s)`, `clip.end`**:
  timing. `trim` is in source seconds and keeps the start. On a narrated film
  whose clips belong to cuts, a plain number given to `on` is an offset from
  the clip's cut; use a word or a moment string there.
- **`clip.split(at, id=)`**: native split at timeline seconds; the right half
  gets `id`. Requires registry-backed parent media, an interior cut, an
  explicit source window for moving media, and no timing anchors,
  animation or parent transitions.
- **`clip.swap_asset(path_or_key)`**: plays another file (imported) or
  catalog key in place; timing stays.
- **`clip.set_track`, `clip.set_look`, `clip.remove`** (`remove` leaves a gap).
- **`t.arrange(ids, at=, gap=)`**: shot occurrences in caller order. It keeps
  their ids, lengths and source windows, refuses unknown lengths and
  collisions with occurrences you did not select, and never ripples.

## Words, beats and ripple

Words are numbers you can compute with (`w.start`, `w.end`). A moment string
(`'after "Astrid"'`, `'beat 2 after "Astrid"'`, `'"tool" in v20a #2'`) is
stored on the clip and re-resolved when the narration moves; the grammar is
in [the editing front door](../astrid/packs/rendering/docs/references/editing.md#moments).
Beats are only reachable through moment strings today.

Ripple helpers work on flat picture and audio tracks inside a function, one
commit and one undo each:

```python
tl.commit(lambda t: t.insert_time(4, 2), label="Open 2 s at 4 s")
tl.commit(lambda t: t.ripple_delete(4, 6), label="Remove 4–6 s")
tl.commit(lambda t: t.close_gap(before=t.word("Meanwhile"), keep=0),
          label="Close gap before Meanwhile")
```

Clips after the point move on every track; picture spanning it is held longer
or shortened; audio spanning a removed window is split so later sound stays in
sync; clips wholly inside a removed window are deleted. The music bed follows
the `music=` policy: `"keep_end"` (default) cuts it at a bar with a crossfade
so it still ends with the film; `"plays_on"` leaves it whole. Within one
function each call sees the previous one, so times after a ripple have
already moved.

## Preview and apply

`tl.commit(fn, dry_run=True)` returns Runtime's commands
(`["data"]["commands"]`) and a readable diff (`["data"]["diff"]`), with
`receipt` `None`. It may import media and lists those imports. It takes no
key and leaves nothing waiting to be sent. Applying the returned list keeps
its exact references, media identities and the expectations it captured; it
never selects again. Calling the function again re-evaluates it.

## Conflicts with a person

Runtime merges disjoint changes from different authors. When a change
clashes:

1. a function is evaluated again on the new head, at most three evaluations
   in total;
2. a list is refused at once;
3. after that, `CommitConflict` is raised. Stop, report which edit did not
   land, and leave the decision to the person.

Function commits are guarded broadly: any concurrent commit can count as a
clash. Precise read tracking is a planned follow-on, so expect reruns while
someone is actively editing.

## Keys, retries, status and undo

`idempotency_key=` is optional and explicit; nothing derives one for you. A
keyed function call whose key already landed returns the original receipt
without evaluating the function or importing anything, even if the function
is different, so name the task and timeline in every key. After a lost reply,
call again with the same key, or simply call again in the same session: the
saved request is replayed byte for byte. A final refusal releases the
saved request and any queued edits, so the next edit is not blocked.

`timelines status` shows the head and any request with an unknown outcome;
`timelines discard` drops unsent work but keeps a request that may have
landed (it cannot undo one whose reply was lost).

```python
tl.undo(publications=[receipt_id], idempotency_key="undo-42")
tl.redo(publications=[undo_receipt_id], idempotency_key="redo-42")
```

```sh
astrid timelines undo TL --project PROJECT --commit RECEIPT_ID --idempotency-key undo-42
astrid timelines redo TL --project PROJECT --commit UNDO_RECEIPT_ID --idempotency-key redo-42
```

Undo restores the fields and order the commit changed, so unrelated later
edits survive. It refuses when a later commit overlaps; undo that one first.
Repeating an undo without its key can be refused by the same guard. Whole
revision restore is a deliberate rollback, not undo.

## Series and variants

Run one function per timeline, with one key and one receipt each:

```python
for ep in episodes:
    try:
        r = Timeline.open(project, ep).commit(add_outro, label="Add outro",
                                              idempotency_key=f"outro-{ep}")
        row = {"status": r["data"]["status"], "receipt": r["receipt"]["receipt_id"]}
    except CommitConflict as exc:
        row = {"status": "conflict", "detail": str(exc)}
    except Exception as exc:
        row = {"status": "refused", "detail": str(exc)}
    ledger.append({"timeline": ep, **row})   # write it to a file as you go
```

Record progress per episode as it happens, continue past a clash, and report
failures individually. Rerunning the loop is safe: landed keys return their
receipts. There is no transaction across timelines. A preview list belongs
to one timeline; preview a series with the function on one episode, then run
the function per episode.

`tl.duplicate(as_="variant-01")` creates the destination timeline, then
copies the head into it with fresh shot and occurrence ids, returning
`destination_setup` and `copy_receipt` separately. The source is only read.
Its operation key comes from the project, source and name, so a retry never
creates a second destination. `timelines archive` removes an unwanted copy.
The CLI form is `timelines duplicate <timeline> --project <project> --slug variant-01`.

## Direct CLI and the sheet

```bash
python3 -m astrid timelines edit <timeline> --project <project> \
  --add-layer media --layer-asset /path/to/video.mp4 --on 0 --for 3 --track V1 --id opening \
  --idempotency-key first-video-42 --json
python3 -m astrid timelines edit <timeline> --project <project> \
  --clip parent/clip:opening --on 1.5 --idempotency-key move-42 --json
python3 -m astrid timelines edit <timeline> --project <project> \
  --clip parent/clip:opening --trim-in 0.5 --trim-out 2.5 \
  --idempotency-key trim-42 --json
```

These three forms commit directly; each is one commit and one undo.
`parent/clip:<id>` addresses a clip by its `show` id; `--on` is timeline
seconds and `--trim-in`/`--trim-out` are file seconds. A still image has no
source window; change its length with `--for`. Add audio and text with a
Python function (`--add-media` is the legacy draft verb). Symbolic moments
and the other `edit` flags still edit a detached working copy; prefer a
Python function for those changes.

For a table of cuts, `timelines show <timeline> --as sheet --native --range
c10..c12 > cut.sheet`, edit the rows, then `timelines apply <timeline>
cut.sheet --idempotency-key sheet-42`. Supported clip and track rows commit
natively; anything else is refused rather than half applied.

## Results and errors

A commit result has `data.status` (`accepted`, `merged`, `rebased`, `preview`) and
`receipt.receipt_id`. CLI `--json` wraps the same data in
`ok`/`data`/`error`/`receipt`/`idempotency_key`. Report the label, receipt,
imports and how to undo.

Every refusal should read as a headline (what went wrong), a detail (where:
the clip, time or receipt) and a fix (what to do next). Ambiguous names list
their candidates. `TimelineEditError` is local and nothing was sent;
`CommitConflict.failure` carries Runtime's `message` and `details` (including
`status` and the `current` head on a clash). Never describe an unknown outcome
as a failure, a retry as a redo, or a preview as reserved.

## Looking at the result

Structure and timing can be read back; appearance cannot. Unless the person
asks for frames or a render, give them the editor link and the times to check,
and say the look is unverified. When they ask, the frame commands are in
[render, inspect, transfer and worlds](../astrid/packs/rendering/docs/references/render-inspect-transfer.md).
The final perception guidance (project P) will replace this section.

## Not possible yet

- Public beat list; a CLI word-anchor adapter.
- Grouping existing clips into a shot; regrouping beyond `timelines restructure`.
- Cross-timeline transactions and group undo.
- Aspect-ratio variants.
- A portable `--changes` file for the CLI.
- Creating a timeline and its content in one public call: create with
  `timelines create`, then add the content in one commit.

## Checks and the journal

```bash
python3 -m astrid timelines check <timeline> --project <project> --sweep
python3 -m astrid timelines log <timeline> --project <project> --verify --json
```

`check --sweep` validates a saved working copy and compares bounded samples across every cut. Sweep status is 0 for expected results, 1 for unexpected picture changes, and 2 when capture was not made; a validation failure returns 1. Without a saved working copy, `check` prints a checkout hint and does not sweep. `--no-sweep` suppresses it. These bounded samples do not prove every-frame or audio identity.

`log --verify` checks the journal hash chain. A broken chain returns 1; JSON reports `error.code: validation_error`. A missing journal is reported as “no journal yet” and returns 0. Journal queries accept `--since`, `--actor`, `--op`, `--cut`, `--clip`, and `--outcome`; a query validation error is printed to stderr and returns 2.

## Shared timeline and shot contracts

`@banodoco/timeline-schema` owns `TimelineConfig` and timeline clip semantics.
Workspace Runtime's `contract/schemas/shot-composition.json` owns the outer
shot publication envelope (revision identity, head/CAS, dependencies, and
occurrences) and references the generated canonical config schema for nested
timelines. Consumers project these contracts into their local views; they do
not define a competing `TimelineConfig`.

Visible clip duration is the selected source duration divided once by positive
`speed`: `hold`, transport `duration_ms`, or source trim `to - from` supplies
the source duration. Parent occurrence `duration_ms` caps the resulting visible
interval. Source trims remain in source units, and the renderer owns final frame
rounding against the shared conformance vectors.

## Opening sources and returned artifacts

Keep these identities distinct: a clip's `asset`/`asset_id` is a timeline-local
registry alias; a managed media ID identifies a project media record; a
`source_object_id` identifies managed bytes; an artifact handle identifies a
returned view or run output. Never pass a display alias to an API that asks
for a managed ID, or construct an artifact URL from an alias/digest.
For a returned, non-null source object, `client.media.read_bytes(source_object_id)`
retrieves its bytes; media metadata alone does not prove that they were viewed.
