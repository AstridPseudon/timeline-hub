# G5 inverse fidelity review

## Source verdict

**PASS for source/test fidelity; behavior remains PENDING.**

Candidate `5dcf78e31` was reviewed against `b9092fe27`. Scope was only
`tests/sdk/test_timeline_restructure_guarded_runtime.py`.

The new fixture overlays the unchanged shared `restructure_runtime` setup,
binds `RemoteTimelines.open_bundle.__get__(...)`, and maps the three public
immutable revision methods to the fixture Runtime service. Its document reader
passes the exact current revision/publication pair. Production `open_bundle`
then performs the authenticated closure reads, publication receipt pairing, and
canonical closure equality checks. No private `revision_closure`, cache, or
invented authority appears in the new fixture.

AST comparison preserved the original restructure command/request metadata,
accepted canonical/receipt assertions, opaque null/order preservation, whole
undo and redo assertions, and overlap refusal. The candidate adds only the
required unchanged-head, unchanged-history, and unchanged-canonical assertions
after refusal. The shared legacy fixture is byte-identical to `b9092fe27`.

The strict-pair control/source review also found the existing owner-pin and
mismatched-response controls, and the production opener's exact
`revision_id`/`publication_id`/receipt and closure-integrity checks. This is a
fidelity review only: it cannot certify the known Runtime inverse 503 repair or
claim undo/redo behavior passes.

## Evidence

- Target + legacy collection: **49 collected**.
- Scoped Ruff: **passed**.
- Private mypy: **passed**.
- `git diff --check`: **passed**.
- Independent AST/source audit: **passed**.
- Reused unchanged prior evidence: **35 legacy restructure tests passed** and
  **2 duplicate neighbors passed**.

The known failing inverse body and prohibited full/D17/P1/P4/native suites were
not run. No repository or product files were changed by this review.

