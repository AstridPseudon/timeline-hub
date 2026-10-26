# Validation

The same author/reviewer invocation is:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P evidence/check-source.py check
```

Result: exit 0, `control_status=PASS`,
`pair_status=WAITING_FOR_GENUINE_CONTROLLER_BINDING`, `admission_cases=10`,
`lifecycle_cases=36`. The retained control log is
`control-logs/check-1792999454132331673.json`.

Direct checks also passed:

```bash
bash -n evidence/command-cut.sh evidence/command-pristine.sh evidence/controller-continuation.sh evidence/tiny-controls.sh evidence/positive-stub.sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P -c 'import ast, pathlib; [ast.parse(pathlib.Path(p).read_text()) for p in ["evidence/check-source.py", "evidence/binding-source.py"]]'
evidence/controller-continuation.sh check
```

The checker executed the unchanged production launcher controls: positive
exit 17 with one stub call, poison exit 1 with zero calls. Its isolated binding
fixture exercised one positive only in the explicit fixture path and nine
negative path/hash/tuple/brief/service/request cases through the same consumer;
fixtures cannot pass `consume`. The 36 lifecycle controls preserve body,
monitor, evidence, raw/JUnit, KEEP, cleanup, disk and final-status propagation.

No pytest collection/body, request-test, test-run, row installation, service
submission, P4, heavy suite, product import, lint or typecheck was run. Lint
and typecheck are N/A because these are operational evidence scripts, not
product sources. Python syntax/AST and shell syntax were checked.

The copied disk trace is retained from the prior source-only control packet,
with its disclosed historical gap preserved. It remains above the continuous
4 GB stop; it is not a claim of a new heavy run.
