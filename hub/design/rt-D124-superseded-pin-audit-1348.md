# D124 superseded-pin audit decision

Audit `rt-D124-superseded-pin-audit-1348` is **SAFE for manager-only KEEP release/bin/recycle** of exactly:

- `/home/user/work/wt/agt-pin-07ff6c71` at `07ff6c71d301d6cdc230664c4ed2cc4b4bf2e6e5` / tree `7f8f324e85381831acdfdb9bf256b2942c7b589e`;
- `/home/user/work/wt/rt-pin-42aad0e9` at `42aad0e92f6da8ea83dd0a382a87e3acd12651b0` / tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`.

Both are detached and clean, with zero status entries and zero staged/unstaged diff. Their orchestration KEEP markers are present and empty, and neither pin worker has a running marker. Exact process path matchcounts are zero for cwd, exe, root, maps, fd, cmdline and environ; all inspected fields were readable. No exact-path use was found in pending/provisioning/superseded queue state, test request/snapshot/extension state, or suite/env/lease/live-registration state.

The one active Farm STATUS reference to Runtime `42aad0e9` is classified **active source identity on separate Farm checkouts/receipts**, not active use of the exact pin worktree. Runtime STATUS classifies the old `07ff`/`42aad` preparation as zero-body and superseded by Agent `16bb`/Runtime `5e9ad`. Preserve that active Farm checkout and every branch, artifact, report, receipt, and zero-body preparation record; only the two exact worktree paths are eligible for manager action.

Composition source remains read-only and clean at `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`. No source, Git, pin, process, test, or body mutation was made by this worker. Full evidence: `workers/rt-D124-superseded-pin-audit-1348/evidence/audit-summary.md` and `.json`.

