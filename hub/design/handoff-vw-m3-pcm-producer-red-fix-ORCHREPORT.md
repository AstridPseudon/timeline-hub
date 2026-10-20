# Inactive normal PCM producer: focused RED repair

Complete on base `9fd669e48` (`tl/vw-m3-normal-pcm-producer-current`). Only three tracked files changed: the inactive `normal_audio.py` and its two direct Python test files. No core, provider, compiler, schema, runtime, renderer route, dependency pin or native kernel changed. No rendering activated.

## Source change and boundary

`prepare_normal_audio_sources` now optionally accepts `window: FrameWindow` and `tracks: Sequence[str]`. Its caller supplies the actual **unsliced compiled Root props**. The inactive adapter snapshots the full original compiled occurrences, calls the existing `RenderService._window_timeline`, and carries the originals through its existing `original_clips` subprocess seam. The map uses the existing slicer's disposable ID convention (`id_startFrame_endFrame`); it does not infer identity from caller app metadata. The existing JS helper translates the public original envelope using the public rounded source clock. No alternate slicer, clock, compiler, DSP or sample alignment was added.

The existing explicit `original_clips` entry remains available to an owner that already performed a transform. Supplying that entry together with `window` is rejected as an ambiguous invocation; selecting tracks requires a window. Normal render paths do not call this helper. The adapter still requires its source owner to validate the actual compiled pair before calling it.

Important scope distinction: the two old tests sliced their input before invoking preparation and discarded the original. They now invoke this actual inactive adapter with the unsliced input plus window/layer arguments, retaining their exact positive PCM assertion. Already-sliced input passed without the original seam still lacks sufficient information; no claim that this call shape or the normal service/serialization path is fixed. Core is read-only in this task.

The four old strict xfails imported the callable and checked nothing else; this was why they XPASSed. Their bodies now prepare both whole and sliced native stereo WAVs for two distinct managed assets and both window/layer modes, compare every PCM sample at the existing 1e-7 precision, and assert the exact source-.5s pair, full-source length, public clock, unchanged scalar gain, registry and authored props. False authored slice metadata is overwritten only by the existing host slicer. The misleading `host_served_wav` test name becomes `attempt_wav`: the URL resolver checks local containment, not HTTP. Markers were removed only with these real positives and the RED/green proof below. No test was weakened, skipped or newly marked.

Two additional rational/integer-fps cases cover explicit `audio.envelope` clips for which core emits no `astrid_slice_origin`, child rate 1.5, IDs already containing window-like suffixes, and an excluded layer with an invalid asset. They compare full PCM against unsliced output and verify the public rounded trim clock. Thus retention cannot depend on the fade-only app stamp or accidentally decode another layer.

## RED before / green after

- Original tests on unchanged base: **6 failed, 16 passed**. Two actual-source failures produced `(0, -0)` instead of `(.25, -.125)`; four failures were strict XPASS. `red-before.log`.
- Real PCM assertions added, before the window interface: **6 failed, 16 passed** (`TypeError`, missing window seam). `red-real-positives.log`.
- Existing host slicing added to the inactive adapter but original transport deliberately not yet added: **6 ordinary failed, 16 passed**. Both original exact sample assertions fail; all four former import-only cases fail their full PCM comparison. This isolates the source-phase transport defect, rather than accepting import success as evidence. `red-missing-transport.log`.
- Original retention added: final focused run **51 passed, 2 existing xfailed**. The two untouched compiler-vector xfails still express the missing active compiled `render_source` join. No XPASS remains in these focused files.

All log names below have the flat `handoff-vw-m3-pcm-producer-red-fix-` prefix alongside this report. `source.patch` contains the exact full source/test diff.

## Exact commands and results

Run from `/home/user/work/wt/vw-m3-pcm-producer-red-fix`, unless otherwise stated. Environment aliases below are reporting shorthand only:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER=$ORCH/workers/vw-m3-pcm-producer-red-fix
PROJECT=$WORKER/checks/remotion
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node

env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_REMOTION_PROJECT_DIR=$PROJECT /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py tests/editing_conformance/test_compile_contracts.py
# Final: 51 passed, 2 existing xfailed in 5.06s, exit 0. pytest-green.log.
# The three RED runs used the same command/environment with only the two
# tests/packs/rendering files (without the editing-conformance file).

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -B -m pytest -p no:cacheprovider -q tests/core/rendering/test_service.py -k 'window_timeline or segment_request'
# 5 passed, 47 deselected in .28s, exit 0. pytest-service.log.

/home/user/work/venv-agent/bin/ruff check astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py tests/packs/rendering/test_normal_audio_sources.py tests/packs/rendering/test_normal_audio_source_phase.py
# All checks passed, exit 0. ruff.log.
git diff --check
# PASS, exit 0.

# Native targeted tests, cwd=$PROJECT:
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/normal-audio-sources.test.mjs
# 8 passed, 0 failed/skipped, 1.873s. node-normal.log.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH TIMELINE_HEAVY=1 $NODE tests/long-audio-source.test.mjs
# 2 passed, 0 failed/skipped, 3.516s. node-long.log.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH $NODE tests/gapless-mp3-source-origin.test.mjs
# 4 passed, 0 failed/skipped, 2.047s. node-mp3.log.
```

The long test independently matches the entire public WAV SHA256 `8592a32de5b2c4f46fd176ac2129edfcea2ab9489aa0b0e178c8049b2e4681a2`: 8,388,609 stereo frames at 48kHz, 67,108,872 decoded bytes (>64MiB), including edge impulses, no constant-gain baking or clipping. Observed max RSS 201,000KiB; not bounded-memory evidence.

Runtime setup reused the previous worker's immutable dependency extraction via a read-only-in-practice symlink from this worker's own checks directory; no writes into the other worker. The three native modules and three native tests copied into this worker's checks directory were verified byte-identical to this worktree. Public12 artifact SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` and all 77 package members were checked, as were actual React/DOM18.3.1, Remotion/media/layout-utils4.0.509, Node20.19.4, authorized changed-path census and diff whitespace. `verify.log`. No install or dependency modification.

## Remaining trust gaps / next step

No blocker to this bounded inactive prerequisite; no PLAN decision changed. The source-owning activation work must carry the actual unsliced compiled props into this entry (or retain the existing explicit original map), validate the actual source/transformed path+digest pair through its inherited admission and serialization, and preserve the attempt/server lifetime through consumption. The helper itself is not an authorization mechanism. Its private ID mapping is coupled to the existing core slicer naming; corresponding tests now cover suffix-like original IDs, and a future core ID change needs a coordinated adapter change.

No HTTP serving/server-close lifecycle, Player/export PCM parity, browser, socket, full suite or normal-render activation was run or claimed. The official Agent pin remains 0.0.10; these inactive tests use the exact released public12 package. The two compiler xfails remain until the actual active compiled-source join is qualified. Integrate this prerequisite, then have the source owner join it and centrally run the separately prepared real serving fixture when authorized.

Inherited codec/memory limits remain: metadata-free MP3 is late by 1105/1106 samples; absent-start ADTS AAC by 1024; timestamped AAC retains its pre-existing refusal; M4A preserves onset but has 640 trailing frames. No new codec refusal or per-clip fitting. Whole-source public arrays/WAV consume duration-dependent memory, RIFF size limits remain, and existing 30-second subprocess budgets are not arbitrary-duration qualification.

No git commit/merge/rebase/checkout/push performed. Harness owns the commit. No build output or temporary files left in the worktree.
