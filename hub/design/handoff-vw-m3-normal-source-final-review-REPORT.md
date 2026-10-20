# MINIMAL DEFECT — the actual normal PCM source join is absent

Independent review of `2019d7e69ceb9b10f18cc311e570d635b16c15d8`, also the current `tl/vw-m3-normal-pcm-source-carry` tip, against `ce2510034f3edebef7430dd018c566101ea298fb`. Review worktree: `/home/user/work/wt/vw-m3-normal-source-final-review`.

**The inactive prerequisite is acceptable to land as such. This is not approval of grant 07:58 source carry, activation, or M3/Gate 6.** One blocking finding: that new work is entirely absent. The producer accurately reports the blocker; this review found no additional defect requiring a change to the approved inactive unit.

Read PLAN, `design/audio-compile-contract.md`, the source-carry REPORT and central-qualification handoff, `agent-pcm-source-carry.md`, and the grant 07:58 worker brief. Reviewed every changed product/test file, not only the commit description or helper tests. No product or repository documentation changed.

## Exact prerequisite versus new work

The complete `ce251..2019d7e69` diff is **exactly** the ten-file `0a8c757723f0cee8ba128e453fce613d4c5c6262..ab935f77378ba5ea1df55ba775654f8bba233ebc` prerequisite. Every resulting file is byte-identical to `ab935`; the phase-test starting blob is identical as well. There is no additional changed path, imported old ancestry, or hidden uncommitted implementation. Total: 1,373 additions / 15 deletions; 319 product lines.

- Product: `astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py`; `remotion/{attempt-envelope-pcm,compiled-audio-source-clock,normal-audio-sources}.mjs`.
- Tests: `remotion/tests/{gapless-mp3-source-origin,long-audio-source,normal-audio-native-sources,normal-audio-sources}.test.mjs`; `tests/packs/rendering/{test_normal_audio_source_phase,test_normal_audio_sources}.py`.

**NEW grant 07:58 source join: zero lines.** Service, Timeline serializer, normal renderer caller, Root, package/lock/public12 archive, SDK, filmstrip/composed-frame, compiler, client and provider are unchanged from ce251. No Runtime/App/Composition changes were made by this review.

## Blocking finding and minimal next action

The required chain does not exist on this cohort:

| Stage | Actual source evidence |
| --- | --- |
| Admit unsliced compiled request and validate its deterministic transformed pair | `astrid/core/rendering/contracts.py:735` still exposes paths/window/materialized media, with no inherited compiled-pair association. Neither it nor `for_backend` carries such a binding. Searching rendering/execution/Timeline sources finds no `verified_source`, `inherited_source`, `source_for_timeline` or `mint_prepared_source`. This is a missing handoff on this base, not a claim that all existing render/media admission is absent. |
| Retain original compiled occurrences through host slicing | `astrid/core/rendering/service.py:1052` still loads the supplied JSON and calls `_window_timeline` on it; it neither serializes the unsliced render view first nor validates/retains the compiled originals. It returns only the replacement path/null window and materialized-timeline hash (`:1109`). Window-aware unlayered renders still return the original request (`:1072`). |
| Carry that association through `Timeline.for_render` | `astrid/core/timeline/banodoco_composer.py:255` only constructs the render view. `TimelineRenderView.to_json_data` (`:172`) copies serialized data, excludes source tracks and supplies a theme default. `_serialize_timeline` in `astrid/packs/rendering/shared/rendering_backend/__init__.py:53` returns that dict; no trusted originals cross this boundary. |
| Prepare on the normal export path | `astrid/packs/rendering/rendering/renderers/remotion/run.py:1104` constructs timeline/assets/theme/review props and writes them at `:1167`. It neither imports nor calls `prepare_normal_audio_sources`, nor supplies `compiledTransitions` to that helper. Repository Python call sites are the direct helper fixture only. |
| Same attempt/server lifetime through real consumption | The existing materializer/server ExitStack at `run.py:1067` remains, but no derived-audio attempt or cleanup callback is attached. The new helper documents caller ownership; its local success test manually removes the attempt. That proves a helper lifetime, not the normal export lifetime. With reused materializations, `AssetMaterializer.serving_root` can be the shared materialized root (`assets.py:305`), making explicit attempt cleanup necessary when the join is implemented. |

The helper's `original_clips` parameter is explicitly internal data, not admission. Its JS adapter checks asset/track/rate agreement but does not establish the unsliced/transformed-pair proof; the Python helper does not rederive the host transformation. Calling it on already-sliced props without retained originals would restart the fade, while treating the app stamp or clip-ID suffix as proof would violate the grant. These are activation prerequisites, not newly introduced failures on an active route.

**Minimal owner action:** supply or identify the approved existing admission handoff for this exact public12 cohort, including authorization of the deterministic host transform; then finish the allowed source-owner retention/validation and normal caller, with actual normal-path regressions. If that requires a new admission representation outside the grant, return that concrete contract/base decision to the orchestrator. The older design's additive DTO/sidecar suggestion is not authorization: grant 07:58 expressly prohibits inventing it. This review adds no protocol or substitute authority.

## Semantics, public12 policy and xfails

The prerequisite deep-copies disposable props; it does not write authored timelines/media/registry. Tests assert the full input and registry remain equal, retain clip volume 3 and track volume 0.5, and reject prepared-source reuse and altered managed bytes. `compiledAudioSourceClock` uses public rounded `computeMediaTrim` and sanitized child speed, without interpreting occurrence metadata as a clock.

`attempt-envelope-pcm.mjs:102` calls the pinned public12 `applyAudioEnvelope` once on complete native-rate/channel source PCM, then public `audioEnvelopeWav`. Constant gain is not baked into those arrays. The exact archive's `dist/index.js:133–149` applies track mute and scalar track × clip volume downstream; its non-Player envelope path at `:117` requires the matching prepared tuple. Full-source WAV equality, unequal stereo channels, rational trim/rate, recursive phase translation, distinct asset binding, gapless MP3, >64 MiB, amplification beyond unity, and failure cleanup passed locally. This is not bounded-RAM streaming and is not claimed to be.

No App authority, new DTO/endpoint/wire change, compiler/second writer, activation flag, fallback policy or official10 activation claim was introduced. Normal routes/cache/retry/cancel/mute/amplify and opaque-field behavior have no new executable caller and remain byte-identical to ce251. This is source-level preservation, not new end-to-end retry/cancel or audibility qualification. Direct visual-video audio must continue through its existing video consumer; preparing audio-track envelopes is not proof of an external full mix.

The four import-only strict xfails replaced by real window/layer native WAV tests belong entirely to the exact approved `ab935` prerequisite. Their stronger sample assertions are retained, with no skip, new expected failure, refusal expectation or tolerance widening. **No new xfail removal occurred.** Both active compiler fade requirements remain strict xfails, and this review independently obtained their expected red failures with `--runxfail`: missing `audio.render_source`, not an import/setup error. There is no normal-path green-after result; helper positives cannot justify removing those markers.

## Exact independent checks

All Python runs used this review worktree's code. Native JS tests used byte-verified copies of this tree's helpers/tests and its exact 77-file public12 archive, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. Private `node_modules`, `@banodoco` and `@remotion` scopes were real directories; only individual existing peers were linked for read-only use. No install ran.

For the commands below, these variables expand to exact absolute paths:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
P=$ORCH/design/handoff-vw-m3-normal-source-final-review-
PROJECT=$ORCH/workers/vw-m3-normal-source-final-review/project
PY=/home/user/work/venv-agent/bin/python
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
```

From `/home/user/work/wt/vw-m3-normal-source-final-review`:

```sh
python3 -B ${P}verify.py setup
# PASS: exact prerequisite only, public12/archive/test copies and peer versions.

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_REMOTION_PROJECT_DIR=$PROJECT $PY -B -m pytest -p no:cacheprovider -q tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py tests/core/rendering/test_service.py tests/editing_conformance/test_compile_contracts.py
# 103 passed, 2 existing xfailed in 28.93s; exit 0. ${P}pytest.log

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD $PY -B -m pytest -p no:cacheprovider -q tests/editing_conformance/test_compile_contracts.py --runxfail -k 'fade-in-needs-prepared-envelope-source or fade-out-needs-prepared-envelope-source'
# EXPECTED RED: 2 failed, 27 deselected in 0.11s; exit 1.
# Both fail at test_compile_contracts.py:78, audio.render_source absent.
# ${P}compiler-red.log

/home/user/work/venv-agent/bin/ruff check --no-cache astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py tests/packs/rendering/test_normal_audio_source_phase.py tests/packs/rendering/test_normal_audio_sources.py
# All checks passed; exit 0.
git diff --check ce2510034 HEAD
# PASS; exit 0.
```

From `$PROJECT`:

```sh
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/normal-audio-sources.test.mjs
# 8 passed / 0 failed / 0 skipped; exit 0. ${P}node-normal.log
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/gapless-mp3-source-origin.test.mjs
# 4 passed / 0 failed / 0 skipped; exit 0. ${P}node-mp3.log
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/normal-audio-native-sources.test.mjs
# 5 passed / 0 failed / 0 skipped; exit 0. ${P}node-native.log
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH TIMELINE_HEAVY=1 $NODE tests/long-audio-source.test.mjs
# 2 passed / 0 failed / 0 skipped; exit 0. ${P}node-long.log
```

An initial `env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE --test tests/normal-audio-sources.test.mjs tests/gapless-mp3-source-origin.test.mjs` also passed (2 file-level entries, exit 0; `${P}node.log`). The direct runs above expose all 12 case results; this is not 12 additional distinct tests. Total distinct native JS cases: **19 passed**.

After all processes completed, from the review worktree:

```sh
python3 -B ${P}verify.py after
# PASS: all source/archive checks and shared graph unchanged, 2056 entries.
python3 -B ${P}verify.py cleanup
# Removes only the private project; shared peer targets are not traversed.
git status --short
# Clean.
```

The flat `${P}verify.py`, `${P}shared-before.json`, `${P}shared-after.json` and logs accompany this report. The owned project was removed. No build output/temp file remains in the repository. This manifest proves no mutation of the graph these direct tests used; it does not clear the separately recorded graph hold for a central controller.

## Remaining actual gates — none claimed here

1. **Normal source-route gate:** real `RenderService → _segment_request → Timeline.for_render → normal run.py` whole/window/layer cases, admitted unsliced/transformed-pair tamper refusal, original exit/entry phase, explicit recursive envelope, overlapping distinct assets, rational fps, child rate and opaque fields. No helper-only substitute. Require intended normal-path red/green before changing either compiler xfail.
2. **Actual HTTP/WAV gate:** on a freshly frozen exact source/peer cohort, invoke that normal route and GET each prepared URL during consumption; compare its own complete native WAV bytes, rate/channels/sample count and phase; test swapped/forged/double-prepared inputs. Prove URLs/server live through consumption, then unavailable/closed with derived files removed after success, error, cancellation and retry, including reused materialized roots. No invented test authority. The current normal-HTTP handoff is correctly blocked.
3. **Actual normal MP4/A/V gate:** run the final encoder/export and read back delivered media; compare Player/export continuous fade audio and frames with the existing thresholds and a planted mismatch. Prove scalar gain once, mute/amplification, source trim/rate, start/end alignment and AAC priming/sample-count behavior, whole versus host window/layers, embedded video-audio preservation, default/no-envelope routes, cache/retry/cancel and error cleanup. Native PCM preparation alone proves none of these encoder or parity outcomes. Unknown-origin MP3/AAC characterization remains debt, not broad codec qualification.

No browser, listener/live socket, full suite, central request, MP4 export, network/install, push, or git mutation ran. Review task is complete; source-join implementation remains blocked with its owner. Recommended next step: land/name the exact prerequisite only, resolve the concrete admission/base handoff, then resume the bounded join and obtain the central gates above.
