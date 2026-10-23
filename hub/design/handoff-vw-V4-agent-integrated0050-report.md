# FAIL/BLOCKED — V4 integrated proof

Verified:

- HEAD: `e5c260c834acdcf6844f62d87e91e35225a30c8d`
- Tree: `b4ee5f92b2775ab774bf4776d24e28ffb5f665e2`
- `cf31566e8` ancestor: PASS
- Six stale sources absent; active `threejs-live-editor` pack/catalog linkage retained.
- Recipe copies and canonical anchor test byte-identical; `clip.anchor` assertion preserved.
- Catalog tests: **4 passed**
- Manifest check: **PASS**
- `git diff --check`: **PASS**

Required anchor suite: **FAIL, 54 setup errors**. Runtime rejects Agent `PreparedCommit` fields `label`, `steps`, and `merge_mode` as unexpected. No source changes made.

Wrote `report.md`, `commit-msg`, and `BLOCKED` artifacts.