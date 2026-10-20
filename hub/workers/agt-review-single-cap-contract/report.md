## Result: ACCEPT

Reviewed candidate `5bf1731a` independently.

- Exact raw fixture SHA and byte comparison passed.
- Normal managed projection/serialization preserves authored hold5, projects hold4, and yields public12 f90=1, f105=0.5, f119 present, f120 absent.
- Targeted suite: **152 passed, 2 unchanged xfails** (audio vectors 10–11).
- Direct Node v20.19.4 public evaluator check passed.
- Ruff and `git diff --check` passed.
- No production code, pin, Runtime/product schema, or worktree changes.
- No new xfail; superseded fake raw-input production xfail was not ported.
- App policy remains external; no real Runtime, pixel rerun, audio parity, or owner-film claim made.

Reports written:

- [design review](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-single-cap-contract.md)
- [worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-single-cap-contract/notes/report.md)

Commit message and `DONE` were created.