# U2b independent review — FAIL

`55c1e7aa7` has the correct two-parent ancestry (`ef851b22c` plus live
`74f3f7edb`) and the live tip is an ancestor. Policy/registry tests pass
(`55 passed`), Ruff is `2149/2149`, mypy is `1912/1912`, vendor/artifact checks
pass, and protected schema/client/lock/Composition bytes are unchanged.

Approval is blocked by source-backed findings:

- `tests/packs/rendering/test_timeline_inspector_viewer.py:9` was restored,
  but its imported `astrid/.../inspector_viewer.py` product was deleted by the
  prior dead-viewer cleanup. The focused test has a collection
  `ModuleNotFoundError`; remove the obsolete test, not the retired product.
- `tests/packs/video_editing/test_runtime_publication_chain.py:939-976`
  removed a strict xfail and calls deleted
  `GenericPackHost._publish_assembled_timeline`; the selected target is
  `1 failed, 1 passed`. Resolve/classify this stale conflict assertion without
  restoring the old route.
- Three committed `tests/**/__pycache__/*.pyc` binaries are unintended author
  artifacts and require return.
- `git diff --check ef851b22c..HEAD` reports new EOF blank lines in
  `tests/packs/runpod/conftest.py` and
  `tests/test_runtime_correctness_inventory.py`.

The compile-contract positives remain unskipped and visibly failing in the two
known prepared-envelope vectors (`32 passed, 2 failed`), while the no-invisible-
skips guard negatives pass. Journey and filmstrip controls pass; local Runtime
admission and custody runs have separate environment failures and are not
claimed as proof. No D17 content was imported; no full/browser/native14/58
suite was run.
