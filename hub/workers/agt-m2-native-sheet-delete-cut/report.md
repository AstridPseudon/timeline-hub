Implemented bounded native clip-row deletion.

- Omitted bound `parent/clip:<id>` rows emit existing guarded `clip.delete` through `TimelineSession`/outbox.
- Track, occurrence, added, rebound, or unsupported rows still refuse safely.
- Added SDK and native CLI coverage for preservation, retry, undo/redo, rebase, and membership conflict.

Tests:

`PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider ...`  
Result: **120 passed**

Central HTTP attempt: **9 integration tests deselected**; no suitable named Agent lane exists, so HTTP integration remains unverified. No full suite run.

Artifacts written:

- Design: `/tmp/.../design/agent-native-sheet-delete-cut.md`
- Commit message: `/tmp/.../workers/agt-m2-native-sheet-delete-cut/commit-msg`
- Completion marker: `/tmp/.../workers/agt-m2-native-sheet-delete-cut/DONE`