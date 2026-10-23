# Handoff — ap2-P1-noPOST-diagnostic-budget-1542

The App P1 failure capture now emits a compact priority diagnostic before the
unchanged detailed traffic packet. The priority line carries existing basis,
displayed-head, outbox summary, UI, and error state, so a large readonly reply
cannot consume the only diagnostic budget before causal state is logged.

`formatPriorityDiagnostic` keeps the existing 16 KiB cap, redaction, UTF-8
measurement, parseable JSON payload, and guarded logging. The old
`formatDiagnostic` path and detailed packet remain intact for evidence.

Focused safety tests, scoped ESLint, root/app/node TypeScript checks, and
`git diff --check` pass. The central targeted app request was not applicable to
these `tests/e2e` files because that service's targeted Vitest configuration
only includes `src/**/*.test.{ts,tsx}`; no browser/live-harness run was made.

The original P1 case body from the first test declaration through EOF is byte
identical to base `6759fcacd`, SHA-256
`582dc8fbc3cdf1991b981dce969e3981b63484b70aaeb70f331d907f5b2fc9bd`.
