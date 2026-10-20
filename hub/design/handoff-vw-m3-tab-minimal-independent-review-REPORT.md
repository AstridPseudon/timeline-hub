# FLAT independent review — Chrome155 tab capability probe

## Decision

**APPROVE**, conditional on a fresh exact-source grant for the committed source below. This review authorizes one central Chrome155 capability run only; it does not authorize a browser run, a listener run, a network run, an App/player run, a fake-Runtime run, a PulseAudio fallback observation, or any phase/parity claim.

No source defect was found in the reviewed capability probe or its guards.

## Reviewed source

- App worktree: `/home/user/work/wt/vw-m3-tab-minimal-independent-review`
- exact clean committed source SHA: `e421b5d4438d8b27b689e9ae8c0218b7a30c68c6`
- exact source tree: `76141fb32e0a3133dd202b84b05a4192e99c0ab6`
- parent complete-package guard source: `ef1366bc9ec3076c5f567805fe76686841419b61`
- full tracked source hash: `7a417a86b52b0732d8bd722a8e6f33885947d71ec80c09cb96ff04932dff24e7` (`5879` files)
- selected-input hash: `2161aa4c9398528253c0d82dba5fec0d5f176b662da2304d66ce49af9197aebc`
- worktree status at review: clean; no untracked files

The existing `ef1366bc9` grant is stale for this source and must not be reused. The fresh grant must name `e421b5d4438d8b27b689e9ae8c0218b7a30c68c6` and all fingerprints above.

## Review findings

- `tab-audio-capture.config.ts` is standalone: it does not import the App Playwright config, defines no `webServer`, has one named `native-codec-chrome155-tab-audio` project, `workers: 1`, and `retries: 0`, with the pinned Chrome executable and native-codec arguments.
- `tab-audio-capture.probe.ts` starts a fixture-owned `http.createServer` on `127.0.0.1:0`, serves only generated HTML and the generated finite 48 kHz stereo PCM WAV, supplies the URL to the test, and closes all connections and the server in fixture `finally` teardown.
- The test performs a real Playwright locator click on the fixture button. The click handler then calls `getDisplayMedia({video: true, audio: true, preferCurrentTab: true})`, creates one `MediaRecorder`, and records the tab stream.
- The two declared sources are independent: an 880 Hz WebAudio oscillator and a generated 1320 Hz HTMLAudio WAV. The analysis checks both frequencies independently, with positive mixed-source and pure-source negative controls, without phase/alignment/resampling/level-normalization claims.
- `dataavailable` payloads receive callback-order indexes; asynchronous payload reads are chained and the encoded chunks are reassembled by those indexes. `ffprobe` checks one video plus one audio stream and monotonic native PTS within each stream, retaining native time bases and making no cross-stream alignment claim.
- No probe/config import reaches App support, the editor URL, fake Runtime reset, SDK code, Runtime, or Composition source. `playwright.config.ts`, `support.ts`, and `tests/e2e/fake-runtime/` occur only in the controller's selected-input drift hash; they are not loaded by the standalone config or probe. No code sets or changes `HOME`.
- The 11-package graph is collected from the actual installed package graph, including `@remotion/media`, `@remotion/web-renderer`, and `@remotion/layout-utils`; `playwright-core` is separately frozen and checked. Full tracked source, selected inputs, browser tree/executable, Node identity, package graph, six render-graph files, and Composition's 77-file graph are guarded.
- Preflight requires the quiet guard to be absent, the shared flock to be held, clean committed source, and a grant matching the exact fingerprint. Claim uses an exclusive one-shot marker. Postflight rechecks clean source and all dependency fingerprints and requires the marker when `TAB_AUDIO_RUN=1`. The launcher holds FD 9 for the complete run and runs postflight from its EXIT trap.

## Exact environment fingerprint requirements

The fresh grant must retain these exact values and the complete objects returned by the controller's `packageGraphFingerprint()` and `renderGraphFingerprint()`:

- profile: `native-codec-chrome155`
- browser: `/opt/google/chrome/chrome`, version `155.0.8059.84`, package `155.0.8059.84-1`, executable SHA256 `cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76`, full tree SHA256 `5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e`, `255` files
- Node: `/tmp/vw-m3-agent-gate-node20.19.4/bin/node`, `v20.19.4`, executable SHA256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`
- package graph SHA256: `215e32c6fc86ba57ad36f766a273e43b8c9d328341308fafcda752b03e9eb858`
- package versions: `@playwright/test`/`playwright`/`playwright-core` `1.60.0`; `react`/`react-dom` `18.3.1`; `remotion`, `@remotion/player`, `@remotion/media`, `@remotion/web-renderer`, `@remotion/layout-utils` `4.0.509`; `@banodoco/timeline-composition` `0.0.8` with exactly `77` files
- render-graph hashes: `PlayerUI.js=5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb`; `use-player-methods.js=ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46`; `use-playback.js=6c8369a19d7a29eab5dab4642799172d4f2a7e11dad25edcb673ec5729fb0`; Player `index.mjs=d3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12`; Remotion `index.mjs=5a1584f7660fa8fffa7eb8fe016b82a4d719e67d4b7904d4fa4f299eb1355f28`; shared audio tags `949ccec3419398183e8e22f63820a4a57cb8379befb184fbac9a3acde040c5b8`
- grant `backendOrder`: exactly `['tab', 'private-pulse']`; this probe may claim only the tab result, never private PulseAudio evidence
- grant `environmentApprovalReference`: required and must identify the manager/orchestrator approval for this one run

## Exact one-shot invocation

Run once from the exact clean worktree containing the SHA above, with a newly created grant and unique, nonexistent preflight/marker paths. The manager must substitute the actual grant path and unique namespace paths:

```bash
TAB_AUDIO_GRANT_PATH=/absolute/path/to/fresh-e421b5d4438d8b27-grant.json \
TAB_AUDIO_FINAL_SHA=e421b5d4438d8b27b689e9ae8c0218b7a30c68c6 \
TAB_AUDIO_PREFLIGHT_PATH=/tmp/timeline-tab-audio-chrome155-e421b5d4-READY_GRANTED.json \
TAB_AUDIO_RUN_MARKER=/tmp/timeline-tab-audio-chrome155-e421b5d4-RUN_STARTED.json \
TAB_AUDIO_LOCK_PATH=/tmp/timeline-viewing-browser.lock \
TAB_AUDIO_RUN=1 \
bash /home/user/work/wt/vw-m3-tab-minimal-independent-review/tests/e2e/timeline/setup-tab-audio-capture.sh
```

The launcher must be the unchanged `tests/e2e/timeline/setup-tab-audio-capture.sh`; it supplies the pinned Node default, takes the shared flock on FD 9, runs `--preflight`, then `--claim`, invokes only the named standalone Playwright config/project, and runs `--postflight` from the EXIT trap. Use a distinct central namespace such as `e2e-viewing-tab-audio-capability-chrome155`. Do not reuse any prior READY/RUN marker or prior grant.

## Allowed result claim

The single live run may report only: one live video track, one live tab-audio track, both declared source tones present in decoded captured audio, and monotonic native per-stream PTS/time bases. Decoded VP8 marker bytes remain diagnostic only. The run does not establish App-player/source capability, audio/video phase, clip alignment, parity, global origin, or private-PulseAudio behavior.

## Checks run

All passed locally without browser, listener, network, install, grant, central-service, or full-suite execution:

```text
node --test tests/e2e/timeline/tab-audio-capture.analysis.test.mjs tests/e2e/timeline/tab-audio-capture.controller.test.mjs  # 2 files, 0 failures/skips
npm exec -- tsc --noEmit --target ES2022 --lib ES2023,DOM --module ESNext --moduleResolution bundler --strict --skipLibCheck --allowJs --resolveJsonModule --types node tests/e2e/timeline/tab-audio-capture.probe.ts tests/e2e/timeline/tab-audio-capture.config.ts  # pass
npm exec -- eslint tests/e2e/timeline/tab-audio-capture.probe.ts tests/e2e/timeline/tab-audio-capture.config.ts tests/e2e/timeline/tab-audio-capture.analysis.mjs tests/e2e/timeline/tab-audio-capture.analysis.test.mjs --max-warnings 0  # pass
node --check tests/e2e/timeline/tab-audio-capture.controller.mjs  # pass
bash -n tests/e2e/timeline/setup-tab-audio-capture.sh  # pass
git diff --check  # pass
```

