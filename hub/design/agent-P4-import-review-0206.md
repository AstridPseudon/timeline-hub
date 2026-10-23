# P4 import review: PASS

Reviewed `70e6d33de527779d8a2a4318b09e4b85a532d347` on base `5a313eb88e8ddce1e9e033ed9cfde7ef433f7c55` against PLAN §3 P4/G3/R2 and `/home/user/timeline-hub/hub/design/commit-v2.md`.

Exactly the requested two tests were added, byte-identical to donors:

- `tests/sdk/test_p4_commit_v2.py` = donor `2d21a98919767016b5ff32a37c2ee207ec1c31fe` (blob `85218e8e99a1c7602d2b7ee399f3847fac759186`).
- `tests/sdk/test_p4_ten_note_provider.py` = donor `e7385882ef50a59e6f62f32058fe211eb6e0b69f` (blob `1ed257c4604552793d2eaabfc117babe93c5b445`).

Existing `tests/sdk/test_p4_commit_cases.py` is unchanged; no product files, deletions, or unrelated ancestry were imported. The tests use the documented fake generated transport and detached real provider, preserve ten independent step undo/redo, other-nine and opaque/history/ABA assertions, and leave the broader existing v2 request/reply coverage intact.

Evidence:

- Targeted pytest (the two imported files plus existing P4 collection): **15 passed in 6.94s**.
- Scoped Ruff: **All checks passed**.
- Private `/tmp/astrid-u2-typecheck/bin/python` mypy: **Success: no issues found in 3 source files**.
- The private interpreter lacks pytest, so pytest was run in the shared read-only Agent venv; no full suite was requested.
