# D118a Native Checkout4 Report

- No source changes made; assigned test remains byte/AST/call-AST identical to base.
- Exact four-node run against Runtime `42aad0e…` / tree `085a5be…` reached the real provider but all errored during shared M1 fixture setup:
  `astrid/sdk/timeline/validation.py:650` → `native_word_anchor.py:169`, `candidate.timing: legacy word anchor is missing`.
- This is the known shared `m1.film` legacy-word-anchor boundary, outside this task’s allowed file. Checkout4 behavior remains unverified; no speculative caller/test fix applied.

Checks passed:

- Ruff
- Mypy with `--follow-imports=skip`
- `py_compile`
- `git diff --check`
- Byte, AST, and call-AST conservation
- Target absent at pristine/D60 commit `08e6b905`

Worktree is clean. Commit message and `DONE` sentinel were written.