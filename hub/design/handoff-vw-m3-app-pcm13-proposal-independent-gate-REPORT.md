# Independent D08 review — App continuous PCM public13 consumer

## Decision

**APPROVE for the App owner’s actual port, conditionally on the existing adoption gates.**

This is a review of the unapplied proposal only. No App consumer release, package pin, physical parity, or Gate 6 qualification is claimed.

## Findings

- The proposed source-clock mapping is correct. It computes `computeMediaTrim(original clip, fps).trimBefore / fps` from the authored/compiled child, and passes the already sanitized child playback rate to public `applyAudioEnvelope`. Occurrence bounds only change the native `trimAfter`/window; they do not recompile or re-origin the envelope.
- The ordinary preview path applies the public envelope exactly once over all decoded source channels, emits the complete source as public IEEE-float WAV, and leaves native trim/rate plus the constant track×clip scalar to the media element. There is no caller-side slicing, resampling, frame-step gain, or second envelope application in the proposal.
- The prepared path calls the public `encodedEnvelopeSource` admission function. The matching HTTPS positive is accepted; wrong envelope identity, raw fractional origin, wrong child rate, and a `blob:` URL are refused. A supplied prepared record without a compiled envelope is also refused. The public contract is HTTP(S)-only for prepared external sources; this review does not broaden it to non-HTTP URLs.
- Rendering/export with an envelope requires an admitted prepared source and does not create an `AudioContext`, fetch, Blob, or browser decode. The native export node receives the admitted URL, native trim/rate, and constant gain.
- The existing `PreviewAudio` attempt remains the lifecycle owner. The proposal keeps the existing 500/1000/2000 ms retry budget, 10 s starvation release, premount behavior, late join without restarting a slow request, native readiness/progress/teardown, chrome Retry, and failure reset. Fetch/decode aborts, stale completions, `AudioContext.finally` close, and owned Blob URL revocation are attached to that attempt. `mediaFetchCredentials(src)` remains on the source fetch, preserving the existing gateway credential policy.
- The proposal includes `render_source` in the semantic identity used for reset/remount, so correcting a refused prepared record can recover through the existing error boundary rather than remaining stuck on the old failure.

## Evidence reviewed

- Current App base was verified read-only at `b1ef4b9b910ba72375c34cf319692f90d22edc25` (tree `8d8a10b057ed31fed69517e18a23b8ec3811447a`). The old `AudioTrack` helper and its existing attempt/retry/hold/error tests were read directly.
- Composition public13 archive SHA256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; archive safety check found 77 regular `package/` members and no unsafe/non-regular members.
- Public13 runtime smoke passed for trim/rate, full-source float WAV, matching admission, and all four prepared-source forgeries.
- `git -C .../port-check apply --check handoff-vw-m3-app-pcm13-implementation-brief-consumer.patch`: exit 0.
- Reviewed the handoff’s final isolated staging log: **3 files / 42 passed**, exit 0, using the verified public13 export-map entry; its baseline was **19 passed / 5 failed**, with the five failures being the intended matching-positive plus four refusal cases. The editable staging source was recycled before this independent review, so I did not claim a fresh 42-case rerun.

## Limits and required next steps

The 42-case evidence uses eight extracted App declarations and mocked Remotion/native media/fetch/AudioContext boundaries. It proves caller control flow and public PCM/admission behavior, not browser decoder behavior, gateway authorization on a live request, Blob playback, device resampling, memory/startup cost, or audible Player/export parity. The scoped lint and patch checks are not a project typecheck or App suite.

The App owner must first adopt and byte-verify Composition 0.0.13 in the actual App manifest/lock, then port this leaf and tests onto that exact cohort. Run the existing `AudioTrack.test.tsx`, `RemotionPreview.audioFailure.test.tsx`, and `TimelineComposition.media-conformance.test.tsx` (the prior cohort had 91 passing tests), preserving their positive fade/mute/boost/readiness/retry assertions as continuous-PCM equivalents rather than deleting or inverting them. Then perform the approved browser and physical parity gates. Until those pass, this remains an approved implementation handoff only.

No Composition product files were changed. No full suite, browser, socket, network, install, or render was run.
