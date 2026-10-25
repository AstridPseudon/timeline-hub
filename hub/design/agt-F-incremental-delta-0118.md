## F-D89 report

- Created private evidence packet under `/tmp/.../agt-F-incremental-delta-0118/evidence/`.
- Exact new delta: 13 selectors — scalar11 + graph-redo2.
- Zero overlap with original 298; combined count would be 311.
- Preserved all 550 original identities/categories/statuses; 537 remain outside the delta.
- CLI trim3 and held families excluded.
- Agent HEAD: `219b9ca8b196bcf4ee6fda6e08c2e50ae251ae4b`; tree and parents recorded.
- No product-source changes.

Validation:

- AST parse/in-memory compile: PASS.
- Ruff: PASS.
- Python 3.13 mypy: PASS.
- Default mypy: blocked by known NumPy/Python-version stub diagnostic.
- Dependency hashes: 0 mismatches / 1,932.
- JSON/TSV/set/lossless validation: PASS.
- Existing recipe `bash -n`: PASS.
- No pytest, collection, service, browser, build, or functional qualification run.

Graph is reported as `SOURCE_EXACT`, not behavioral PASS. Main functional qualification remains pending. DONE marker and conventional commit message were written.