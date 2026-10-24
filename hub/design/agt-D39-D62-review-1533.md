## D30 report — U4a/D39 custody review

**Source review: PASS**

- Agent: `0eda0abf3c825203536b1b85def307a190dd8633`, tree `78da9b18…`
- Runtime producer: `e02f3e3d9d972be74450536ec0ee49e8bc51c2ec`, tree `a095ecbe…`
- Exact 15/15 canonical mappings match byte-for-byte.
- Schema digest: `sha256:867f3553…`
- Delta is exactly four files: three generated client files plus `runtime.lock.json`.
- Full request/reply DTOs and `/commit` caller remain intact; only additive change is `HistoryEntry.recorder_abi: 1|2`.
- Production path uses `astrid/sdk/workspace_client.py` → generated `WorkspaceClient`.
- Generator, artifact manifest, vendor lock, Ruff (changed files), mypy, and `git diff --check`: passed.
- Worktree is clean.

**Focused acceptance**

Command:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-e02f3e3d
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-e02f3e3d"
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider
  --junitxml=.../evidence/review.xml
  tests/test_vendor_lock.py
  tests/test_artifact_manifest.py
  tests/stage1/test_runtime_client_cutover.py
  tests/stage1/test_vendored_workspace_client_parity_luna.py
```

Result: **37 passed, 39 automatically deselected**, exit 0. The 39 integration-lane node IDs are recorded in `review.log`; real JUnit XML was produced. XML SHA-256: `694c736e…`.

The author’s prior 37/39 result had no JUnit XML. A separate diagnostic with cleared pytest `addopts` admitted integration tests and found one unrelated `history_unavailable` failure; it is retained as `review-unfiltered.*`, not counted as acceptance.

**Merge status: HOLD**

Source adoption passes, but Runtime independent security review `tl/rt-R-D62-security-review-1511` remains active. Manager should hold merge until that producer qualification completes.

Commit message and `DONE` marker created. No product, test, fixture, lock, or generated-file edits were made.