PASS_SOURCE

Reviewed candidate `2154168d30` against parent `7e23790248`.

Files/blobs:

- `native_word_anchor.py`: `4c8dec...` → `edeb0a...`
- `_commit_timing_validation.py`: `194acc...` → `a5496a...`

Findings:

- ID3 source-move/reorder and ID9 stale-window paths now obtain the exact namespaced choice through `authored_refs`, including mirrored parent representations.
- Authenticated `binding()` remains authoritative for pins, closure/source identity, selection, stable word IDs, and half-open timing bounds.
- Legacy flat declarations still use `legacy_binding`; D12/D12a preservation remains intact.
- No input rewriting outside detached validation copies; no history, authority, retry, inverse, ABA, or no-write guard changes.
- Identity validity remains enforced by existing candidate validation. A malformed standalone bundle could make mirror lookup choose its first duplicate, but current production callers validate identity first.
- D14 positives and original test/fixture bodies are unchanged. No behavioral claim made.

Checks:

- AST parse/in-memory compile: parent and candidate passed.
- Scoped Ruff on both files: parent and candidate passed.
- Scoped mypy: parent and candidate passed.
- `git diff --check`: passed.
- Pytest, collection, services, and full suites: intentionally not run.

Targeted meaningful MAIN originals remain owed before source qualification. Separate missing test-oracle literals require their own review.

Worktree is clean. Completion marker and commit message were created.