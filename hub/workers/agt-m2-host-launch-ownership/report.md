Implemented cleanup from the returned child handle through birth capture, registration and readiness polling. Replacement registrations remain untouched.

- Local targeted tests: **177 passed, 5 deselected**.
- Central targeted tests: **197 passed, 5 deselected**.
- New-test Ruff check and `git diff --check`: passed.
- Ruff baseline comparison exits 1 because findings decreased by three; baseline left unchanged.

Pre-return interruption remains unverified. No implementation blocker; integration remains held pending M1.

[Report with exact commands, guarantees and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-host-launch-ownership/notes/report.md). Both commit-message files are written for the harness.