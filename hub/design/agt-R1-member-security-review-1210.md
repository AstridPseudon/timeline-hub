# R1 Review Report

## Verdict

Source/security qualification: **FAIL — do not release or merge red.**

`doc.patch` accepts literal slash/`::` IDs, but authenticated redo fails:

- `_collections.py:32-33` rejects `/` and `::` identities.
- `inverse.py:984-985` invokes that validation during inverse restoration.
- `_doc_patch.py:443-445` explicitly routes these IDs through the aggregate path, exposing the mismatch.

Results:

- `clip/a`: forward/undo pass; redo fails.
- `clip::a`: forward/undo pass; redo fails.
- `clip:a`: forward/undo/redo pass.

This is a production behavior/source flaw, not a fixture-only failure.

## Tests

- New focused file: **42 passed, 1 failed**.
  - Failure: `ancestor-first` mixed-operation redo; reproduced with the old handler, so classified as an existing R2/nested-mirror seam.
- Adjacent doc-patch/inverse cohort: **380 passed, 19 integration cases deselected**.
- `ruff`: passed.
- `mypy` on `_doc_patch.py`: passed.
- `git diff --check` and `py_compile`: passed.
- Runtime vendor lock check: passed.
- Worktree remains clean; no product files changed.

The production caller path uses `doc.patch` through the provider execution/Runtime commit service. Authenticated inverse-record checks and native/source controls passed; no fragment-control authentication bypass was found.

The requested Agent `timeline-r4` BOARD-HEADER/design path was unavailable in the provided checkout; I used PLAN.md and the available Runtime `contract/commit-v2.md`.

Recommended next step: fix literal slash/`::` identity handling consistently in collection ordering/inverse restoration, then rerun the focused literal-ID and redo cases.