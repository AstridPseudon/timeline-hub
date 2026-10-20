# M2 placement CREATE / UNPLACE — Agent unit candidate

Worker: `agt-m2-placement-create-unplace-b` (continuation of the interrupted
`agt-m2-placement-create-unplace`, which left no WIP and no commits).
Branch `tl/agt-m2-placement-create-unplace-b`, base `027bd16d` (frozen027,
unchanged). Source worktree `/home/user/work/wt/agt-m2-placement-create-unplace-b`.
This is an Agent unit-qualified candidate only. It is not Runtime or App
qualification, not a merge request, and it does not change PLAN's M1 status.

## Published operations (version `"1"`)

Both ops are occurrence-owned and explicit. Their intent is exactly
`{"ownership": "occurrence"}`. Neither op accepts parent owners or `shared`.

### `placement.create`

Select `occurrence:<raw occurrence ID>`. Args (closed, `PlacementCreateArgs`):

| key | type | meaning |
|---|---|---|
| `id` | raw string, no `/` or `::` | caller-reserved child clip ID; occupied refuses |
| `on` | finite number ≥ 0 | absolute global timeline seconds; quantized once with pinned rational fps (`clip_start_frame`, same as `clip.move`) and converted to occurrence-local `at` |
| `hold` | finite number > 0 | literal occurrence-local image duration, seconds |
| `media` | `MediaSelection` (five fields) | exact Runtime-verified **image** pin; its `asset` is the reserved registry alias |

Created refs: `occurrence:<id>/asset:<alias>` (only when the registry binding
is born) and `occurrence:<id>/clip:<id>`. The clip row is
`{id, clipType:"image", asset:<alias>, track:<occurrence lane>, at, hold}`.

Export: `astrid.sdk.timeline.native_placement_commands.capture_placement_create(bundle, owner, clip_id, media, on, hold, *, ownership, verified_media)`.

### `placement.unplace`

Select `occurrence:<id>/clip:<raw child ID>`. Args `{}` (closed).
Removes the one placed expression. The registry binding survives (media bytes
are never deleted), matching the legacy `unplaceGeneration`.

Export: `capture_placement_unplace(bundle, owner, clip_id, *, ownership)`.

## Guards (what the captured command proves)

* `placement.owners` must equal `[owner]`: a shot shared by another occurrence
  refuses on every lane, at capture, replay and inverse.
* create: reuses occurrence media birth (`occurrence.add-media` internals):
  `_owner` (translation-only active occurrence, fps, no source window),
  collection membership/order, exact five-field media dependency,
  create-or-require registry binding, reserved-ID collision, active visual output
  lane, and `at ≥ 0` with `at + hold ≤ occurrence duration`.
* create: image kind only; video/audio/unknown refuse as `unsupported_media`.
* unplace: membership/order of the occurrence's clips, whole-row read of the
  target, a whole-binding read at `occurrence:<id>/source` `registry.assets[alias]`
  (ABA-protected), and the clip.delete declared-relation check across members
  (`transition`, `app.*` RELATIONS). Nested/mapped rows refuse.
* Parent clips, parent registry, other occurrences and shots are untouched.

## Commit path

`RuntimeCommitService.commit` fetches `selected_media` for `placement.create`
the same way it does for `occurrence.add-media`. Without this the provider
cannot verify the image pin.

## Refused / deliberately unsupported (no App equivalent is reproduced)

* automatic positioning (`timeline_frame` undefined → append), pooling (`null`),
  collision shifting (App `nextFreeFrame`), `keepAsPooled` on unplace,
  shared authored placement, parent-owned placement, video/audio generations.
* No registry upsert or root replace; no coordinator; relational
  `shot_generations.timeline_frame` / `metadata.end_frame` untouched.
* No same-ID recreate (decision 2026-10-20; earlier guidance withdrawn).
  Re-placing existing, unchanged media at an explicit time is `placement.move`.
  A separately chosen replacement is `placement.create` with a NEW reserved
  clip ID (optionally after `placement.unplace` of the old one). Callers pass an
  explicit occurrence owner and a verified media pin; auto, pool, null, shift,
  video and registry refresh stay on the legacy writer.

## Golden and evidence

Golden `tests/editing_conformance/fixtures/recipe_m2_placement_create_unplace.json`
(sha256 `bc92ad372b4dc7c76071e2986c81a3f9aa199739bd08d7ce0a5a2f9e57c91468`),
keys `create` and `unplace`: input document, verified media, exact command,
authoritative records and compiled output.

Schema `astrid/core/timeline/schema/edit-command.schema.json` sha256
`d3423bb9a54a0c75204444d05261e2e5bdf8019266614ff6170161b7a5463e92`.

Tests: `tests/editing_conformance/test_recipe_m2_placement_create_unplace.py`.
Case inventory:

* portable goldens (create, unplace);
* exact capture/replay/inverse/redo (create, unplace; redo uses
  `accepted_boundaries` for re-inserted rows, like the removal recipe);
* scoped birth (created = alias + clip), sibling and parent untouched, clear
  (`after == ABSENT`) on unplace with registry kept;
* provider create undo/redo and unplace undo/redo through `MediaRealm`;
* 16 create refusals and 5 unplace refusals, each preserving input;
* registry ABA: changed binding refuses replay; same-value intervening write
  rebases but blocks undo;
* disjoint rebase keeps the original capture and unrelated values;
* later consumer of the created alias blocks inverse (`surviving dependents`);
* member relation blocks unplace (`semantic dependencies`);
* capture refuses parent/shared/bad owner and identity before execution;
* `on=None`, `'auto'`, `timeline_frame`, `frame` refuse.

## Known semantics to review

* **Undo is strict ABA, not a LIFO stack.** Undoing a create after ANY
  intervening write to the created clip address (even an equal-value one, or
  unplace followed by undo-of-unplace) is refused with `intervening_write`
  (409). Only the immediate undo/redo of the latest write is exact. Tests:
  `test_undo_of_create_refuses_after_any_intervening_write_to_the_created_clip`
  and `test_create_cannot_reuse_a_removed_clip_identity_while_it_is_occupied`.
* **Image only.** App placements may carry video generations; this unit refuses
  them. Video needs a source window the App placement does not carry.
* **Hold is caller-supplied.** App uses 4 s (`DEFAULT_CLIP_HOLD`); the caller
  passes it, so the contract has no hidden default.

## Runtime / App follow-up (not done here)

* Runtime's pinned `contract/schemas/edit-command.json` is an older copy (it has
  no `occurrence.*` ops either). The same pin refresh that covers
  occurrence media must include these two ops. Runtime owns that.
* Runtime must also fetch `selected_media` for `placement.create` (Agent
  `commit.py` already does; Runtime's port must provide it).
* App: map `placeGeneration` (create) and `unplaceGeneration` (remove, no
  keepAsPooled) onto these captures with an explicit occurrence owner and a
  reserved clip ID; keep the legacy writer until accepted reload/undo and zero
  legacy traffic are proven.
