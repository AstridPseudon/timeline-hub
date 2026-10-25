# D132 trace commands and results

- `git status --short --branch` — PASS; required base `134d9787c791b54db695a2332bd352ca1c0a6a78`, clean.
- `git diff --check` — PASS.
- `git diff --exit-code -- .` — PASS; no worktree diff.
- Whole-repository read-only AST parse — PASS; 2,216 Python files parsed with Python 3.11 AST.
- Whole-repository JSON parse — PASS; 362 JSON files parsed.
- Targeted source hashes — PASS; recorded in `source-custody.json`.
- First `PYTHONPYCACHEPREFIX=<prescribed tmpdir>/pycache python3.11 -m compileall ...` — NOT EVIDENCE; the prescribed `tmpdir` path was an existing file, so Python reported `NotADirectoryError` for cache output. No repository file changed.
- Corrected `PYTHONPYCACHEPREFIX=<worker scratch>/tmpdir-compile/pycache /usr/bin/python3.11 -m compileall -q -f astrid tests test-support` — PASS, exit 0; cache confined to the worker scratch area.
- Final `git diff --check`, porcelain-clean check — PASS.

No pytest was run. No original-9 rerun, full/family/P2/P4/browser/native/service suite, collector, or additional body was run.
