## Report

No code changes were made. The exact own3 run reproduced all three failures on Runtime `42aad0e...`, tree `085a5be...`:

```text
3 failed in 4.62s
```

Cause: production `astrid/sdk/timeline/commit.py:369-373` unconditionally adds hydrated `pinned_documents` to the manifest before command consumption, changing the dependency manifest and parent revision. This is outside the allowed test file, so no test weakening or workaround was applied.

Checks passed:

- Ruff
- mypy `--follow-imports=skip`
- `py_compile`
- `git diff --check`
- AST conservation: 15 assertions, 43 calls, unchanged

The allowed test remains SHA-256 `20ae264e...`; pristine `08e6b905` does not contain it. Evidence is under the worker evidence directory, `DONE` was created, and the required commit message was written.