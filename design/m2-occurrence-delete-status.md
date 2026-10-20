# M2 occurrence.delete v1: branch status

Branch `tl/agt-m2-occurrence-delete-continue`, from `tl/agt-m2-occurrence-delete`
(`1d3ead87`, one commit on the Bundle2 stack `a31d712d`). Candidate only. It is
not composable onto `tl/integration` until the stack below is composed.

## What was done here

`tl/integration` gained 8 M1 commits since the branch point (merge base
`fc324e83`). The branch's Bundle2 stack already contains most of them in
evolved form: opaque-item remap, `source_bundles` inverse images, shared-redo.
Folded in what was genuinely missing, preferring the branch's own code:

- `commit.py` `document_from_bundle` and `authoring_bundle.py`: immutable
  image reuse now compares exact encoded content (`_json`/`_canonical_json`),
  so `2` vs `2.0` and `1` vs `True` do not reuse an old image.
- Tests from integration: `test_commit_runtime_numeric_move.py` (new), the
  extra cases in `test_commit_runtime_opaque_items.py` and
  `test_commit_runtime_shared_inverse.py`, `test_timeline_commit_provider.py`,
  `test_timeline_commit_provider_document.py`, `test_authoring_bundle.py`,
  `test_recipe_m1_commands.py`; `artifacts.json` refreshed to integration's
  catalog digest (the catalog source is identical).
- Kept the branch side for the other `commit.py` conflicts (`AcceptedRecords`
  inverse records, `inverse_sources`, boundary verification): the branch
  supersedes integration's equivalent code. `_command_state.py` merged clean
  and unchanged.

## Machinery it depends on (all absent from `tl/integration`)

| Needs | Where (branch) | Introduced by |
|---|---|---|
| `root_identity`, `State.matches/get` root guards | `_command_state.py` | `84db8bde` native editing foundation |
| `AcceptedRecords`, restoration orders | `_collections.py` | `84db8bde` |
| `clip.delete` (`_delete_commands.delete`), collection selects/clear | `_delete_commands.py` | `84db8bde` |
| Recording/guard/selection, `ctx.capture_input`, `ctx.bind/clear/select` | `_recording.py`, `commands.py` | `cdf88d7e` (M1 engine) + `84db8bde` |
| Placement / occurrence media ops (`placement.move`, `occurrence.add-media`, `.swap-media`) | `native_placement_commands.py`, `native_occurrence_media_commands.py` | `7b61efd5` popup editing candidate |
| Shared-source materialization, `_remap_known_item_references`, `_authoring_shot_id` | `authoring_bundle.py` | main, plus Bundle2 `d4743e29` / `a31d712d` |
| Root-guard rebase for survivor alias, accepted-boundary inverse recovery | `_command_state.py`, `inverse.py`, `commit._check_reservations` | this commit |

New in this commit: `native_occurrence_delete.py`, `_root_inverse.py`
(`recover_source`, `occurrence_orders`, `arrange_restored`), the
`OccurrenceDeleteArgs` schema def, the golden
`recipe_m2_occurrence_delete.json`, and recipe and provider tests. The schema
stays a later group artifact candidate pending Runtime generation and App
native acceptance.

## Compose order for the group bundle

1. `84db8bde` native editing foundation (`AcceptedRecords`, `clip.delete`, `root_identity`).
2. `7b61efd5` popup editing candidate (placement and media ops).
3. `d4743e29` Bundle2 editing source.
4. `a31d712d` Bundle2 product successor.
5. The M1 integration commits above. This branch already carries them
   (reconciled here), so on a rebase they should drop out as already applied.
6. `1d3ead87` + this commit (`occurrence.delete`).
7. Group migration command (recorded, guarded `pinnedShotGroups` migration) and
   App read-side legacy group view. Delete refuses nonempty legacy groups with
   `migration_needed` until this lands.

Steps 1-4 are about 34k lines (96 files vs the merge base). Composing them is a
separate Bundle2 compose task, not part of this one.

## Evidence

Targeted via the test service (agent tree `72c7521e`): 358 passed, 23 deselected.
The 23 deselected are `integration`-marked and need a Runtime checkout.
Not run: Runtime `-m integration` lanes for delete, full suite, and App proof.
