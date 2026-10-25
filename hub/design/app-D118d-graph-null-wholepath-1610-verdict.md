# D118d verdict: PASS

The independent source finding passes: the first-return no-diff conclusion is correct. The candidate changes only the graph test’s v2 request envelope; it does not alter the authored gain:null, compiler, provider registration, schema, or assertions.

The actual seam is:

- tests/editing_conformance/test_recorded_graph_roots.py:46-51 authors gain: None.
- astrid/core/timeline/authoring_bundle.py:1249-1305 copies the placement and leaves gain untouched.
- tests/sdk/test_timeline_commit_graph_roots.py:56-65,108-142 reaches the genuine registered commitTimeline provider.
- runtime_protocol/timeline_commit_store.py:1599-1605 validates the prepared candidate, while runtime_protocol/timeline_commit_validation.py:162-175 applies the public schema.
- runtime_protocol/schemas/timeline-commit-bundle.json:3376-3385 requires Occurrence.gain to be a number, so explicit null is refused.

The passing same-property source case uses gain: 1 (tests/editing_conformance/test_commit_runtime_video_unplace.py:73-85; producer astrid/sdk/timeline/native_occurrence_create.py:46-50). It does not establish null support. The adjacent Runtime normalizer also rejects explicit None; it does not silently default it.

This is an existing deliberate schema refusal, not evidence of a candidate product regression. Whether authored null should be supported remains a C0 owner decision; the intended semantics cannot be inferred from this review. D12/D12a’s unchanged-invalid untouched-field rule does not apply to a newly created/written occurrence. No product repair or functional GO is proposed.

The original typed-root, tamper, no-write, unrecorded/orphan, inverse/redo, and authored-fact purposes and all 33 assertions remain preserved.
