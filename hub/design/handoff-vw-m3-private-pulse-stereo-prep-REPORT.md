# Private Pulse stereo fallback preparation

Status: **READY FOR INDEPENDENT REVIEW; no actual capture was run.**

The approved fallback is packaged as a source-only handoff and patch:

- `handoff-vw-m3-private-pulse-stereo-prep.patch` adds the standalone probe,
  Chrome155 config, offline controller, and central launcher to the App's
  `tests/e2e/timeline/` area.
- `handoff-vw-m3-private-pulse-stereo-prep-manifest.json` records the source,
  toolchain, signal, lifecycle, and claim boundaries.

The probe reuses the existing `CONTROLLED_AUDIO` fixture and L/R detector from
the 6323 tab source, and the proven `player-audio-monitor.ts` private-Pulse
lifecycle from area history. It starts a per-run PulseAudio daemon only inside
an owned mode-0700 `/tmp/timeline-private-pulse-*` directory, creates a
48,000 Hz, two-channel null sink, and passes `PULSE_SERVER`, `PULSE_SINK`,
`PULSE_RUNTIME_PATH`, and `PULSE_STATE_PATH` only to that browser/ffmpeg child
environment. The monitor records `player.monitor` as native float PCM/WAV.
Every daemon/recorder path is stopped and reaped in `finally`; only the owned
runtime directory is removed.

The first observation is a Pulse snapshot before the first real Playwright
click/warm. The GDM path still requests one video+audio `MediaRecorder` mux.
If its native ffprobe stream reports two channels, the unchanged 1760 Hz-left /
1980 Hz-right detector is eligible for review and the mux is retained. If GDM
reports mono, the mux is explicitly unsupported and the result is only the
separate Pulse monitor channel-capability diagnostic. No A/V phase, Player or
export parity, source-clock, or Gate 6 claim is made.

The offline controller refuses root/system mode, checks that `pulseaudio`,
`pactl`, `ffmpeg`, and `ffprobe` are installed, and statically checks the
private sink/environment and cleanup controls. The existing tab controller
continues to own the full source, App package/77-file Composition graph,
whole private dependency graph, six peer hashes, Node20.19.4, Chrome155,
free-disk, flock, fresh marker, and pre/postflight identity checks. A new
grant and final source SHA are required; the failed 1534 and earlier 1532/mono
grants remain historical and are not reused.

## Host prerequisite check

Installed on this worker (read-only checks; no package installation):

```text
/usr/bin/pulseaudio  pulseaudio 16.1
/usr/bin/pactl       pactl 16.1
/usr/bin/ffmpeg      ffmpeg 6.1.1-3ubuntu5
/usr/bin/ffprobe     ffprobe 6.1.1-3ubuntu5
```

## Offline evidence

Passed:

```text
node --check ...private-pulse-stereo.controller.mjs
node --check ...private-pulse-stereo.probe.ts
node --check ...private-pulse-stereo.config.ts
bash -n ...setup-private-pulse-stereo.sh
git apply --check ...private-pulse-stereo-prep.patch
git diff --check
node --test <App>/tests/e2e/timeline/tab-audio-capture.analysis.test.mjs <App>/tests/e2e/timeline/tab-audio-capture.controller.test.mjs
```

The existing offline analysis/controller tests passed: 2 files, 2 passed, 0
failed. No daemon, browser, localhost server, live socket, network, install,
central test service, or full suite was run. The actual GDM/Pulse result is
therefore unverified pending independent review and a fresh grant.
