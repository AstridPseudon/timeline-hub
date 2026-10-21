# WC8 detached-sheet slice report

## Status

BLOCKED: no bounded migration exists for the remaining legacy detached-sheet
consumer on base `cc37291af12ac6504eb48dd71ea39b9dfdb56d71` without adding a
new carrier or changing the documented local behavior.

## Product/test diff

No product or test files were changed.

The required existing detached positive remains:

`tests/sdk/test_timeline_sheet.py::test_a_fragment_touches_only_its_cuts_and_a_new_line_adds_a_layer`

The relevant native guard remains:

`tests/sdk/test_timeline_sheet_native.py::test_native_rows_cannot_fall_into_the_legacy_sheet_writer`

The connected CLI consumer is already routed through
`commit_edit(parsed, sheet=True)` and `NativeSheet`/`TimelineSession` in the
current base. The remaining no-client caller is:

`astrid/packs/timeline/cli.py:_cmd_apply` →
`astrid/sdk/timeline_sheet.py:apply_sheet` → `merge_sheet` (for an old sheet) →
`_apply_parsed` → `Checkout.save`.

## Bounded blocker

The detached sheet exports only a whole-document short `v` digest and an
optional local `_exported` snapshot. It does not retain the native
revision/publication basis, stable `# ref` row bindings, captured read/order
claims, created IDs, or a durable Runtime/outbox target at authoring time.

The existing `NativeSheet` entrypoint explicitly rejects legacy `lines`,
`sound`, cut/layer, and mixed rows. The documented positive above also adds a
new layer from a fragment, which cannot be represented by the existing native
row commands. Routing it through `NativeSheet` would therefore require a
whole-snapshot diff writer, fresh submit-time guard capture, a new carrier, or
refusing/narrowing a passing local behavior. Each is outside the settled WC8
scope.

Local-only detached edits consequently remain local. No duplicate merge
consumer was deleted because the live caller is still required for its
documented grammar and rollback/three-way behavior.

## Verification

```text
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet.py::test_a_fragment_touches_only_its_cuts_and_a_new_line_adds_a_layer tests/sdk/test_timeline_sheet_native.py::test_native_rows_cannot_fall_into_the_legacy_sheet_writer
```

Result: **2 passed in 0.92s**.

```text
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet_native.py tests/packs/timeline/test_cli_native_sheet.py tests/sdk/test_timeline_sheet.py tests/packs/timeline/test_verbs_working_copy.py
```

Result: **122 passed in 20.80s**.

No full, browser, renderer, or live-socket suite was run. No Runtime source,
store/DTO/op, schema/generated/pin, or other worktree was modified.

## Recommended next step

Reopen this slice only when an existing authoring entrypoint supplies the
native bundle/publication basis, stable row bindings, and explicit Runtime
outbox target before mutation. Then reuse `NativeSheet.preview/apply` for one
supported row family, qualify exact retry/conflict/rebase/inverse behavior,
and delete only that family’s duplicate detached consumer.
