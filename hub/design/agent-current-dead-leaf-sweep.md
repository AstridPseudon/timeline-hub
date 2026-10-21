# Proposed Agent dead-leaf sweep row

Manager: please add/update the Agent deletion ledger; this worker does not edit the ledger.

| id | what (path) | contradicts | replaced by | owner | milestone | proposed status | evidence |
|---|---|---|---|---|---|---|---|
| AG-M2-DEAD-LEAF-01 | private `_CheckMixin._scene_only_problems` adapter in `astrid/sdk/timeline/check.py` (12 product lines) | stale duplicate formatter for a managed Scene result | live connected `Checkout.check()` path: `_managed_scene_spans()` -> `_invoke_scene_only()` / `_scene_only_spans()` -> `_scene_problems()` | agent | M2 | DELETED (worker branch; pending manager merge) | `git grep -n -i -E 'scene[_ -]?only[_ -]?problems|scene only problems' -- . ':!*.pyc'` returns no matches after deletion. No dynamic/public-export/entrypoint/pack-resource references found by repository-wide `rg`; `timeline_checkout.py` re-exports only the established public check helpers and not this private method. The public Scene caller is merged in `d49cef1da`; native PARAM/clear/split migrations are present in current base `5c5173dcb`. |

## Commit mapping

Proposed conventional commit:

`refactor(timeline): remove dead scene problem adapter`

Body: remove the uncalled private `_scene_only_problems` method now that the connected public check path formats the live managed Scene spans directly. No public API, behavior test, canonical timing/compiler/guard, fallback writer, or held WC3/WC6/D13 path changes.

## Test mapping

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/sdk/test_scene_caller_preservation.py tests/sdk/test_scene_save_core.py tests/sdk/test_scene_dispatch_contract.py tests/sdk/test_timeline_checkout_facade.py tests/sdk/test_timeline_filmstrip.py` — **89 passed, 2 skipped** in 5.10s.
- `git diff --check` — passed.
- Full suite, browser/live suite, and artifact/package build — not run; not relevant to this private-method deletion and prohibited by the task scope.

No tests were deleted, weakened, or changed.
