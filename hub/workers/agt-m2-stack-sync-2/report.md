`tl/agt-m2-stack-sync-2` now has `tl/integration` merged into the M2 stack, with all 17 conflicted files resolved and no markers left. Targeted tests pass apart from one failure that `tl/integration` itself already has (`test_giant_file_inventory_matches_rationale`, details below). I didn't commit; the commit message is at `…/workers/agt-m2-stack-sync-2/commit-msg` and `DONE` is created.

## How I resolved the conflicts
- **Runtime client and lock (`runtime.lock.json`, `astrid_runtime_client/*`):** I took the stack's pin. Its Runtime commit `4c145dc` is a descendant of integration's `6be9706`, and the stack's client already exports `TrackSetArgs`.
- **CLI, parser, `commands.py`, `sync.py`, `commit.py`, edit-command schema, `authoring_bundle.py`, `_track_commands.py`:** I kept the stack's side. Integration's versions of these were earlier forms of the same code, such as the `move_parser` and `track_label_parser` attributes and the `track.set`-only operation list. The stack's registry covers them.
- **Tests:**
  - I kept the stack's occurrence-label and `clip.set-params` assertions in `test_parent_track_label.py` and dropped integration's M1-only restriction test and its occurrence-select refusal case, since the stack deliberately lifts both. If you disagree, those two lines are the ones to revisit.
  - I kept both sides in `test_recipe_m1_commands.py` and `test_timeline_commit_provider.py`.
  - In `test_commit_runtime_opaque_items.py` I kept integration's two undo-restores-original assertions, and they pass.
- **Seam fix:** the text-binding spike's test seam now accepts the recorder's `restoring` and `after` options, because the stack's inverse code passes `restoring=True`. This was the only conflict-induced test failure.
- **`artifacts.json`:** I regenerated it with `scripts/artifact_manifest.py`, which updated the `cli-surface.json` hash.
- **D05/D06 deletions:** `inverses.py` and `core/extensions` are not re-added or imported anywhere. The only mention left is an assertion that `inverses.py` is absent.

## Test results (central service, targeted only)
| Run | Result |
|---|---|
| `tests/editing_conformance tests/timeline tests/sdk/test_timeline_capture_projection.py` | 1721 passed, 4 skipped, 5 xfailed, 2 failed. Both failures were the text-binding seam signature, now fixed. |
| text-binding spike, commit provider, `tests/packs/timeline`, `test_timeline_sync_native.py` (after the fix) | 402 passed, 1 xfailed |
| Broader neighbours: `tests/core`, `tests/sdk`, `tests/test_structure_contracts.py`, `tests/test_artifact_manifest.py` | 5675 passed, 403 skipped, 9 xfailed, 2 failed |
| Rerun of the two structure and manifest files after regenerating `artifacts.json` | 40 passed, 1 failed (`test_giant_file_inventory_matches_rationale`) |

- **Conflict-induced and fixed:** the two spike failures, and `test_committed_artifact_manifest_is_current`.
- **Pre-existing:** `test_giant_file_inventory_matches_rationale` says `generic_host.py` has 13798 lines against 13598 in the rationale file. The file and `docs/architecture` are identical to `tl/integration`, so this failure comes from there.
- **Unverified:** I only ran the targeted paths above, no full suite.

## Size against `tl/integration`
The whole diff is 94 files, +39643/−403. Outside `tests/` it is 38 files, +3818/−391. Of that, 31 files and +3676/−371 are under `astrid/` plus `cli-surface.json` and the runtime client. The remaining 56 files are tests and fixtures, mostly the roughly 7000-line recipe fixtures.

The largest product pieces are the edit-command schema (+794), `project_packs.py` (+375), `commit.py` (+340), `inverse.py` (+314) and `_collections.py` (+259).

## Proposed split into gated units
Product and test lines per commit:

| Unit | Commits | Product | Tests | What it proves |
|---|---|---|---|---|
| A | `3bf9e536` parent track labels with pinned Runtime client | +224/−17 | +1347 | Track-label edit end to end. This overlaps integration's own track-label work, so it may collapse to a small delta. |
| B | `84db8bde` native editing foundation | +1256/−169 | +4955 | Recorder, collections, scalar/trim/split/delete/clip-add commands, and the inverse/rebase engine. This is the large unit; if it needs splitting, put the schema and commands before the inverse and rebase changes. |
| C | `7b61efd5` popup editing candidate and `d4743e29` Bundle2 editing source | +1900/−153 | +18870 | Project-pack inputs and media inputs. |
| D | `a31d712d` product successor, `8c9c7428` release candidate and `027bd16d` Runtime pair qualification | ~+425/−137 | ~+1950 | The Runtime pin and contract metadata. Keep `027bd16d` with this unit, since it qualifies the exact Runtime pair. |
| E | `a6c2db3d` placement create/unplace and `d720b92f` placement corrections | +324/−3 | +10741 | Placement contracts. |
| F | `27037f0b` duplicate root-identity re-derive | +27 | +19/−9 | Duplicated occurrences get a re-derived root identity. |

Gate each unit with `tests/editing_conformance`, `tests/timeline` and `tests/sdk/test_timeline_capture_projection.py`. Add the commit-provider and sync tests from B onward. Since the stack is one merge on top of a linear 10-commit history, either gate cumulative tips A→F or cherry-pick each unit onto `tl/integration`. Conflicts in the cherry-picks would be the same ones resolved here.

## Evidence worth a look
- **Dead `inverse_intervening` in `commit.py`:** the stack keeps it as an always-empty list and checks intervening writes per target instead, so the variable is effectively dead there.
- **Overlap between A and integration's Bundle1:** integration's `_track_commands.py` and the stack's `_scalar_commands.track_set` are two implementations of the same feature. I kept the stack's, and `_track_commands.py` is now a re-export shim.
