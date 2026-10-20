# Unapplied App continuous PCM unit

Port `consumer.patch` to the App owner’s current cohort after its normal public13 pin/lock adoption. This Composition repository does not activate or ship these files. The patch changes only App `AudioTrack.tsx` (+110/−34, net +76 product lines) and adds two direct test files. `AudioTrack.tsx` here is the complete proposed App leaf, extracted from `b1ef4b9b910ba72375c34cf319692f90d22edc25`.

The public compiler/admission/trim/rate/apply/WAV own semantics. The existing PreviewAudio attempt owns fetch/decode/abort/URL lifetime, readiness and retry. No new shared hook, decoder service, store, authority field, compiler, root or package change. Prepared sources bypass local decoding after public admission. Ordinary envelope sources become full-source float WAV; native trim/rate and the constant track×clip gain apply once downstream. An export with an envelope still requires its existing attempt-served prepared source.

`continuousPCM.contract.test.tsx`, `compiledAudioSourceClock.test.ts` and its helper are byte-identical to the prior consumer handoff. Only the first goes into the App patch; the clock helper/tests remain offline contract support. `continuousPCM.lifetime.test.tsx` adds 18 direct cases. The patch ports 24 tests; the offline run totals 42 including the 18 preserved public clock cases.

Run `python proposals/app-continuous-pcm13/stage.py`, then `node proposals/app-continuous-pcm13/stage.mjs`. The scripts read eight App files at the exact SHA, extract only required declarations, unpack the verified public13 leaf inside this worker’s fixture and borrow unchanged dependency leaves read-only. `PCM_BASELINE=1 node .../stage.mjs` selects the unchanged App leaf for the five required REDs. Vite needs one public-export alias because this repository itself has the Composition package name; its target is resolved through public13’s actual export map, never a private chunk.

Full results, exact commands, adoption order and remaining limits are in the flat handoff report. Neither App installation nor real media playback/rendering is qualified here.
