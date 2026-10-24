# R-P2 D80 Security Review

Semantic review: PASS.

- `_fork_owner_before` derives ownership from authenticated occurrence, physical shot/revision/digest, and Runtime-supplied nonempty `(project_id, timeline_id)`.
- Complete projected rows, source pins, sibling retention, allocation roots, aliases, materialization, and no-write tamper cases are enforced.
- Agent ownership/materializer/reservation functions match the recorded original via hashes/AST; no Agent patch is needed.
- C0 citations and contract hash verified.

Tests:

- Focused 12: 12 passed
- Strict rejects 9: 9 passed
- New definition 15: 15 passed
- Production tamper 5: 5 passed
- ABI/history 10: 10 passed
- Shared inverse 36: 36 passed
- Agent conformance evidence: 97 passed, 1 integration test deselected
- Ruff, Pyright, compileall, and `git diff --check`: passed
- Strict mypy: 13 baseline and 13 candidate diagnostics; zero new/removed

Reviewed committed evidence confirms original `327da` reproduces the owner mismatch, while `a4d4` and `52b` pass the genuine production path with four helper calls.

Blocked integration findings:

- `52b` tracks 70 root-level `evidence/` files; these must not ship. Originals were preserved under the worker evidence directory.
- `52b` predates `1bae/09c79`; port only the D80 auth/test changes and preserve the `<` empty-inverse-range predicates.
- Initial Agent-dependent test attempts lacked `ASTRID_CHECKOUT`; corrected reruns passed.

No product or test repairs were made. Commit message and `DONE` marker were written for the harness.