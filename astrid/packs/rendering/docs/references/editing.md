# Edit a timeline: the front door

A narrated film runs on its words. You edit a **working copy** (a draft of the published timeline),
look at it, then publish it. Times are timeline seconds; **positions are canvas px** for every element.
*When* things happen is written as **moments** (`on "viral"`), so a new take moves everything with its words.

Every `timelines` below is short for **`python -m astrid timelines`** (venv active, from the `Astrid` install dir,
`ASTRID_RUNTIME_DATA_ROOT` set as your install says). A bare `timelines` is not on PATH.

## The loop
```bash
timelines show TL c41.mink --project P                 # ONE thing's whole record: every param (typed, canvas px,
                                                       #   formula, default, allowed keys), its moments in seconds
timelines show TL --project P --as sheet --range c30..c31 > cut.sheet   # several cuts as an editable sheet
timelines edit move TL --project P --clip parent/clip:ID --on 33.9       # native guarded command
timelines edit TL --project P --clip c30.cover --until Astrid --verify    # legacy detached draft edit
timelines check TL --project P --at '"Astrid" in n21'                      # look at any moment (fast; no queue)
timelines check TL --project P --at 33.9 --zoom c08.loras   # + both sides cropped around a layer, full resolution
timelines status TL --project P   ·   timelines undo TL --project P
```
`show`, `lint`, `diff`, `find` and `words` read the working copy; `--published` reads the live one.
`timelines find TL "the conclusion"` (also `--text "Astrid."`, `--asset ROCKET`, `--line w23c`, `--cut c30`) → addresses and times.
`timelines lines TL` (`--line w23c`: one in full) · `timelines words TL Astrid --beats` · `show --as sheet --detail`
prints long values (`inset=`, `lines=`) as editable JSON instead of `…`. The sheet's element column drops `am-`
(`footage` = `am-footage`; both are accepted).
**Make one timeline equal another** (a finished duplicate → the film) remains a
legacy detached-draft capability. `timelines checkout FILM --project P --from
round2[@rev]` creates that draft, but its broad publish is held; do not use it
as the native command path.

## Addresses (the same everywhere: show, edit --clip, check --at, Python)
`c41.mink` (cut.layer; a layer carried into a later cut also answers to it: c30.cover = c29.cover) ·
`c41.mink.x` (one param) · `c30` (a cut; `c30..c31` inclusive) · `"Building" in v27 #2` (a spoken word) ·
`93.5` · an asset key · a layer name. Ambiguous names list their choices; outputs print the canonical address.
`c1` and `c01` are the same cut; `c10..c41` runs by time (c10's start to c41's end); with `--as sheet`,
`--range c10,c29,c33a` (or repeated `--range`) is exactly those cuts. `·` in outputs only separates fields.
In Python, `tl.time(X)` gives the seconds of any of these, or of a moment.
A cut's picture is `--cut 42` (`timelines edit TL --cut 42 --until c43`). Its layers print with their names in
`show TL c42` (the picture sits on the `plate` track, so `--clip c42.plate` matches no layer name).

## Moments
`"viral"` · `after "Astrid"` (word end) · `"tool" in v20a #2` · `beat 2 after "Astrid"` · `c22` · `end of c30` (=`c30.end`) ·
`end` (the clip's cut; with no clip, the film) · `+0.8s` (after the clip's cut starts) · any of these `+2f`.
A clip has `on`, and `until` or `for 1.9s`. A param takes a moment too: `--set 'states[3].at="adapt" in w05c'`.
Offsets: `"Astrid" +3f` = 3 frames after the word starts (30 fps); `"Astrid" +0.3s` = 0.3 s after it. Cuts too:
`until c17` = cut 17's START (the shot change); `until end of c17` = its end. Every moment, word or cut, is
re-resolved on each re-flow, so a clip on one moves with its words.
Length (`for`): CLI `edit --for 1.2` (bare seconds only; `--for 1.2s` is a usage error) · sheet `for 1.2s` or
`for 36f` · Python `clip.for_("1.2s")`, `clip.hold_for(1.2)`, or `"36f"`.
Beats come from the music clip's grid: `--swap-asset run:<id>/music` brings the run's beats; `--beats FILE|HANDLE`.

## The sheet
```
 91.50 ┃ c30   on "And" in n21                                    · 2.50 s     ← cut id and its moment
         sprite  cover   sprite  MYSTERY  until "Astrid"  enter=stamp x=1356 y=198
         sprite  tool    sprite  TOOL-16  on "Building"   x=ƒ(B2-HAND -42) y=ƒ(B2-HAND -384)
```
A layer line: `track name element [ASSET] ["text"] [on …] [until …|for …] [k=v …]`. A partial sheet is safe:
apply changes ONLY the cuts in the file; a layer line deleted from one of those cuts removes that layer.
A brand-new layer is a new name: `sprite  paw  sprite  PAW  on "Building" in v27  x=ƒ(B2-HAND -177.5) y=600`
(element: sprite, type, pixel-shape, footage, …; fractional ƒ offsets are fine). Stacking is by TRACK, not line
order: chrome > type > fx > sprite > plate; to put a layer behind another, give it a lower track (to be sure,
not the same one). A sprite's `scale` is canvas px per art px (default 6); a pixel-shape's `px_scale` is the same
for its cells. The film line ends `· v 1a2b…`: the version you exported. If the working copy was edited since,
apply merges: lines you did not change keep the newer value; a line changed both places refuses (re-export).
A NEW cut: a header `┃ c05b on "word"` with a `plate` line (its picture) and any layers; the cut before ends there.
Or `timelines edit TL --project P --split c33 --on MOMENT` (or `--add-cut --on M [--after c33]`; Python
`tl.cut("c33").split(on=…)`, `tl.add_cut(…)`): later layers move with it, spanning ones carry over it.
`…` values in a sheet are kept as they are.
`tl.add("am-type", at='"Building" in v27', layer="title", hold=1.2)` joins the cut on screen as `cNN.title`.
`x=ƒ(MARK ±px)` follows a slot's mark: a plain number replaces it (and says so). `k=…` is unchanged, `~k` is info.
The `sound` section lists the music bed and other audio in no cut: edit its asset, `for`, `volume=` there.
A cut's notes: `why: …` and `hold: deliberate` (lint's HOLD/STILL leave it; `hold: off` clears), or
`timelines edit TL --project P --cut c33 --why "…" --hold deliberate`. JSON params go in one token:
`inset={"x":12,"y":40}`; a nested one: `--set lines[0].at=…`.
Units are the element's own declaration (element.yaml `metadata.units`): positions canvas px, `…at` params clip frames.
`am-callout`: `x`,`y` are the card's TOP-LEFT (not its centre) and `width` its width, all canvas px; `anchor` (x,y) is
where the connector ends. The connector leaves the card's left or right edge, whichever faces the anchor.

The native command is the supported write path for covered operations. The
cut-sheet and broad Checkout edit surface below are retained for legacy drafts
only; their three-way merge and whole-candidate publication are held.

## The same edit as a legacy verb or in Python
```bash
timelines edit TL --project P --clip c30.cover --until Astrid   # --on, --for, --set k=v, --swap-asset, --clear-asset, --remove
```
```python
from astrid.sdk.timeline.sync import TimelineSession
session = TimelineSession.open("P", "TL", client=client)
result = session.move("parent/clip:c30-cover", 33.9, idempotency_key="move-42")
```

The detached `Checkout` surface below is held for capabilities that have not
migrated. It is not a general writer:

```python
from astrid.sdk.timeline_checkout import Checkout
tl = Checkout.draft("P", "TL")                 # held legacy working copy
tl.clip("c30.cover").until("Astrid"); tl.clip("c41.tool-16").set(x=1200)   # canvas px
print("\n".join(tl.changes() + tl.check().brief())); tl.save()
```

## Python: the method table
```
session = TimelineSession.open(P, TL, client=client)
session.move("parent/clip:c30-cover", 33.9, idempotency_key="move-42")
session.trim("parent/clip:c30-cover", out_s=3.0, idempotency_key="trim-42")
session.commit(command, idempotency_key="command-42")
session.commit_many(commands, idempotency_key="batch-42")
session.undo([publication_id], idempotency_key="undo-42")

# Read/check methods remain projection operations:
tl = Checkout.draft(P, TL)   tl.find("the conclusion")  tl.time('end of c30')  tl.words()
tl.check().brief()  tl.changes()
```
`on`/`until` a word mean its START (`after "word"` = its end); `until c30b` = when c30b STARTS; `until end of c30`
ends with that cut. Clip methods return the clip, so they chain: `tl.clip("c30.cover").on('"x"').hold_for(1.2)`.
`Checkout.draft(P, TL)` opens the held detached working copy if one exists;
its mutation/save methods are not the native write path. `--verify`/`check --at`
write only their page and frames, in the fast lane's cache in the temp dir. In check,
"intent" (was "app") is a clip's moments, cut and words; "shot" is the film's one authoring shot; a layer that
carries over later cuts counts as a change in each of them. A moment
lands on the frame it falls in (148.13 s → frame 4443 = 148.10 s at 30 fps), so a clip on it starts there.

A time-lapse (a stepped sequence) moves and stretches as ONE unit and fills its cut (or `until` its first step's
moment): `timelines edit TL --project P --clip c17.rt-01 --fit-sequence --on 'after "So" in w17' --until c19 [--shape-from round0]`,
in Python `tl.sequence("c17.rt-01").fit(on=…, until=…, shape_from=…)`. check blocks a PICTURE GAP (a span nothing covers).
A line break in text is JSON: `--set 'text="One\nTwo"'`; look at several moments: `check TL --at A --at B`.
`lint --only SAFE,FACE` narrows lint; with a working copy it also counts what was resolved since checkout.
`show TL c18.churn` counts long lists (`highlights: 41 items`); `--full` or `--keys highlights,totals` prints them.
A cut's `why`/`hold` belong to the cut (they stay when its picture changes). `diff --all` prints every change.

## The narration (re-flow)
`timelines edit TL --project P --from-script vo.json --takes DIR` (DIR has `<id>.wav` + `<id>.words.json`;
`--script-gaps` uses the script's gaps) · `--line ID --take … --words …` · `--insert-line` · `--remove-line`.
Everything after a change moves; clips on words follow them; the music bed stays whole. A removed line's
clips are kept as **orphans** (status, sheet and check list them; publish waits): `--cut c07 --on '"word" in w05'`
moves an orphaned cut's picture to a new moment, `--clip X --on …` one layer, `--keep` accepts it in place,
`--remove` drops it.

**What sets the film's length:** the end of its last cut (`Checkout.duration` is the latest cut end). The music bed
is one clip and does NOT follow a ripple: after a removal it can end before the film (the re-flow report then says
`music: the bed ends at …`). Fix it with `for` in the `sound` section (a known gap, below).

The native session never overwrites a change published after its original
capture: Runtime rebases disjoint commands and refuses real clashes. Its outbox
keeps the original request and identity across retries. The legacy draft
publisher's merge/force behavior is held; do not use two writers on one draft
as a substitute for native commands.
`edit`/`apply` exit 0 once saved; what still blocks publishing is check's (printed) state: `timelines check TL`
shows only lint that is new since checkout (`--all` for everything).

> **Known gaps (as of this writing; check before relying on them)**
> - `--set volume=` on audio is stored but does not change the render yet (use the clip-level field when it lands).
> - No fade-in or entrance on our elements yet. The cookbook's `effects.fade_in` applies only to legacy `local` elements.
> - Extending the film's content does not extend its rendered length yet, and `check` still says VALID. Look at the
>   new end with `check TL --at <end>`: "out of range" means it does not render.
> - The music bed does not follow a ripple (see above).
> - `check --at` and `--verify` can be slow or fail ("frame owner closed"). Retry once; if it fails again, say so
>   and do not publish a change you have not seen.
