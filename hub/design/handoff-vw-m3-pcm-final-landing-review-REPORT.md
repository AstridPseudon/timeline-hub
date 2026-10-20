# APPROVE — inactive prerequisite only

Reviewed producer `9fd669e481cf94ee641d9719f3ed7341910c2dcf` plus redfix `d65471fd0d34d1e87c26486e56a39b8c40289ad5` at the latter HEAD. Compared all nine changed product/test files against integration/common ancestor `0a8c757723f0cee8ba128e453fce613d4c5c6262`, and inspected current integration `86d7cf9b1fcaab7afb7a2e1ba66f57ef84935e31`. Integration's unrelated baseline fixes and two-line audio join-status addition are outside this branch; this is a landing review, not a recommendation to revert those changes. Read PLAN, audio contract, producer and flat redfix ORCHREPORTs. No required small fix for this bounded inactive landing. No repository files changed.

The implementation is sufficient and narrow: 319 new product lines across one Python adapter and three JS helpers, using the existing materializer/resolver, host slicer and public Composition functions. No parallel policy/compiler, new authority protocol, source grant or route activation. The sizeable remaining diff is direct native-source/PCM regression coverage.

- **Public12 envelope/clock/gain once:** `compileAudioEnvelope`, `applyAudioEnvelope`, `audioEnvelopeWav`, `computeMediaTrim` and sanitized child playback rate all come from the exact released public package. Original E0 keyframes, including recursive multiply/minimum, shift by `-(q1-q0)/r`; public rounded trim and rate remain downstream. Constant clip/track/occurrence gain is not baked into PCM. Public12 AudioTrack consumes the prepared URL and applies scalar gain/mute once; it does not reapply the envelope to prepared PCM. No trimming, normalization, alignment, padding or resampling added. Native stereo contents and lengths are checked, including amplification above unity.
- **Trusted originals and mapping:** the window entry retains full unsliced compiled clips before calling the existing `_window_timeline`; explicit `original_clips` remains a trusted internal alternative. Forged app slice metadata is unused. The JS seam checks asset, track and sanitized rate, but does not authenticate the caller's original map. Identity/closure validation must precede this internal call. App metadata must never become that authority.
- **Suffix and duplicate IDs:** appending the fixed window suffix is injective for valid unique string IDs; it never strips/interprets suffixes. Independent checks ran three simultaneous IDs `sound`, `sound_15_45`, `sound_15_45_15_45` with different fades/placements and retained each original's entire PCM in window and layer modes. Exact duplicate IDs WOULD overwrite the Python dictionary entry; this adapter alone is not a duplicate validator. Existing `validate_timeline` rejects duplicates (`validators/timeline.py:291`), independently exercised here. Normal `Timeline.load` validates by default, and managed render admission also calls that validator. Thus no required duplicate-ID fix for the documented validated-input contract; activation must preserve validation of the actual compiled input, including any IDs produced by projection. Raw unvalidated duplicate props are not qualified.
- **Managed bytes and cleanup:** complete Root registry equality binds clip asset keys to the materializer; the selected staged source's immutable managed SHA256 is streamed and checked again before Node decode. Distinct sources sharing envelope/clock retain distinct URLs and waveform contents. Wrong URLs, swapped/corrupt managed bytes, forged preparation and double application have direct controls. Failed Node batches remove predecessors and their own failing scratch; Python removes its whole private batch on decode/response/registration failure. Successful files survive until attempt-owner cleanup; unrelated files and original assets survive. This relies on the inherited immutable/isolated host input lifecycle; it is not proof against concurrent mutation between hash and decode.
- **Four strict xfails:** removal is justified for these local producer requirements. The old bodies only imported the callable. Their replacements compare every stereo float sample at the unchanged 1e-7 precision for both managed assets and both window/layer modes, assert the exact source-.5s pair, full source length, clock, scalar gain and unchanged inputs/registry. The redfix's retained missing-transport log shows all four replacements plus both ordinary slice requirements failing actual PCM comparisons before transport, not merely failing import. Current tests pass with real native decode. The renamed attempt-WAV test correctly makes no HTTP claim. No passing behaviour was replaced by refusal, and no new xfail/skip was introduced.

## Independent verification

Own ORCH fixture: freshly extracted public12 archive SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, all 77 members compared byte-for-byte. Six JS module/test copies equal this reviewed worktree. Existing Composition peer dependencies are read-only symlinks: React/DOM 18.3.1, Remotion/media/layout-utils 4.0.509. Node is 20.19.4. No installation or other-worker fixture mutation.

Exact commands (aliases below identify absolute paths):

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER=$ORCH/workers/vw-m3-pcm-final-landing-review
PROJECT=$WORKER/checks/remotion
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
# cwd=/home/user/work/wt/vw-m3-pcm-final-landing-review
python3 -B $WORKER/verify.py
# PASS, before and after tests: archive/source/peers/Node/syntax/clean-source qualification.

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_REMOTION_PROJECT_DIR=$PROJECT /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py tests/editing_conformance/test_compile_contracts.py tests/core/rendering/test_service.py -k 'not xx'
# 103 passed, 2 existing xfailed in 28.49s; exit 0. Four focused files, no deselections.

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_REMOTION_PROJECT_DIR=$PROJECT /home/user/work/venv-agent/bin/python -B -m pytest -c pyproject.toml -p no:cacheprovider -q $WORKER/review_checks.py
# 3 passed in 4.61s; exit 0. Additional review diagnostics, not new main-suite tests.

/home/user/work/venv-agent/bin/ruff check astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py
# All checks passed; exit 0.
git diff --check tl/integration...HEAD
# PASS; exit 0.
git diff --check
# PASS; exit 0. git status --porcelain is empty.

# cwd=$PROJECT for each native command:
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/normal-audio-sources.test.mjs
# 8 passed; 0 failed/skipped; exit 0, 1.672s.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/gapless-mp3-source-origin.test.mjs
# 4 passed; 0 failed/skipped; exit 0, 1.913s.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH TIMELINE_HEAVY=1 $NODE tests/long-audio-source.test.mjs
# 2 passed; 0 failed/skipped; exit 0, 3.229s.
```

Long-source result: 8,388,609 stereo frames, 48kHz, 67,108,872 decoded bytes; complete public WAV SHA256 `8592a32de5b2c4f46fd176ac2129edfcea2ab9489aa0b0e178c8049b2e4681a2`. Observed max RSS 200568KiB; this is not bounded-memory or arbitrary-duration qualification.

## Explicit holds and next steps

No ordinary failure/XPASS remains in the executed public12 focused repository lane. The two unchanged compiler-vector strict xfails still require an ACTIVE `audio.render_source` join. This is not an all-suite or official-dependency-environment green claim: Agent's official pin remains 0.0.10, and these tests explicitly selected qualified public12. That coordinated package adoption remains separate.

Normal rendering is still inactive: `_execute_remotion_locked` has no call to this producer. The real `_segment_request` file/digest transport and `Timeline.load(...).for_render()` serialization have not been joined to retained originals and the disposable prepared props. Already-sliced input without the original map still loses phase. Current focused positives deliberately exercise unsliced props plus the new window entry; they do not prove that existing already-sliced normal route. Admission/actual source-transformed pair validation, matching fps, original retention and attempt/server lifetime must be joined and qualified by the source owner.

**Served HTTP remains open.** The separate flat served-source fixture still has TWO ordinary window/layer positive requirements that slice before calling preparation without originals. They remain expected RED under that invocation, not fixed by this landing or hidden as xfails. I inspected them but did not run them: they require live sockets and central authorization. Neither whole-source HTTP GET nor 404/server-close/thread cleanup was exercised here. Local containment is not serving evidence, and the public envelope-key check does not authenticate swapped source bytes. Preserve the fixture's original PCM expectations when connecting its real source-owner caller.

No socket, browser, full suite, renderer/export, normal-task, Player/export PCM parity, gate6 or M3 run/claim. Known native codec debt remains: metadata-free MP3 onset +1105/1106, absent-start ADTS AAC +1024, M4A +640 trailing frames, and the inherited timestamped-source refusal. Public whole-source arrays/WAV, RIFF size and 30-second subprocess limits remain. No settled decision contradicted by this review.

Recommended next steps: land only this inactive prerequisite; source owner joins validated original/derived transport and disposable props, coordinates public12 adoption, then manager authorizes the separate central served-HTTP lane and later normal-route/parity qualification. Documentation owner should reconcile integration's stale join-status paragraph/four-xfail wording with this bounded local result while preserving all active/HTTP holds. No product or repo design changes made by this reviewer; no git commit/merge/rebase/checkout/push performed.
