# D118d independent protected review

Verdict: **FAIL — exact-unapplied setup seam**.

The exact retained nine-node command ran against `e02180cedafa581bc8105d77341456b8b1c50b5b` with the pinned Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`. It exited 1 with 9 setup errors, 0 test failures. The first failure is:

`tests/sdk/test_timeline_capture_projection.py:303` — `KeyError: 'revision_id'` while evaluating `source_shot["revision_id"]`.

`source_shot` is the authoring shot returned by `bundle_from_document()`. Its revision identity is intentionally retained in `bundle["source_mapping"]["shots"][source_placement["shot_id"]]["revision_id"]`; the authoring shot itself has no `revision_id`. Therefore the new registered Runtime `doc.patch` is not called, and accepted source-item provenance, canonical reload, saved projection, and opener equivalence remain unproven.

The earlier 1545 failure is not reused as the verdict. The canonical fixture projection correction is independently valid: `_saved_document()` now retains the exact shot/internal canonical image fields used by the genuine current reader, while top-level project/timeline scope remains on the canonical document. The old clean saved-item setup was also independently traced: the Runtime occurrence-create path starts with `payload.items: []`, so a registered guarded `doc.patch` is the intended physical source admission. This review cannot approve it because the current setup fails before that call.

Source conservation passes. The final lineage is base `20177e66564f9f91735ed1a11bac821682d60edf` → candidate `a92c6afe0ccd2359e952fc534788d1fce2169049` → final `e02180cedafa581bc8105d77341456b8b1c50b5b`, all by the same author line. Only `tests/sdk/test_timeline_capture_projection.py` changed; all 43 original test assertions, test-function ASTs, decorators, inputs, golden bodies, ordering, opaque fields, pins, and fixture tail are conserved. Candidate `a92c6afe` exactly matches historical setup commit `28081580dc95f02470d82ad81b826335d8e4bd09`. Runtime custody is clean, and the D120 target path is absent at upstream `92443771676ef2bbb547d0a103d708fa8bec4c63`.

This is the second FAIL in the protected review sequence. Per the settled rule, escalate to HARDSol; no further Luna author or speculative approval is warranted. No source, product, test, generated, pin, or Git files were modified by this review.
