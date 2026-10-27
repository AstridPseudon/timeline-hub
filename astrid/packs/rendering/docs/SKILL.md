---
name: rendering
description: >
  Edit, inspect, render and open runtime-owned Astrid timelines: place media,
  text and audio, trim, split, ripple and arrange with one undoable commit,
  run the same edit across many timelines, and render Remotion output,
  worlds and effects on request.
---

# Timeline editing

How to change a timeline well. Elsewhere: [render, inspect, transfer and
worlds](references/render-inspect-transfer.md); addresses, moments and the
sheet in [the editing front door](references/editing.md); recipes in the
[video editing skill](../../video_editing/docs/SKILL.md); new media from
[creative work](../../_core/docs/creative-work/SKILL.md). The connected
runtime owns every timeline and revision; change them only through the CLI or
`tl.commit` below. Ask a verb's `--help` before a new flag.

## The model

- A **timeline** has **tracks** (`V1`, `V2`, `A1`, `titles` …) holding
  **clips**; higher video tracks draw on top.
- A clip has an **id**, a **track**, `start` and `end` in **timeline
  seconds** (half-open, `[start, end)`), and for video or audio a **source
  window**: the seconds of the file it plays.
- A narrated film also has **cuts**, **shot occurrences** (`occurrence_id`)
  and spoken **words** with times. A flat timeline has only clips.
- **One accepted commit is one undo** (one revision, one receipt), and
  **nothing moves unless you say so**: ripple is its own explicit call.

## Pick one path

| The task | Use |
|---|---|
| One move, trim or picture add you can name | Direct CLI: `timelines edit` |
| Editing cuts as rows of a table | The sheet: `show --as sheet --native`, edit, `timelines apply` |
| Anything with logic, several changes, audio, text or ripple | A Python function: `tl.commit(fn)` |
| A reviewed set of exact changes that must not be recomputed | A Python list: `tl.commit(changes)` |

If the edit needs an `if` or a `for`, write a function. Do not mix the CLI,
the sheet and Python in one task; a preview and its list are one Python path.

## Read before you write

```bash
python3 -m astrid timelines list --project <project> --json
python3 -m astrid timelines show <timeline> --project <project> --json
python3 -m astrid timelines words <timeline> --project <project>
python3 -m astrid timelines history <timeline> --project <project> --json
```

Name a timeline by the slug or id that `list` prints, never by a title you
guessed; pass `--project` whenever more than one project exists. `show` lists
clip ids, tracks, times and source windows. `history --json` lists commits
newest first in `data.revisions`: `message` is the commit's label and
`publication_id` is the same id as that commit's `receipt_id`. In Python:

```python
from astrid.sdk.timeline.api import CommitConflict, Timeline, TimelineEditError

tl = Timeline.open("<project>", "<timeline>")    # uses the configured runtime
occurrences = [p["occurrence_id"] for p in tl.bundle["placements"]]  # stored, not time, order
```

- `tl.clips()` is every clip in time order, as a list. Filters: `track`,
  `asset` (the key `show` prints), `text`, `role`, `shot`, `time`, `audio`.
- `tl.clip("intro")` is one clip. It matches an id or id prefix, an asset key,
  an element or on-screen text, and refuses, listing candidates, when several
  match; pass the exact id from `show`.
- `tl.words(between=(10, 20))`, `tl.words(text="flood")`; `tl.word("flood",
  n=2)` is its second occurrence. Words have `start`, `end`, `text`, `id`.
- `tl.duration` is where the last picture ends, on any video track; one
  track's end is `max(c.end for c in tl.clips(track="V1"))`.

## Edit with a function

A function receives a fresh copy of the timeline and changes it in ordinary
Python. Everything it does becomes **one commit**; if it raises, nothing is
committed.

```python
def tighten_intro(t):
    intro = t.clip("intro")
    intro.trim(1.0, 5.0)                       # source seconds 1–5; start stays
    t.clip("title").hold_for(2).on(intro.end + 0.25)
    for c in t.clips(track="V2"):
        if c.start < 10:
            c.remove()

r = tl.commit(tighten_intro, label="Tighten intro", idempotency_key="tighten-intro-ep01")
print(r["data"]["status"], r["receipt"]["receipt_id"])
```

Each line sees the lines before it: after a ripple, later times have moved.
It may run up to three times, so do prints, file writes and network calls
after `commit` returns.

### Helpers

| Call | Does |
|---|---|
| `t.add(path, at=, hold=, track=, id=)` | Imports a local image, video or audio file (relative to the working directory) and places it. See the note below |
| `t.add_text(text, at=, hold=, track="titles", id=)` | Places a plain text clip at `at` timeline seconds for `hold` seconds. A missing track is created as a picture track; an existing one is used where it is. No position or style arguments. Runtime behavior pending E14 |
| `t.track("titles", above="V2", kind=)` | Creates that track, or selects the existing one (never a second), and can put it above `V2`; `.rename("Opening")` labels it. Moving an existing track is not runtime-qualified (pending E14) |
| `clip.on(seconds)` | Moves the start to that timeline time; the length stays. See the note below |
| `clip.trim(in_s, out_s)` | Sets the source window in **file** seconds; the start stays, the length follows |
| `clip.hold_for(seconds)` | Sets a literal length; on video or audio the source window keeps its in-point and refuses a length the file cannot fill |
| `clip.set_track("V2")` | Moves the clip to another existing track |
| `clip.split(at, id="right-id")` | Cuts at timeline seconds and returns the left half, which keeps the original id; the right is `t.clip("right-id")`. Refuses a cut at either edge, a moving clip with no explicit source window, and a clip with a moment string, animation or transition |
| `clip.swap_asset(path_or_key)` | Plays another file (imported) or catalog key in place; the start stays. Pending E14: image and video keep their length; audio that played its whole file plays the whole new one. Swapping a music clip that has a beat grid to a file without one may refuse until a grid is attached (`clip.set_beats`) |
| `clip.remove()` | Deletes the clip and leaves its gap |
| `t.arrange(occurrence_ids, at=0, gap=0)` | Places shot occurrences in the order of your ID list (build it: stored order is not time order; the guide shows how to sort by start), from `at`, `gap` apart (timeline seconds), leaving their old slots empty; refuses to overlap a shot you did not select |
| `t.insert_time(at, seconds, music=)` | Opens time; everything later moves later |
| `t.ripple_delete(start, end, music=)` | Removes a window from every track and closes it up |
| `t.close_gap(before=word, keep=0, music=)` | Shortens the silence between the previous word and this one (a Word or its text) to `keep` seconds |

**`clip.on` with a number** is always timeline seconds. On a plain timeline it
also clears any moment string the clip had. On a narrated film it is stored
relative to the start of the clip's cut, so the clip moves with the cut if the
narration is re-flowed. To follow a word, give a moment string (below).

**`t.add`:** `at` is timeline seconds. With `hold=N` a still lasts N seconds
and video or audio plays source seconds 0–N (a draft rule E14 checks); without
`hold` they play whole. Name the `track`: a missing one is created to match
the file, a track of the wrong kind refuses. Helpers chain, `t.add("a.mp4",
at=0, track="V1", id="a").trim(0, 4)`; give new clips an explicit `id`.

### Words and beats

Use a word's time as a number, or give `clip.on` a **moment string**, which
is stored on the clip and follows the word if the narration later moves:

```python
def follow_the_words(t):
    t.clip("aerial").on(t.word("flood", n=2).start)   # the word's time now
    t.clip("badge").on('after "Astrid"')              # follows the word's end
    t.clip("hit").on('beat 2 after "Astrid"')         # second beat after it
```

`"Astrid"` alone means the word's start; `after "Astrid"` its end. A word
said more than once is refused until you say which, in the form `timelines
words <timeline> flood` prints (`'"flood" in v20a #2'`). Beats come from the
music clip's beat grid; `timelines words <timeline> Astrid --beats` prints the
beats near that word with their moment strings. The grammar is in the front door.

### Ripple is explicit

`insert_time`, `ripple_delete` and `close_gap` move everything after the
point on every track. Picture spanning the point is held longer (insert) or
shortened (delete); clips wholly inside a removed window are deleted; other
audio spanning it is split there. The **music bed** (audio on the track with id
`music`, or with a beat grid) that spans the edit is not cut at the edit point:
default `keep_end` cuts it at a nearby bar, with a crossfade, so it still ends
with the film; `plays_on` leaves it where it was and moves what follows
against its beats. Only a bed that begins at or inside the edit is pending
E14, in both modes: do not promise it stays whole; read it back and say what
changed. Put a bed on `music` with
`t.add(path, track="music")`, or `t.track("music", kind="audio")` (the default
kind is `"visual"`) and `clip.set_track("music")`; pending E14. A flat ripple
refuses to move clips with a moment string, animation or transition.

A 15-second cut, `t.ripple_delete(15, t.duration)`, removes everything after
15 s, an end card included. To keep the card, delete up to it:
`t.ripple_delete(15, t.clip("end-card").start)`; the film ends one card later.

## Preview, then apply the reviewed list

When a person should approve an edit first, preview it. A preview imports new
files but makes no commit and reserves nothing:

```python
preview = tl.commit(recut, label="Recut", dry_run=True)
print(preview["data"]["diff"])           # show this to the person
changes = preview["data"]["commands"]    # exact references and values
r = tl.commit(changes, label="Recut", idempotency_key="recut-ep01")   # after approval
```

The list applies exactly what was reviewed, on that one timeline;
`tl.commit(recut)` re-evaluates on the newest timeline and may differ. Keep
`changes` until the person answers; if it is lost, preview again. For a series,
apply the reviewed list (not a rerun) to the approved episode; run the function
for the others.

## When someone else edits

Runtime merges changes that do not touch the same things (`status` is then
`merged`). A **clash** is a commit that landed after your base and overlaps yours.

- **A function reruns** on the newer timeline, up to three evaluations in
  total. Other refusals do not rerun it.
- **A list never reruns**: a clash raises `CommitConflict` at once; so does
  a function's third clash. Do not retry on your own; tell the person which
  edit did not land, then run `timelines discard <timeline> --project
  <project>` (the refused changes stay saved) before you edit or preview again.
  Say what happened: "applied after one rerun because the timeline moved".

## Keys, retries and undo

- `idempotency_key=` names one intent on one timeline. A key that already
  landed returns that earlier receipt **without running anything, even if the
  function is different**, so put the task and the timeline in every key
  (`f"outro-{ep}"`) and use a new key for each new intent.
- After a lost reply, repeat the same call with the same key; it lands once.
  `timelines status` shows a request with an unknown outcome; `discard` keeps it.
- Undo by receipt, from your result or the `publication_id` of the `history`
  row with your label: `tl.undo(publications=[receipt_id],
  idempotency_key="undo-recut-ep01")`. Undo restores only what that commit
  changed, so a later unrelated edit survives; a later overlapping commit
  makes it refuse. Imported files stay in the catalog. A refused commit made
  no revision, so "undo my last edit" means the last receipt that landed.

## A series: one function per timeline

```python
import json

def add_outro(t):
    v1_end = max((c.end for c in t.clips(track="V1")), default=0)
    t.add("outro.mp4", at=v1_end, track="V1", id="outro")

def record(ep, **row):                                   # one line per outcome
    with open("outro-ledger.jsonl", "a") as f:           # survives a crash
        f.write(json.dumps({"timeline": ep, **row}) + "\n")

for ep in episodes:                                      # "ep-001" … "ep-100"
    try:
        tl = Timeline.open(project, ep)
        r = tl.commit(add_outro, label="Add outro", idempotency_key=f"outro-{ep}")
        record(ep, status=r["data"]["status"], receipt=r["receipt"]["receipt_id"])
    except CommitConflict as exc:                        # first: it is a TimelineEditError
        record(ep, status="conflict", detail=str(exc))   # someone is editing it
    except Exception as exc:                             # refused, or no verified reply
        record(ep, status="error", detail=str(exc))
```

Continue past a clash and report it at the end. Rerunning the loop is safe:
landed keys return their receipts (discard a clashed timeline first). To skip
a timeline, check first and record it: `if not any(c.id == "sponsor-card"
for c in tl.clips()): record(ep, status="skipped"); continue`.

**Variants** start from a copy; the source is only read. `tl.duplicate(as_="variant-a")`
returns `destination_setup` and `copy_receipt` (a repeat returns the same copy).
The copy keeps the source's clip ids, so the same names find the same clips;
shot and occurrence ids are new (runtime behavior pending E14). Open it with
`Timeline.open(project, "variant-a")`. `timelines archive variant-a --project
<project>` removes an unwanted copy; `timelines recover` brings it back.

## Direct CLI and the sheet

```bash
python3 -m astrid timelines edit <timeline> --project <project> --add-layer media \
  --layer-asset ./clip.mp4 --on 0 --for 3 --track V1 --id opening --idempotency-key add-opening-1 --json
python3 -m astrid timelines edit <timeline> --project <project> \
  --clip parent/clip:opening --on 1.5 --idempotency-key move-opening-1 --json
```

`parent/clip:` is literal; `<id>` is the clip id `show` printed. `--on` is
timeline seconds; `--trim-in`/`--trim-out` are file seconds; `timelines undo
<timeline> --commit <receipt-id> --idempotency-key undo-1` undoes by receipt.
These forms commit directly; other `edit` flags change a detached working
copy, so use Python for audio, text or anything else. For a table of cuts:
`timelines show <timeline> --as sheet --native --range c10..c12 > cut.sheet`,
edit the rows, then `timelines apply <timeline> cut.sheet --idempotency-key sheet-1`.

## Results and errors

A commit returns `r["data"]["status"]` (`accepted`; `merged` or `rebased` when
other edits landed first; `preview`) and `r["receipt"]["receipt_id"]` (`None`
for a preview). Report the label, receipt, imported files (only a preview lists
them yet) and how to undo. Catch `CommitConflict` before `TimelineEditError`
(`exc.failure` holds Runtime's details); any other means nothing landed, unless
it says no reply could be verified. Messages read *what went wrong*, *where*, *what to do*:

| Headline | Fix |
|---|---|
| A name matches several clips; candidates listed | Use one of the listed ids |
| No pending timeline edits | The function changed nothing; record it as skipped |
| No clip/word matches a name | Check `show`; in a loop, skip that timeline |
| The source file is too short for this length | Trim in, or choose a shorter hold |
| The timeline changed (a list, or a third clash) | `timelines discard`; retry only when the person asks |
| A previous request has an unknown outcome | Repeat the same call with the same key |

## Looking at the result

A commit and a read-back prove timing and structure, not appearance. Unless
the person asks for frames or a render, give them the times to check and the editor link,
`https://astrid.haus/tools/video-editor?project=<project-id>&timeline=<timeline-id>`
(`<project-id>` is the `project_id` from `projects show <project> --json`; `<timeline-id>` is
the `timeline_id` from `timelines list --project <project> --json`); say the look is unverified.

<!-- Project P's perception guidance replaces this section; frame commands are in references/render-inspect-transfer.md until then. -->

## Not possible yet

- A beat list; beats only through moment strings and `words --beats`.
- Changing existing text in place (`clip.set(text=...)`): not qualified, awaiting E14.
- Ripple on one track only: every ripple moves every track.
- Grouping existing clips into a new shot (beyond `timelines restructure`).
- A commit or undo across several timelines; loop per timeline.
- Aspect-ratio variants: a copy keeps the master's canvas.
- A portable change file for the CLI; previews and lists are Python only.
- One call that creates a timeline with content: `timelines create`, then commit.
- Finding content by what it shows: get asset keys from an understanding tool, then `t.clips(asset=...)`.

If a task needs one of these, say so and stop; do not build it from lower-level writes.
