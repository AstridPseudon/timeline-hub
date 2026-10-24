Implemented the bounded G2 fix on base `43bbb472216e9696458290b3918f039a2ef1ac9e`.

- `commit_session.py`: pass the verified revision/publication pair through public `open()` and function evaluation; retain the accepted receipt’s publication ID in the landed bundle.
- `publish.py`: diagnose a historical original pair before generic closure comparison.
- Added `tests/sdk/test_timeline_session_pair.py`. Left `store.py`, existing tests, shared fixture, schemas, pins, and inverse code unchanged.

Source cause: both session fetch calls supplied only `revision_id`, although the session already held the verified publication ID. The production reader already authenticates and retains the complete pair, so no synthetic authority or reader bypass was needed.

Tests used:
```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f
P=/home/user/work/venv-agent/bin/python

$P -m pytest -q -oaddopts= -p no:cacheprovider \
  tests/sdk/test_timeline_session_pair.py \
  tests/sdk/test_timeline_helper_capture.py::test_genuine_anchor_capture_has_exact_source_scope_and_base_pair \
  tests/sdk/test_timeline_restructure_guarded_runtime.py::test_fixture_reader_authorizes_exact_pair_and_refuses_wrong_scope_without_writes \
  tests/sdk/test_timeline_restructure_guarded_runtime.py::test_fixture_restructure_caller_refuses_mismatched_original_closure_without_writes
```

Result: **5 passed, 1 failed, 5 errors**. The existing reader control and four strict no-write controls passed, including historical refusal specificity. The original anchor selector still failed with missing `publication_id` because the separately owned shared opener ignores it. The five setup errors were my missing fixture import, subsequently corrected.

```bash
$P -m pytest -q -oaddopts= -p no:cacheprovider \
  tests/sdk/test_timeline_session_pair.py
```

Result: **5 passed**. This includes the unchanged original anchor test body using the existing production-reader fixture, capture/reload and function-commit propagation, historical reading, and forged revision/publication or unavailable-history refusal without writes.

Other checks:

- Scoped Ruff: no new diagnostics; two existing `publish.py` findings match parent identities.
- Scoped Mypy using `/home/user/work/venv-agent-typecheck-v2/bin/python`, `--follow-imports=silent`, private before/after caches: **21 unchanged parent diagnostic identities**.
- `python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`: **PASS**.
- `python scripts/artifact_manifest.py --check`: **PASS**.
- `git diff --check`: **PASS**.
- Before/after module origins stayed in this worktree for Agent/client and `rt-pin-8ea0766f` for Runtime.

Stable SHA-256 values remained unchanged:

| File | SHA-256 |
|---|---|
| Original helper tests | `2e4925262bbc605ab199ab0d4dea92e9cc5724eb4fc5865e2030b0307fe890e2` |
| Shared restructure fixture | `8a3a22dafcd3e84d9f79f680bed0176ad15edad21a30b416ca074ff549b9a8f4` |
| Runtime lock | `320d278366bc344aad35f3564845d9b62d9cc5f2e000a8a4cc6b6fea508d6cd2` |

No full suite ran; the retained overall failure status is unchanged. Next: combine with `agt-F-SDK-closure-fixture-0008`’s reviewed fixture repair and rerun the original anchor selector. No expectations were weakened or skipped.

Commit message and `DONE` were written. No Git writes or shared-environment mutations occurred.