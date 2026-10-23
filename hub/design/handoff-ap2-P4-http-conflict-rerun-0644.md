# Handoff — P4 real-HTTP note-04 conflict/rerun

Worker `ap2-P4-http-conflict-rerun-0644` prepared the single permitted new
source file:

`tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`

Readiness is **PASS / source-ready only**. The test uses the existing real
daemon/generated HTTP fixture and public `timeline.open` → `tl.commit(fn)` API.
It seeds the nine other note values through a public setup commit, makes the
peer note-04 commit inside callback evaluation one, asserts the real 409/current
pair/no-write boundary, and asserts exactly two callback evaluations with a
fresh retry key/base and absent→present guards. It retains the reviewed seed,
full shared closure, null/opaque/authoring-preservation, canonical digest and
history/receipt/step/binding/dependency assertions, and restart readback.

Static evidence:

- exact collection: 1 test;
- scoped Ruff: PASS;
- private mypy: PASS;
- whitespace diff check: PASS;
- no tracked changes outside the new file; original ten-note test, fake SDK
  rerun test, and fixture unchanged.

No HTTP/body/socket/service/full run or service request was made. Manager must
obtain independent review, then run the bounded body after the reviewed Runtime
correction. No product/helper/generated/schema/pin/fixture changes are needed.
