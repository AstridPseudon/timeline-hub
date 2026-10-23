## P1 current R1 real-document corpus

Result: **PASS: 42 passed, 1 warning.**

### Revisions and packet verification

- Base/current Agent tree: `b7a32c5238f0948a913869b06437f174a277172c`
  (`hub/timeline/agent/tl/agt-R1-membership-current`).
- Donor packet: `52e9c0ea659123c86d6cbadc94f78ef972d74308`; original packet:
  `d8e1578bd9f717eb975addb50c2654de70815475`; prior independent result:
  PASS42.
- All 15 permitted packet blobs were checked with `git hash-object` against
  the donor tree: 15/15 exact, 0 mismatches. The three older/missing paths
  imported exactly were:
  `tests/sdk/test_p1_doc_patch_provider.py`,
  `tests/sdk/test_p1_doc_patch_requests.py`, and
  `tests/sdk/fixtures/p1_feasibility/doc_patch_requests.json`.
- Worktree changes are limited to those three packet paths. No product,
  schema, generated, pin, lock, launcher, outside-test, skip, or xfail file
  changed.

### Scope and evidence

The provider test uses the production Agent caller
`create_runtime_commit_service().commit(...)` through the existing detached
`DetachedRealm`/`DetachedPort` service. The corpus preserves the exact
commands, guards, physical roots, created IDs, absent-vs-null distinctions,
opaque/order/alias/trim/inverse assertions, collection
`selection_changed`, and same-field `value_conflict` cases.

The detached disjoint-head witness remains legacy `rebased`; it is not v2
`merged` evidence. The mounted App/HTTP chain, including the App journey and
Runtime HTTP publication, remains unexecuted and unverified. Product merge
eligibility remains Agent-owned. No full/browser/heavy/socket suite was run.

### Commands

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py`
  → `42 passed, 1 warning`, exit 0. Log:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-current-R1-corpus/pytest.log`.
- `/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py`
  → passed, exit 0. Log: `.../ruff.log`.
- `/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py`
  → passed, exit 0. Log: `.../mypy.log`.
- `git diff --check` → passed, exit 0. Log: `.../diff-check.log`.

The `...` log paths above are relative to the same worker directory as the
pytest log.

