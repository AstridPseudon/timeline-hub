# U4a independent review

Verdict: **PASS** for the bounded U4a adoption. The only product change is the
allowed `runtime.lock.json` source pin from Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`
to qualified Runtime `ab1e4f6141987706132916e2da16477f5a019464`.

## Source and scope

- Reviewed `cec01ed6612f2b56e8d170a5d066dc7a4882805f` against Agent base
  `20177e66564f9f91735ed1a11bac821682d60edf`.
- `git diff --stat` is one file, two lines: `runtime.lock.json` only.
- Independent `git diff --quiet BASE HEAD -- . ':(exclude)runtime.lock.json'`
  passed; no outside blob changed.
- The lock mapping and all 15 entries are unchanged from base. Each consumer
  is byte-identical to base, the released `rt-pin-5e9ad1c6` producer, and the
  adopted `rt-pin-ab1e4f61` producer. Each producer hash matches its lock entry.

The 15 verified mappings are:

1. `astrid/core/timeline/schema/timeline-config.schema.json` <- `contract/schemas/timeline-config.schema.json`
2. `astrid_runtime_client/__init__.py` <- `packages/python/astrid_runtime_client/__init__.py`
3. `astrid_runtime_client/contract_metadata.py` <- `packages/python/astrid_runtime_client/contract_metadata.py`
4. `astrid_runtime_client/generated.py` <- `packages/python/astrid_runtime_client/generated.py`
5. `astrid_runtime_client/timeline_commit_types.py` <- `packages/python/astrid_runtime_client/timeline_commit_types.py`
6. `tests/fixtures/runtime-responses/events_page_1_200.json` <- `conformance/responses/events_page_1_200.json`
7. `tests/fixtures/runtime-responses/events_page_2_200.json` <- `conformance/responses/events_page_2_200.json`
8. `tests/fixtures/runtime-responses/invalid_cursor_400.json` <- `conformance/responses/invalid_cursor_400.json`
9. `tests/fixtures/runtime-responses/managed_outputs_200.json` <- `conformance/responses/managed_outputs_200.json`
10. `tests/fixtures/runtime-responses/not_found_404.json` <- `conformance/responses/not_found_404.json`
11. `tests/fixtures/runtime-responses/publish_conflict_409.json` <- `conformance/responses/commit_conflict_409.json`
12. `tests/fixtures/runtime-responses/task_admission_201.json` <- `conformance/responses/task_admission_201.json`
13. `tests/fixtures/runtime-responses/task_read_200.json` <- `conformance/responses/task_read_200.json`
14. `tests/fixtures/runtime-responses/validation_error_422.json` <- `conformance/responses/validation_error_422.json`
15. `tests/fixtures/visual-boundary-v1.json` <- `conformance/fixtures/visual-boundary-v1.json`

## Runtime custody

The completed checkout receipt is
`checkout-runtime-ab1e4f6141987706132916e2da16477f5a019464` and points to
`/home/user/work/wt/rt-pin-ab1e4f61`. Independent current checks report:

- HEAD `ab1e4f6141987706132916e2da16477f5a019464`;
- tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`;
- clean index and worktree.

The author evidence records the same HEAD/tree and clean before/after. The
D130-held WAL branch is separate (`011cbdc88e0577bed87a3465e772d6ffbdcd46fe`)
and was not used or adopted; the D130 absolute hold remains intact.

## Exact validation commands

- `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-ab1e4f61` — PASS (`ok runtime.lock.json`).
- `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — PASS (`artifacts.json is current`).
- `PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-ab1e4f61 /home/user/work/venv-agent/bin/python -m pytest -q tests/test_vendor_lock.py tests/test_artifact_manifest.py` — PASS, 24 passed in 5.43s.
- `PYTHONPYCACHEPREFIX=/tmp/w-2c94b52bc3/rt-U4a-inverse-adopt-review-1634-compile/pycache /home/user/work/venv-agent/bin/python -m compileall -q scripts/vendor_lock.py scripts/artifact_manifest.py scripts/refresh_runtime_client.py astrid_runtime_client/*.py` — PASS; private cache only.
- `make PY=/home/user/work/venv-agent/bin/python ruff` — PASS; Ruff current 2143 equals baseline 2143.
- `git diff --check 20177e66564f9f91735ed1a11bac821682d60edf cec01ed6612f2b56e8d170a5d066dc7a4882805f` — PASS.
- `make PY=/home/user/work/venv-agent/bin/python mypy` — UNVERIFIED: runner failed before producing a baseline because the shared Python 3.13 environment lacks `types-PyYAML`; it also reports installed NumPy stubs using Python 3.12-only syntax. This is unrelated to the lock-only diff.

The author-reported 24-pass result is retained and independently reproduced.
No full suite, browser journey, refresh, manual pin, code fix, WAL retry, or
other held-route activity was performed.
