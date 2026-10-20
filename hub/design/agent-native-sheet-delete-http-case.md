# AG03 / Gate 1 — NativeSheet omission over Runtime HTTP

Status: proven for the bounded parent-clip omission slice; AG03 is not
complete because the detached legacy sheet consumer remains.

## Exact proof identity

- Agent source: worktree `/home/user/work/wt/agt-m2-native-sheet-delete-http-case`,
  base `b24144d9759641980c0d072ddaa80373733d7308`; final central snapshot tree
  `2fc50570ba4e5bfc0980e248da93960106bdf4bd`.
- Exact node:
  `tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_omitted_native_clip_row_delete_retries_rebases_and_refuses_changed_selection`
- Central request:
  `agt-m2-native-sheet-delete-http-case-commit-integration-1020152736-25044`
- Runtime source: `/home/user/work/runtime`, commit
  `81f8c7e0b22c34804015c054762af3d737e4698a`, tree
  `0e3a5b938d9ca489fc760b09d34b02d4ac9aad51`.
- Central command:
  `env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/editing_conformance/test_native_sheet_current_runtime.py`
- Central result: **16 passed in 51.61s**, exit 0. The focused node passed
  locally in **1 passed in 6.69s** with the same Runtime checkout.

## What the node proves

The real generated WorkspaceClient/RuntimeHandler path exports two parent clip
rows with identical visible content but distinct `# ref` bindings, removes one
bound row, and commits the existing `clip.delete` through NativeSheet and the
durable outbox. It then verifies the lost-ack restart retry sends the exact
original request, reloads the surviving row with its opaque data and order,
performs guarded undo/redo, and restores the pre-rebase state for the remaining
checks. An old export rebases over another actor's disjoint sibling property
edit and preserves that edit. A later membership addition and a later deletion
of the selected target each refuse with no additional accepted head/history
entry.

The implementation uses the existing `capture_clip_delete`, command registry,
Runtime provider, inverse, and rebase machinery. No operation, DTO, route,
provider, SQL history path, renderer dependency, or client-side three-way merge
was added.

## Remaining AG03 consumer

The detached legacy `apply_sheet` API at
`astrid/sdk/timeline_sheet.py:849` still reaches `_apply_parsed` and its
legacy omission handling at line 1109 (`if name not in seen ... clip.remove()`).
It remains intentionally unchanged, along with its positive tests. This proof
does not claim AG03 deleted or that the legacy writer is retired.
