# Handoff: ap2-P1-D13 oracle and reply

- App worktree base: `5077995cb` (tree `20c8c1ed5e9ca48bc1f56f66f0404c83f8d97473`).
- Changed file only: `tests/e2e/local/three-products.p1-chain.spec.ts`.
- Change: line 375 expectation `merge: 'atomic'` -> `merge: 'fields'`.
- Current file SHA-256: `0a9271e73316be894b3b6bf65eebf6dd593be3d7e082044d225fb1dc3a1a2753`.
- Oracle verdict: **PASS**; actual retained split request sent `fields`, and source proves declared reads are authentic.
- Second-case verdict: **FAIL/unresolved**; line 479 saw no `response.data`. The retained log has only the test TypeError, not the public response status/body. Do not add optional chaining or rewrite the accepted split assertion. Owner is the Runtime/Agent public commit path; manager should run the next original execution with response JSON/status retained.
- Checks: exact two-case list, App and Node TypeScript projects, scoped ESLint, diff check, private exact819acf graph/normal34 checks all passed.
- No service/body/browser/full run; no product/fixture/config/generated/pin/lock/helper/opsrow changes.
