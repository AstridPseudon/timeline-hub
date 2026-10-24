## Report

Imported the exact donor file into [tests/sdk/test_timeline_persistence.py](/home/user/work/wt/agt-F-persistence-review-0028/tests/sdk/test_timeline_persistence.py). No implementation or expectation changes.

Result: bounded fixture FAIL, `9 passed, 1 failed`.

The sole failure is the post-restart “merge other clips” case. The production caller emits `merge:"atomic"` (`publish.py:284`), so Runtime correctly refuses with:

- `atomic_scope_changed`
- guard: `ref="timeline", path=[]`
- base: `rev-0 / txn-e01990...`
- current: `authoring-parent-revision-dbaf... / txn-dca027...`
- peer changed only `b-type.params.text`
- no write occurred

Classification: production-intended atomic fallback, not stale fake history. Next owner: Agent G5 production publish caller owner to decide whether this path should remain atomic or gain declared field-level merge semantics.

Tests/checks:

- Required `pytest ... -x --tb=short --timeout=45`: `7 passed, 1 failed`
- Full exact fixture run: `9 passed, 1 failed in 17.26s`
- Scoped Ruff: one unchanged pre-existing `BLE001` at line 191
- Ruff baseline: `2148 == 2148`
- Private Mypy baseline: `1911 == 1911`
- Artifact manifest check: pass
- Runtime vendor lock against frozen `34eac004…`: pass
- Import origins and donor SHA verified
- `git diff --check`: pass

No full suite or browser/live suite was run. Completion marker and commit message were written.