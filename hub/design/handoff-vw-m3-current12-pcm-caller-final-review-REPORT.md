**NARROW CALLER: APPROVE. No genuine new caller defect found; no patch proposed.**

**WHOLE PREREQUISITE / RELEASE GATE: separate, not approved by this review.** The completed, narrowly composed prerequisite subset is green locally. Owner acceptance/integration of those units, latest-tree historical-fixture provisioning and actual serving/render/parity/adoption qualification remain separate. The six original prerequisite failures are not caller defects.

Source and scope

- Reviewed source: `b24a2acf565a3ab3ce23b35c6ea0a5196c6decd6`, based on `c456b3281497653cecf44f61acd6fa30565d83c8`. Assigned worktree remained byte-clean throughout. No repository patch, backup, report, build output or dependency link was added there.
- Approve ONLY the three-path `handoff-vw-m3-current12-pcm-caller-preserve-main-caller-only.patch`, SHA-256 `b6a6e45df1ed8be8ea6c1c623404e1c3de0cdcc3b2ade081f3fa2c391be57619`: `run.py`, `normal_audio.py`, and the new `test_normal_audio_run.py` in their existing rendering directories. The complete 20-path branch also contains prerequisites and is not approved wholesale here.
- Frozen starting prerequisites: public12/inactive kernel `082cf265b448712b031730d61cf3b9f63b813ab3` and native extent `626eed656edf2a6398703e9e5318343069e47019`. Their exact bytes and the caller-only delta were independently reconstructed and checked.
- The entire current M2 compiler/projector/provider directory, generated client and Runtime lock remain unchanged relative to the reviewed base. MAIN's serializer and for_render/duration implementation remain byte-identical; capture_remotion_frames remains AST-identical, and the current final-props callback invocation is retained. Three.js source remains unchanged. This is preservation at the reviewed source, not qualification of a later integration tuple.
- No feature flag, trust stamp, source factory, new projector/DTO, per-clip clock repair, DSP copy or new xfail was introduced. Scalar clip/track gain and mute remain in the consumer props; only the continuous envelope is baked.

Paired prerequisite composition

The original before/after-caller neighbor runs BOTH produced **6 failed, 69 passed, 1 deselected**. Failure node lists match exactly: two old sliced-service-input expectations, two old null-window expectations, the old null-window rejection expectation, and the old public0.0.10 package expectation. All source-carry nodes passed. See `-inherited-six.json` and `-original-{baseline,caller}-neighbors.log`.

After completion, I staged only the eight approved fixture paths from owner source `5f6c81309d96e7cd7abc2f22b32a377621c29092`, following the completed consumer unit and its final review. I did not apply that owner commit wholesale: it deletes ten PCM kernel paths and includes unrelated presenter fixtures. The exact eight selected hashes are in `-fixtures.json`.

I then staged the completed extent unit's seven paths from its exit-0/DONE, hash-sealed final patch. Its base is `df2739f903edac02bd36b4446deeea847524c040`; patch SHA-256 is `ae4695c47b3a2ee2a92da76cff774a7ec2ae9f1ebb134ac835580e58dd1ca77c`. The harness had not yet frozen a new commit when staged, so the immutable final patch plus all seven final file hashes identify the exact input. Every affected pre-unit path was checked against the reviewed caller's older base: no intervening unowned change was imported.

The ORIGINAL caller patch applied verbatim with zero fuzz (one hunk had a 12-line positional offset). Its helper and test remain byte-identical; its complete executor body remains AST-identical. A reverse dry-run also passed. The final private candidate differs from the reviewed caller tree only in eight approved fixture files and four extent/tail files. See `-stage-extent.py`, `-stage-extent.log`, `-extent-stage.json`, and `-private-guard.json`.

**Final paired subset: 232 passed without caller; 261 passed with caller; each 1 deselected, no failures/errors/new xfails.** The only deselection is the prohibited real browser/render case. The additional 29 cases are the exact new caller tests. Both private trees use the identical completed fixture and extent inputs.

What the positive tests actually establish

The six full/native-window/native-layer cases at 30/1 and 30000/1001 use the real M2 compiler once, the real canonical projector once, the actual service adapter and normal executor. They assert final MAIN-serialized `at=0.017`, start frame 1, projected trim/rate/duration/gain, overlapping mute and track gain. Real native decoding and public12 primitives produce and independently verify every byte of each full 90,000-frame stereo float WAV. Source origin is exactly `2/fps`, playback rate 1.5, scalar gain remains unbaked, muted PCM stays nonzero with zero consumer volume, false app slice metadata supplies no authority, and original inputs remain unchanged.

Failure, cancellation, timeout, malformed-envelope, integrity, decode and cleanup cases exercise the existing asset lifetime. Preparation is bounded to normal TimelineComposition video; selected PNG capture and the existing Three.js source path are preserved. Actual public12 native tests also exercise gapless MP3, rational trim/rate, wrong-origin controls, unknown-origin debt and full stereo sources beyond 64 MiB. No sample alignment or clock adjustment is used.

The normal tests double admission/registry generation/port choice, URL serving and video consumption. They prove the component handoff and lifetime, not HTTP transport, video output, actual Runtime admission or Player/export parity. Root tests transpile the actual component with framework/package imports stubbed; they are not semantic TypeScript or rendered-output qualification.

Exact commands and results

All paths below are absolute through these variables. Main suite tests ran directly; no full/browser/socket suite was requested.

```sh
WT=/home/user/work/wt/vw-m3-current12-pcm-caller-final-review
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
TASK=$ORCH/workers/vw-m3-current12-pcm-caller-final-review
P=$ORCH/design/handoff-vw-m3-current12-pcm-caller-final-review-
PROJECT=$TASK/audio-project
PY=/home/user/work/venv-agent/bin/python
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node

cd "$WT"
python3 -B "${P}setup.py"
# exit 0; own real scopes and read-only individual peer leaves; exact 77-member12 archive.

env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WT" \
 ASTRID_NODE_EXECUTABLE="$NODE" ASTRID_REMOTION_PROJECT_DIR="$PROJECT" \
 PATH="$(dirname "$NODE"):$PATH" "$PY" -B -m pytest -q -o addopts= \
 -p no:cacheprovider --tb=short tests/packs/rendering/test_normal_audio_run.py \
 tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py \
 tests/packs/rendering/test_remotion_native_window.py tests/packs/rendering/test_native_layer_extent.py \
 tests/packs/rendering/test_remotion_capture_scene_props.py
# 162 passed in 16.47s; exit 0; -initial-targeted.log.

python3 -B "${P}stage-extent.py"
python3 -B "${P}run-paired.py"
# Both exit 0. Exact argv and source cwd for each invocation: -paired-results.json.
# Baseline: 232 passed, 1 deselected in 40.62s; -final-baseline.log.
# Caller:   261 passed, 1 deselected in 47.18s; -final-candidate.log.
```

`run-paired.py` executes the following exact common pytest selectors on each private tree, with `-q -o addopts= -p no:cacheprovider --tb=short -k 'not real_render'`, PYTHONPATH set to that tree, the Node pin above, and both ASTRID_TEST_NODE_MODULES and ASTRID_COMPOSITION_TEST_NODE_MODULES set to `$PROJECT/node_modules`. Only the caller run additionally selects `tests/packs/rendering/test_normal_audio_run.py`:

```text
tests/packs/rendering/test_scene_source_carry.py
tests/packs/rendering/test_live_scene_composition.py
tests/packs/rendering/test_composition_package.py::test_locked_release_is_built_and_requires_no_separate_schema_or_theme
tests/packs/rendering/test_remotion_native_window.py
tests/packs/rendering/test_native_layer_extent.py
tests/packs/rendering/test_remotion_capture_scene_props.py
tests/packs/rendering/test_remotion_layer_tail_compat.py
tests/packs/rendering/test_normal_audio_sources.py
tests/packs/rendering/test_normal_audio_source_phase.py
```

Additional commands:

```sh
env -u NODE_OPTIONS -u NODE_PATH -u NODE_TEST_CONTEXT "$NODE" "$PROJECT/tests/normal-audio-native-sources.test.mjs"
# 5 passed, exit 0; -public12-node-native-direct.log (includes >64 MiB case).
env -u NODE_OPTIONS -u NODE_PATH -u NODE_TEST_CONTEXT "$NODE" "$PROJECT/tests/normal-audio-sources.test.mjs"
# 8 passed, exit 0; -public12-node-normal-direct.log.
# Earlier node --test on these two files also exited 0, reporting 2 file-level passes;
# the direct commands above supply the actual 5+8 case counts.

cd "$TASK/candidate"
env -u NODE_OPTIONS -u NODE_TEST_CONTEXT ROOT_SOURCE_DIR="$PWD/remotion/src" \
 NODE_PATH="$PROJECT/node_modules" "$NODE" remotion/tests/root-metadata.test.cjs
# 7 passed, exit 0; -root-final.log. Original Root also passed 7/7 (-root-original.log).
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" "$PY" -B -m pytest -q \
 -o addopts= -p no:cacheprovider --tb=short tests/core/rendering/test_service.py \
 -k 'window_timeline or segment_request'
# 5 passed, 47 deselected in 0.30s, exit 0; -service-final.log.

cd "$WT"
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WT" "$PY" -B -m pytest -q \
 -o addopts= -p no:cacheprovider --tb=short tests/editing_conformance/test_compile_contracts.py \
 tests/timeline/test_shot_composition_projection.py tests/core/timeline/test_shot_composition_projection_volume.py \
 tests/timeline/test_authoring_bundle.py::test_full_authored_field_edits_compile_without_normalizing_opaque_fields \
 tests/timeline/test_authoring_bundle.py::test_placement_edits_without_shared_projection_semantics_fail_before_publish \
 tests/timeline/test_authoring_bundle.py::test_publish_uses_one_compilation_and_returns_complete_mapping \
 tests/timeline/test_authoring_bundle.py::test_independent_unique_shot_reuses_untouched_revision_and_direct_edits_compile_identically \
 tests/core/timeline/test_source_role_tracks.py tests/timeline/test_timeline_characterization.py
# 81 passed, 2 existing xfailed, 161 subtests passed in 5.43s; exit 0; -current-m2.log.

/home/user/work/venv-agent/bin/ruff check --no-cache \
 astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py \
 tests/packs/rendering/test_normal_audio_run.py
# exit 0, all checks passed. Runner stdin Ruff JSON compared to frozen extent:
# same seven inherited code/message diagnostics, zero new (-lint.json).
git diff --check
python3 -B "${P}private-guard.py"
python3 -B "${P}guard.py"
# all exit 0; -private-guard.log, -guard.log and associated JSON.
```

The original paired neighbor commands used the first three common selectors above, the same Node/private peer environment and `-k 'not real_render'`, once in `$TASK/baseline` before the final prerequisite overlays and once in `$WT`. Exact failed node lists and counts are in `-inherited-six.json`. An independent direct `_composition_package_problem(Path(PROJECT))` call against the current source returned None; this is the package check, not full CLI/Runtime admission.

Portability, fixture decision and limits

The private dependency graph was outside the repository, with real node_modules/scopes and links only to existing individual Composition dependency leaves. All **77 installed public12 members** match the tracked archive, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; lock SHA-512 matches. React/ReactDOM are 18.3.1; Remotion/media/layout-utils are 4.0.509. All 2,056 entries of the shared Composition graph match before/after. No shared venv, dependency, cache, scope or runtime was modified. The final guards passed after the paired tests; disposable private source/dependency trees were then removed.

The reviewed staging HEAD already tracks the historical0.0.10 archive used explicitly by the unchanged tail test; both private trees retained those original bytes. The latest extent base has removed that archive and its own report requires private historical fixture provisioning. This review does not silently add it to latest integration or waive that replay requirement. The exact tail test and its stronger M2 migration were not weakened or edited here.

No full suite, make check, semantic Root typecheck, browser, socket, HTTP, actual video render, MP4, Runtime certificate, parity, adoption, installation, network or git mutation/push ran. The two existing M2 xfails remain unchanged. General tail/empty-gap limits, precision retirement and Three.js sliced audio qualification remain outside this caller verdict.

Next: owner gates the narrow eight-file fixture overlay and completed seven-file extent unit independently, then consumes the exact caller-only patch. Resolve the latest-tree historical test fixture explicitly before claiming a clean tracked-only prerequisite replay; obtain separately authorized actual serving/render/parity evidence afterward. No merge or remote action was requested. Commit message and DONE are supplied for the harness; there are no repository changes to commit.
