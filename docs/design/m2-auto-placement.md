# M2 completion auto-placement (step 1)

Restores the lost "anchor-after / absent-anchor fallback" completion placement for
an exact occurrence binding, image and video, from existing primitives only.
Agent unit candidate: not Runtime or App qualification. Step 2 is not done here.

## Contract

`astrid.sdk.timeline.native_auto_placement.auto_place_completion(bundle, owner,
clip_id, media, *, ownership, verified_media, anchor=None, duration=None)` is pure.
It reads the caller's original bundle and returns
`{'commands': [one ordinary EditCommand], 'capture': {...}}`.

* `owner`: `occurrence:<raw ID>` with `ownership='occurrence'`, or `parent` with
  `ownership='parent'` and `track=<parent output track>` (see Parent media birth).
  `shared`, display IDs and a shot shared by another occurrence refuse
  (`unsupported_ownership`).
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


# Shared auto-placement (step 2)

`auto_place_shared(bundle, owner, clip_id, media, *, ownership, verified_media, frame=None,
anchor=None, pooled=False)` in the same module; pure, one ordinary command plus a capture.
Owner is the canonical occurrence that exclusively owns its shot (a legacy group after
`timeline.migrate-groups`). A shot shared by two occurrences refuses `unsupported_ownership`;
non-empty `pinnedShotGroups` refuses `migration_needed`; display IDs never identify an owner.

* Hold: 4 s for image and video (completion stays 5 s). Image -> `placement.create`
  (or `occurrence.add-media` when the lane is not the occurrence lane); video ->
  `occurrence.add-media` with window `0..4`. The legacy video hold ignored media length;
  a native row authors the window, so media shorter than 4 s refuses.
* Append (`frame=None`): after the greatest end frame over ALL clips of the shot (any lane);
  empty shot -> occurrence start.
* Explicit `frame`: clamped at 0, then +1 while a clip START frame in the shot is equal
  (capture `skipped`); interval overlap is allowed.
* Lane: the anchor's lane when the anchor is in the shot, else the occurrence lane. The
  anchor never moves the start. Capture records anchor state, lane, extent / skipped frames.
* Replay/inverse are exact (literal start); a deleted shot clip refuses via the existing
  membership guard and a rebuild records `absent`.
* `unplace_shared(..., keep_as_pooled=False)` = `placement.unplace` (image only; binding kept).

Evidence: `test_recipe_m2_shared_auto_placement.py`, golden `recipe_m2_shared_auto_placement.json`.
App RED parity met Agent-side: 4 s video append (frame 120 at 30 fps), group-lane inheritance,
equal-start shift 30 -> 31 with overlap allowed. Pool membership follows (`shot.pool`).

## Shot pool (`shot.pool` v1)

Canonical home: an ordered list of registry asset aliases at `app.astrid.pool` of the shot's
internal timeline (the same `app.astrid` namespace clips use for authored intent). Members are
bound in the shot registry exactly like placed media, so the dependency manifest pins them.

* **Absent vs empty.** Absent = never authored here; `[]` = authored empty pool. `remove` of the
  last member writes `[]`, never clears the key. Inverse of the first `add` restores absence.
* **Clear policy.** Only an explicit `remove` shrinks the pool. Placing, unplacing or deleting a
  clip never touches it, except promote (below).
* **Op.** `shot.pool` v1, select `occurrence:<id>` (exclusive owner, like `placement.create`),
  args `{"action": "add"|"remove", "media": <five-field pin>}`, closed. `add` refuses a member
  (`identity_collision`) or an alias a shot clip already uses (`identity_conflict`; the clip
  `asset`/`asset_id` are read-guarded), binds the exact media (existing equal binding is fine),
  appends. `remove` refuses a non-member, guards the exact binding and keeps it. A malformed
  pool (not a list of strings) refuses `unsupported_pool`.
* **Ordered semantics.** The write replaces the whole list, so the recorded before/after make
  undo restore the exact original position and redo the exact result; ABA is the usual guard on
  the after-state (an intervening write to the pool path, even an equal one, refuses undo).
  Rebase replays the captured intent: edits disjoint from this pool (other clips, other shots'
  pools, the parent) rebase; a concurrent change to the same pool is a real conflict.
* **Builder.** `auto_place_shared(pooled=True)` = `shot.pool add` (no frame/anchor). Placing a
  media whose alias is pooled promotes it: birth command + `shot.pool remove` in one batch
  (capture `promoted: true`). `unplace_shared(keep_as_pooled=True, media=, verified_media=)` =
  `placement.unplace` + `shot.pool add`; the caller supplies the exact pin (the registry has no
  catalog digest). Video keepAsPooled stays out with `placement.unplace` (image only).
* **Legacy `poolGenerationIds`.** `timeline.migrate-groups` (on the group branches) keeps them
  only in `provenance.group_migration.legacy_group` and leaves `app.astrid.pool` absent;
  provenance is never rewritten. Adoption is an explicit recorded step: one `shot.pool add` per
  legacy generation, with the pin the caller resolved (alias `gen:<id>` in App). The duplicate
  guard makes adoption idempotent-refusing, and each add is a guarded, invertible command.
  Making the migration emit those adds itself is a follow-up on the group branch.

Evidence: `test_recipe_m2_shot_pool.py`, golden `recipe_m2_shot_pool.json`; the two former strict
xfails in `test_recipe_m2_shared_auto_placement.py` now pass. Runtime artifact regeneration for
the new args is a follow-up.

## BLOCKED (no existing writer; none invented)

1. ~~Pool membership~~ — done above.
2. **Append beyond the occurrence window.** Migration sets `duration_ms` to the member span, so
   every append refuses `occurrence_boundary`. Proposed closed op `occurrence.set-extent` v1,
   select `occurrence:<id>`, args `{"duration_ms": <positive number>}`, guarded on the old
   value; the builder would emit it with the birth command. Tests use a widened window.
3. Group migration (`timeline.migrate-groups`) lives on `tl/agt-m2-group-*` branches, not in this base.

## Parent media birth (`clip.add-media` v1)

`select: "parent"`, `intent: {}`, closed args `{id, track, at, hold, media, from?, to?, speed?, replace?}`
(`ClipAddMediaArgs`, additive to the schema). Evidence: `test_recipe_m2_parent_media.py`, golden
`recipe_m2_parent_media.json`.

* **Timing.** `at` is seconds, quantized once to a start frame at the pinned rational fps and written as
  `frame / fps` (half-open, like `placement.create`). `hold` is SOURCE seconds; a video window `[from, to)` must
  equal it and fit the verified duration; playback is `hold / speed`. An image has hold only.
* **Row.** `{id, clipType, asset: media.asset, track, at, hold[, from, to, speed]}`. `id` is reserved by the
  caller; an occupied id refuses and accepted history retires ids as for every other birth.
* **Track.** Must exist and be an active visual output track. A track that any occurrence names as its lane
  (`placement.track` / `track`) belongs to that occurrence's shot and refuses `unsupported_ownership`.
* **Registry (create-or-require).** The alias `media.asset` is created as a recorded write with the exact
  binding when absent, else must equal it exactly. The registry lives where `effective_parent_registry` reads it:
  `parent.registry` when present, else `parent.config.registry`; both present refuses. Inverse removes a created
  alias only if no clip or `asset_ref` still uses it.
* **Replace.** `replace: <clip id>` names a populated media clip on the same track. The same command removes it
  (same relation guards as `clip.delete`) and appends the new clip; the other clips keep their order. It is one
  recorded unit, so undo restores the removed clip at its original position and drops the new one.
  Slot-preserving replacement is not available: it would need a create-after proof whose anchor is then
  removed, which the inverse cannot re-select.
* **Inverse / rebase.** Exact and ABA-guarded like the occurrence births; replay keeps the recorded literal
  start. Two supporting changes: the parent asset address follows the real registry location, and
  `_ordinary_create` accepts removals beside the create so replace is invertible.
* **Completion.** `auto_place_completion(..., ownership='parent', track=...)` uses the same anchor-after rule on
  that track from frame 0 (absent anchor -> track end, empty track -> 0) and emits `clip.add-media`.
* **Runtime follow-up.** Regenerate the Runtime artifact for the added `ClipAddMediaArgs` def and the
  `clip.add-media` branch of `EditCommand`; `commit.py` already verifies its media pin.
