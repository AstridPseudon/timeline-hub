## F-D86 report

- No source changes made; protected test remains unchanged.
- Exact contradiction documented: `OLD` is shared across incompatible `image/png` and `video/mp4` roles, which current authenticated media admission cannot represent without changing identity/topology.
- Emitter failure remains: reload assertion does not change the managed-edge refusal.

Checks:

- Ruff — PASS
- Mypy — PASS
- In-memory compile — PASS
- `git diff --check` — PASS
- No pytest/service/full suite run.

Evidence: [sheet13-unapplied.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-sheet13-return-0405/evidence/sheet13-unapplied.md)

Marked `BLOCKED`; no commit is warranted.