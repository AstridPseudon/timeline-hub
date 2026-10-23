# G3 integrated ordinary-show readonly review — PASS

Reviewed integrated merge `12b40af0123c3e0782b99ebe44f719d29a40e0af` (tree
`8eca71a4eaf0cd9633edb71e3f6a806589f59dff`) on G234 parent
`ea302e0f504c12e7f71c21745e1ef99cac014d9a`, with reviewed port
`126aff176cab03ec9659fbdbb824ec41d2c9de19` as the second parent.

**PASS.** The integrated delta contains exactly the reviewed three paths:
`astrid/core/timeline/cuts.py`, `astrid/sdk/timeline_cuts.py`, and
`tests/sdk/test_timeline_show_views.py`. Stable patch-id:
`61ea449935e17a160fa295a4630df8fc5f9a91ea`. This proves the reviewed
three-path delta only; it does not claim whole-author-tree equality.

Production caller is wired: `cli_show.py:224` → `build_cut_table` →
`occurrences_from_bundle`. Targeted neighboring cut/show tests: **55 passed,
2 subtests passed**. Normal Ruff: **2149/2149**. Persistent mypy and explicit
`compare_mypy_baseline`: **1914/1914**. Vendor lock, artifact manifest, and
`git diff --check`: PASS. Core/test scoped Ruff passes; SDK scoped Ruff has
10 pre-existing findings. Imports resolve from this worktree except
`runtime_protocol` from `/home/user/work/runtime`. Worktree is clean.

No source, schema, generated, pin, dependency, executor, or HTTP-body change
was made. No full/browser/live-socket suite was run. PLAN §3,
`commit-v2.md` §§1–5, and `BOARD-HEADER.md` were read. Queue decision: PASS.
