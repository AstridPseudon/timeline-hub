## Report

- Retained valid WIP unchanged; fixture matches donor `7c7170…` byte-for-byte.
- Only changed path: `tests/editing_conformance/native_word_anchor_fixture.py`.
- Verified normal `occurrence_id:occ`, ordered steps, FPS corrections, full C0 request fields, and protected recipe/test blobs.
- Created `commit-msg` and `DONE`.

Checks passed:

- `python3 -m py_compile …/native_word_anchor_fixture.py`
- AST/source invariants
- Donor/hash comparison
- Protected blob hash comparison
- `git diff --check`
- Production caller/provider/runtime census

No pytest/full/body tests run per brief. Product remains HELD; seed behavior is still an explicit dependency.