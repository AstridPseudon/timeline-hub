**Gate 6 remains open.** Mixed playback has real backend-relative discontinuities; capture artifacts alone cannot explain it. No product/test edits, installs, browser runs, or commit were made. Both existing failed test verdicts remain unchanged.

Paths below are relative to `/home/user/work/wt/vw-m1-player-mix`, except installed dependencies, which resolve through shared `node_modules`.

| Finding | Diagnosis and confidence |
|---|---|
| Mixed clock excess | **High:** Player timing changed independently of PCM capture. Base mix: `(20097.1−15592.4)/1000−118/30 = 0.571367 s`. Frames 11→12 took 235.1 ms; 15→16 took 182.3 ms. These can include intentional buffering pauses; they do not by themselves prove erroneous scheduling. |
| Mixed gaps/phase | **High:** actual discontinuities exist upstream of the common recorder. Base mix contains exact stereo-zero runs at 1.230667–1.262812 s and 3.668771–3.697396 s. Untouched repeat contains 18.146 ms and 76.417 ms zero runs. |
| Repeat gain failure | **High:** the fixed measurement window confounds gain with interruptions. It is not evidence of a gain-control defect. |
| Decoded-video tail | **High:** prolonged captured output; **unresolved cause**. Constant startup latency cannot explain increased duration. |
| Fade duration | The generic audible-duration metric is biased, but **threshold bias alone does not explain this recording**. Backend/envelope timing remains unresolved. |

**Calculations from captured PCM**

The repeat’s steady 1.7–1.8 s and 2.2–2.3 s windows retain approximately 0.1250/0.2500/0.1253 tone amplitudes. Their phase changes are:

- 440 Hz: 1.583039 rad.
- 880 Hz: 1.964035 rad.
- A common recorder sample displacement requires `Δφ880 = 2Δφ440 (mod 2π)`. Observed residual: **−1.202042 rad**.

Thus whole-stream capture loss or displacement cannot be the sole cause. Backend scheduling, pausing, or resynchronization is implicated; the responsible implementation path is not yet isolated.

The original gain window is `onset+0.5` through `onset+2.5` (`player-audio-capture.probe.ts:68–73`). Its repeat result is **+0.561 dB**. Diagnostic whole-record energy, `E=Σ(left²)/48000`, gives:

| Capture | E | `10 log10(E/Ebase)` |
|---|---:|---:|
| Mixed | 0.1346325025 | 0 dB |
| Untouched repeat | 0.1385322349 | +0.124009 dB |
| Player half | 0.0339375916 | −5.984689 dB |
| Capture half | 0.0336387094 | −6.023106 dB |

Stable 2.8–3.1 s mixed/repeat RMS values are 0.21659566/0.21659432. This identifies substantial window bias; whole-record energy is diagnostic only and does not replace the failed continuity/comparator checks.

Decoded video retains approximately **0.1253 peak amplitude at 3.5–3.6 s**, with phase unchanged from an earlier steady window, despite only −8.933 ms aggregate Player drift. This is more than threshold-edge rounding. Scheduling/replayed audio and downstream capture insertion remain distinguishable possibilities; periodic tones cannot reveal every repeated/dropped whole cycle.

**Fade assessment**

`src/tools/video-editor/lib/audioFade.ts:30–46,59–65` implements linear **amplitude** ramps: 18 frames in/out over 90 frames at 30 fps. The measured plateau RMS is approximately 0.176779.

The continuous-ramp threshold approximation is:

`3 − 2×0.6×(0.004/0.176779) = 2.972847 s`

Frame stepping and 20 ms detector windows bias the edges, so thresholded onset is not playback start. Nevertheless, the observed support is approximately **0.621083–3.441375 s**; RMS at 3.42–3.44 s remains approximately **27.6–27.7% of plateau**, then vanishes. The measured falling-envelope extrapolation reaches zero near 3.614 s. Consequently, dismissing the 2.84 s verdict as merely the threshold would be unsupported. Product ownership of the cutoff is unproven.

**Relevant implementation**

- `AudioTrack.tsx:122–125,151–166` deliberately holds playback until `HAVE_FUTURE_DATA`; the probe’s initial readiness check requires only `readyState >= 2` (`probe.ts:163–165`). After warm-up/rewind, it checks frame zero but does not record renewed readiness (`:177–187`).
- `ReadinessVideo.tsx:23,42–46` records that a frame was decoded; this does not establish sustained decoder/audio readiness.
- Installed `@remotion/media/dist/esm/index.mjs:659–704` blocks while collecting 100 ms of audio; `:1662–1689,1714–1732` can restart video iterators with playback holds; `:2294–2298,2370–2373` destroys audio iterators on anchor changes.
- Installed `@remotion/player/dist/cjs/use-playback.js:229–239` intentionally suspends/waits during buffering and resets its wall-clock origin on resume. Native media also pauses during Player buffering (`remotion/dist/cjs/use-media-playback.js:109–118`).
- The managed-media wrapper changes request credentials/CORS, not scheduling (`vendor/astrid-browser/astrid/packs/rendering/shared/managed-media.tsx:17–20`).

Neither trace contains scheduling/readiness console events. Existing observations therefore cannot separate intended holds from faulty resume/rescheduling, and establish no host-load cause.

`player-audio-monitor.ts:45–61,81–83` trims to **288,000 received frames**. This guarantees file length, not continuous acquisition: dropped packets can be followed by later samples. WAV discards original acquisition timing. Keep the existing gap/phase rejection; even that cannot detect every whole-period loss.

**One next experiment**

Have the central test service run **one quiet, unchanged mixed replay**, retaining the current assertions. Record a shared clock timeline containing Player `waiting/resume/frameupdate`, native media `currentTime/readyState/seeking`, AudioContext state/currentTime/output timestamps and decoded-node start/stop times, alongside recorder packet PTS/sample totals and monotonic capture/gesture times. This will locate discontinuities relative to buffering and distinguish backend rescheduling from capture-clock loss. No speculative product fix is justified yet.

**Validation:** read-only Python analysis (`wave`, NumPy, `zipfile`, JSON) checked all ten recordings: each is 48 kHz, stereo s16, 288,000 frames; muted PCM is exactly zero. `git status --short` returned clean. No tests or full suites were run; existing browser evidence remains **2 failed**. Export parity and absolute capture latency remain unverified.