# CURRENT inactive normal PCM prerequisite

Task complete as an inactive prerequisite on Agent base `0a8c757723f0cee8ba128e453fce613d4c5c6262` (HEAD remains unchanged until harness commit). Eight new actual product/test files, 997 lines total; no tracked files modified. This is APPLIED in the assigned worktree, not another proposed helper. Harness owns the source commit; no commit, merge, checkout, ref operation or push was performed.

## Delivered

- `astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py`: expected `prepare_normal_audio_sources` import/interface. Exact Root registry comparison against the actual materializer; selected clip asset key resolves to its staged local path; streamed managed-digest recheck immediately before decode, including reused host files; unchanged original registry. Public-helper-derived full-source WAV is registered by the actual supplied `asset_server.local_url`. This base has no `register_attempt_file`, so none was invented.
- `remotion/normal-audio-sources.mjs`: private subprocess adapter. No authority/factory/provider/DTO/certificate. The source owner must already validate the actual transformed pair. Rejects caller `render_source`, including matching metadata with a forged/wrong WAV and double application. Existing asset key and constant gain/mute/trim/rate metadata remain downstream.
- `remotion/attempt-envelope-pcm.mjs` and `compiled-audio-source-clock.mjs`: reuse reviewed d2ad helper plus reviewed file-backed long-source and qualified MP3 deltas, with no replacement compiler/DSP/clock implementation. The only additional kernel differences from the final MP3 proposal are its package-version comment and checking preprepared input before the no-envelope early return. Unchanged public12 compile/apply/WAV/rounded trim/rate functions; no resampling, alignment, normalization, scalar gain bake, trimming, padding or decoded stdout cap.
- Direct main-suite tests: 14 passing Python cases and 14 passing native Node cases; two ordinary positive RED requirements for the missing source-owner transform join. No new xfail/skip and no existing test/marker edited.

The optional typed internal seam is:

```python
original_clips: Mapping[str, Mapping[str, Any]] | None = None
```

It maps the current disposable clip ID to the actual original compiled occurrence clip retained by the trusted source owner before slicing. It is ordinary internal data, never an authorization grant. The JS adapter compiles original E0 with the public helper; gets q0/q1 and child rate from the public helpers; translates every envelope keyframe recursively by `-(q1-q0)/r`; passes the derived existing `audio.envelope` through the unchanged kernel once; attaches that envelope beside render_source in copied Root props. Tests cover rounded-origin differences, rational fps, child speed, original fade-in AND fade-out, recursive multiply/minimum, and false caller slice-origin data. `app.astrid_slice_origin` is never read. Original props/authoring bytes are unchanged.

Omitting the seam is only qualified here for unsliced input. There is no claim that current core threads it, binds a transformed source pair, or that a manual module seam test proves source admission. No `run.py`/normal-route activation; no core/provider/Runtime/pin edits. No valid window/layer feature refusal was added.

The caller keeps an attempt TemporaryDirectory under materializer.serving_root alive with its existing ExitStack until consumption. Each Python call owns one subdirectory; both Node and Python remove partial batches on failure, including predecessor WAVs and registration failure. Success files survive until the caller cleans the attempt; unrelated attempt files and managed originals survive. Native local containment resolver tests establish this file lifetime; real HTTP/server-close evidence belongs to the separate fixture worker and has NOT run here.

## Exact verification

Commands ran from `/home/user/work/wt/vw-m3-normal-pcm-producer-current`, except native Node commands which ran from `$PROJECT` below. These are targeted tests only.

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER=$ORCH/workers/vw-m3-normal-pcm-producer-current
PROJECT=$WORKER/checks/remotion
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_REMOTION_PROJECT_DIR=$PROJECT /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q tests/packs/rendering/test_normal_audio_sources.py
# 14 passed, 2 ordinary failed in 2.64s. pytest-final.log.
# Both failures: actual slicer -> adapter lacks source-owner original transport;
# source sample 15000 is (0, -0), required (.25, -.125), for window and layer.

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q tests/editing_conformance/test_compile_contracts.py tests/packs/rendering/test_normal_audio_source_phase.py
# 29 passed, 2 EXISTING xfailed, 4 EXISTING strict-XPASS failures in .43s.
# pytest-existing-requirements.log. The four old tests only import the new
# callable, so now XPASS; their PCM/host names are not PCM/HTTP evidence.
# Preserved markers exactly, as instructed; only actual positives permit removal.

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q tests/core/rendering/test_service.py -k 'window_timeline or segment_request'
# 5 passed, 47 deselected in .29s. pytest-service.log.

# cwd=$PROJECT for the following three actual Node20.19.4 runs:
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/normal-audio-sources.test.mjs
# 8 passed, 0 failed/skipped, 1.507s. node-normal.log.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH TIMELINE_HEAVY=1 $NODE tests/long-audio-source.test.mjs
# 2 passed, 0 failed/skipped, 3.474s. node-long.log.
# 8,388,609 stereo frames / 48kHz / 67,108,872 decoded bytes, greater than
# former 64MiB limit; full WAV SHA256 equals independent public apply/WAV oracle.
# Observed process max RSS 201,260KiB; not a memory bound.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/gapless-mp3-source-origin.test.mjs
# 4 passed, 0 failed/skipped, 1.923s. node-mp3.log.

# cwd=assigned worktree:
/home/user/work/venv-agent/bin/ruff check astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py tests/packs/rendering/test_normal_audio_sources.py
# All checks passed.
python3 -B $WORKER/verify.py
# PASS: exact public12 SHA256, all 77 original archive files, shared actual
# React/DOM18.3.1 + Remotion/media/layout-utils509, Node20.19.4, byte equality
# between tested Node modules/tests and current source, JS syntax, no tracked edits.
git diff --check
# PASS. All eight changes are new source/test paths; no build output in worktree.
```

Tests use an ORCH-local extraction of the unchanged released public12 archive: SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 exact members. Shared existing Composition peers are read-only symlinks, no install. Python imports its actual current worktree module; the Node helper/test files in the ORCH runtime are byte-identical copies, verified after tests. Official Agent package remains 0.0.10; no claim these helpers can activate against that old dependency. Public12 adoption is separate owner work. Initial Python attempts failed because the repository conftest injects PYTHONPYCACHEPREFIX, which the real launch policy rejects; the test fixture removes that test-only override. Product launch validation remains unchanged. Initial native `node --test` reported all three files passing; each was subsequently executed directly to obtain the per-test counts above.

## Holds and next steps

No blocker to this bounded inactive prerequisite. Activation remains blocked by the existing source-owner join: preserve actual original compiled occurrence mapping before `_segment_request`, validate the actual derived path/digest pair through inherited source transport and serialization, then invoke this module at disposable Root props. Two new ordinary RED tests make the missing join explicit without new xfails/refusal expectations. Four existing import-only strict xfails now XPASS and must be replaced/fulfilled by real positives under their owner's instruction, not removed here.

Native codec debt remains explicit: metadata-free MP3 is 1105/1106 samples late; absent-start ADTS AAC is +1024; timestamped AAC retains the old refusal; M4A onset is preserved in the characterization but has 640 trailing native frames. Only the characterized source-backed gapless MP3 metadata relation is admitted by the narrow nonzero-start relaxation. No zero/absent-start safety claim or new codec refusal. File-backed decode removes the arbitrary decoded stdout cap, but public channel arrays and WAV still require duration-dependent memory (~2D), public RIFF has its existing size limit, and inherited 30-second subprocess budgets are not arbitrary-length qualification. Those existing owner seams remain before general activation.

Flat coordination: `design/handoff-vw-m3-normal-pcm-producer-current-interface.md` supplies the exact compatible callable, project/Node paths, lifecycle and missing original-input seam to `vw-m3-pcm-served-source-fixture`. Its real HTTP tests/controller are prepared separately. After harness commit, give that worker the exact source SHA; manager approves scope and centrally runs its whole-source HTTP fixture, then retains ordinary RED window/layer requirements until source owner joins. Verify two managed assets -> unequal exact WAV URLs/bytes, forged/swapped source controls, consumption lifetime, cleanup and authored immutability there.

No browser, renderer/export, live socket/HTTP listener, full suite, central service request, install or network run was performed. No trusted normal producer/Player-export parity or real server-lifetime positive is claimed. Earlier reports/proposals were read as data; frozen R4 refs were not checked out. PLAN decisions were not changed.

Flat handoff prefix (all absolute under ORCH design): `handoff-vw-m3-normal-pcm-producer-current-`. Product patch is a copy of the eight actual additions, not a separate proposed branch. `FILES.txt` carries exact source hashes; final source commit is emitted by the harness after exit. Logs and verify.py are copied alongside this report.
