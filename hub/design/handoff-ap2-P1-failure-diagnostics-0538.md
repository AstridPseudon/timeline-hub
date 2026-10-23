# Handoff: P1 failure diagnostics

Status: **source checks PASS; live diagnosis UNVERIFIED**.

Worker `ap2-P1-failure-diagnostics-0539` started at App base `ec8e8a25cf7ac29247d06bc5a224b94145ee71c3` (tree `25140dfd23eeea6e731a4168fce10fa4bff87d8f`). It changed only `tests/e2e/local/three-products.p1-chain.spec.ts`.

The source preserves both original P1 tests and all original positive/refusal/readiness assertions. `openChain` now installs failure-only diagnostics and, if its existing navigation/connection/first-track/idle wait fails, emits one `[P1 openChain diagnostics]` JSON line to stdout. It observes only:

- the existing timeline-filtered `astrid.command-outbox` owners store shape, summarized without request bodies;
- owner/generation/intent IDs and bases, pending method/path/key/outcome, and accepted head;
- selected timeline text, connection state/text, targeted recovery/timeline error UI, and visible alerts;
- runtime response method/path/status with no URL query strings;
- bounded page errors and console errors with URL/query, bearer, credential-like, and JWT redaction.

It does not read credentials, cookies, auth headers, request bodies, broad localStorage, or alter control flow, waits, routes, fixtures, assertions, outcomes, ports, sessions, executors, guards, or suite configuration. The diagnostics are intentionally stdout-first because service snapshots/error context may be removed.

Hashes:

- Base target SHA-256: `926cdadd0370f0648e03b4bba743b56c1e7c80f0ff3fa1887ba985e9bc772fd1`
- Current target SHA-256: `e673cad227dba0957088aa88fc764de7fff3951eff91fab7132d3f0929fdc1ad`
- Current diff: one file, `104 insertions(+), 4 deletions(-)`; the four deletions are only the wrapped original `openChain` lines.

Validation:

- `npm exec tsc -- --noEmit` — PASS
- `npx eslint tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0` — PASS
- `npx playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts --list` — PASS, exact 2 tests
- `git diff --check` — PASS

No browser, HTTP/socket, build, service, or full-suite execution was performed. This is not an H3/P1 behavioral qualification. Independent review should verify the bounded redaction and source-only diff; after approval, run exactly one original existing service retry and inspect the persistent stdout line for owner-vs-pending/intents, selected timeline, load/basis/session error, and runtime path/status evidence.
