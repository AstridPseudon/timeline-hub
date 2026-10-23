# Handoff — ap2-P1-noPOST-diagnostic-return-1553

PASS on source HEAD `6dc8f4c5f52f9ecd72030bccc5fcae63db41dd2e`, reviewed tree
`83932d0ac2520138a259123deab660fad4341b51`, base `6759fcacd`.

The formatter now projects recognized priority state before JSON serialization.
Large basis reads are summarized with count/summarized/truncated metadata rather
than consuming the 16 KiB line budget, and the production caller sends the raw
reads through that same priority seam. Causal basis/head/outbox/UI/error state
survives; detailed packet behavior and all original P1 body bytes are retained.

Pure diagnostics are 6/6; exact three-file ESLint, all three TypeScript configs,
exact two-test Playwright listing, and base-to-working-tree `git diff --check`
pass. The original body hash is unchanged at
`582dc8fbc3cdf1991b981dce969e3981b63484b70aaeb70f331d907f5b2fc9bd`.

No causal diagnostics test file exists in this base, so there is no causal test
run beyond the existing safety suite. Browser/live harness and full suites were
not run. The worktree delta is confined to the three allowed diagnostic files;
the harness may now commit it using the assigned commit message.
