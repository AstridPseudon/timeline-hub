# App public13 PCM consumer independent review

## Verdict

**APPROVE — source review only.** Candidate 35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a, tree db0da562200367715858b11d258b40a3f5664b20, is acceptable for the reviewed public13 PCM consumer scope. This is not a parity, integration, release, or production qualification claim.

The detailed qualified-source flatdesign handoff was absent from the accessible filesystem. I reconstructed this report from the actual candidate source, the available worker-report.md/report.md, the readiness report, the reviewed pin, the immutable public13 archive, and fresh controls below. I did not assume the missing artifact existed.

## Exact identities

| Item | Identity |
| --- | --- |
| Reviewed public13 pin | commit 2b3c431fb0efb967c59662c50f5a5bd694f9157e, tree eff2edbae8cf7cc4a68d3861873267f9795992bd |
| Candidate | commit 35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a, tree db0da562200367715858b11d258b40a3f5664b20 |
| Candidate parent | 2b3c431fb0efb967c59662c50f5a5bd694f9157e |
| Public13 archive | vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz, 58,477 bytes |
| Archive SHA-256 | 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738 |
| Lock integrity | sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ== |
| Archive SHA-512 | eaa80401c7d8a841ae89eb284650458f54271200ca759b22b1076b322bce36d73794072df2d85dcd56cd57a2fb958e5fd83f6fbd32191d30fcbca85f5a02ceb9 |
| Archive contents | 77 regular files; all 77 extracted overlay files byte-equal to the archive |
| Manifest/lock | Both resolve to file:vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz; lock version/resolved/integrity and peer pins match |

Changed files, exactly seven:

- src/tools/video-editor/compositions/AudioTrack.tsx
- src/tools/video-editor/compositions/AudioTrack.test.tsx
- src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx
- src/tools/video-editor/compositions/compiledAudioSourceClock.ts
- src/tools/video-editor/compositions/compiledAudioSourceClock.test.ts
- src/tools/video-editor/compositions/continuousPCM.contract.test.tsx
- src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx

## Source review

- AudioTrack.tsx uses only public @banodoco/timeline-composition/evaluation APIs: compileAudioEnvelope, computeMediaTrim, applyAudioEnvelope, audioEnvelopeWav, encodedEnvelopeSource, and the public error/type.
- compiledAudioSourceClock.ts delegates trim/rate to public computeMediaTrim and getSanitizedPlaybackRate; it contains no timing/DSP implementation.
- No private Composition imports, validator copy, envelope canonicalizer copy, resampler, or local DSP was added.
- The consumer compiles once, decodes full channels once per attempt, applies the public envelope once at source time, emits public float WAV once, and retains native trim/rate plus one downstream numeric track×clip scalar.
- Prepared records go through exact public admission. Wrong envelope key, fractional/raw source clock, child rate, or non-HTTP(S) URL refuses with the existing canonical error path; it does not silently fall back to the original source.
- Existing readiness/backoff/hold/retry/manual Retry/mute/boost behavior remains. Preparation shares the existing attempt state: fetch aborts on abandonment, late decode completion cannot publish, decoder contexts close in finally, and owned Blob URLs revoke on cleanup/replacement.
- The original authored source clock is preserved through occurrence bounds: the source clock uses the original clip while renderClip supplies only the shortened native window. The downstream scalar is not baked into PCM.

## Old-to-new assertion mapping

All 37 AudioTrack.test.tsx test declarations remain (the two renamed declarations retain their behavior domains); lifecycle tests were not deleted or inverted.

| Reviewed old assertion/test | Candidate replacement and evidence |
| --- | --- |
| compares trimmed, sped audio fades with the public envelope: trim/rate, authored clock through occurrence bound, mute | Prepared URL + numeric scalar + native trim/rate assertions in the same test; actual source-clock/Blob evidence in continuousPCM.lifetime.test.tsx “bakes the full …” and “keeps the original child source clock …” |
| matches the public envelope at every frame fade-case matrix | Numeric downstream scalar/source admission in the same parameterized cases; public envelope boundary/multiply assertions retained as audioEnvelopeAt owner checks; actual continuous PCM and between-frame-vs-step-hold proof in lifetime “bakes the full …” |
| Fixed authored music boundaries; overlapping ramps | Same named tests retain every boundary/multiply value against the public compiled envelope; actual consumer WAV bytes are checked in lifetime tests |
| Unsupported fade, invalid speed, authored curve, authored envelope, semantic recompilation | Plain-gain fallback, public curve/envelope compilation, remount/source-identity assertions retained; source-clock speed sanitation is covered by the 18 direct helper tests |
| Export fade behavior and volume-function identity | Constant export scalar plus prepared source; prepared source identity across equivalent re-render replaces callback identity |
| Boost/nested boost, mute/zero/half gain, threshold remount, occurrence-bound boost | Web Audio/cross-origin, downstream scalar, remount, native trim/rate, and authored-window assertions retained; lifetime covers prepared gain, mute, boost, export, and bounded window |
| Existing loading/lifecycle tests: premount, readiness, hold, progress, retry/backoff/give-up, failure chrome, recovery, source-change and timing remount | Same declarations and original lifecycle assertions remain; continuousPCM.lifetime.test.tsx adds fetch/decode failure, hold, stale completion, retry, abort, context close, and URL revoke coverage |
| TimelineComposition.media-conformance.test.tsx callback-clock test | Renamed to “keeps native media clock separate from the PCM owner scalar”; Remotion elapsed/local clock assertions remain |
| Media conformance audio fade/envelope/admission matrix | Both public and App endpoints now assert the admitted prepared source, no callback, native trim/rate, and one scalar gain; actual Blob-WAV consumer proof is in the lifetime suite |

The old callback-valued audio assertions are intentionally obsolete under the settled continuous-PCM policy. They were replaced by the owner’s public envelope semantics plus actual consumer Blob evidence; no distinct lifecycle behavior was changed to refusal or removed.

## Fresh controls and exact results

All tests used a private overlay at /tmp/app-public13-pcm-independent-review.IVYT1S, extracted from the immutable archive, over read-only shared dependencies. Vitest used --no-cache --configLoader=runner --maxWorkers=1 --no-file-parallelism and the overlay’s private cache directory.

For the commands below: V=/tmp/app-public13-pcm-independent-review.IVYT1S/node_modules/vitest/vitest.mjs; OV=/tmp/app-public13-pcm-independent-review.IVYT1S; RED=/tmp/app-public13-pcm-independent-red.iQTFvo; MUT=/tmp/app-public13-pcm-independent-mutant.Fyk2nk.

Green affected controls:

    node "$V" run --no-cache --configLoader=runner --maxWorkers=1 --no-file-parallelism \
      --config "$OV/vitest.config.mjs" \
      src/tools/video-editor/compositions/compiledAudioSourceClock.test.ts \
      src/tools/video-editor/compositions/continuousPCM.contract.test.tsx \
      src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx \
      src/tools/video-editor/compositions/AudioTrack.test.tsx \
      src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx
    # 5 files, 132 tests passed

The actual consumer Blob-WAV tests include full-channel byte equality, IEEE-float WAV metadata, continuous sample-vs-frame-step discrimination, mute/boost/scalar behavior, occurrence-window behavior, export admission, stale completion, abort, retry, hold, context close, and owned URL revoke.

Required public13 RED control, in an isolated copy with the consumer admission/preparation branch replaced by the reviewed parent implementation:

    node "$V" run --no-cache --configLoader=runner --maxWorkers=1 --no-file-parallelism \
      --config "$RED/vitest.config.mjs" \
      "$RED/src/tools/video-editor/compositions/compiledAudioSourceClock.test.ts" \
      "$RED/src/tools/video-editor/compositions/continuousPCM.contract.test.tsx" \
      --testNamePattern='^(?!.*retries).*$'
    # 19 passed, 5 failed, 1 skipped
    # failures: matching prepared positive plus four exact admission negatives

The candidate’s added corrected-record retry test also fails under the consumer-off mutation (6 failures total when included); it passes in the restored candidate.

Actual consumer planted-negative:

    # isolated candidate copy with sourceFrom changed from
    # compiledAudioSourceClock(clip, fps).source_from to raw clip.from (0.05)
    node "$V" run --no-cache --configLoader=runner --maxWorkers=1 --no-file-parallelism \
      --config "$MUT/vitest.config.mjs" \
      "$MUT/src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx" \
      --testNamePattern='bakes the full'
    # 2 failed (44100 Hz and 48000 Hz); WAV byte-equality assertion returned false

Restoring the caller passes those lifetime positives in the green 132-test run. This is actual consumer Blob-WAV evidence, not a public-math-only test.

git diff --check passed. The review worktree remained product-clean; no product file was edited by this review.

## Limits

Not run or claimed: full suite, browser/e2e, build, project TypeScript check, live sockets, install/network, frame/audio parity, current integration pin, current-root release qualification, or owner-film review. No parity or production qualification claim is made here. The available worker handoff’s detailed flatdesign file was missing; this report is reconstructed evidence.

