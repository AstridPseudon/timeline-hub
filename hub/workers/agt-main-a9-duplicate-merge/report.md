Implemented the upstream duplicate merge onto Main.

- Preserved Main’s `_check_core`, draft-history, reset behavior, and all unrelated features.
- Added stored-form duplicate guards, repeated-shot preservation, exact copy validation, and exact narration binding adoption.
- Added upstream regression tests.

Incoming five commits applied:

`ff55850f`, `3754c661`, `2ed38b18`, `add1fff3`, `a9a3550c`.

Evidence:

- Local focused tests: `174 passed, 17 deselected`
- Central targeted runtime tests: `63 passed, 1 skipped, 48 deselected`
- `ruff check astrid/sdk/timeline_duplicate.py`: passed
- `git diff --check`: passed
- Prospective tree: `4b578bf70c0fb217ea80ad1f022f6bc3ef554c92`

The full touched-file Ruff check still reports pre-existing lint issues in `publish.py`, checkout tests, and restructure tests; none were introduced by the merge. No full/broad suite was run.

Wrote commit message and `DONE` marker at the requested paths.