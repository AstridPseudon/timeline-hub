Implemented a **HELD F-D86/R2 candidate** in [_step_undo.py:349](/home/user/work/wt/agt-R2-restore-order-sol-0403/astrid/sdk/timeline/_step_undo.py:349): 10 added lines retain the complete reversed authenticated step patch for eligible ordinary restore stages. The existing independent execution-effect comparison remains unchanged.

Restore stages carrying derived clip-timing caches retain their existing path because cache lookups depend on record identity. Runtime, validators, tests and other producer seams are untouched.

Static checks passed:

```bash
/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_step_undo.py
/home/user/work/venv-agent/bin/python -m mypy --no-incremental --follow-imports=skip --ignore-missing-imports --cache-dir /tmp/w-e7631082a1/restore-order-static/mypy-candidate astrid/sdk/timeline/_step_undo.py
git diff --check
```

Parent Ruff/mypy also passed using stdin/shadow-file baselines. In-memory compilation passed; removing the added branch reproduces the parent module AST exactly, including all 42 existing raises. Mypy’s default untyped-body limitation applies.

[Evidence, exact baseline commands and regression proposal](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-restore-order-sol-0403/evidence/source-trace-and-regression-proposal.txt) total approximately 13 KB. No functional tests or services ran.

**Unverified:** ID5 and the other three historical cases. Qualification still needs the complete authenticated source records, candidate PreparedCommit/ranges/bindings, and segment closures. The other cache/range and parent-projection seams remain unapplied.

Next: independent protected core/custody review, then exact MAIN candidate proof before merge. Commit message and `DONE` were written; no git commit or ref changes were made.