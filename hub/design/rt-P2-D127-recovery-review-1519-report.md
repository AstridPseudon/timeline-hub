# P2 D127 review — FAIL / not ready

Source: base `453b3e6f92045980219ec4948419ee5ad25c817d`; candidate tree `a9e652a8502f6f20742406162998cf12060679bc` (`tl/rt-P2-D127-recovery-review-1519`). No product or existing-test edits.

Blocking finding: `_replacement_connection_is_current()` validates only canonical path and WAL mode, not the mounted connection’s physical DB/WAL identity. An adversarial probe showed a stale quiescent connection can return authenticated history after the canonical DB is replaced with tampered contents. Add physical identity binding or reopen-and-verify fail-closed before adoption.

Evidence: [review.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-D127-recovery-review-1519/evidence/review.md)

Tests:

- History controls: 81 passed.
- Adjacent controls: 247 passed, 40 deselected.
- Compileall and `git diff --check`: passed.
- Ruff: 10 inherited diagnostics, zero new.
- Pyright: inherited diagnostics only; none at changed lines.
- Adversarial identity probe: reproduced stale-history authorization, 1 passed.

The two parent authorizer failures denying `PRAGMA data_version` remain explicitly preserved from the author comparison: 154 passed, 84 deselected, 2 pre-existing failures.

Authentic real-provider SWAP replay: **NOTRUN**. Launch `d22e9a6e` has the observed recovery stack, but request binding remains UNKNOWN; no substitute replay was fabricated.