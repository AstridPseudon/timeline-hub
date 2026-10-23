# Handoff: P3 D28 mounted-readiness preflight

Added only `tests/e2e/local/three-products.mounted-readiness.spec.ts`.

It reuses the real App support fixture/helpers, defers timeline initialization, seeds the full native three-products fixture, reads the scoped outbox before page load, verifies the production hosted editor is connected and showing the seeded project/timeline, then waits up to the original 90-second ceiling for a fresh settled scoped owner and verifies connected again. It has no gesture or commit body and does not import or execute any original journey.

Diagnostics are bounded valid JSON in `testInfo.outputPath`, with only allowlisted endpoint/status/outbox/selection/error projections. The original Playwright assertion is rethrown unchanged. No old P1/P2/P3 spec, support, config, product, kit, env, or suite file changed.

Static evidence passed: targeted ESLint, root/app/node TypeScript no-emit, `git diff --check`, and Playwright `--list` (new leaf exactly one; original P1 two, P2 eight, Gate 5 one). No browser or live service run was performed, so runtime mounted readiness remains unverified until Farm applies the report-only suffix after the unchanged native/history prefix.

See the worker report for the exact proposed Farm output carrier/invocation, source/blob identities, protected body hashes, and retained-evidence limitations.
