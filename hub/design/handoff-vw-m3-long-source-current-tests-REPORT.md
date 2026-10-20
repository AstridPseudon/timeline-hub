# Current long-source / gapless native tests

Complete, tests-only on Agent base `9fd669e481cf94ee641d9719f3ed7341910c2dcf`.
Only repository addition: `remotion/tests/normal-audio-native-sources.test.mjs`
(278 lines, five ordinary cases). No new xfail/skip or changed existing test.
Commit is left to harness. No integration/other worker changes or ref operations.

Read PLAN, audio contract, flat long-source and gapless reports/design/patches,
and current PCM producer handoff/scope note. Reconstructed frozen d2ad helper
with both UNAPPLIED patches in own disposable directory. Current decoder differs
ONLY in a package-version comment and moving the preprepared-source guard ahead
of the no-envelope early return. Clock and existing long test are byte-identical.
See adjacent `helper-comparison.diff`. **No missing product fix to port.** Kept
helper unchanged; no Python/source-phase/transport/normal wrapper/pin/core edits.
Coordination was written first in adjacent `COORDINATION.md`.

New coverage runs the existing normal adapter, rather than only its kernel:

- 8,388,609 frames, stereo 48kHz float32: 67,108,872 decoded bytes (64MiB+8),
  174.7626875 seconds. Independent bounded-write float source with unequal
  channels/tail impulses, rational fps 30000/1001, public rounded origin
  2/fps = .06673333333333334 and child rate 1.5. Full WAV SHA256 equals the
  independent public apply/WAV oracle:
  `8592a32de5b2c4f46fd176ac2129edfcea2ab9489aa0b0e178c8049b2e4681a2`.
  Full native FFmpeg readback hash/count also equal the oracle PCM; rate/channels,
  source/clip immutability, envelope metadata and decoded scratch cleanup checked.
  Scalar volume 7 stays downstream. Peak RSS 215488KiB, not a memory bound.
- Gapless MP3: independent PCM16 source 86400 stereo frames at 48kHz. Native
  MP3 retains all 86400 frames; 87552 packet samples -1105 skip -47 discard.
  Original onsets [9606,14405], MP3 [9606,14406], delta [0,1] (lossy waveform,
  not an alignment correction). Unity WAV retains EVERY native float byte and
  native readback; SHA256 d8a6de77461ad1040ae64f4d411beb12319a7a5c61f48bde8ed81e96de2d7ddf.
  Rational trim/1.5x full WAV SHA256
  2dce02df933ad094b75790971a9acb0d798549cf20e707df148af4960dd49696;
  adding the wrong 1105/48000 origin changes its bytes/hash. No fitting,
  resampling, trimming, padding, gain bake or global start_time subtraction.
- Timestamped MP3-in-MKA without first skip still fails the existing guard:
  87505 native frames, onset debt [1105,1106]. Attempt contents/unrelated file
  survive. This ports the existing negative control; it changes no behavior.
- Direct characterization retains unresolved metadata-free MP3 (87552 frames,
  debt [1105,1106]), ADTS (88064, debt [1024,1024]), M4A (87040, zero onset debt
  but 640 extra trailing frames), offset AAC (88064, debt [1024,1024]). These
  are native decoder facts, not new normal-producer refusal expectations.

## Exact targeted commands and results

Commands ran from own disposable `$PROJECT`. Each exited 0, directly executing
native node:test cases (no wrapper-only counts):

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
PROJECT=$ORCH/workers/vw-m3-long-source-current-tests/checks/remotion
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
cd "$PROJECT"
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH "$NODE" --expose-gc tests/normal-audio-native-sources.test.mjs
# 5 pass / 0 fail / 0 skipped, 5.914s; adjacent native.log.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH "$NODE" tests/normal-audio-sources.test.mjs
# 8 pass / 0 fail / 0 skipped, 1.649s; adjacent neighbor.log.
env -u NODE_OPTIONS -u NODE_PATH PATH=/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH TIMELINE_HEAVY=1 "$NODE" --expose-gc tests/long-audio-source.test.mjs
# 2 pass / 0 fail / 0 skipped, 3.492s; adjacent existing-long.log.
# Same 64MiB+8 full-source bytes/hash, nonfinite/empty cleanup controls;
# peak RSS 200948KiB in this separate process.
```

All 15 cases green. Both large runs sequential, one fixture/process at a time.
FFmpeg/FFprobe 6.1.1-3ubuntu5, CPU decode threads=1, Node20.19.4. No installs.
Own project used the released unchanged public12 archive SHA256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, all 77
members verified, with read-only shared React/DOM18.3.1 and Remotion/media/layout
4.0.509 dependency links. All six executed modules/tests verified byte-identical
to this worktree after tests; JS syntax, package members/peers and source hashes
in adjacent `verification.txt`. `git diff --check` passed; new-file
`git diff --no-index --check /dev/null remotion/tests/normal-audio-native-sources.test.mjs`
returned normal new-file status 1 with zero diagnostics. Existing tracked source
unchanged. All generated fixtures and own disposable checks directory removed.

## Limits / next steps

No blocker to this task; no decision deviation. Tests-only is deliberate because
both reviewed fixes are already present. Public pin stays 0.0.10: qualification
here uses public12 and does not claim old-pin activation works. No full/central
suite, Python/source-phase test run, socket/HTTP, browser, renderer, actual normal
route, Player/export parity, owner film or macOS run. Native MP3 bytes are not
claimed equal to its lossy pre-encode source, nor to browser decoding.

Zero/absent-start codec origin/count debt remains as above. File-backed stdout
removes the 64MiB cap but full arrays/public WAV remain duration-dependent;
public RIFF sizes and inherited 30s subprocess budgets are not arbitrary-length
qualification. Activation stays with source owner: actual transformed-pair
binding, original phase transport, served-WAV lifetime/admission and coordinated
public release adoption. Integrate this single disjoint test file alongside
red-fix worker's phase/transport fixes, then qualify those actual joins. No
additional behavior cut, origin tolerance or blanket codec refusal is justified.
