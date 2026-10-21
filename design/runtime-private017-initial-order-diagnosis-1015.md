# Runtime PRIVATE017 initial namespace-order diagnosis

Date: 2026-10-21 UTC

## Disposition

The initial-order mismatch was a test-fixture premise error, not normal API
data loss. The unchanged seed commands create `config.app` in authored order,
but authoritative Runtime result/storage readback uses sorted-key canonical
JSON. The permitted setup-only correction makes the target namespace truly
middle in that authoritative order while retaining the canary target and all
semantic assertions. The one authorized ordered run then reached the body and
stopped at a separate first assertion: the normal Agent recorder enriches the
accepted command with capture fields, so the test's raw-command equality fails.
No remove, inverse, redo, or restart qualification is claimed.

## Exact order trace

1. The test builds `seed` in list order: before sibling, canary target,
   after sibling. `_commit()` sends that list unchanged in the normal
   `RuntimeService.commit_timeline()` request.
2. The Agent provider loads the accepted bootstrap through
   `RequestCommitPort.revision_closure()` and `bundle_from_document()`. The
   `project-data.write` handler applies the three commands sequentially;
   `ctx.object()` creates containers and `ctx.write()` inserts each leaf in
   that sequence. The in-memory authored map therefore has the seed order.
3. Agent `document_from_bundle()` passes the authored parent payload to the
   Runtime prepared commit. It does not sort `config.app` members; its
   canonical `_json()` is used for validation/digests.
4. Runtime acceptance validates the prepared document, then
   `_persist_closure()` stores the parent payload with Runtime
   `canonical_json()`. Runtime `util.canonical_json()` is
   `json.dumps(..., sort_keys=True, separators=...)`, so stored JSON member
   order is lexical. The receipt result is likewise canonicalized by the
   command ledger and reloaded by `_envelope()`; `revision_closure()` reloads
   the same canonical bytes.
5. Consequently the original literals read back as
   `after, before, com.example.compiler-canary`, exactly as run 30759
   reported. This is object-member textual order only: values, null/opaque
   content, and list order remain intact. The source contract documentation
   explicitly distinguishes semantic JSON/object equality from canonical
   sorted-key text; that distinction does not make the old middle-order
   fixture premise true.

## Permitted setup correction and assertion mapping

The canary target remains literal `com.example.compiler-canary`. Only its
lexical sibling bounds changed so canonical readback is target-middle:

| semantic role | old fixture key | new fixture key | affected assertions |
| --- | --- | --- | --- |
| before, `opaque_before` | `before` | `a-before` | initial map/order, removed map/order, recorded `insertion_order`, inverse restored order |
| ordered removal target | `com.example.compiler-canary` | unchanged | all remove command/path assertions |
| after, `opaque_after` | `after` | `z-after` | initial map/order, removed map/order, recorded `insertion_order`, inverse restored order |

The diff is confined to `tests/test_timeline_owned_reference_integration.py`
setup constants/seed literals and the corresponding literal expected maps and
orders. Null target value, opaque sibling values, target path, remove command,
receipt equality, no-duplicate/restart checks, inverse/redo checks, and every
other semantic assertion remain present. No expected order is derived from a
damaged result.

## Preflight

Exact source identities:

- Runtime worker tree under test: `ecdab2b4a10c4e9fbc4deb572f0382e54f3e6f00`,
  tree `176558a5abda7f53ee786e86f22a935f4e54b463`.
- Normal Agent: `6c1989adf723ae0ea0f4205c1cc8f1c0e4b22e79`, tree
  `cc0a8dd1360324a1b440ba7d318a083e7f8814cc`.
- Locked producer identity: Runtime `42a7203f49bb89f299ec854cfbf2b1444e815a7c`,
  tree `1f220b3d3a27e8eb061b15c944bad784c8fdb82e` (checked read-only through
  Git objects; the disposable producer worktree was not modified).

Read-only checks passed:

- Runtime artifact manifest: 76 entries, version
  `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- Agent lock: 15 entries; all 15 current Agent bytes equal the locked
  Runtime42a producer blobs.
- Schema raw SHA-256
  `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`,
  canonical SHA-256
  `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`,
  65 definitions and 37 `EditCommand.allOf` clauses.
- Client contract version `0.2.17`, schema digest
  `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`,
  imports resolved from this Runtime worker and the exact Agent checkout, and
  Astrid provider profile loaded.
- `venv-agent` resolved pytest/jsonschema/referencing/filelock/Pillow/PyYAML;
  shared worktrees/venv/node_modules were only read, with direct realpaths.
- Temporary directory create/remove and disk checks passed (`10,573,576 KiB`
  available on both `/home/user/work` and `/tmp`).
- Syntax and `git diff --check` passed.

Fixture closure and collection command:

```text
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --collect-only -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo
```

Result: `1 test collected`. The no-body setup plan resolved
`tmp_path_factory -> tmp_path -> film` and
`monkeypatch -> astrid_importable`; `film, astrid_importable, monkeypatch ->
agent`. The two-node combined collection also collected 2 tests, with no
semantic body execution.

## Authorized proof result

Exactly one central request was made, after the corrected setup and complete
preflight:

```text
rt-m2-private017-initial-order-diagnosis-1015-private017-agent6c-integration-1021101825-7616
```

Exact command:

```text
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6c1989ad PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-6c1989ad" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_owned_reference_integration.py::test_actual_provider_removes_ordered_project_data_and_retries_inverse_redo
```

Result: `1 failed in 1.51s`, first failure at line 284:

```text
assert record["command"] == remove
```

The accepted record contains the normal Agent-generated capture fields,
including `authorship`, `bindings`, `created`, `reads`, `selections`, and
`expect`, while `remove` is the raw input command. This is a recorder-shape
assertion mismatch, not a namespace-order or data-loss witness. Per the task
stop rule, no automatic retry and no second node were run. The target's
remove/restart/exact-retry/inverse/redo assertions were not reached and have
no product outcome from this run.

## Next step

The Runtime/Agent source owners should decide how the existing recorder
assertion is intended to compare the raw command with the authoritative
captured command. Any follow-up must be separately authorized and must retain
the full recorder fields and all downstream remove/restart/inverse/redo
assertions. No immutable42a source, schema, artifact, pin, or product code
was changed.
