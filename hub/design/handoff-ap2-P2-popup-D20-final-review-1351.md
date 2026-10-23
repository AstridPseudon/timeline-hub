# Handoff: ap2-P2-popup-D20-final-review-1351

NO-WEAKENING PASS. Exact `791a1a8a5` reviewed against App base
`4282d776497f651bce3870d1d9e6a37a5eaa2030`; only
`tests/e2e/local/three-products.p2-popup.spec.ts` changes.

The setup now uses authenticated public `occurrence.place-shared` followed by
guarded atomic `doc.patch`, preserving exact source topology, 12000 ms
placement, original target/raw-registry present/absent assumptions, real media
identity, opaque/null/absence coverage, and exact base chaining. No physical
clone or retired publication path remains; request `reads` is omitted rather
than invented. The mounted gesture tail is byte-exact with mandated SHA-256
`2eda7eb8fe2fa77ed69195f471ecf5d6d46736bed012cbd78035c5487e5e35cb`.

Scoped ESLint, App/Node TypeScript, Playwright discovery (exactly 2), offline
envelope/invariant scan, changed-path audit, and `git diff --check` passed.
`runtimeJson` supplies a per-request UUID `Idempotency-Key`; retry-stable
idempotency and actual Runtime/browser behavior were not qualified here.

Source readiness only: no HTTP/live Runtime, browser, service, full suite,
native, or original P1/P2/P3 run. Central integration remains required.
