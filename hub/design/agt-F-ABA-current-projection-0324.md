## Report

Implemented the donor `5694c7147` ABA inverse-projection repair on current `622b30a8c3`, preserving the current reorder/history `list.move` logic.

Changed:

- `_commit_patch.py`: `CommitPatch.after`, `CommitPatch.finish`, `rebase_patch`, `_materialization_sites`, `inverse_address_resolver`
- Added exact donor test file `test_authoring_undo_projection.py`
  - SHA-256: `e7f006ebbc75536418ed7d4756eeec8dbbcc855a4877a533c5398f1ec8ab95c4`

Tests:

- Donor lane: `55 passed`
- Neighbor lane: `112 passed`
- Current reorder/history lane: `42 passed`
- Ruff, private mypy, vendor lock, artifact manifest, and `git diff --check`: passed

The existing ABA oracle remained byte-identical:

- `tests/timeline/test_authoring_media.py`
- SHA-256: `e22fb91ff0820ec37fea99f4109850fc72bcb78c91103019a91ac9b29b19015c`

No reserved files, Runtime code, schemas, pins, or known failing service bodies were changed or rerun. Donor review/Luna0312 and any required independent join review remain pending.

Commit message and `DONE` marker written; no Git commit/merge performed.