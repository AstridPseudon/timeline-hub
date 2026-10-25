# D118a report

Implemented the one-line production repair in `timeline_document.py`: detached publication now uses the existing private `_capture_bundle()` exact-pair authority, preserving public bundle privacy while retaining `_runtime_document` for the emitter.

Tests:

- Original atomic node: `1 passed in 2.68s`
- Private source/wrong-pair/no-write checks: `4 passed in 19.52s`
- Ruff: pass
- Mypy `--follow-imports=skip`: pass
- `py_compile`: pass
- `git diff --check`: pass
- Original test SHA/AST: unchanged/equal

Runtime pin verified clean: `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`.

No blockers. One product file changed; no tests changed. Evidence and commit message are under the assigned worker directory. Independent protected review and manager-controlled merge remain next steps.