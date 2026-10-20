# App public13 candidate coverage mapping

Reference: repaired `70e378e3f780308628bd98b55405115d74288a48`; candidate:
`35e3ebdf2ca74a6a1bbdb1486d503b7f5b3c744a`.

| Repaired consumer-level assertion | Candidate state | Review |
| --- | --- | --- |
| Invalid speed `0/-1/NaN` applied to generated PCM | `AudioTrack.test.tsx` only renders and checks native volume; helper test checks sanitizer in isolation | Missing consumer PCM |
| Six interpolation curves | `AudioTrack.test.tsx` checks native/Web Audio props; no generated WAV samples | Missing consumer PCM |
| Overlap and exact fade boundary samples | `audioEnvelopeAt` source checks exist, but no generated WAV/source-sample assertions | Missing consumer PCM |
| Unsupported native fade inputs | Native finite-gain path remains represented; no issue found for this narrow native behavior | Retained only at source/prop level |
| Authored envelope precedence and semantic curve/envelope re-bake | Candidate checks source identity/fetch/remount shape; exact output samples removed | Partial; restore PCM oracle |
| Four nested multiply/minimum boost forms | Candidate checks Web Audio admission props | Missing baked PCM matrix |
| Nested boost silenced by minimum | Candidate checks Web Audio admission only | Missing silent PCM assertion |
| Native ↔ prepared transitions and readiness | Candidate retains transition/readiness controls and lifetime stale/retry tests | Mostly retained; verify after repair |
| Boosted fade frames below unity | Candidate checks Web Audio and constant volume; no baked samples | Missing consumer PCM |
| Boosted occurrence with trim/speed/bounds | Candidate checks sequence/native props; non-boosted window has one WAV check | Missing boosted occurrence samples |
| Preparation chunks renew the same hold | Candidate removes reader/progress callback in source and removes the test | Behavior regression |

The candidate still retains the public full-source WAV positive, matching
prepared positive, four forged negatives, constant downstream gain/rate,
native no-envelope behavior, export no-decode, abort/stale/close/revoke,
retry, premount, starvation bound, and ordinary native lifecycle tests. Those
retained positives do not cover the removed matrix or chunk-renewal behavior.
