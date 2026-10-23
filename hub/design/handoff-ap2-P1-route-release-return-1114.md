# Handoff: P1 route-release cleanup

PASS. Commit candidate is the current worktree change on `tl/ap2-P1-route-release-return-1114`.

Changed only `tests/e2e/local/three-products.p1-chain.spec.ts`: the second P1 refusal case now releases the authentic held trim route in `finally` around the body/read assertions and real Agent move. The release remains the unchanged captured request (`route.fetch` then `forward`), uses a fail-closed abort fallback, and preserves the original assertion/Agent error. Existing assertions and all seed/helper/diagnostic content were retained.

Validation:

- scoped ESLint: PASS;
- P1 `--list`: PASS, exactly 2 tests;
- root and Node TypeScript checks: PASS;
- source-backed synthetic release probe: PASS for success, assertion throw, Agent throw, and original-error preservation;
- diff check/outside-identity/EOF checks: PASS.

Browser/HTTP/full/build/service execution was intentionally not run. Real Runtime refusal and the practical App journey remain unverified.
