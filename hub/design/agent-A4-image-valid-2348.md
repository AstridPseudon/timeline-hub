## Report: BLOCKED

Implemented the D18 fixture correction in [test-support/a4_image_witness.py](/home/user/work/wt/agt-A4-image-valid-2348/test-support/a4_image_witness.py):

- Preserved `visual.track.opaque == [null, false]` verbatim under supported `visual.track.app.opaque`.
- Applied via public `doc.patch`; accepted Runtime repair head:
  `authoring-parent-revision-0264057…`, publication `txn-fe0674…`.
- New input SHA: `8f665538…f7e0e0`.
- Original `e61c49fe…3b01d` remains immutable.
- Published input matched durable evidence byte-for-byte.
- No product/App/Runtime/schema/client/pin/guard edits.

Tests:

- `pytest -q tests/editing_conformance/test_a4_track_doc_patch_witness.py` — 9 passed.
- `ruff check test-support/a4_image_witness.py` — passed.
- `python3 -m py_compile ...` — passed.
- `git diff --check` — passed.

The unchanged qualified App producer produced no output by the 25-minute deadline (READY 23:50:52Z; timeout 00:15:49Z). Therefore no Runtime acceptance, retry, refusal, undo, or end-to-end PASS was claimed. Durable evidence is under the worker evidence directory (52 KB), and `BLOCKED` records the handoff.