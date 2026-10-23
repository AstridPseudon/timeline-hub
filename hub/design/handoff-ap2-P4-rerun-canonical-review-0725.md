# P4 rerun canonical review — handoff

**PASS / FAIL:** source and scope PASS; live rerun readiness FAIL/not ready.

Reviewed source `dd0bd73e2cef92cdca8213d26e175e350b484af6` (tree
`e762ea942c4139b97f782a1882e7de3453b42cb8`) to branch
`cd585ac2304706d7bb5b039846d86cd1543d468f` (tree
`4e9911074ad97cb47b5c46402bf1e2c99a04754d`). Exactly one tracked path changed:
`tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`.

Rerun blob is `cbd332db227ecb9c6254e8ced0af72c3de91821e` →
`72d11a2a8f9f8915a22e325bc15f2edadbae96ff`; it exactly matches reviewed
correction `14562a66e57d9b658a6fcdd0979403997e56d60b`. Ten-note blob remains
`b8876628d100897a9dcda6750fc5395a3b5b41f3`.

The ordinary restarted `timeline.open()` still proves public cache absence.
The existing authenticated exact revision/publication `open_bundle` read is
then used for canonical closure, with exact project/timeline/revision/current-
head and parent binding checks and public-vs-authenticated bundle equality.
Original peer/conflict/bounded-rerun, exact request/keys/reply, digest,
authoritative history/receipt/readback, physical ONE shared closure,
source-mapping, opaque/null/absence, restart and outbox assertions remain;
the ten-note show/history and per-step undo/redo neighbor is byte-identical.
No synthetic cache/document, fixture change, product edit, loosened assertion,
or detached HTTP path was introduced.

Evidence passed:

- exact two-test collection: 2 collected; only known unknown-`timeout` warning;
- scoped Ruff: PASS;
- private-cache scoped mypy: PASS, no issues in 2 files;
- `git diff --check`: PASS;
- outside-file diff/blob equality: PASS;
- only the rerun test changed; ten-note blob unchanged.

No HTTP/body/socket/service/browser/build/full/request run was made. This is
source qualification only.

Operational boundary: the actual original ten-note node currently fails at
the first `opened.command` in production `command_session → _doc_patch →
commit.py:304` because the ordinary public bundle lacks
`source_mapping["_runtime_document"]`. Sol readonly-0722 and Agent peer-0723
own that defect. Do not claim the rerun ready or run live bodies until that
source seam is corrected and independently reviewed; then run the original
ten-note and rerun nodes separately.
