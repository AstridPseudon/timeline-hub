# P4 HTTP readback independent review

## PASS — source readiness only

Independent review of `ddff86c18` against `b9a640b5d` passed. Exactly one new test file changed. It preserves the original authored `initial_bundle()` parent, performs the real sheet edit `parent/clip:a` `0 -> 5`, seeds only Runtime's required empty canonical `occurrences` container, and checks unchanged sibling/config/placement/shot/source claims while excluding only the derived `_runtime_document` wrapper from source-mapping equality.

The production caller is traced through the real CLI parser, `NativeSheet`, `TimelineSession` outbox, generated transport, `RuntimeHandler`/provider, and back through CLI `show` and `history`. The existing runtime fixture's `runtime.calls` observer records actual HTTP commit request/response traffic; it is not an acceptance fake. Submitted semantic `steps[].patch=[]` is valid; accepted/history authoritative step metadata is checked for presence and round-trip identity.

Checks passed:

- integration collection: exactly 1 test collected;
- Ruff;
- mypy;
- `git diff --check`.

No socket body was run. The current Agent lock still names old Runtime client source `27f0306b94d136d25f237edf4b8225b5d8487be0`, so this is not a wire qualification. After official normal U4a client adoption and compatible Runtime source import, run on the future compatible owner-join worker (replace `OWNER_JOIN_WORKER` with that worker's actual name; do not use this old review worker or a recycled author path):

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test OWNER_JOIN_WORKER targeted --files '-m integration tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back') && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The service's resulting pytest command is exactly:

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back
```

The explicit integration selector is required: the Agent default `addopts` deselects integration tests, and the same command without `-m integration` collected zero tests and exited 5 in the source-readiness check. The actual body remains deferred until the compatible owner join supplies the corrected official client and matching Runtime checkout.

Do not merge or claim wire PASS before that body passes on the compatible owner source. Conflict/invalid/preview, ten-note undo, rerun, and other P4 wire qualifications remain open.
