## HOLD

Reviewed commit `fabac58180e4f964e3afc47e8ce0fa9a17096ff7` (tree `be93973cae36ffa607772e6e073209cc510e467d`).

Findings:

- The old readable-audio/RIPPLE `bound.publish` positive was converted into a no-audio, preserve-timing test using monkeypatched capture/commit.
- Normal speech output lacks the required five-field media selection and Runtime producer pin; real Runtime selection retrieval is still missing.
- The known-child proof is synthetic and does not prove real durable outbox/reload/retry behavior.
- `TargetBound.publish` must remain until all callers migrate.

Evidence:

- `27 passed in 1.26s`
- `py_compile`: passed
- `git diff --check`: passed
- No full/live suite run.

Artifacts:

- [Review report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-wc5-known-intent-preservation/report.md)
- [ORCH design](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-wc5-known-intent-preservation.md)
- Completion marker created; no product changes made.