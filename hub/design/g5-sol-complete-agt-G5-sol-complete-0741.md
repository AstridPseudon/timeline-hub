# G5 completion attempt — FAIL / BLOCKED

Worker: agt-G5-sol-complete-0741. Merge remains gated on P1; no integration merge requested.

Source base: `1d74f90bfb04b8f9975c2acb758e235eb3e8d9e1` (base tree `541a1f2cd3e6c0b3c227d07cc975de6db63de3ed`).
Final working tree: `02394e52650c1e72c0899e00341367e06ddec1bf`, calculated read-only using Git object hashing and checked against the indexed base tree; no commit/tree object/index writes.
Binary diff SHA-256: `0126b38307227ac0595ae4086769e402d96eb1db58fbdd20de6d5f7b7564c4df`.
Runtime checkout used: `a5d4258312c979024865ee704da2d632ca5b2730`.

## Changes and protected behavior

- Fixed the stale parser assertion by checking the selected apply command; retained all sheet/body/provenance/full-bundle assertions.
- Removed deleted three_way imports from both affected SDK behavioral modules. Their disjoint-edit and overlapping-edit witnesses now use the existing emitter/execute/replay path, preserving the original value and named-conflict assertions.
- Migrated the obsolete disk-merge scaffold to two real Timeline sessions with separate outboxes: disjoint changes merge, overlapping changes refuse without losing the successful writer, and an explicit chosen position is reapplied against a fresh head. The old 1.5/1.6/1.4 and text assertions remain. This adapts removed local merger/force entrypoints; it does not restore a stale-draft overwrite route.
- Migrated renderer-free publication scaffolds to the mounted commit caller and authenticated generated-client fixture. All 16 renderer-free save/validation/duplicate/narration scenarios pass; invalid candidates send zero commits, off-canvas authored values stay exact.
- Fixed the production copy staging: core preflight, stale-base refusal, staged output tracks (including a temporary lane for legacy implicit placement), exact authored placement fields with Runtime-owned links retained, destination child pins, and removal of old occurrences after payload capture.
- Added production CLI restructure proof comparing the entire parent payload, shot images, internal images and dependency manifest with the existing compiler's expected bundle. It also checks the original occurrence is removed and narration/transcript follow-ups run.
- Cut and narration lost-ack tests prove exact original body/key retries, one acceptance per operation, recovery of the original cut receipt through Runtime history, and one transcript creation followed by unchanged readback.
- Deleted the unreachable detached publish body and its unused imports; the retirement error and attached native publisher remain.
- No skips/xfails, assertion-to-absence replacements, alternate executor, provider/schema/pin/generated/dependency/HTTP changes, budget increases or suppressions.

## Final commands and results

Actual emitter/diff suite names were resolved with `rg --files tests/sdk tests/editing_conformance tests/timeline`: the two emitter conformance files and the SDK/format authoring-diff files below. The brief's literal initial command exited 4 before collection at its obsolete emitter filename; the corrected collection then exposed the retained three_way import. Both raw outputs are retained in tmpdir.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_sync.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_cli_sheet_v2.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/sdk/test_authoring_diff_cli.py tests/timeline/test_authoring_diff_format.py tests/sdk/test_timeline_restructure.py tests/sdk/test_scene_save_core.py tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones tests/sdk/test_timeline_checkout.py::test_two_writers_on_one_working_copy_merge_and_never_drop_each_others_edits
```

**2 failed, 215 passed in 29.49s** (exit 1). Raw output: `/tmp/w-623b7f1011/acceptance-complete.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/timeline/test_verbs_working_copy.py -k 'duplicate or copy_content or id_map or parses_to_its_handler'
```

**10 passed, 26 deselected in 1.66s** (exit 0). Raw output: `/tmp/w-623b7f1011/verbs-complete.log`. Deselection selects task-related cases; no test skip was introduced.

```sh
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-623b7f1011/ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 MYPY_CACHE_DIR=/tmp/w-623b7f1011/mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

All PASS (exit 0): Ruff **2148/2148**, private mypy **1904/1904**, vendor lock OK, artifacts current, whitespace clean. Baselines unchanged.

Earlier broader targeted run (including the complete checkout file): **316 passed, 3 failed, 4 warnings** in 72.03s, `acceptance-final.log`. Its failures were the same two duplicate gaps plus a fixture readback metadata mismatch in P4 note-rerun. Preserving that fixture's existing draft readback while enabling canonical readback for the new bundle adapter fixed the third failure without changing P4 assertions; P4-only confirmation **3 passed**, and the final command above reran P4 and both migrated checkout witnesses. All intermediate stdout/stderr and failure lists remain in `/tmp/w-623b7f1011/*.log`; none is represented as final green evidence.

## Caller/import proof and remaining blockers

Imported `astrid.sdk.timeline_duplicate`, `astrid.sdk.timeline_restructure`, `astrid.packs.timeline.cli`, and `astrid.sdk.timeline.store` from this worktree. `hasattr(store, "three_way")` and `hasattr(store, "publish_bundle")` are both false. Production search:

```sh
rg -n 'publish_bundle|three_way|document_diff|_cmd_publish|_configure_publish|commands-file|--publication' astrid/sdk/timeline astrid/sdk/timeline_duplicate.py astrid/sdk/timeline_checkout.py astrid/packs/timeline
```

No matches (rg exit 1). Mounted paths remain duplicate → _duplicate → _commit_bundle → timeline.open/commit, and CLI restructure → _commit_bundle → the same session/emitter/native capture path. Runtime still owns acceptance. No wire DTO or acknowledgement validation was changed.

Two positive behavioral tests remain failing, with their success expectations intact:

1. `test_duplicate_of_a_chapter_film_keeps_one_distinct_shot_per_chapter`: the real empty-destination commit path reaches `_doc_patch.py:311` and refuses **patch references media outside Runtime-verified inputs** (`dependency_changed`). The old publish stub only collected an intended document; the current witness requires actual existing command execution/compilation before asserting the same three-shot/placement/name properties. Source media belongs to the source closure, not the destination's empty closure. No fixture inserts unauthorized media into verified inputs. Existing duplicate archive cleanup executes after refusal.
2. `test_duplicate_commit_keeps_a_repeated_shot_shared`: the new production witness isolates a media-free shared-shot copy; the second occurrence.create raises **created identity is occupied** (`identity_collision`, `_recording.py:196`). The existing pure repeated-shot copy/identity/faithfulness assertions still pass. The return draft silently skipped the second occurrence; this draft exposes the actual unsupported birth instead of claiming a faithful copy.

These are evidence that caller-only migration is insufficient for the promised duplicate behavior. occurrence.create always creates a new shot; occurrence.duplicate creates a distinct shot; generic patches cannot create managed occurrence edges or authorize arbitrary new media. Fixing either by bypassing those guards, restoring detached writers, extending schemas, or adding an executor would violate this brief. Recommend an orchestrator-owned, narrowly scoped provider/capture capability for authenticated source-closure copying and placement of an existing copied shot, followed by independent review and this targeted rerun. Do not merge G5 before that work and P1 GO.

No full, live-HTTP, native14 or browser suite was requested/run. Existing targeted checkout tests did execute their local ffmpeg pixel witnesses. No Git writes, ref changes, network fetch/push or shared dependency mutations were performed. Other narration failure modes beyond the tested cut/narration lost acknowledgements are not qualified here.

