# D118a parent track labels2 report

- Ran both exact nodes once against clean Runtime `42aad0e…` / tree `085a5be…`.
- Result: `2 errors in 5.08s`, both at `validation.py:650`: `candidate.timing: legacy word anchor is missing`.
- Failure occurs in shared `m1.film` setup, outside the authorized file. No source edit made.
- Checks passed: Ruff, mypy, py_compile, `git diff --check`; worktree clean.
- Target source hash preserved: `1e3517c5…`.
- Evidence saved under the assigned worker evidence directory; `DONE` and commit message marker created.
- Next step: Runtime/shared-fixture owner should address the timing/provider setup seam.