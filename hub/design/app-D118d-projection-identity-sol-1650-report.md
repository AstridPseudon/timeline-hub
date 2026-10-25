Blocked by a missing production dependency; no repository files changed.

The initial source-item commit fails before duplication. The frozen base lacks cited D100 commit `d3b5cfef`: `_command_state.py` rejects the authored empty-to-one item replacement. Fixing that product guard exceeds the authorized test-file scope.

Preservation checks passed: all 43 original assertions, 11 test functions, 54 fixture statements, goldens, inputs and pins remain exact.

Commands passed:

```sh
/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py
/home/user/work/venv-agent/bin/mypy --cache-dir "$TMPDIR/mypy" --follow-imports=skip tests/sdk/test_timeline_capture_projection.py
PYTHONPYCACHEPREFIX="$TMPDIR/pycache311" /usr/bin/python3.11 -m py_compile tests/sdk/test_timeline_capture_projection.py
git diff --check
```

Own9 **NOTRUN**: no causal source correction exists, so an unchanged rerun was prohibited. All nine purposes remain unverified.

Wrote the five requested evidence files, `commit-msg`, and `BLOCKED`. Next: owner resolves the D100 product dependency before another exact9 run.