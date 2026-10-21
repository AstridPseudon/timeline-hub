# Current Agent group contract handoff to App

Status: **source evidence only; integration remains held** (2026-10-21).

This answers App's 2026-10-20 23:54 request. The settled PLAN choice is Option
A: canonical shot/occurrence ownership is the editable representation;
`config.pinnedShotGroups` is migration input, and App receives only a derived
legacy-shaped read view. The three original App success expectations remain
exact `it.fails` tests.

## The release answer

No normal release currently includes the group or free-multi operations.

The normal Main014/Runtime95bd staging tuple is the ordinary Agent source:
ordinary raw schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
(55 definitions / 29 operations), with the generated Main014 schema recorded
as `7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`.
That source is not a group release. The 55/29 floor is specifically a
reconstruction check; it is not evidence that groups are present. The staged
normal Agent pin is `e35ad5e72ed9acc61d659a6b4b9c32d69208ab8d` (tree
`a2454c2cb472fa5404289c9f48bb7779d330879e`), paired to Runtime producer
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` (tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`). This is staging evidence, not
App activation or group qualification.

The current private Agent group source is c064:

- commit `c0644cf1a7b63c9bcff7f70502b953a07879c9f3`;
- tree `0699f877a4c809005536a80f5956b8051a814ef7`;
- schema SHA-256 `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`;
- 58 definitions / 32 operation clauses;
- added operations only: `timeline.migrate-groups` and `occurrence.move`.

The c064 source is private and was source-reviewed by Runtime. Runtime's
bounded ACK says the existing generic carrier is sufficient and requires no
group-specific DTO, endpoint, materialization API, or Runtime source change.
That ACK does not authorize generation, pinning, adoption, or native release.

The separate private free-multi source candidate defines `clip.move-set`; it is
not part of c064 and is not part of normal95bd/ordinary6ba. Its source contract
is recorded in `design/m2-free-move-contract.md` and must be composed and
normally generated with the group source before App can consume it.

The App writer census keeps the whole-parent snapshot, shot graph, duplicate /
group, placement, and ordinary-batch writer rows open. A retired route or a
Runtime `410` is not zero-traffic evidence, and this handoff does not authorize
writer deletion or fallback restoration.

## Existing canonical source, captures, and goldens

The reviewed c064 source has these exact pieces:

| Purpose | Existing source | Existing pure tests |
| --- | --- | --- |
| Legacy admission/migration | `astrid/sdk/timeline/new_group_commands.py`: `capture_migrate_groups`, `migrate_groups`; closed `timeline.migrate-groups` v1 | `tests/editing_conformance/test_recipe_m2_group_migration.py` |
| Canonical temporal move and child retrack | `astrid/sdk/timeline/occurrence_commands.py`: `capture_occurrence_move`, `occurrence_move`; closed `occurrence.move` v1 | `tests/editing_conformance/test_recipe_m2_group_move.py` |
| Derived App-compatible view | `astrid/sdk/timeline/group_view.py`: `project_group_view` | `tests/editing_conformance/test_group_read_view.py` |
| Current membership/inverse guards | c064 changes in `_collections.py`, `_recording.py`, `commands.py`, `commit.py`, and `inverse.py` | `tests/editing_conformance/test_current_group_slice.py` |

The group capture records explicit parent/raw-child ownership, membership and
order, lane occupancy, source/dependency inputs, timing, and inverse facts.
`occurrence.move` is fixed, translation-only, single-output-lane movement.
An optional new child lane is an ordinary typed `track.create` before
`occurrence.move` in the same batch; it is not physical materialization. The
view derives current canonical children and order, maps raw child tracks to
parent tracks, and copies legacy group metadata only for display/history.
Display `(shotId, trackId)` values are not edit selectors.

The portable private existing-lane golden is:

```text
/home/user/work/wt/agt-m2-group-existing-lane-view/tests/editing_conformance/fixtures/recipe_m2_group_move.json
sha256 488b7f475d0a760a7ba0e268b6b6121c81bf623d60c07958153ba18ca33d5d98
```

It reproduces App's `clip-1`/`clip-2`, `shot-1`, `images`, 30-fps fixture and
checks V1 empty, V2 `[1,3)` and `[3,5)`, hold 2, order/mode, bindings, inverse,
and canonical reload. The same test family checks rational 30000/1001 fps
quantization (`1.001` / `3.001`). The migration golden remains at
`tests/editing_conformance/fixtures/recipe_m2_group_migration.json`; these are
Agent portable fixtures, not Runtime-generated artifacts or an App release.

The private free-multi golden is:

```text
/home/user/work/wt/agt-m2-free-move-set/tests/editing_conformance/fixtures/recipe_m2_free_move_set.json
```

Its permanent check is
`tests/editing_conformance/test_recipe_free_move_set.py::test_exact_app_drag_golden_selection_order_and_created_track_are_one_unit`.
The exact batch is existing `track.create(V3)` followed by `clip.move-set` in
one grouped commit: clip-1 to V2 at 1, clip-2 to V3 at 3, hold 2, with UI
selection order `[clip-2, clip-1]` and no pinned group. This candidate is also
private; no official generated client or App artifact exists for it.

Existing evidence, not release claims:

- c064 group source tests: **170 passed** using the eight-file targeted command
  recorded in `design/agent-group-full-union-review.md`.
- Runtime generic carrier checks: **89 passed**; the unchanged real migration
  probe is **7 passed / 2 failed** before accepted migration because the
  trusted bootstrap history/capture boundary is incompatible. No accepted
  group migration, restart, inverse, or browser result follows from that run.
- free-multi private Agent tests: **416 passed**, with Ruff and diff checks
  clean, as recorded by its worker. No official artifact, App qualification,
  or live release follows from that result.

## The three App contracts still to qualify

The source of truth is App
`src/tools/video-editor/hooks/useClipDrag.test.tsx` in the inspected current App
tree (`b1b27fa9cc77c517b82aacc560852d16fa7bfe44`). Preserve these tests and
their assertions:

1. `:774` — free multi onto a new bottom track: tracks V1/V2/V3; clip-1 on V2
   at 1 and clip-2 on V3 at 3, hold 2 each; one transaction; no pinned-group
   override; selection `[clip-2, clip-1]`; secondary ghosts.
2. `:1120` — existing-lane pinned group across tracks: V1 empty; clip-1 and
   clip-2 on V2 at 1 and 3 with original effect IDs, half-open length 2, ordered
   group metadata (`shot-1`, `images`, `clipIds`), selection
   `[clip-1, clip-2]`, one transaction.
3. `:1230` — pinned group onto new V3: one gesture creates/uses V3, preserves
   ordered `clipIds` and `mode: images`, and accepted readback must additionally
   show clip spans `[3,5)` and `[5,7)`.

The current producer deliberately refuses these cases in
`useClipDrag.helpers.ts:260-266,319-354` and
`commands/semanticGestures.ts:62-78`; this is the correct held state. The
canonical projection already exposes explicit occurrence, raw clip, raw child
track, and parent-track identity in
`src/tools/video-editor/data/shotCompositionProjection.ts:327-400`. Do not add
another editable group store, infer ownership from display IDs, or replace the
whole parent group array.

## Smallest next executable units

1. **Agent source composition and normal generation.** Compose the reviewed c064
   group source and the reviewed private `clip.move-set` source onto the current
   Main014 ordinary source, preserving the 55/29 ordinary floor. Produce one
   newly reviewed normal schema/client/artifact tuple containing the exact
   operations and captures above. Keep private source proposals, ordinary6ba,
   and any older published tuple distinct.

2. **Runtime matched source qualification.** Generate the matching Runtime
   counterpart from that exact Agent source. Resolve the known trusted-bootstrap
   `record.created`/command `created` (and history-boundary) blocker without
   weakening Agent reservation or capture guards. Run the unchanged group
   migration-plus-move real-provider cases, including accepted reload, lost-ACK
   retry/restart, guarded inverse/redo, and stale/disjoint rebase. Runtime's
   existing generic contract tests remain the carrier check; they are not group
   qualification.

3. **App existing-lane adapter.** After the matched generated tuple exists,
   add only the row-local read-side projection adapter and consume the published
   `occurrence.move` capture port. Capture from the pointer-down canonical basis;
   submit atomic child retrack and preserve explicit raw/parent bindings. Use
   the existing-lane golden and targeted Agent/App capture-parity tests before
   touching the two new-track/free-multi cases.

4. **App new-track group batch.** Reuse published `track.create` in the same
   durable grouped submission as the occurrence move; qualify the private
   existing-lane golden extended to V3 and accepted readback. Do not imply that
   standalone `track.create` proves group support.

5. **App free multi batch.** Consume the normally generated `clip.move-set`
   capture and submit it with the exact one-batch `track.create` shown in the
   private golden. Preserve authored member order separately from UI selection
   order and preserve the original free-multi assertions.

6. **Final App qualification.** Only after the three targeted tests pass should
   the App manager run the central current-source browser journey and the
   existing outbox/reload/undo/readback gates. No legacy snapshot writer or
   `pinnedShotGroupsOverride` parent writer is a substitute for the canonical
   command path.

## Exact tests for the next units

Agent pure group source:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_composed_schema.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/editing_conformance/test_pristine_initialize.py \
  tests/editing_conformance/test_current_group_slice.py \
  tests/editing_conformance/test_group_read_view.py \
  tests/editing_conformance/test_recipe_m2_group_migration.py \
  tests/editing_conformance/test_recipe_m2_group_move.py
```

Agent free-multi source:

```text
PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_free_move_set.py \
  tests/editing_conformance/test_recipe_m1_commands.py \
  tests/editing_conformance/test_recipe_add_delete_composition.py \
  tests/editing_conformance/test_recipe_m2_clip_add.py \
  tests/editing_conformance/test_recipe_clip_delete.py \
  tests/editing_conformance/test_recipe_scalar_commands.py \
  tests/editing_conformance/test_recorded_graph_roots.py \
  tests/sdk/test_timeline_semantic_reservations.py
```

Runtime's existing bounded carrier command is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_commit_validation.py \
  tests/test_timeline_commit_contract.py \
  tests/test_timeline_commit_closure_invariants.py
```

After matched generation, add/run the unchanged real group provider/runtime
cases and the App targeted file:

```text
npm exec vitest run --config config/testing/vitest.config.ts \
  src/tools/video-editor/hooks/useClipDrag.test.tsx
```

The App test command and the real Runtime/browser journey are next-unit gates,
not evidence available from this source-only handoff. Do not remove or weaken
the three `it.fails` markers until their original assertions pass through the
accepted command/outbox/readback path.

