Implemented the c17 helper-closure cleanup.

- Relocated `_media_kind` to `_common.py`; preserved `edits._media_kind` compatibility.
- Removed native split’s lazy `edits` import.
- Restored `model.py` formatting while retaining source-unit hold semantics.
- Added fresh-interpreter MIME move→split import fence.

Tests:

- Targeted split/trim/provider: **172 passed**
- Adjacent checkout/helper tests: **110 passed, 17 deselected**
- `git diff --check`: passed
- Ruff: existing baseline `I001` findings only; no broad cleanup applied.

Reports and messages:

- [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-literal-helper-closure/notes/report.md)
- `commit-msg` and `commit-msg.txt` written at the worker path.

No full suite, install, network, browser, merge, or artifact-pin runs were performed.