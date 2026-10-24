## Report — agt-G4-duplicate-return-1240

No product changes retained; worktree is clean.

Investigation confirmed:

- `authoring_commit.py:104` is the production guard blocking detached duplicate membership.
- A caller-only `occurrence.duplicate` reservation can be generated, followed by residual `doc.patch` commands.
- Runtime then rejects the intermediate duplicate state because it copies a non-default `source_offset` before the residual patch is applied. Fixing this requires the explicitly reserved Runtime/commit continuation seam; source mutation or guard weakening would violate the task.

Tests:

- Targeted acceptance: **63 passed, 2 failed, 13 deselected**.
- Ruff: **PASS**
- Mypy: **2 existing baseline errors at `timeline_editing.py:525`**
- Vendor lock: **PASS**
- Artifact manifest: **PASS**
- `git diff --check`: **PASS**

Created the required `BLOCKED` marker and commit message.