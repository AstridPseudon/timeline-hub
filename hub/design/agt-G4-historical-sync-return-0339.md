## Report

- Applied only the reviewed `975dd47157` `sync.py` hunk. Foreign `occurrence.place-shared` commands now remain frozen for Runtime authentication; normal local capture/guards are unchanged.
- Changed only `astrid/sdk/timeline/sync.py`.
- Commit message written; `BLOCKED` marker written.

Tests:

- Historical redo/session lane: **28 passed**
- Historical controls: **21 passed**
- D20 controls: **9 passed**
- D17 source-copy controls: **9 passed**
- Ruff, scoped mypy, vendor lock, artifact manifest, and `git diff --check`: **passed**

The single authorized last-owner test against Runtime `36760ee` failed once:

`inverse stage native writes do not cover its authenticated effect image`

Failure occurs in Runtime `_inverse_stage_boundaries` during validation. The forward source/request uses the authenticated five-field `source_ref`; the inverse request is generated via `timeline.inverse` after the accepted forward record. No Agent-only fix is authorized, so this remains blocked.