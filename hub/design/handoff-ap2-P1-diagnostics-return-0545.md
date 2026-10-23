# Handoff: ap2-P1-diagnostics-return-0545

Status: **source checks PASS; live diagnosis remains UNVERIFIED pending independent review and one new existing-service run**.

## Change

On App source parent `f7f45ad0babfa6cb6e17070182c7021adef20587` (tree `f2dcc578601b724fb8dc8400488c19ca3a844e9e`), the one assigned spec now uses a structural diagnostic allowlist. It does not serialize arbitrary outbox IDs, bases, request keys, bodies, headers, cookies, auth, URL queries/paths, console/pageerror text, alerts, or UI text. It records only bounded owner/intents/pending lengths, fixed outcome/state labels, booleans, fixed error classifications/counts, and numeric statuses with fixed method/route templates. Routes cover the real three-products prefixes `/api/runtime`, `/api/astrid`, and `/runtime-config` without dynamic path data.

The original accepted/merged/lost-ack/restart/retry and refusal/rollback P1 bodies/assertions are unchanged; exact comparison of the source after `// Source proof only:` passes. No product, fixture, support, generated, lock, pin, suite, or launcher change was made.

Working file SHA-256: `956aaf219aae927d23a4f13e0ce8b0e358fe235508454fe70b0c6ad6ed84eb8c`.
Working binary diff SHA-256: `d055ce93f1adc23d882732b78ecc897710a444779d32c42300158dc410485de5`.
PLAN SHA-256: `bdff6fbea3f6021af1f739eaff0c91650f90a17c34dccb62fb76d120eceb5075`.
Unchanged private graph/spec pin: `sha256:819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
Final commit SHA is pending the harness commit.

## Validation

- `npm exec tsc -- --project tsconfig.app.json --noEmit` — PASS.
- `npm exec tsc -- --project tsconfig.node.json --noEmit` — PASS.
- `npx eslint tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0` — PASS.
- `npx playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts --list` — PASS, exact 2 tests.
- `git diff --check` — PASS.
- Offline allowlist witness using quoted/unquoted secret-shaped arbitrary message/key/body/path inputs — PASS; no input secret appeared in output.

No HTTP/socket/browser/body/build/full/service run was performed. Do not infer P1/H3 behavioral credit from these source checks. After independent PASS, manager should run the original existing service once and inspect the new safe failure-state line; do not rerun an unchanged known-red source.
