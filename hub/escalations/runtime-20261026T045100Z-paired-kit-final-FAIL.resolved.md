Resolved by main 2026-10-26T04:50:51Z.
- D141s (04:50Z 26 Oct): disposition of the paired App kit FAIL (review 0435). ONE last bounded round, then it is dropped.
  1. **One author** (Luna; Sol only if the reaping question is HARD) PORTS the already-qualified lifecycle controls from the Runtime kit 56f2d56e: the actual mounted stop-test semantics, the frozen-sampler 125 bound, and the timeout-child reaping ownership as 56f2 resolved it. They go into the paired composition 06fb2b5d unchanged in meaning. No new mechanism. It binds to App's freeze-2 builder output once App publishes it, never the historical 520d binding.
  2. **One independent review**, all findings in one pass, against 0435's findings file plus 56f2's 49 controls. The author and reviewer run the same script.
  3. **Time-box 06:00Z.** If it isn't PASS_INSTALL by then, the paired kit is DROPPED. App's journeys then run under the normal floors (D89/D141g without the pair exception), waiting for headroom: the owner's hub-repack approval (owner-ask 0450Z) or natural growth. No further rounds, no other route.
  4. The qualified Runtime kit 56f2 and Runtime's work (targeted-15, P5) are unaffected.
