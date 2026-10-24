Delivered a bounded forward implementation. **G4 remains incomplete because foreign-source undo fails.** Wrote `commit-msg` and `BLOCKED`; no `DONE`.

The carrier is:
```json
{
  "op": "occurrence.place-shared",
  "select": "parent",
  "args": {
    "occurrence_id": "destination-id",
    "on": 12,
    "source_ref": {
      "project_id": "...",
      "timeline_id": "...",
      "revision_id": "...",
      "publication_id": "...",
      "content_digest": "sha256:..."
    },
    "source_occurrence_id": "source-id"
  },
  "created": ["occurrence:destination-id"]
}
```

[Native placement](/home/user/work/wt/agt-G4-historical-sharing-sol-0226/astrid/sdk/timeline/native_occurrence_shared.py) authenticates through Runtime’s existing source port, retains exact shot/internal revisions, and creates only the destination occurrence. [Production `TimelineSession.commit`](/home/user/work/wt/agt-G4-historical-sharing-sol-0226/astrid/sdk/timeline/sync.py:341) freezes this intent and supports identical-request retries after a lost acknowledgement. Reserved files and public contracts were untouched.

Controls cover inline-origin/reference-origin sources, newer global heads, unchanged physical revision counts, media/null/opaque fidelity, malformed authority, destination guards, and archive/retry behavior.

All pytest runs used the prescribed environment:
```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider
```

Arguments and results:

- `tests/editing_conformance/test_occurrence_shared_historical.py tests/editing_conformance/test_occurrence_shared_d20.py --basetemp=/tmp/w-00f76ac455/historical-release --tb=short` — **30 passed, 1 failed**.
- Broader targeted run adding `test_commit_runtime_source_copy.py`, `tests/sdk/test_timeline_sync.py`, and `test_timeline_sync_native.py` — **172 passed, 3 failed**. The two D17 redo failures reproduced identically using exact parent modules.
- Scoped Ruff and private mypy — **clean**, with clean parent diagnostics.
- `python scripts/artifact_manifest.py --check` and `git diff --check` — **passed**.

The retained undo success test fails at Runtime `timeline_commit_auth.py:1391`: `inverse stage native writes do not cover its authenticated effect image`. Removing the sole foreign occurrence retires child images from the canonical closure, while its native inverse only removes the occurrence.

Remaining work: guarded child-image retirement, retained/revalidated foreign authority for redo, and media/document cleanup. No tests were weakened, skipped, or marked xfail. No full suite or vendor checker ran.