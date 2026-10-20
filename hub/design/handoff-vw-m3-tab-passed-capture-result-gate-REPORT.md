# vw-m3-tab-passed-capture-result-gate

## Verdict

**PASS, narrowly:** the actual central run proves the standalone Chrome155 whole-tab capture backend capability. It does not prove Player/export-frame/audio parity or any App viewing path.

## Actual run

- Test: `composition-e2e-viewing-tab-short-owned-temp-capability-chrome155-1020133821-14480`
- Namespace: Composition only; scheduler snapshot tree `23a994070b8e25aba18703af1c6a0c840df1ab62`.
- Result: 1 test passed, total 7.4s, body 5.2s, exit 0.
- Controller log: `READY_GRANTED`, `RUN_STARTED`, and `POSTFLIGHT_OK`, all bound to source `2b388e769d9e153122e43b16b5d21e6e1ddf5b71` / tree `0124b608968c3baa371d6683ca3d0f2c953c235b`.
- The central command used the frozen App source by absolute path and the pinned App guard; the source had 5,835 tracked files and was clean.

## Retained media and offline audit

The retained artifact was not copied or rewritten:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-tab-short-owned-tmp-fix/capability-1340-output/tab-audio-capture.probe.ts-8ea9e-rome155-MediaRecorder-clock-native-codec-chrome155-tab-audio/whole-tab.webm`

- Size: 80,477 bytes.
- SHA-256: `f35483bab8f4992489ccd617ca4c2375599dc9337f1fbc7b37c2e3d0820eb6c8`.
- `ffprobe`: one VP8 video stream (1440x900, index 1, 5 packets, time base `1/1000`, PTS 42..3487, monotonic) and one Opus audio stream (index 0, 66 packets, time base `1/1000`, PTS 0..3900, monotonic).
- `ffmpeg` decoded audio: 48 kHz mono, 190,080 samples; DFT amplitudes 880 Hz `0.04818113852883244` and 1320 Hz `0.041814309247712324`.
- Decoded marker diagnostic: 62 frames; exact pre-event color 0 and event color 42. The probe itself marks this diagnostic-only and makes no event-phase claim.

The two tone measurements are from the decoded captured Opus, not the synthetic WAV fixture. No tone replacement, resampling, normalization, per-clip alignment, or synthetic result substitution occurred.

## Probe assertions reviewed

The actual probe installs the capture handler before a real Playwright locator click, requests `video: true`, `audio: true`, and `preferCurrentTab: true`, records `video/webm;codecs=vp8,opus`, serializes/awaits all recorder chunks, and writes `whole-tab.webm`. It then asserts the stream/track shape, native monotonic PTS, and both decoded tones with ffprobe/ffmpeg. The source's attached JSON/raw-RGB artifacts were not retained by the central result directory; the small companion metrics file is an explicitly labelled offline recomputation from the retained WebM.

## Identity and cleanup

- Source commit/tree: `2b388e769d9e153122e43b16b5d21e6e1ddf5b71` / `0124b608968c3baa371d6683ca3d0f2c953c235b`.
- Full tracked source: 5,835 files; hash `bd5866305fa997e556f92e6e8eb790513a52d6fe4fed17c614bebaaf217ff851`.
- Composition package: version 0.0.12, 77 files, hash `71b44e67e4eeffb0f904bb3a21e24d12ba06c4b2e41d43592a859aced3bb3139`.
- Full private graph: 32,382 files/symlinks, hash `4a54ed6f3300cba740b377e3c780f330996ead23147647f9c963ed4dd5bdd7a4`.
- Node: v20.19.4, executable SHA recorded in the matching grant/preflight.
- Chrome: 155.0.8059.84, executable/tree SHAs recorded in the matching grant/preflight.
- Short-temp calibration: old singleton path 175 bytes (`>108`), fresh direct `/tmp/timeline-tab-audio-*` path 85 bytes (`<108`). Static gate evidence verified UID/GID ownership, mode 0700, pre-existing-directory preservation, and ownership-safe cleanup on failure. The actual run's marker was created and consumed for this exact source; postflight was OK and its run-owned temp was cleaned.

## Historical control and boundary

The older `1020124802-7076` run remains a failed pre-recording Chrome startup caused by the long singleton socket path, with postflight OK. It is not an unsupported-backend or fallback result.

This PASS is standalone backend evidence only. It must not be represented as Player/export-frame/audio parity, Composition evaluator parity, or App end-to-end viewing evidence. No new run, grant, permission, browser, listener, network, install, or product change was made by this audit.

See [commands](handoff-vw-m3-tab-passed-capture-result-gate-commands.md), [findings](handoff-vw-m3-tab-passed-capture-result-gate-findings.md), and [offline metrics](handoff-vw-m3-tab-passed-capture-result-gate-metrics.json).
