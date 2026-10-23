# Handoff — ap2-P1-correlated-collector-review-1708

**FAIL** on exact author branch `439f6ddbfe250c01a56be721f41cff2eaf03291b` (parent `4c4c9c77c96fab70c4efef09db9a3bc456b0d803`).

The source-only checks are green: approved Node 20.19.4 safety tests 6/6, root/App/Node TypeScript, scoped ESLint, exact two-test listing, diff check, allowed-path identity, unchanged locks, and the original first-test-through-EOF SHA-256 `582dc8fbc3cdf1991b981dce969e3981b63484b70aaeb70f331d907f5b2fc9bd`. No product/test edits were made and no browser/body/full/service run was performed.

The review does not grant PASS because the actual second-case failure packet still logs `readonlyTraffic[].requestBody` and `commitTraffic[].request.raw` (`three-products.p1-chain.spec.ts:797-810`), contrary to the absolute no-rawbody boundary. Also, `sourceWindowSnapshot` treats Playwright's `isVisible() === false` for missing/detached locators as observed invisibility rather than `UNKNOWN` (`:465-468`, `:510-511`), weakening evidence after pageerror/reload/unmount. The added before/after DOM reads do not appear to settle the held-route race, but that does not offset these evidence failures.

Smallest correction: allowlist structural request/reply heads/counts only in emitted packets, and distinguish absent/ambiguous DOM nodes from a genuine invisible node before serializing visibility. Re-run the six pure diagnostics and static gates, then independently review again. Actual mounted capture/basis/adoption and Runtime refusal remain UNKNOWN; no source-only GO is claimed.
