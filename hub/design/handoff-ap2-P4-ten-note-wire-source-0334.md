# P4 ten-note wire source handoff

Source file: `tests/editing_conformance/test_p4_ten_note_v2_runtime.py`

This is source readiness only. The test was collected as exactly one positive
integration node and passed scoped Ruff, mypy, and `git diff --check`. The HTTP
body was not run on held Runtime `rt-pin-780da6d6`; this handoff does not claim
P4/H3 acceptance.

## Later one-node command

After the new strict-envelope producer is normally adopted, compatible G3/R2
is joined with canonical d106 restored, and the existing `p4-v2-http-nodes`
service is pointed at that compatible Runtime checkout, run the exact node via
the existing suite (replace the owner placeholder with the actual compatible
owner-join worker):

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test OWNER_JOIN_WORKER p4-v2-http-nodes --files tests/editing_conformance/test_p4_ten_note_v2_runtime.py::test_http_ten_note_commit_per_step_inverse_and_redo) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

## Source identity and call trace

The authored source is the original `ten-notes-one-commit` case in
`tests/sdk/fixtures/p4_commit_cases/cases.json`, using the shared
`tests/sdk/test_timeline_commit_provider_document.py::document_fixture`.
The test creates the permitted isolated genesis boundary
`app.org.example.p4_note = {}` on `clip-a`; the ten note keys are still absent
and are set one at a time. The source retains the original two shared sibling
placements, `clip-b`, ordering, explicit null, opaque values, and child
closure.

Production path:

```text
timeline.open()
  -> Timeline.command() x10
  -> G3 emit_document_commands()
  -> Timeline.commit()
  -> TimelineSession.submit/_flush()
  -> generated client commit route
  -> Runtime HTTP handler/coordinator/provider
  -> canonical reply and CLI show/history readback

TimelineSession.undo(..., steps={publication: [step-id]})
  -> timeline.inverse over the same generated commit route
  -> inverse-of-inverse for redo
```

The one forward call is explicitly checked as ten `doc.patch` commands and ten
ordered steps, with `fields`, `reads: []`, base revision/publication pins,
idempotency key, and `dry_run: false`. Accepted data/history checks cover the
canonical document, digest, accepted/previous pins, commands, empty `id_map`,
authoritative steps/dependencies, merge mode, publisher, provider/compiler
metadata, receipt, and CLI readback. Each selected inverse checks the exact
step selector, target-note removal, preservation of the other nine notes and
the non-note closure, then redo restores the ten-note state.

## Open limitations

- No HTTP/socket/body execution was performed in this source-preparation task.
- The body must wait for strict-envelope normal producer adoption, compatible
  current G3/R2, and canonical d106 restoration; the current pre-adoption
  client signature lacks the v2 `steps` selector, so the source uses a narrow
  `Any` cast at that call boundary.
- Conflict/merged landing, invalid structured errors, preview `would_status`,
  lost-ACK exact retry, and bounded `timeline.open().commit(fn)` rerun are
  separate open coverage; no variants are invented or claimed here.
- No full, browser, live-socket, or heavy suite was run.

