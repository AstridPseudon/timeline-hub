**No fix retained.** The smallest snapshot-copy optimization preserved observed behavior but showed no useful CPU gain, so I restored the worktree exactly.

| Accepted history | Baseline CPU | Candidate CPU |
|---|---:|---:|
| 2 | 46.872 ms | 47.571 ms |
| 4 | 119.616 ms | 120.210 ms |
| 6 | 191.411 ms | 191.498 ms |

The finite controls conserved accepted receipts, canonical-output hashes, tracked SQL/CAS snapshots, refusals, and all three end checks. Repeated live SQL and replay-key construction remain an open seam; their redundancy across callbacks is unproven.

Validation:

- Proposed candidate’s three-file subset: **196 passed, 74 deselected**.
- Finite genuine-provider controls: **3 passed**.
- Unchanged warm-forgery witness on restored baseline: **1 passed**.
- Scoped Ruff: **11 existing diagnostics → 11**.
- Scoped Pyright: **74 existing diagnostics → 74**, unchanged identities.
- `git diff --check`: passed.
- Exact four-file acceptance remains **unverified**: the central runner rejected `--timeout=45` in its file-selector argument before execution.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-history-input-cost-sol-0301/evidence/commands.json) · [Proposed D72 entry](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-history-input-cost-sol-0301/evidence/proposed-D72-entry.txt)

Provenance:

- Base/final commit: `6634a17f3ffd885567ba3c91b6c7a560df7375a4`
- Base/final store blob: `60628ab8ebd1a794d02183eacda3715780ce76b5`
- Unapplied candidate blob: `be2077b1c64efec9761b2c5cd4e565e69938655e`

No product/test changes or commit retained. Commit message and `DONE` written. Recommend manager review of the no-fix evidence before authorizing further work. No P4 original, browser, or full suite ran; no release or gate credit claimed.