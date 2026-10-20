# Viewing review — App public13 PCM owner candidate

## Decision

**Narrow REJECT for the exact owner gate candidate `35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a`.**

The public13 pin and the core PCM/admission policy are correct, but this
candidate is not equivalent to the reviewed/ repaired `2e9939810` consumer.
It removes an existing preparation-lifecycle behavior and drops the repaired
consumer-level PCM assertions for several audible groups. Source-only compiler
or prop-shape checks do not replace those assertions.

## Exact inputs

- Candidate: App `35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a`.
- Normal pin parent: `2b3c431fb0efb967c59662c50f5a5bd694f9157e`.
- Reviewed implementation: `2e9939810cbe600d1f7cfcf16d987e50bdecaaeb`.
- Repaired coverage reference: `70e378e3f780308628bd98b55405115d74288a48`.
- Composition archive: SHA256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`;
  77 unique safe regular tar members.

The candidate is rooted on the immutable pin: `package.json`,
`package-lock.json`, and the committed `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`
are unchanged from `2b3c431` and the lock selects version `0.0.13` with the
matching SHA512 integrity.

## Policy/source review

The candidate's `AudioTrack.tsx` uses only the approved public evaluation
surface: `compileAudioEnvelope`, `computeMediaTrim`, sanitized child rate,
`applyAudioEnvelope`, `audioEnvelopeWav`, and `encodedEnvelopeSource`.
The source clock is `computeMediaTrim(compiledChild, fps).trimBefore / fps`
with the sanitized child rate. Preparation applies the envelope once to all
decoded channels and emits a full-source IEEE-float WAV; native playback keeps
the occurrence trim, child rate, and constant track×clip gain. Prepared
positive admission and four forged negatives remain. Native no-envelope audio
and export-with-prepared-source/no-browser-decode remain covered.

The new `compiledAudioSourceClock` helper is a small public-API adapter and
does not introduce a second compiler or copied DSP. I found no private
Composition import or second envelope/gain/rate application.

## Blocking divergences

1. The candidate removes the prepared-source fetch's `response.body` reader,
   chunk collection, and `preparationProgress` hold renewal from
   `AudioTrack.tsx`; it replaces them with one `response.arrayBuffer()` call.
   It also deletes the corresponding “source chunks arrive before the native
   WAV element exists” lifecycle test. The existing hold contract says each
   received chunk renews the same hold and a slow request is not restarted.
   This is a behavior regression, not merely a shorter test.

2. Relative to repaired `70e378e3f`, `continuousPCM.lifetime.test.tsx` drops
   consumer-level PCM byte/sample assertions for invalid speeds, all six
   curves, overlap, exact fade boundaries, envelope/curve re-bakes, backend
   transitions, boosted fade frames, nested boost/minimum including silent
   PCM, and boosted occurrence samples. `AudioTrack.test.tsx` now contains
   source-only `audioEnvelopeAt` or native-prop checks for many of these; it
   does not prove the generated WAV bytes or the actual consumer's source-time
   mapping. The repaired 116-case evidence therefore cannot be reused for this
   changed candidate.

The detailed old-to-candidate mapping is in
`handoff-vw-m3-app-owner13-pcm-domain-review-mapping.md`.

## Evidence

Commands run:

```text
git -C /home/user/banodoco/reigh-app diff --check \
  2b3c431fb0efb967c59662c50f5a5bd694f9157e \
  35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a
# exit 0

# private extraction of the candidate's committed public13 archive, then a
# node --input-type=module probe against dist/evaluation.js
# result: six approved exports present; trim/rate pass; WAV pass;
# matching prepared positive pass; four forged negatives rejected (4/4)

git -C /home/user/banodoco/reigh-app show \
  35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a:src/tools/video-editor/compositions/AudioTrack.tsx \
  | rg 'applyAudioEnvelope|audioEnvelopeWav|compileAudioEnvelope|computeMediaTrim|encodedEnvelopeSource|response\\.body|getReader|preparationProgress'
# public API calls present; body/getReader/preparationProgress absent

git -C /home/user/banodoco/reigh-app diff \
  70e378e3f780308628bd98b55405115d74288a48 \
  35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a -- \
  src/tools/video-editor/compositions/AudioTrack.tsx \
  src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx
# confirms removal of chunk renewal and repaired consumer-level PCM groups
```

Attributable prior evidence: the repaired branch reported the exact five-file
public13 overlay at 116/116 and lifetime at 44/44, and the restored review
independently passed the requested repaired groups. Those results are not
candidate evidence after the candidate's source/test changes. No full suite,
browser, render, socket, install, typecheck, or physical parity run was made.

## Required next step

Restore the chunk-progress preparation behavior and its lifecycle assertion;
restore one-to-one consumer-level PCM byte/sample coverage for every dropped
group listed above; then rerun the exact five-file public13 lane on this
candidate's actual source/pin. Re-request the Viewing gate only after that
source and coverage repair. No Composition product files were changed here.
