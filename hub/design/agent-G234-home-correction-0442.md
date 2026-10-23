# FAIL qualification — G234/P4 home correction 0442

The requested source correction and ancestry audit are complete. Current-tree qualification is **FAIL** because exact approved V2 rejects the retained historical render control before task admission. This is a concrete V2/D12 blocker, not an assertion changed to expect refusal. Independent correction review is still required.

- Branch: `tl/agt-G234-home-correction-0442`.
- Authored source base SHA: `9729c07b764ba6cce1bb31686cb93d29fc72b14d`, base tree `81233b797eee27dedb8a39a3c2528fb5dff0765e`.
- Final authored working tree: `8f751a030024190625f1162d72552880203aa2a4`. Commit SHA is assigned by the exit harness; no commit was created by this worker. Resolve this branch after harness commit to obtain the authored commit SHA for review. Tree hash was computed without Git writes and the same algorithm was checked against HEAD's existing Git tree.
- Intended combined source: `5f0fb2edb72aae37ba86e3ffe28f5e79b63aa026` plus V2 `89c700aded947a4c498043e0f1a46b4ab3e0a873`.
- Public facade: exact `246f92507f15ac16c3bb559b7ce1576a608c86d8`; six P4 tests: exact `c4c6236838cf3758905cc195164f4021e8905e18`.
- G4 additions: `33fc387968c0b1bd4a78e828c34677d6f9cadd21` admission; `e045b37fa6ee00c402e00287fa683d12080c04ae` groups; three-file `f677e9bab7def6bcff8cd4faed55f29827b8af30` create_empty delta. The latter now has independent PASS from `agt-G4-create-empty-review-0442` (14 direct + 1 live).

## Correction and decisions

Restored only missing approved combined-source files/hunks: render assembly and wrappers, remote requester entry point, assembly retry checks, inverse physical-binding safeguards, narration commit path, element commit path, and their original tests. `publish.py` was patched at its missing narration hunks; its final blob is exact approved `ec1687a4a7f1123d8a17a2fcd95dfe21f4fec427`. Group forwarding and task admission are composed separately in their owned wrappers; no stale whole-file reset or Proof dependency graph was imported.

The imported 29-file/2417-add/430-delete ancestry was not silently qualified. It dropped pre-existing metadata validation, authored-meta opacity during media discovery, public exports, and original tests. Restored five core files and four test files exactly from pre-import `f894c3c9d`, and restored only the metadata media-discovery hunks in `commit.py`, preserving its exact V2 admission hook and approved inverse logic. This is a necessary deviation from stale parts of 5f0. The formerly 71-test current replacement command now includes the restored test and passes 72.

Four emitter cases relied on invalid namespaces (`org.example:literal.key` and `content_digest`). Migrated their fixtures to valid `org.example` namespaces, retaining punctuation in the opaque child key `literal:key.name`. Every existing assertion is retained at the corresponding nested location; one additional exact emitted-path assertion protects the literal token. No acceptance expectation was replaced by an error, and no tests were skipped, deleted or xfailed.

Deleted only the explicitly named accidental `design/agent-G3-R2-resume-0136.md` using apply_patch. Legitimate design documents and all G5-gated surfaces remain. Ruff's imported 2150 budget was restored to approved 2149; mypy improved from 1915 to 1914 with create_empty and was tightened through the normal `--write-baseline` tool.

The production callers are wired: public `timeline.open` exports `Timeline`, public `Timeline.undo` delegates publication/step selectors while preserving local numeric draft undo; CLI and sheet callers use the session; `RemoteTimelines.create_empty` uses shell creation followed by `TimelineSession` native initialization and guarded config patch; narration submits native commands; render publication forwards `group_id` and calls actual `RemoteTasks.create`. Exact request sealing/replay and complete v2 requests/replies are preserved by the approved session/emitter/provider blobs, including reads, steps, annotations and historical `rebased` envelopes.

## Qualification blocker

The service ran the unchanged real render assertion alongside the new live create_empty control: **1 passed, 1 failed**. Create_empty reaches the real commit door and exact replay. Render fails at `validation.py:_validate_params`, before `RemoteTasks.create`:

`candidate.shots['shot-1'].internal_timeline.clips['clip-1'].clipType: must identify an element`

The captured film actually has `clipType: "media"` and an unchanged historical `elementRef` containing `kind: "text"`, `binding_id`, and `anchor`. V2 treats any elementRef mapping as an element selection, takes its missing `id`, and rejects it. This conflicts with BOARD D12 / preservation of untouched legacy declarations. Exact V2 was explicitly required, so no validator change or fixture repair was substituted. Original live acceptance assertions remain intact. Prior independent 0416 admission PASS (1 real + 13 controls) is donor evidence only and does **not** qualify the final V2 join.

Recommended next step: an owned V2 correction recognizing legacy text-binding elementRef separately from selected-element refs, with the existing real render assertion retained, then independent review and the same two live nodes. Do not mark all G4/R5 or this final home qualified before that passes. P4 HTTP bodies remain Proof-owned and were not executed here.

## Exact verification

All direct commands ran in this assigned worktree, using shared dependencies read-only and private caches under `/tmp/w-86ab96f84a`. The joined command's integration node was split out to the central service, as required; no direct sockets, full suite, browser, native14, crash24 or Proof HTTP body was run.

### join-final

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m 'not integration' tests/sdk/test_timeline_open_commit_v2.py tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_inverse_binding.py tests/sdk/test_timeline_narration_commit.py tests/core/test_timeline_element_publication.py tests/sdk/test_timeline_render_publication.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py > /tmp/w-86ab96f84a/join-final.log 2>&1
```

```text
...................................................................      [100%]
283 passed, 1 deselected in 257.71s (0:04:17)
```

### parent184

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m 'not integration' tests/editing_conformance/test_recipe_parent_media.py tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_commit_runtime_parent_media.py tests/editing_conformance/test_commit_runtime_parent_media_swap.py tests/timeline/test_authoring_media.py > /tmp/w-86ab96f84a/parent184.log 2>&1
```

```text
........................................                                 [100%]
184 passed, 63 deselected in 54.46s
```

### current72

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_open_commit.py tests/sdk/test_timeline_sheet.py > /tmp/w-86ab96f84a/current72.log 2>&1
```

```text
........................................................................ [100%]
72 passed in 8.49s
```

### artifact41

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_vendor_lock.py tests/test_artifact_manifest.py tests/v10/test_release_reproducibility.py tests/stage1/test_vendored_workspace_client_parity_luna.py > /tmp/w-86ab96f84a/artifact41.log 2>&1
```

```text
.........................................                                [100%]
41 passed in 13.49s
```

### p4-sdk

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_cli_sheet_v2.py > /tmp/w-86ab96f84a/p4-sdk.log 2>&1
```

```text
...............                                                          [100%]
15 passed in 8.19s
```

### group-final

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m 'not integration' tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_render_publication.py tests/packs/video_editing/test_runtime_orchestration.py > /tmp/w-86ab96f84a/group-final.log 2>&1
```

```text
.........................                                                [100%]
25 passed, 1 deselected in 3.35s
```

### create14

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/v10/test_timelines_create.py > /tmp/w-86ab96f84a/create14.log 2>&1
```

```text
..............                                                           [100%]
14 passed in 1.53s
```

### controls-final

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m 'not integration' tests/sdk/test_p4_commit_v2.py tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_note_rerun.py tests/sdk/test_p4_cli_sheet_v2.py tests/v10/test_timelines_create.py tests/sdk/test_timeline_assembly.py tests/sdk/test_timeline_render_publication.py tests/packs/video_editing/test_runtime_orchestration.py tests/timeline/test_authoring_bundle.py tests/timeline/test_meta_validator.py tests/timeline/test_shot_composition_projection.py > /tmp/w-86ab96f84a/controls-final.log 2>&1
```

```text
...........................................                              [100%]
115 passed, 2 deselected in 30.36s
```

Additional direct controls (same environment and pytest options `-q -o addopts= -p no:cacheprovider`):

- `tests/editing_conformance/test_commit_timing_validation.py tests/editing_conformance/test_commit_v2_validation.py tests/sdk/test_p1_doc_patch_provider.py`: **73 passed**.
- `tests/editing_conformance/test_document_patch_emitter_engine.py`: **36 passed** after valid-namespace fixture migration.
- `tests/sdk/test_timeline_render_publication.py tests/sdk/test_timeline_narration_commit.py tests/core/test_timeline_element_publication.py -m 'not integration'`: **56 passed, 1 deselected**.
- `tests/sdk/test_timeline_checkout_history_boundaries.py::test_new_unsent_steps_stop_before_the_accepted_boundary tests/sdk/test_timeline_persistence.py::test_restart_a_fresh_process_sees_every_edit_and_the_undo_history`: **2 passed**.
- Public facade command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_open_commit_v2.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py`: **146 passed in 222.74s**.

Central live command:

```bash
$ORCH/bin/request-test agt-G234-home-correction-0442 native-script-current-integration --files 'tests/sdk/test_timeline_pristine_initialize_runtime.py::test_remote_create_empty_uses_live_commit_bootstrap_and_exact_replay tests/sdk/test_timeline_render_publication.py::test_requester_render_reaches_real_task_admission_after_commit'
$ORCH/bin/wait-test agt-G234-home-correction-0442-native-script-current-integration-1023045021-12459
```

Result: **1 failed, 1 passed; exit 1**. [Service log](../../tests/agt-G234-home-correction-0442-native-script-current-integration-1023045021-12459/log.txt).

The service's existing named command omitted Runtime from PYTHONPATH. A temporary test-only pyproject `pythonpath = ["/home/user/work/runtime"]` overlay was snapshotted; it was restored byte-for-byte afterward and is absent from the final diff. Live evidence tree `f5ea4d1a1f90a7d6595e4c3f0ec8bcfd2d42377c` differs from the final source tree only by that overlay. Earlier setup attempts recorded missing runtime_protocol (exit 4), a rejected option in the file-only service API, and a malformed temporary overlay (exit 4); none are reported as behavior passes.

Quality commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" RUFF_CACHE_DIR=/tmp/w-86ab96f84a/ruff-cache make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" MYPY_CACHE_DIR=/tmp/w-86ab96f84a/mypy-cache /tmp/astrid-u2-typecheck/bin/python -m scripts.reshape.compare_mypy_baseline --write-baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" MYPY_CACHE_DIR=/tmp/w-86ab96f84a/mypy-cache /tmp/astrid-u2-typecheck/bin/python -m scripts.reshape.compare_mypy_baseline
/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Results: Ruff **2149/2149**, mypy **1914/1914** (tightened through normal tool), vendor lock **PASS**, artifacts **current**, diff **PASS**. The initial bare-script mypy command lacked PYTHONPATH and failed import; the corrected normal command above passed. An artifact-script --help probe rewrote identical bytes; artifacts.json has no diff.

Scoped Ruff was run on session/emitter/assembly/inverse/publish/remote/render wrappers and changed G4 tests. Raw result: 123 inherited findings. Per-file code/message multisets match the appropriate exact donors (246f, 5f0, f677, 33fc/e045), with no additions. Scoped private mypy used `--follow-imports=silent` on the eight production files: 34 inherited findings in remote/publish/video wrapper; donor shadow-file and final path/message multisets match exactly after normalizing line references. Logs and executable comparison script: `/tmp/w-86ab96f84a/scoped-ruff-comparison.log`, `scoped-mypy-comparison-final.log`, `compare_scoped_mypy.py`. Raw probes are not claimed lint-clean; the ratchets and donor comparisons pass.

## Source preservation

`runtime.lock.json`, every generated `astrid_runtime_client` file, artifacts.json, canonical d106 edit schema and both f252 schema tests match approved 5f0 exactly. Lock source is `34eac0041b0891e9011966b39bcbd26053fde5bc` with exactly 15 mappings; lock SHA-256 `320d278366bc344aad35f3564845d9b62d9cc5f2e000a8a4cc6b6fea508d6cd2`. Canonical edit schema SHA-256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`. Schema test blobs are `d2225bf268ad33073b725eec9fdb9fb184ae4c50` and `14f0953375541c81be4e68b3b40c09319eed5bc0`.

Exact 5f0 restoration blobs include inverse `8d1ead5f132c2c551b142abd64c4e4f79e23d311`, element writer `30a0cbbb83a772715901fb74e9eed0bdcc104310`, emitter `23b7618c64daf34a0d34238d8ab02669a2bfab4d`, inverse regression `cd909f5d8156683cc6aa6bba1295d30c9abe83a6`, narration regression `d4197ab2c9bb0a6c518bb3747b8da95fe919b1b1`, assembly regression `719ef7e44a22ecc284d1d31ae4a7e881b8400cfe`.

Every non-5f0 path (36 total) is accounted for below. All other files equal approved 5f0; metadata restores, composited G4 additions, exact P4 additions and the tightened baseline are explicitly disclosed.

| Path | Final blob | Intended source / deviation |
| --- | --- | --- |
| `astrid/core/timeline/__init__.py` | `92a26c467c4c9975d8a969f6b037b0cae37353c7` | f894c3c9d exact |
| `astrid/core/timeline/authoring_bundle.py` | `d0d7dbd0aa961f1b2bd1442f2d4daa2ad7b53193` | f894c3c9d exact |
| `astrid/core/timeline/shot_composition.py` | `23105de991d1bde32b4ed8c98e0c036f560e0629` | f894c3c9d exact |
| `astrid/core/timeline/shot_composition_projection.py` | `04493587ea7de6b933774914df9ed4d4706ef860` | f894c3c9d exact |
| `astrid/core/timeline/validators/registry.py` | `c9ba3bcf86902ffa518f2a5e96881ff29d2d6168` | f894c3c9d exact |
| `astrid/packs/rendering/shared/runtime_stitch.py` | `cf16b09077c30f4efb18eaa58744a2f4cced7358` | 5f0 + 33fc supported create + e045 group forwarding |
| `astrid/packs/video_editing/shared/runtime_orchestration.py` | `1358b3a248d5d39f13d9add4dc35cff2f1e11501` | e045b37f exact |
| `astrid/sdk/remote.py` | `5c62de2c215f37ff2d3874bde2603bb0205df54a` | 5f0 + exact f677 create_empty delta + e045 group forwarding |
| `astrid/sdk/timeline/_commit_timing_validation.py` | `990d256c975b87ddeff381087187be6524d52d7c` | 89c700ade exact |
| `astrid/sdk/timeline/_timing_evaluators.py` | `29471c40804ab88f6cbddb92cb1774dbd2c5c6b6` | 89c700ade exact |
| `astrid/sdk/timeline/assembly.py` | `55e29d1245469d447821e39b3daa0f4d391d072f` | e045b37f exact |
| `astrid/sdk/timeline/commit.py` | `0d150f2523c4b9a3d5703af18dc7ffd951fe7dc4` | 5f0 + exact V2 eight-line admission hook + f894 metadata media-discovery restoration |
| `astrid/sdk/timeline/commit_session.py` | `b139373806031d0d6e50f5eb1d27d0b3973d2255` | 246f92507f exact |
| `astrid/sdk/timeline/compiler.py` | `7a2f3e2168342fbb5500e70cf0d8d5f578627025` | 89c700ade exact |
| `astrid/sdk/timeline/sync.py` | `5e7dfeec3b2a7f03849b58e5d09a5456b81a0a7b` | 246f92507f exact |
| `astrid/sdk/timeline/validation.py` | `fadda7ed794fe708434ccac8bdf94fa7acf60ecc` | 89c700ade exact |
| `scripts/reshape/baselines/mypy_astrid.json` | `276cba7275abd06a423e72208947c77e78ff7508` | normal tool tightens 1915 to 1914 |
| `tests/editing_conformance/test_commit_timing_validation.py` | `4819d4e2102d55a5fb3c03a9190889ca628ef184` | 89c700ade exact |
| `tests/editing_conformance/test_commit_v2_validation.py` | `d87c64715e03b8435ed3f90b4a275e080f51bced` | 89c700ade exact |
| `tests/editing_conformance/test_document_patch_emitter_engine.py` | `1632ba66d5fc28d073d99a3dcddb9493c7044b6c` | 5f0 with equally strong valid-namespace fixtures; all old assertions plus exact opaque path assertion |
| `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` | `05f7aa2bd862fc608ee17515d373c5f5b47c27eb` | c4c6236838 exact |
| `tests/editing_conformance/test_p4_ten_note_v2_runtime.py` | `5ee8dd5b863c164e0ea5f03257ac61849a425061` | c4c6236838 exact |
| `tests/sdk/test_p1_doc_patch_provider.py` | `f7d701d7af718099be5d1cd8ac97b8e1d3e8b7e2` | 89c700ade exact |
| `tests/sdk/test_p4_cli_sheet_v2.py` | `fd248182a0e1c120fa6440994da545c4e13219ad` | c4c6236838 exact |
| `tests/sdk/test_p4_commit_v2.py` | `85218e8e99a1c7602d2b7ee399f3847fac759186` | c4c6236838 exact |
| `tests/sdk/test_p4_note_rerun.py` | `80c15e2944b5660a18077aa38f84cf3b3ced09bb` | c4c6236838 exact |
| `tests/sdk/test_p4_ten_note_provider.py` | `1ed257c4604552793d2eaabfc117babe93c5b445` | c4c6236838 exact |
| `tests/sdk/test_timeline_commit_provider_document.py` | `1b1d0378e52e10e84549e6f651914dbba0a972eb` | f894c3c9d exact |
| `tests/sdk/test_timeline_open_commit_v2.py` | `f12ee8fc57f443f3aef43dece2627e0845d7bd04` | 246f92507f exact |
| `tests/sdk/test_timeline_pristine_initialize_runtime.py` | `0c2a112a200a496cd48c2b6a3e9ce75c7ad00207` | f677e9bab exact |
| `tests/sdk/test_timeline_render_publication.py` | `74c97482a69d2b8beda67a7c3cf935710ffa893b` | 33fc real admission + e045 group tests; create naming composed; original live assertions retained |
| `tests/sdk/test_timeline_sync.py` | `0fb59fc3f34d786a90ecc15496013ef24b8a7c05` | 246f92507f exact |
| `tests/timeline/test_authoring_bundle.py` | `b0f56b3844056197637831e375588d95ea4b3ded` | f894c3c9d exact |
| `tests/timeline/test_meta_validator.py` | `e311a61ecdb6fa7291760d4d7de88e3f8c577445` | f894c3c9d exact |
| `tests/timeline/test_shot_composition_projection.py` | `2cbe0a660c3bf8f36443a348758a4bf6bcc325a1` | f894c3c9d exact |
| `tests/v10/test_timelines_create.py` | `c23cd4e6b7d4979950c70cdab84b09cb0d8be8f0` | f677e9bab exact |

## Disposition of all unqualified imported paths

| Imported path f894..ccc | Disposition |
| --- | --- |
| `astrid/core/timeline/__init__.py` | restored f894 original behavior |
| `astrid/core/timeline/authoring_bundle.py` | restored f894 original behavior |
| `astrid/core/timeline/shot_composition.py` | restored f894 original behavior |
| `astrid/core/timeline/shot_composition_projection.py` | restored f894 original behavior |
| `astrid/core/timeline/validators/registry.py` | restored f894 original behavior |
| `astrid/packs/rendering/docs/scripts/timeline_document.py` | approved 5f0 exact |
| `astrid/packs/timeline/cli_native.py` | approved 5f0 exact |
| `astrid/sdk/_remote_timeline.py` | approved 5f0 exact |
| `astrid/sdk/timeline/__init__.py` | approved 5f0 exact |
| `astrid/sdk/timeline/api.py` | approved 5f0 exact |
| `astrid/sdk/timeline/commit.py` | 5f0 + exact V2 eight-line admission hook + f894 metadata media-discovery restoration |
| `astrid/sdk/timeline/commit_session.py` | 246f92507f exact |
| `astrid/sdk/timeline/emitter.py` | approved 5f0 exact |
| `astrid/sdk/timeline/store.py` | approved 5f0 exact |
| `astrid/sdk/timeline/sync.py` | 246f92507f exact |
| `astrid/sdk/timeline_sheet.py` | approved 5f0 exact |
| `design/agent-G3-R2-resume-0136.md` | removed accidental report |
| `scripts/reshape/baselines/ruff_astrid.json` | approved 5f0 exact |
| `tests/editing_conformance/test_document_patch_emitter_engine.py` | 5f0 with equally strong valid-namespace fixtures; all old assertions plus exact opaque path assertion |
| `tests/editing_conformance/test_document_patch_emitter_v2.py` | approved 5f0 exact |
| `tests/editing_conformance/test_p4_ten_note_v2_runtime.py` | c4c6236838 exact |
| `tests/sdk/test_timeline_commit_provider_document.py` | restored f894 original behavior |
| `tests/sdk/test_timeline_open_commit.py` | approved 5f0 exact |
| `tests/sdk/test_timeline_open_commit_v2.py` | 246f92507f exact |
| `tests/sdk/test_timeline_sync.py` | 246f92507f exact |
| `tests/timeline/test_authoring_bundle.py` | restored f894 original behavior |
| `tests/timeline/test_authoring_media.py` | approved 5f0 exact |
| `tests/timeline/test_meta_validator.py` | restored f894 original behavior |
| `tests/timeline/test_shot_composition_projection.py` | restored f894 original behavior |
