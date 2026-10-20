Fixed grouped inverse refusal; removed the strict xfail after actual success. Authored guards remain intact; schema remains 53 definitions / 26 operations.

- Portable neighbours: **503 passed, 4 existing xfailed**.
- Adversarial controls: **10 passed**.
- Real-service joint controls: **8 passed**.
- Runtime neighbours: **116 passed, 2 fixture-import failures**, reproduced on untouched `b5cfce50`.
- Ruff and whitespace checks passed.

[Detailed report with exact commands, results, decisions, and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-grouped-root-inverse-fix/notes/report.md).

Commit message and `DONE` written. Private archives removed. No full suite or public freeze requested. Next: review the repair; migrate the two legacy fixtures separately.