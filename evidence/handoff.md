# D141p receiving handoff

`NOT_READY`: this packet is ready to receive a genuine freeze-2 source tuple and regenerate the paired production binding, but it is not a final binding and contains no proof result.

## Must arrive before the caller runs

- Qualified App freeze-2 full commit/tree after the `d822d2f5…` merge-forward, independent review, and source-worker-only manifest regeneration.
- Qualified Agent freeze-2 producer full commit/tree and receipt, with the merge-forward-first decision honored.
- Exact Runtime and Composition identities, detached clean checkouts, parent/origin/source manifests, and all required checkout receipts.
- Installed Runtime paired-kit receipt, source/review/CAS hashes, and supported admission/trace API.
- Fresh paired admission at `>=4.6 GB`, continuous 5-second `KEEP` trace, 4 GB stop, and one-heavy reservation.
- Final D66 builder outputs for each requested selector: exact command bytes, no-newline command hash, one-LF row bytes/hash, and the registered-byte comparison before either part.
- Final authorization and any P4 path-applicability decision against the existing 0226 map.

The exact immutable source values are intentionally null where the final App and Agent heads are unknown. Do not fill them from candidate `8f278b91…`, App `520d7e4f…`, or Agent `28e56cac…`.

## Caller sequence

Use the existing D66 `--submit`/`request-test`/`wait-test` path only. Register and compare the pair, run preflight first, then normal. Execute placement first, then the other five P2 selectors, then P1 and P3. Keep P1’s original split → trim-new-clip → intervening Agent edit → lost-ack/restart chain and accepted/merged/refused outcomes. Keep all eight original selector blobs, C0 v2 request/reply fields, history/reload/guarded-undo checks, raw/private `KEEP` outputs, and zero legacy traffic.

Popup ADD retains D141j wording: PASS is `NOT REPRODUCED`, cause undetermined; FAIL is preserved and stops popup, with no collector now. SWAP/Element and all named out-of-scope investigations remain excluded. Existing old rows `18617` and `19479` are unchanged.

P4 is only checked for freeze-2 source-path applicability; there is no duplicate P4/P5 body. Unit-service work follows controller 0043: one new full per head, exact `npm test` script, and standalone `npm run test:node` on each head if Vitest short-circuits.
