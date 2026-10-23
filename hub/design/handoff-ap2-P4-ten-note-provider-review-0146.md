# P4 independent Luna review: ten-note provider

**Result: PASS**

Candidate: `e7385882ef50a59e6f62f32058fe211eb6e0b69f`  
Candidate tree: `6a838ae7b10334ffc0d62b3f876a62556a4e6621`  
Reviewed from: `/home/user/work/wt/ap2-P4-ten-note-provider-review-0146`  
Dependency reviewed: `5a313eb8` (joined G3/R2 handoff)

The candidate contains exactly one new file, `tests/sdk/test_p4_ten_note_provider.py`,
matching the only expected P4 delta. It uses the existing detached realm/port
and ABI fixture; it adds no source, fixture, schema, ABI stub, marker, skip,
xfail, launcher, or product report.

The test proves the requested provider slice: the ten fixture note texts and
IDs are used; all ten sequential inputs go through the real
`emit_document_commands`; each emitted change has the exact parent path and
absent-before birth; one production `RuntimeCommitService.commit` receives ten
distinct commands and ten ordered steps; each note is independently selected
for guarded inverse and then redone; nine-note preservation, mirrored clips,
opaque/null/absence/order and all other closure/document fields are compared;
stored original history remains unchanged. The ABA A→B→A refusal is checked for
no head/history/document partial acceptance. JSON reload is honestly limited
to an in-memory serialization round trip.

The actual production caller chain was inspected:

```text
Timeline._capture_free_edits
  -> astrid.sdk.timeline.emitter.emit_document_commands
  -> Timeline.commit / TimelineSession.submit
  -> TimelineSession._flush
  -> client.timelines.commit (Runtime commit route)
```

Therefore the provider/emitter path is used by the Python production caller.
The test itself remains direct-provider evidence only: detached/in-memory
acceptance is not official Runtime acceptance or HTTP/history proof.

Checks, all from the candidate worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p4_ten_note_provider.py tests/sdk/test_p4_commit_cases.py
PASS: 13 passed, 1 warning in 5.42s (unknown pytest `timeout` config option)

/root/.local/bin/ruff check tests/sdk/test_p4_ten_note_provider.py
PASS

/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p4_ten_note_provider.py
PASS

git diff --check
PASS
```

Remaining qualification boundaries are explicit: no official Runtime v2
ABI/wire proof (`api_version`/scope/base pair/commands/label/steps/merge/
optional reads/dry-run/`Idempotency-Key` and complete accepted/merged replies),
no durable Runtime history or restart proof, and no public CLI/sheet/App
journey. Owner source review, official wire/merge, and test-only import
approval remain required. This review gives no P4/H3 GO and does not authorize
wholesale merging of unlanded dependencies.
