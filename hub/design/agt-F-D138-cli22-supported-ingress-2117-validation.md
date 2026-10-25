# D138 validation

## Source checks

- Python 3.11 AST parse: pass.
- Python 3.11 private compile: pass (PYTHONPYCACHEPREFIX=/tmp/w-e71ff038e7/pycache python3 -m py_compile tests/editing_conformance/test_native_batch_ingress.py).
- make PY=/home/user/work/venv-agent/bin/python ruff: pass, current=2143 baseline=2143.
- make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy: pass, Python 3.11, current=1902 baseline=1902.
- git diff --check: pass.

## Behavioral service

- Central targeted request agt-F-D138-cli22-supported-ingress-2117-targeted-1025212206-14373 collected the exact 22 root-045 node IDs but the default targeted lane deselected all integration-marked cases: 22 deselected, exit 5. No case executed; behavioral outcome is unverified.
- Earlier request agt-F-D138-cli22-supported-ingress-2117-targeted-1025212032-23594 was a collection-only command-line construction error (exit 4) and executed no tests.
- No live localhost test was run in this sandbox.

## Scope checks

- Only tests/editing_conformance/test_native_batch_ingress.py changed in the worktree.
- The parser-only retired-spelling test was not edited.
- No commands-file parser, production caller, Runtime, fixture, schema, pin, generated client, kit, suite, or assertion was changed.
