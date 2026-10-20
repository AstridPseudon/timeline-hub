# Stereo 1534 actual-result gate

## Verdict

**UNSUPPORTED STEREO AFTER ACTUAL CAPTURE.** Central terminal
`composition-e2e-viewing-tab-stereo-grantpath-chrome155-1020153403-18318`
ran once against the exact `6323b5bd6fdfc1bb680eba6f8a1a46f21acf6adb`
source with the fresh `1534` grant. It reached Chrome and produced a real
video+audio WebM, then refused the result at the native pre-decode channel
gate because `ffprobe` reported audio `channels=1`.

This is an unsupported-stereo diagnostic, not a capture-before-browser guard
failure. The old 1532 pre-browser failure remains a failure and was not
retried; its marker/grant were not reused. No retry, new grant, PulseAudio
startup, browser launch, render, network, install, socket, or test was run by
this worker.

## Actual result

- Artifact: 80,477-byte WebM, SHA-256
  `07fc9b7278eb449068c4b4ddb6cb1d8da05c5741c77e09698446fc0f2abede50`.
- Video: VP8, 1440x900, 5 nonempty packets, native time base `1/1000`,
  start PTS 45.
- Audio: Opus, 48 kHz, **1 channel / mono**, 66 nonempty packets, native time
  base `1/1000`, start PTS 0.
- Native audio/video PTS were nonempty and monotonic before the stereo refusal.
- The probe captured real `getSettings()` and `getCapabilities()` for one live
  video track and one live audio track, and the capability assertion passed.
  The exact settings/capabilities objects were not retained in the central
  failure attachment because the probe correctly aborts before its final
  outcome attachment; therefore this report does not invent their values.
- L/R identity and leakage were not measured: the required native
  `channels=2` gate refused before decode.

The compact artifact bundle and machine-readable metrics are in the companion
files. No raw giant capture or decoded dump was copied.

## Guard audit

The central log records `READY_GRANTED`, `RUN_STARTED`, the exact source SHA
and tree, and `POSTFLIGHT_OK`. The fresh preflight/grant records verify:

- full source: 5,835 tracked files, full hash
  `dc912e773a36c40271b13ab0abdeac6824cef394790d26658952e7c5763630fb`;
- private dependency graph: 32,382 files, hash
  `4a54ed6f3300cba740b377e3c780f330996ead23147647f9c963ed4dd5bdd7a4`;
- Composition package: 77 files, hash
  `71b44e67e4eeffb0f904bb3a21e24d12ba06c4b2e41d43592a859aced3bb3139`;
- all six pinned Remotion/Player peer hashes, Node `v20.19.4` and its
  admitted SHA, Chrome `155.0.8059.84` and its executable/full-tree hashes;
- profile `native-codec-chrome155-clean-install-public12`, `runMode=stereo`,
  one discovered test, fresh grant, and one-shot marker consumption;
- source/tree identity remained unchanged through postflight. The launcher
  exit trap removed the current run's short private temp directory; only older
  unrelated `/tmp/timeline-tab-audio-*` directories remained and were not
  touched.

The historical 80,477-byte mono artifact remains the separate
`f35483bab8f4992489ccd617ca4c2375599dc9337f1fbc7b37c2e3d0820eb6c8` artifact
and remains a mix/tone-presence plus native-PTS PASS only. It is not stereo
evidence and was not overwritten or relabelled.

## Boundary and next step

Do not claim Player/export parity, gain/phase parity, Gate 6 completion, or
stereo capability from this run. The minimal next backend diagnostic is to
retain the actual tab track settings/capabilities alongside the recorder's
native Opus channel metadata and determine whether Chrome155 tab capture
collapses the source before encoding. Do not force `-ac`, coerce channels,
change the `0.001` threshold, start PulseAudio, or make another attempt from
this audit.

## Evidence

- Central suite: `e2e-viewing-tab-stereo-grantpath-chrome155`; **failed exit 1**
  at the native channel guard, with `POSTFLIGHT_OK`.
- Artifact inspection command and output are recorded in the companion
  COMMAND file; no repository test suite was run by this worker.
