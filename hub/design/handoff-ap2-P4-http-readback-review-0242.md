# P4 HTTP readback independent review

## PASS — source readiness only

Independent review of `ddff86c18` against `b9a640b5d` passed. Exactly one new test file changed. It preserves the original authored `initial_bundle()` parent, performs the real sheet edit `parent/clip:a` `0 -> 5`, seeds only Runtime's required empty canonical `occurrences` container, and checks unchanged sibling/config/placement/shot/source claims while excluding only the derived `_runtime_document` wrapper from source-mapping equality.

The production caller is traced through the real CLI parser, `NativeSheet`, `TimelineSession` outbox, generated transport, `RuntimeHandler`/provider, and back through CLI `show` and `history`. The existing runtime fixture's `runtime.calls` observer records actual HTTP commit request/response traffic; it is not an acceptance fake. Submitted semantic `steps[].patch=[]` is valid; accepted/history authoritative step metadata is checked for presence and round-trip identity.

Checks passed:

- integration collection: exactly 1 test collected;
- Ruff;
- mypy;
- `git diff --check`.

No socket body was run. The current Agent lock still names old Runtime client source `27f0306b94d136d25f237edf4b8225b5d8487be0`, so this is not a wire qualification. After official normal U4a client adoption and compatible Runtime source import, run:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-P4-http-readback-review-0242 targeted --files "tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Do not merge or claim wire PASS before that body passes on the compatible owner source. Conflict/invalid/preview, ten-note undo, rerun, and other P4 wire qualifications remain open.
