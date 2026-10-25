FAIL_SOURCE — F-D86/R2 review of `7d35b32343d32fa94091b9e9f1fa160c2868e0cb`.

Findings:

- `tests/sdk/test_timeline_restore_effect_order_runtime.py:37–57` bypasses the required public path with `WorkspaceClient.__new__`, `SimpleNamespace`, patched resolver/open methods, direct `RuntimeService` calls, and `authorize=lambda: None`. The new history lambda only wires the fake seam; it does not prove generated transport → authenticated Runtime.
- `:138–140` uses production `inverse_changes(source_patch)` as the oracle, so inverse ordering/content is not independently specified. Source-patch assertions only check sibling-path counts, not the complete ordered effect list.

The historical `test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse` and existing inverse capture/order/ABA controls remain present and untouched. No functional credit granted.

Checks:

- AST parse/in-memory compile: PASS
- Ruff target and parent via stdin: PASS
- mypy target and parent via process substitution: PASS
- `git diff --check`: PASS
- No pytest, collection, imports, services, or functional suites run.

MAIN selector recipe after repair:

```text
tests/sdk/test_timeline_restore_effect_order_runtime.py::test_id5_public_undo_of_restore_preserves_authenticated_effect_order
tests/editing_conformance/test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse
tests/sdk/test_timeline_commit_provider.py::test_original_capture_claims_are_verified_before_refresh
tests/sdk/test_timeline_commit_provider.py::test_reversed_inverse_target_order_is_refused_without_partial_acceptance
tests/sdk/test_timeline_commit_provider.py::test_undo_detects_aba_and_unchanged_write_publications
```

No worktree files changed. Commit message prepared and `DONE` created.