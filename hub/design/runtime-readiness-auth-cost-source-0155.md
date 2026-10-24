Implemented the Runtime fix on `28bb65668`: the production caller carries the fully authenticated head entry through one locked history read, reducing repeated bound authentication from **3 calls to 1**. No persistent cache or verification guard was removed. Existing tests were unchanged.

Uninstrumented observations using the frozen fixtures:

| Fixture | Parent direct / door | Candidate direct / door |
|---|---:|---:|
| native21 | 5.715 / 5.944s | 1.885 / 2.010s |
| P1 | 0.917 / 0.971s | 0.376 / 0.334s |

Every reply contained exactly two history entries; direct and door replies matched.

Exact acceptance command, executed through the central service:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_history_boundaries.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_history_authenticated_read.py
```

**145 passed in 53.60s.** The new regression fails on the parent with three authentications and passes on the candidate with one. It covers reply equality, pagination, distinct same-revision publications, later-request revalidation, tamper refusal, authorization precedence, and no writes.

Additional checks:

- `pyright --pythonpath /home/user/work/venv-runtime/bin/python --outputjson runtime_protocol`: parent/candidate both 1,449 existing diagnostics; **zero new or removed identities/multiplicities**.
- Ruff changed files: 44 unchanged existing findings; new Python files pass.
- `git diff --check`: passed.
- Credential scan and capture-manifest integrity: passed.

[Captures, source/state identities, and validation manifest](/home/user/work/wt/rt-R-readiness-auth-cost-sol-0155/diagnostics/readiness-auth/manifest.json) are retained.

**Historical browser hang cause remains UNKNOWN.** These measurements establish reduced authentication cost, not historical deadline causality. No original journey, browser, or full suite ran.

No blockers. Commit message and `DONE` are written. Next: independent Luna review, then the normal merge queue.