# Runtime PRIVATE017 ordered oracle contract correction

Date: 2026-10-21 UTC

## Disposition

The remaining ordered failure is conclusively a test-oracle wiring defect. The
test compared the accepted record's normal, enriched command to the raw remove
request. The bounded correction compares that field to the complete command
produced by the existing Agent recorder from the accepted pre-remove document.
No product source, schema, artifact, lock, pin, body, guard, submitted command,
or downstream assertion was changed. The ordered test body was not run after
the correction; no remove, restart/retry, inverse, or redo qualification is
claimed.

The two accidental process documents previously at Runtime `report.md` and
`design/runtime-private017-initial-order-diagnosis-1015.md` were copied byte
for byte to both required ORCH destinations before being deleted from this
branch. Their hashes were verified before deletion.

## Exact source-contract audit

The command path was traced from the ordered test through the accepted record:

1. `_commit()` submits `remove_body`, whose only command is the raw
   `project-data.write` remove command.
2. Agent `RuntimeCommitService.commit()` loads the exact base closure, then
   calls the existing `astrid.sdk.timeline.commands.execute()` entrypoint.
3. `Recording.finish(capture=True)` preserves the raw operation and adds the
   recorder-owned capture fields: `intent`, `resolved`, `reads`,
   `selections`, `bindings`, `created`, `expect`, and `authorship`.
4. Runtime `TimelineCommitStore._publish()` persists the complete records
   object in `timeline_commit_history.records_json` using canonical JSON.
5. Runtime `_envelope()` reconstructs the accepted `data.commands` from the
   persisted record commands; `list_timeline_commits()` returns the same
   accepted records. Exact retry returns this stored envelope without calling
   the Agent provider.

The raw remove command therefore cannot equal the normal accepted record
command. The independent pure recorder probe produced this exact authoritative
command for the ordered target:

```json
{"args":{"key":"gone","mode":"remove","target":"com.example.compiler-canary"},"authorship":{"parent::config.app[\"com.example.compiler-canary\"]":"direct","parent::config.app[\"com.example.compiler-canary\"].gone":"direct"},"bindings":{},"created":[],"expect":{"parent::config.app[\"com.example.compiler-canary\"]":{"state":"present","value":{"gone":null}},"parent::config.app[\"com.example.compiler-canary\"].gone":{"state":"present","value":null}},"intent":{},"op":"project-data.write","reads":[],"resolved":[],"schema_version":1,"select":"parent","selections":[],"version":"1"}
```

The new helper calls `agent.bundle(document)` and Agent `execute()` on the
accepted `original` seed document plus a deep copy of the unchanged raw remove
command. It returns `plan.records[0]["command"]`, a dict containing the full
authoritative capture. It does not inspect or transform the result under test,
derive a subset, strip metadata, loosen equality, or write a normalized
fixture. The expected command is generated from the pre-remove accepted
closure, independently of the remove acceptance result.

## One-to-one assertion mapping

| Existing assertion | Contract authority | Disposition |
| --- | --- | --- |
| `accepted["receipt"]["result"] == accepted["data"]` | Runtime accepted envelope/receipt replay | unchanged |
| Removed `config.app` map and key order | Agent authored document plus Runtime canonical closure | unchanged; target remains absent and siblings remain `a-before`, `z-after` |
| `record["command"]` | Agent normal capture, persisted verbatim by Runtime | corrected only from raw `remove` equality to complete `_authoritative_recorded_command(agent, original, remove)` equality |
| Two exact `writes` entries | Agent recorder writes: leaf clear, then empty namespace clear; second write carries full `insertion_order` | unchanged, including null-before and absent-after states |
| Restart exact retry returns `accepted` | Runtime idempotency ledger/envelope | unchanged |
| Provider execution tripwire on retry | Runtime exact retry must not call Agent | unchanged |
| SQLite dump and history unchanged on retry | Runtime idempotency has no duplicate durable write | unchanged |
| Inverse restores the exact original app map and order | Authenticated accepted record/inverse machinery | unchanged |
| Restored payload equals original payload | Complete canonical document contract | unchanged |
| Redo matches removed map/order and payload | Authenticated inverse of the accepted inverse | unchanged |

The fixture still preserves the null target value, opaque sibling values,
absence after removal, complete canonical document, exact receipt replay,
insertion order, no duplicate SQL/history, and strict inverse/redo equality.

## Changes

Only `tests/test_timeline_owned_reference_integration.py` was product-edited:

```diff
 def _authoritative_recorded_command(agent, document, command):
     from astrid.sdk.timeline.commands import execute
     plan = execute(agent.bundle(document), [copy.deepcopy(command)])
     return plan.records[0]["command"]
 
-assert record["command"] == remove
+assert record["command"] == _authoritative_recorded_command(agent, original, remove)
```

The prior lexical fixture correction remains unchanged. No assertion was
deleted or weakened, no marker/xfail was added, and no RT03 hunk was touched.

## Independent pre-execution review and cheap checks

The exact assertion conversion was reviewed against the Agent recorder,
Runtime prepared-record validation, Runtime persistence, and Runtime envelope
replay before any ordered test-body execution. The pure probe used
`empty_bootstrap_document`, `bundle_from_document`, `execute`, and
`document_from_bundle` only; it printed the complete command above and passed.

Checks completed:

```text
PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B <pure source/recorder probe>
  -> PASS; complete expected command printed above

PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B <AST parse>
  -> PASS

git diff --check
  -> PASS
```

No target body, full suite, HTTP/socket, browser, renderer, install,
generation, or old passing lane was run.

## Proposed fresh preflight for the independent manager

Before any future body execution, independently re-check the exact normal
tuple and source identities from the prior diagnosis: Runtime42a/Agent6c,
public014 unchanged, current Runtime tree including this bounded test-only
correction, Agent imports resolved from the exact pinned checkout, all 76
producer artifacts and 15 lock entries, schema raw/canonical digests and
contract version, Astrid provider profile, shared dependency realpaths/read
only state, `PYTHONDONTWRITEBYTECODE=1`, private temp/disk headroom, syntax and
`git diff --check`.

Then use collection/setup only first:

```text
env ASTRID_RUNTIME_CHECKOUT="$PWD" \
    ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad \
    PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" \
    PYTHONDONTWRITEBYTECODE=1 \
    /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
    --collect-only -m integration \
    tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo
```

The next decision and any body run belong to the independent manager. This
worker makes no qualification, adoption, merge, or private-proof claim.

