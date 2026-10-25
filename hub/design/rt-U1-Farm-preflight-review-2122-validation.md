# D135 review validation

## Commands and results

- `ruff check ops-u1-farm-preflight/preflight.py` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-e10f2febca/d135-review/pycache /home/user/work/venv-agent/bin/python -m py_compile ops-u1-farm-preflight/preflight.py` — PASS.
- `/home/user/work/venv-agent/bin/python -m json.tool ops-u1-farm-preflight/source-manifest.json` — PASS.
- `git diff --check HEAD^ HEAD -- ops-u1-farm-preflight` — PASS.
- Frozen Git-object audit for the manifest’s 21 source files — **21/21 PASS**.
- Frozen AST/import-manifest audit for all seven actual modules — **7/7 PASS**; no denied top-level calls found in those modules.
- `/home/user/work/venv-agent/bin/python ops-u1-farm-preflight/preflight.py --runtime-checkout /home/user/banodoco/banodoco-workspace-runtime --agent-checkout /home/user/peteromallet/astrid-agent --output-dir /tmp/w-e10f2febca/d135-review/negative-census --expected-interpreter /home/user/work/venv-agent/bin/python` — exit **1**; **7 attempted, 4 failed**, all four module names retained, `body_authorized=false`, `test_body_run=false`.
- Recipe XML counter probe with a `<testsuites>` root and child-only counts — parser returned zero aggregate counts; FAIL against the required aggregation rule.

The interpreter used for the safe checks was `/home/user/work/venv-agent/bin/python`,
CPython 3.13.16. Observed local packages were pytest 9.0.2,
pytest-timeout 2.4.0, PyYAML 6.0.3, jsonschema 4.26.0, and referencing 0.37.0.
These local package observations do not qualify Farm.

## Scope and evidence

Read-only candidate files and prior permanent evidence were reviewed. No
Runtime/Agent checkout was changed; no Git refs were changed; no Runtime venv
was acquired; no six-file test, collection, provider, socket, Store, or broad
suite was run. The actual Farm PASS is **NOTRUN**, independent of the local
negative control.
