# Flat handoff — Chrome155 tab capability probe

READY small diff on App base `ef1366bc9` / `tl/vw-m3-tab-complete-package-guard`.

Changed only:
- `tests/e2e/timeline/tab-audio-capture.config.ts`: standalone named pinned Chrome155 config; workers 1; retries 0; no inherited App webServers.
- `tests/e2e/timeline/tab-audio-capture.probe.ts`: fixture-owned `http.createServer` at `127.0.0.1:0`, HTML + generated native 48 kHz stereo PCM WAV only, finally cleanup; one real-click getDisplayMedia + MediaRecorder flow.
- `tests/e2e/timeline/tab-audio-capture.analysis.mjs` and `.test.mjs`: 880 Hz WebAudio + 1320 Hz HTMLAudio constants/generator, mixed positive and pure negative controls, existing phase-blind tone presence checks.

Controller, guard framework, 11-package graph, Chrome155 255-file tree, Playwright 106-file tree, six render hashes, Node20.19.4, and Composition package8 were left unchanged. No App/player/provider/pin/product code changed.

Passed: strict targeted TypeScript, analysis/controller Node tests (2 files, 0 failures/skips), scoped ESLint, controller `node --check`, setup `bash -n`, and `git diff --check`.

No browser, listener/socket probe, network, install, central test service, or full suite was run. The old ef136 central failure remains a pre-browser config.webServer cwd duplication failure; it is not an unsupported-backend conclusion.

Manager: after harness commit and exact final-SHA grant, register a new central namespace (suggested `e2e-viewing-tab-audio-capability-chrome155`) and invoke the unchanged `tests/e2e/timeline/setup-tab-audio-capture.sh` once with unique `TAB_AUDIO_GRANT_PATH`, `TAB_AUDIO_PREFLIGHT_PATH`, `TAB_AUDIO_RUN_MARKER`, `TAB_AUDIO_RUN=1`, and the shared flock. The result may claim only one live video track, one live tab-audio track, both declared source tones present, and native per-stream PTS. No App-player/source or parity claim.

