# ap2-m2-parent-main-pointer-original-source-0935

Outcome: KEEP / minimal lease. One current parent proof source is frozen on top of `44e9a83bcc155e713da56b1e0aaed8c2f88dd1e0` (0930).

## Final source

- File: `tests/e2e/local/three-products.spec.ts`
- Test: `M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data`
- Main-correct fixture pointer is preserved at `manualDropPointerAt = 22.5` for both external drops. Main's `computeDropPosition` uses the centered default offset `clipDuration * pixelsPerSecond / 2`; with the five-second fixture this places the committed V1 left edge at 20 seconds.
- The approved strict refusal is restored exactly: status `404`, code `not_found`, message `selected media is not a managed project generation/variant/object`, and bounded `request_id` matcher.
- All other raw/hold/opaque/order/epoch/source/ACK/retry/restart/undo/zeroLegacy assertions, current HOME code, and approved projection blobs are unchanged.

## Exact minimal diff

```diff
-  expect([404, 409]).toContain(wrongVerified.status());
+  expect(wrongVerified.status()).toBe(404);
+  await expect(wrongVerified.json()).resolves.toEqual({
+    code: 'not_found',
+    message: 'selected media is not a managed project generation/variant/object',
+    request_id: expect.stringMatching(/^[A-Za-z0-9][A-Za-z0-9._~-]{0,127}$/),
+  });
```

Pre-commit source identity:

- HEAD: `44e9a83bcc155e713da56b1e0aaed8c2f88dd1e0`
- HEAD tree: `5b96d5c0df0f71d8feb28d224e31518d76a9e8e2`
- HEAD file blob: `18fc9a5a1e81b1f76dfd6bfd14e30b09631b9585`
- Working final file blob: `49d406d76608dde1d6b94df2c4038e5d3c8e5ba4`
- Approved 8eb4d08e6 source blob: `67934dbcd263d6dc52648e176c8401f94338bfc7`

## Checks

- `git diff --check` — PASS.
- `./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --max-warnings 0` — PASS.
- `realpath node_modules` confirmed the shared install `/home/user/work/app/node_modules`; it was not modified.
- No browser, build, daemon, socket, actual/full/service, install, or repeated three-products/product run was performed, per the brief. The actual runtime journey therefore remains unverified on this worker.

## Prerequisites / next step

The harness commit manager should bind the existing approved execution template by data-only source identities. No new wrapper logic is needed. The source is ready for harness commit and later central qualification.
