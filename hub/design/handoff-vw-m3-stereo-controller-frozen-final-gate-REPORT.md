# Stereo controller frozen final gate

Verdict: **NARROW REJECT**. The exact stereo source unit is sound offline, but the committed controller is not runnable under the required retained own Node/state paths, and the probe does not assert the native `ffprobe` channel count before decoding.

## Exact source reviewed

- App source commit: `bca5ed45cb741e0cb7ea47ed81baad914dfe983c`
- Parent: `2b388e769d9e153122e43b16b5d21e6e1ddf5b71`
- App tree: `982e68d884ee124f47fede300c478216e8546226`
- App change is exactly the three intended files: `tab-audio-capture.analysis.mjs`, `tab-audio-capture.analysis.test.mjs`, and `tab-audio-capture.probe.ts`.
- Composition `HEAD` is `5a4e9b72f`; prep commit `147d47aea` is not an ancestor and its report-only `.md`/`.patch` files are absent from `HEAD`.

The source has true L/R fixture tones (1760/1980 Hz), real `getSettings()` plus `getCapabilities()`, native recorder metadata, and no forced `-ac`, channel coercion, or downmix operation. The detector rejects swapped channels, one-channel mono, and a duplicated-mono signal represented as two channels. The prior shared-tone assertion remains unchanged.

## Blocking findings

1. `tab-audio-capture.controller.mjs` still hardcodes `NODE_EXECUTABLE = /tmp/vw-m3-agent-gate-node20.19.4/bin/node`; that path is absent. The admitted retained binary is instead `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node`, Node `v20.19.4`, SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.

   `setup-tab-audio-capture.sh` accepts `TAB_AUDIO_NODE_EXECUTABLE`, but that does not solve the controller identity check or its `discover()` child-process path: both still use the stale constant. No global symlink or identity bypass was used.

2. The controller also hardcodes the prior worker state root `vw-m3-tab-short-owned-tmp-fix`. An exact Playwright `--list` with caches/output under this worker's own state fails before discovery with `Probe state must stay inside its own worker folder`. Reusing the other worker's state was intentionally not attempted.

3. In `tab-audio-capture.probe.ts`, `ffprobe` identifies `audioStream.channels` before `readDecodedAudio`, but the source does not assert `channels === 2` until `assertStereoTones` is called after decode. Add an explicit native channel-count refusal immediately after the audio stream lookup and before `readDecodedAudio`; keep the detector and decoder free of `-ac`/downmix coercion.

## Passing evidence

From a clean `/tmp` archive of exact App commit `bca5ed45c`, using the retained own Node and the readonly private graph:

- `node --test ...analysis.test.mjs ...controller.test.mjs ...environment.test.mjs`: **3 modules passed**.
- Strict `tsc --noEmit` for the probe/config: **passed**.
- `node --check ...analysis.mjs`: **passed**.
- `bash -n setup-tab-audio-capture.sh`: **passed**.
- Offline duplicated-mono detector check: **rejected as expected**.
- Static no-forced-channel-coercion check: **passed**.
- App commit diff `--check`: **passed**.
- Own Node verification: `v20.19.4`, SHA-256 `43d6cf63...bb99490`.

The source-port handoff's prior `--list` result was not reproduced under this final gate's required own state root; the exact committed source reaches Playwright config loading and fails on the stale state-root binding before discovery. No browser, render, capture, grant, network, install, live socket, or full suite was run.

## Required correction and next step

In the App test/controller source, bind both launcher and controller to the retained own Node path (or an explicit run-scoped `TAB_AUDIO_NODE_EXECUTABLE` whose realpath and hash remain grant-bound), and bind controller/setup cache/output state to an explicit own `TAB_AUDIO_STATE_ROOT`. Preserve the existing `process.execPath`/grant hash checks and `discover()` child-process identity check. Add the pre-decode `channels === 2` refusal and a direct duplicated-mono unit case. Commit those controller/test changes, then generate a fresh source fingerprint and grant; only after that should the manager rerun pure preflight and consider a future central run.
