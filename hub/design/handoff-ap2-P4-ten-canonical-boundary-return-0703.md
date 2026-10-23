# P4 ten-note canonical-boundary return

Worker: `ap2-P4-ten-canonical-boundary-return-0703`

Changed only:

- `/home/user/work/wt/ap2-P4-ten-canonical-boundary-return-0703/tests/editing_conformance/test_p4_ten_note_v2_runtime.py`

Diagnosis: the failing `_runtime_document` lookup was a wrong test oracle at
the public `timeline.open()` boundary. Ordinary revision reads intentionally
strip this provider-only immutable closure annotation. The remote facade
retains it only for an authenticated exact revision/publication pair after
history receipt and canonical closure equality checks. The test now uses the
seeded receipt's exact base pair for the full physical canonical assertions,
while asserting absence on ordinary initial and post-restart reads.

Preserved: public physical placement/working-alias source mapping assertions;
all physical/shared source images, occurrences, opaque values, media pins,
dependency manifest and content digests; ten doc.patch commands and steps;
request scope/base pair/label/reads/merge/dry-run/idempotency; accepted
canonical document, digest, publication/head and receipt checks; show/history,
restart, and every per-step undo/redo assertion. No product/helper/fixture/
rerun/schema/generated/pin/launcher/suite files changed.

Evidence: exact collection of the ten-note and rerun nodes collected 2;
scoped Ruff PASS; private-cache mypy PASS; offline canonical round-trip
witness PASS; diff/scope PASS. No live HTTP/service/body/socket/full run was
made under this task's explicit limit, so the final test body remains for the
central service on the integrated tree.
