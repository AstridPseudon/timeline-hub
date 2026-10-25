# D115 report

- Confirmed minimal Runtime seam: `runtime_protocol/timeline_commit_auth.py:773-844` compares an unchanged intermediate parent image against the final accepted candidate instead of its actual ordinal boundary.
- Agent correctly emits an empty effect patch; no effect ordinal should be invented.
- No product/test edits; evidence is in `evidence/ownership-manifest.md` and `evidence/test-results.txt`.
- Missing artifacts recorded: Agent Sol report, source manifest, and retained XML/recipe hashes. No replay or new probe attempted.

Tests:

- Focused auth: 4 passed.
- Private sequential verifier: 17 passed.
- Broader verifier run: non-qualifying (1 fixture failure, 10 missing-Agent-package errors).
- AST parse and `git diff --check`: passed.

Recommended follow-up: one Runtime author should narrowly adjust intermediate no-effect projection plus a Runtime-focused regression, preserving all effect ordinal, ownership, pin, CAS, and refusal guards.