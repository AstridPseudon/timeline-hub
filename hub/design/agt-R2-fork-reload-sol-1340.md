Implemented R2 repair in `commit.py` plus one focused regression file. Original tests and fixtures remain unchanged.

The prior diagnosis does **not** match base `47b744dfe9`: failures occur in reservation proof validation. Fixed shared-internal owner membership, requested-base versus landing-head checks, and complete ABI-1 native capture compatibility. Existing authenticated inverse codec handling remains unchanged. [Precise source/caller proof]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-fork-reload-sol-1340/evidence/source-caller-proof.md)

Validation:

- Four required originals: **old RED → new GREEN**; one additional ABA neighbor also recovered.
- Fork/M1/inverse neighbors: **345 passed**.
- Strict controls: **17 passed**; null/validation: **46 passed**.
- Source-copy/v2/forged-authority controls: **134 passed**.
- Qualified mypy, vendor lock, artifact manifest and diff checks passed.
- Ruff retains three pre-existing import-order findings; new regression file is clean.

[Exact pytest commands](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-fork-reload-sol-1340/evidence/fork-neighbors-command.json>) and adjacent command manifests, XML memberships, source hashes and original AST comparisons are retained in evidence. No full/gate/HTTP run performed.

Candidate tree: `e6cab01a3540302e7639a883ee777573147c004d`. Commit SHA awaits harness commit. `commit-msg` and `DONE` written.

Next: independent Luna security/core review, particularly native-only compatibility and base/landing authority.