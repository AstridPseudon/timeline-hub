Changed only the permitted shared-inverse test file:

- Added exact per-command step patches and conservative closure reads.
- Committed source preparation before capturing shared placement.
- Diffed canonical physical payloads without remapping new item IDs.
- Preserved all five original test bodies, ten cases, timing and opaque inputs.

Actual prior XML shows **five missing-step-patch errors and five alias-contradiction errors**, rather than ten identical errors. Both prior failed proofs remain unchanged.

Checks passed, exit 0:

- Baseline and candidate scoped `ruff check` and `mypy`.
- `python3 /tmp/w-a66c28e2a6/verify_source.py` — in-memory compile and AST/input conservation.
- `git diff --check`.

Exact commands, caller/schema trace and hashes are in [evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D91-step-claims-sol-0409/evidence/static-checks.json). Candidate tree: `7a37b062da5ecfe732da6618f81028f222573a93`; commit SHA awaits the harness.

No behavioral execution was performed, as required. Source correction is complete; independent protected review and one authorized MAIN proof remain pending. Commit message and `DONE` written.