# D136a/D100 joined command results

## Source controls

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d136_fps_upstream_compat.py
45 passed in 2.56s

/home/user/work/venv-agent/bin/ruff check astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py
All checks passed!

/home/user/work/venv-agent/bin/mypy astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py
Success: no issues found in 3 source files

python -m compileall -q -f -d /tmp/d136a-compile astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py
PASS

git diff --check
PASS
```

## Sole original9 command

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<ownsource>:/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=<private-own9.xml> <the exact nine retained selectors>
```

Result: exit 1; 9 tests collected, 9 setup errors, 0 failures, 0 skipped, 0 passes; XML-reported test time 10.88s and wall time 11.977741395s. First common seam: `candidate: all authored fps declarations must retain their typed locations`.

Admission was 5,039,394,816 free bytes before launch and 5,038,260,224 after. Agent source hashes and all three Runtime pin module hashes were identical before and after.
