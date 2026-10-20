## WC3 review: APPROVE

- Branch/tree: `tl/agt-review-wc3-current014-native-final` / `3dae5bd4`
- Bounded scope: candidate commit atop `e86f44d0`, five changed files only.
- Tests: 22 focused, 154 neighbouring, and 22 pinned-a0 Runtime-provider tests passed.
- Ruff and `git diff --check` passed; worktree is clean.
- Exact retry identity, receipt/base preservation, malformed/unrelated refusal, opaque/order/mirror preservation, and legacy API behavior verified.
- Actual HTTP lost-ACK remains unverified: evidence uses a transport fake plus direct `RuntimeService`.
- WC3 ledger row should remain non-DELETED until this body is integrated and replaces the old implementation on `tl/integration`.

Reports, commit messages, and `DONE` marker written.