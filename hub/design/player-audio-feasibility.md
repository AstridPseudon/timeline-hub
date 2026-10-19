# Early M1 Linux Player-audio capture feasibility

## Viewing-machine three-repetition qualification — 2026-10-19

Worker: `vw-m1-audio-quiet`. **FAILED: 6/6 tests, 26 real recordings, exit 1 in 588 s. Gate 6 remains OPEN; `d0954f18b` remains HELD RED.** No successful repetition was selected as the qualification result. Run 1 stops at its hard empty-mix assertion, so its Player-half/mute/capture-half/repeat controls are unexecuted. Runs 2 and 3 execute all nine control recordings; all three independent fade recordings execute.

This is the current Viewing-machine source/environment summary. The earlier main-machine report, including its adverse data, is preserved below. The requested quiet condition was only partially achieved: the shared Viewing-browser lock was held, but another Chromium tree was present during run 1. Its native/video/fallback/mix intervals consumed 72–82% of four host CPUs. Later captures were substantially lighter (roughly 20–38% aggregate), yet video tails, mixed discontinuities and the fade failure persisted. This does not certify a completely isolated quiet window or isolate host load as the sole cause. Competing work was not stopped; M1 priority was respected.

Source: App diagnostic base `d0954f18b984da60d81cf737231785ebbf216945`, central snapshot tree `2bc77ea0b8e9f697910df369f55893af3354e8e7`, plus the worker's diagnostic changes. The only final-source difference from the snapshot is the explicit TypeScript type of the comparator's assertion callback; TypeScript ES2022 transpilation of the snapshot and final monitor was compared and emits identical JavaScript. The focused comparator and helper typecheck were rerun on final source. No second browser request was submitted.

Environment: hostname `vm`, four CPUs; Linux `6.18.44-fc-v139 x86_64`; Node `22.22.0`; Playwright `1.60.0`; Chromium `141.0.7390.37` from `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`; Remotion `4.0.509`; actual Composition package version **0.0.2** (this diagnostic branch does not qualify the future 0.0.8 package); ffmpeg/ffprobe `6.1.1-3ubuntu5`; PulseAudio/pactl `16.1`. Package-lock SHA-256: `cc166c9c3cbe6555ad2dc38813e266e508aa09b764bd9998bddc1da4d43891ff`, identical in all six test attachments. No dependency installation or shared audio/default-sink mutation occurred.

All six tests generated identical media bytes. Native object: `sha256:1d3939943d6c952688e82d8e7e2ba7fab12bdbb45f5933260d06ad4905986dbe`; amplified: `sha256:fad180bf58e52a91d2df0a195a8b57bf2d56b44dd1d2a075fc6db762743bb8a6`; video: `sha256:e44ba749440cdbee9f948b7d007099a7e99c3e893dacf32c004068100fc49d89`. The sole fixture-generation change is `-fflags +bitexact`, suppressing random WebM container IDs; the playable tones, encoded media, clip durations, fades, backends and controls are unchanged. A local two-generation diagnostic found different unmodified WebM hashes and identical hashes with this muxer flag. Within each controls test, all mixed/control/repeat captures share one immutable revision (`e2e-external-22749-4`, `e2e-external-24775-4`, `e2e-external-27672-4` respectively; authoritative labels are in the attachments). Independent test-reset labels differ; their semantic inputs and object hashes match.

Exact central request (submitted once):

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m1-audio-quiet full-e2e-viewing-audio-quiet
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test vw-m1-audio-quiet-full-e2e-viewing-audio-quiet-1019200121-24009 1
```

Intermediate waits returned 124 while the same request was running; the final wait returned **1**. The service executed:

```bash
flock -x /tmp/timeline-viewing-browser.lock env \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  PLAYWRIGHT_TIMELINE_DEVICES=1 npm exec -- playwright test \
  --config tests/e2e/timeline/player-audio.config.ts --repeat-each=3 --workers=1
```

The opt-in config adds `--disable-background-timer-throttling` and `--disable-renderer-backgrounding`, removes `--mute-audio`, retains the existing DNS isolation, and uses one browser/private 0700 Pulse monitor at a time. No tab-capture retry, direct worker browser run, full Vitest suite, product/evaluator fix, export or parity qualification ran.

Focused final-source checks:

```bash
node --import tsx tests/e2e/timeline/player-audio-comparator.test.ts
node_modules/.bin/tsc --noEmit --target es2022 --moduleResolution bundler --module preserve --types node --skipLibCheck tests/e2e/timeline/player-audio-monitor.ts tests/e2e/timeline/player-audio-comparator.test.ts
npm exec -- eslint tests/e2e/timeline/player-audio*.ts tests/e2e/timeline/player-tab-capture.probe.ts --max-warnings 0
git diff --check
```

Results: **1 node test passed**, helper/comparator typecheck exit 0, ESLint exit 0, whitespace check exit 0. A separate ad hoc capture-file typecheck is not green: importing `support.ts` without the full application typing context reports missing `Window.__ASTRID_APP_LOCAL_TEST__`; including its declaring product file additionally requires the application's `@astrid/editor-sdk` alias. No project-wide typecheck pass is claimed.

The same live comparator is used by the synthetic diagnostic and captured PCM. Known-good 0.25-peak 660 Hz stereo, with 0.6 s linear in/out ramps over a three-second clip, measures **2.96 s**; a 30 fps frame-stepped ramp measures **2.98 s**. Both pass the unchanged strict `2.88 < duration < 3.12` bounds. A deliberately supplied 2.84 s duration is rejected by `three-second live media duration`. Real captured fades are **2.86 s in every repetition**, each failing that exact lower-bound assertion (`Received: 2.8600000000000003`, expected `> 2.88`). Their gain-envelope ratio checks pass. This evidence does not justify a comparator correction or relaxed live bounds; it points to the actual fade/playback envelope for follow-up. Synthetic PCM is only a unit diagnostic, never capture/parity evidence.

### Every real recording

Every retained WAV independently verifies as 48 kHz, two-channel s16 PCM, exactly 288,000 stereo frames. Startup/cardinality, managed-object inclusion, stereo, gaps and per-tone phase checks remain in place, as do the original duration/drift/gain limits. Gain-control expectations use soft assertions only to retain the failing verdict while collecting later recordings. Empty output remains a hard stop. All three media elements/backends are observed through the real mounted Player; no per-clip shift, correlation alignment, synthetic substitution or tolerance change is applied.

| Run | Case | Onset → offset (s) | Drift (ms) | Silent 5 ms blocks | Max phase step (rad) |
|---|---|---:|---:|---:|---:|
| 1 | native | 0.34 → 3.36 | -9.1 | 0 | 0.000005 |
| 1 | amplified | 0.20 → 3.22 | -1.2 | 0 | 0.000213 |
| 1 | video | 0.40 → 3.56 | +39.3 | 7 | 2.609272 |
| 1 | video-native-fallback | 0.18 → 3.20 | +8.6 | 1 | 3.098517 |
| 1 | mixed | silence | +24.8 | — | — |
| 1 | amplified-fade | 0.38 → 3.24 | +3.2 | 0 | 0.000184 |
| 2 | native | 0.20 → 3.22 | -0.3 | 0 | 0.000031 |
| 2 | amplified | 0.20 → 3.22 | +11.8 | 0 | 0.000088 |
| 2 | video | 0.34 → 3.54 | -1.7 | 0 | 0.000008 |
| 2 | video-native-fallback | 0.18 → 3.20 | -1.8 | 0 | 0.000037 |
| 2 | mixed | 0.16 → 3.20 | -1.8 | 0 | 0.000024 |
| 2 | mixed-player-half | 0.18 → 3.20 | +15.4 | 0 | 0.000010 |
| 2 | mixed-player-muted | muted | +10.0 | — | — |
| 2 | mixed-capture-half | 0.38 → 3.58 | +16.2 | 0 | 0.000013 |
| 2 | mixed-repeat | 0.16 → 3.36 | +116.2 | 0 | 0.000011 |
| 2 | amplified-fade | 0.52 → 3.38 | +15.3 | 0 | 0.000177 |
| 3 | native | 0.42 → 3.44 | -12.2 | 0 | 0.000186 |
| 3 | amplified | 0.40 → 3.42 | -1.5 | 0 | 0.000010 |
| 3 | video | 0.16 → 3.36 | +140.9 | 0 | 0.000014 |
| 3 | video-native-fallback | 0.18 → 3.20 | -11.1 | 0 | 0.000021 |
| 3 | mixed | 0.32 → 3.50 | +15.2 | 0 | 1.393019 |
| 3 | mixed-player-half | 0.38 → 3.78 | +177.5 | 0 | 0.234732 |
| 3 | mixed-player-muted | muted | +2.8 | — | — |
| 3 | mixed-capture-half | 0.36 → 3.40 | +34.9 | 0 | 1.594902 |
| 3 | mixed-repeat | 0.16 → 3.38 | -17.5 | 0 | 0.000023 |
| 3 | amplified-fade | 0.36 → 3.22 | +14.2 | 0 | 0.000207 |

Run 1 mixed PCM is entirely zero, despite frame 119 and +24.8 ms Player clock drift. Its media were already buffered 0–3 s, readyState 4, paused at currentTime 0 before the gesture, with visible document state. The observed shared AudioContext was suspended at 0.021333 s. After the measurement gesture both native/amplified elements emit `playing`, but there are **zero new decoded `buffer-start` events** (101 existed from warm-up), no media `ended` event, and no audible signal. This is a precise real-output/readiness blocker, not evidence that the recorder is empty or that inclusion passed. AudioContext lifetime/resume and decoded-audio rearming across warm-up/rewind are concrete follow-up targets; the responsible product callsite is not proven.

The isolated decoded-video durations are **3.16 / 3.20 / 3.20 s**; run 3 also exceeds the 120 ms frame-clock drift limit at +140.9 ms. Native and amplified isolated durations are consistently 3.02 s; native-video fallback has gaps/phase failures only in the higher-load first run. Run 2 mixed baseline has a clean interior, but its untouched repeat lasts 3.20 s. Run 3 mixed baseline lasts 3.18 s and all three phase checks fail (1.236 / 0.419 / 1.393 rad against <0.1). Its Player-half lasts 3.40 s with +177.5 ms drift. Its capture-half also fails amplified/video phase checks. Therefore there is no stable three-repetition positive mixed baseline.

Runs 2/3 Player-half gain differences are -6.020603 / -5.978111 dB; capture-half differences are -6.021131 / -5.974940 dB. Both trigger the existing gain-mismatch detector. Untouched-repeat differences are -0.000465 / +0.044651 dB, inside the unchanged 0.5 dB gain bound, but their durations are 3.20 / 3.22 s. Mute is exactly zero in both channels in the two runs that reach it. These are gain/mute observations only; planted mismatches do not count as qualification while positive integrity fails.

### Host/process CPU and capture timing for every interval

Host busy is the aggregate `/proc/stat` delta over each capture (idle+iowait excluded, guest counters not double-counted). Browser CPU sums CDP cumulative CPU-time deltas for process IDs present at both endpoints, expressed as percent of one core; raw per-process samples are retained. Pulse and ffmpeg CPU use their `/proc/<pid>/stat` utime+stime deltas and the measured 100 Hz clock tick. Host load, raw process accounting, browser process types/IDs/CPU, and host-wide `ps` snapshots are recorded in each WAV's diagnostics and trace attachment, sampled approximately every 500 ms without overlap.

| Run | Case | Host busy % | Browser CPU % of one core | Pulse / ffmpeg CPU % of one core | Load (1 min) | Spawn → Pulse input PTS (ms) |
|---|---|---:|---:|---:|---:|---:|
| 1 | native | 82.1 | 67.0 | 1.90 / 3.62 | 3.09–3.49 | 272.4 |
| 1 | amplified | 31.4 | 59.9 | 1.07 / 1.16 | 4.12–4.22 | 57.6 |
| 1 | video | 73.1 | 85.6 | 1.21 / 2.29 | 3.88–4.40 | 264.8 |
| 1 | video-native-fallback | 78.9 | 78.2 | 1.81 / 0.98 | 3.65–4.08 | 99.7 |
| 1 | mixed | 72.3 | 70.6 | 1.21 / 2.46 | 4.70–4.94 | 177.2 |
| 1 | amplified-fade | 24.3 | 58.6 | 0.92 / 0.99 | 4.43–4.89 | 85.1 |
| 2 | native | 23.0 | 59.8 | 1.38 / 0.99 | 4.56–5.13 | 83.8 |
| 2 | amplified | 22.3 | 55.8 | 0.92 / 1.33 | 4.18–4.55 | 70.2 |
| 2 | video | 26.2 | 66.8 | 0.92 / 2.65 | 4.15–4.17 | 217.3 |
| 2 | video-native-fallback | 21.4 | 70.5 | 1.22 / 1.49 | 3.89–4.42 | 91.0 |
| 2 | mixed | 21.2 | 69.2 | 1.22 / 1.16 | 3.95–4.30 | 194.7 |
| 2 | mixed-player-half | 37.9 | 75.2 | 1.53 / 1.16 | 4.32–4.61 | 54.7 |
| 2 | mixed-player-muted | 26.4 | 70.1 | 0.91 / 2.80 | 3.95–4.21 | 207.8 |
| 2 | mixed-capture-half | 24.1 | 73.5 | 1.21 / 1.97 | 4.25–4.62 | 128.6 |
| 2 | mixed-repeat | 27.8 | 75.4 | 1.37 / 1.32 | 3.77–4.19 | 63.4 |
| 2 | amplified-fade | 23.4 | 64.5 | 0.76 / 1.81 | 3.79–4.05 | 113.0 |
| 3 | native | 34.6 | 76.4 | 1.81 / 2.12 | 3.47–4.10 | 127.9 |
| 3 | amplified | 19.6 | 55.6 | 0.92 / 1.66 | 3.08–3.09 | 86.2 |
| 3 | video | 23.3 | 68.7 | 1.07 / 1.49 | 3.17–3.75 | 65.4 |
| 3 | video-native-fallback | 25.1 | 74.4 | 1.52 / 1.82 | 2.83–3.08 | 190.9 |
| 3 | mixed | 25.2 | 79.5 | 1.52 / 2.80 | 3.36–3.47 | 154.0 |
| 3 | mixed-player-half | 29.8 | 98.6 | 1.67 / 2.95 | 3.47–3.77 | 247.1 |
| 3 | mixed-player-muted | 24.0 | 70.1 | 1.06 / 1.80 | 2.86–3.38 | 76.6 |
| 3 | mixed-capture-half | 31.4 | 96.1 | 1.67 / 3.45 | 2.73–2.88 | 173.2 |
| 3 | mixed-repeat | 23.2 | 73.9 | 1.22 / 1.32 | 3.28–3.57 | 80.0 |
| 3 | amplified-fade | 28.7 | 58.9 | 0.92 / 1.16 | 2.96–3.13 | 85.5 |

No fixed sleep is used as recorder readiness. Each interval waits for ffmpeg's `Output #0`, then records the Node play-request bounds and real browser click/media/buffer events. The raw input-start PTS, output declaration, play request/completion and full ffmpeg/Pulse logs are kept. Spawn-to-first-Pulse-PTS varies (see table), so it is not honestly describable as a fixed startup constant. One operational latency estimate is fixed from **run 1 native only**: Pulse input-start PTS plus its 0.34 s PCM onset gives **66.0 ms after the browser click** (48.8 ms after `playing`), with 20 ms detector quantization. This estimate is recorded, never subtracted or retuned per clip. Pulse wall-clock PTS and browser performance epoch are not an independently calibrated physical/export clock; absolute Player/export latency is unqualified. The same native diagnostic gives 89.7 / 97.5 ms in later runs; these are retained variance checks, not replacement calibrations.

Diagnosis order and limits: host contention is measured, not excluded; explicit anti-throttle flags did not produce a stable baseline. Media-element/frame-zero readiness alone does not certify the decoded audio queue or a running/rearmed audio graph. The repeatable decoded-video tail and first-run missing post-rewind scheduling make Player decoded-audio resume/queue/stop behavior the next focused investigation, with media-element gain-envelope callbacks a separate fade target. The Pulse recorder stays at the expected sample format/cardinality with no overrun/underrun/drop/corruption report, and native/amplified controls remain stable. This narrows the investigation but does not prove a particular source fix or exclude sink/start-clock effects. No product fix was authorized or applied.

Artifacts: all **26 WAVs**, their `.wav.diagnostics.json` files, **six failed-test traces**, `player-capture-metrics` attachments and per-recording diagnostics remain under `/tmp/timeline-player-audio-results/`. Central request/summary/full log: `ORCH/tests/vw-m1-audio-quiet-full-e2e-viewing-audio-quiet-1019200121-24009/`. Direct source-generated media directories and private Pulse daemons/directories are torn down in the existing `finally` paths; the central snapshot is removed. Nothing is left as build output in the worker worktree.

Recommended next step: keep the diagnostic branch red; authorize a bounded Player audio-graph/decoded-queue investigation using the suspended-context/no-rearm repro and preserved lower-load tails, alongside the main measurement analyst's conclusions. Obtain an actually isolated window if needed after M1 work, then rerun the same complete fixture only after a concrete follow-up change. Final-export comparison, common 44.1 kHz parity, an independently calibrated latency, positive picture/audio parity and qualified planted mismatch detection remain unverified.

---

## Earlier main-machine capture report — preserved


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
