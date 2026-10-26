# D141ii writer-caller protected review validation

## Source scope

- Reviewed final Sol commit `66720e11e8daa26a4e192a83d592cbe5caafc109`, tree `a302a0bca0cc941dafd0122bdbdc38430ad7c33d`.
- Lineage checked from `14ccf296f3768fcde857047b263834e4a6bbe52e` through `c61c56d2f2b926febde4dad67d83d114790766ab`, `3638da72332dee5ffccacb704c9ac3c794b7c959`, and final Sol.
- Final delta is exactly `tests/packs/timeline/test_verbs_working_copy.py`; no product, generated, runtime, config, or shared-environment change.
- Runtime source is commit `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`.
- Original test blobs remain present; the whole lineage contains only the eight approved paths.

## Required targeted run

Selectors were loaded from the Sol `per-id.json` as a Python list and passed as argv, preserving the parameter IDs and spaces:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-U2-D141ii-writers-caller-review-next:/home/user/work/runtime /home/user/work/venv-agent/bin/python -c 'import json,sys,pytest; selectors=json.load(open("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-D141ii-writers-caller-sol-1331/evidence/per-id.json"))["selectors"]; argv=["-q","-o","addopts=","-n3","--timeout=45","--junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-U2-D141ii-writers-caller-review-next/evidence/targeted.xml","--basetemp=/tmp/w-c1ff1737ec/targeted-basetemp","-o","cache_dir=/tmp/w-c1ff1737ec/targeted-cache",*selectors]; raise SystemExit(pytest.main(argv))'
```

Result: **2 passed in 2.99s**, zero failures/errors/skips. The XML contains exactly the editor-namespace and generic-namespace selectors.

## Static checks

| Command | Result |
|---|---|
| `RUFF_CACHE_DIR=/tmp/w-c1ff1737ec/ruff-cache /home/user/work/venv-agent/bin/ruff check tests/packs/timeline/test_verbs_working_copy.py` | PASS: all checks passed |
| private `py_compile.compile(..., cfile=/tmp/w-c1ff1737ec/test_verbs_working_copy.pyc, doraise=True)` | PASS |
| `git diff --check 14ccf296f3..HEAD` | PASS |
| `/home/user/work/venv-agent/bin/mypy --follow-imports=silent --ignore-missing-imports astrid/packs/timeline/cli_native.py` in candidate | FAIL_ENVIRONMENT at NumPy `__init__.pyi:737` before target checking, exit 2 |
| same exact command in baseline `/home/user/work/wt/agt-U2-D141ii-writers15-return-1319` | same FAIL_ENVIRONMENT and same diagnostic, exit 2 |
| `/home/user/work/venv-agent/bin/mypy --follow-imports=silent --ignore-missing-imports --python-version 3.12 astrid/packs/timeline/cli_native.py` in candidate | PASS, no issues found |
| same target command in baseline `/home/user/work/wt/agt-U2-D141ii-writers15-return-1319` | PASS, no issues found |

Default mypy is not relabeled green and no dependency/configuration change was made. The installed interpreter is Python 3.13.16; repository target selection is Python 3.11 while NumPy stubs contain Python 3.12 `type` syntax.

## Scope limits

No full/core/browser/install/render/child/live-journey suite was run. No broad duplicate of the prior 29-node evidence was run. No source repair was made.
