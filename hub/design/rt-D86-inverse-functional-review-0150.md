## Report

**PASS_SOURCE** for candidate `bc569d8140ee…`: the one-line correction at `test_commit_runtime_shared_inverse.py:50` reads `payload.metadata.title`, matching `shot.set`’s production payload mapping.

- Five test bodies, fixture params/IDs, all branches, 29 assertions, and both refusal paths are AST-identical.
- Physical shared-placement setup and real Runtime/provider paths remain unchanged.
- Source hashes: baseline `2657e31b53fa…`; candidate `b2a44a6c474f…`.
- Ruff and mypy passed for baseline and candidate-shadow sources.
- In-memory compile/AST checks and `git diff --check` passed.
- No pytest, collection, helper/function execution, browser, or service tests were run.

Remaining finding: the five `[original-third]` failures are owned by the original test input at `test_commit_runtime_shared_inverse.py:120`. `capture_move` defines `on` as absolute global time; source fixture data gives occurrence-3 a 1.8s bound at 3.3s, so `3.5 - 3.3 + 1.8 = 2.0s`, exceeding the bound. Runtime correctly rejects this at `validation.py:252`, reached through `commit.py:1410`. This is an invalid original setup, not established caller drift or a product defect; it remains unapplied.

10077 outcome evidence: `handoff-rt-D86-10077-outcomes.tsv:91-100` records exactly five setup `KeyError: 'name'` cases and five interval failures. No blockers. Commit message and `DONE` marker were written.