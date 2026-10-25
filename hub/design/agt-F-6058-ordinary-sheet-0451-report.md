Implemented F-D86 in `tests/editing_conformance/test_native_sheet_ordinary_runtime.py`:

- Released the fixture service before preflight reopens the realm, fixing `OwnerBusyError`.
- Added conditional `media.admit` for the exact ingested CAS media pin, preserving MIME, identity, and document topology.
- No product/runtime changes.

Validation:

- Ruff parent/candidate: PASS.
- Mypy parent/candidate: PASS.
- AST parse/compile and assertion conservation: PASS.
- `git diff --check`: PASS.
- Pytest/collection intentionally not run per source-only restrictions.

Protected review and MAIN behavioral proof remain unverified. Commit message written and `DONE` created.