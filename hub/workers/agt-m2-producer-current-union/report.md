Composed the current-source union with both reviewed deltas; pins and endpoints remain unchanged.

- **555 targeted tests passed.**
- Real Runtime qualification: **4 passed, 1 strict xfail**. Preview rejects Agent’s normalized guard record.
- Runtime `6023cfb` also lacks the public producer schema claimed in the brief.

[Report with exact commands/results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-producer-current-union/report.md) · [Schema hash, operations and source handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-canonical-current-union.md)

`commit-msg` and `DONE` are written. Next: harness commit, manager freeze, then Runtime compatibility fixes before activation.