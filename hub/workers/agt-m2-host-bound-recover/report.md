Recovered both files byte-for-byte; the old worktree remains untouched.

- Targeted tests: **106 passed**, 6 deselected.
- Central `real-pack-host-integration`: **6 passed**, 37 deselected, 374.34s.
- Ruff and `git diff --check`: passed.
- Parent SIGALRM/SIGTERM counterexamples reproduced.

Cancellation now interrupts progressing startup. The remaining constraint is the production gap between child creation and registration: safe cleanup there requires a separately authorized fix. The 180-second alarm is not a total-exit deadline. Manager review is needed before Viewing handoff.

[Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-host-bound-recover/notes/report.md). Both commit-message files are written. No full suite, install, commit, merge or push; frozen refs untouched and M2 held.