# P4 rerun canonical-boundary return

Worker: `ap2-P4-rerun-canonical-return-0713`

Changed exactly one file:

- `tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`

Applied the independently reviewed ten-note canonical-boundary correction to
the post-restart rerun assertion. The ordinary restarted `timeline.open()`
must not expose provider-private `_runtime_document`; the test now performs
the existing authenticated exact revision/publication `open_bundle` read,
checks its identity/current-head metadata, and runs the unchanged full
physical/shared-closure oracle against that authenticated bundle. Existing
conflict, fresh callback evaluation, fresh key/base, request/reply, history,
receipt, restart, outbox, and preservation assertions remain intact. No
product, helper, fixture, synthetic cache/document, or other path changed.

Evidence:

- 2-test integration collection: PASS (`test_p4_note_rerun_v2_runtime.py` and
  `test_p4_ten_note_v2_runtime.py`); pytest emitted only the known unknown
  `timeout` config warning. Bodies were not run.
- Scoped Ruff on the changed file: PASS.
- Private scoped mypy on the changed file: PASS, no issues.
- Offline canonical-boundary structural proof: PASS.
- `git diff --check` and exact outside-file scope proof: PASS.

No HTTP/body/service/socket/browser/build/full/request suite was run, as
required. The central service should run the independent Luna rerun next,
followed separately by the original rerun node.
