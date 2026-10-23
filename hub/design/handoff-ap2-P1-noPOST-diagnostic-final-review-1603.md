# Handoff — ap2-P1-noPOST-diagnostic-final-review-1603

PASS on current `0b3cef4d21610031049b2c8809089a730d0abfbe` (tree `2652d85a0ab40bcf0e88443f721dc4b868eeb743`), parent `e5ca2db05e3e96ebdfd2b843b1beb74be68116c2`.

The exact three current blobs match final donor `effc3fe1b55ee66afd376be1f82b6e69f90f7eec`; no `6dc`/`effc`/`1542` ancestry was borrowed. Only the three permitted files differ from the base, the required first-test-through-EOF SHA is `582dc8fbc3cdf1991b981dce969e3981b63484b70aaeb70f331d907f5b2fc9bd`, and both P1 test bodies are byte-identical.

The actual failure-diagnostic caller routes raw `basis.reads` through the priority seam. Compact causal basis/head/outbox/UI/error state survives oversized readonly input, while the original detailed packet and chain assertions remain unchanged. No material regression or security weakening found.

Checks: safety `6/6`; all three TypeScript configs; scoped ESLint; exact two-test listing; committed-range `git diff --check`; focused circular/UTF-8/oversized-label/large-input controls all PASS. No browser/body/full run was performed. Overall P1 remains NO-GO until the actual original mounted chain passes.
