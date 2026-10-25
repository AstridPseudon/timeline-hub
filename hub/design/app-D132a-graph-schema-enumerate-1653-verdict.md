# D132a verdict

PASS. The whole authored canonical document was constructed through the pure Agent fixture path before editing and validated against the frozen Runtime `PreparedCommit` schema at `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`.

The complete pre-edit census found exactly one invalid value: `$.canonical_document.shot_revisions[1].payload.metadata`, an authored explicit null in an object-typed slot. No predicate-relevant or non-null-to-object invalid values were found. The one approved migration changes that slot to `{}` in `tests/editing_conformance/test_recorded_graph_roots.py`.

The after-census reconstructed the complete graph and found zero schema errors. The three shared seed consumers and all 22 fixture test bodies were audited; no predicate depends on null handling or preservation at the changed slot. The fixture's 90 assertions and graph consumer's 33 assertions remain unchanged by AST/hash census. The six prior request metadata lines and the earlier numeric gain migration remain read-only.

No Runtime, schema, provider, product, guard, generated, pin, assertion, or other authored-input changes were made. Pytest and the protected own9 run were not run.
