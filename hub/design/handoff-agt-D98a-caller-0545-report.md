## Report

Implemented F-D86/D98a in `test_commit_runtime_occurrence_media.py`: replaced the hand-authored occurrence birth with registered `capture_occurrence_create`, preserving all inputs and assertions.

Affected canonical IDs: `shot:chapter-shot`, `occurrence:occ-a`. Shared callers audited across all five authorized test files.

Checks passed:

- Ruff parent and candidate
- Mypy parent and candidate
- In-memory compile of all five files
- `git diff --check`

No pytest, imports, collection, helpers, fixtures, services, or behavior runs were performed per source-only instructions.

Protected review and meaningful MAIN proof remain pending externally. Commit message and `DONE` marker created.