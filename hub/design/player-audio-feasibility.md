# Early M1 Linux Player-audio capture feasibility

Date: 2026-10-19  
Worker: `vw-m1-player-audio`  
Result: **blocked for full Player-mix capture; native managed-audio partial path demonstrated**

## Scope

This was the bounded M1 experiment required by PLAN gate 6 and `design/viewing.md` §6. It used the current App Player and the existing `audio-reactive-colour-export.spec.ts` managed-object fixture. It did not claim M3 parity, compare two exports, decode the source WAV as a substitute for Player output, or add product code.

## Environment and exact commands

Read-only host probes:

```text
ffmpeg: /usr/bin/ffmpeg
ffprobe: /usr/bin/ffprobe
pactl: absent
pulseaudio: absent
pw-cli: absent
/dev/snd: absent
/run/user/*/pulse: absent
```

Playwright 1.60 expected a missing Chromium 1223 bundle. The image did contain Chromium 1194, so the focused browser commands explicitly selected that existing executable; no browser or system package was installed:

```bash
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
PLAYWRIGHT_TIMELINE_DEVICES=1 \
npm exec -- playwright test --config playwright.config.ts \
  --project=timeline-devices tests/e2e/timeline/audio-reactive-colour-export.spec.ts \
  --grep 'loads and plays the managed source_audio asset' --workers=1

PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
PLAYWRIGHT_TIMELINE_DEVICES=1 \
npm exec -- playwright test --config playwright.config.ts \
  --project=timeline-devices tests/e2e/timeline/player-audio-capture-probe.spec.ts \
  --workers=1
```

The probe was temporary and has been removed from the worker worktree after the run. It used a real managed Runtime object URL, then tried (a) a browser `MediaElementSource -> MediaStreamDestination -> MediaRecorder` tap and (b) `getDisplayMedia({audio:true})` tab capture. Recordings were decoded with the local `ffprobe`/`ffmpeg` commands embedded in the probe; no source-WAV decode was used for the capture result.

## Results

### Real Player and managed-object path: PASS

The existing real-Player test passed in 1 test / 36.1s. It fetched the content-addressed managed WAV through the local Runtime proxy, including a successful 206 range request, and the Player audio element became playing with advancing `currentTime` after the Play gesture.

### Native HTML audio partial tap: PASS, but not sufficient

The probe found one real Player `<audio>` element with the managed Runtime object URL, `paused: false` at tap setup, `volume: 1`, and `muted: false`. The destination contained one live audio track labeled `MediaStreamAudioDestinationNode`. The emitted WebM was nonempty (6,031 bytes); decoding that captured recording produced:

```text
decoded PCM: 84,672 bytes = 21,168 stereo samples
ffprobe stream: 48,000 Hz, 2 channels
RMS: 508.9484984031616
```

This proves a real, audible native-media element can be captured in-browser on this host. It does not prove the Player mix because it only taps media elements that are not already owned by another Web Audio graph.

### Browser/tab capture: FAIL

`navigator.mediaDevices.getDisplayMedia({video: true, audio: {suppressLocalAudioPlayback: false}})` was invoked from a user-gesture handler. The existing launch had no automatable tab-share source/chooser; after 5 seconds the negative result was:

```text
Timeout waiting for browser tab-share chooser (5s)
```

No tab-audio track was obtained. The Playwright config has no tab-audio or system-loopback recorder/launch setup.

### Amplified/Web Audio path: FAIL (conclusive inclusion blocker)

The probe first published the same canonical fixture with `audio_source.volume = 2`, which activates the current `AudioTrack.tsx` `useWebAudioApi` path. The Player still loaded the same managed object and played it. Attempting to attach a second `MediaElementSource` to that element failed with:

```text
InvalidStateError: Failed to execute 'createMediaElementSource' on 'AudioContext':
HTMLMediaElement already connected previously to a different MediaElementSourceNode.
```

This is the required negative: an in-browser tap that can capture the native element misses the active amplified/Web Audio backend. It cannot be used as the full Player-mix recorder.

### Video-with-audio: NOT PROVABLE from the current fixture

The managed audio-reactive fixture contains no video element and no checked-in playable managed video-with-audio asset. The only managed media used by this experiment is the WAV. The existing `demo-clip` fixture is a non-playable stub and was not substituted. Therefore video-with-audio inclusion was not silently claimed or replaced with synthetic media.

### Mute and 0.5-volume response: NOT CLAIMED

The native partial tap is nonempty and audible, but because it misses the active Web Audio path and there is no video-with-audio fixture, mute/0.5 response on that partial tap would not establish the required full Player behavior. No parity or gate-6 pass is claimed.

## Concrete blocker and recommended route

Full true Player-output capture is blocked by two independent missing prerequisites:

1. Provision an isolated Linux audio capture backend or browser tab-output capture route. The current host has no `/dev/snd`, PulseAudio, PipeWire CLI, or visible Pulse socket. This needs system/browser-launch permission outside this worker; do not install it silently.
2. Extend the test-only managed-object fixture with a real playable video-with-audio asset and pin it in the fake Runtime seed. The current audio-reactive fixture cannot test that backend.

The recommended M1 continuation is an isolated Chromium launch with a deterministic tab-audio/system-loopback recorder, then the existing real Player fixture plus a pinned managed video-with-audio fixture. Validate native audio, volume > 1/Web Audio, and video-with-audio separately before measuring the mix; then add explicit mute and 0.5-volume captures with decoded PCM sample counts/timing. If browser capture is preferred, it must instrument the Player's actual shared AudioContext destination before media mounts and still demonstrate all three backends; the `MediaElementSource` tap tested here does not satisfy that requirement.

Gate 6 remains open for Player audio. Renderer-independent save, frame rendering, and two-export audio checks are unrelated evidence and were not used to close this experiment.
