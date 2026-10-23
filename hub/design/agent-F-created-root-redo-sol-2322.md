**PASS: created-child reload redo fixed. FAIL: combined acceptance remains 37 passed / 4 failed.**

Changed only `_root_inverse.py` and new `tests/sdk/test_timeline_created_root_stage_redo.py`.

Offline comparison established the exact cause: the restored stage-entry root has `hold=3`, while the root’s later deletion input has `hold=2`. Both had been required to match simultaneously. Nested restoration now checks the authenticated stage-entry image; forward replay still guards every intermediate previous value, including deletion. Source identity, complete owner comparisons, and compiler baseline checks remain.

The new regression covers causal restoration, corrupt intermediate values, and public whole/selected redo with immutable previews and exact accepted closures. Original test bodies/assertions remain unchanged.

Validation:

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=40 tests/sdk/test_timeline_commit_graph_roots.py tests/sdk/test_timeline_inverse_fork_guard.py tests/sdk/test_timeline_created_root_stage_redo.py
```

**37 passed, 4 failed.** The exact original created-child regression passes. All four failures are the existing child-alias variants returning `inverse_conflict` instead of `intervening_write`.

Using the same environment and pytest options:

- Dedicated causal test before production change: **1 failed**, reproducing `_root_inverse.py:217`.
- `tests/sdk/test_timeline_created_root_stage_redo.py tests/editing_conformance/test_transient_root_baseline.py`: **15 passed**, including existing source/partition/owner corruption controls.

Static checks passed:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_root_inverse.py tests/sdk/test_timeline_created_root_stage_redo.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --follow-imports=silent --no-incremental --cache-dir "$TMPDIR/mypy" astrid/sdk/timeline/_root_inverse.py tests/sdk/test_timeline_created_root_stage_redo.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
git diff --check
```

Exact SHA-256 values:

| File | SHA-256 |
|---|---|
| `_root_inverse.py` | `20961c438b6c2056e9538bb4f82a5a32dc0fd7906dbf1d12eaaee5a1d841c43d` |
| New regression | `2cb071c3b51207433649fff5ca04fe5e470272057b30bceb8657718ae91f3305` |
| Unchanged `inverse.py` | `e3e9c428e61f4bd04cb314d83edc20cda5f1846b68e69e0bca315dfa9b17d166` |
| Unchanged original graph-root tests | `19a04ccf8cc3fa30cd067c55b6a3941d4c2f46270fb850ce37ca92353f40c148` |
| Unchanged fork-guard tests | `97ee42cc2f96ff2491711f039530e87c7340a1f560440f2caa7a53e71af84e16` |

All other tracked files match base `d7db17a60cb91bc97e1941b8f8ca1a5e983b0859`.

Complete offline document/history/boundary/stage/owner/native/effect/binding/pin capture: `$TMPDIR/created-root-offline.json`, 420,390 bytes, SHA-256 `7a770a085bbd835bcbce734df2392524beb0b0c975a79f3d051bdc9daf4abf61` (scratch retention only).

Next step: hand the four alias reason mismatches to the independent `inverse.py` owner for normalized write-overlap classification before consumer refusal. No `inverse.py` change was needed for this fix. No full suite requested or full PASS claimed. Commit message and `DONE` written.