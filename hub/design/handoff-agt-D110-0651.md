# R2 D110 handoff — removed local shot owner inverse

## Result

Implemented the minimal one-side fix in `astrid/sdk/timeline/inverse.py`.
After authenticated `restore_root_baselines`, physical owner pairs are retained only when both the occurrence owner is live and its local shot is present in the restored bundle. This removes only stale absent-local-shot pairs before the existing `remember()` materialization boundary. No guard, authority, catchall, schema, client, Runtime pin, or materialization bypass changed.

Added `tests/sdk/test_inverse_removed_shot_owners_runtime.py` with genuine Runtime/provider cases for separate ADD+Undo and SWAP+Undo. Each case uses the supported public path: create a shared sibling, submit `occurrence.fork` plus ADD/SWAP in one commit through Runtime `commitTimeline`, then submit the public inverse.

## RED

Exact test file on unchanged product before the fix:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1daca2a3 \
PYTHONPATH=/home/user/work/wt/agt-R2-D110-removed-shot-0651:/home/user/work/wt/rt-pin-1daca2a3 \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 \
  --junitxml=<worker evidence>/D110-red.xml \
  tests/sdk/test_inverse_removed_shot_owners_runtime.py
```

Result: `2 failed`, no skips. Both cases reached the real registered Agent provider and exact Runtime checkout, then failed as the reported ordinary Runtime catchall/503: `builtins.KeyError: 'local-shot'` at `_doc_patch_materialize.remember` line 18, called by `inverse.apply_inverse` line 1177 after root restoration.

## GREEN and neighbors

The exact same targeted command after the fix: `2 passed` (`[add]`, `[swap]`), no skips.

Focused existing neighbors:

```text
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 \
  --junitxml=<worker evidence>/D110-neighbors.xml \
  tests/sdk/test_timeline_inverse_shared_root_baseline.py \
  tests/sdk/test_timeline_inverse_fork_guard.py \
  tests/sdk/test_timeline_inverse_binding.py
```

Result: `42 passed`, no skips.

The new cases assert that the untouched sibling occurrence remains byte-identical through the accepted fork+media edit, that its original shot root remains in the accepted closure, and that whole-commit inverse restores the exact pre-fork shared document: occurrence rows, shot revisions, internal timeline revisions, and dependency manifest.

## Source and tree custody

- Agent base: `b27ff3449ec4d9b5e14ac25b8f5a18c1999c21f6`, tree `972188c76ed7a9e8f41d1baf6768673de2596efc`.
- Runtime producer: immutable `/home/user/work/wt/rt-pin-1daca2a3`, commit `1daca2a33f6d7b10053e07c539a54843e3984e19`, tree `a522511414947e48e317a5e5c2103483b121a750`, clean. `runtime.lock.json` names the same source commit.
- Changed product: `astrid/sdk/timeline/inverse.py` only.
- New test: `tests/sdk/test_inverse_removed_shot_owners_runtime.py`.
- `runtime.lock.json`, schemas, generated clients, auth/store/fixtures, and other product files are unchanged.

Static checks passed: Ruff, mypy, in-memory `py_compile`, and `git diff --check`.

No full suite, browser/App suite, P4, family bulk, D108, or P2GO claim is made. Independent protected/core review is still required by the brief before release/merge.
