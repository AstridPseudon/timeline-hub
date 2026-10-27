---
name: rendering
description: >
  Edit, inspect, render and open runtime-owned Astrid timelines: place media,
  text and audio, trim, split, ripple and arrange with one undoable commit,
  run the same edit across many timelines, and render Remotion output,
  worlds and effects on request.
---

# Timeline editing

This skill teaches how to change a timeline well. Rendering, frames, timeline
transfer and Three.js worlds are in
[render, inspect, transfer and worlds](references/render-inspect-transfer.md);
addresses, moments and the sheet format are in
[the editing front door](references/editing.md). Production recipes belong to
the [video editing skill](../../video_editing/docs/SKILL.md); new generated
media comes from [creative work](../../_core/docs/creative-work/SKILL.md).

The connected workspace runtime owns every timeline and revision; change them
only through the CLI or SDK below. Ask a verb's `--help` before a new flag.

## The model

- A **timeline** has **tracks** (`V1`, `V2`, `A1`, `titles` …); higher video
  tracks draw on top. Tracks hold **clips**.
- A clip has an **id**, a **track**, `start` and `end` in **timeline
  seconds**, and for video or audio a **source window**: the seconds of the
  file it plays. Intervals are half-open: `[start, end)`.
- A narrated film may also have **shot occurrences** (`occurrence_id`) and
  spoken **words** with times. A flat timeline has only clips.
- **One accepted commit is one undo**: one revision, one receipt, however
  many changes it makes.
- **Nothing moves unless you say so**: ripple is its own explicit call.

## Pick one path

| The task | Use |
|---|---|
| One move, trim or picture add you can name | Direct CLI: `timelines edit` |
| Editing cuts as rows of a table | The sheet: `show --as sheet --native`, edit, `timelines apply` |
| Anything with logic, several changes, audio, text or ripple | A Python function: `tl.commit(fn)` |
| A reviewed set of exact changes that must not be recomputed | A Python list: `tl.commit(changes)` |

If the edit needs an `if` or a `for`, write a function. Do not mix paths in
one task.

## Read before you write

```bash
python3 -m astrid timelines list --project <project> --json
python3 -m astrid timelines show <timeline> --project <project> --json
python3 -m astrid timelines words <timeline> --project <project>
python3 -m astrid timelines history <timeline> --project <project> --json
```

`show` lists clip ids, tracks, times and source windows; `history` lists past
commits with their receipt ids. Pass `--project` whenever more than one
project exists; never guess a timeline from its name. In Python:

```python
from astrid.sdk.timeline.api import CommitConflict, Timeline, TimelineEditError

tl = Timeline.open("<project>", "<timeline>")    # uses the configured runtime
for c in tl.clips(track="V1"):
    print(c.id, c.track, c.start, c.end)
occurrences = [p["occurrence_id"] for p in tl.bundle["placements"]]
```

- `tl.clips()` is every clip in time order, as a list. Filters: `track`,
  `asset`, `text`, `role`, `shot`, `time`, `audio`.
- `tl.clip("intro")` is one clip; it refuses, listing candidates, otherwise.
- `tl.words(between=(10, 20))`, `tl.words(text="flood")`; `tl.word("flood",
  n=2)` is its second occurrence. Words have `start`, `end`, `text`, `id`.
- `tl.duration` is the end of the last picture.

## Edit with a function

A function receives a fresh copy of the timeline and changes it in ordinary
Python. Everything it does becomes **one commit**. If it raises, nothing is
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
The function may run up to three times, so keep prints, file writes and
network calls out of it; do those after `commit` returns.

### Helpers

| Call | Does |
|---|---|
| `t.add(path, at=, hold=, track=, id=)` | Imports a local image, video or audio file and places it; no `hold` plays the whole file. Creates a missing track |
| `t.add_text(text, at=, hold=, track="titles", id=)` | Places a plain text clip |
| `t.track("titles", above="V2")` | Creates (or selects) a track and orders it; `.rename("Opening")` labels it |
| `clip.on(seconds)` | Moves the start to that timeline time; the length stays |
| `clip.trim(in_s, out_s)` | Sets the source window in **file** seconds; the start stays, the length follows |
| `clip.hold_for(seconds)` | Sets a literal length (stills, text) |
| `clip.set_track("V2")` | Moves the clip to another existing track |
| `clip.split(at, id="right-id")` | Cuts at timeline seconds; the original id keeps the left half |
| `clip.swap_asset(path_or_key)` | Plays another file (imported) or catalog key in place; timing stays |
| `clip.remove()` | Deletes the clip and leaves its gap |
| `t.arrange(occurrence_ids, at=0, gap=0)` | Places shot occurrences in that order |
| `t.insert_time(at, seconds)` | Opens time; everything later moves later |
| `t.ripple_delete(start, end)` | Removes a window from every track and closes it up |
| `t.close_gap(before=word, keep=0)` | Shortens the silence before a word (a Word or its text) to `keep` seconds |

Helpers chain: `t.add("a.mp4", at=0, track="V1", id="a").trim(0, 4)`. Give
new clips an explicit `id` so later steps and reports can name them.

### Selection and timing are plain Python

There is no query language beyond those filters. Compute with ordinary code:

```python
def place_in_order(t):            # items: [(path, at, hold), ...]
    for n, (path, at, hold) in enumerate(sorted(items, key=lambda x: x[1]), 1):
        t.add(path, at=at, hold=hold, track="V1", id=f"shot-{n:02d}")

def shift_late_titles(t):
    for c in t.clips(track="titles"):
        if c.start > 5:
            c.on(c.start + 0.5)
```

### Words and beats

Use a word's time as a number, or give `clip.on` a **moment string**, which
is stored on the clip and follows the word if the narration later moves:

```python
def follow_the_words(t):
    t.clip("aerial").on(t.word("flood", n=2).start)   # fixed time
    t.clip("badge").on('after "Astrid"')              # follows the word's end
    t.clip("hit").on('beat 2 after "Astrid"')         # second beat after it
```

`"Astrid"` alone means the word's start; `after "Astrid"` its end. Beats come
from the music clip's beat grid and are reachable only through moment strings;
there is no beat list yet. The full moment grammar is in the front door.

### Ripple is explicit

`insert_time`, `ripple_delete` and `close_gap` move everything after the
point on every track, picture, audio and text. A clip spanning the point is
held longer (insert) or shortened (delete); audio spanning a removed window is
split so later sound stays in sync. The music bed is cut at a bar with a
crossfade so it still ends with the film; pass `music="plays_on"` to leave it
whole instead. To cut a film to 15 seconds: `t.ripple_delete(15, t.duration)`.
`arrange` refuses to overlap a shot you did not select instead of pushing it.

## Preview, then apply the reviewed list

When a person should approve an edit first, preview it. A preview imports any
new files but makes no commit and reserves nothing:

```python
preview = tl.commit(recut, label="Recut", dry_run=True)
print(preview["data"]["diff"])           # show this to the person
changes = preview["data"]["commands"]    # exact references and values
r = tl.commit(changes, label="Recut", idempotency_key="recut-ep01")   # after approval
```

The list applies exactly what was reviewed, on that one timeline, and is never
recomputed: on a clash it is refused and you preview again.
`tl.commit(recut)` instead re-evaluates the intent on the newest timeline.

## When someone else edits

A person may be editing in the editor while you work. Runtime merges changes
that do not touch the same things (`status` is then `merged`). A **clash** is
a conflict refusal: another commit landed after your base and overlaps yours.

- **A function reruns** on the newer timeline, up to three evaluations in
  total. Other refusals do not rerun it.
- **A list never reruns.** Preview again and ask.
- **After the third clash**, `commit` raises `CommitConflict`. Do not retry on
  your own. Tell the person which edit did not land and that the timeline is
  changing.

Say what happened: "applied after one rerun because the timeline moved".

## Keys, retries and undo

- `idempotency_key=` names one intent on one timeline. A key that already
  landed returns that earlier receipt **without running anything, even if the
  function is different**. So put the task and the timeline in every key
  (`f"outro-{ep}"`) and use a new key for each new intent.
- After a lost reply, repeat the same call with the same key. It lands once.
  `timelines status` shows a request still waiting on an unknown outcome;
  `timelines discard` drops unsent work but keeps a request that may have
  landed.
- Undo by receipt (from your result or `timelines history`):

```python
tl.undo(publications=[r["receipt"]["receipt_id"]], idempotency_key="undo-recut-ep01")
```

  Undo is a new commit. It restores only what that commit changed, so a later
  unrelated edit survives; if a later commit changed the same things, undo
  refuses rather than overwrite it.
- Imported files stay in the project catalog after undo; only placements go.

## A series: one function per timeline

```python
import json

def add_outro(t):
    t.add("outro.mp4", at=t.duration, track="V1", id="outro")

for ep in episodes:                                   # "ep-001" … "ep-100"
    try:
        r = Timeline.open(project, ep).commit(
            add_outro, label="Add outro", idempotency_key=f"outro-{ep}")
        row = {"status": r["data"]["status"], "receipt": r["receipt"]["receipt_id"]}
    except CommitConflict as exc:
        row = {"status": "conflict", "detail": str(exc)}   # someone is editing it
    except Exception as exc:
        row = {"status": "refused", "detail": str(exc)}
    with open("outro-ledger.jsonl", "a") as f:             # survives a crash
        f.write(json.dumps({"timeline": ep, **row}) + "\n")
```

Record every outcome as it happens and continue past a clash; report clashed
timelines at the end instead of retrying them. Rerunning the loop is safe:
landed keys return their original receipts. When a timeline may not need the
edit (no `sponsor-card` clip), check before committing and record it as
skipped: `if not any(c.id == "sponsor-card" for c in tl.clips()): continue`.
A function that changes nothing is refused with "no pending timeline edits".

**Variants** start from a copy; the source is only read:
`copy = tl.duplicate(as_="variant-a")` returns `copy["destination_setup"]`
and `copy["copy_receipt"]`; then `Timeline.open(project, "variant-a")`.
Repeating it with the same name returns the same copy, never a second one;
`timelines archive` removes an unwanted copy.

## Direct CLI and the sheet

```bash
python3 -m astrid timelines edit <timeline> --project <project> \
  --add-layer media --layer-asset ./clip.mp4 --on 0 --for 3 --track V1 \
  --id opening --idempotency-key add-opening-1 --json
python3 -m astrid timelines edit <timeline> --project <project> \
  --clip parent/clip:opening --on 1.5 --idempotency-key move-opening-1 --json
python3 -m astrid timelines edit <timeline> --project <project> \
  --clip parent/clip:opening --trim-in 0.5 --trim-out 3.0 \
  --idempotency-key trim-opening-1 --json
python3 -m astrid timelines undo <timeline> --project <project> \
  --commit <receipt-id> --idempotency-key undo-1 --json
```

`parent/clip:<id>` addresses a clip by the id `show` printed. `--on` is
timeline seconds; `--trim-in`/`--trim-out` are file seconds. These forms commit
directly; other `edit` flags change a detached working copy, so use a Python
function for audio, text or anything else. For a table of cuts:

```bash
python3 -m astrid timelines show <timeline> --project <project> \
  --as sheet --native --range c10..c12 > cut.sheet
python3 -m astrid timelines apply <timeline> cut.sheet --project <project> \
  --idempotency-key sheet-1 --json
```

## Results and errors

A commit returns `r["data"]["status"]` (`accepted`; `merged` or `rebased` when
other edits landed first; `preview`) and
`r["receipt"]["receipt_id"]` (`None` for a preview). Report the label, receipt,
the files you imported (a commit result does not list them yet; a preview
does) and how to undo. `TimelineEditError` is a local refusal; nothing
was sent. `CommitConflict` is Runtime's; `exc.failure` holds the details. Read
each message as *what went wrong*, *where*, *what to do*:

| Headline | Fix |
|---|---|
| A name matches several clips; candidates listed | Use one of the listed ids |
| No pending timeline edits | The function changed nothing; record it as skipped |
| No clip/word matches a name | Check `show`; in a loop, skip that timeline |
| The source file is too short for this length | Trim in, or choose a shorter hold |
| The timeline changed and clashes (third time) | Stop; retry only when the person says so |
| A previous request has an unknown outcome | Repeat the same call with the same key |
| Undo overlaps a later commit | Undo that later commit first, or leave it |

## Looking at the result

A commit and a read-back prove timing and structure, not appearance. Unless
the person asks for frames or a render, give them the editor link and the
times to check, and say the look is unverified:

```text
https://astrid.haus/tools/video-editor?project=<project-id>&timeline=<timeline-id>
```

<!-- Waiting for project P: its perception guidance replaces this section
(when to look, the ways of looking, full-size frames for text). Frame commands
are in references/render-inspect-transfer.md until then. -->

## Not possible yet

- A beat list in Python; beats only through moment strings.
- Grouping existing clips into a new shot (beyond `timelines restructure`).
- A commit or undo across several timelines; loop per timeline.
- Aspect-ratio variants: a copy keeps the master's canvas.
- Split on anything but plain parent media with an interior cut and no
  animation, moment anchors or transitions.
- A portable change file for the CLI; previews and lists are Python only.
- Creating a timeline and its content in one call: `timelines create` first,
  then add the content in one commit.
- Finding content by what it shows: get asset ids from an understanding tool,
  then select with `t.clips(asset=...)`.

If a task needs one of these, say so plainly and stop; do not build it from
lower-level writes.
