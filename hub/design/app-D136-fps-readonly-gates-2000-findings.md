# D136 findings

1. The receiving source is pristine except for the approved projection test
   receive at `3082cad490ce1cee764ff137f99cb791a67ddd08`; no source edit was
   made by this worker.
2. The historical D100 result remains `27/27 PASS` for the independent lane and
   `9 setupERROR` for the authored projection lane. No nine-selector body ran in
   this review.
3. The receiving provider's typed FPS rule is decisive locally: scalar or exact
   positive `{numerator, denominator}` only. The authored `[30000, 1001]` is not
   an opaque field.
4. The captured pristine upstream public schema does not reject the list because
   `ThemeOverrides.visual` is open. The corresponding public validator ignores
   the non-scalar value for its transition-check FPS and uses `30.0`.
5. This is the D54a regression condition: upstream accepts/does not reject the
   list while receiving Agent rejects it. The proper owner is Runtime/Agent;
   fixture conversion is forbidden in this result.
6. G1 remains NOTQUALIFIED until the lead supplies current-tip provenance and an
   exact path census. The local absence proof is not promoted to actual-tip proof.
7. The 43 original predicates, 11 test bodies and 54 fixture statements remain
   conserved by the protected AST record. No predicate depends on traversing the
   old array shape; the array only blocks provider setup before the nine bodies.

No additional invalid authored value is asserted because the conditional whole
seed schema census was stopped by the gate outcome. No value was changed.
