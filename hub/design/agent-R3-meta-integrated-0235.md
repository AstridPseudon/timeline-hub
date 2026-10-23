# R3 / AG-V1seam integrated-head proof

**PASS, read-only.** Exact HEAD `d6f05e8a983375338eabcfa45b704c1868126e3b`,
tree `847f44f969971fcc21c69bd41b70a05adaf8ec8b`; the tree exactly matches
reviewed `ce8639a265d21399fa0baac5a396e71890bb6a22` (zero tree-diff files).
HEAD parents are R3/R1 merge `c51d1465b60833f0a27f6ce1f9f7afdf930e345d`
and AG-V1seam/meta merge `ce8639a265d21399fa0baac5a396e71890bb6a22`.
Reviewed `ce8639a` parents are `ae68a1bea6c2511bce62b30b3def942d17fe8431`
and `360826a1724c16e4066da47abea153bac894363d`; all are actual ancestors.

Targeted tests: **150 passed, 2 subtests**. Authored-meta/reload selectors:
**7 passed/104 deselected**, **3 passed/33 deselected**, and
**1 passed/27 deselected**. Scoped Ruff passed; private valid mypy for
`validators/meta.py` passed. Exact-tree inherited ratchets remain Ruff
**2151/2151** and mypy **1915/1915** from the independent review. Status,
diff-check, and merge-marker checks are clean.

R3/V2, R1 reads, V1 allowlists/denied `AssetEntry.meta`, V3/P1/V4,
generated lock/client/schema, and the authored-meta seam are preserved.
Original-base invalid remains distinct from replay HTTP 409; authored meta is
preserved but ignored in reference discovery, while `params.meta` remains a
real dependency. No full/browser/Runtime-P5/native14 run and no real-wire claim:
old `691` client remains while official `21482` generated adoption is
Runtime-blocked. No files were modified or deleted.
