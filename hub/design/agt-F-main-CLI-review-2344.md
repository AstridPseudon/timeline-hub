## Report

**Verdict: FAIL — bounded source finding.**

The fixture uses genuine Runtime bootstrap/provider/closure/commit plumbing, and only the assigned test file changed. All 12 test ASTs, decorators, parameters, assertions, raises, and bodies are conserved.

Finding:

- `tests/packs/timeline/test_cli_document_commit.py:167-203`
- `_runtime_idempotency` bypasses Runtime on exact retries and fabricates `idempotency_conflict` for changed bodies.
- Runtime’s actual store returns `idempotency_mismatch` at `timeline_commit_store.py:222-223`.

Affected assigned cases: three idempotency selectors. Their retry/refusal oracles are not live against Runtime.

Checks:

- In-memory compile/AST parse: pass.
- AST conservation: pass.
- Candidate Ruff: pass.
- Candidate and baseline mypy: pass.
- Baseline Ruff: existing 11 `F811` errors from imported `public_session`; candidate removes them.
- `git diff --check`: pass.
- No pytest, service, body, build, or functional qualification run per D85/D86 rules.
- No production caller drift versus `tl/integration`.

No product changes or merge request requested. Recommended next step: repair the fixture helper to delegate idempotency behavior to Runtime, with any expectation correction authorized separately. `DONE` marker created.