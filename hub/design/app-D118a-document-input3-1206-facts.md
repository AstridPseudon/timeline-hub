# D118a document input capture3 facts

- Base and HEAD: `cf7b8d7c2b4cb980de1d873f0498784d5210d508`; worktree clean.
- Allowed test file remained byte-identical: SHA-256 `20ae264e920c39c124ff6c98a5e05af89fef6632e8efda1a6c9e7c58c37e5266`.
- Exact own3 used Runtime `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, with the existing agent venv and current test caller. Result: all 3 requested nodes failed in 4.62s.
- Failures occur before command execution. After `_hydrate`, `document_from_bundle` returns a transcript pin in `dependency_manifest.documents` and a derived `authoring-parent-revision-*`, while the immutable Runtime document has no document pin and revision `parent-1`.
- The causal owner is production `astrid/sdk/timeline/commit.py:369-373` (`document_from_bundle`), not the sole allowed test file. The test’s exact conservation assertions must remain; no speculative test-only carrier or guard was added.
- Static checks all passed: Ruff, mypy with `--follow-imports=skip`, `PYTHONPYCACHEPREFIX=... python -m py_compile`, and `git diff --check`.
- AST conservation: 15 assertions and 43 calls; current file AST equals HEAD. The file is absent at pristine `08e6b905`.
