# Runtime F full rerun review handoff — 2026-10-23

Classification is **FAIL** and the authorized full failure is retained:
`runtime-full-1023091021-9458` on Runtime commit `a01e9d806` / tree
`645de16949982723f67db58be204611cf0a5bb95` reported `6237 passed, 1 failed,
0 errors, 26 skipped, 15 xfailed, 12 warnings` in `430.86s`, exit `1`.

The sole node is
`tests/test_timeline_current_union_contract.py::test_public_python_union_types_and_nested_item_references_resolve`,
failing because the public package root lacks `astrid_runtime_client.DocPatchArgs`.
`DocPatchArgs` exists in the generated DTO module and schema. Both the package
root and `generators/python_client_init_template.py` omit the import and
`__all__` entry. The exact bounded probe reproduced the failure in `1.02s`.
This is the known real R0/generated-client public-namespace regression and
P1/freeze gate, not an R2r provider/store failure, upstream-4563 baseline, or
PLAN deferral. Preserve this failed node; do not pin, add a tuple, or apply a
product fix in this review.

The previous `8246` full had `31 failed, 6162 passed, 45 errors`; its 29
fixture failures plus 45 setup errors and stale-envelope assertion are cleared
by the exact targeted current-tree lane `runtime-reference-fixture-agent-current-integration-1023090143-10656`,
which selected those files/nodes and passed `297/297` in `53.36s`. Thus all 75
previous non-export nodes are cleared. This is suite-level evidence, not a
claim of verbose per-node traces.

Captured full external identities were Agent
`2e21af300abbefc8afbad217189fa4715cf82616`, App
`2d3d14d998be2b59fb017b4c0f2458c3a7340423`, and Composition
`635f4de06fda22a85fc2e4cfc764d0153a4c9f40`. No newer-head, unmerged D17, or
inverse-auth claim is made. Current relevant source blobs match the prior
captured tree: root `665d9955`, template `f1b00f99`, DTO
`8cfbcc41`, test `4a10974a`; current worktree is clean and `git diff --check`
passes. No full rerun was requested.

See the worker evidence report for raw paths, exact commands, source blob
identities, and proof limits.
