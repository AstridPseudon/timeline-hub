Implemented authored `app.astrid.word_anchors` references. Identical echoes selecting different words now produce distinct revisions/digests; restore, inverse and redo preserve each choice. Removed the history fold and made the pure evaluator resolve bound IDs without text searching.

Verification:

```bash
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -o addopts= -q -rx tests/editing_conformance/test_word_binding_recipe.py tests/editing_conformance/test_timing_retained_inputs.py tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py
```

**97 passed, 1 strict xfailed** preserving the pre-fix collision evidence. Targeted Ruff and `git diff --check` passed.

[Design](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-word-binding-contract.md) and [report with exact commands and boundaries](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-word-authored-reference/notes/report.md) written, plus both commit-message files.

No blockers. Product registration/default compiler remain inactive; full suites were not run. Next: review the schema, then qualify first-use hydration and ownership/projection support.