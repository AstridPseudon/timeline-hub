PASS_SOURCE — F-D86/R2

Reviewed candidate `a67e77df9ccc99ebac1d6767114b0c755c334271` against parent `7d35b32343d32fa94091b9e9f1fa160c2868e0cb`.

- Candidate blob: `d85d96ea5fc00fc4c53dbdb030a8874ae5e54617`
- Parent blob: `173891ccef902d02c8835b78ebafbc39401d8f04`
- Only `tests/sdk/test_timeline_restore_effect_order_runtime.py` changes.
- Reuses the authenticated P4 fixture, owner credential, generated client, real route, Runtime handler, authorization, coordinator/provider/store, and public history reads.
- No mock transport seam, fake authorization/history, raw SQL, fixture bypass, or production inverse oracle.
- Independent complete ordered source and inverse patches preserve op/ref/path/before/value and duplicate/order semantics.
- Restore/undo signatures, envelopes, exact base pairs, restart, dry-run null-receipt/no-write, head/history, and exact idempotent retry guards are covered.
- Historical ID5 and the three strict capture/order/ABA controls remain unchanged and separately required. Product `72a` remains unchanged/HELD.

Static checks:

- AST parse/in-memory compile: PASS for candidate and parent.
- Scoped Ruff: PASS for candidate and parent.
- Scoped mypy: PASS for candidate and parent; imports skipped.
- `git diff --check`: PASS.
- No pytest, collection, imports, helpers, fixtures, services, or functional execution performed.

MAIN old-RED/new-GREEN proof remains unverified. Required selector recipe:

```text
tests/sdk/test_timeline_restore_effect_order_runtime.py::test_id5_public_undo_of_restore_preserves_authenticated_effect_order
tests/editing_conformance/test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse
tests/sdk/test_timeline_commit_provider.py::test_original_capture_claims_are_verified_before_refresh
tests/sdk/test_timeline_commit_provider.py::test_reversed_inverse_target_order_is_refused_without_partial_acceptance
tests/sdk/test_timeline_commit_provider.py::test_undo_detects_aba_and_unchanged_write_publications
```

Commit message written and `DONE` created.