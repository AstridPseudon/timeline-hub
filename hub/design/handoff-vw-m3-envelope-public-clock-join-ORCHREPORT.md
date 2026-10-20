# Inactive envelope PCM / public clock join

Result: **22 targeted tests PASS (original 15 unchanged + 7 new)**. The public-clock blocker is removed for already-compiled clips. No normal-route activation or canonical eleven-vector qualification is claimed.

## Changes

Base Agent `4a75f68f3` (current M1 integration at dispatch). Four new files only, **371 added / 0 removed lines**: two helpers (83 lines total), two test files (288 lines). Every tracked M1 file is byte-preserved (`git diff --exit-code HEAD` = 0).

- Composed predecessor `remotion/attempt-envelope-pcm.mjs` (70 lines) and its 209-line, 15-case test file. The test file is byte-identical to the completed prep worker; the helper differs only in its obsolete package-10 clock comment.
- Added `remotion/compiled-audio-source-clock.mjs` (13 lines). `compiledAudioSourceClock(compiledClip, fps)` calls ONLY public `/evaluation` `computeMediaTrim` and `getSanitizedPlaybackRate`, converting returned source frames to seconds using the supplied resolved fps. It validates positive finite fps. No trim rounding, speed sanitization, occurrence offset/inheritance, status/label inference, or DSP policy is duplicated.
- The PCM kernel retains its required explicit `sourceClock` input. A future trusted caller passes `sourceClock: compiledAudioSourceClock(compiledClip, fps)`; the kernel does not infer compiler provenance or silently manufacture a missing clock.
- Seven new cases exercise defaults/rate sanitization and literal compiled inputs at fps 30 and 30000/1001: nonzero trim, 2x/0.5x rates, and an already-compiled occurrence-shaped result (`from=.475`, `to=1.475`, `speed=1.5`). Actual public TimelineComposition/AudioTrack executes with media/frame-context primitives mocked. It accepts the derived metadata and rejects unrounded origins, shifted origins and wrong rates. Clock comparisons are exact; no tolerance was added.

The kernel remains inactive. It decodes the full first audio stream at its original rate/channel count, applies public compile/apply/WAV semantics once, retains full source sample count, and emits fresh attempt-local float WAV bytes. Trim, speed, constant clip/track gain, mute, boost and mixing remain downstream. No core/provider/source port/prepared binding/server/Root/registry/pin/normal route files changed.

## Final package qualification

Composition merged source `ff0536bb5`, tree `cc5491fbd9289d63554a92061a99d7a1822b95b5`. Existing manager-owned central result `composition-full-1020040915-15314`: **exit 0, 65 PASS / 0 FAIL / 0 SKIP**, `npm test`. This worker requested no full suite.

Verified producer artifact and subsequently published ORCH artifact are byte-identical: **0.0.11, 58,344 bytes**, SHA256 `dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601`. All **77** archive files match the producer manifest and own extraction before and after tests. Manifest SHA256 `003c053d47e52104e35229ee20fd96fa220d61f4a9ee0c0c5e9623f1cdf6976f`. Tests resolve only advertised built package exports. A fresh native Node ESM process also imported the actual package by its root and `/evaluation` names and checked public trim/rate plus compile/apply/WAV exports.

Readonly App peers reused (React/ReactDOM 18.3.1, Remotion 4.0.509). Pre/post package path/version/hash identity matches; frozen 0.0.8/0.0.9/0.0.10 archive hashes match the saved preflight. Details: `environment-before.json`. No installs, package edits, peer mutation or dependency graph copy.

## Exact commands and results

Working directory `/home/user/work/wt/vw-m3-envelope-public-clock-join`. Below, `P=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-envelope-public-clock-join`.

Every CPU invocation used `sh "$P/cpu-guard.sh"`, which reads own REVIEW and checks both absolute ORCH/QUIET.md and ORCH/managers/viewing/QUIET.md before execution; a live marker writes fresh PAUSED_ACK and exits 75. Neither actual marker existed during these checks. No release was inferred.

```sh
sh "$P/cpu-guard.sh" env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$P/artifact-env.py" prepare
```

**Exit 0**: full result/source tree, artifact SHA/size, all77 manifest/extraction, old archives and readonly peers verified.

```sh
set -o pipefail
sh "$P/cpu-guard.sh" /home/user/work/app/node_modules/.bin/vitest run --config "$P/vitest.config.mjs" --reporter=verbose 2>&1 | tee "$P/tests.log"
```

**Exit 0; 22 PASS / 2 files / 3.42s**. One invocation only. Original 15 positive/control cases unchanged, including real FFprobe/FFmpeg decode and independent FFmpeg WAV readback, six curves, overlapping fades, rational fps, full source/channel impulses, float boost, downstream gains/mutes, malformed metadata and bounded failure controls.

```sh
sh "$P/cpu-guard.sh" node "$P/artifact/public-import-smoke.mjs"
sh "$P/cpu-guard.sh" env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$P/artifact-env.py" verify
```

Both **exit 0**. Postflight additionally checks published 0.0.11 bytes and published SHA sidecar against the tested exact artifact.

The following checks ran in one guarded `sh -c` batch (exact batch recorded in worker log):

```sh
node --check remotion/attempt-envelope-pcm.mjs
node --check remotion/compiled-audio-source-clock.mjs
node --check remotion/tests/attempt-envelope-pcm.test.mjs
node --check remotion/tests/compiled-audio-source-clock.test.mjs
git diff --exit-code HEAD
git diff --check
# Each of the four new files:
git diff --no-index --check /dev/null <new-file>
cmp remotion/tests/attempt-envelope-pcm.test.mjs /home/user/work/wt/vw-m3-attempt-envelope-pcm-prep/remotion/tests/attempt-envelope-pcm.test.mjs
```

Syntax, tracked-tree, whitespace and byte-identity checks **PASS**. No-index diff checks return 1 for new-file differences, with empty whitespace diagnostics, as expected. Temporary WAVs were removed by test teardown; external Vite cache removed after checks. No build output or temporary dependencies in the worktree.

## Decisions, remaining holds and next steps

Applied settled 03:17/03:20/03:25 decisions. Chose a separate tiny adapter to preserve the existing explicit-clock kernel contract and original tests. Positive finite resolved-fps validation prevents invalid frame-to-seconds conversion; all speed/trim behavior remains the public helpers' behavior.

**Canonical semantic join still pending:** the ONE Agent compiler's eleven-vector contract is not published. The literal already-compiled occurrence result is NOT evidence for canonical occurrence source_offset/speed inheritance. Agent must prove its MAIN-audible eleven vectors, publish the compile contract, and then rebase the goldens/adapters onto that output. No second compiler or occurrence policy was introduced here.

**Normal export still held:** Agent owns trusted source materialization/transformed prepared-binding admission. Then the existing attempt/asset-stage owner can call these helpers on verified compiled clips, serve the disposable output through its actual resolver, attach `audio.render_source`, and run the original strict ENVELOPE_UNRENDERED requirement. The repository still pins 0.0.8; these unreferenced helpers need the later coordinated App+Agent 0.0.11 adoption before use (the separately approved 0.0.10 adoption is unaffected).

**Decoder-origin compatibility debt:** the inherited helper currently refuses an explicitly nonzero first-stream start_time. This is NOT an accepted feature refusal for MAIN AAC/MP3/video and does NOT qualify priming/encoder-delay behavior. Only zero-origin stereo PCM WAV fixtures were tested. Preserve the original source origin/priming in a compatible trusted decoder join and qualify MAIN compressed/video sources before activation; do not trim, pad, resample, normalize or shift clocks to hide this debt.

No browser, actual export/render, sockets, managed source/capture certification, physical Player/export audio parity, full Agent suite, canonical vector run or normal-route closure was run/claimed. No tests were removed, weakened, skipped or marked xfail. No git mutation, branch/ref change, commit, push, integration write or other worker write. This bounded inactive task is complete; the named downstream joins remain held with their owners.
