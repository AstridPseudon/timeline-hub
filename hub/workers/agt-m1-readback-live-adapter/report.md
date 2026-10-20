## Done

- Wired `RuntimeRevisions` through public `RemoteTimelines.history`; direct `WorkspaceClient.list_timeline_commits` remains supported.
- Preserved fallback only for genuinely absent/legacy history methods; route errors now surface.
- Enforced exact `summary.revision_id` identity in `RuntimeRevisions.get`.
- Added real facade fixture coverage for repeated publications.
- Published the call path in shared `m1-agent-coordination.md`.
- Wrote harness commit message.

## Verification

- Ruff + `git diff --check`: passed.
- Targeted suite: `170 passed, 1 skipped`.
- Focused revisions/history suite: `38 passed`.
- No full, socket, or browser suites run.

No blockers.