# VW-AUDIO-STEP closure packet (UNAPPLIED ledger text)

The retired per-frame, step-held audio callback is physically absent from both
exact live sources. App frozen source `3ee1900621f5ae27450ce5b1b69a3b7987e4b8`
(tree `38d6f715f05d0c00b89e131c3b8d4ae28a57fd44`) uses full-source PCM/WAV
preparation through public `applyAudioEnvelope` and passes constant
`volume={baseVolume}`. Agent source `5c5173dcb57669a9d43e5add2674543333f1c6d2`
(tree `8626f868a3869b23baaca9814adb930e8952e4c7`) uses the live chain
`run.py:67-68 -> root_preparation.py:242-246 -> normal_audio.py:23-133 ->
normal-audio-sources.mjs:19-47 -> attempt-envelope-pcm.mjs:11-113` to prepare
full-source PCM, leaving only scalar gain downstream.

The exact Agent historical callback ancestry is `f042b16e1` (introduced the
frame-valued `volumeProp`) to `a3ca13cb2` (deleted it and switched to baked
source plus constant gain). The current Agent PCM replacement was introduced
by `9fd669e48`, ported/expanded by `2019d7e69`, and activated by `951e9f412`.
The App historical removal is `2e9939810`, with replacement tests in
`continuousPCM.contract.test.tsx` and `continuousPCM.lifetime.test.tsx`.
Active Agent replacement tests are `normal-audio-sources.test.mjs`,
`normal-audio-native-sources.test.mjs`, `test_normal_audio_sources.py`,
`test_normal_audio_run.py`, and `test_normal_audio_source_phase.py`.

Exact source scans found no old callback symbol in either live source. This
closes completed code retirement only; physical Gate 6 Player/export parity is
**OPEN**, with no qualification result ID available. Manager must apply or
edit this ledger text; this packet is **UNAPPLIED**.
