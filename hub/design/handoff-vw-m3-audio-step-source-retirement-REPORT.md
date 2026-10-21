# vw-m3-audio-step-final-source-closure

## Result

The retired per-frame, step-held audio callback is physically absent from both
exact live sources. This packet makes no product or test change and applies no
deletion patch. Current PCM helpers remain in place.

This is code-retirement closure only. Physical Gate 6 (Player/export frame +
audio parity) is **OPEN**: no physical qualification result ID was available
to this worker, so none is claimed.

## Exact live sources

### App

- Frozen qualified source commit: `3ee1900621f5ae27450ce5b1b69a3b7987e4b8c8`
  (tree `38d6f715f05d0c00b89e131c3b8d4ae28a57fd44`).
- Production source:
  `src/tools/video-editor/compositions/AudioTrack.tsx`, blob
  `6d63e0808015f0349da1bbe44b8d14fcd72dc3bf` (SHA-256
  `8763ad48a69c520312115f112dd4329cf63fd23d6f4a4c477e2dccf4ccefad06`).
- Current replacement at lines 189–235 fetches and decodes the full source,
  applies the public `applyAudioEnvelope` to all PCM channels, and publishes a
  WAV Blob through the existing attempt lifetime. Lines 439–483 use the
  prepared source for render/preview and pass constant `volume={baseVolume}`.
- The historical App callback source was at commit
  `b1ef4b9b910ba72375c34cf319692f90d22edc25`, blob
  `631192fea2ee9eab1a62fe99b7015ca0f85aed99`; its removal/replacement is
  `2e9939810cbe600d1f7cfcf16d987e50bdecaaeb` (`feat(app): use continuous PCM
  audio consumer`). The replacement `AudioTrack.tsx` blob is
  `9de8d0b6eff36e4fb9ff3c449c5fae148b154678`.
- Exact production-source scan at the frozen source returned no matches for
  `getAudioFade`, `getAudioVolumeProp`, `useAudioEnvelope`,
  `useFrameForVolumeProp`, `frameOffset`, `audioEnvelopeAt`, or the old
  frame-valued `volume` type. The two `useFrameForVolumeProp` matches noted in
  the prior map are test instrumentation only, not `AudioTrack.tsx`.

### Agent

- Current source commit: `5c5173dcb57669a9d43e5add2674543333f1c6d2`, tree
  `8626f868a3869b23baaca9814adb930e8952e4c7`.
- Live caller chain:
  `astrid/packs/rendering/rendering/renderers/remotion/run.py:67-68` imports
  `prepare_normal_audio_sources`; `root_preparation.py:242-246` calls it for
  the normal export; `normal_audio.py:23-133` validates the managed source,
  invokes the helper, and attaches attempt-local WAV metadata;
  `remotion/normal-audio-sources.mjs:19-47` translates retained clocks and
  invokes the PCM helper; `remotion/attempt-envelope-pcm.mjs:11-113` decodes
  the full source, applies the public envelope per sample, and writes WAV.
- Current source blobs:
  `run.py` `6ce24f9e5fbe3dc31d3b5b1579f8b06301a8f88`,
  `root_preparation.py` `017227e930f3ae5017f96f2ff69c1aca6f18f5be`,
  `normal_audio.py` `68f49d42fbebbf54db12aaac21eed8211d6b5011`,
  `normal-audio-sources.mjs` `c4f16ff61efafd1960d50e21ef84ff237a68afd7`,
  `attempt-envelope-pcm.mjs` `4c99b9e6efd3178a04cb57daf3c810ad6fa68c64`,
  `compiled-audio-source-clock.mjs`
  `badc39f4257a8e4409e8080facdb251513904414`.
- Exact current Agent scan over the live normal-audio source/helper/test scope
  returned no old callback symbols. The only `useAudioEnvelopeSource` text is
  a negative package-boundary assertion in
  `tests/packs/rendering/test_composition_package.py:90`; it is not a live
  consumer.

## Agent introduction/removal ancestry

The exact Agent analogue to the known App removal is in the historical
vendored Composition source:

1. `f042b16e14628dec445f9f7ab111adf3eda8f49c` (`Consume admitted Composition
   EVAL source in Astrid renderer`) introduced
   `remotion/vendor/timeline-composition/typescript/src/AudioTrack.tsx` with
   the per-frame `volumeProp` callback (blob
   `6526e4db03b45180e2259e273d8a9559f55758dd`).
2. `a3ca13cb25ff440288453bc25d82bbf35f2e3700` (`Repin Astrid Remotion to
   Composition 0.0.7 artifact`) is the exact removal diff: it deletes
   `toFiniteSeconds`, `fadeInFrames`, `fadeOutFrames`, `durationFrames`, and
   the frame-valued `volumeProp`; imports `useAudioEnvelopeSource`; passes the
   baked source and constant `volume={baseVolume}`. The resulting source blob
   is `0d9f029cf187bcf5ebdff7c03bb8327a9b32128e`, and the helper blob is
   `ae1865bcfd90e206d1f50500a99c44e31b2395ef`.
3. The current Agent replacement is the full-source PCM path, introduced as
   inactive preparation by `9fd669e48` (source plus
   `remotion/tests/normal-audio-sources.test.mjs` and
   `tests/packs/rendering/test_normal_audio_sources.py`), ported/expanded by
   `2019d7e69` (including native-source tests), and activated at the live
   caller by `951e9f412` (including `test_normal_audio_http.py` and
   `test_normal_audio_run.py`).

## Named active replacement tests

Existing qualified results are reused; no tests were replayed for this packet.

- App `continuousPCM.lifetime.test.tsx`: full-source bake once with native
  trim/rate and constant scalar; between-frame sample distinction from the
  retired step table; invalid-speed, all curve forms, fade boundaries,
  overlap, retry, cleanup, and export cases.
- App `continuousPCM.contract.test.tsx`: exact public full-source PCM/WAV
  positive, matching prepared source with constant gain, forged prepared
  source refusal, and corrected retry after refusal.
- Agent `remotion/tests/normal-audio-sources.test.mjs`: distinct source bytes
  for equal envelope/clock, recursive phase translation, forged/double-apply
  refusal, and failed-batch cleanup.
- Agent `remotion/tests/normal-audio-native-sources.test.mjs`: gapless MP3,
  rational trim/child speed, unknown-origin controls, and full stereo source
  beyond 64 MiB.
- Agent `tests/packs/rendering/test_normal_audio_sources.py`: full stereo WAV
  and exact compiler clock, internal original-clip phase seam, required
  original compiled-clip transport, and exact asset-key-to-managed-byte
  binding.
- Agent `tests/packs/rendering/test_normal_audio_run.py`: constant-gain
  caller, lifetime/cleanup, digest and decode refusals, and non-audio path
  preservation.
- Agent `tests/packs/rendering/test_normal_audio_source_phase.py`: host-owned
  slice phase and PCM equality against the original attempt WAV.

## Proposed replacement ledger evidence (UNAPPLIED)

> **UNAPPLIED — manager only:** At Agent `5c5173dcb57669a9d43e5add2674543333f1c6d2`
> (tree `8626f868a3869b23baaca9814adb930e8952e4c7`) and App frozen source
> `3ee1900621f5ae27450ce5b1b69a3b7987e4b8c8` (tree
> `38d6f715f05d0c00b89e131c3b8d4ae28a57fd44`), the retired per-frame,
> step-held audio callback is physically absent from both exact live sources.
> App `AudioTrack.tsx` consumes full-source PCM/WAV via `applyAudioEnvelope`
> and uses constant `baseVolume`; Agent's live export chain is
> `run.py:67-68 -> root_preparation.py:242-246 -> normal_audio.py:23-133 ->
> normal-audio-sources.mjs:19-47 -> attempt-envelope-pcm.mjs:11-113`, which
> prepares full-source PCM and leaves only scalar gain downstream. Exact
> source scans found no `getAudioFade`, `getAudioVolumeProp`,
> `useAudioEnvelope`, `useFrameForVolumeProp`, `frameOffset`,
> `audioEnvelopeAt`, or old frame-valued `volume` callback in either live
> source. The historical Agent introduction/removal is `f042b16e1 ->
> a3ca13cb2`; the App removal is `2e9939810`. Active replacement tests are
> the App `continuousPCM.contract.test.tsx` and
> `continuousPCM.lifetime.test.tsx`, plus Agent
> `normal-audio-sources.test.mjs`, `normal-audio-native-sources.test.mjs`,
> `test_normal_audio_sources.py`, `test_normal_audio_run.py`, and
> `test_normal_audio_source_phase.py`. This closes code retirement only;
> physical Gate 6 qualification remains OPEN (no result ID supplied).

## Commands and limits

Read-only evidence commands completed:

```text
git show/diff f042b16e1..a3ca13cb2 -- remotion/vendor/timeline-composition/typescript/src/AudioTrack.tsx
git show --name-status 9fd669e48 2019d7e69 951e9f412 -- remotion astrid/packs/rendering/rendering/renderers/remotion tests/packs/rendering
git rev-parse HEAD:<live source/test path>
git grep -n -i -E '<old callback symbols>' HEAD -- <Agent live scope>
git -C /home/user/banodoco/reigh-app show 3ee1900621f...:<App AudioTrack.tsx>
git -C /home/user/banodoco/reigh-app show 2e9939810cbe... -- <App source/tests>
git status --short
git diff --check
```

`git status --short` was clean before packet files were written and
`git diff --check` passed. No test command, browser, renderer/export replay,
physical parity run, dependency install, shared-graph write, or Gate 6
qualification was performed.
