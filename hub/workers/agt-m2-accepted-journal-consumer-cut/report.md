Implemented AG01’s first accepted-history cut.

- Removed duplicate local `kind="publish"` journal writes from [`publish.py`](/home/user/work/wt/agt-m2-accepted-journal-consumer-cut/astrid/sdk/timeline/publish.py).
- Preserved draft/legacy journal records, Runtime receipts, and outbox behavior.
- Updated the regression test.

Validation:

- Targeted suite: **139 passed**.
- Ruff import checks: **passed**.
- Central Runtime integration was unqualified: no Runtime checkout available; 1 skip, exit 5.
- No full suite requested.

AG01 remains in progress; WC7/WC8 remain held. Report and commit message written; `DONE` created.