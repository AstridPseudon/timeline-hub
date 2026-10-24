## D30 Report — F/D54

Prepared [final-core-collection.json](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-final-core-collect-1443/evidence/final-core-collection.json>).

- Final CORE superset: **8,665 parametrized nodes**, 386 files.
- Separate P4 HTTP originals: **3 nodes**.
- D13 managed node: **1 node**.
- D23 selectors retained, including the `["second"]` parameter.
- Historical full9758 checkpoint159 remains distinct and was not reused as the final CORE selector.
- Inventory covers commit door/EditCommand, provider/session/rebase/inverse/undo/history, occurrence/placement/split/trim/move, show/sheet/visualize, CLI and editing runner seams.
- Production caller paths verified in `commit_session.py`, `sync.py`, `commit.py`, `commands.py`, `remote.py`, and `timeline_sheet.py`.

Checks:

- Pytest collection-only: PASS.
- JSON validation: PASS.
- `git diff --check`: PASS.
- Worktree remains clean.

No test bodies, HTTP/authenticated requests, browser/gate/full suites, installs, or product/test/generated/lock/registry edits were performed. The acceptance run remains pending D61’s source/client refresh. Durable JUnit paths and the existing venv/Runtime service invocation are recorded in the evidence.

Created the required `DONE` marker and commit message:

`test(agent): prepare F/D54 final core collection`