# WC4 deletion-ready review

Approved candidate `e36b505656f5b98c8bab3495c38f5d04fe8fbee5` (tree `cd13be81bf14c05e5acc7089a1e66d109000c61d`) for merge. Recommend marking WC4 `DELETED` and retaining permanent tests.

Findings:

- Old whole-parent publisher imports, call, and fallback are deleted from `timeline_elements.py`.
- Consumer route remains compatible: public helper → existing outbox → `/v1` commit.
- Original P1 authority, legacy HOLD, retry/restart/pagination, F1 inverse guards, bool/number intent, opaque fields, and foreign-owner refusal are preserved.

Evidence:

- Direct helper: 38 passed.
- Helper/lifecycle: 19 passed, 40 deselected.
- Authority tests: 17 passed, 10 deselected.
- F1 tests: 5 passed, 27 deselected.
- Foreign-owner test: 1 passed, 58 deselected.
- Ruff: passed.
- `git diff --check`: passed.

No full suite, App/browser, renderer/audio/pixel, or macOS qualification claimed.

Reports: [design review](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-wc4-deletion-ready.md>) and [worker report](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-wc4-deletion-ready/notes/report.md>). `DONE` and commit message were written; source worktree is clean.