# D141ee protected restoration review

Result: `PASS_SOURCE_RESTORATION`; restored-targeted behavior: `FAIL_WITH_VISIBLE_FAILURES_AND_COLLECTION_ERRORS`.

- Independent manifest/blob/AST checker: 55 unique accepted IDs (15 writer + 38 inverse + 2 installer), all 55 pristine Git blobs and authored function ASTs match; `tests/timeline/test_inverses.py` is byte-identical to pristine 64197afa.
- The commit is test-only and additions-only across nine `tests/` paths. No product, generated, pin, profile, environment, kit, hub, or source file changed; no current tests/helpers/predicates were overwritten.
- Exact 55-node pytest invocation exited 4 with two real collection errors: missing `astrid.core.timeline.inverses` (38 nodes) and missing `promote_approved_authoring_candidate` (2 nodes). It ran zero nodes in that mixed invocation; the errors were not converted into passes.
- Exact unaffected accepted selectors then executed 15 nodes (13 writer + 2 installer): all 15 failed against current behavior. XML records the 15 failures. No test passed, skipped, xfailed, or was deselected.
- Ruff exits 1 only on the byte-identical pristine inverse file: import ordering (`I001`) and unused `InverseRequest` (`F401`). No fix was applied because it would violate exact source conservation. `git diff --check` exits 0.
- No owner retirement was inferred, and no product fix was attempted.

Finite follow-up ownership: restore/decide the missing inverse implementation and old authoring/publish surfaces, and separately resolve the installer/CLI/runtime behavior failures before claiming targeted behavior complete.
