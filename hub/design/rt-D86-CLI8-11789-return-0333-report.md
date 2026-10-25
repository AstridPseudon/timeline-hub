Implemented the F-D86 fixture correction in [test_cli_document_commit.py](/home/user/work/wt/rt-D86-CLI8-11789-return-0333/tests/packs/timeline/test_cli_document_commit.py): serialized detached files now omit the private `_runtime_document` marker, preventing false provenance mismatches.

Checks passed:

- AST/in-memory compile; all 12 test bodies conserved.
- `ruff check ...` — pass.
- `mypy --config-file pyproject.toml ...` — pass.
- `git diff --check` — pass.

Pytest/helper/collection/service execution was intentionally not rerun per task instructions, so functional success remains unverified. Commit message and `DONE` marker were written.