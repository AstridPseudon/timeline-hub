# Validation

All checks were read-only against the existing evidence/canonical paths.

- `sha256sum delivery/README.template.md delivery/gate-results.md bin/delivery-build` — PASS; exact required hashes.
- `stat` mode/size checks — PASS; both canonical targets regular `0644`.
- Private independent checker `evidence/tmp/independent_review.py` — PASS; exact candidate/prefix/suffix checks, all 568 outside current readbacks, historical accounting, publication hashes, disposition counts, known-gap markers, AST render definition, and function-only renderer call.
- `python3 -m json.tool evidence/review.json` — PASS.
- `python3 -m json.tool evidence/source-manifest.json` — PASS.
- `python3 -m json.tool evidence/sampler-lifecycle.json` — PASS.
- `python3 -m json.tool evidence/tmp/renderer-result.json` — PASS.
- `python3 -m json.tool evidence/tmp/independent-review-result.json` — PASS.
- `python3 -m py_compile evidence/tmp/independent_review.py` — PASS.
- Private `ast.parse` of `evidence/tmp/independent_review.py` — PASS.
- `ruff check --select F --no-cache evidence/tmp/independent_review.py` — PASS.
- Fresh ordinary disk sampler — PASS for bounded run: 3 samples at 5-second intervals, PID/exit/wait/reap recorded, stop not reached; first-tool gap explicitly retained.

Not run by design: original pre-CAS `check_join.py` after CAS; types; product tests; full suites; browser/live sockets; delivery-build CLI/main; staging/cloning; rehearsal; services/bodies; canonical write/CAS; ZIP.
