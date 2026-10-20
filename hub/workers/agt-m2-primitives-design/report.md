Updated [m2-move-draft.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-move-draft.md) with ordered restoration, staged guarded inverse, M1 compatibility, overlap handling, and precise future acceptance nodes.

- Group ownership/projection remains pending; speculative fields and group-ref support removed.
- Proposed primitives reuse existing fields/history; no new store or undo path.
- Offline `probe.py` and `check_sources.py`: **exit 0**. All three App success assertion blocks preserved.
- Repository tests **UNRUN by design**. Agent worktree clean; no merge/full-test request.
- After M1 is recorded: implement shared primitives, then staged inverse, then move-set/capture. Group work waits for the ownership decision.

[Full report with exact commands, sources, tradeoffs, and blockers](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-primitives-design/report.md).