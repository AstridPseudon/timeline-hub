APPROVE — bounded three-file patch.

- Source: `46f2b9e2ff5d74f03249b0f90bc9b00910b23856`, parent `65c87dd5`; exact `+67/-2`, no product edits.
- Central render qualification: `2 passed, 1 deselected`.
- Focused process tests: `61 passed, 5 deselected`.
- Focused custody/pidfd tests: `12 passed, 564 deselected`.
- Broader custody run had 24 sandbox socket `EPERM` failures; no changed-path failures.

Verified exact retained-incarnation proof, PID-reuse refusal, custody/session safeguards, and teardown refusal preservation. Full review: [agent-review-d13-main-custody-patch.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-d13-main-custody-patch.md).

Commit message written, worktree clean, and `DONE` created. Landing plan requires porting only this narrow delta onto clean current013; do not merge the D13/014 tree wholesale.