# Canonical OPS check validation

The single invocation was run unchanged from the final working tree:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python ops-child-custody/tests/canonical_check.py
```

Result: exit 0. The unaltered stdout/stderr and nested command exits are in
`canonical-check.log`.

- Governing Ruff `/root/.local/bin/ruff` 0.16.8: exit 0, explicit three-file scope.
- Repository Ruff `/home/user/work/venv-agent/bin/ruff` 0.12.0: exit 0, `ops-child-custody/tests` scope.
- Existing unittest suite: exit 0, exactly 64 tests.
- Private-cache `py_compile`: exit 0.
- Owned source diff check: exit 0.
- Canonical script no-index whitespace check: exit 1 with no diagnostics (expected for a new file).
- Historical maker EOF diff check: exit 2 with exactly the two preserved maker EOF diagnostics; not an authored failure.
- Negative census: structured exit 2, complete expected missing set, and all four mutation flags false.
- Final canonical status: PASS for source/unit qualification only; genuine whole-maker E2E remains NOTRUN.

No setup, Store initialization, Git carrier mutation, maker invocation, package
acquisition, network, production child, or full suite was run.
