# RT03 foreign raw-refusal oracle

Date: 2026-10-21 UTC

## Change

Changed only `tests/test_timeline_owned_reference_integration.py:230`:
the foreign raw-object refusal now asserts the exact status `404`, with a
comment preserving the non-disclosing contract. The existing raw-media message
check and SQLite no-write assertion are unchanged. No Runtime source, schema,
generated artifact, lock, metadata, or other test bytes changed.

## One-to-one source mapping

The foreign fixture creates the raw object under `foreign` but submits the
commit under `project` (`tests/test_timeline_owned_reference_integration.py:220-227`).
The private capture path calls `MediaReads.raw_media_info` for the request
project (`runtime_protocol/timeline_commit_port.py:277-296`). Its concrete
membership query joins `objects` to `project_objects` with the request
`project_id` and `relation='managed'` (`runtime_protocol/timeline_commit_port.py:908-913`);
the foreign object therefore has no matching row and raises
`NotFoundError("raw media is not a managed project object")`
(`runtime_protocol/timeline_commit_port.py:914-920`). `NotFoundError` maps
one-to-one to status 404 (`runtime_protocol/errors.py:45-48`). This refuses
without revealing foreign ownership and does not broaden raw access.

The mapping agrees with current Main's non-disclosing project-scope behavior:
foreign project-scoped reads use `NotFoundError` (`tests/test_timeline_commit_read_basis.py:248-253`),
and authenticated foreign reference/shot resources use exact 404/not_found
(`tests/test_timeline_authority_door.py:104-113`).

## Verification

Static conversion review, run locally:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B -m py_compile runtime_protocol/timeline_commit_port.py tests/test_timeline_owned_reference_integration.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B - <<'PY' ... AST/source-oracle assertions ... PY
git diff --check
```

Result: **PASS**. Both files parsed; the exact source mapping and exact 404
assertion were found; no bytecode remained in the worktree.

Required single RT03 run through the central test service:

```text
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_preserves_original_owned_unplaced_reference_contract
```

Result: **1 passed in 1.42s** (central run exit 0). This run reached and
passed the foreign 404 refusal, and also passed the first test's positive,
no-placement, role/id/receipt, restart retry, changed-payload, invalid-role,
occupied, inverse, and closure assertions.

## Static review of the remaining unexecuted sibling

The ordered project-data sibling was not run, per the task boundary. Against
the actual Agent6c/Runtime42a source, no concrete defect was found:

- Agent6c records the pre-removal `config.app` key order when clearing the
  namespace (`astrid/sdk/timeline/_project_data_commands.py:111-128`).
- Agent6c inverse restoration passes the recorded `insertion_order` and
  rejects order drift before reinsertion (`astrid/sdk/timeline/inverse.py:70-82`;
  `astrid/sdk/timeline/_command_state.py:564-584`).
- Runtime validates undo targets in acceptance order and verifies the restored
  revision closure/digest before persistence (`runtime_protocol/timeline_commit_store.py:607-615`;
  `runtime_protocol/timeline_commit_store.py:324-355`).

The ordered inverse body remains Agent-owned peer1034; it was not duplicated,
run, or patched here. No source contradiction or custody issue was found.

## Limits and next step

No full suite, target body beyond the one authorized RT03 test, HTTP/socket,
browser, renderer, install, generation, schema, pin, or sibling run was done.
The harness can integrate this test-only oracle correction. Any ordered
inverse qualification remains with peer1034 and requires its own authorization.
