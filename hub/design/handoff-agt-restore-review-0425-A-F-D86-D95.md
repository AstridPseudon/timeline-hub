# A — F-D86/D95 protected review

Verdict: `PASS_SOURCE` (static source qualification only; no behavior credit).

## Exact reviewed objects

- Commit: `33be39334ddac2ee54091a58ec1f96bcb0249092`
- Parent: `b8a48a91b01a543ec56e44cee6f6f251d6c90986`
- File: `tests/editing_conformance/test_commit_runtime_text_binding.py`
- Parent blob: `d77d9e1162bbf681630530505efaec74323c30f0`
- Candidate blob: `0f83aae261265c20ddaf33ac3f8cda39bc7bb99e`

## Decision and conservation

The source0405 appendix (`source-disposition.md`, lines 3–58) supports the exact D95 legacy-only disposition for original IDs 99 and 101: current `word_anchors` use an authenticated transcript-document pin, while the originals use historical `elementRef.binding_id`; the registered `text-binding.set` changes/removes that row, and `_validate_element_reference` requires unchanged declaration/source basis. The appendix names the existing unbound inverse replacements and the missing bound-invalidating refusal case.

The commit adds exactly one parametrized test, `test_bound_main_descriptor_invalidating_set_and_clear_refuse_without_writes`, with FIRST MAIN selectors:

- `tests/editing_conformance/test_commit_runtime_text_binding.py::test_bound_main_descriptor_invalidating_set_and_clear_refuse_without_writes[rebind]`
- `tests/editing_conformance/test_commit_runtime_text_binding.py::test_bound_main_descriptor_invalidating_set_and_clear_refuse_without_writes[clear]`

The parent body hashes verified against the exact parent blob are:

- `test_rebind_existing_main_descriptor_undo_is_exact`: `89fe35961b080093706962b2d3183f6f3adac813038e2b4701154e33a87df094`
- `test_clear_existing_main_descriptor_and_inverse_are_exact`: `481335a01f05363a4460873466a2c6b3ac8efb96185a8528793a28161a5a0a6d`

The candidate removes only those two function definitions. In-memory AST comparison conserved every other top-level function exactly; AST counts were retired=2 and replacement=1. The appendix itself has no body-hash table, so these hashes are independently derived from the parent blob rather than credited to the appendix.

## Provider, predicates, and no-write guards

The fixture registers `create_runtime_commit_service()` with `RuntimeService`; `submit()` calls `service.commit_timeline` with the normal `route_path` and authorization callback. The new test submits a dry-run baseline, snapshots canonical closure, head, history, live binding row, original CAS bytes, and replacement CAS bytes, then submits either the native rebind or clear. It requires `RuntimeErrorBase`, `validation_error`, `invalid_document`, empty path, and the exact historical-reference refusal message. It then requires unchanged head/history/closure/live row/original bytes/replacement bytes. This conserves the exact refusal and no-write/CAS/ABA boundary without changing source or authority.

## Static commands/results

- `git diff 33be^ 33be --check`: PASS.
- In-memory `ast.parse`/compile of parent and candidate: PASS.
- Unchanged-function AST conservation: PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check --no-cache --stdin-filename tests/editing_conformance/test_commit_runtime_text_binding.py -` on the candidate blob: PASS (`All checks passed!`).
- `/home/user/work/venv-agent/bin/python -m mypy --no-incremental --cache-dir /tmp/agt-F-D95-mypy tests/editing_conformance/test_commit_runtime_text_binding.py` on the current parent-equivalent worktree file: PASS (`Success: no issues found in 1 source file`).
- Author0405 scoped Ruff/mypy evidence for the six traced source/test files: PASS.

No pytest, collection, helper/fixture execution, service, probe, browser, package install, or full suite was run.
