# D118d whole-path facts

## Verdict and source version

This is an independent read-only audit. The finalized source under review is `e02180cedafa581bc8105d77341456b8b1c50b5b` on `tl/app-D118d-projection-first-return-1551`, not this worker's unchanged `20177e66564f9f91735ed1a11bac821682d60edf` worktree. No source or product file was changed here.

The protected own9 result remains an exact setup seam: all nine nodes stopped at `bundle_from_document(document)` with `AuthoringBundleError: project scope belongs on the canonical document`. The registered source-item `doc.patch` was not reached. The finalized writer source corrects only `_saved_document()` by projecting Runtime child reads to canonical image fields; its test-function ASTs, authored inputs, assertions, pins, ordering, and golden bodies remain unchanged. This correction has no post-fix own9 behavioral result.

## Exact boundary

`_verify_document()` keeps `project_id` and `timeline_id` at canonical-document scope, rejects `project_id` on every revision row, and requires exact shot/internal image key sets. `bundle_from_document()` validates that DTO, then adds project/timeline scope only while opening the authoring bundle. Runtime's `_image()` creates the canonical `{revision_id, content_digest, payload}` image; `revision_closure()` adds the exact shot/internal identity fields. Therefore the protected failure was a fixture row-shape mismatch, not evidence that the canonical validator or production guard should be relaxed.

The genuine current source path in `tests/sdk/test_capture_source_runtime.py::read_document()` uses the same two child field sets as finalized `_saved_document()`: shot rows retain `shot_id`, `revision_id`, `internal_timeline_revision_id`, `content_digest`, `payload`; internal rows retain `timeline_id`, `revision_id`, `content_digest`, `payload`. The source comparison found those field tuples equal.

The supported current production capture caller is `prepare_filmstrip()` through `_open_current_input_closure()` in `astrid/sdk/timeline_filmstrip.py`; it delegates to the managed timeline exact-parent projection and consumes projected config/registry/authority. It is not a reason to weaken canonical DTO validation. The fixture adapter must therefore project public Runtime row envelopes to the canonical DTO before invoking `bundle_from_document()`.

## Whole path

The real source fixture creates Runtime state, registers `load_timeline_commit_provider("astrid")`, and submits setup commands through Runtime's `commit_timeline`. The finalized projection fixture then:

1. reads the saved closure through the corrected canonical converter;
2. derives the source media identity from the source shot's internal registry clip;
3. submits the guarded `doc.patch` for source item `item-1`, with the exact source revision ref and `before: {state: present, value: []}`;
4. requires the response status `accepted`, reloads the canonical document, and authors the existing opaque source graph;
5. publishes through `_RuntimeAuthoringWriter.commit_timeline`, which uses Runtime's registered provider route;
6. compares the saved `project(document)` output with Runtime's exact-parent projection and compares candidate edits with `_open_candidate_input_closure`.

Runtime's pinned source validates the provider ABI, calls the provider through the commit coordinator, and on acceptance persists the provider's `canonical_document`, publishes the receipt, and reconstructs saved closures as canonical images. This supports the caller route; it does not prove the corrected nine-node behavior without execution.

The preserved checks cover config, registry, expansion identity and parent digest, `shot-z` then `shot-a` order, authored payload/opaque fields, dependency and read-row pins, and candidate opener equivalence for the six named changes. Those are source-preserved expected outcomes, not observed post-fix results.

## Next gate and limits

The expected next gate is the exact retained nine-node own run against source `e02180cedafa581bc8105d77341456b8b1c50b5b` with Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, after the required 5,000,000,000-byte disk admission, followed by the still-required protected review. This worker did not run pytest, a service, browser, acquisition, full suite, or original rerun.

No auth root, new IDs, new stages, new digests, or new authored input was introduced by this audit.
