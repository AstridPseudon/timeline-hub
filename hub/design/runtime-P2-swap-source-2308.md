## Report

- Diagnosed the exact refusal: `commands[1].created` was omitted by App SWAP, while Agent generated one occurrence-asset creation claim for the newly imported alias. Runtime correctly rejected the mismatch at `runtime_protocol/timeline_commit_auth.py:318-327`.
- Production owner: App’s `shotTimelineDataProvider.ts:866-868`.
- Minimum correction: add the conditional asset `created` claim, matching the existing ADD logic; do not weaken Runtime validation.
- Confirmed C0 requires caller-declared canonical `created` refs in the same command envelope.
- Evidence: [source comparison](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-swap-source-2308/evidence/source-comparison.md), [verification](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-swap-source-2308/evidence/verification.md).

Tests:

- Agent targeted controls: `6 passed`.
- Runtime guard controls: `2 passed`.
- No browser/full/core/profile rerun; no product or test files changed.
- Runtime worktree remains clean. DONE and commit message were written.