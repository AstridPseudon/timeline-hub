# Handoff: vw-m3-player-tab-mix-instrument-port

Status: READY literal for manager-controlled capture; no physical mix claim.

Implemented a fifth existing viewing-parity case in App. It keeps the normal Render/download path, uses the existing actual managed Player frame helper, starts one MediaRecorder on getDisplayMedia video+audio before actual Player warm/readiness/play, and checks one video stream, one audio stream, non-empty mux bytes, native monotonic packet PTS, and cleanup lifecycle.

The helper observes media readiness, paused/currentTime/mute/volume state, and AudioContext state before/after warm/readiness/play. It does not create a silent primer, keepalive, mute reset, OS-audio path, waveform, PCM claim, clip realignment, start-offset tuning, or synthetic fixture. Existing 640x360 video and 44.1kHz audio fixtures are unchanged. The four prior cases and strict RGB 2/255, .001, audio, mute/.5/boost, and planted-negative expectations remain.

The controller records the exact pending App13 candidate and matching graph:

- App source `b1ef4b9b910ba72375c34cf319692f90d22edc25`, tree `8d8a10b057ed31fed69517e18a23b8ec3811447a`.
- Agent13 source `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, tree `75354d38c898729bac09619679f5421faba319ed`.
- Runtime13 source `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Composition13 source prefix `af98594d`, artifact prefix `9412ae25`.
- App13 consumer status remains `pending-consumer-adoption`; no pin or product consumer change was made.

The controller requires own-leaf-only App changes, whole-graph/77-byte controls, clean source roots, and Chrome155 `155.0.8059.84` discovery. It does not authorize capture by itself.

## Evidence

All targeted tests, lint, targeted TypeScript, offline discovery, and `git diff --check` passed. The targeted neighbor lane ran 9 files with 9 passing subtests.

No browser, render, localhost, network, install, full suite, or central capture was run by this worker, per the task boundary. The manager must request the central actual-capture grant and run controlled capture after integrating this leaf. Any resulting artifact is stream/mux/native-PTS proof only until App13 adoption and physical-mix verification occur.
