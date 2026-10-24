## Report

Blocked; no product changes applied.

- Confirmed live helper: `astrid/sdk/timeline_editing.py`; requested `astrid/core/timeline_editing.py` does not exist.
- Existing `capture_occurrence_duplicate()` emits valid `occurrence.duplicate` reservations and executes locally.
- Production caller reaches forbidden `authoring_commit.py:104` first, so helper-only wiring cannot consume the reservation without changing an owned-forbidden file or bypassing guards.

Tests:

- Targeted diagnostic: **73 passed, 2 failed, 3 deselected**.
  - Failures are the duplicate residual tests at the production caller.
- Ruff: **PASS**
- Vendor lock: **PASS**
- Artifact manifest: **PASS**
- `git diff --check`: **PASS**
- Mypy: existing baseline errors in `timeline_editing.py:525`.

Recorded blocker and commit message in the assigned orchestration paths. Recommended next step: expand ownership to the production authoring caller for explicit reservation consumption.