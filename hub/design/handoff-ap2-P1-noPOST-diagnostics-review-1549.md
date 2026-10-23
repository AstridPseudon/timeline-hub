# Handoff — ap2-P1-noPOST-diagnostics-review-1549

**FAIL** on reviewed HEAD `6dc8f4c5f52f9ecd72030bccc5fcae63db41dd2e`
(tree `83932d0ac2520138a259123deab660fad4341b51`) against base `6759fcacd`.

The original P1 body from the first test declaration through EOF is byteexact
to base (SHA-256
`582dc8fbc3cdf1991b981dce969e3981b63484b70aaeb70f331d907f5b2fc9bd`), and
the six pure safety tests, three TypeScript configs, exact three-file ESLint,
two-test Playwright listing, and committed diff check all passed. The causal
diagnostic filename requested by the brief is absent, so it was not run.

The required priority guarantee is not met: a large `basis.reads` value causes
`formatPriorityDiagnostic` to emit only `priority_over_budget`, losing basis,
head, outbox, UI, and error state. The new oversized-readonly test array is
never passed to the formatter/caller, and the real caller performs verbose
readonly/commit redaction before calling the priority logger. Rework the
priority selection/caller and add meaningful caller-path coverage before a new
review. No worktree edits were made.
