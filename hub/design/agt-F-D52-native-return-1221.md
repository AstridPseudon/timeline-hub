## Report

Implemented the D52 return fix.

- Moved sheet authentication setup into file-local helpers/fixture; restored the original sheet test body AST.
- Moved P4 publication registration into `_open_real_document`; restored the original P4 body AST.
- Text-node ASTs remain identical.
- Structure test remains the previously approved v2 migration.
- No product/shared-helper changes.

Tests:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime:/home/user/work/runtime/packages/python ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --tb=short [five selectors]
# 5 passed in 4.06s

... pytest ... [four assigned files]
# 115 passed in 22.08s
```

Static checks:

- Ruff: passed
- Mypy: `Success: no issues found in 4 source files`
- `git diff --check`: passed

No blockers. Full/gate suites were not run per instructions. Commit message and `DONE` marker are in place.