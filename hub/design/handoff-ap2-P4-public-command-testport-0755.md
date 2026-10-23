# P4 public command test port — handoff

**Source qualification: PASS. Live body: NOT READY.**

Base `68d54e15a8d217634045b6dcc0acb719fd93c4aa` (tree `6ba7770dac3843b4d24d933521893277139d5ba1`) received only the two final original HTTP test files from donor `tl/ap2-P4-rerun-canonical-boundary-0717` at `cd585ac2304706d7bb5b039846d86cd1543d468f` (tree `4e9911074ad97cb47b5c46402bf1e2c99a04754d`):

- `tests/editing_conformance/test_p4_ten_note_v2_runtime.py` — exact blob `b8876628d100897a9dcda6750fc5395a3b5b41f3`.
- `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py` — exact blob `72d11a2a8f9f8915a22e325bc15f2edadbae96ff`; reviewed correction commit `14562a66e57d9b658a6fcdd0979403997e56d60a).

Independent review `tl/ap2-P4-rerun-canonical-review-0725` passed source/scope qualification and retained all original canonical closure, cache-boundary, request/reply, conflict/peer/bounded-rerun, undo/redo, history/show/readback, exact bytes/key, restart/outbox, opaque/null/absence, digest, dependency, and source-mapping assertions. It records live readiness FAIL/not ready because the production public command path reaches `commit.py:304` without `source_mapping["_runtime_document"]`.

Exact evidence commands and outcomes are in `WORKERreport.md`. Collection found 2 tests; Ruff, private-cache mypy, diff check, outside-target equality, and exact donor blob checks passed. No HTTP/socket/service/browser/full/build/request run was made.

Source-vs-body limit: `timeline/store.py:open` and `timeline/commit_session.py:_execution_bundle` show the intended public open → exact authenticated canonical hydration → existing provider/Runtime path; `timeline/_remote_timeline.py:open_bundle` is the existing exact-pair hydrator. This is source evidence only, not behavioral PASS. Live body waits for Agent owner0744 PASS and operational exact existing service-row review.

Next: after that source seam is corrected and independently reviewed, run the original ten-note and original rerun nodes separately. Do not add a synthetic cache or alter the tests.

