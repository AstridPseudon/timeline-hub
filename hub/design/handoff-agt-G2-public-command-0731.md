# G2 public command source callable (qualification in progress)

Worker `agt-G2-public-command-0731`, branch `tl/agt-G2-public-command-0731`.
Worktree `/home/user/work/wt/agt-G2-public-command-0731`; base HEAD `d24da4af0f1ca83880b4b9ef57559e28ebe52a2a`. Changes are uncommitted; harness owns the resulting commit SHA. No Git writes were performed.

Production seam: `commit_session.Timeline._execution_bundle` fetches the existing exact `_basis` revision/publication pair through `store.fetch_bundle` / the preserved `_remote_timeline.open_bundle` canonical reader. The verified document is private to the handle, supplied only to execution/emitter copies; `.bundle` and `._command_bundle` stay portable. Child free-edit emission receives matching hydrated before/after copies. Function evaluations use their own pair; accepted documents seed the private cache.

Initial new canonical-reader regression: **6 passed** (direct two-step patch, accepted provider/history, portable restart, child free edit, changed pair, foreign source, outside closure, wrong previous value). Existing targeted vectors: **66 passed** in the prior combined run, whose two new failures were test-adapter receipt format issues now corrected. Final combined run and quality checks pending. No HTTP/originalten/conflict-node/full reruns.

Proof can prepare against this source path now; do not claim integrated qualification before harness commit/review/merge.

Source SHA-256:
- `astrid/sdk/timeline/commit_session.py`: `72d1d68b69dd0efb63d4a1e4727f8d1f8861e509f98da3016e8265ef67cee4d7`
- `tests/sdk/test_timeline_public_command.py`: `2e6a728a352ad565d59b5bcaa2318ee868776959e96769ec49fb9ed48d6e05eb`
