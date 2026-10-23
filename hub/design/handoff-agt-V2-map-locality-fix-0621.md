# agt-V2-map-locality-fix-0621 — PASS

Implemented on Agent base `b42b7d72a65cab305a4b953093963019aabc70b9` in `/home/user/work/wt/agt-V2-map-locality-fix-0621`. No commit, merge, checkout, fetch, push, dependency installation, or shared dependency writes performed. Harness owns the commit.

## Change and production caller

Only `_commit_timing_validation.py` and the new focused `test_commit_map_locality_d12.py` change. The existing mounted path remains Runtime provider loader → `create_runtime_commit_service()` / `RuntimeCommitService.commit()` → `validate_final_candidate()` → `validate_candidate_timing()`.

The old catch-and-return compared every clip's geometry and could also stop before validating other components. The replacement selects timing dependency components using the existing kernel's map detector, cut lookup, Moment grammar and word-binding adapter. It compares retained components' clips/declarations, used tracks/assets, and physical source/owner/clock/extent/document inputs. Baseline and candidate components are joined so removed targets remain guarded. Only unchanged pre-existing unsupported components are nonblocking; every written or involved component remains in the existing timing compiler. Authored maps/declarations are never rewritten. Complete authored anchor validation runs before the selection. Unbounded unsupported timing forms retain conservative dependencies.

The request/reply, source bundle, authentication, idempotency, history, undo, native fork, executor and schema implementations are unchanged. No tests, recipes, fixtures, maps or bindings from the base were edited, deleted, skipped, weakened or marked xfail. The b42 null-speed/bounds fixes remain intact.

## Exact verification commands and results

All commands ran from the worker worktree. `/tmp/w-f6487e0f5e` is the private scratch directory recorded by the worker's `tmpdir` pointer.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -o cache_dir=/tmp/w-f6487e0f5e/pytest-cache tests/editing_conformance/test_commit_map_locality_d12.py tests/editing_conformance/test_commit_boundaries_d12.py tests/editing_conformance/test_commit_timing_validation.py tests/editing_conformance/test_commit_anchor_d12.py tests/editing_conformance/test_commit_fps_d12.py tests/editing_conformance/test_commit_v2_validation.py tests/sdk/test_timing_compiler.py tests/editing_conformance/test_provider_occurrence_fork.py tests/editing_conformance/test_recipe_occurrence_fork.py tests/editing_conformance/test_commit_runtime_occurrence_fork.py tests/editing_conformance/test_recipe_m2_clip_add.py tests/sdk/test_timeline_clip_add_provider.py
```

**PASS: 262 passed, 1 deselected in 9.96s.** The one deselection is the existing repository-default integration marker, independently enabled below; no new deselection or skip was introduced. Output: `/tmp/w-f6487e0f5e/targeted-pytest.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-f6487e0f5e ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -m integration --basetemp=/tmp/w-f6487e0f5e/pytest-real-fork -o cache_dir=/tmp/w-f6487e0f5e/pytest-cache tests/editing_conformance/test_commit_runtime_occurrence_fork.py
```

**PASS: 1 passed in 3.95s.** This uses in-process RuntimeService/RealmStore and persistent acceptance, merged fork, guarded undo/redo and schema validation; no sockets/browser. Output: `/tmp/w-f6487e0f5e/real-fork.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 USE_REAL_RUNTIME=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python /tmp/agt-V2-map-locality-audit-0616-probe.py
```

**PASS: exact original unchanged 0616 probe.** Same-image `clip-b.at: 5 → 6` accepted once with one preparation, one receipt and one retained original map. Mutating `clip-a.source_window.to: 30 → 31` still returns 422 invalid_document with zero preparations/acceptances and the original head. Output: `/tmp/w-f6487e0f5e/exact-0616-probe.log`. Probe SHA256: `68771e7cf2fb5104293fc98ad0e8ce34629b78fe85b1ba0d89cb3a7a01820246`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python /tmp/w-f6487e0f5e/mounted-locality.py
```

**PASS: 12 cases through `load_timeline_commit_provider('astrid')` and real Runtime ABI exceptions**, without the pytest ABI stub. Runs the checked-in regression functions directly: unrelated move and independent new literal clip, each accepted and dry-run preview/would_status accepted; no-write 422 controls for map mutation, actual asset target mutation, new map, new invalid declaration and invalidation of a previously resolvable cut; plus unchanged mapped cut dependency with independent edit accepted and actual target move/removal refused. Payload equality checks permit only the intended edit and the canonical authenticated successor pins/digests. Output/origins: `/tmp/w-f6487e0f5e/mounted-locality.log`. Script SHA256: `ef090cd48477f7981857b97fdac297468aafe80959b3265fde2da04e21cb224c`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_CACHE_DIR=/tmp/w-f6487e0f5e/ruff /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_commit_timing_validation.py tests/editing_conformance/test_commit_map_locality_d12.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-f6487e0f5e/mypy /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/timeline/_commit_timing_validation.py tests/editing_conformance/test_commit_map_locality_d12.py --follow-imports=skip
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. RUFF_CACHE_DIR=/tmp/w-f6487e0f5e/ruff make ruff PY=/home/user/work/venv-agent/bin/python
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. MYPY_CACHE_DIR=/tmp/w-f6487e0f5e/mypy-ratchet /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

**All PASS.** Scoped Ruff clean; scoped mypy clean (2 files); normal Ruff `2150/2150`; normal mypy `1915/1915`, no budget changes; lock `ok runtime.lock.json`; `artifacts.json is current`; whitespace clean. Mypy output: `/tmp/w-f6487e0f5e/mypy-ratchet.log`.

Development iterations: the first pytest attempt lacked Runtime in PYTHONPATH, and a first cache path treated the harness's tmpdir pointer as a directory; both were corrected without dependency writes. Draft new-test requests were corrected to the existing list-insert/created-ID ABI and canonical successor-pin expectations. The full mypy ratchet initially caught one new Optional[Moment] assignment; an explicit optional annotation fixed it. Final commands above pass; no baseline increase or existing expectation change.

## Tested source and import origins

- Runtime observed HEAD: `85dafdf46742b02ae5e4a300656cd6f5d68f0d4d`.
- Runtime provider loader and ABI: `/home/user/work/runtime/runtime_protocol/timeline_commit_provider.py` and `timeline_commit.py`.
- Agent commit, validation, adapter and compiler imports all resolve below `/home/user/work/wt/agt-V2-map-locality-fix-0621/astrid/sdk/timeline/`, never the integration Agent worktree or an installed Agent copy.
- Test interpreter `/home/user/work/venv-agent/bin/python`; schema package `/home/user/work/venv-agent/lib/python3.13/site-packages/banodoco_timeline_schema/__init__.py`; Ruff `/home/user/work/venv-agent/lib/python3.13/site-packages/ruff/__init__.py`.
- Persistent typecheck interpreter `/home/user/work/venv-agent-typecheck-v2/bin/python`, CPython 3.11.17; mypy `/home/user/work/venv-agent-typecheck-v2/lib/python3.11/site-packages/mypy/__init__.cpython-311-x86_64-linux-gnu.so`.
- Adapter SHA256: `871a4b140be60863a8238ac60acf1ab12f56d7a71d4a59bc4f3f3792de46f58f`.
- New regression SHA256: `ab7cb86c798809bcd698d12a755df2e7f5b3c091e0e66fdabd1d067c81d73ff4`.

## Read-only review disposition

| Check | Result |
| --- | --- |
| Existing mounted production caller uses fix | PASS |
| Exact independent 0616 positive and map negative | PASS |
| Independent literal creation and move; byte preservation | PASS |
| Map/asset/cut target/new invalid/previously resolvable invalidation guards | PASS |
| Null-speed, bounds, fps, anchors, timing and fork controls | PASS |
| Full source_bundles/auth/DTO paths retained, no implementation changes there | PASS (scope inspection; no claim of whole-suite requalification) |
| Scoped lint/typecheck and normal unchanged ratchets/tools | PASS |
| Original tests/recipes/fixtures and shared dependencies untouched | PASS |

No policy decisions changed and nothing is blocked. Explicit maps remain unsupported when newly created or when their component is involved. Selection uses conservative shared word pools/cut successors and retains full physical clock/extent/source identity guards; it does not add map semantics. Full suites, original whole-54, P4 HTTP bodies, browser/heavy/native14/crash24/farm suites and historical replay-wide qualification were intentionally not run, as instructed. Recommended next step: read-only review and harness commit/normal Agent merge queue.
