# M2 completion auto-placement (step 1)

Restores the lost "anchor-after / absent-anchor fallback" completion placement for
an exact occurrence binding, image and video, from existing primitives only.
Agent unit candidate: not Runtime or App qualification. Step 2 is not done here.

## Contract

`astrid.sdk.timeline.native_auto_placement.auto_place_completion(bundle, owner,
clip_id, media, *, ownership, verified_media, anchor=None, duration=None)` is pure.
It reads the caller's original bundle and returns
`{'commands': [one ordinary EditCommand], 'capture': {...}}`.

* `owner`: `occurrence:<raw ID>` with `ownership='occurrence'`. Parent ownership,
  `shared`, display IDs and a shot shared by another occurrence refuse
  (`unsupported_ownership`). Parent-owned completion needs parent-media birth
  (`clip.add-media`), which this stack does not have.
* `clip_id`: caller-reserved raw child ID (a replacement needs a new one).
* `media`: the exact five-field pin of the **completed variant**, with its
  Runtime-verified entry in `verified_media`. The gallery primary and the latest
  variant are never consulted. Kind comes from the verified `media_type`.
* `anchor`: raw clip ID in the same occurrence, or `None`.

Emitted command: image -> `placement.create` (`hold` 5); video ->
`occurrence.add-media` with `{from: 0, to: d, hold: d, speed: 1}` where `d` is
`duration` (the completed asset's verified length) or 5 when none is supplied.
`d` may not exceed the verified duration. The image hold ignores `duration`.
These are the completion defaults, kept distinct from the shared 4 s hold (step 2).

## Start rule

Frames at the pinned rational fps, intervals half-open, using the same
`clip_end_frame` as the compositor (`start + max(1, round(duration * fps))`).

* Anchor present: start = anchor end frame.
* Anchor absent (no id, or no such clip in the occurrence): start = lane end, the
  greatest end frame of the occurrence's own clips on the occurrence lane; an
  empty lane starts at the occurrence start.
* A present anchor with unusable timing refuses. It never falls back.

The start is quantized once, exactly as `placement.create` does, and written as a
literal. New clip goes on the occurrence lane. Result must fit the occurrence
(`at + hold <= duration`) or the existing `occurrence_boundary` refusal applies.

## Capture contract and replay

`capture` = owner, clip, kind, media pin, `anchor {id, state: present|absent}`,
`resolution` (`anchor-after|lane-end`), fps, `start_frame`, `on`, `seconds`.
It explains the choice for the App's persisted continuation. The command's literal
start is the authority, so:

* replay and inverse are exact (no resolution is re-run);
* if the anchor merely *moved* afterwards, replay keeps the recorded start;
* if the anchor was *deleted* (membership changed), replay refuses via the
  existing collection-membership guard; the caller rebuilds, which now falls
  back to lane end and records `absent`;
* undo is the existing strict ABA of create/add-media (any intervening write to the
  created clip refuses), redo follows the removal recipe.

## Evidence

`tests/editing_conformance/test_recipe_m2_auto_placement.py`, golden
`fixtures/recipe_m2_auto_placement.json` (keys `image-anchor`, `image-absent`,
`video-anchor`, `video-absent`: commands, capture, created child row). Covers
anchor present/absent, empty lane, defaults and supplied/over-long video duration,
exact variant binding, shared/parent/unbound refusal, unverified/audio media,
unusable anchor timing, anchor moved/deleted replay, guarded undo/redo and the
provider undo/redo through `MediaRealm`.

## Known gaps

* The video path (`occurrence.add-media`) has no exclusive-owner check at replay;
  isolation is enforced at capture only. A one-line `_exclusive` in `add_media`
  would close it but changes that op's existing goldens, so it is left for the
  owner. (`placement.create` already re-checks at replay.)
* Anchor *movement* is not a conflict: there is no read-only guard op, and a no-op
  `placement.move` would write `fixed_start` intents. Guarding it needs a read of
  the anchor inside the command, i.e. a schema change.

## Step 2 needs (out of scope)

Shared 4 s image/video hold; shared append (after the group's greatest extent,
numeric fps default 30, empty group at 0); lane inheritance (shot-group lane, else
first group's lane, else first track, else `V1`); start-frame-only collision shift;
canonical pool membership with promote / unplace-to-pool (`keepAsPooled`);
legacy pinned-group migration; parent-owned completion (`clip.add-media`); Runtime
schema/provider pair for `placement.create` and the video row; App durable
continuation (task/attempt guards from Agent/Runtime, reserved IDs, verified pin).
