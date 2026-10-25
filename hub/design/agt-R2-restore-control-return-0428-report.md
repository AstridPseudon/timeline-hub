Implemented F-D86/R2 in `tests/sdk/test_timeline_restore_effect_order_runtime.py`.

- Added the genuine `list_timeline_commits` generated transport backed by `RuntimeService`.
- Preserved all restore, undo, inverse-order, history, retry, and no-write assertions.
- No product or other test changes.

Static checks:

- In-memory AST compile: PASS
- Candidate Ruff: PASS
- Candidate mypy: PASS
- Parent Ruff/compile comparison: PASS
- `git diff --check`: PASS
- No pytest, collection, services, or full suites run per source-only instructions.

Selectors retained:

- Original: `tests/editing_conformance/test_word_binding_recipe.py::test_last_write_clear_undo_restore_and_restore_inverse`
- New: `tests/sdk/test_timeline_restore_effect_order_runtime.py::test_id5_public_undo_of_restore_preserves_authenticated_effect_order`
- Strict negatives: the `[rebind]` and `[clear]` `test_bound_main_descriptor_invalidating_set_and_clear_refuse_without_writes` cases.

Commit message written for F-D86/R2 and `DONE` created. Behavioral proof remains pending the fresh protected review and candidate test run; product `72a` remains held.