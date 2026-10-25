## Report

Produced corrected artifacts:

- [JSON](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-element3111-correlation-return-0221/evidence/p2-element3111-safe-facts-corrected.json>)
- [Markdown](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P2-element3111-correlation-return-0221/evidence/p2-element3111-safe-facts-corrected.md>)

The immutable 0212 packet is explicitly superseded. Dump identity and ordinal mapping are now `UNKNOWN`; ordinal 3 remains correlated only to the App `apply-1` request. Global two-capture watchdog budget, timer/follow-up/cancellation semantics, all hashes, timings, XML facts, and phase cardinality were preserved.

Validation:

- `jq empty`: PASS
- Retained artifact/source SHA-256 cross-check: PASS
- Cardinality/UNKNOWN/budget consistency assertions: PASS
- App worktree status: clean
- Product tests/typechecks/lint were not run per task scope.

Commit message written and `DONE` marker created. No blockers. Recommended next step: manager publishes the corrected packet and marks the original 0212 packet superseded.