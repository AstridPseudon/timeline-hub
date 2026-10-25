Applied two status-only corrections in `tests/sdk/test_timeline_selected_schema_runtime.py`, covering three new requests. Source tracing supports `merged`; authenticated historical retries retain their original `rebased` envelope. All authored inputs, other predicates, HTTP setup, and seven UNKNOWN cases are preserved.

Validation:

- Python 3.11 AST/compile and conservation audit: PASS.
- Governing Ruff and `git diff --check`: PASS.
- Scoped mypy: only the known missing PyYAML stubs error.
- Immutable Runtime `ab1e4f61…` origins/provider compatibility: PASS.
- Live tests: **NOT RUN; no behavior credit**.

I interpreted `noheavy` as requiring no active heavy work. The guard found `agt-F-D137-real-child-core-2044` active and refused admission; I stopped without retrying. Disk exceeded 5 GB. No live product fault was established.

[Evidence and exact commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D134-selected-status-sol-2041/evidence/validation.md). Commit message and `BLOCKED` written. Next step: resolve admission/routing and qualify the exact four nodes against immutable ab1e.