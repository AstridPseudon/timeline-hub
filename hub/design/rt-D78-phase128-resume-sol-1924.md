Completed the saved D78 interpretation. Product/tests and worktree remain unchanged; commit message and `DONE` written.

- Authentic SAFE128 input matches **13,355 bytes / SHA256 `280f186c…85a8836`**.
- Ordinal 1 completed provider, accept and receipt calls. Provider elapsed **1,724.956 ms**.
- Ordinal 2 entered `TimelineCommitStore.accept` at **35,259.487 ms**. Last retained event: authorization entry at **45,430.793 ms**. Later outcome is **UNKNOWN** after event-budget exhaustion.
- Found two concrete observer defects: stale handler/thread mappings misattribute later responses and consume budget; generator resume resets admission tracking and hides lock completion. Retained a minimal [unapplied proposal](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D78-phase128-resume-sol-1924/evidence/observer-fix.UNAPPLIED.diff), with owning file and regression requirements.
- Peer “two occurrences” for ordinal 1 are start/end pairs, not two invocations. Ordinals cannot establish daemon or native-seed identity.
- Actual13100 and all five D80 failures occurred during native-seed setup, before intended gestures. No blocked Python frame, supervised PID or all-thread dump exists; no attach was attempted or refused.
- Supplied publication was locally **0644**; the retained byte-identical copy is **0600**.

Verification: offline interpretation command exited **0**, validating hash, fields, counts, ordering and source hashes. `git diff --check` passed; `git status --porcelain=v1` was empty. **No tests or live operations ran.** Exact commands, logs and exits accompany the [detailed interpretation](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D78-phase128-resume-sol-1924/evidence/phase-interpretation.md).

Next: owner review of the observer fixes and correlation of existing per-launch sinks/native-seed acceptance files. Full D78 cause resolution still needs an authentic owned all-thread dump; no auth, performance or concurrency cause is established.