## D69 report

- No product or test changes made. Existing `_check_core()` guards were retained.
- The restored original test is not safely repairable via `check()`: its fixture uses noncanonical media IDs (`m-r`, etc.), and honoring its mocked `check()` seam would bypass canonical admission.
- `_check_core()` is deliberate renderer-free validation from `f5d0b4e090`; restoring `check()` would violate renderer-off requirements.

Caller check: `_cmd_duplicate` reaches `duplicate_timeline`; restructure uses `Checkout.publish`, whose `_commit_restructure` submits through `TimelineSession`. No stale writer defect found.

Tests:

```text
4 passed in 2.89s
```

Covered valid duplicate, invalid-input all-or-nothing, renderer-off core-only duplicate, and copy-collapse rejection.

```text
ruff check astrid/sdk/timeline_duplicate.py: All checks passed
mypy astrid/sdk/timeline_duplicate.py: Success
git diff --check: clean
```

The unchanged original failing body was not rerun. Durable XML/log evidence was read: XML exit 1, 49 cases, with this failure recorded as the invalid-media/mock-seam mismatch.

Commit message recorded; `DONE` created.