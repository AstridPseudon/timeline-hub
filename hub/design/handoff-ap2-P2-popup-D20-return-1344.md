# Handoff: ap2-P2-popup-D20-return-1344

SOURCE_PASS: PASS for the bounded one-file P2 fixture return. Only `tests/e2e/local/three-products.p2-popup.spec.ts` changed from App base `4282d776497f651bce3870d1d9e6a37a5eaa2030`.

The exact donor fixture blob was imported, then corrected only to remove the child payload clone and invented `reads: []`. `runtimeJson` was checked directly and supplies a fresh `Idempotency-Key` on non-GET requests. The native fixture retains shared physical source topology, genuine Runtime media IDs, exact `on: 12` / 12000 ms placement, guarded authored patch, opaque/null/absence values, and unchanged mounted ADD/SWAP gesture tail (`2eda7eb8fe2fa77ed69195f471ecf5d6d46736bed012cbd78035c5487e5e35cb`).

Scoped ESLint, App/Node TypeScript, Playwright `--list` (exactly 2), offline source/invariant checks, diff-check, retired-route inventory, and LF EOF checks pass. No browser, HTTP/live Runtime, service, full suite, build, dependency install, or body qualification was run. The central integration run must still qualify the actual Runtime fixture commits and mounted gestures.
