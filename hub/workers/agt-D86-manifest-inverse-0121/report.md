## F-D86 report — SOURCE_EXACT

No files changed. Current `HEAD` and `tl/integration`: `219b9ca8b196bcf4ee6fda6e08c2e50ae251ae4b`.

Source identities:

- `test_commit_runtime_media_manifest_inverse.py`: `1bc4b5ad…`
- `test_occurrence_media_manifest_inverse.py`: `f416287f…`
- Runtime lock: `a3cd1a3214fa1632879c21d82d1abb9ea720b1de`
- Relevant Agent sources: `commit.py 6c2fc6c8…`, `inverse.py 0702cda4…`, `_commit_patch.py 05a1ebc6…`
- Current transitive fixture migrations: `134f1c276a`, `2f935f6d4d`

The runtime fixture’s prior `IndexError` is addressed by the existing current parent-media fixture migration. The detached popup tests still encounter the current authenticated fork-materialization guard (`ambiguous or unexpected fork materialization`); fixing this would require out-of-scope product changes or synthetic custody, so it remains unapplied.

Checks:

- AST parse/compile and selector conservation: PASS
- Scoped Ruff: PASS
- Scoped mypy: PASS
- `git diff --check`: PASS
- Pytest, collection, fixture/service execution: not run per brief

Required commit message and `DONE` marker created.