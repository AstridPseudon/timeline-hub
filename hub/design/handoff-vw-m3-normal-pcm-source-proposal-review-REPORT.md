# Normal PCM proposal independent review — complete, UNAPPLIED

Deliverables (only worktree changes):

- `design/normal-audio-source-owner-handoff.md`: ONE next step for Agent's normal-source/capture coordinator: compose trusted original -> segment inputs -> serializer -> Root props, preserving original phase and materialized asset/WAV identity. Do not apply the prior wiring by itself.
- `design/normal-audio-source-regressions.patch`: two new main-suite files, 202 test lines, UNAPPLIED. Actual slicer + proposed native decoder adapter regression for exact .5s cut/.5s fade, two overlapping stereo sources independently, window and layer filter; same-clock/envelope distinct-asset URL/bytes control; non-invertibility counterexample; unchanged public11 phase-translation proof at integer/rational fps and child speed.

Reviewed PLAN, this tree's audio contract, prior worker ORCHREPORT, and `git show tl/vw-m3-audio-normal-source-join-plan:design/{normal-audio-source-join.md,normal-audio-source-join.patch,normal-audio-source-wiring.patch}`. Source candidate `435357aec` and inactive kernels `d2ad2ff82` inspected. Worktree base `6b108a8ef5b8a658bae26de59b373342dec40c71`. No git history/ref mutation or push.

## Findings and concrete owner correction

Existing proposal's six pytest/four vitest tests pass but do not test slice phase or trusted served-WAV identity. The actual .5s slice restarts .5s fade: sound PCM at source .5 is (0,-0), original (.25,-.125). All four overlapping-source/window-layer requirement cases independently fail at PCM equality with `--runxfail`.

Original timeline is available before `RenderService._segment_request` slices it. Window-start metadata survives, original clip at/from/to do not. Two distinct original timelines produce exactly the same sliced timeline yet different original fade phase (passing counterexample). Original data must come through the existing Agent source owner, not be guessed from sliced props. Source candidate validates only the original path/digest pair; `_segment_request` replaces the path but retains that binding. Rechecking it in the adapter is insufficient. No transformed factory/API exists in that candidate, and none is invented here.

Smallest phase representation already exists: compile public E0 from the original *compiled occurrence* (after existing occurrence caps/gain), derive q0/q1 from actual public rounded trims, r from child speed, and translate every envelope keyframe recursively by `-(q1-q0)/r` into existing derived `audio.envelope` in disposable Root props. Original fade-out duration, curves and overlapping fade products survive. Four public11 tests prove this with original full-source PCM, including .05 trim / rate1.5 / 30000/1001fps; seven-decimal precision matches existing attempt-PCM tests, exact .5s and new Python comparisons use exact float bytes. Kernel/public helpers unchanged, no second fade compiler or sample alignment.

Root's original asset URL is `assets.assets[clip.asset].file`; no invented assetURL property. Preserve registry key -> managed digest/local_path -> decoded bytes -> prepared WAV -> existing server URL throughout the same trusted producer. Two distinct assets under the SAME envelope/clock generate distinct URLs and correct unequal stereo samples. Public encodedEnvelopeSource does not bind bytes/original URL: real host-served WAV testing remains required. Mock containment resolver and mocked media primitives do not qualify authority/export.

No settled decision changed. Offset 350 milliseconds and occurrence speed remain metadata; child rate only, occurrence gain already folded once into clip volume, track gain/mute/amplify downstream. Core/provider/source/pins are read-only. Keep public11 immutable and defer adoption to coordinated owner work. No valid window/layer refusal, kernel/tolerance/codec changes, lost-behavior test rewrite, bypass, fallback or new source grant.

## Exact verification

All commands ran from `/home/user/work/wt/vw-m3-normal-pcm-source-proposal-review`.

```sh
P=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-normal-pcm-source-proposal-review/checks
python3 -B "$P/setup.py"
# Extracts prior proposed additions and unchanged d2ad helpers into OWN scratch;
# symlinks existing readonly public11 peers, no install, no source admission.
sh "$P/cpu-guard.sh" env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$P" AUDIO_PROPOSAL_PROJECT="$P/proposal/remotion" /home/user/work/venv-agent/bin/python -m pytest -c pyproject.toml -p no:cacheprovider -q -p proposal_import "$P/proposal/tests/packs/rendering/test_normal_audio_sources.py" "$P/proposal/tests/packs/rendering/test_normal_audio_source_phase.py"
# 8 passed, 4 strict xfailed, 3.38s; pytest.log
sh "$P/cpu-guard.sh" env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$P" AUDIO_PROPOSAL_PROJECT="$P/proposal/remotion" /home/user/work/venv-agent/bin/python -m pytest -c pyproject.toml -p no:cacheprovider -q -p proposal_import --runxfail "$P/proposal/tests/packs/rendering/test_normal_audio_source_phase.py"
# EXPECTED RED: 4 failed at actual PCM assertion, 2 passed, 3.17s; pytest-red.log
sh "$P/cpu-guard.sh" /home/user/work/app/node_modules/.bin/vitest run --config "$P/vitest.config.mjs" --reporter=verbose
# 8 passed / 2 files, 3.25s; vitest.log
sh "$P/cpu-guard.sh" env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -p no:cacheprovider -q tests/core/rendering/test_service.py -k 'window_timeline or segment_request'
# 5 passed, 47 deselected, .33s; pytest-service.log
sh "$P/cpu-guard.sh" env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -p no:cacheprovider -q tests/editing_conformance/test_compile_contracts.py
# 27 passed, 4 EXISTING strict xfailed, .21s; pytest-contract.log
sh "$P/cpu-guard.sh" /home/user/work/venv-agent/bin/ruff check "$P/proposal/tests/packs/rendering/test_normal_audio_source_phase.py"
sh "$P/cpu-guard.sh" node --check "$P/proposal/remotion/tests/normal-audio-source-phase.test.mjs"
sh "$P/cpu-guard.sh" python3 -B "$P/verify.py"
git apply --check design/normal-audio-source-regressions.patch
git diff --check
```

Lint/syntax/patch/whitespace checks PASS. verify.py checks tested patch bytes, public11 archive SHA256 `dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601`, all 77 extraction files, unchanged d2ad kernels and empty tracked product diff. CPU batches check ORCH/QUIET.md and viewing/QUIET.md; no active marker at execution. Four NEW strict xfails preserve successful slice behavior as a positive requirement, not rejection; original markers/expectations untouched. No tests weakened or skipped.

## Status and next step

Bounded review COMPLETE; no worker blocker. Owner dependency: Agent source coordinator must implement the actual trusted transformed-pair transport and original clip mapping, then carry these positive sample expectations through the real normal producer/serializer and centrally test served WAV consumption, overlapping audio, forgery/swapped bytes/WAV, cleanup and authored immutability. Remove new markers only when restored; retain existing ENVELOPE_UNRENDERED requirements until genuine normal producer succeeds. Rebase wiring only onto that qualified flow.

Decoder-origin compatibility (prior MP3 false refusal, AAC +1024 debt), public11 coordinated adoption and real trusted producer/Player-export parity remain activation holds. No browser/export/full/network/socket/install/central test service was run. Prior 22/27 codec counts and 138 PASS/5 RED corpus reconciliation were read, not rerun. This handoff is not activation evidence. Scratch only in own worker directory; no build output/temp files in worktree.
