# Validation

## Exact author command

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-return-0735/evidence/check-source.py check
```

Exit `78`: missing retained `0249/exit`; manifest audit found 45/45 retained
original/control paths absent. No missing evidence was reconstructed.

## Direct controls

```text
bash -n <command-cut.sh> <command-pristine.sh> <controller-continuation.sh> <tiny-controls.sh> <positive-stub.sh>
```

Exit `0`; five shells parsed.

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P -c 'import ast,pathlib; [ast.parse(pathlib.Path(p).read_text()) for p in [<check-source.py>,<binding-source.py>]]'
```

Exit `0`; two Python files parsed.

```text
/bin/bash <controller-continuation.sh> check
```

Exit `0`; source-only status, no request/test-run/wait/row/body.

The exact isolated producer/consumer fixture functions from `check-source.py`
were invoked in private reviewer controls: controller route exit `0`, two
distinct returned IDs, row restoration; admission `10` cases (1 positive, 9
negative); lifecycle `36` cases, all expected exits. These are fixture-only and
authorize no live admission.

The unchanged tiny launcher control was run directly. Positive exited `1` with
zero calls because the pinned Node/runtime profile is absent; poison was not
reached. Required `17/1` and `1/0` evidence is therefore unavailable.

No pytest collection/body, product test, request-test, test-run, wait-test,
registry mutation, row installation, service body, full suite, lint, or
typecheck was run. Lint/typecheck are N/A because this is an operational
evidence review, not product source. The current integrated tuple worktrees
were read-only checked clean. The pristine checkout paths were absent.
