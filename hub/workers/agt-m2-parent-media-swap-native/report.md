Implemented native parent media swaps with shared verification and guarded undo/rebase. Preserved existing replacement positives and the digest-only adapter pending paired review.

Validation passed:

- Targeted command/inverse tests: **481 passed**.
- Current private S2 Runtime acceptance tests: **22 passed**.
- Strengthened reload tests with renderer calls trapped: **2 passed**.
- Existing occurrence acceptance tests: **48 passed**.
- Ruff: no new diagnostics; `git diff --check` passed.

Exact commands, fixture provenance, decisions, and limits are in [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-parent-media-swap-native/notes/report.md).

No blocker remains. No full suite, browser journey, public pin, or legacy deletion was performed. Next step: paired Agent/Runtime contract review and consumer qualification.

`commit-msg` and `DONE` are written.