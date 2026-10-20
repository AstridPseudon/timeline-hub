Product tree: unchanged App 0ea988bdd2907c876b82fd2620820e3fb6d6ea84. Exact patch is empty.

| Test / probe | Outcome | Meaning |
| --- | --- | --- |
| Existing AudioTrack.test.tsx + RemotionPreview.audioFailure.test.tsx + TimelineComposition.media-conformance.test.tsx | 91 pass; exit 0 | Existing readiness, bounded retry, hold, gain, failure handling and both renderer wiring remain baseline green. Existing public prepared-source positive is present. These still test historical App frame callbacks, not continuous PCM. |
| compiledAudioSourceClock.test.ts | 18 pass | Unapplied clock adapter replay against clean public12: fractional .05 trims, rates 2/.5, 30/rational fps, full-source stereo float WAV byte equality, scalar/occurrence neutrality. Prior 9 raw-from-negative controls are retained in the original clock handoff, not rerun here. |
| continuousPCM.contract.test.tsx public apply/WAV test | 1 pass | Full-source real public apply/WAV bytes match independent literal 2/30 origin; no mocked public math. |
| continuousPCM.contract.test.tsx matching preparation | 1 fail | Prepared URL + constant 0.4 expected; original URL returned. |
| continuousPCM.contract.test.tsx wrong envelope / raw .05 origin / wrong rate / blob URL | 4 fail | Expected existing failure channel/refusal; original URL still mounts. |
| public-source-seam.mjs | exit 0, probe confirms missing seam | encodedEnvelopeSource and useAudioEnvelopeSource absent from both advertised modules; deep imports blocked with ERR_PACKAGE_PATH_NOT_EXPORTED. |

New red harnesses live outside product source and are also supplied as an UNAPPLIED test-only red-proposal.patch. No passing behavior test was edited, removed, skipped, xfailed or inverted. The old frame-table RED history and original clock handoff are untouched.
