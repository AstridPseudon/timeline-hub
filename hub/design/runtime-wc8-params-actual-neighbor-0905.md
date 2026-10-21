# Runtime WC8 retained opaque parameter actual-neighbor

This is the Agent-side bounded actual-proof design/result for the retained opaque parameter-cell family.

## Product boundary

The approved product is Agent commit `c0671afddb34f4fe6b8ca66f511df9fc530cc344`, on the existing retained author-time path. Runtime remains current `b92d3e7a05eec65c142294ef4873edd059e9b31d` with published source `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, all 76 contract artifacts, ordinary `6ba7b51e`, and Composition C13 / 0.0.13.

The existing detached view grammar carries an existing opaque parameter as a JSON token. It carries a JSON null and a renamed JSON value. It does not encode omission as an explicit clear, so the proof intentionally does not claim opaque clear behavior.

## Case shape

The case uses the existing detached historical fixture and normal generated HTTP/door path. It retains the original bundle and publication basis, changes only the existing card opaque cell to null, commits one `clip.set-params`, reloads, and checks exact inverse/redo. It then makes a fresh retained export from the accepted null head, renames the same opaque JSON cell, commits with the new retained basis, reloads, and checks inverse/redo. The original first `NativeSheet` is finally used with its native text against the later session to prove stale original-basis refusal before any outbox or HTTP write.

The test preserves target owner/source, parameter order, sibling occurrence, and existing refusal behavior. It changes no production code and no live caller.

## Evidence and disposition

The independent data-safety review `rt-m2-wc8-params-safety-review-0903` returned **APPROVE** and confirmed basis retention, exact provider validation, opaque preservation, null/clear/rename behavior where representable, and no guard refresh or draft loss.

The no-socket neighbors passed 18 tests. The one allowed central run reached the actual Runtime path through the null and rename commits plus inverse/redo, then failed only because the stale witness supplied detached legacy text to `NativeSheet.apply`. The final source now supplies `native.text` and matches the exact stale-basis error, but central qualification remains unverified because no second run is permitted.

This is source/integration test scope only. It is not a whole WC8 result, a deletion claim, or a claim that any App/Runtime live caller changed.

