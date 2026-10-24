## Report

Created the review-only artifacts:

- [proposed.patch](/home/user/work/wt/app-P3-recovery-proposal-1722/proposed.patch)
- [fullproposal.md](/home/user/work/wt/app-P3-recovery-proposal-1722/fullproposal.md)

The proposal replaces the fixture-only recovery-button click with observation of production sole-owner automatic recovery, holds the exact retry across Runtime restart, and preserves all existing wire, retry, history, undo, and canonical assertions.

Verification:

- `git apply --check proposed.patch` — PASS
- Protected source remains unmodified.
- No browser, service, full-suite, or original P3 rerun performed per instructions.

Existing P3 result remains UNKNOWN beyond the missing button failure; no product defect was established. Independent read-only proposal review and ORCH approval are required before applying the patch.

Commit message and `DONE` marker were written.