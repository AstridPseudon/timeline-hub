# G4 bootstrap test-preservation repair

## Verdict

FAIL for final qualification: the requested test-only changes are present, but the provider gate cannot reach 112 because the exact restored guard test fails against the current product merge.

## Exact changes

- `tests/sdk/test_timeline_commit_provider.py`: restored the exact 33-line test body from `a8c2b5b88533c7b58207f0b77d179a1dc523c0d2`.
- `tests/timeline/test_authoring_media.py`: changed only the stale operation-kind expectation and added the strict G3 mapping:

  ```python
  ["occurrence.swap-media", "doc.patch"]
  [
      ("set", ["clips", "id:clip-1", "at"],
       {"state": "present", "value": 0}, 0.125),
      ("set", ["clips", "id:clip-1", "hold"],
       {"state": "present", "value": 1.8}, 0.75),
  ]
  ```

  The two changes must share the same ref. Every later original assertion remains unchanged.

## First cause

The restored scope test expects a mismatched physical timeline binding to raise `CommandError("unsupported entity reference 'timeline'")`. Current `astrid/sdk/timeline/inverse.py` skips all bindings containing `physical_ref` before that entity check, so the exact original test fails with `DID NOT RAISE`. This is a product behavior mismatch in the current merge. The brief explicitly disallows production changes and test weakening, so no workaround was applied.

The real-runtime command-kind mismatch is stale after G3, not observed data loss: the untouched assertions continue to prove timing, source window, media identity, alias order, opaque fields, child closure, narration, metadata, sibling preservation, history/reload, lost-ack undo retry, ABA, disjoint rebase, and refusal.

## Evidence

- Provider file with Runtime checkout and PYTHONPATH: **111 passed, 1 failed**; the sole failure is the restored guard test, so required 112 is not claimed.
- Focused authoring-media tests: **74 passed, 2 deselected**.
- Scoped Ruff and `git diff --check`: **passed**.
- Central exact real-runtime test request `agt-G4-bootstrap-test-preserve-0332-targeted-1023033435-8246`: collection blocked by `ModuleNotFoundError: runtime_protocol`; migrated assertion not reached.

No product/schema/generated/pin/client/lock changes, dependency writes, skips, xfails, or deletions.
