## Done

- Expanded only the two requested dispatch branches in `astrid/sdk/remote.py`.
- Preserved behavior/API/imports; no tests added.
- Wrote commit message to the requested path.

## Verification

- `pytest -q tests/sdk/test_workspace_client_timeline_commit.py` — **8 passed**
- `git diff --check` — **passed**
- Scoped Ruff JSON: **E701 reduced 116 → 114**; total findings **124 → 122**. Unrelated findings unchanged.
- Final diff touches only `astrid/sdk/remote.py`.

No full, socket, install, or git mutation commands run.