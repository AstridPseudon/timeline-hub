# Agent source handoff — App original three drag vectors

Date: 2026-10-21 UTC

Disposition: **SOURCE ACK only; App qualification remains held.** This closes
the requested source answer for the three original `useClipDrag` expectations.
It does not freeze, generate, pin, activate, change App `it.fails`, or claim a
native/browser/Runtime acceptance result.

## Exact source boundary

The reviewed complete private Agent source is:

- commit `5672d2b7deee2bfe2ab375fd6db5fc35a192591d`;
- committed tree `6dd13b552c4f07fff5586b1fa772bdbdf64accba`;
- raw schema `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`;
- canonical formatted schema `9c05ec496e957548fe4656ca655a67a7b936ff4f220bdedae474a680e6d32eb9`;
- inventory: 62 definitions / 36 closed operation clauses.

The current assigned worktree is `a905fa29b1bb47739df438f4203ed987be588e46` on top of that source. Its only
post-5672 changes under the relevant Agent paths are rendering-adjacent
`astrid/sdk/timeline/check.py` and `reflow.py`; the 5672 timeline schema,
registry, group handlers, and existing conformance source are unchanged.
The added `tests/editing_conformance/test_recipe_m2_group_new_parent_track.py`
is the one compact generated-at-runtime proof added by this task; it writes no
large frozen JSON.

The normal Main014/Runtime95bd tuple is separate:

- Agent raw schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
  55 definitions / 29 closed operations;
- Runtime producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`;
- generated Runtime schema `7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`.

That normal schema contains `track.create` and ordinary `clip.move`, but does
not contain `timeline.migrate-groups`, `occurrence.move`, or `clip.move-set`.
Therefore none of the three original vectors is in the normal published
schema. In particular, `track.create` alone does not prove the
track-create-plus-group batch. The 62/36 private count is not a release claim.

The companion reviews used here are
`design/agent-source-unions-final-contract-review.md` (5672 source ACK),
`design/m2-group-contract.md` (existing-lane contract and projection), and
`design/agent-group-track-staged-inverse-review.md` (the corrected new-parent
grouped-inverse proof at `1ee4561a5`).

## Canonical recipe and exact exports

Option A from PLAN is used throughout: canonical shot/occurrence ownership is
the editable representation; `config.pinnedShotGroups` is migration input and
legacy display metadata only.

### 1. Canonical migration

Source: `astrid/sdk/timeline/new_group_commands.py:56,154`, registered by
`astrid/sdk/timeline/commands.py:68`.

Exact capture:

```python
groups = [{'legacy_shot_id': 'legacy', 'shot_id': 'new-shot',
           'occurrence_id': 'new-occ'}]
command = capture_migrate_groups(document, groups)
plan = execute(bundle_from_document(document, migration_command=command), [command])
```

The command is `timeline.migrate-groups@1`, `select: "parent"`, with closed
`args.groups`. It creates exactly `shot:new-shot` and
`occurrence:new-occ`; the occurrence starts at 0 on `V1` for 4000 ms, and the
child owns `c1,c2` in order. The legacy group object, snapshots, nulls, opaque
siblings, and `{legacy_clip_id, clip_id}` pairs remain under
`occurrence:new-occ` migration provenance. The parent legacy clips and
`config.pinnedShotGroups` are removed only by this command; parent/config clip
mirrors remain equal.

The real source golden is generated in
`tests/editing_conformance/test_recipe_m2_group_migration.py`:

- `test_first_group_canonical_roots_full_provenance_pins_and_portable_golden`;
- `test_compiled_reload_guarded_inverse_restores_exact_legacy_then_redo_same_ids`;
- `test_inverse_refuses_overlapping_aba_without_mutation`;
- `test_capture_guards_full_consumed_values_and_original_membership`;
- `test_destination_collisions_and_forged_capture_are_atomic`.

This 5672 source does not check in a migration JSON blob; the test constructs
`{'input', 'commands', 'records', 'output'}` at runtime. Do not invent a
second fixture export or claim a missing file is a generated artifact.

### 2. Existing-lane group temporal/retrack

Source: `astrid/sdk/timeline/occurrence_commands.py:37,186`, registered by
`commands.py:69`; read projection: `astrid/sdk/timeline/group_view.py:13`.

Exact capture on the migrated canonical bundle:

```python
command = capture_occurrence_move(
    bundle, 'occurrence:new-occ', 1,
    track='parent/track:V2',
    child_track='occurrence:new-occ/track:V2',
)[0]
```

The emitted command is `occurrence.move@1` with fixed intent
`{ripple:none, anchor:fixed, position:absolute, ownership:occurrence}` and
closed args `{on: 1, track: parent/track:V2,
child_track: occurrence:new-occ/track:V2}`. It records
`move.owner`, `move.track`, `move.child-track`, one `move.member:i` and one
`move.raw-track:i` for each child, the exact source/dependency pin
`move.images`, destination `lane.members`, source/child lane identity, and
the complete member/order/timing reads. Writes are the occurrence placement
start/lane and each canonical child clip's raw track; no parent group array is
written.

The exact visible/raw output is `c1` on `V2` at `[1,3)`, `c2` on `V2` at
`[3,5)`, both hold 2; `V1` is empty. `project_group_view` returns the legacy
display group with `shotId: legacy`, `trackId: V2`, ordered `clipIds: [c1,c2]`,
`mode: images`, and bindings:

```json
[
  {"occurrence":"occurrence:new-occ","clip":"occurrence:new-occ/clip:c1",
   "raw_child_track":"occurrence:new-occ/track:V2","parent_track":"parent/track:V2"},
  {"occurrence":"occurrence:new-occ","clip":"occurrence:new-occ/clip:c2",
   "raw_child_track":"occurrence:new-occ/track:V2","parent_track":"parent/track:V2"}
]
```

The real tests are:

- `test_recipe_m2_group_move.py::test_existing_lane_exact_app_view_capture_and_portable_golden`;
- `test_recipe_m2_group_move.py::test_original_app_pinned_fixture_exact_existing_lane_visible_values`;
- `test_recipe_m2_group_move.py::test_rational_fps_quantization_and_half_open_adjacent_boundary`;
- `test_recipe_m2_group_move.py::test_independent_groups_rebase_and_undo_preserve_other_group_and_opaque_state`;
- `test_recipe_m2_group_move.py::test_equal_value_intervening_writes_are_guarded`;
- `test_recipe_m2_group_move.py::test_membership_aba_and_destination_lane_aba_replay_by_final_state`.

As with migration, the existing-lane test constructs its golden at runtime;
there is no checked-in `recipe_m2_group_move.json` in the 5672 source.

### 3. `track.create` plus group batch onto a new parent track

This is the vector behind App line 1230. It is not a child-track birth and not
physical materialization. The exact private source proof is now
`tests/editing_conformance/test_recipe_m2_group_new_parent_track.py`.

The compact capture recipe is deliberately explicit and uses existing
operations only:

```python
create = capture_track_create(bundle, 'parent', {
    'id': 'V3', 'kind': 'visual', 'role': 'output',
    'active': True, 'opaque': [None],
})
staged = execute(bundle, [create])
move = capture_occurrence_move(
    staged.bundle, 'occurrence:new-occ', 1,
    track='parent/track:V3',
    child_track='occurrence:new-occ/track:V2',
)[0]
commands = [create, move]
plan = execute(bundle, commands)
```

The exact batch is `[track.create(parent/track:V3), occurrence.move]`.
`track.create` records `created: [{ref: parent/track:V3, kind: track,
owner: parent}]`; the move binds the new parent track and the existing raw
child track. Output is `c1` on V3 at `[1,3)`, `c2` on V3 at `[3,5)`, with the
derived group retaining ordered legacy metadata and bindings whose
`raw_child_track` remains `occurrence:new-occ/track:V2` while
`parent_track` is `parent/track:V3`. The parent canonical config has no
`pinnedShotGroups` after migration.

The proof IDs are:

- `test_new_parent_track_batch_has_one_capture_golden_and_exact_group_view`;
- `test_new_parent_track_batch_reload_inverse_redo_and_retry_are_exact`;
- `test_new_parent_track_refuses_later_dependent_clip_before_removing_track`.

There is no frozen large JSON export for this vector by design. The three
tests generate the fixture from the existing migration helper and assert the
raw commands, created IDs, bindings, output spans, retry identity, exact
reload, inverse/redo, and later-dependent refusal.

## Direct mapping from the three original App vectors

| App source vector | Real Agent proof | Raw expected output |
| --- | --- | --- |
| `useClipDrag.test.tsx:774` free multi to new bottom track | `test_recipe_free_move_set.py::test_exact_app_drag_golden_selection_order_and_created_track_are_one_unit` | One batch `[track.create(parent/track:V3), clip.move-set]`; V1/V2/V3; `clip-1@V2,[1,3)`, `clip-2@V3,[3,5)`, no `pinnedShotGroups`, resolved selection `[clip-2,clip-1]`. |
| `useClipDrag.test.tsx:1120` pinned group across existing lanes | `test_recipe_m2_group_move.py::test_original_app_pinned_fixture_exact_existing_lane_visible_values` plus `test_existing_lane_exact_app_view_capture_and_portable_golden` | `V1=[]`; `c1@V2,[1,3)`, `c2@V2,[3,5)`, hold 2; derived group `shot-1`, V2, `[clip-1,clip-2]`, `images`; explicit occurrence/raw/parent bindings. |
| `useClipDrag.test.tsx:1230` pinned group onto new V3 | `test_recipe_m2_group_new_parent_track.py::test_new_parent_track_batch_has_one_capture_golden_and_exact_group_view` plus its reload/inverse/dependent tests | One batch `[track.create(parent/track:V3), occurrence.move]`; `c1@V3,[1,3)`, `c2@V3,[3,5)`; raw child remains occurrence V2; derived group track V3 with ordered legacy metadata. |

The App assertions additionally mention effect IDs, selection calls, secondary
ghosts, and transaction identity. Those are App presentation/gesture outputs;
the Agent raw proofs above cover authored rows, ownership, timing, membership,
and grouped command records. No UI display ID is used as a raw owner.

### 4. Free-parent multi movement onto a new bottom track

Source: `astrid/sdk/timeline/_move_set.py:38,98`, registered by
`commands.py:77`, with ordinary `capture_track_create`.

The exact batch is the existing `staged_drag()` recipe in
`tests/editing_conformance/test_recipe_free_move_set.py`:

```python
create = capture_track_create(original, 'parent', {'id': 'V3', 'kind': 'visual'})
staged = execute(original, [create]).bundle
move = capture_move_set(
    staged,
    [{'clip': 'parent/clip:clip-2', 'track': 'parent/track:V3'},
     {'clip': 'parent/clip:clip-1', 'track': 'parent/track:V2'}],
    'parent/clip:clip-2', 3,
)
create['group_id'] = move['group_id'] = 'free-drag-1'
plan = execute(original, [create, move])
```

The checked-in golden is
`tests/editing_conformance/fixtures/recipe_m2_free_move_set.json`, SHA-256
`ae0f95433287c98072ac4508942b31dc9a1a3e4e9b7b6595f4ebc8bc1235199a`.
`clip.move-set@1` preserves authored member argument order separately from UI
selection order. Raw output is tracks `V1,V2,V3`; `clip-1` is on V2 at 1 with
hold 2 and `clip-2` is on V3 at 3 with hold 2; `pinnedShotGroups` is absent;
the command's resolved selection is
`[parent/clip:clip-2, parent/clip:clip-1]`. The golden also proves reload,
inverse/redo, exact retry, source/track/rate reads, and created-track guards.

The real App-vector test is
`test_recipe_free_move_set.py::test_exact_app_drag_golden_selection_order_and_created_track_are_one_unit`.
Relevant guard tests are `test_forward_equal_value_aba_accepts_original_guards`,
`test_forward_source_and_identity_aba_remain_guarded`,
`test_forward_changed_membership_refuses_atomically`, and
`test_created_track_surviving_dependent_refuses_after_own_moves_are_reversed`.

## Projection and identity rules

`project_group_view` is read-side only. It derives current membership/order and
source geometry from canonical occurrence children, maps raw child tracks to
parent lanes, and carries legacy `shotId`, mode, snapshots, nulls, and opaque
metadata only for display/history. It does not make `pinnedShotGroups` an
editable authority. App adapters must retain explicit `occurrence`, raw clip,
raw child track, and parent track refs. A `(shotId, trackId)` display pair,
display clip ID, media alias, or UI row index never identifies an owner.

## Guard/inverse/rebase floor

The original safety behavior remains in the real tests, not in the App display
assertions:

- migration: exact consumed legacy values/membership, destination collisions,
  forged capture rejection, exact reload/inverse/redo, and overlapping ABA
  refusal;
- existing-lane: original values are captured before preview; lane membership,
  source/dependency, owner, timing, order, and raw-child bindings are guarded;
  equal-value intervening writes refuse inverse, while independent groups
  rebase and preserve each other; destination membership ABA is checked by the
  existing final-state policy;
- new-parent batch: the created parent track is typed and reserved once,
  inverse/redo/retry reuse the exact records, and a later dependent clip keeps
  the track from being removed;
- free multi: member/order/lane/source/rate identities are captured; forward
  equal-state ABA is accepted when intent still holds, but source/identity or
  membership changes refuse; inverse still refuses intervening publication
  writes and surviving dependents.

No guard is refreshed from the UI projection or current head after capture.

## Evidence run for this handoff

Focused command, with shared Runtime read-only on `PYTHONPATH`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/editing_conformance/test_recipe_m2_group_migration.py \
  tests/editing_conformance/test_recipe_m2_group_move.py \
  tests/editing_conformance/test_recipe_m2_group_new_parent_track.py \
  tests/editing_conformance/test_group_read_view.py \
  tests/editing_conformance/test_current_group_slice.py \
  tests/editing_conformance/test_recipe_free_move_set.py
```

Result: **167 passed in 22.25s**. The new-parent-only run was **3 passed in
1.37s**. The first new-parent collection attempt without Runtime on
`PYTHONPATH` failed at import with `ModuleNotFoundError: runtime_protocol`; it
was an environment setup miss and was not counted as product evidence.

No full/full-*, native, browser, render, localhost, Runtime live acceptance,
schema generation, freeze, pin, activation, or App assertion conversion was
run or inferred. `useClipDrag.test.tsx:774,1120,1230` remain exact `it.fails`.

## Exact source gaps / next owners

1. Normal generation still lacks the three group operations and must compose
   the exact reviewed source before App can consume a generated capture/client.
2. Current 5672 source has runtime-generated migration/existing-lane goldens,
   not checked-in JSON exports; this is a packaging/export gap, not a missing
   recipe or a reason to add an alias. The free-multi JSON golden is present.
3. App still needs a row-local read-side projection adapter and a producer
   adapter that consumes these exact capture ports. It must preserve the three
   original visible outputs and accepted readback, then separately qualify
   outbox/retry/undo. No whole-parent writer or `pinnedShotGroupsOverride`
   authority is implied.
4. Runtime's existing generic carrier has a bounded source ACK for the 5672
   shape, but no generated/native group qualification follows from it. The
   accepted migration bootstrap/retry/restart pair is still a separate gate.

The missing normal artifact, App adapter, and Runtime native acceptance are
exact source/qualification gaps; no new alias, caller API, DTO, or projection
authority is proposed here.
