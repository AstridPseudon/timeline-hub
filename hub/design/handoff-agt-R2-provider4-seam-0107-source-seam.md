# R2/F-D86 provider source-seam evidence

## Scope and identity

- Agent worktree HEAD: `0ae146e1b0acc6e4a82ba6b4f905d88bad48320c`; tree: `c91cfe3a28f2951584289bea31f1005222178bed`.
- Agent assigned test files were source-exact against the prior handoff; current file SHA-256 values are:
  - `tests/sdk/test_timeline_commit_provider.py`: `06228341db69c9604af57a786d4b8fc462ba881e59c195281c7151f2ce2e0ef4`
  - `tests/sdk/test_timeline_commit_provider_add_delete_runtime.py`: `02cae41f93c28b6167f11e342e70d0f717de97a7121342a11a7f7932ac6c1f67`
  - `tests/sdk/test_timeline_semantic_reservations.py`: `6112aa1743b0958da91eaec8354a2861a7189b43b3c5bfab2f91c5a82c13e6f0`
- Rehearsal-recorded Runtime: `766fd6700c3128ea9fc833086a517de2acb535e2`.
- Released qualified Runtime pin: `a3cd1a3214fa1632879c21d82d1abb9ea720b1de`.
- Runtime `timeline_commit_auth.py`, `timeline_commit_store.py`, and `timeline_commit_port.py` blobs compare equal between those refs. No current behavioral outcome was rerun or inferred from that comparison.

## Four live targets

1. `tests/sdk/test_timeline_commit_provider.py:990-1010`, `test_restore_undo_redo_exact_full_closure_and_unknown_fields`.
   - Authentic XML observation: `CommitRejected: ambiguous or unexpected fork materialization`; traceback terminates at Agent `astrid/sdk/timeline/inverse.py:1021`, wrapped by `astrid/sdk/timeline/commit.py:1467`.
   - Caller/fixture/seam: `DetachedRealm.call` (`test_timeline_commit_provider.py:103-105`) -> `create_runtime_commit_service().commit` -> fixture’s two occurrence moves and exact `timeline.restore` (`:960-963`) -> inverse execution (`astrid/sdk/timeline/commands.py:265-269`) -> accepted-history materialization validation (`inverse.py:995-1024`). The logical input is the exact retained timeline closure; the failing physical seam is the accepted materialization binding check.
   - Passing comparator: `test_restore_dry_run_digest_and_accept_race` (`:966-987`) and `test_restore_and_inverse_capture_only_resulting_retained_inputs` (same file, XML-qualified transcript/config variants) pass, but neither exercises this two-move full undo/redo closure.
   - Classification: observed historical error; source seam is Agent inverse materialization validation; current behavioral status is unknown. No source correction is justified by this trace.

2. `tests/sdk/test_timeline_commit_provider_add_delete_runtime.py:63-149`, `test_native_add_delete_one_publication_inverse_redo_restart_reservations[net-zero]`.
   - Authentic XML observation: inverse-record assertion mismatch. The target expected `writes=[ref, before=ABSENT, after=ABSENT]`; the actual record retained the `parent/clip:first-clip` absent-to-present row with its full literal/opaque value.
   - Caller/fixture/seam: `submit` (`:37-42`) -> Runtime `commit_timeline` -> Agent provider command batch (`:63-100`) with native add followed by native delete -> inverse retry (`:121-149`) -> authenticated history record returned by the commit path. This is an exact record-image mismatch, not a Runtime exception; the source trace does not establish whether record projection belongs to Agent or Runtime.
   - Passing comparator: native clip delete reload/inverse/redo with retained pins (`tests/sdk/test_timeline_commit_provider.py:1402-1431`) and retired-identity reallocation protection (`:1500-1520`) pass, but they do not cover add/delete net-zero record coalescing.
   - Classification: observed historical error; ownership/current outcome unknown. No guessed common cause or product edit.

3. `tests/sdk/test_timeline_commit_provider_add_delete_runtime.py:63-149`, `test_native_add_delete_one_publication_inverse_redo_restart_reservations[replace-existing]`.
   - Authentic XML observation: Runtime terminal error `inverse stage native writes do not cover its authenticated effect image`; stack passes through Runtime store and ends at Runtime auth validation.
   - Caller/fixture/seam: `submit` (`:37-42`) -> Runtime `commit_timeline` -> native delete-existing then native add-existing batch (`:63-100`) -> inverse retry (`:121-149`) -> Runtime auth effect-image validation at `runtime_protocol/timeline_commit_auth.py:1739`, reached through `timeline_commit_store.py:32`.
   - Passing comparator: the ordinary native clip-delete reload/inverse/redo neighbor cited above passes; it does not exercise replacement of an existing physical identity in one publication.
   - Classification: observed historical Runtime terminal seam only; no Runtime diagnosis or fix attempted, and no Agent test change is indicated. Relevant Runtime auth/store/port source is identical at recorded local HEAD `766fd670` and released pin `a3cd1a`; current behavioral outcome remains unknown.

4. `tests/sdk/test_timeline_semantic_reservations.py:84-94`, `test_aggregate_children_are_retired_in_their_occurrence_scope`.
   - Authentic XML observation: `CommitRejected: ambiguous or unexpected fork materialization`; traceback terminates at Agent `astrid/sdk/timeline/inverse.py:1021`, wrapped by `astrid/sdk/timeline/commit.py:1467`.
   - Caller/fixture/seam: `DetachedRealm.call` -> custom `test.create-roots` plus `fixture.clip-delete` (`semantic_reservations.py:24-45`, `recorded_graph_roots.py:34-58`) -> inverse redo -> accepted-history materialization validation (`inverse.py:995-1024`). The fixture intentionally includes opaque root values and an aggregate parent/child retirement; Agent `_physical_state` projects aggregate placements at `inverse.py:93-108` before the materialization check.
   - Passing comparator: seeded clip deletion and aggregate removal without child writes (`semantic_reservations.py:70-114`), plus introduced-and-deleted-in-one-publication (`:128-131`), pass. They do not qualify this introduced aggregate child-retirement undo/redo topology.
   - Classification: observed historical error; source seam is the same Agent validation boundary but the fixture topology is distinct, so no common-cause claim. Current behavioral status unknown; no source correction justified.

## Checks

- `PYTHONPYCACHEPREFIX=/tmp/agt-R2-provider4-source-seam-0107-static/pycache python3 -m py_compile tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_add_delete_runtime.py tests/sdk/test_timeline_semantic_reservations.py` — passed.
- `/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_add_delete_runtime.py tests/sdk/test_timeline_semantic_reservations.py` — passed.
- Mypy baseline and candidate, each with an isolated cache and `--follow-imports=silent`, both returned the same environment diagnostic in NumPy `__init__.pyi:737` (`Type statement is only supported in Python 3.12 and greater`); no target-specific diagnostic.
- `git diff --check` — passed.
- No pytest, test collection, service execution, build, browser, render, probe, cache, or ABI-policy work was run.
