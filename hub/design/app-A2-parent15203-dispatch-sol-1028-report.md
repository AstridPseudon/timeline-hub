Current parent15203 starts mouse-down while the mounted clip has an `inert` ancestor. The connection pill already says connected, but the gate remains closed until its leaving panel exits. Inert clears during the subsequent mouse move. The clip’s retained position and selection remain unchanged; the network contains zero commit POSTs.

This establishes a readiness failure before clip gesture admission. Exact callback execution, capture refusal, save scheduling, and IndexedDB outbox state remain **UNKNOWN**. No Runtime cause is attributed.

The source path is gesture → upstream track management → mounted capture → `localSaveSession` → shared outbox → provider transport. The separate `commitSession` move port is not this parent caller.

No production or protected-test files changed. The [unapplied proposal]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A2-parent15203-dispatch-sol-1028/evidence/proposal.patch) adds the existing connection-panel removal check to tour readiness.

Verification:

- `python "$TMPDIR/inspect_parent15203.py"` — PASS: reconstructed nine bounded snapshots and verified inert timing, unchanged geometry, and zero commit POSTs.
- `git apply --check <worker>/evidence/proposal.patch` — PASS; unapplied.
- `git diff --check` — PASS.
- `git status --porcelain` — empty.
- Protected-file SHA256 comparison — **487/487 identical**.

No tests, browser/service runs, typechecks, or lint runs were performed because no code edit was justified. No oldRED/newGREEN or original-browser GO is claimed.

[Safe facts and source citations](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A2-parent15203-dispatch-sol-1028/evidence/facts.json) retain the limits and unchanged guarantees. Next step: orchestrator scope handback for the protected readiness proposal, followed by independent core/protected review and authorized validation. Commit message and `DONE` are written.