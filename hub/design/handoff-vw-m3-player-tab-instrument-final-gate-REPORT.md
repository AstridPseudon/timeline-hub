# Independent review: `vw-m3-player-tab-mix-instrument-port`

## Verdict

**Narrow REJECT for future qualification until the controller and PTS guard are tightened.** The completed App leaf is structurally conservative and the offline lifecycle checks pass. I did not run a browser, localhost service, render, capture, network, install, or full suite.

## Reviewed source

- App branch: `tl/vw-m3-player-tab-mix-instrument-port`
- App tip: `c60cef9470d0e02abc42c4850cdbd4d1112e7c76`
- App13 base recorded by the branch: `b1ef4b9b910ba72375c34cf319692f90d22edc25` / tree `8d8a10b057ed31fed69517e18a23b8ec3811447a`
- Agent13 constant: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`
- Runtime13 constant: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Composition13 constant: source `af98594d`, artifact `9412ae25`

The branch changes only the six intended viewing-parity leaf files. No App product/root/pin/DTO/source files changed, and the normal Render/download helper was not rewritten.

## Verified positives

- The parity source contains exactly five cases. The new whole-tab case is before the picture-negative case; the obsolete four-case assertion was correctly changed to five.
- The new case uses the existing mounted Player, calls `getDisplayMedia({video: true, audio: true, preferCurrentTab: true})`, requires exactly one video and one audio track, creates one `MediaRecorder` with `video/webm;codecs=vp8,opus`, and rejects empty mux bytes.
- The recorder starts before `warm`, then observes `after-warm`, waits for readiness, observes `after-readiness`, plays, and observes `after-play`. There is no silent primer, keepalive, mute/volume reset, source factory, per-clip realignment, calibration fudge, OS-audio path, certificate/global-OS mutation, or fixture change in the diff.
- Normal Render/download remains the existing path and is still exercised before the tab capture. Existing strict `2/255` and `.001` pixel controls and the planted picture negative remain; no mute/half/boost controls were altered.
- `finally` stops an active recorder and all real capture tracks. `error` and `abort` listeners reject the capture; simulated offline error/abort runs stopped both tracks.
- `--discover` exists, and source-level list verification finds all five cases in the required order. The controller constants keep App13 as `pending-consumer-adoption` and physical mix as unclaimed.

## Blocking findings

1. `tab-audio.controller.mjs --ready` does not call `discover`, does not require the completed App tip/tree, and does not invoke the existing `sourceVersions`/preflight/postflight controls. `assertAppOwnLeaf` only rejects forbidden paths, so App13 base itself (or another arbitrary descendant with only allowed paths) can pass the ancestry/clean-tree check. The controller’s `CONTROL` booleans are declarations, not checks. It therefore does not fail closed for the requested source/profile/version, 77-file Composition, whole private graph/six peer pins, Node pre/post, resource floor, flock, short-0700 temp, or fresh manager grant controls. The existing parity harness contains several of those checks, but this independent `--ready` path bypasses them.
2. `assertChrome155` accepts only a digest prefix (`cb19b599`), while the existing browser-profile guard has the full Chrome155 SHA-256. This is weaker than the requested version/profile fail-closed gate.
3. `assertNativePts` checks that the declared streams are one video and one audio and that present packet PTS values are monotonic, but it does not require any packet for each stream. A probe with one video stream’s packets and zero audio packets is accepted. That is insufficient evidence for a mixed video+audio native-PTS capture. Add a per-stream `values.length > 0` assertion and a regression test.
4. The committed unit tests cover warm failure and a video+audio monotonic-positive / video-nonmonotonic-negative case, but do not directly cover recorder `error` or `abort`, missing audio packets, wrong track cardinality, or recorder-start failure. The implementation’s simulated error/abort cleanup behavior passed, but the branch’s own tests do not prove those paths.

Because App13’s actual consumer is still pending and the matching Agent13 pair is not ready, no capture grant or actual-capture claim is valid from this branch. The rejection is narrow: after the controller is made the single fail-closed gate and the PTS guard/tests are strengthened, the fifth case is suitable for a separately manager-granted central qualification run.

## Exact checks run

- `node .review-tab-audio.controller.test.mjs` (temporary exact controller-test extraction; 2/2 pass; removed afterward).
- Exact target `tab-audio.ts` transpile-and-run via stdin: recorder ordering, VP8/Opus MIME, one video+one audio track, chunk retention, native PTS positive/negative, and cleanup (pass).
- Exact target `tab-audio.ts` transpile-and-run via stdin with simulated recorder `error` and `abort` (both pass; both tracks stopped).
- Exact target `cases.ts` source-level list check via stdin: 5 cases, tab case before picture negative (pass).
- `git diff --check tl/vw-m3-player-tab-mix-instrument-port^ tl/vw-m3-player-tab-mix-instrument-port` (pass).
- Static changed-path and forbidden-topology scan (six intended files only; no source factory, primer, keepalive, mute reset, realignment, calibration, certificate, Pulse/OS mutation matches).
- A negative audit of `assertNativePts` with no audio packets was intentionally run and **incorrectly accepted**, confirming finding 3.

No Playwright browser was launched. A full App suite, localhost suite, live socket, render, and actual capture were not run.

## Recommended next steps

1. Make the controller require the exact completed App source/tree, invoke the five-case `--list` check as part of readiness, use the existing full source/profile/private-graph preflight and postflight, and require explicit manager-grant/fence markers before any capture-capable mode. Compare the full Chrome155 digest, not a prefix.
2. Require at least one finite PTS packet for both audio and video and add wrong-cardinality, start-failure, `error`, `abort`, and missing-audio regression tests.
3. Re-run the small offline lanes after those changes. Only then request one central capture after App13 adoption and the matching Agent13 pair are both qualified; retain the result as native stream/mux/PTS evidence only until physical-mix verification is separately proven.
