# PASS — agt-G234-current-qualified-join-0524 current-preserving join

Implemented the authorized current-preserving G2/G3/G4 join and the two independently reviewed narrow fixes. The final candidate is source-qualified and the exact two requested live nodes pass on exact Runtime be584. It is ready for independent review of the new composition; this is an implementation report, not that independent review.

## Exact identity and scope

- Base commit: `bf40d6bb5923210a3f5d210414c9ad737b40403d`; tree `7b914a6e935571b11e8ea1ffdf596aa6e25a4c83` (exact brief baseline).
- Final source tree: **`5226dfdd98d50e06328c523691c09bcf7f4408f1`**; matched by the central test service snapshot.
- Final commit: pending harness; this worker did not commit, merge, checkout, fetch, push, change refs, or write Git internals.
- Exactly **25 changed paths**: 21 reviewed remaining G234 paths, two elementRef paths and three replay paths, with provider-test overlap. Zero deleted files.
- All paths outside that union remain at the audited current base. The two native_word_anchor fixture/status files are excluded and remain exact 5292.
- No pending FPS e50/9ea, anchor repair, fork, inverse-stage48d, show feature, generated file, schema, pin, executor, or Proof-owned HTTP implementation was imported.

## Provenance and integration decisions

- `9cf0fde2` = `9cf0fde2f57603813d81733ee8b0f7117ffd634c`.
- `736cfdd15` = `736cfdd15a83c9d22bfcc1269967d3b319eae9a8`.
- `c79398561` = `c79398561e5612d0a393074e6b9a198992d77f5b`.

Used worktree-only patch application, checked before each apply: `HEAD..9cf0fde2` restricted to the 19 nonbaseline remaining G234 paths; `736cfdd15^..736cfdd15` restricted to its exact two paths; and `c79398561^..c79398561` restricted to its exact three paths. No ancestry or merge parent was adopted. Baselines were tightened only after normal tools measured the exact reviewed improvements.

The current validation blob matched 9cf exactly before porting. Final validation is the exact 736 donor blob. The replay delta applied cleanly to current commit.py and rebase.py; commit.py keeps the audited metadata discovery and V2 admission hook. The provider test composes the exact 9cf scope-binding regression with the exact c793 replay regressions. Existing assertions were not rewritten, removed, skipped, or marked xfail.

The independent evidence consumed was G234 correction review 0500 (source PASS 147/87/112/58/146), V2 elementRef review 0521 (PASS 69 + two live nodes on be584), legacy replay review 0453 (source PASS 2/28/127), G4 admission/group/create reviews, and current audit restoration PASS. No settled decisions were changed.

## Production callers and contract preservation

The mounted public timeline.open -> Timeline/TimelineSession path, bounded function rerun, emitter, CLI/sheet adapters, authenticated outbox, guarded public publication undo and local numeric undo are retained at current audited blobs. RuntimeCommitService.commit now passes the authenticated request and actual evaluated landing head through legacy rebase.replay -> commands.execute and keeps replay-generated landing steps/dependencies rather than overwriting them with original-base metadata. Final validation calls the exact reviewed elementRef validator.

G4 remains wired through RemoteTimelines.create_empty -> legal shell + session commit_many initialization/config patch; narration and element writers use commits; requester publication forwards group_id and reaches real RemoteTasks.create. The two unchanged live tests establish create/bootstrap/exact retry and real render-task admission/retry on this final tree.

Full v2 request fields remain: api_version/project_id/timeline_id/base_revision_id/base_publication_id/commands/label, steps(id,label,intent,tags,command_ordinals,patch,reads), merge(fields|atomic), reads/dry_run/source/rationale/group_id and stable idempotency. Existing complete {data,receipt}, accepted/merged/authentic historical rebased, canonical document/head/revision/digests/records/effects/steps/dependencies/history/undo_steps, structured conflict/invalid details and preview would_status handling remain protected by unchanged session/provider facades plus the original DTO, provider, emitter, metadata, step-undo and publication controls below. No metadata filtering or guard bypass was introduced.

## Environment and import origins

Agent tests use shared `/home/user/work/venv-agent/bin/python` (3.13.16), dependency files read-only, source via explicit PYTHONPATH. All caches, basetemps, archive and private type environment are under `/tmp/w-4f3d8d00b5` (the worker tmpdir locator resolves there).

Runtime source is a private read-only-use `git archive be5848e17fbf68100286114883f5820fe4755911` from the shared Runtime object store: tree `d6f20f841098811ad1351926139f515807e9c5ed`. All **465** extracted tracked blobs match the exact source commit after testing. The shared Runtime checkout had advanced to 1a5baea32903586073d121cabd9d610cea0f3704 during this task; it was not changed by this worker.

Actual loaded runtime_protocol service/store/timeline_commit/port/provider all resolve under `/tmp/w-4f3d8d00b5/runtime-be584/runtime_protocol/`. Direct Agent imports resolve under this worker worktree; live Agent imports resolve under the service snapshot. The test-only bootstrap asserts every relevant module origin, prints it, sets PYTHONPATH to snapshot + private be584, and changes no product function or assertion. ASTRID_RUNTIME_CHECKOUT points at `/home/user/work/runtime` only as the helper Git object locator for existing pinned fixture archives; loaded production Runtime modules are exact be584.

The historical `/tmp/astrid-u2-typecheck/bin/python` was absent. Recreated its documented environment privately with `/usr/bin/python3.11` (3.11.17), mypy 1.17.0, numpy 2.4.6, PyYAML 6.0.3, types-PyYAML 6.0.12.20260906, mypy-extensions 1.1.0, pathspec 1.1.1, typing-extensions 4.16.0. No shared installation was edited.

## Exact direct test commands and results

All commands below run from the assigned worktree, with this environment (no service/sockets in the direct lanes):

```bash
export TMPDIR=/tmp/w-4f3d8d00b5
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=/home/user/work/wt/agt-G234-current-qualified-join-0524:/tmp/w-4f3d8d00b5/runtime-be584
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
export ASTRID_WORD_ANCHOR_SEED_RUNTIME=/home/user/work/runtime
export RUFF_CACHE_DIR=/tmp/w-4f3d8d00b5/ruff
export MYPY_CACHE_DIR=/tmp/w-4f3d8d00b5/mypy
```

### assembly147: 147 passed in 24.32s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/timeline/test_authoring_bundle.py tests/timeline/test_meta_validator.py tests/timeline/test_shot_composition_projection.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_commit_timing_validation.py tests/editing_conformance/test_commit_v2_validation.py --basetemp=/tmp/w-4f3d8d00b5/assembly147-base
```

### assembly87: 87 passed in 20.08s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_open_commit.py tests/sdk/test_timeline_sheet.py tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_cli_sheet_v2.py --basetemp=/tmp/w-4f3d8d00b5/assembly87-base
```

### assembly112: 112 passed, 5 deselected in 19.54s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m 'not integration' tests/sdk/test_timeline_render_publication.py tests/sdk/test_timeline_pristine_initialize_runtime.py tests/packs/rendering/test_assemble_timeline.py tests/v10/test_timelines_create.py tests/timeline/test_authoring_media.py --basetemp=/tmp/w-4f3d8d00b5/assembly112-base
```

### assembly58: 58 passed in 19.91s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer tests/sdk/test_timeline_inverse_binding.py tests/sdk/test_timeline_narration_commit.py tests/core/test_timeline_element_publication.py tests/sdk/test_timeline_assembly.py tests/packs/video_editing/test_runtime_orchestration.py --basetemp=/tmp/w-4f3d8d00b5/assembly58-base
```

### assembly146: 146 passed in 211.38s (0:03:31)

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_open_commit_v2.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py --basetemp=/tmp/w-4f3d8d00b5/assembly146-base
```

### core90: 90 passed in 18.25s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_commit_provider_document.py tests/timeline/test_authoring_bundle.py tests/timeline/test_meta_validator.py tests/timeline/test_shot_composition_projection.py --basetemp=/tmp/w-4f3d8d00b5/core90-base
```

### facade107: 107 passed in 20.05s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_open_commit_v2.py tests/sdk/test_timeline_current_union_schema.py::test_inverse_steps_is_exactly_the_new_optional_shape tests/sdk/test_timeline_composed_schema.py::test_inverse_schema_accepts_whole_and_selected_step_forms_and_rejects_bad_shapes --basetemp=/tmp/w-4f3d8d00b5/facade107-base
```

### numeric2: 2 passed in 3.73s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_checkout_history_boundaries.py::test_new_unsent_steps_stop_before_the_accepted_boundary tests/sdk/test_timeline_persistence.py::test_restart_a_fresh_process_sees_every_edit_and_the_undo_history --basetemp=/tmp/w-4f3d8d00b5/numeric2-base
```

### required6: 106 passed, 1 deselected in 9.76s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m 'not integration' tests/editing_conformance/test_commit_legacy_text_reference.py tests/sdk/test_timeline_inverse_binding.py tests/sdk/test_timeline_commit_provider_document.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/sdk/test_timeline_render_publication.py tests/sdk/test_timeline_narration_commit.py --basetemp=/tmp/w-4f3d8d00b5/required6-base
```

### replay28: 28 passed in 8.01s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_native_word_anchor_vectors.py tests/editing_conformance/test_doc_patch_v2.py::test_mixed_native_capture_keeps_inherited_reads_at_original_boundaries tests/editing_conformance/test_doc_patch_v2.py::test_mixed_native_inherited_reads_replay_at_landing_head tests/editing_conformance/test_doc_patch_v2.py::test_inherited_native_read_conflicts_with_later_dependency_writes tests/sdk/test_timeline_commit_provider.py::test_legacy_rebase_records_landing_step_metadata tests/sdk/test_timeline_commit_provider.py::test_replay_accepts_legacy_request_head_and_builds_steps --basetemp=/tmp/w-4f3d8d00b5/replay28-base
```

### patchundo: 427 passed in 68.67s (0:01:08)

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_doc_patch_v2.py tests/editing_conformance/test_inverse_clear_batches.py tests/editing_conformance/test_grouped_clip_cache_inverse.py tests/editing_conformance/test_occurrence_media_manifest_inverse.py tests/sdk/test_timeline_commit_provider.py --basetemp=/tmp/w-4f3d8d00b5/patchundo-base
```

### artifacts: 41 passed in 8.82s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_vendor_lock.py tests/test_artifact_manifest.py tests/v10/test_release_reproducibility.py tests/stage1/test_vendored_workspace_client_parity_luna.py --basetemp=/tmp/w-4f3d8d00b5/artifacts-base
```

### replay2: 2 passed in 1.27s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_commit_provider.py::test_legacy_rebase_records_landing_step_metadata tests/sdk/test_timeline_commit_provider.py::test_replay_accepts_legacy_request_head_and_builds_steps --basetemp=/tmp/w-4f3d8d00b5/replay2-base
```

### validation69: 69 passed in 2.45s

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_commit_legacy_text_reference.py tests/editing_conformance/test_commit_v2_validation.py tests/editing_conformance/test_commit_timing_validation.py --basetemp=/tmp/w-4f3d8d00b5/validation69-base
```

Marker deselections are the original integration exclusions in the specified non-live lanes. The original two live nodes are executed separately below; no test was skipped, weakened or xfailed. The original retained-source replay node remains FPS-blocked before its body per review 0453; it was not rerun. The three known Runtime-owned failures were not redone.

## Exact central-service live run

- Service ID: `agt-G234-current-qualified-join-0524-agt-G234-current-qualified-join-0524-live-two-integration-1023053451-549`.
- Snapshot tree: `5226dfdd98d50e06328c523691c09bcf7f4408f1`.
- Result: **PASS, exit 0; 2 passed in 9.04s**, 12s service duration.

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-G234-current-qualified-join-0524 agt-G234-current-qualified-join-0524-live-two-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agt-G234-current-qualified-join-0524-agt-G234-current-qualified-join-0524-live-two-integration-1023053451-549
```

The two exact nodes and full external runner:

```bash
#!/bin/bash
set -e
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$PWD:/tmp/w-4f3d8d00b5/runtime-be584"
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
export TMPDIR=/tmp/w-4f3d8d00b5
exec /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -o pythonpath=/tmp/w-4f3d8d00b5 -p qualified_runtime -p no:cacheprovider -m integration tests/sdk/test_timeline_pristine_initialize_runtime.py::test_remote_create_empty_uses_live_commit_bootstrap_and_exact_replay tests/sdk/test_timeline_render_publication.py::test_requester_render_reaches_real_task_admission_after_commit --basetemp=/tmp/w-4f3d8d00b5/live-two-base
```

Bootstrap source, which only selects/asserts import origins:

```python
"""Test-only bootstrap of the exact reviewed Runtime; no product overrides."""
import importlib
import os
import pathlib
import sys

sys.path.insert(0, '/tmp/w-4f3d8d00b5/runtime-be584')
os.environ['PYTHONPATH'] = str(pathlib.Path.cwd()) + ':/tmp/w-4f3d8d00b5/runtime-be584'
os.environ['ASTRID_RUNTIME_CHECKOUT'] = '/home/user/work/runtime'

def pytest_configure(config):
    runtime = '/tmp/w-4f3d8d00b5/runtime-be584'
    agent = str(pathlib.Path.cwd())
    sys.path.insert(0, runtime)
    os.environ['PYTHONPATH'] = agent + ':' + runtime
    os.environ['ASTRID_RUNTIME_CHECKOUT'] = '/home/user/work/runtime'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    for name in ('runtime_protocol.service', 'runtime_protocol.store', 'runtime_protocol.timeline_commit',
                 'runtime_protocol.timeline_commit_port', 'runtime_protocol.timeline_commit_provider',
                 'astrid.sdk.timeline.commit', 'astrid.sdk.timeline.validation'):
        module = importlib.import_module(name)
        origin = pathlib.Path(module.__file__).resolve()
        expected = pathlib.Path(runtime if name.startswith('runtime_protocol') else agent)
        assert origin.is_relative_to(expected), (name, origin, expected)
        print('QUALIFIED_IMPORT', name, origin)
```

Operational service setup: added one unique worker-owned named entry to the task-named shared tests/suites.conf, invoking the external runner in this worker directory. Existing suite entries were untouched. The first service request attempted CLI options in --files and was rejected as `bad file arg -o` before snapshot/execution; this is not a product/test failure. A local collect-only probe initially lacked Runtime before conftest load; moving import-path setup to plugin import fixed collection (two exact nodes). No sockets were opened directly by this worker.

Live log: [agt-G234-current-qualified-join-0524-agt-G234-current-qualified-join-0524-live-two-integration-1023053451-549/log.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-G234-current-qualified-join-0524-agt-G234-current-qualified-join-0524-live-two-integration-1023053451-549/log.txt).

## Quality, baseline tightening, artifacts and diff

Normal measured counts were Ruff 2149 vs old baseline 2150, and private mypy 1914 vs old baseline 1915. Used normal --write-baseline tools to lock those improvements. Final make ruff is **2149/2149**, final compare_mypy_baseline is **1914/1914**. No budget increase.

The mypy baseline equals the reviewed 9cf baseline except the normal tool records the new private interpreter path in command[0]. Ruff baseline is exact 9cf. This is the only environment-specific metadata composition.

```bash
/home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline --write-baseline
make ruff PY=/home/user/work/venv-agent/bin/python
export MYPY_CACHE_DIR=/tmp/w-4f3d8d00b5/mypy-private
/tmp/w-4f3d8d00b5/typecheck/bin/python -m scripts.reshape.compare_mypy_baseline --write-baseline
/tmp/w-4f3d8d00b5/typecheck/bin/python -m scripts.reshape.compare_mypy_baseline
```

Scoped Ruff checked all 23 changed Python files against exact reviewed donor source through --stdin-filename: **124 inherited findings; no added per-file code/message findings**. Scoped private mypy --follow-imports=silent checked all 10 production files: **34 inherited findings in 3 files**, exactly matching a donor --shadow-file comparison; no added path/message findings. Raw scoped output exits 1 for inherited debt and is not claimed lint-clean. The normal ratchets pass.

```bash
/tmp/w-4f3d8d00b5/typecheck/bin/python -m mypy --follow-imports=silent astrid/packs/rendering/actions/assemble_timeline/run.py astrid/packs/rendering/shared/runtime_stitch.py astrid/packs/video_editing/shared/runtime_orchestration.py astrid/sdk/remote.py astrid/sdk/timeline/assembly.py astrid/sdk/timeline/commit.py astrid/sdk/timeline/publish.py astrid/sdk/timeline/rebase.py astrid/sdk/timeline/validation.py astrid/sdk/timeline_elements.py
python3 /tmp/w-4f3d8d00b5/compare_mypy.py
python3 /tmp/w-4f3d8d00b5/scoped_checks.py
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
python3 /tmp/w-4f3d8d00b5/audit_source.py
```

Vendor lock (exact frozen normal34e producer) PASS; artifact manifest current; vendor/artifact/reproducibility/client-parity test lane **41 passed**; tracked diff check PASS; source-scope/tree/protected-blob audit PASS. Patch application reported an inherited donor trailing blank line at EOF in the new narration test; exact reviewed donor blob is retained rather than silently reformatted. No original source line or assertion was changed to mask a failure.

Initial quality setup attempts are recorded honestly: the original runner could not spawn the missing historical private checker; the shared Python 3.13 checker stops on missing yaml stubs and NumPy syntax under the configured 3.11 target. These were environment setup failures. The privately recreated exact original environment completed the normal gate and donor comparisons above.

## Every changed path: donor map and final source hash

Full source commit IDs are listed above. Git blob hashes are complete. JSON with base/final Git blob IDs and SHA-256 for every changed file is retained at `workers/agt-G234-current-qualified-join-0524/source-audit.json`.

| Path | Donor | Donor blob | Final blob / composition |
| --- | --- | --- | --- |
| `astrid/packs/rendering/actions/assemble_timeline/run.py` | `9cf0fde2` | `3588d5481e1ec5a60d2368c489d4bef33034f05d` | `3588d5481e1ec5a60d2368c489d4bef33034f05d` — exact donor blob |
| `astrid/packs/rendering/shared/runtime_stitch.py` | `9cf0fde2` | `cf16b09077c30f4efb18eaa58744a2f4cced7358` | `cf16b09077c30f4efb18eaa58744a2f4cced7358` — exact donor blob |
| `astrid/packs/video_editing/shared/runtime_orchestration.py` | `9cf0fde2` | `1358b3a248d5d39f13d9add4dc35cff2f1e11501` | `1358b3a248d5d39f13d9add4dc35cff2f1e11501` — exact donor blob |
| `astrid/sdk/remote.py` | `9cf0fde2` | `5c62de2c215f37ff2d3874bde2603bb0205df54a` | `5c62de2c215f37ff2d3874bde2603bb0205df54a` — exact donor blob |
| `astrid/sdk/timeline/assembly.py` | `9cf0fde2` | `55e29d1245469d447821e39b3daa0f4d391d072f` | `55e29d1245469d447821e39b3daa0f4d391d072f` — exact donor blob |
| `astrid/sdk/timeline/commit.py` | `c79398561` | `74307b7213147ffc9139160f9b6247641e4701d3` | `219b0093eb1ab9c25d82a8cc2834e95c097d781d` — audited current base plus narrow c793 legacy replay hunks; metadata/V2 retained |
| `astrid/sdk/timeline/publish.py` | `9cf0fde2` | `ec1687a4a7f1123d8a17a2fcd95dfe21f4fec427` | `ec1687a4a7f1123d8a17a2fcd95dfe21f4fec427` — exact donor blob |
| `astrid/sdk/timeline/rebase.py` | `c79398561` | `9b416d026183703db31d8f008272f6c1d4a7e181` | `9b416d026183703db31d8f008272f6c1d4a7e181` — exact donor blob |
| `astrid/sdk/timeline/validation.py` | `736cfdd15` | `6d9b3dd3d0cdc7f25ead8b9546c1db6912365b03` | `6d9b3dd3d0cdc7f25ead8b9546c1db6912365b03` — exact donor blob |
| `astrid/sdk/timeline_elements.py` | `9cf0fde2` | `30a0cbbb83a772715901fb74e9eed0bdcc104310` | `30a0cbbb83a772715901fb74e9eed0bdcc104310` — exact donor blob |
| `scripts/reshape/baselines/mypy_astrid.json` | `9cf0fde2` | `276cba7275abd06a423e72208947c77e78ff7508` | `1f53ed011a64dcc52c3c6622e3be5a4281408a9c` — normal tool: measured one-finding tightening; private interpreter path retained in mypy command |
| `scripts/reshape/baselines/ruff_astrid.json` | `9cf0fde2` | `7b0797217108c04ddc84ed70644b556cba3b4ffd` | `7b0797217108c04ddc84ed70644b556cba3b4ffd` — normal tool: measured one-finding tightening; private interpreter path retained in mypy command |
| `tests/editing_conformance/test_commit_legacy_text_reference.py` | `736cfdd15` | `f58fff911b0913de297f20447024d31724cc0b27` | `f58fff911b0913de297f20447024d31724cc0b27` — exact donor blob |
| `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` | `9cf0fde2` | `05f7aa2bd862fc608ee17515d373c5f5b47c27eb` | `05f7aa2bd862fc608ee17515d373c5f5b47c27eb` — exact donor blob |
| `tests/packs/rendering/test_assemble_timeline.py` | `9cf0fde2` | `719ef7e44a22ecc284d1d31ae4a7e881b8400cfe` | `719ef7e44a22ecc284d1d31ae4a7e881b8400cfe` — exact donor blob |
| `tests/sdk/test_p4_cli_sheet_v2.py` | `9cf0fde2` | `fd248182a0e1c120fa6440994da545c4e13219ad` | `fd248182a0e1c120fa6440994da545c4e13219ad` — exact donor blob |
| `tests/sdk/test_p4_commit_v2.py` | `9cf0fde2` | `85218e8e99a1c7602d2b7ee399f3847fac759186` | `85218e8e99a1c7602d2b7ee399f3847fac759186` — exact donor blob |
| `tests/sdk/test_p4_note_rerun.py` | `9cf0fde2` | `80c15e2944b5660a18077aa38f84cf3b3ced09bb` | `80c15e2944b5660a18077aa38f84cf3b3ced09bb` — exact donor blob |
| `tests/sdk/test_p4_ten_note_provider.py` | `9cf0fde2` | `1ed257c4604552793d2eaabfc117babe93c5b445` | `1ed257c4604552793d2eaabfc117babe93c5b445` — exact donor blob |
| `tests/sdk/test_timeline_commit_provider.py` | `9cf0fde2` | `c8fb3f9b4606ff1d8e1169988a16b79df1da5350` | `90412927b5a6f6b998bf0961c46be0dcee87962f` — exact 9cf blob plus narrow c793 replay regression delta |
| `tests/sdk/test_timeline_narration_commit.py` | `9cf0fde2` | `d4197ab2c9bb0a6c518bb3747b8da95fe919b1b1` | `d4197ab2c9bb0a6c518bb3747b8da95fe919b1b1` — exact donor blob |
| `tests/sdk/test_timeline_pristine_initialize_runtime.py` | `9cf0fde2` | `0c2a112a200a496cd48c2b6a3e9ce75c7ad00207` | `0c2a112a200a496cd48c2b6a3e9ce75c7ad00207` — exact donor blob |
| `tests/sdk/test_timeline_render_publication.py` | `9cf0fde2` | `74c97482a69d2b8beda67a7c3cf935710ffa893b` | `74c97482a69d2b8beda67a7c3cf935710ffa893b` — exact donor blob |
| `tests/timeline/test_authoring_media.py` | `9cf0fde2` | `25037aa6cfbd14f55b10bf01b6084a103f933d6f` | `25037aa6cfbd14f55b10bf01b6084a103f933d6f` — exact donor blob |
| `tests/v10/test_timelines_create.py` | `9cf0fde2` | `c23cd4e6b7d4979950c70cdab84b09cb0d8be8f0` | `c23cd4e6b7d4979950c70cdab84b09cb0d8be8f0` — exact donor blob |

## Protected exact blobs

| Path | Required source | Retained blob |
| --- | --- | --- |
| `artifacts.json` | `HEAD` | `d68a3884c65c5684634c22ebb03def35ba277992` |
| `astrid/core/timeline/__init__.py` | `HEAD` | `92a26c467c4c9975d8a969f6b037b0cae37353c7` |
| `astrid/core/timeline/authoring_bundle.py` | `HEAD` | `d0d7dbd0aa961f1b2bd1442f2d4daa2ad7b53193` |
| `astrid/core/timeline/shot_composition.py` | `HEAD` | `23105de991d1bde32b4ed8c98e0c036f560e0629` |
| `astrid/core/timeline/shot_composition_projection.py` | `HEAD` | `04493587ea7de6b933774914df9ed4d4706ef860` |
| `astrid/core/timeline/validators/registry.py` | `HEAD` | `c9ba3bcf86902ffa518f2a5e96881ff29d2d6168` |
| `astrid/sdk/timeline/_commit_timing_validation.py` | `HEAD` | `990d256c975b87ddeff381087187be6524d52d7c` |
| `astrid/sdk/timeline/commit_session.py` | `HEAD` | `b139373806031d0d6e50f5eb1d27d0b3973d2255` |
| `astrid/sdk/timeline/inverse.py` | `HEAD` | `8d1ead5f132c2c551b142abd64c4e4f79e23d311` |
| `astrid/sdk/timeline/sync.py` | `HEAD` | `5e7dfeec3b2a7f03849b58e5d09a5456b81a0a7b` |
| `runtime.lock.json` | `HEAD` | `924834f795b81c0716e8bf40ab3f08de71d819fa` |
| `tests/editing_conformance/native_word_anchor_fixture.py` | `5292b388a` | `af7407a5a2d42bb63b5cc11ba4a4924d3186c607` |
| `tests/editing_conformance/test_document_patch_emitter_engine.py` | `HEAD` | `1632ba66d5fc28d073d99a3dcddb9493c7044b6c` |
| `tests/editing_conformance/test_native_word_anchor.py` | `5292b388a` | `5db819f485da679f613ef04455ec19708d316d6a` |
| `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` | `c4c6236838` | `05f7aa2bd862fc608ee17515d373c5f5b47c27eb` |
| `tests/editing_conformance/test_p4_ten_note_v2_runtime.py` | `c4c6236838` | `5ee8dd5b863c164e0ea5f03257ac61849a425061` |
| `tests/sdk/test_p4_cli_sheet_v2.py` | `c4c6236838` | `fd248182a0e1c120fa6440994da545c4e13219ad` |
| `tests/sdk/test_p4_commit_v2.py` | `c4c6236838` | `85218e8e99a1c7602d2b7ee399f3847fac759186` |
| `tests/sdk/test_p4_note_rerun.py` | `c4c6236838` | `80c15e2944b5660a18077aa38f84cf3b3ced09bb` |
| `tests/sdk/test_p4_ten_note_provider.py` | `c4c6236838` | `1ed257c4604552793d2eaabfc117babe93c5b445` |
| `tests/sdk/test_timeline_commit_provider_document.py` | `HEAD` | `1b1d0378e52e10e84549e6f651914dbba0a972eb` |
| `tests/sdk/test_timeline_inverse_binding.py` | `HEAD` | `cd909f5d8156683cc6aa6bba1295d30c9abe83a6` |

The source audit reconstructs Git tree hashes entirely in memory and verifies its algorithm against the existing base tree before calculating the final tree. All tracked paths outside the allowed 25-file union are unchanged; no deletion, schema/client/pin/artifact diff or extra product file exists.

## Remaining limits and next step

No implementation blocker remains for this bounded join. Do not treat this as a full-suite, all-G4/R5, P4 HTTP, native14, crash24, mounted App, FPS/anchor/fork, or all54 qualification. No full, browser, farm, heavy suite or Proof-owned P4 HTTP body was run.

The harness should create the one supplied G234-current-join commit. Independent review must verify its tree is exactly 5226dfdd98d50e06328c523691c09bcf7f4408f1, inspect the two mechanical compositions (current metadata commit.py + c793, and 9cf provider test + c793), the private-interpreter baseline command spelling, all 25 donor-map entries and the exact final-tree live evidence. Preserve 5292, original six P4 files, current public facade/076/metadata and every original assertion. FPS e50 and anchor repair remain separate owned work; reattempt the retained-source node only after those owners resolve its prerequisite.
