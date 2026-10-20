Ready for the owner's bounded caller gate. The latest assigned Agent base is
`43d567f9d972386dc4cf585fbacc3ad9afc56bdd`; it already owns public 0.0.12,
the ten inactive PCM paths and the current M2 timing kernel. The approved
extent tip `5d0f1ddcad54936b36cedf1d89bf34f45fa612b5` is not an ancestor.
Only its exact seven-path delta from `df2739f903edac02bd36b4446deeea847524c040`
was applied as the prerequisite. No older complete tree, Root, archive,
provider, schema, client pin or M2 compiler was imported.

The caller is the approved frozen three-path caller-only patch, with its
executor AST, helper and 29-case test file unchanged. The additional fourth
caller path is the exact portable HTTP test from `e5a636d59`; its 22 cases
pass through the central named service. Its default is the imported Remotion
root, with an explicit environment override and no ORCH fallback.

The final source has exactly ten changed paths: seven prerequisite paths and
four caller paths overlapping at `run.py`. The extent paths are byte-equal to
5d0f1dd before the caller; all existing files outside these paths are unchanged.
`capture_remotion_frames` is AST-unchanged and the current final-props callback
is retained. MAIN quantization/serialization, scalar and track gain, mute,
boost, managed source errors, Three.js and current source/callback behavior
remain covered. There is no precision change, Three.js PCM activation, new
DTO/factory/projector/flag/stamp, or new xfail/test weakening. The only changed
existing M2 test expectations are the exact authorized extent migration,
which strengthens actual final Three.js payload/refusal coverage.

The six serialized Root clock goldens pass at 30/1 and 30000/1001 across full,
native-window and native-layer routes. They use actual M2 publication and
projection, MAIN's serialized `at=0.017`, projected trim/rate/gain, native
decode and the pinned public audio primitives; every prepared stereo WAV byte
is checked. Failure/cancellation/timeout, source digest/decode failure and
attempt-before-server cleanup cases pass. All six formerly inherited
prerequisite failures are absent from the final 266-case lane.

Handoff files all have absolute prefix
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-caller-current-land-unit-`:

- `prerequisite.patch`: exact seven-path approved extent delta, SHA-256
  `a37e0da0be03439df1b3ddbab40727c37c046e03b533b171839db74cc2dc3501`.
- `caller-only.patch`: ONLY the two caller source paths and two new test files,
  relative to extent plus current kernel tree
  `3e26c4a33f4799cfaa83237462c40dac5fa5cb81`. SHA-256
  `ebe571848275f7a7181a7e005cd3595ee8b6d254fcb114741e4f7f4710cf5397`.
  This is the owner landing unit after extent, not the entire branch.
- `TREE.tar.gz`: all 3,033 final source entries, with executable/symlink modes;
  SHA-256 `307a6bfc41528207cdde1aa429067a49ffe514e71073783554148d79627f5533`.
- `mainpair.patch`: complete binary diff against frozen `origin/main`
  `a411628f8fd6129f9c58c332019b56769d997384` (main tree
  `e0ca791bb8adbf11e25e0e97843aaf246a04f965`). SHA-256
  `becf4a4224bd417ce3ad299ff0326620b92d88d749e7e8bc0282cca9cdfc58c6`.
- `scope.patch`, `source.json`, `blobs.json`: complete worktree diff, exact
  source/base/main/tree data, and every file's mode/Git blob/SHA-256.
- `export.py`: independently computes Git tree hashes without writing Git
  objects/index/refs, verifies approved source boundaries, and replays both
  patch routes into private source directories.

Both replay routes produce byte-and-mode-equal final tree
**`303452fe7aa075d8451f641f577db7dcd0b74ca2`**, matching the central HTTP
service's tested snapshot: (1) current base plus prerequisite then caller;
(2) frozen main plus mainpair. The whole-main pair is delivery/reproduction
data, not permission to land unrelated current-integration changes wholesale.

Exact test commands and results follow. CWD is `$WT`; all commands exited 0
unless explicitly described as diagnostic. Environment variable definitions:

```sh
WT=/home/user/work/wt/vw-m3-pcm-caller-current-land-unit
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
P=$ORCH/design/handoff-vw-m3-pcm-caller-current-land-unit-
TASK=$ORCH/workers/vw-m3-pcm-caller-current-land-unit
PROJECT=$TASK/audio-project
PY=/home/user/work/venv-agent/bin/python
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node

python3 -B "${P}setup.py"
# Own real scopes; 77 exact public12 package members; existing peer leaf links.

env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WT" \
 ASTRID_NODE_EXECUTABLE="$NODE" ASTRID_REMOTION_PROJECT_DIR="$PROJECT" \
 ASTRID_TEST_NODE_MODULES="$PROJECT/node_modules" \
 ASTRID_COMPOSITION_TEST_NODE_MODULES="$PROJECT/node_modules" \
 PATH="$(dirname "$NODE"):$PATH" "$PY" -B -m pytest -q -o addopts= \
 -p no:cacheprovider --tb=short tests/packs/rendering/test_normal_audio_run.py \
 tests/packs/rendering/test_normal_audio_sources.py \
 tests/packs/rendering/test_normal_audio_source_phase.py \
 tests/packs/rendering/test_scene_source_carry.py \
 tests/packs/rendering/test_live_scene_composition.py \
 tests/packs/rendering/test_composition_package.py \
 tests/packs/rendering/test_remotion_native_window.py \
 tests/packs/rendering/test_native_layer_extent.py \
 tests/packs/rendering/test_remotion_capture_scene_props.py \
 tests/packs/rendering/test_remotion_layer_tail_compat.py -k 'not real_render'
# 266 passed, 1 deselected in 50.65s; targeted-final.log.
# The sole deselection is the prohibited real browser/render test.

env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WT" \
 ASTRID_NODE_EXECUTABLE="$NODE" ASTRID_TEST_NODE_MODULES="$WT/remotion/node_modules" \
 ASTRID_COMPOSITION_TEST_NODE_MODULES="$WT/remotion/node_modules" \
 PATH="$(dirname "$NODE"):$PATH" "$PY" -B -m pytest -q -o addopts= \
 -p no:cacheprovider --tb=short tests/packs/rendering/test_scene_host.py \
 tests/packs/rendering/test_scene_answers.py tests/packs/rendering/test_live_scene_boundary.py \
 tests/packs/rendering/test_capture_scene_labels.py
# 83 passed in 16.51s; scene-all.log.

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WT" "$PY" -B -m pytest -q \
 -o addopts= -p no:cacheprovider --tb=short tests/core/rendering/test_service.py \
 tests/core/rendering/test_storage.py tests/packs/rendering/test_managed_timeline_render.py \
 -k 'render_clock or declared_render_tail or window_timeline or segment_request'
# 12 passed, 106 unrelated deselected in 5.02s; service.log.

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WT" "$PY" -B -m pytest -q \
 -o addopts= -p no:cacheprovider --tb=short \
 tests/editing_conformance/test_compile_contracts.py \
 tests/timeline/test_shot_composition_projection.py \
 tests/core/timeline/test_shot_composition_projection_volume.py \
 tests/timeline/test_authoring_bundle.py::test_full_authored_field_edits_compile_without_normalizing_opaque_fields \
 tests/timeline/test_authoring_bundle.py::test_placement_edits_without_shared_projection_semantics_fail_before_publish \
 tests/timeline/test_authoring_bundle.py::test_publish_uses_one_compilation_and_returns_complete_mapping \
 tests/timeline/test_authoring_bundle.py::test_independent_unique_shot_reuses_untouched_revision_and_direct_edits_compile_identically \
 tests/core/timeline/test_source_role_tracks.py tests/timeline/test_timeline_characterization.py
# 81 passed, 2 EXISTING xfailed, 161 subtests passed in 5.24s; m2.log.

env -u NODE_OPTIONS -u NODE_TEST_CONTEXT ROOT_SOURCE_DIR="$WT/remotion/src" \
 NODE_PATH="$WT/remotion/node_modules" "$NODE" remotion/tests/root-metadata.test.cjs
# 7 passed; root.log. Actual Root callbacks, framework imports stubbed.
env -u NODE_OPTIONS -u NODE_PATH -u NODE_TEST_CONTEXT \
 "$NODE" remotion/tests/normal-audio-native-sources.test.mjs
# 5 passed; native-node.log, including >64 MiB full stereo and native codec cases.
env -u NODE_OPTIONS -u NODE_PATH -u NODE_TEST_CONTEXT \
 "$NODE" remotion/tests/normal-audio-sources.test.mjs
# 8 passed; source-node.log.

$ORCH/bin/request-test vw-m3-pcm-caller-current-land-unit integration-viewing-normal-pcm-http
$ORCH/bin/wait-test vw-m3-pcm-caller-current-land-unit-integration-viewing-normal-pcm-http-1020104047-30462
# 22 passed in 25.19s; central service exit 0, snapshot tree matches above.
# Exact service command:
# env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
# PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH \
# /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
# -p no:cacheprovider tests/packs/rendering/test_normal_audio_http.py

/home/user/work/venv-agent/bin/ruff check --no-cache \
 astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py \
 tests/packs/rendering/test_normal_audio_run.py tests/packs/rendering/test_normal_audio_http.py \
 tests/packs/rendering/test_native_layer_extent.py \
 tests/packs/rendering/test_remotion_layer_tail_compat.py \
 tests/packs/rendering/test_live_scene_composition.py
# All checks passed; lint.log.
git diff --check
python3 -B "${P}export.py"
# Both passed; source.json records unchanged runner diagnostic multiset
# (seven pre-existing diagnostics), exact caller/extent and successful replays.
```

An initial diagnostic used the same 266-case selection but mistakenly exported
`NODE_PATH=$PROJECT/node_modules`. The unchanged launch policy rejected it:
39 failed, 227 passed, 1 deselected (`targeted.log`). The corrected command
above removes NODE_PATH and passes without any source/test change. A separate
clean `test_normal_audio_run.py` invocation also passed all 29 cases in 14.85s.

The public12 archive remains SHA-256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
All 2,056 entries of the shared Composition graph are unchanged, recorded in
`shared-before.json` and `shared-after.json`. Shared venvs/runtimes/modules and
caches were read-only. Private replay trees, extracted project/dependency graph
and local dependency links were removed. No temporary/build output remains in
the worktree; the two small prerequisite source snapshots remain under the
assigned worker directory for export-driver reproduction.

No blocker remains for this caller unit. No full suite, browser, render,
install, network request, push, commit/merge/rebase/checkout, or local socket
test was run. Patch replay touched only disposable source files, with no Git
state mutation. HTTP is physical serving/cleanup component evidence with
admission/registry/encoder doubles. Root is callback/source behavior evidence,
not semantic TypeScript or rendered output. Actual matched Runtime admission,
MP4, Player/export parity, precision retirement, Three.js PCM ownership and
general tail ownership remain separate and unqualified here.

Next: owner lands/gates the exact extent prerequisite, then the four-path
caller-only patch against the recorded current kernel tree. Requalification
against a changed base and subsequent Runtime/render/parity work remain the
owner's separate gates. Commit message and DONE are supplied for the harness;
this worker did not land integration changes.
