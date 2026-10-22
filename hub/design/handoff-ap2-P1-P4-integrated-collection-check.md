# P1/P4 integrated collection check: PASS

- Integrated source SHA: `250db8c8d9f5bda5f0130ecf3fe46bf78e298641`
- Integrated tree SHA: `b4e279948ada77ba49d00d2d1a176d67fecbc21d`
- Worktree status after checks: clean.

Exact targeted checks and results:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_case_corpus.py tests/sdk/test_p4_commit_cases.py
15 passed, 2 warnings in 4.40s

/root/.local/bin/ruff check tests/sdk/test_p1_case_corpus.py tests/sdk/test_p4_commit_cases.py
All checks passed!

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_case_corpus.py tests/sdk/test_p4_commit_cases.py
Success: no issues found in 2 source files
```

Pytest warnings were the environment's unknown `timeout` and `timeout_method` config options. No tracked files or dependencies were changed. Collection only: this does not prove R1 `doc.patch`, the App mixed chain, G2/G3/R2 lifecycle, H3 GO, or P4 execution credit.
