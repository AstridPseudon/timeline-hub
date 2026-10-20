Completed the read-only custody ABI investigation.

- Report: [agent-activation-fingerprint-authority.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-activation-fingerprint-authority.md)
- Runtime handoff appended to `managers/runtime/INBOX.md`.
- Confirmed Agent authority: `<boot UUID>:<start ticks>`.
- Confirmed Runtime mismatch: `proc-start-ticks:<ticks>`.
- Recommendation: Runtime aligns its producer; Agent remains strict. No ABI/schema/pin changes.

Checks:

- Pure format check: PASS.
- `git diff --check`: PASS.
- Worktree clean; no activation, browser, or full suite run.
- Wrote commit message and empty `DONE` marker.

Actual activation remains blocked pending Runtime’s correction.