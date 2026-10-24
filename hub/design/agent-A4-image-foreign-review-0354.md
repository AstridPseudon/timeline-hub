## Verdict: PASS — fixture-only

- Reviewed candidate `a1036f9e8d` against parent `8657e83653`.
- `foreign_pin` refreshes only after `waiting_for_worker`, uses one fresh key, preserves current epoch/capability, verifies the claimed foreign project, and settles through the real Runtime path.
- Approved support pair matches `4ae4389062` byte-for-byte.
- No product, Runtime, App, schema, or assertion weakening changes.

Tests:

- Foreign/support controls: **17 passed**
- Runtime malformed-shape, wrong-scope/epoch, stale-fence, and settled-authority controls: **7 passed**
- Ruff, private mypy, vendor lock, artifact manifest: **passed**
- Working-tree diff check: **passed**

Independent parent comparison:

- Parent run: **20 failed, 16 passed**.
- Candidate’s exact remaining 20 failures match the parent selectors and all fail at the unchanged `provider executed a different command` path:
  - fresh film: 2
  - ordinary birth/replacement: 4
  - stale replacement: 2
  - dependent/ABA: 8
  - old-source tuple: 2
  - ordered replacement: 2

These remain pre-existing and are not credited as candidate failures or parent-family passes.

Caveat: parent→candidate diff check reports an inherited blank EOF line in the byte-identical approved support file; it was intentionally unchanged. No next code action is required for this fixture.