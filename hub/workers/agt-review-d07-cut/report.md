## D07 Review: REJECT

Reviewed `225ae22f` against `c456b328`.

Findings and exact replacement mappings are in [agent-review-d07-current.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-d07-current.md).

Required fixes:

- Add/identify native/compiler tests preserving track-scoped ripple, untouched audio, source windows, and parent extension.
- Test relocated lazy SDK exports.
- Remove stale `retime`/`retime_with_ripple` documentation and executable examples.

Evidence: targeted suite **24 passed**; target-unit rational/half-open/source-speed smoke **passed**; AST parse **passed**. No full suite run. No product files changed.

Report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-d07-cut/report.md).