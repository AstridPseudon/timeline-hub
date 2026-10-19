# Early M1 Linux Player-audio capture feasibility

Date: 2026-10-19  
Worker: `vw-m1-player-mix`  
App base: `d52ef5341`  
Result: **private full-output recording works, including every current backend; mixed-output timing/continuity qualification FAILED. Gate 6 remains open.**

This replaces the earlier missing-audio-backend blocker. PulseAudio is now provisioned and the actual current App Player can be recorded. The remaining blocker is observed playback/capture synchronization and discontinuous mixed output, not an inability to obtain audio. Do not interpret the audible recordings, level controls, or planted gain detection as successful M3 Player/export parity.

## Reproduction and exact checks

Run from `/home/user/work/wt/vw-m1-player-mix`:

```bash
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  npm exec -- playwright test --config tests/e2e/timeline/player-audio.config.ts

npm exec -- eslint tests/e2e/timeline/player-audio*.ts tests/e2e/timeline/player-tab-capture.probe.ts --max-warnings 0

git diff --check
```

Final browser result: **2 failed**, exit 1. `captures real Player mixed output controls` ran nine recordings (3.9 minutes); `captures real Player amplified fade timing` ran one recording (26.9 seconds). Both preserve their timing/integrity failures. Soft assertions collect the remaining recordings without changing the failing verdict; empty output, wrong sample counts, missing backend setup and media errors remain hard failures. No tests were skipped, disabled, or made green by widening bounds. ESLint and `git diff --check` passed. New-file whitespace was also checked with `git diff --no-index --check /dev/null <file>` for each added TS file.

Only these focused browser experiments and touched-file checks ran. No full suite, broad browser suite, export, package migration, or product change was performed. The custom task explicitly permits these focused local browser runs.

The retained worker-local config inherits the normal isolated Vite/fake-Runtime servers and DNS blocking, sets their cwd explicitly, removes Chromium's default `--mute-audio`, and collects only `.probe.ts` files. Ordinary shared Playwright config and normal timeline collection are unchanged. The probes are opt-in; an ordinary timeline run will not collect these red feasibility tests.

Environment: Node 22.22.0; Playwright 1.60.0; Chromium 141.0.7390.37 from bundle 1194 (1223 absent); Remotion 4.0.509; ffmpeg/ffprobe 6.1.1; PulseAudio/pactl 16.1. No packages were installed by this worker.

## Capture backend and launch steps

The cheaper tab-capture attempt ran first against the real Player, with a user-gesture handler calling `getDisplayMedia({video:true, audio:true, preferCurrentTab:true})` and Chromium `--auto-accept-this-tab-capture`, `--enable-usermedia-screen-capturing`, `--allow-http-screen-capture`. It failed after 31.3 seconds with `locator.getAttribute: Target page, context or browser has been closed`; no audio track or recording was obtained. The retained reproduction selector is:

```bash
PLAYER_AUDIO_CAPTURE=tab \
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  npm exec -- playwright test --config tests/e2e/timeline/player-audio.config.ts
```

The original attempt used the same config command while that config selected the tab probe directly; the selector above reproduces it with the final config. Browser closure was observed; its underlying cause was not established. The native-element tap from the previous report was not reused as full-mix evidence.

The selected fallback is implemented in `tests/e2e/timeline/player-audio-monitor.ts`. It creates a mode-0700 `.player-pulse-*` directory under the worker cwd and passes the following environment **only to its daemon, Chromium, pactl and recorder**, never to shared servers or the shell's default audio:

```text
XDG_RUNTIME_DIR=<private directory>
PULSE_RUNTIME_PATH=<private directory>
PULSE_STATE_PATH=<private directory>
PULSE_SERVER=unix:<private directory>/native
PULSE_SINK=player
```

Exact daemon arguments (no system mode, default.pa, hardware detection or shared state):

```bash
pulseaudio -n --daemonize=no --use-pid-file=no --exit-idle-time=-1 --log-target=stderr \
  --load="module-native-protocol-unix socket=<private directory>/native auth-anonymous=1 auth-cookie-enabled=0" \
  --load="module-null-sink sink_name=player rate=48000 channels=2 channel_map=front-left,front-right"
```

Disabling cookie loading is necessary here: the first private protocol-module attempt failed while looking for the root user's default cookie. Authentication is disabled only on this private socket inside its 0700 directory. No shared/default sink was changed.

Exact recorder arguments, generated without a shell:

```bash
ffmpeg -hide_banner -y -f pulse -sample_rate 48000 -channels 2 \
  -i player.monitor -af 'volume=1,atrim=end_sample=288000' -c:a pcm_s16le <recording.wav>
```

The planted control changes only this live recorder's `volume=1` to `volume=0.5`, after normal browser mixing. It changes neither shared input nor the Player, and performs no offline mixing. Chromium has one actual Player page at a time. Browsers close before daemon teardown; recorders have a 15-second deadline and are killed in `finally`; the daemon and private runtime directory are removed in `finally`. Generated media input directories are also removed. No build output, recording, private runtime directory or temporary file remains in the worktree.

A preliminary wall-clock `-t 6` recording contained 287,255 frames and correctly failed the exact sample-count check. Sample-based `atrim` now terminates after 288,000 received frames without resampling or padding. Exact length alone does not hide source silence: the independent interior-gap and phase checks reject the observed bad mixes.

## Real media, Player and managed-object inclusion

`player-audio-fixture.ts` generates ordinary three-second playable inputs with ffmpeg: native 440 Hz stereo WAV, amplified 660 Hz stereo WAV, and a real moving 320x180/30 fps VP8 + 880 Hz Opus WebM. The deterministic tone has right amplitude 0.75 of left. The amplified clip has authored volume 2, exercising the existing `AudioTrack.tsx` Web Audio path. An initial H.264/AAC MP4 reached the object route but emitted browser `MediaError` and produced silence; it was rejected and replaced with the browser-playable WebM.

Bytes are ingested through the existing fake Runtime's project-object API and addressed by their actual SHA-256 digest. Fixture revisions are published with the existing guarded composition helper. Every final case observed managed-object **200 and 206** responses through the current App's normal Vite Runtime proxy. Trace inspection includes CORS-mode object requests without browser Authorization or Cookie headers; the existing server proxy supplies Runtime authorization. Native/amplified media use the current anonymous-media policy; decoded video uses the current managed-media fetch path. Hosted/cross-origin deployment was not tested.

The test mounts the actual editor and `@remotion/player`, clicks its real Play button, warms the same Player through a complete play, rewinds, and records another real gesture-driven play. Media begins at frame zero so decoder readiness can be checked before measurement. The harness reads the mounted PlayerRef through React's existing ref; it uses real `setVolume()`/`mute()` methods and adds no product debug API. Backend spies only observe existing media-source/buffer-source creation; they neither attach a new MediaElementSource nor reroute audio.

Native audio, volume-2 Web Audio, decoded-video audio, and supported native video fallback were exercised separately. The fallback test removes browser `VideoDecoder` support and verifies a real `<video>` during warm-up; the default decoded-video case verifies a decoded frame and active buffer sources. All three tones are then present together in the monitor recording. Source WAV decode, synthetic PCM mixing, exports and two-export comparisons were never used as capture substitutes.

All mixed/control/repeat recordings use the same immutable fake-Runtime head, `e2e-external-104-4`, with unchanged object bytes/config. Only Player controls or the live recorder gain vary.

## Final recorded measurements

Every recording decoded to **48,000 Hz, two-channel s16 PCM, exactly 288,000 stereo frames (six seconds)**. The table reports onset/offset in captured PCM seconds, Player wall-clock drift relative to its reported frame span, and left-channel interior RMS. These are measurements of Player output, not exported/source audio. Onsets use 20 ms energy windows; no per-source time shift or correlation alignment is applied.

| Case | Onset → offset | Player drift | Left RMS | Result |
|---|---:|---:|---:|---|
| Native 440 Hz | 0.40 → 3.42 | -6.1 ms | 0.088394 | Individual capture checks passed |
| Amplified 660 Hz | 0.42 → 3.44 | +1.2 ms | 0.176779 | Individual capture checks passed; correct 2x level |
| Decoded video 880 Hz | 0.38 → 3.62 | -8.9 ms | 0.088594 | 3.24 s audible duration failed |
| Native video fallback | 0.34 → 3.36 | -14.2 ms | 0.088595 | Individual capture checks passed |
| Mixed | 0.36 → 4.00 | +571.4 ms | 0.191623 | Duration, gaps and phase failed |
| Mixed Player volume 0.5 | 0.38 → 4.12 | +735.0 ms | 0.092412 | Level response observed; timing/integrity failed |
| Mixed Player muted | silence | +170.3 ms | **0**, right **0** | Mute silence passed; clock bound failed |
| Mixed capture gain 0.5 | 0.38 → 4.16 | +840.8 ms | 0.093504 | Planted level mismatch detected; timing/integrity failed |
| Mixed untouched repeat | 0.34 → 3.58 | +167.0 ms | 0.204397 | Timing/integrity and repeat gain failed |
| Amplified 0.6 s in/out fades | 0.62 → 3.46 | -8.8 ms | 0.174826 | 2.84 s audible interval failed |

The inclusion evidence is real: isolated native, amplified and video peak spectral amplitudes are approximately 0.1250, 0.2500 and 0.1253, with both stereo channels present. The mixed capture contains all three frequencies. However, it is explicitly **not** accepted merely because it is non-silent.

Integrity bounds remain visible in the probe: 2.88–3.12 s audible duration; <120 ms Player clock drift; no silent 5 ms interior blocks; every tone present in each 100 ms interior spectral window; adjacent spectral phase step <0.1 rad; right/left level ratio 0.70–0.80. Mixed output failed these checks, including six wholly silent 5 ms interior windows in the base mix (post-decode count), 39 in Player-half, 27 in capture-half, and 17 in the untouched repeat. Maximum per-tone phase steps in the base mix were 1.704, 2.821 and 1.868 rad, versus at most 0.000169 rad for isolated native/amplified and 0.000025 rad for isolated decoded video. This rejects discontinuous recordings rather than manufacturing a pass from their fixed total sample count. Phase changes can reflect Player resynchronization as well as missing audio; their underlying cause is unproven.

Player volume 0.5 measured **-6.334 dB** relative to the base mixed RMS. The single-host live capture-only 0.5 control measured **-6.232 dB** and triggered the expected `captured output gain mismatch: -6.232 dB`. The untouched repeat differed by **+0.561 dB**, failing the same comparator's 0.5 dB positive bound. Consequently the planted detection has **no qualified positive baseline** and is not a completed M3 negative-control proof.

The fade recording contains a nontrivial gain envelope: early/plateau RMS ratio 0.165 and late/plateau ratio 0.128, with no silent interior window. Its edge-duration assertion still fails and has not been relaxed or dismissed as intended fading. Distinguishing envelope callback timing, detector threshold effects, and scheduling is follow-up work.

An earlier isolated decoded-video diagnostic passed once (one test / 49.8 s overall, 3.02 s audible duration); another repeat showed +438.3 ms Player drift and 3.74 s audible output. This variability is retained as adverse evidence, not hidden by selecting the passing run.

Artifacts: `/tmp/timeline-player-audio-results/` contains ten short WAV recordings and the two failed-test traces. Each trace has the `player-capture-metrics` JSON attachment with revisions, managed-object requests, backend observations, stereo/spectral/phase measurements and frame clocks. They are intentionally outside the worktree. Override `PLAYWRIGHT_OUTPUT_DIR` to preserve a separate reproduction run.

## Escalation and remaining M3 work

**The missing Linux recording backend is resolved. Full mixed-output qualification is still blocked.** Current real Player output exhibits extended decoded-video tails, frame-clock stalls, silent interior gaps and phase discontinuities when backends play together. Cause is not isolated to Player scheduling, decoded-media buffering, host load, or the capture clock. The successful isolated native/amplified/fallback recordings make this a narrower problem than the old missing-device prerequisite.

Recommended next step: Viewing owner investigates actual Player decoded-video/audio scheduling and buffering against these preserved recordings and frame clocks, plus the amplified fade edges. Add focused regression coverage and resolve the discontinuities before accepting a synchronized mixed-output baseline. This worker cannot change preview product code under its assigned scope; no settled architecture decision was changed.

M3 still needs a pinned package/revision/media closure, an absolute playback/capture latency calibration, stricter onset/offset/drift and waveform comparison against the **actual final export** in the common 44.1 kHz stereo domain, positive frame/audio parity, picture-only planted mismatch, and a repeated audio-only planted mismatch against a successful positive baseline. The current RMS capture-only comparator is not that export comparator. No export or picture parity was run, and gate 6 is not closed.
