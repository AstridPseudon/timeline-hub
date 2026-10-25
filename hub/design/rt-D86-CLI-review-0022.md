## PASS_SOURCE

Reviewed author commit `27dc8f04cd1fff78debcf07d5f7e14aaf5c76b59`:

- Only [`test_cli_document_commit.py`](/home/user/work/wt/rt-D86-CLI-review-0022/tests/packs/timeline/test_cli_document_commit.py) changed.
- `_runtime_idempotency`, fabricated replay/conflict logic, and bypasses are absent.
- Retry and changed-key requests reach genuine Runtime `commit_timeline` → coordinator/store idempotency lookup.
- Refusal reason is correctly `error.details.reason == "idempotency_mismatch"`.
- All 12 tests and 8 assigned selectors/input topologies are conserved.
- Runtime registration/caller traces and integration production paths are unchanged.

Checks:

- Candidate Ruff: pass.
- True baseline Ruff: 11 known `F811` diagnostics.
- Candidate and baseline mypy: pass.
- In-memory compile/AST conservation: pass.
- `git diff --check`: pass.
- No pytest, collection, fixture/helper execution, Runtime execution, build, browser, or full suite run per instructions.

Source identity: tree `dc81cb5973df67435e42c72529fdcecea9b82ce2`; candidate blob `78234fb1f760d0a1dcf146ef8551b342ffbc3e28`.

No product or test edits made. Commit message and `DONE` marker recorded.