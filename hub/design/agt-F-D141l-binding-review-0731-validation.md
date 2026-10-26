# Validation

Reviewed source: Composition commit `6a2d1c22ec800229812f4d756d7198aece8111ed`.

The exact author command was run in the original author worktree:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P evidence/check-source.py check
```

Result: exit `0`; `control_status=PASS`, `pair_status=WAITING_FOR_GENUINE_CONTROLLER_BINDING`, `admission_cases=10`, `lifecycle_cases=36`. The newly written control log was:
`/home/user/work/wt/agt-F-D141l-controller-binding-prep-0718/evidence/control-logs/check-1792999830236902248.json`.

Reviewer checks on the committed packet:

```bash
bash -n evidence/command-cut.sh evidence/command-pristine.sh evidence/controller-continuation.sh evidence/tiny-controls.sh evidence/positive-stub.sh
```

Result: exit `0`.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P -c 'import ast, pathlib; [ast.parse(pathlib.Path(p).read_text()) for p in ["evidence/check-source.py", "evidence/binding-source.py"]]'
```

Result: exit `0`.

```bash
evidence/controller-continuation.sh check
```

Result: exit `0`; `WAITING_FOR_GENUINE_CONTROLLER_BINDING`, no request-test,
test-run, row install, heavy body, or floor admission.

```bash
evidence/controller-continuation.sh materialize /tmp/d141l-missing-controller-binding-0731.json /tmp/d141l-output-0731
```

Result: refused with exit `78` because the required binding file is absent.

The author's control log reports the allowed isolated launcher and lifecycle
results: positive `17/call=1`, poison `1/call=0`, 10 fixture-only admission
cases, and 36 lifecycle cases. No request-test, test-run, pytest body,
collection, full suite, product import, lint, or typecheck was run for this
review. Lint/typecheck are N/A because all reviewed files are operational
evidence scripts.

The source packet's committed trace is historical 06:38–07:02 evidence. Four
reviewer samples at 5-second cadence were collected after review work began,
from 07:31:33Z through 07:31:48Z, all above the 4 GB stop. They do not repair
the missing pre-work trace and are reported only for transparency.
