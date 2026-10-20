## Report

Implemented bounded top-level `clip.opacity` support through existing closed `clip.set` SET/CLEAR semantics.

- Added schema support for raw opacity `0..1`; no alias, params bypass, clamp, DTO, or new operation.
- Added conformance for Main-shaped capture, presence/null/zero, inverse/redo, occurrence isolation, opaque-neighbor preservation, strict ABA, and disjoint rebase.
- Published handoff: [agent-opacity-private-source-proposal.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-opacity-private-source-proposal.md)
- Candidate tree: `ff2a0144563bb27b7a1169ae0276c3e3d1b7b195`
- Schema SHA-256: `110165ab9f7e4be3e9766d06b5ceacab8c5e8c7cc12e7180929005b67bcc82d6`

Tests:

- Targeted opacity suite: `111 passed`
- JSON validation, Ruff, and `git diff --check`: passed
- Neighbor schema suite: `178 passed, 7 expected frozen-schema/hash mismatches`; frozen 613/6ba artifacts were intentionally unchanged.

No full suite, generation, pin, integration, or consumer activation was performed. Commit message and `DONE` marker written.