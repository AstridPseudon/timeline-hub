# D136a/D100 command results

## Source and focused checks

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d136_fps_upstream_compat.py
57 passed in 3.24s

RUFF_CACHE_DIR=/tmp/w-b2cbf5d8b9/d136a-ruff /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py
All checks passed!

MYPY_CACHE_DIR=/tmp/w-b2cbf5d8b9/d136a-mypy /home/user/work/venv-agent/bin/python -m mypy astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py
Success: no issues found in 3 source files

PYTHONPYCACHEPREFIX=/tmp/w-b2cbf5d8b9/d136a-compile /home/user/work/venv-agent/bin/python -m compileall -q -f -d /tmp/w-b2cbf5d8b9/d136a-compile astrid/sdk/timeline/validation.py astrid/sdk/timeline/_timing_evaluators.py tests/sdk/test_d136_fps_upstream_compat.py
PASS

git diff --check
PASS
```

## Exact original9 command

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<ownsource>:/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --junitxml=<private-own9.xml> <the exact nine retained selectors>
```

The concrete selectors are recorded in `predicate-map.json`. Result: exit 1;
9 tests collected, 9 setup errors, 0 failures, 0 skipped, 0 passes; XML
reported time 34.783 seconds and measured wall duration 35.996764405 seconds.
All nine first seams were `provider intermediate command lacks an
authenticated physical observation`.

## Guards

Runtime pin guard passed: clean checkout, commit
`ab1e4f6141987706132916e2da16477f5a019464`, tree
`7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`. Free-space admission passed at
5,316,198,400 bytes before the run. Post-run worktree scope and diff check
passed. No broad/full/browser/socket/collector/acquisition run was made.
