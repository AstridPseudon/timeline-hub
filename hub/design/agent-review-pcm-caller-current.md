# Agent owner review: current PCM caller

**APPROVE the four-file caller-only landing unit.** No blocking source defect found. This approves the normal `TimelineComposition` caller and the bounded preparation/serving evidence below. It does not certify Runtime admission, an encoder, an MP4, Three.js PCM, Player/export parity, or an owner's film.

Reviewed remote `tl/vw-m3-pcm-caller-current-land-unit` at `b6ec4922abebe0672cb7115f073c1ab555870fa1`, against assigned current integration `6a59522421a8a5c0e93fca080aa2d1fd478952f1`. Required extent `86405964` is an ancestor of this base. Current service, Root and extent/compatibility tests already equal the submitted branch. The later observed integration `5430a9719542880ddf295ae0acd181270aac42ac` adds history work; it changes none of the rendering, serializer, authoring compiler/projector or Remotion paths inspected here. Execution evidence is specifically on `6a595224` plus the caller patch.

Landing artifact: `$ORCH/design/handoff-vw-m3-pcm-caller-current-land-unit-caller-only.patch`, SHA-256 `ebe571848275f7a7181a7e005cd3595ee8b6d254fcb114741e4f7f4710cf5397`. It applies with zero fuzz to current integration and produces four files byte-equal to the remote commit:

- `astrid/packs/rendering/rendering/renderers/remotion/run.py`
- `astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py`
- `tests/packs/rendering/test_normal_audio_run.py`
- `tests/packs/rendering/test_normal_audio_http.py`

Do not merge the entire old branch or apply its whole-main delivery patch. The ten-file branch delta includes the already-merged extent dependency; the current integration also has newer unrelated work absent from that branch.

## Source judgment

Read PLAN, AGENTS, the 11:02:07 Agent INBOX handoff, source-carry design, compile-idempotence finding, exact patch, producer/final-gate reports and branch diff. The old design assumes every layered render is time-sliced. The merged extent dependency changes that premise for window-aware renderers: `_segment_request` filters tracks while retaining original clip IDs and complete clocks, preserves the native frame window, and computes extent from the original render view. Thus this caller needs no reconstructed originals, new sidecar or transport field. The existing legacy `supports_windows: false` slicer remains separate; this review does not activate normal PCM for that legacy domain.

The caller runs after `Timeline.load(...).for_render().to_json_data()` and effect staging, before final props serialization, inside the existing asset ExitStack. The input is the real serialized unsliced compiled render view, or its track-isolated equivalent. Source-role tracks are excluded by the existing render serializer. No authored `astrid_slice_origin` stamp or guessed/split clip ID is read as authority. A direct source probe uses a deliberately misleading stamp and an ID containing slice-like suffixes, and verifies retained identity, full `at/from/to/speed`, exact allowed tracks, excluded reference tracks, immutable authored bytes and original compiled equality.

The six existing new caller goldens exercise actual M2 publication and projection, then normal full/native-window/native-layer execution at 30/1 and 30000/1001. They retain serialized `at=0.017`, source `from=0.051`, `to=1.825977`, rate 1.5 and occurrence identity. Public `computeMediaTrim` gives q0=2 and q1=55 at both frame rates; the adapter's source origin is exactly `2/fps`, with public sanitized rate 1.5. Full prepared stereo WAV bytes match the public apply/envelope/WAV primitives. Occurrence gain 1.5, track gain 0.5, and the muted overlapping clip remain consumer props; gain/mute are not baked twice into PCM. These are preparation/props observations, not audible encoder output.

Managed source selection uses the existing materializer and its registry. Selected file bytes are rehashed before native decode. Native ffprobe/ffmpeg, public continuous envelope application and float WAV writing are real; the helper registers the resulting file through the existing invocation server. The caller's TemporaryDirectory is inside the serving root, registered after the server in the ExitStack, so prepared WAVs are removed before the server stops, including reused materialized roots. Consumer error, cancellation, timeout, preparation/decode failure, digest failure and retry cleanup are covered. No new DSP, serializer precision policy, package pin, DTO, projector or stamp was introduced. Capture/frame mode and Three.js do not call this preparation branch.

The arithmetic in the old design needs a small factual correction: `.502 - .5016 = .0004` seconds (0.4 ms), not 1.6 ms. Its underlying raw-versus-compiled-domain concern is valid. The approved native-clock retention avoids that time-slice mismatch; no serializer change was made.

## Tests and exact commands

All commands below exited 0 unless explicitly described as setup diagnostics. Logs and review drivers are under the absolute worker directory defined here. No full suite was requested or run.

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W=$ORCH/workers/agt-review-pcm-caller-current
S=$W/source
PY=/home/user/work/venv-agent/bin/python
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node

python3 -B "$W/prepare.py"
# Archives assigned HEAD; applies exact caller-only patch to private source.
# Private actual public12 package, own scope directories, read-only peer leaves.
cd "$S"
env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" \
 ASTRID_NODE_EXECUTABLE="$NODE" ASTRID_REMOTION_PROJECT_DIR="$S/remotion" \
 ASTRID_TEST_NODE_MODULES="$S/remotion/node_modules" \
 ASTRID_COMPOSITION_TEST_NODE_MODULES="$S/remotion/node_modules" \
 PATH="$(dirname "$NODE"):$PATH" "$PY" -B -m pytest -q -o addopts= \
 -p no:cacheprovider --tb=short \
 tests/packs/rendering/test_normal_audio_run.py \
 tests/packs/rendering/test_normal_audio_sources.py \
 tests/packs/rendering/test_normal_audio_source_phase.py \
 tests/packs/rendering/test_native_layer_extent.py \
 tests/packs/rendering/test_remotion_native_window.py \
 tests/packs/rendering/test_scene_source_carry.py
# 210 passed in 76.59s; notes/targeted.log. No deselections/skips/xfails.

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" "$PY" -B -m pytest -q \
 -o addopts= -p no:cacheprovider --tb=short "$W/test_source_review.py" \
 tests/core/rendering/test_service.py \
 -k 'compiled_original_pair or window_timeline or segment_request'
# 7 passed, 47 unrelated deselected in 7.42s; notes/source-review.log.

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" "$PY" -B -m pytest -q \
 -o addopts= -p no:cacheprovider --tb=short \
 tests/editing_conformance/test_compile_contracts.py \
 tests/timeline/test_shot_composition_projection.py \
 tests/core/timeline/test_shot_composition_projection_volume.py \
 tests/timeline/test_authoring_bundle.py::test_full_authored_field_edits_compile_without_normalizing_opaque_fields \
 tests/timeline/test_authoring_bundle.py::test_placement_edits_without_shared_projection_semantics_fail_before_publish \
 tests/timeline/test_authoring_bundle.py::test_publish_uses_one_compilation_and_returns_complete_mapping \
 tests/timeline/test_authoring_bundle.py::test_independent_unique_shot_reuses_untouched_revision_and_direct_edits_compile_identically \
 tests/core/timeline/test_source_role_tracks.py \
 tests/timeline/test_timeline_characterization.py
# 81 passed, 2 existing xfailed, 161 subtests passed in 4.55s; notes/m2.log.

/home/user/work/venv-agent/bin/ruff check --no-cache \
 astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py \
 tests/packs/rendering/test_normal_audio_run.py \
 tests/packs/rendering/test_normal_audio_http.py
# All checks passed.
```

The q0/q1 direct probe ran from `$S/remotion`, using `env -u NODE_OPTIONS -u NODE_PATH "$NODE" --input-type=module -` with this exact stdin:

```js
import assert from 'node:assert/strict';
import {computeMediaTrim, getSanitizedPlaybackRate} from '@banodoco/timeline-composition/evaluation';
import {compiledAudioSourceClock} from './compiled-audio-source-clock.mjs';
const clip = {id: 'occ-1:sound', at: 0.017, from: 0.051, to: 1.825977, speed: 1.5};
for (const fps of [30, 30000/1001]) {
  const trim = computeMediaTrim(clip, fps);
  const clock = compiledAudioSourceClock(clip, fps);
  assert.deepEqual(trim, {trimBefore: 2, trimAfter: 55});
  assert.equal(clock.source_from, 2/fps);
  assert.equal(clock.playback_rate, getSanitizedPlaybackRate(clip.speed));
  assert.equal(clock.playback_rate, 1.5);
  console.log(JSON.stringify({fps, q0: trim.trimBefore, q1: trim.trimAfter, ...clock}));
}
```

Both probes passed: source origins `0.06666666666666667` and `0.06673333333333334` respectively.

All socket tests ran through central service, using a temporary worktree symlink to `$W/test_central_http.py`; the link was removed after the service finished. The service requires relative selectors, so the first request with an absolute selector was rejected before any tests ran (`...-1020110835-26724`). The corrected request was:

```sh
$ORCH/bin/request-test agt-review-pcm-caller-current targeted --files test_pcm_owner_review.py
$ORCH/bin/wait-test agt-review-pcm-caller-current-targeted-1020110935-466
# pass, exit 0 in 46s; 1 wrapper passed in 43.65s.
```

The wrapper launches precisely this child command with `cwd=$S`, `PYTHONPATH=$S`, `PYTHONDONTWRITEBYTECODE=1`, `ASTRID_NODE_EXECUTABLE=$NODE`, `ASTRID_REMOTION_PROJECT_DIR=$S/remotion`, pinned Node prepended to PATH, and NODE_OPTIONS/NODE_PATH/PYTHONPYCACHEPREFIX removed:

```sh
$PY -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
 --basetemp=$W/http-temp tests/packs/rendering/test_normal_audio_http.py \
 $W/test_http_review.py
# 26 passed in 42.80s; notes/http.log.
```

That is the submitted HTTP file's 22 cases plus four independent owner-review cases: `asset={sound,other}` × `mode={window,layer}`. Each additional case runs whole and selected routes with the real service adaptation, managed materializer, native preparation and InvocationAssetServer; it GETs the prepared WAV while the server is alive, checks every stereo sample against the expected original fade, checks the source-.5-second sample and requires whole/selected WAV byte equality. The four original helper-phase tests remain unchanged and passed, but use a URL double; they are not relabelled as HTTP evidence. The supplemental four are real host-served WAV positives. The encoder, project admission/registry setup, profile/theme/effect setup and port selection are still doubled as explicitly documented in the submitted HTTP fixture. Thus this is physical component serving evidence, not an admitted Runtime/render journey.

Additional read-only checks: `git diff --check HEAD b6ec4922a` passed; required extent ancestry passed; all four patched caller files still matched remote after testing, and all 77 extracted public12 package members still matched the pinned archive. A setup diagnostic initially found the historical shared Composition node_modules absent; the private graph instead uses existing peer leaves from `/home/user/work/runtimes/agent-remotion-0012/node_modules`. No shared dependency, venv, runtime or tool cache was written, and no install ran.

## Weakening, limits and disposition

No product/test source was changed in the assigned worktree. No new skip/xfail or weaker expectation is in the caller patch. The seven-path prerequisite's old expectation migrations are already merged; they retain legacy slicing/null-window refusals and add actual Three.js final-payload checks. The two remaining strict compiler-vector xfails (`fade-in-needs-prepared-envelope-source`, `fade-out-needs-prepared-envelope-source`) are unchanged. Their reason text still describes a missing normal producer, while those vectors themselves inspect the projector before attempt-local preparation; this review does not claim those vectors are closed or change their expectations. The active normal caller has separate real preparation and HTTP positives above.

No full suite, browser, Runtime admission, actual Remotion encoder, MP4, matched App/Player parity, owner-film run, package/pin update, git mutation, push or integration edit was performed. The only repository temporary was the removed central-service test symlink. Assigned worktree is clean. Private source/dependency overlay and HTTP basetemp were removed; report, small review probes, preparation driver and logs remain under this worker's ORCH directory.

No blocker. Recommended next step: owner gates/lands only the exact four-path caller patch on the integrated extent/public12/kernel base. Keep Runtime admission, encoder/MP4/parity and owner-film gates separate. Later reconcile the existing compiler-vector reason/stage with attempt-local source ownership without weakening its behavior requirement.
