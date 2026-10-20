Fixed duplicate creation to record the two factory-derived destination root identities before recording the occurrence. Preview, raw records, immutable compilation, and reload now agree; strict inverse guards remain intact.

- Combined compile → reload → undo → redo regression and safety controls pass.
- Targeted verification: **570 passed, 1 integration test deselected**.
- Ruff and `git diff --check`: passed.
- No full suite, Runtime pair acceptance, or App activation performed.
- No blockers. `commit-msg` and `DONE` written.

[Detailed report with exact commands, results, decisions, and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-duplicate-reload-inverse-fix/notes/report.md)

Next: review the repair, then qualify the publishedS2 pair before retrying the App port.